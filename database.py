from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'RegisteredUsers'

    id_users = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    added = db.Column(db.DateTime, nullable=False, default=func.now())



