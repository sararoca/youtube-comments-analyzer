from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import timezone, datetime

from src.config.database import Base


class SentimentAnalysis(Base):
    __tablename__ = "sentiment_analysis" # Nombre de la tabla en PostgreSQL

    id = Column(Integer, primary_key=True, autoincrement=True) # ID interno
    comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"),nullable=False, unique=True, index=True)
    label = Column(String, nullable=False, index=True)
    score = Column(Float, nullable=False)
    analyzed_at = Column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc))

    comment = relationship("Comment", back_populates="sentiment")