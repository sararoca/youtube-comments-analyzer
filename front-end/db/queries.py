from db.database import engine
import pandas as pd


# ------------------------------------------- GLOBAL -------------------------------------------

# Contadores globales
def get_global_counts():
    query = """
        SELECT
            (SELECT COUNT(*) FROM v_video_latest)   AS total_videos,
            (SELECT COUNT(*) FROM v_comments_latest) AS total_comments,
            (SELECT COUNT(*) FROM v_channel_latest)  AS total_channels;
    """
    return pd.read_sql(query, engine)


# KPIs globales + medias (desde vídeos)
def get_global_and_avg_kpis():
    query = """
        SELECT
            COUNT(video_id)     AS total_videos,
            SUM(views)          AS total_views,
            SUM(likes)          AS total_likes,
            SUM(comments)       AS total_comments,
            AVG(views)          AS avg_views,
            AVG(likes)          AS avg_likes,
            AVG(comments)       AS avg_comments
        FROM v_video_latest;
    """
    return pd.read_sql(query, engine)

# Emociones globales
def get_global_emotion():
    query = """
        SELECT *
        FROM v_comments_emotion_summary;
    """
    return pd.read_sql(query, engine)

# Sentimiento global
def get_global_sentiment():
    query = """
        SELECT *
        FROM v_comments_sentiment_summary;
    """
    return pd.read_sql(query, engine)

# ------------------------------------------- CANALES -------------------------------------------

# Canal por ID
def get_channel_by_id(channel_id):
    query = """
        SELECT *
        FROM v_channel_latest
        WHERE channel_id = %(channel_id)s;
    """
    return pd.read_sql(query, engine, params={"channel_id": channel_id})

# KPIs del canal
def get_channel_kpis(channel_id: int):
    query = """
        SELECT
            ch.channel_id,
            ch.subscribers,
            ch.views,
            ch.videos,
            COUNT(c.comment_id) AS analyzed_comments
        FROM v_channel_latest ch
        LEFT JOIN v_comments_latest c
            ON ch.channel_id = c.channel_id
        WHERE ch.channel_id = %(channel_id)s
        GROUP BY
            ch.channel_id,
            ch.subscribers,
            ch.views,
            ch.videos;
    """
    return pd.read_sql(
        query,
        engine,
        params={"channel_id": int(channel_id)}
    )

# Conteo canales
def count_channnels(name: str = "", min_views: int = 0, min_subscribers: int = 0):
    query = "SELECT COUNT(*) FROM v_channel_latest WHERE 1=1"

    params = {}

    if name:
        query += " AND name ILIKE %(name)s"
        params["name"] = f"%{name}%"

    if min_views is not None:
        query += " AND views >= %(min_views)s"
        params["min_views"] = min_views

    if min_subscribers is not None:
        query += " AND subscribers >= %(min_subscribers)s"
        params["min_subscribers"] = min_subscribers


    return pd.read_sql(query, engine, params=params).iloc[0, 0]

# Canales paginados
def get_channels_paginated(limit: int, offset: int, name: str = "", min_views: int = 0, min_subscribers: int = 0):
    query = """
        SELECT
            channel_id,
            yt_channel_id,
            name,
            description,
            created_at,
            subscribers,
            videos,
            views,
            thumbnail_url AS image
        FROM v_channel_latest
        WHERE 1=1
    """

    params = {
        "limit": limit,
        "offset": offset,
    }

    if name:
        query += " AND name ILIKE %(name)s"
        params["name"] = f"%{name}%"

    if min_views is not None:
        query += " AND views >= %(min_views)s"
        params["min_views"] = min_views

    if min_subscribers is not None:
        query += " AND subscribers >= %(min_subscribers)s"
        params["min_subscribers"] = min_subscribers

    query += """
        ORDER BY name ASC
        LIMIT %(limit)s OFFSET %(offset)s;
    """

    return pd.read_sql(query, engine, params=params)

# Resumen emoción agregada de un canal
def get_channel_emotion(channel_id: int):
    query = """
        SELECT
            ve.emotion,
            SUM(ve.total_comments) AS total_comments
        FROM v_video_emotion ve
        JOIN v_video_latest v ON v.video_id = ve.video_id
        WHERE v.channel_id = %(channel_id)s
        GROUP BY ve.emotion
        ORDER BY total_comments DESC;        
    """

    return pd.read_sql(query, engine, params={"channel_id": channel_id})

