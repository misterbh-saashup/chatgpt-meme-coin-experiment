FROM python:3.13

WORKDIR /usr/src/app

COPY requirements.txt ./requirements.txt
COPY config.yaml ./config.yaml
COPY data ./data
COPY logs ./logs
COPY prompts ./prompts
COPY scripts ./scripts

RUN pip install -r requirements.txt

CMD ["python3", "./scripts/chatgpt_decision.py"]
