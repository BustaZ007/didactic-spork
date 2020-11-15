import pika
import requests
import json

credentials = pika.PlainCredentials('user', 'user')
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit', 5672, '/', credentials))

channel = connection.channel()

channel.queue_declare(queue='app_que', durable=True)
channel.exchange_declare(exchange='app_que_ex', exchange_type='fanout')

channel.queue_bind(exchange='app_que_ex', queue='app_que')


def callback(ch, method, properties, body):
    json_body = json.loads(body.decode())

    try:
        request = requests.get("https://" + json_body['link_url'])
        status = str(request.status_code)
    except Exception as e:
        status = "404"

    requests.put('http://app:5000/add_link', data={'link_status': status, 'link_id': json_body['link_id']})
    # conn_str = "http://nginx:80/links?link_id=" + str(json_body['link_id']) + "&link_status=" + status
    # requests.put(conn_str)
    # requests.post("http://app:5000/links?link=" + conn_str)


channel.basic_consume(queue='app_que', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
