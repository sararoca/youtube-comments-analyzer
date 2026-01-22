from sqlalchemy import ForeignKey, Column, BigInteger, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime,timezone

from src.config.database import Base


class CommentStats(Base):
    __tablename__ = "comment_stats" # Nombre de la tabla en PostgreSQL

    id = Column(Integer,primary_key=True, autoincrement=True) #ID interno
    comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=False, index=True)
    fetched_at = Column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc),index=True)
    like_count = Column(BigInteger, default=0)

    comment = relationship("Comment", back_populates="stats")
    