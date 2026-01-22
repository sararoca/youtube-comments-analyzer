from sqlalchemy.orm import Session
from src.models import VideoStats


def save(db: Session, vs: VideoStats):

    db.add(vs)

