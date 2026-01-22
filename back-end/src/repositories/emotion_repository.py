from sqlalchemy.orm import Session
from src.models import EmotionAnalysis

def save(db: Session, e: EmotionAnalysis):

    db.add(e)

# TODO: SE USA?
def get_by_comment_id(db: Session, comment_id : str):

    return (
        db.query(EmotionAnalysis)
        .filter(EmotionAnalysis.comment_id == comment_id)
        .first()
    )