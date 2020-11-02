from app import app, db
from .models.link import Link


@app.route('/', methods=['GET'])
def index():
    return 'HelloWorls'


@app.route('/links', methods=['GET'])
def get_limks():
    return Link.query.all()


@app.route('/add_link', methods=['POST'])
def add_link(url):
    db.append(Link(url))
    return 'Vse good'
