import pika
import requests
import json
import redis
from datetime import timedelta

credentials = pika.PlainCredentials('user', 'user')
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit', 5672, '/', credentials))

channel = connection.channel()

channel.queue_declare(queue='app_que', durable=True)
channel.exchange_declare(exchange='app_que_ex', exchange_type='fanout')

channel.queue_bind(exchange='app_que_ex', queue='app_que')

redis_connection = redis.Redis(host='redis', port=6379, db=0)

def callback(ch, method, properties, body):
    status = ''
    json_body = json.loads(body.decode())
    link_url = json_body['link_url']
    cache_value = redis_connection.get(link_url)
    if(cache_value == None):
        try:
            request = requests.get("https://" + link_url)
            status = str(request.status_code)
        except Exception as e:
            status = "404"
        redis_connection.setex(link_url,timedelta(minutes=1), value=status )
    else:
        status = cache_value.decode("utf-8")
    conn_str = "http://nginx:80/add_link"
    data = {}
    data['link_id'] = str(json_body['link_id'])
    data['link_status'] = status
    requests.put(conn_str, json=data)


channel.basic_consume(queue='app_que', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
