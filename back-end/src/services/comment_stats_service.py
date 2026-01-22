from src.models.comment_stats import CommentStats
from src.repositories import comment_stats_repository

def save_comment_stats(db, id: int, data: dict):
    
    stats = CommentStats(
        comment_id=id,
        like_count=data["like_count"],
    )
    
    comment_stats_repository.save(db, stats)

    


