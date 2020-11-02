FROM python:3-alpine
COPY ./app /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install pymysql


CMD ["python", "app.py"]