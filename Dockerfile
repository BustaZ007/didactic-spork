FROM python:3-buster
COPY ./app /apps/app
WORKDIR /apps
RUN pip install -r app/requirements.txt
RUN pip install pymysql

RUN apt-get update
RUN apt-get -y install build-essential libssl-dev libffi-dev python-dev
RUN pip install cryptography


CMD ["python", "app/app.py"]