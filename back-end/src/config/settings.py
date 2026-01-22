import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Configuración global del proyecto
class Settings:

    
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    #print("YOUTUBE API KEY LEIDA: ", YOUTUBE_API_KEY)
    DATABASE_URL = os.getenv("DATABASE_URL")
    #print("DATABASE URL LEIDA: ", DATABASE_URL)
    APP_NAME = os.getenv("APP_NAME")
    #print("APP NAME LEIDO: ", APP_NAME)
    EMOTION_MODEL = os.getenv("EMOTION_MODEL")
    #print("EMOTION MODEL LEIDO: ", EMOTION_MODEL)
    SENTIMENT_MODEL = os.getenv("SENTIMENT_MODEL")
    #print("SENTIMENT MODEL LEIDO: ", SENTIMENT_MODEL)

settings = Settings()