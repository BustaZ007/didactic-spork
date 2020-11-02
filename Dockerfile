FROM python:3-buster
COPY ./app /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install pymysql

RUN apt-get update
RUN apt-get -y install build-essential libssl-dev libffi-dev python-dev
RUN pip install cryptography


CMD ["python", "app.py"]