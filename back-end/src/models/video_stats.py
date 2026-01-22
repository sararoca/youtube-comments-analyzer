from sqlalchemy import Column, ForeignKey, Integer, DateTime, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime,timezone

from src.config.database import Base

class VideoStats(Base):
    __tablename__ = "video_stats" # Nombre de la tabla en PostgreSQL

    id = Column(Integer, primary_key=True, autoincrement=True) # ID interno
    video_id = Column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), nullable=False, index=True)
    fetched_at = Column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc),index=True)
    view_count = Column(BigInteger)
    like_count = Column(BigInteger)
    comment_count = Column(BigInteger)

    video = relationship("Video", back_populates="stats")
    