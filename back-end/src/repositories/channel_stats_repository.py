from sqlalchemy.orm import Session
from src.models import ChannelStats

def save(db: Session, cs: ChannelStats):

    db.add(cs)
