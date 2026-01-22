from sqlalchemy.orm import Session
from src.repositories import emotion_repository
from src.services import comment_service
from src.models import EmotionAnalysis, Comment
from src.analysis.emotion_analyzer import analyzeEmotion
from typing import Iterable
from tqdm import tqdm

def analyze_emotion_and_save_comments(db: Session, comments: Iterable[Comment]):

    for c in tqdm(comments, desc="Analizando emociones", unit="comment"):

        result = analyzeEmotion(c.text)

        e = EmotionAnalysis(
            comment_id=c.id,
            label=result["label"],
            score=result["score"]
        )

        emotion_repository.save(db, e)
        comment_service.finalize_emotion_analysis(db, c) # Lo marca como analizado

