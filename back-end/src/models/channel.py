from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.orm import relationship

from src.config.database import Base

class Channel(Base):
    __tablename__ = "channels" # Nombre de la tabla en PostgreSQL

    id = Column(Integer, primary_key=True, autoincrement=True) #ID interno
    channel_id = Column(String, unique=True, nullable=False, index=True) #ID real de YouTube
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False, index=True)
    thumbnail_url = Column(String, nullable=False)
    
    stats = relationship("ChannelStats", back_populates="channel", cascade="all, delete-orphan")
    videos = relationship("Video", back_populates="channel", cascade="all, delete-orphan")

