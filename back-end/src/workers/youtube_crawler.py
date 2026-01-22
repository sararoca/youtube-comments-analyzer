import logging
from tqdm import tqdm
from langdetect import detect, LangDetectException

from src.config.database import SessionLocal
from src.services.youtube_client import YouTubeClient
from src.services.channel_service import get_or_create_channel
from src.services.video_service import get_or_create_video
from src.services.comment_service import get_or_create_comment
from src.services.channel_stats_service import save_channel_stats
from src.services.video_stats_service import save_video_stats
from src.services.comment_stats_service import save_comment_stats

logger = logging.getLogger(__name__)


def is_spanish_comment(comment: dict) -> bool:
    text = comment.get("text", "").strip()
    if not text:
        return False
    try:
        return detect(text) == "es"
    except LangDetectException:
        return False


def is_spanish_video(video: dict) -> bool:
    return (
        (video.get("default_audio_language") or "").startswith("es")
        or (video.get("default_language") or "").startswith("es")
    )


class YouTubeCrawler:

    def crawl(query: str, max_videos: int, max_comments: int):

        logger.info("Crawler started")

        db = SessionLocal()
        yt = YouTubeClient()

        total_comments_saved = 0
        detailed_videos = []
        detailed_channels = []

        try:
         
            ids = yt.search_videos(query, max_videos)
            detailed_videos = yt.get_detailed_videos(ids)

            if not detailed_videos:
                logger.warning("No video details retrieved")
                return

           
            spanish_videos = [
                v for v in detailed_videos
                if is_spanish_video(v)
            ]

            # logger.info(
            #     "Videos total=%d | Videos en español=%d",
            #     len(detailed_videos),
            #     len(spanish_videos)
            # )

            if not spanish_videos:
                logger.warning("No spanish videos detected")
                return

            channel_ids = {v["channel_id"] for v in spanish_videos}
            detailed_channels = yt.get_detailed_channels(list(channel_ids))

            if not detailed_channels:
                logger.warning("No channel details retrieved")
                return

            channel_id_dict = {}

            for ch in tqdm(detailed_channels, desc="Procesando canales", unit="channel"):
                channel = get_or_create_channel(db, ch)
                channel_id_dict[ch["channel_id"]] = channel.id

                stats_channel = {
                    "subscriber_count": ch["subscriber_count"],
                    "view_count": ch["view_count"],
                    "video_count": ch["video_count"],
                }
                save_channel_stats(db, channel.id, stats_channel)

            for video_data in tqdm(spanish_videos, desc="Procesando vídeos y comentarios", unit="video"):

                video = get_or_create_video(
                    db,
                    channel_id_dict[video_data["channel_id"]],
                    video_data
                )

                stats_video = {
                    "view_count": video_data["view_count"],
                    "like_count": video_data["like_count"],
                    "comment_count": video_data["comment_count"],
                }
                save_video_stats(db, video.id, stats_video)

                raw_comments = yt.get_comments_from_video(
                    video_data["video_id"],
                    max_comments
                )

                for c in raw_comments:

                    if not is_spanish_comment(c):
                        continue

                    if len(c.get("text", "").strip()) < 3:
                        continue

                    comment = get_or_create_comment(db, video.id, c)
                    save_comment_stats(
                        db,
                        comment.id,
                        {"like_count": c["like_count"]}
                    )
                    total_comments_saved += 1

            db.commit()

        except Exception:
            db.rollback()
            logger.exception("Crawler failed")

        finally:
            db.close()
            # logger.info(
            #     "Crawler finished: channels=%d videos=%d comments=%d",
            #     len(detailed_channels),
            #     len(spanish_videos) if "spanish_videos" in locals() else 0,
            #     total_comments_saved
            # )


    if __name__ == "__main__":
        crawl(query="true crime español", max_videos=500, max_comments=1000)
