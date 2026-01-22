from pandas import DataFrame


def get_channel_detail(df_channel: DataFrame):
    
    if df_channel is None or df_channel.empty:
        return None

    row = df_channel.iloc[0]

    return {
        "channel_id": row["channel_id"],
        "yt_channel_id": row["yt_channel_id"],
        "name": row["name"],
        "description": row["description"],
        "thumbnail_url": row["thumbnail_url"],
        "created_at": row["created_at"],
        "subscribers": int(row["subscribers"]),
        "views": int(row["views"]),
        "videos": int(row["videos"]),
    }
