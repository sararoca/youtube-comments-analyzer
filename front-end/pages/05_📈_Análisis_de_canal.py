import streamlit as st
from db import queries
from utils import utils
from services.channels_service import get_channel_detail
from services.timeseries_service import prepare_channel_growth_timeseries
from services.emotion_service import prepare_emotion_pie
from services.sentiment_service import prepare_sentiment_pie
from services.pagination_service import paginate
from plots.line import plot_line
from plots.pie import plot_pie
from cards.video_card import video_card
from components.pagination import render_pagination

VIDEOS_PAGE_SIZE = 5
VIDEOS_STATE_KEY = "channel_videos_page"
VIDEOS_PARAM_NAME = "vpage"
VIDEOS_CARD_HEIGHT = 400
STATE_KEY = "canal_seleccionado"
PARAM_NAME = "idChannel"

st.set_page_config(page_title="YouTube Comments Analyzer - Análisis del canal", layout="wide")

st.title("Análisis detallado de canal")
st.divider()

# Comprobamos si se ha pasado un id de canal y si es así actualizamos state_key 
raw_page = st.query_params.get(PARAM_NAME) # Leemos el parámetro de la URL

if raw_page != None: # Si se ha pasado un parametro
    
    st.session_state[STATE_KEY] = raw_page

else: # Si no se ha pasado un parametro, seguiremos comprobando
    pass

if STATE_KEY not in st.session_state: # Comprobamos que tenemos en STATE_KEY

    st.error("No se ha especificado ningún canal")
    st.stop()

else:

    canal_id = st.session_state["canal_seleccionado"]

    df_channel = queries.get_channel_by_id(int(canal_id))
    channel = get_channel_detail(df_channel)

    if not channel: # Puede ser que el ID no se encuentre
        st.error("Canal no encontrado") 
        st.stop()

    else:

        youtube_url = f"https://www.youtube.com/channel/{channel['yt_channel_id']}"

        with st.container(border=True, height=450):
            col_img, col_info = st.columns([1.2, 3.8])

            with col_img:
                st.image(channel["thumbnail_url"], use_container_width=True)

            with col_info:
                st.title(f"{channel['name']}")
                st.caption(
                    f"Creado el {channel['created_at'].strftime('%d-%m-%Y')}"
                )

                col_yt, col_m1, col_m2, col_m3 = st.columns([1.6, 1, 1, 1])
                
                with col_yt:

                    st.markdown(
                        f"""
                        <a href="{youtube_url}" target="_blank">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg"
                                width="180"
                                style="float:left; margin-top:8px;">
                        </a>
                        """,
                        unsafe_allow_html=True
                    )

                    df_kpis = queries.get_channel_kpis(channel["channel_id"])
                    kpis = df_kpis.iloc[0]
            
                    col_m1.metric("Vídeos", kpis["videos"])
                    col_m2.metric("Visualizaciones", kpis["views"])
                    col_m3.metric("Suscriptores", kpis["subscribers"])

    st.divider()

    
        
    raw_page = st.query_params.get(VIDEOS_PARAM_NAME)

    try:
        page_from_url = int(raw_page)
    except (TypeError, ValueError):
        page_from_url = 1

    page_from_url = max(1, page_from_url)

    if VIDEOS_STATE_KEY not in st.session_state:
        st.session_state[VIDEOS_STATE_KEY] = page_from_url

    col_comments, col_charts = st.columns([3, 2])
        
    with col_comments:
        with st.container(border=True):

            st.subheader("Vídeos analizados del canal")

            # Vídeos analizados del canal
            total_comments = queries.count_videos_by_channel(int(channel["channel_id"]))

            pagination = paginate(
                total_items=total_comments,
                page=st.session_state[VIDEOS_STATE_KEY],
                page_size=VIDEOS_PAGE_SIZE,
            )

            videos_df = queries.get_channel_videos_paginated(
                channel_id=int(channel["channel_id"]),
                limit=pagination["limit"],
                offset=pagination["offset"],
            )

            videos_page = videos_df.to_dict("records")

            # Render videos
            for video in videos_page:
                video_card(video, VIDEOS_CARD_HEIGHT)

            # Paginación
            render_pagination(
                page=pagination["page"],
                total_pages=pagination["total_pages"],
                state_key=VIDEOS_STATE_KEY,
                param_name=VIDEOS_PARAM_NAME,
            )

    with col_charts:

        df_channel_sentiment = queries.get_channel_sentiment(int(channel["channel_id"]))
        if not df_channel_sentiment.empty:
            sentiment_data = prepare_sentiment_pie(
                df_channel_sentiment,
                utils.SENTIMENT_LABEL_MAP,
                utils.SENTIMENT_COLOR_MAP
            )
            with st.container(border=True):
                fig_sentiment = plot_pie(
                    title="Distribución agregada de sentimiento",
                    labels=sentiment_data["labels"],
                    values=sentiment_data["values"],
                    color_map=sentiment_data["colors"],
                    legend_title="Sentimiento",
                    h=300
                )
                st.plotly_chart(fig_sentiment, use_container_width=True)
        else:
            st.info("No hay datos de sentimiento para este canal.")

        df_channel_emotion = queries.get_channel_emotion(int(channel["channel_id"]))
        if not df_channel_emotion.empty:
            emotion_data = prepare_emotion_pie(
                df_channel_emotion,
                utils.EMOTION_LABEL_MAP,
                utils.EMOTION_COLOR_MAP
            )
            with st.container(border=True):
                fig_emotion = plot_pie(
                    title="Distribución agregada de emociones",
                    labels=emotion_data["labels"],
                    values=emotion_data["values"],
                    color_map=emotion_data["colors"],
                    legend_title="Emociones",
                    h=300
                )
                st.plotly_chart(fig_emotion, use_container_width=True)
        else:
            st.info("No hay datos de emociones para este canal.")

 
        df_channel_growth = queries.get_channel_growth_timeseries(int(channel["channel_id"]))
        growth_data = prepare_channel_growth_timeseries(df_channel_growth)

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
            st.info("No hay datos de interacción para este canal.")

