from src.models import ChannelStats
from src.repositories import channel_stats_repository

def save_channel_stats(db, id: int, data: dict):
    
    stats = ChannelStats(
        channel_id=id,
        subscriber_count=data["subscriber_count"],
        view_count=data["view_count"],
        video_count=data["video_count"]
    )
    
    channel_stats_repository.save(db, stats)

