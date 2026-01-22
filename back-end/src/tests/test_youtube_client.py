from src.services.youtube_client import YouTubeClient
import json
from langdetect import detect, LangDetectException

def is_spanish_comment(comment):

    text = comment.get("text", "").strip()
    
    if not text:
        return False

    try:
        return detect(text) == "es"
    except LangDetectException:
        return False

def is_spanish_video(video):
    return (
        video.get("default_audio_language", "").startswith("es")
        or video.get("default_language", "").startswith("es")
    )

def main():
    yt = YouTubeClient()

    comentarios_es = []
    comentarios_not_es_not_len = []

    channel_ids = []

    print("Buscando vídeos sobre 'true crime español'...")
    video_ids = yt.search_videos("true crime español", 100)

    print(f"Obteniendo detalles de {len(video_ids)} vídeos...")
    videos_detallados = yt.get_detailed_videos(video_ids)

    # Filtrar vídeos en español
    videos_es = [
        v for v in videos_detallados
        if is_spanish_video(v)
    ]

    videos_otro_idioma =[
        v for v in videos_detallados
        if not is_spanish_video(v)
    ]

    print(f"Vídeos en español detectados: {len(videos_es)}")
    print(f"Vídeos en otro idioma detectados: {len(videos_otro_idioma)}")

    with open("videos_es.json", "w", encoding="utf-8") as f:
        json.dump(videos_es, f, indent=4, ensure_ascii=False)
    with open("videos_otro.json", "w", encoding="utf-8") as f:
        json.dump(videos_otro_idioma, f, indent=4, ensure_ascii=False)

    # Obtener canales solo de vídeos en español
    for v in videos_es:
        channel_ids.append(v["channel_id"])

    detailed_channels = yt.get_detailed_channels(list(set(channel_ids)))

    with open("detailed_channels.json", "w", encoding="utf-8") as f:
        json.dump(detailed_channels, f, indent=4, ensure_ascii=False)

    print("Extrayendo comentarios y detectando idioma...")

    for v in videos_es:
        raw_comments = yt.get_comments_from_video(v["video_id"], 200)

        for c in raw_comments:
            text = c.get("text", "").strip()

            if len(text) < 3:
                c["reason"] = "too_short"
                comentarios_not_es_not_len.append(c)
                continue

            if not is_spanish_comment(c):
                c["reason"] = "not_spanish"
                comentarios_not_es_not_len.append(c)
                continue

            c["detected_language"] = "es"
            comentarios_es.append(c)


    with open("comentarios_es.json", "w", encoding="utf-8") as f:
        json.dump(comentarios_es, f, indent=4, ensure_ascii=False)
    with open("comentarios_otro.json", "w", encoding="utf-8") as f:
        json.dump(comentarios_not_es_not_len, f, indent=4, ensure_ascii=False)

    print(f"Comentarios en español guardados: {len(comentarios_es)}")
    print(f"Comentarios en otro guardados: {len(comentarios_not_es_not_len)}")


if __name__ == "__main__":
    main()
