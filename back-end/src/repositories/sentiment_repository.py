from sqlalchemy.orm import Session
from src.models import SentimentAnalysis

def save(db: Session, s: SentimentAnalysis):

    db.add(s)

# TODO: SE USA?
def get_by_comment_id(db: Session, comment_id : str):

    return (
        db.query(SentimentAnalysis)
        .filter(SentimentAnalysis.comment_id == comment_id)
        .first()
    )