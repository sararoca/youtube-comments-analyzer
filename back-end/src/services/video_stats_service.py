from src.models import VideoStats
from src.repositories import video_stats_repository

def save_video_stats(db, id: int, data: dict):
    
    stats = VideoStats(
        video_id=id,
        view_count=data["view_count"],
        like_count=data["like_count"],
        comment_count=data["comment_count"]
    )
    
    video_stats_repository.save(db, stats)

