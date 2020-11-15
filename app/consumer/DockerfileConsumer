FROM python:latest

WORKDIR usr/src/app

RUN python -m pip install pika
RUN python -m pip install requests

CMD ["python", "consumer.py"]

COPY . .