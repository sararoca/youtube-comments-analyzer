from sqlalchemy.orm import Session
from src.repositories import sentiment_repository
from src.services import comment_service
from src.models import SentimentAnalysis, Comment
from src.analysis.sentiment_analyzer import analyzeSentiment
from typing import Iterable
from tqdm import tqdm

def analyze_sentiment_and_save_comments(db: Session, comments: Iterable[Comment]):

    for c in tqdm(comments, desc="Analizando sentimientos", unit="comment"):

        result = analyzeSentiment(c.text)

        e = SentimentAnalysis(
            comment_id=c.id,
            label=result["label"],
            score=result["score"]
        )

        sentiment_repository.save(db, e)
        comment_service.finalize_sentiment_analysis(db, c) # Lo marca como analizado

