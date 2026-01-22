import logging

from src.config.database import SessionLocal
from src.services.comment_service import get_comments_for_emotion_analysis, get_comments_for_sentiment_analysis
from src.services.emotion_service import analyze_emotion_and_save_comments
from src.services.sentiment_service import analyze_sentiment_and_save_comments

logger = logging.getLogger(__name__)

class CommentsAnalyzer:

    def analyze_comments():

        logger.info("Comments analyzer started")

        db = SessionLocal() # Sesión de la base de datos
        
        try:
            try:
                commentsEmotion = get_comments_for_emotion_analysis(db)
                analyze_emotion_and_save_comments(db, commentsEmotion)
            except Exception:
                logger.exception("Emotion analysis failed")

            try:
                commentsSentiment = get_comments_for_sentiment_analysis(db)
                analyze_sentiment_and_save_comments(db, commentsSentiment)
            except Exception:
                logger.exception("Sentiment analysis failed")
            
            db.commit()

        except Exception as e:
            logger.exception("Comments analyzer failed")

        finally:
            db.close()
            logger.info("Comments analyzer finished")

    if __name__ == "__main__":
        analyze_comments()
