from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.config.database import Base

class Comment(Base):
    __tablename__ = "comments" # Nombre de la tabla en PostgreSQL

    id = Column(Integer, primary_key=True, autoincrement=True) # ID interno
    comment_id = Column(String, unique=True, nullable=False, index=True) # ID real de YouTube
    video_id = Column(Integer, ForeignKey("videos.id", ondelete="CASCADE"),nullable=False, index=True)
    published_at = Column(DateTime(timezone=True), nullable=False, index=True)
    author = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    emotion_analyzed = Column(Boolean, default=False, index=True)
    sentiment_analyzed = Column(Boolean, default=False, index=True)

    stats = relationship("CommentStats", back_populates="comment", cascade="all, delete-orphan")
    video = relationship("Video", back_populates="comments")
    emotion = relationship("EmotionAnalysis", uselist=False, back_populates="comment")
    sentiment = relationship("SentimentAnalysis", uselist=False, back_populates="comment")