import requests
import logging

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from src.config.settings import settings

logger = logging.getLogger(__name__)

# Controlar la cuota de la API
def is_quota_exceeded(e: HttpError) -> bool:
    try:
        return any(
            err.get("reason") == "quotaExceeded"
            for err in e.error_details
        )
    except Exception:
        return False

# Cliente para interactuar con la API de YouTube Data v3
class YouTubeClient:

    # Inicialización del cliente
    def __init__(self):
        try:
            self.api_key = settings.YOUTUBE_API_KEY
            self.youtube = build(serviceName='youtube', version='v3', developerKey=self.api_key)
        except Exception:
            logger.exception("Failed to initialize YouTube client")
            raise

    # -------------------------- LLAMADAS A LA API --------------------------
    # Método para buscar videos 
    def search_videos(self, query: str, max_videos: int):

        video_ids = []
        next_page = None

        try:
            while len(video_ids) < max_videos:

                request = self.youtube.search().list(
                    part="snippet",
                    q=query,  # Palabra(s) clave(s) para la búsqueda
                    type="video",
                    maxResults=min(50, max_videos - len(video_ids)), # La API solo devuelve máximo 50 vídeos por llamada
                    videoCategoryId="24",  # Entertainment
                    order="relevance",   # Los más relevantes
                    safeSearch="none",    # Sin filtros
                    pageToken=next_page
                )

                response = request.execute()
                page_ids = [item["id"]["videoId"] for item in response["items"]]

                if not page_ids: 
                    break

                video_ids.extend(page_ids)

                next_page = response.get("nextPageToken")
                if not next_page: # Si no hay más páginas, se para la búsqueda
                    break

            return video_ids
        
        except HttpError as e:
            if e.resp.status == 403 and is_quota_exceeded(e):
                logger.critical("YouTube API quota exceeded during search")
            else:
                logger.error(f"YouTube search failed (status={e.resp.status}): {e.error_details}")
            return []   

    
    # Método para obtener la información detalla de los videos cuyos IDs pasamos como parámetro
    def get_detailed_videos(self, video_ids):

        videos = []

        if not video_ids: # Si la lista pasada como parámetro está vacía
            return videos

        try:
            for i in range(0, len(video_ids), 50): # La API solo acepta hasta 50 IDs por llamada
                
                tmp = video_ids[i:i+50]

                details_request = self.youtube.videos().list(
                    part="snippet,statistics,contentDetails",
                    id = ",".join(tmp)
                )

                details_response = details_request.execute()

                for item in details_response.get("items", []):
                    snippet = item["snippet"]
                    statistics = item.get("statistics", {})
                    content_details = item.get("contentDetails", {})
                                    
                    videos.append({
                        "video_id": item["id"],
                        "channel_id": snippet.get("channelId", ""),
                        "title": snippet.get("title", ""),
                        "description": snippet.get("description", ""),
                        "published_at": snippet.get("publishedAt", ""),
                        "view_count": int(statistics.get("viewCount",0)),
                        "like_count": int(statistics.get("likeCount",0)),
                        "comment_count": int(statistics.get("commentCount",0)),
                        "duration": content_details.get("duration", ""),
                        "thumbnail_url": snippet.get("thumbnails",{}).get("high",{}).get("url"),
                        "category_id": snippet.get("categoryId", ""),
                        "video_url": f"https://www.youtube.com/watch?v={item['id']}",
                        "default_audio_language": snippet.get("defaultAudioLanguage"),
                        "default_language": snippet.get("defaultLanguage"),

                    })        

            return videos
        
        except HttpError as e:
            if e.resp.status == 403 and is_quota_exceeded(e):
                logger.critical("YouTube API quota exceeded while fetching video details")
            else:
                logger.error(f"Failed to fetch video details (status={e.resp.status})")
            return videos # Devuelve lo que haya podido obtener

    # Método para obtener los comentarios de un vídeo específico pasando su ID como parámetro
    def get_comments_from_video(self, video_id, max_comments):

        comments = []
        next_page = None

        try:
            while len(comments) < max_comments:

                request = self.youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=min(100, max_comments - len(comments)),
                    textFormat="plainText",
                    order="relevance",
                    pageToken=next_page
                )

                response = request.execute()

                for item in response.get("items", []):
                    top_comment = item["snippet"]["topLevelComment"]
                    snippet = top_comment["snippet"]

                    comments.append({
                        "comment_id": top_comment.get("id"),
                        "video_id": video_id,
                        "published_at": snippet.get("publishedAt", ""),
                        "author": snippet.get("authorDisplayName", ""),
                        "text": snippet.get("textDisplay", ""),
                        "like_count": int(snippet.get("likeCount", 0))
                    })

                    if len(comments) >= max_comments:
                        break

                next_page = response.get("nextPageToken")
                if not next_page:
                    break

            return comments

        except HttpError as e:
            if e.resp.status == 403 and is_quota_exceeded(e):
                logger.critical(
                    f"YouTube API quota exceeded while fetching comments for video {video_id}"
                )
            elif e.resp.status == 403:
                logger.info(f"Comments disabled for video {video_id}")
            else:
                logger.error(
                    f"Failed to fetch comments for {video_id} (status={e.resp.status})"
                )
            return []

              
    # Método para obtener la información de los canales cuyos IDs pasamos como parámetro
    def get_detailed_channels(self, channel_ids):

        channels = []

        if not channel_ids: # Si la lista pasada como parámetro está vacía
            return channels

        try:
            for i in range(0, len(channel_ids), 50):

                tmp = channel_ids[i:i+50]

                request = self.youtube.channels().list(
                    part="snippet,statistics",
                    id=",".join(tmp),
                )

                response = request.execute()

                for item in response.get("items", []):
                    snippet = item.get("snippet", {})
                    stats = item.get("statistics", {})

                    channels.append({
                        "channel_id": item.get("id"),
                        "name": snippet.get("title", ""),
                        "description": snippet.get("description", ""),
                        "published_at": snippet.get("publishedAt", ""),
                        "thumbnail_url": (
                            snippet.get("thumbnails", {})
                                .get("high", {})
                                .get("url")
                            or snippet.get("thumbnails", {})
                                    .get("medium", {})
                                    .get("url")
                            or snippet.get("thumbnails", {})
                                    .get("default", {})
                                    .get("url")
                        ),
                        "view_count": int(stats.get("viewCount", 0)),
                        "subscriber_count": int(stats.get("subscriberCount", 0)),
                        "video_count": int(stats.get("videoCount", 0))
                    })

            return channels
        
        except HttpError as e:
            if e.resp.status == 403 and is_quota_exceeded(e):
                logger.critical("YouTube API quota exceeded while fetching channel details")
            else:
                logger.error(f"Failed to fetch channel details (status={e.resp.status})")
            return channels # Devuelve lo que haya podido obtener

