from src.analysis.emotion_analyzer import analyzeEmotion
from src.analysis.sentiment_analyzer import analyzeSentiment

def run_tests():
    texts = [
        "Me encanta este vídeo, es increíble",
        "Este vídeo es horrible, lo odio",
        "No está mal, pero podría ser mejor",
        "",
        None
    ]

    entradas_nuevas = [
        "Qué video tan inspirador, me alegró el día",
        "No entiendo nada de lo que explica, muy confuso",
        "Está bien explicado, aunque se hace un poco largo",
        "Este canal siempre sube contenido de calidad",
        "Perdí cinco minutos de mi vida viendo esto",
        "Me dio mucha risa esta parte del video",
        "Esperaba algo mejor, la verdad",
        "Excelente trabajo, se nota el esfuerzo",
        "No me gustó para nada el final",
        "Es un video normal, nada especial",
        "Gracias por compartir esta información",
        "Qué decepción, pensé que sería útil",
        "Buen video, pero el audio es muy malo"
    ]

    for text in entradas_nuevas:
        print("-" * 50)
        print(f"Texto: {text}")
        emotionResult = analyzeEmotion(text)
        sentimentResult = analyzeSentiment(text)
        print(f"Emoción: {emotionResult}")
        print(f"Sentimiento: {sentimentResult}")

if __name__ == "__main__":
    run_tests()
