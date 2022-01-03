from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    users = db.relationship("User", backref="role", lazy="dynamic")


class User(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    line_id = db.Column(db.String(120), unique=True, nullable=False)
    role_id = db.Column(db.Integer(), db.ForeignKey("role.id"), nullable=False)
