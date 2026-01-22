from sqlalchemy.orm import Session
from src.repositories import channel_repository
from src.models import Channel

def get_or_create_channel(db: Session, channel_data: dict):

    channel = channel_repository.get_by_channel_id(db, channel_data["channel_id"])

    if channel:
        return channel
    
    channel = Channel(
        channel_id  = channel_data["channel_id"],
        name  = channel_data["name"],
        description  = channel_data["description"],
        created_at = channel_data["published_at"],
        thumbnail_url = channel_data["thumbnail_url"]
    )

    channel_repository.save(db, channel)
    db.flush()
    
    return channel

