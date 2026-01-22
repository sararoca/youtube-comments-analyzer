from transformers import pipeline
from src.config.settings import Settings
import logging

logger = logging.getLogger(__name__)

# Cargamos el modelo que vamos a utilizar (BETO)
try: 
    emotionAnalyzer = pipeline(
        "text-classification",
        Settings.EMOTION_MODEL
    )
except Exception:
    logger.critical("Failed to load emotion analysis model")
    raise


# Método para analizar la emoción más probable en el texto pasado como parámetro (Anger, Disgust, Fear, Joy, Sadness, Surprise, Others)
def analyzeEmotion(text: str):

    if not text or not text.strip():
        return None

    try:
        result = emotionAnalyzer(text[:500]) # Reduce el texto a 500 caracteres puesto que BETO no admite textos muy largos (512)
        best = max(result, key=lambda x: x["score"]) # Nos quedamos con la emoción predominante

        return {"label": best["label"],
                "score": round(float(best["score"]),2)}
    
    except Exception:
        logger.warning(f"Emotion analysis failed for text: {text[:30]}...")
        return None