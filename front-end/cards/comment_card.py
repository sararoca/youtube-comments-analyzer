import streamlit as st
from utils.utils import EMOTION_LABEL_MAP, EMOTION_COLOR_MAP, SENTIMENT_LABEL_MAP,SENTIMENT_COLOR_MAP

def render_analysis(label: str, bg_color: str):
    st.markdown(
        f"""
        <div style="
            background-color:{bg_color};
            padding:6px 8px;
            border-radius:6px;
            text-align:center;
            font-weight:600;
            font-size:12px;
        ">
            {label}
        </div>
        """,
        unsafe_allow_html=True
    )


def comment_card(comment: dict, h: int):
    
    # Esta URL no te lleva al comentario específico, para que te lleve se deben cumplir muchos requisitos 
    # (top-level (no respuesta), no oculto por filtros, sesión iniciada, comentario sigue existiendo, vídeo con los comentarios cargados
    # youtube_url = (
    #     f"https://www.youtube.com/watch?v={comment['yt_video_id']}"
    #     f"&lc={comment['yt_comment_id']}"
    # ) 

    with st.container(border=True, height=h):

        # Cabecera
        col_title, col_sentiment, col_emotion = st.columns(
            [6, 1.5, 1.5],
            vertical_alignment="top"
        )

        # --- Canal · Vídeo ---
        with col_title:
            parts = []
            if comment.get("channel_name"):
                parts.append(comment["channel_name"])
            if comment.get("video_title"):
                parts.append(comment["video_title"])

            st.markdown(
                f"**{' · '.join(parts)}**" if parts else "&nbsp;",
                unsafe_allow_html=True
            )

        # --- Sentimiento ---
        with col_sentiment:
            raw = comment.get("sentiment")
            if raw:
                render_analysis(
                    label=SENTIMENT_LABEL_MAP.get(raw, raw),
                    bg_color=SENTIMENT_COLOR_MAP.get(raw, "#F4F6F7"),
                )

        # --- Emoción ---
        with col_emotion:
            raw = comment.get("emotion")
            if raw:
                render_analysis(
                    label=EMOTION_LABEL_MAP.get(raw, raw),
                    bg_color=EMOTION_COLOR_MAP.get(raw, "#F4F6F7"),
                )

        # --- Author + Date + Likes ---
        author = comment.get("author", "Usuario")
        date = comment["published_at"].strftime("%d-%m-%Y %H:%M")
        likes = comment.get("likes", 0)

        st.markdown(f" {likes} likes | {date} |  {author} ")
        

        # --- Texto ---
        st.markdown(comment.get("text", ""))
        # st.markdown(comment.get("text", "") + f"""
        # <a href="{youtube_url}" target="_blank">
        #     <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg"
        #          width="28"
        #          style="margin-top:4px;">
        # </a>
        # """,
        # unsafe_allow_html=True)