# Resumen sentimiento agregado de un canal
def get_channel_sentiment(channel_id: int):
    query = """
        SELECT
            vs.sentiment,
            SUM(vs.total_comments) AS total_comments
        FROM v_video_sentiment vs
        JOIN v_video_latest v ON v.video_id = vs.video_id
        WHERE v.channel_id = %(channel_id)s
        GROUP BY vs.sentiment
        ORDER BY total_comments DESC;        
    """

    return pd.read_sql(query, engine, params={"channel_id": channel_id})

def get_channel_growth_timeseries(channel_id: int):
    query = """
        SELECT
            date,
            subscribers,
            views,
            videos
        FROM v_channel_growth_timeseries
        WHERE channel_id = %(channel_id)s
        ORDER BY date;
    """
    return pd.read_sql(query, engine, params={"channel_id": channel_id})

def count_videos_by_channel(channel_id: int):
    query = """
        SELECT COUNT(DISTINCT video_id)
        FROM v_video_latest
        WHERE channel_id = %s
    """
    return pd.read_sql(query, engine, params=(channel_id,)).iloc[0, 0]

def get_channel_videos_paginated(channel_id: int, limit: int, offset: int):
    query = """
        SELECT *,
            thumbnail_url AS image
        FROM v_video_latest
        WHERE channel_id = %s
        ORDER BY published_at DESC
        LIMIT %s OFFSET %s
    """
    return pd.read_sql(query, engine, params=(channel_id, limit, offset))

# ------------------------------------------- VÍDEOS -------------------------------------------

# Vídeo por ID
def get_video_by_id(video_id):
    query = """
        SELECT *
        FROM v_video_latest
        WHERE video_id = %(video_id)s;
    """
    return pd.read_sql(query, engine, params={"video_id": video_id})

# KPIs del video
def get_video_kpis(video_id: int):
    query = """
        SELECT
            v.video_id,
            v.views,
            v.likes,
            v.comments AS youtube_comments,
            COUNT(c.comment_id) AS analyzed_comments
        FROM v_video_latest v
        LEFT JOIN v_comments_latest c
            ON v.video_id = c.video_id
        WHERE v.video_id = %(video_id)s
        GROUP BY
            v.video_id,
            v.views,
            v.likes,
            v.comments;
    """

    return pd.read_sql(query, engine, params={"video_id": int(video_id)})

# Conteo vídeos
def count_videos(title: str = "", channel: str = "", min_likes: int = 0):
    query = "SELECT COUNT(*) FROM v_video_latest WHERE 1=1" 

    params = {}

    if title:
        query += " AND title ILIKE %(title)s"
        params["title"] = f"%{title}%"

    if channel:
        query += " AND channel_name ILIKE %(channel)s"
        params["channel"] = f"%{channel}%"

    if min_likes is not None:
        query += " AND likes >= %(min_likes)s"
        params["min_likes"] = min_likes


    return pd.read_sql(query, engine, params=params).iloc[0, 0]

# Vídeos paginados
def get_videos_paginated(limit: int, offset: int, title: str = "", channel: str = "", min_likes: int = 0):
    query = """
        SELECT
            video_id,
            yt_video_id,
            title,
            published_at,
            likes,
            comments,
            views,
            thumbnail_url AS image,
            channel_name,
            description,
            video_url
        FROM v_video_latest
        WHERE 1=1
    """
    params = {
        "limit": limit,
        "offset": offset,
    }

    if title:
        query += " AND title ILIKE %(title)s"
        params["title"] = f"%{title}%"

    if channel:
        query += " AND channel_name ILIKE %(channel)s"
        params["channel"] = f"%{channel}%"

    if min_likes is not None:
        query += " AND likes >= %(min_likes)s"
        params["min_likes"] = min_likes

    query += """
        ORDER BY title ASC
        LIMIT %(limit)s OFFSET %(offset)s;
    """

    return pd.read_sql(query, engine, params=params)

