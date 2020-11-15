from app.app import db


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(80), unique=False, nullable=False)

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return self.url
