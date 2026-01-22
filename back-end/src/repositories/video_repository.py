from sqlalchemy.orm import Session
from src.models import Video
from typing import Iterable


def save(db: Session, v: Video):

    db.add(v)


# TODO: SE USA?
def get_by_video_id(db: Session, video_id: str):

    return (
        db.query(Video)
        .filter(Video.video_id == video_id)
        .first()
    )