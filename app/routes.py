# from app.app import db
# from app import app
# from flask import request
# from .models.link import Link
#
#
# @app.route('/', methods=['GET'])
# def index():
#     return 'HelloWorls'
#
#
# @app.route('/links', methods=['GET'])
# def get_limks():
#     links = Link.query.all()
#     print(links)
#     return str(links)
#
#
# @app.route('/add_link', methods=['POST'])
# def add_link():
#     url = request.json
#     link = Link(url['url'])
#     print(link)
#     db.session.add(link)
#     db.session.commit()
#     return 'OK'
#
