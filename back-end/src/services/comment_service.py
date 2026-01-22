from sqlalchemy.orm import Session
from src.repositories import comment_repository
from src.models import Comment, Video
from typing import Iterable

def get_or_create_comment(db: Session, id: int, comment_data: dict):

    comment = comment_repository.get_by_comment_id(db, comment_data["comment_id"])

    if comment:
        return comment

    comment = Comment(
        comment_id = comment_data["comment_id"],
        video_id = id,
        published_at = comment_data["published_at"],
        author = comment_data["author"],
        text = comment_data["text"]
    )

    comment_repository.save(db, comment)
    db.flush()

    return comment

def get_comments_for_emotion_analysis (db: Session):

    return comment_repository.get_comments_pending_emotion(db)

def get_comments_for_sentiment_analysis (db: Session):

    return comment_repository.get_comments_pending_sentiment(db)

def finalize_emotion_analysis (db: Session, comment: Comment):
   return comment_repository.mark_emotion_analyzed(db, comment)

def finalize_sentiment_analysis (db: Session, comment: Comment):
   return comment_repository.mark_sentiment_analyzed(db, comment)