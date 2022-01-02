from app import db


class User(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    line_id = db.Column(db.String(120), unique=True, nullable=False)
    role = db.relationship()
