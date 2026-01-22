from transformers import pipeline
from src.config.settings import Settings
import logging

logger = logging.getLogger(__name__)

# Cargamos el modelo que vamos a utilizar (RoBERTa)
try:
    sentimentAnalyzer = pipeline(
        "text-classification",
        Settings.SENTIMENT_MODEL
    )
except Exception:
    logger.critical("Failed to load sentiment analysis model")
    raise

# Método para analizar el sentimiento más probable en el texto pasado como parámetro (Negative, Neutral o Positive)
def analyzeSentiment(text: str):

    if not text or not text.strip():
        return None
    
    try:
        result = sentimentAnalyzer(text[:500]) # Reduce el texto a 500 caracteres puesto que RoBERTa no admite textos muy largos (hasta 514)
        best = max(result, key=lambda x: x["score"]) # Nos quedamos con el sentimiento predominante

        return {"label": best["label"],
                "score": round(float(best["score"]),2)}

    except Exception:
        logger.warning(f"Sentiment analysis failed for text: {text[:30]}...")
        return None