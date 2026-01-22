from sqlalchemy.orm import Session
from src.models import Comment
from typing import Iterable

def save(db: Session, c: Comment):

    db.add(c)

def get_by_comment_id(db: Session, comment_id: str ):

    return (
        db.query(Comment)
        .filter(Comment.comment_id == comment_id)
        .first()
    )

def get_comments_pending_emotion (db: Session):
    return (
        db.query(Comment)
        .filter(Comment.emotion_analyzed == False)
        .all()
    )

def get_comments_pending_sentiment (db: Session):

    return (
        db.query(Comment)
        .filter(Comment.sentiment_analyzed == False)
        .all()
    )

def mark_emotion_analyzed (db: Session, c: Comment):

    c.emotion_analyzed = True
    db.add(c)


def mark_sentiment_analyzed (db: Session, c: Comment):

    c.sentiment_analyzed = True
    db.add(c)

