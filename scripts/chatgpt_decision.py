# chatgpt-meme-coin-experiment

# Requirements (to be saved in requirements.txt)
# openai==1.10.0
# requests==2.31.0
# pyyaml==6.0.1

import os
import json
from datetime import datetime
import yaml
import openai
import requests

# === Load Configuration ===
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

COINS = config["coins"]
VS_CURRENCY = config.get("vs_currency", "usd")
MODEL = config.get("openai_model", "gpt-4")
PROMPT_FILE = config.get("prompt_file", "prompts/coin_analysis.txt")

DATA_DIR = "data"
LOG_FILE = f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"
PORTFOLIO_FILE = f"{DATA_DIR}/portfolio.csv"
MARKET_DATA_FILE = f"{DATA_DIR}/market_data.json"

# Use OpenAI GPT-4 (requires OPENAI_API_KEY env var)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Ensure dirs exist
os.makedirs("logs", exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)


# === Step 1: Fetch market data ===
def fetch_market_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": VS_CURRENCY,
        "ids": ",".join(COINS),
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": False,
    }
    response = requests.get(url, params=params, timeout=5)
    data = response.json()
    with open(MARKET_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return data


# === Step 2: Format prompt for GPT ===
def create_prompt(market_data):
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        prompt = f.read().strip()
    prompt += "\n\nVoici les données :"
    for coin in market_data:
        prompt += (
            f"\n{coin['name'].upper()} ({coin['symbol'].upper()}): prix ${coin['current_price']},"
            f" volume 24h ${coin['total_volume']},"
            f"variation 24h {coin['price_change_percentage_24h']}%,"
            f" market cap ${coin['market_cap']}"
        )
    return prompt


# === Step 3: Ask ChatGPT ===
def ask_chatgpt(prompt):
    response = openai.chat.completions.create(
        model=MODEL, messages=[{"role": "user", "content": prompt}], temperature=0.7
    )
    return response.choices[0].message.content


# === Step 4: Log result ===
def log_decision(content):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}]\n{content}\n\n")


# === Step 5: Update simulated portfolio ===
def update_portfolio(recommendation_text, market_data):
    portfolio = {}
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                coin, quantity = line.strip().split(",")
                portfolio[coin] = float(quantity)

    lines = recommendation_text.strip().split("\n")
    coin_prices = {c["name"].upper(): c["current_price"] for c in market_data}

    for line in lines:
        if ":" in line and " - " in line:
            coin, decision = line.split(":")
            coin = coin.strip().upper()
            action = decision.split(" - ")[0].strip().upper()
            price = coin_prices.get(coin, 0)

            amount_usd = 10
            quantity = round(amount_usd / price, 6) if price else 0

            if action == "ACHETER":
                portfolio[coin] = portfolio.get(coin, 0) + quantity
            elif action == "VENDRE":
                portfolio[coin] = max(portfolio.get(coin, 0) - quantity, 0)

    with open(PORTFOLIO_FILE, "w", encoding="utf-8") as f:
        f.write("coin,quantity\n")
        for coin, quantity in portfolio.items():
            f.write(f"{coin},{quantity}\n")


# === MAIN RUN ===
def main():
    print("Fetching market data...")
    market_data = fetch_market_data()

    print("Creating prompt for ChatGPT...")
    prompt = create_prompt(market_data)

    print("Querying ChatGPT...")
    result = ask_chatgpt(prompt)

    print("Logging result...")
    log_decision(result)

    print("Updating simulated portfolio...")
    update_portfolio(result, market_data)

    print("✅ Decision logged and portfolio updated.")


if __name__ == "__main__":
    main()
