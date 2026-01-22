from sqlalchemy import Column, ForeignKey, Integer, BigInteger, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from src.config.database import Base

class ChannelStats(Base):
    __tablename__ = "channel_stats" # Nombre de la tabla en PostgreSQL

    id = Column(Integer, primary_key=True, autoincrement=True) # ID interno
    channel_id = Column(Integer, ForeignKey("channels.id", ondelete="CASCADE"), nullable=False, index=True)
    fetched_at = Column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc),index=True)
    subscriber_count = Column(BigInteger)
    view_count = Column(BigInteger)
    video_count = Column(BigInteger)

    channel = relationship("Channel", back_populates="stats")
    

