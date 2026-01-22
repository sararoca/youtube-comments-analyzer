from pandas import DataFrame


def get_comments_detail(df_comment: DataFrame):
    
    comments_page = dict()


    for index, row in df_comment.iterrows():

        comments_page[index] = {
        "comment_id": row["comment_id"],
        "yt_comment_id": row["yt_comment_id"],

        "video_id": row["video_id"],
        "yt_video_id": row["yt_video_id"],
        "video_title": row["video_title"],

        "channel_id": row["channel_id"],
        "channel_name": row["channel_name"],

        "author": row["author"],
        "text": row["text"],
        "published_at": row["published_at"],

        "fetched_at": row["fetched_at"],
        "likes": int(row["likes"]) if row["likes"] is not None else 0,

        "sentiment": row["sentiment"],
        "sentiment_score": float(row["sentiment_score"]),

        "emotion": row["emotion"],
        "emotion_score": float(row["emotion_score"]),
    }
        
    return comments_page
