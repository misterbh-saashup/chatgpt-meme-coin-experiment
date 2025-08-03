# 🧠 ChatGPT Meme Coin Experiment

Ce projet est une simulation de trading sur les 10 meme coins les plus populaires en utilisant l'intelligence artificielle (ChatGPT). L'objectif est de tester si l'IA peut prendre de bonnes décisions sur des actifs ultra-volatils comme PEPE, WIF, DOGE ou MOG.

## 🚀 Fonctionnement

Chaque heure :
- Le script récupère les données de marché via l'API CoinGecko.
- Il génère un prompt à destination de ChatGPT-4.
- Il reçoit une décision pour chaque coin (ACHETER / VENDRE / CONSERVER).
- Il loggue la réponse dans un fichier `logs/YYYY-MM-DD.log`.

## 🛠️ Installation

```bash
git clone https://github.com/misterbh-saashup/chatgpt-meme-coin-experiment.git
cd chatgpt-meme-coin-experiment
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
