import streamlit as st
from db import queries
from utils import utils
from services.videos_service import get_video_detail
from services.emotion_service import prepare_emotion_pie
from services.sentiment_service import prepare_sentiment_pie
from services.timeseries_service import prepare_video_growth_timeseries
from services.pagination_service import paginate
from plots.pie import plot_pie
from plots.line import plot_line
from cards.comment_card import comment_card
from components.pagination import render_pagination
from services.comments_service import get_comments_detail

COMMENTS_PAGE_SIZE = 5
COMMENTS_STATE_KEY = "video_comments_page"
COMMENTS_PARAM_NAME = "cpage"
COMMENTS_CARD_HEIGHT = 190
STATE_KEY = "video_seleccionado"
PARAM_NAME = "idVideo"

st.set_page_config(page_title="YouTube Comments Analyzer - Análisis del vídeo", layout="wide")

st.title("Análisis detallado de vídeo")
st.divider()

# Comprobamos si se ha pasado un id de video y si es así actualizamos state_key 
raw_page = st.query_params.get(PARAM_NAME) # Leemos el parámetro de la URL

if raw_page != None: # Si se ha pasado un parametro
    
    st.session_state[STATE_KEY] = raw_page

else: # Si no se ha pasado un parametro, seguiremos comprobando
    pass

if STATE_KEY not in st.session_state: # Comprobamos que tenemos en STATE_KEY

    st.error("No se ha especificado ningún vídeo")
    st.stop()

else:

    video_id = st.session_state["video_seleccionado"] # ID del video que vamos a analizar

    if not video_id:
        st.error("No se ha especificado ningún vídeo")
        st.stop()

    else:

        df_video = queries.get_video_by_id(video_id)
        video = get_video_detail(df_video)

        if not video: # Puede ser que el ID no se encuentre
            st.error("Vídeo no encontrado") 
            st.stop()

        with st.container(border=True):
            col_img, col_info = st.columns([1.2, 3.8])

            with col_img:
                st.image(video["thumbnail_url"], use_container_width=True)

            with col_info:
                st.title(f"{video['title']} · {video['channel_name']}")
                st.caption(
                    f"Publicado el {video['published_at'].strftime('%d-%m-%Y')}"
                )

                col_yt, col_m1, col_m2, col_m3 = st.columns([1.6, 1, 1, 1])

                with col_yt:
                    st.markdown(
                        f"""
                        <a href="{video["video_url"]}" target="_blank">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg"
                                width="180">
                        </a>
                        """,
                        unsafe_allow_html=True
                    )

                df_kpis = queries.get_video_kpis(video["video_id"])
                kpis = df_kpis.iloc[0]

                col_m1.metric("Visualizaciones", kpis["views"])
                col_m2.metric("Likes", kpis["likes"])
                col_m3.metric("Comentarios analizados", kpis["analyzed_comments"])

        st.divider()

        with st.container(border=True, height=500):
            st.subheader("Análisis de sentimientos y emociones en los comentarios del vídeo")

            raw_page = st.query_params.get(COMMENTS_PARAM_NAME)

            try:
                page_from_url = int(raw_page)
            except (TypeError, ValueError):
                page_from_url = 1

            page_from_url = max(1, page_from_url)

            if COMMENTS_STATE_KEY not in st.session_state:
                st.session_state[COMMENTS_STATE_KEY] = page_from_url

            col_comments, col_charts = st.columns([3.1, 1.9])
            
            with col_comments:
                with st.container(border=True):

                    st.subheader("Comentarios analizados del vídeo")

                    #  Comentarios analizados del vídeo
                    total_comments = queries.count_comments_by_video(int(video["video_id"]))

                    pagination = paginate(
                        total_items=total_comments,
                        page=st.session_state[COMMENTS_STATE_KEY],
                        page_size=COMMENTS_PAGE_SIZE,
                    )

                    comments_df = queries.get_video_comments_paginated(
                        video_id=int(video["video_id"]),
                        limit=pagination["limit"],
                        offset=pagination["offset"],
                    )

                    comments_page = get_comments_detail(comments_df)

                    # Render comentarios
                    for comment in comments_page:

                        comment_card(comments_page[comment], COMMENTS_CARD_HEIGHT)

                    # Paginación
                    render_pagination(
                        page=pagination["page"],
                        total_pages=pagination["total_pages"],
                        state_key=COMMENTS_STATE_KEY,
                        param_name=COMMENTS_PARAM_NAME,
                    )

            with col_charts:

                    df_video_sentiment = queries.get_video_sentiment(int(video["video_id"]))
                    if not df_video_sentiment.empty:
                        sentiment_data = prepare_sentiment_pie(df_video_sentiment, utils.SENTIMENT_LABEL_MAP, utils.SENTIMENT_COLOR_MAP)
                        with st.container(border=True):
                            fig_sentiment = plot_pie(
                                title="Distribución de sentimiento",
                                labels=sentiment_data["labels"],
                                values=sentiment_data["values"],
                                color_map=sentiment_data["colors"],
                                legend_title="Sentimiento",
                            h=300
                            )
                            st.plotly_chart(fig_sentiment, use_container_width=True)
                    else:
                        st.info("No hay datos de sentimiento para este vídeo.")


                    df_video_emotion = queries.get_video_emotion(int(video["video_id"]))
                    if not df_video_emotion.empty:
                        emotion_data = prepare_emotion_pie(df_video_emotion, utils.EMOTION_LABEL_MAP, utils.EMOTION_COLOR_MAP)
                        with st.container(border=True):
                            fig_emotion = plot_pie(
                                title="Distribución de emociones",
                                labels=emotion_data["labels"],
                                values=emotion_data["values"],
                                color_map=emotion_data["colors"],
                                legend_title="Emociones",
                            h=300
                            )
                            st.plotly_chart(fig_emotion, use_container_width=True)
                    else:
                        st.info("No hay datos de emociones para este vídeo.")
                
                    df_growth = queries.get_video_growth_timeseries(video["video_id"])
                    growth_data = prepare_video_growth_timeseries(df_growth)

                    if growth_data:
                        with(st.container(border=True)):
                            fig = plot_line(
                                title="Tendencias de interacción",
                                x=growth_data["x"],
                                y=growth_data["y"],
                                color=growth_data["color"],
                                labels=growth_data["labels"],
                                h=400
                            )
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No hay datos de interacción para este vídeo.")




