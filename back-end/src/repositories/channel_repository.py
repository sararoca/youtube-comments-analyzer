from sqlalchemy.orm import Session
from src.models.channel import Channel


def save(db: Session, c: Channel):

    db.add(c)


def get_by_channel_id(db: Session, channel_id: str):

    return (
        db.query(Channel)
        .filter(Channel.channel_id == channel_id)
        .first()
    )

