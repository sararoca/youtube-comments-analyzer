from sqlalchemy.orm import Session
from src.models import CommentStats


def save(db: Session, cs: CommentStats):

    db.add(cs)

