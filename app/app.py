import pika as pika
from flask import Flask, request, render_template, Response
from flask_sqlalchemy import SQLAlchemy
import json
import os


app = Flask(__name__)
db_user = os.environ["MYSQL_USER"]
db_password = os.environ["MYSQL_PASSWORD"]
db_name = os.environ["MYSQL_DATABASE"]
app_id = os.environ["APP_ID"]
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+db_user+':'+db_password+'@db_mysql:3306/'+db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# from models import link
# Link = link.Link()
class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.String(80), unique=False)

    def __init__(self, url, status):
        self.url = url
        self.status = status

    def __repr__(self):
        return "URL: "+self.url + "   Status: " + self.status


db.create_all()


@app.route('/', methods=['GET'])
def index():
    return 'HelloWorlds'


@app.route('/links', methods=['GET'])
def get_links():
    links = Link.query.all()
    return render_template("index.html",
        links = links)


@app.route('/link', methods=['GET'])
def get_one_link():
    link_id = request.args.get("link_id")
    try:
        link = db.session.query(Link).filter_by(id=link_id).one()
        return {
            'id' : link.id,
            'URl' : link.url,
            'status' : link.status 
        }
    except Exception as e:
        return{
            'ERROR' : "Link at id " + link_id + " not found"
        }


@app.route('/add_link', methods=['POST'])
def add_link():
    url = request.json
    link = Link(url['url'], "Wait please...")
    db.session.add(link)
    db.session.commit()
    send_message(str(link.id), link.url)
    return {
        'id' : link.id,
        'URl' : link.url,
        'status' : link.status
    }


@app.route("/add_link", methods=['PUT'])
def update_link():
    json_body = request.json
    link_id = json_body['link_id']
    link = db.session.query(Link).filter_by(id=link_id).one()
    link.status = json_body['link_status']

    db.session.commit()

    return {
        'message' : 'Link Updated',
        'link_id' : link_id}


@app.after_request
def after_request(response):
    response.headers['App Number'] = app_id
    return response


def send_message(link_id: str, link_url: str):
    credentials = pika.PlainCredentials('user', 'user')
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit', 5672, '/', credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='app_que_ex',
                             exchange_type='fanout')

    channel.basic_publish(
        exchange='app_que_ex',
        routing_key='',
        body=json.dumps({'link_id': link_id,
        'link_url' :link_url}))

    connection.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
