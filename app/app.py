import pika as pika
from flask import Flask, request, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import json
import os
#  didactic-spork % docker-compose -f docker-compose.yml up --build
app = Flask(__name__)
db_user = os.environ["MYSQL_USER"]
db_password = os.environ["MYSQL_PASSWORD"]
db_name = os.environ["MYSQL_DATABASE"]
app_id = os.environ["APP_ID"]
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+db_user+':'+db_password+'@db_mysql:3306/'+db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


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
    return 'HelloWorls'


@app.route('/links', methods=['GET'])
def get_limks():
    links = Link.query.all()
    return render_template("index.html",
    links = links)

@app.route('/link', methods=['GET'])
def get_one_link():
    link_id = request.args.get("link_id")
    result = Response()
    result.headers['App Number'] = app_id
    try:
        link = db.session.query(Link).filter_by(id=link_id).one()
        result.response = json.dumps({
            'id' : link.id,
            'URl' : link.url,
            'status' : link.status 
        })
    except Exception as e:
        result.response = json.dumps({
            'ERROR' : "Link at id " + link_id + " not found"
        })
    return result


@app.route('/add_link', methods=['POST'])
def add_link():
    url = request.json
    link = Link(url['url'], "Wait please...")
    db.session.add(link)
    db.session.commit()
    send_message(str(link.id), link.url)
    result = Response(
        response=json.dumps({
            'id' : link.id,
            'URl' : link.url,
            'status' : link.status 
        }))
    result.headers['App Number'] = app_id
    return result


@app.route("/add_link", methods=['PUT'])
def update_link():
    link_id = request.args.get("link_id")
    link = db.session.query(Link).filter_by(id=link_id).one()
    link.status = request.args.get("link_status")

    db.session.commit()

    return "Link Updated"


def send_message(link_id: str, link_url: str):
    credentials = pika.PlainCredentials('user', 'user')
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit', 5672, '/', credentials))
    message = "{\"link_id\" : \"" + link_id + "\", \"link_url\" : \"" + link_url+ "\"}"
    channel = connection.channel()

    channel.exchange_declare(exchange='app_que_ex',
                             exchange_type='fanout')

    channel.basic_publish(
        exchange='app_que_ex',
        routing_key='',
        body=message,)

    connection.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
