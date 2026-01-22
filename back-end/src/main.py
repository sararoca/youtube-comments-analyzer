from src.config.database import engine, Base, SessionLocal
from src.models import Channel, ChannelStats, Comment, CommentStats, Video, VideoStats, EmotionAnalysis, SentimentAnalysis
from sqlalchemy import text
from pathlib import Path

def init_db():

    #  Crear tablas
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas con éxito")


    # Crear vistas
    views_path = Path(__file__).parent / "views" / "views.sql"
    print("Vistas creadas con éxito")

    with engine.begin() as conn:
        sql = views_path.read_text(encoding="utf-8")
        conn.execute(text(sql))

if __name__ == "__main__":
    init_db()

