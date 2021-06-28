from datetime import datetime
from database import db


class Idea(db.Model):
    __tablename__ = "ideas"
    id = db.Column(db.Integer, primary_key=True)
    repo_id = db.Column(db.String(255), nullable=False)
    body = db.Column(db.String(255), nullable=False)
    author_login = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, repo_id, body, author_login):
        self.repo_id = repo_id
        self.body = body
        self.author_login = author_login


__all__ = [
    Idea,
]