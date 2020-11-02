from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@untitled3_db_1:3306/database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(80), unique=False, nullable=False)

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return self.url


db.create_all()

@app.route('/', methods=['GET'])
def index():
    return 'HelloWorls'


@app.route('/links', methods=['GET'])
def get_limks():
    links = Link.query.all()
    print(links)
    return str(links)


@app.route('/add_link', methods=['POST'])
def add_link():
    url = request.json
    link = Link(url['url'])
    print(link)
    db.session.add(link)
    db.session.commit()
    return 'OK'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
