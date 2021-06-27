from datetime import datetime
from database import db

#class User(db.Model):
#    __tablename__ = 'users'
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(255), nullable=False)
#    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
#    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

class Idea(db.Model):
    __tablename__ = 'ideas'
    id = db.Column(db.Integer, primary_key=True)
    repo_id = db.Column(db.String(255), nullable=False)
    body = db.Column(db.String(255), nullable=False)
    author_login = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


__all__ = [
    Idea,
]