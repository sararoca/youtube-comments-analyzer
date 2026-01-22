CREATE OR REPLACE VIEW v_channel_stats_history AS
SELECT
    ch.id            AS channel_id,
    ch.channel_id    AS yt_channel_id,
    ch.name,
    ch.description,          
    ch.thumbnail_url,        
    ch.created_at,

    cs.fetched_at            AS fetched_at,
    cs.subscriber_count      AS subscribers,
    cs.view_count            AS views,
    cs.video_count           AS videos
FROM channels ch
JOIN channel_stats cs ON ch.id = cs.channel_id;


CREATE OR REPLACE VIEW v_channel_latest AS
SELECT DISTINCT ON (channel_id)
    *
FROM v_channel_stats_history
ORDER BY channel_id, fetched_at DESC;


CREATE OR REPLACE VIEW v_channel_growth_timeseries AS
SELECT
    channel_id,
    fetched_at::date AS date,
    subscribers,
    views,
    videos
FROM v_channel_stats_history;


CREATE OR REPLACE VIEW v_sentiment_latest AS
SELECT DISTINCT ON (comment_id)
    comment_id,
    label    AS sentiment,
    score
FROM sentiment_analysis
ORDER BY comment_id, analyzed_at DESC;

CREATE OR REPLACE VIEW v_emotion_latest AS
SELECT DISTINCT ON (comment_id)
    comment_id,
    label    AS emotion,
    score
FROM emotion_analysis
ORDER BY comment_id, analyzed_at DESC;


CREATE OR REPLACE VIEW v_comments_analysis AS
SELECT
    c.id          AS comment_internal_id,
    c.video_id,
    c.published_at
FROM comments c;


CREATE OR REPLACE VIEW v_video_stats_history AS
SELECT
    v.id                AS video_id,
    v.video_id          AS yt_video_id,

    ch.id               AS channel_id,
    ch.name             AS channel_name,

    v.title,
    v.published_at,
    v.duration,
    v.thumbnail_url,
    v.video_url,
    v.description,       

    vs.fetched_at       AS fetched_at,
    vs.view_count       AS views,
    vs.like_count       AS likes,
    vs.comment_count    AS comments
FROM videos v
JOIN channels ch ON v.channel_id = ch.id
JOIN video_stats vs ON v.id = vs.video_id;


CREATE OR REPLACE VIEW v_video_latest AS
SELECT DISTINCT ON (video_id)
    *
FROM v_video_stats_history
ORDER BY video_id, fetched_at DESC;


CREATE OR REPLACE VIEW v_video_growth_timeseries AS
SELECT
    video_id,
    channel_name,
    fetched_at::date AS date,
    views,
    likes,
    comments
FROM v_video_stats_history;

CREATE OR REPLACE VIEW v_comments_latest AS
SELECT DISTINCT ON (c.id)
    c.id                    AS comment_id,
    c.comment_id            AS yt_comment_id,

    c.video_id,
    v.title                 AS video_title,
    v.video_id              AS yt_video_id,

    ch.id                   AS channel_id,
    ch.name                 AS channel_name,

    c.author,
    c.text,
    c.published_at,

    cs.fetched_at           AS fetched_at,
    cs.like_count           AS likes,

    s.sentiment,
    s.score                 AS sentiment_score,

    e.emotion,
    e.score                 AS emotion_score
FROM comments c
JOIN videos v ON c.video_id = v.id
JOIN channels ch ON v.channel_id = ch.id
JOIN comment_stats cs ON c.id = cs.comment_id
JOIN v_sentiment_latest s ON c.id = s.comment_id
JOIN v_emotion_latest e ON c.id = e.comment_id
ORDER BY c.id, cs.fetched_at DESC;


CREATE OR REPLACE VIEW v_video_sentiment AS
SELECT
    video_id,
    sentiment,
    COUNT(*) AS total_comments
FROM v_comments_latest
GROUP BY video_id, sentiment;


CREATE OR REPLACE VIEW v_video_emotion AS
SELECT
    video_id,
    emotion,
    COUNT(*) AS total_comments
FROM v_comments_latest
GROUP BY video_id, emotion;


CREATE OR REPLACE VIEW v_video_emotion_timeseries AS
SELECT
    video_id,
    published_at::date AS date,
    emotion,
    COUNT(*) AS total
FROM v_comments_latest
GROUP BY video_id, published_at::date, emotion;


CREATE OR REPLACE VIEW v_video_sentiment_timeseries AS
SELECT
    video_id,
    published_at::date AS date,
    sentiment,
    COUNT(*) AS total
FROM v_comments_latest
GROUP BY video_id, published_at::date, sentiment;


CREATE OR REPLACE VIEW v_comments_sentiment_summary AS
SELECT
    sentiment,
    COUNT(*) AS total_comments
FROM v_comments_latest
GROUP BY sentiment;


CREATE OR REPLACE VIEW v_comments_emotion_summary AS
SELECT
    emotion,
    COUNT(*) AS total_comments
FROM v_comments_latest
GROUP BY emotion;


CREATE OR REPLACE VIEW v_comments_sentiment_timeseries AS
SELECT
    published_at::date AS date,
    sentiment,
    COUNT(*) AS total
FROM v_comments_latest
GROUP BY published_at::date, sentiment;


CREATE OR REPLACE VIEW v_comments_emotion_timeseries AS
SELECT
    published_at::date AS date,
    emotion,
    COUNT(*) AS total
FROM v_comments_latest
GROUP BY published_at::date, emotion;
