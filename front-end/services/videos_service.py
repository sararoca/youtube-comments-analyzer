from pandas import DataFrame


def get_video_detail(df_video: DataFrame):
 

    if df_video is None or df_video.empty:
        return None

    row = df_video.iloc[0]

    return {
        "video_id": row["video_id"],
        "yt_video_id": row["yt_video_id"],

        "channel_id": row["channel_id"],
        "channel_name": row["channel_name"],

        "title": row["title"],
        "description": row["description"],
        "published_at": row["published_at"],
        "duration": row["duration"],

        "thumbnail_url": row["thumbnail_url"],
        "video_url": row["video_url"],

        "views": int(row["views"]) if row["views"] is not None else 0,
        "likes": int(row["likes"]) if row["likes"] is not None else 0,
        "comments": int(row["comments"]) if row["comments"] is not None else 0,

        "fetched_at": row["fetched_at"],
    }
