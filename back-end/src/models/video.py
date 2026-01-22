from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

from src.config.database import Base


class Video(Base):
    __tablename__ = "videos" # Nombre de la tabla en PostgreSQL

    id = Column(Integer, primary_key=True, autoincrement=True) # ID interno
    video_id = Column(String, unique=True, nullable=False, index=True) # ID real de YouTube
    channel_id = Column(Integer, ForeignKey("channels.id", ondelete="CASCADE"),nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    published_at = Column(DateTime(timezone=True), nullable=False, index=True)
    duration = Column(String, nullable=False)
    thumbnail_url = Column(String, nullable=False)
    category_id = Column(String, nullable=False)
    video_url = Column(String, nullable=False)
    default_audio_language = Column(String, nullable=True)
    default_language = Column(String, nullable=True)

    stats = relationship("VideoStats", back_populates="video", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="video")
    channel = relationship("Channel", back_populates="videos")
