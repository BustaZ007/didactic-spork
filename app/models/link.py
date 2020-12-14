from app import db


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.String(80), unique=False)

    def __init__(self, url, status):
        self.url = url
        self.status = status

    def __repr__(self):
        return "URL: "+self.url + "   Status: " + self.status