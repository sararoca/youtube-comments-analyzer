from sqlalchemy.orm import Session
from src.repositories import video_repository
from src.models import Video

def get_or_create_video(db: Session, id:int, video_data: dict):

    video = video_repository.get_by_video_id(db, video_data["video_id"])

    if video:
        return video
    
    video = Video(
        video_id = video_data["video_id"],
        channel_id  = id,
        title  = video_data["title"],
        description  = video_data["description"],
        published_at = video_data["published_at"],
        duration = video_data["duration"],
        thumbnail_url = video_data["thumbnail_url"],
        category_id = video_data["category_id"],
        video_url=video_data["video_url"],
        default_audio_language=video_data.get("default_audio_language"),
        default_language=video_data.get("default_language")
    )
    
    video_repository.save(db, video)
    db.flush()

    return video
    