# Resumen emoción de un vídeo
def get_video_emotion(video_id: int):
    query = """
        SELECT
            emotion,
            total_comments
        FROM v_video_emotion
        WHERE video_id = %(video_id)s
        ORDER BY total_comments DESC;
    """
    return pd.read_sql(query, engine, params={"video_id": video_id})

# Resumen sentimiento de un vídeo
def get_video_sentiment(video_id: int):
    query = """
        SELECT
            sentiment,
            total_comments
        FROM v_video_sentiment
        WHERE video_id = %(video_id)s
        ORDER BY total_comments DESC;
    """
    return pd.read_sql(query, engine, params={"video_id": video_id})

def get_video_growth_timeseries(video_id: int):
    query = """
        SELECT
            date,
            views,
            likes,
            comments
        FROM v_video_growth_timeseries
        WHERE video_id = %(video_id)s
        ORDER BY date ASC;
    """
    return pd.read_sql(
        query,
        engine,
        params={"video_id": int(video_id)}
    )

def count_comments_by_video(video_id: int):
    query = """
        SELECT COUNT(DISTINCT comment_id)
        FROM v_comments_latest
        WHERE video_id = %s
    """
    return pd.read_sql(query, engine, params=(video_id,)).iloc[0, 0]

def get_video_comments_paginated(video_id: int, limit: int, offset: int):
    query = """
        SELECT *
        FROM v_comments_latest
        WHERE video_id = %s
        ORDER BY fetched_at DESC
        LIMIT %s OFFSET %s
    """
    return pd.read_sql(query, engine, params=(video_id, limit, offset))

# ------------------------------------------- COMENTARIOS -------------------------------------------

# Conteo comentarios con filtros
def count_comments(search: str = "", sentiment: str = "", emotion: str = ""):
    query = """
        SELECT COUNT(*)
        FROM v_comments_latest
        WHERE text IS NOT NULL
    """
    params = {}

    if search:
        query += " AND text ILIKE %(search)s"
        params["search"] = f"%{search}%"

    if sentiment:
        query += " AND sentiment = %(sentiment)s"
        params["sentiment"] = sentiment

    if emotion:
        query += " AND emotion = %(emotion)s"
        params["emotion"] = emotion

    return pd.read_sql(query, engine, params=params).iloc[0, 0]

# Comentarios paginados con filtros
def get_comments_paginated(limit: int, offset: int, search: str = "", sentiment: str = "", emotion: str = ""):
    query = """
        SELECT
            text,
            author,
            published_at,
            likes,
            sentiment,
            emotion,
            channel_name,
            video_title,
            yt_comment_id,
            yt_video_id
        FROM v_comments_latest
        WHERE text IS NOT NULL
    """
    params = {
        "limit": limit,
        "offset": offset,
    }

    if search:
        query += " AND text ILIKE %(search)s"
        params["search"] = f"%{search}%"

    if sentiment:
        query += " AND sentiment = %(sentiment)s"
        params["sentiment"] = sentiment

    if emotion:
        query += " AND emotion = %(emotion)s"
        params["emotion"] = emotion

    query += """
        ORDER BY published_at DESC
        LIMIT %(limit)s OFFSET %(offset)s
    """

    return pd.read_sql(query, engine, params=params)

# Comentarios destacados (likes)
def get_highlighted_analyzed_comments(limit: int):
    query = """
        SELECT
            text,
            author,
            published_at,
            likes,
            sentiment,
            emotion,
            channel_name,
            video_title
        FROM v_comments_latest
        WHERE text IS NOT NULL
        ORDER BY likes DESC
        LIMIT %(limit)s;
    """
    return pd.read_sql(query, engine, params={"limit": limit})

# Tendencia mensual por años
def get_monthly_comments_by_year():

    query = """
        SELECT
            TO_CHAR(published_at, 'YYYY') AS year,
            TO_CHAR(published_at, 'MM') AS month,
            COUNT(*) AS total_comments
        FROM v_comments_latest
        GROUP BY year, month
        ORDER BY year, month ASC;
    """
    return pd.read_sql(query, engine)

# Texto de comentarios (nube de palabras)
def get_text_all_comments():

    query = """
        SELECT text
        FROM v_comments_latest
        WHERE text IS NOT NULL
    """

    return pd.read_sql(query, engine)