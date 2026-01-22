from db import queries
from services.emotion_service import prepare_emotion_pie
from services.sentiment_service import prepare_sentiment_pie
from services.kpis_service import get_kpis_global_and_avg_row, get_global_count_row
from services.timeseries_service import prepare_monthly_trend
from plots.kpis import plot_kpis_row, plot_mini_kpi
from plots.pie import plot_pie
from plots.wordcloud import plot_wordcloud
from plots.line import plot_line
from cards.comment_card import comment_card
from utils import utils
import streamlit as st
import re

# -------------------------------------------- PÁGINA STREAMLIT ---------------------------------------

st.set_page_config(page_title="YouTube Comments Analyzer", layout="wide", initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 200px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 200px;
        margin-left: -200px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("YouTube True Crime Analytics")

st.divider()

df_counts = queries.get_global_counts()
counts_data = get_global_count_row(df_counts)

col_videos, col_space1, col_comments, col_space2, col_channels = st.columns(
    [1.2, 0.4, 1.2, 0.4, 1.2]
)

with col_videos:
    with st.container(border=True):

        fig_videos = plot_mini_kpi(
            title="Vídeos analizados",
            value=counts_data["total_videos"],
            h=80
        )
        st.plotly_chart(fig_videos, use_container_width=True)

        if st.button(
            "Explorar vídeos",
            use_container_width=True,
            key="btn_videos"
        ):
            st.switch_page("pages/03_🎥_Vídeos.py")

with col_comments:
    with st.container(border=True):

        fig_comments = plot_mini_kpi(
            title="Comentarios analizados",
            value=counts_data["total_comments"],
            h=80
        )
        st.plotly_chart(fig_comments, use_container_width=True)

        if st.button(
            "Explorar comentarios",
            use_container_width=True,
            key="btn_comments"
        ):
            st.switch_page("pages/04_💬_Comentarios.py")

with col_channels:
    with st.container(border=True):

        fig_channels = plot_mini_kpi(
            title="Canales detectados",
            value=counts_data["total_channels"],
            h=80
        )
        st.plotly_chart(fig_channels, use_container_width=True)

        if st.button(
            "Explorar canales",
            use_container_width=True,
            key="btn_channels"
        ):
            st.switch_page("pages/02_📺_Canales.py")

st.divider()

df_kpis = queries.get_global_and_avg_kpis()
kpis_data = get_kpis_global_and_avg_row(df_kpis)

if kpis_data:

    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            fig_kpis_globales = plot_kpis_row(
                title="KPIs globales",
                kpis=kpis_data["global"],
                h=160
            )
            st.plotly_chart(fig_kpis_globales, use_container_width=True)

    with right:
        with st.container(border=True):
            fig_kpis_avg = plot_kpis_row(
                title="Medias por vídeo",
                kpis=kpis_data["avg"],
                h=160
            )
            st.plotly_chart(fig_kpis_avg, use_container_width=True)
else:
    st.warning("No se han podido obtener los KPIs")

st.divider()

df_emotions = queries.get_global_emotion()
emotion_data = prepare_emotion_pie(df_emotions, utils.EMOTION_LABEL_MAP, utils.EMOTION_COLOR_MAP)

df_sentiment = queries.get_global_sentiment()
sentiment_data = prepare_sentiment_pie(df_sentiment, utils.SENTIMENT_LABEL_MAP, utils.SENTIMENT_COLOR_MAP)

df_trend = queries.get_monthly_comments_by_year()
trend_data = prepare_monthly_trend(df_trend, utils.MONTH_MAP)

col_comments_month_by_year, col_emotion, col_sentiment = st.columns([1.8,1.1,1.1])

with col_comments_month_by_year:
    with st.container(border=True):

        fig_month_trend = plot_line(
            title="Tendencia mensual por año",
            x=trend_data["x"],
            y=trend_data["y"],
            color=trend_data["color"],
            labels=trend_data["labels"],
            x_ticks_vals=trend_data["x_ticks_vals"],
            x_tick_labels=trend_data["x_tick_labels"],
            h=300
        )

        st.plotly_chart(fig_month_trend, use_container_width=True)

with col_emotion:
    with st.container(border=True):

        fig_emotion = plot_pie(
            title="Emociones detectadas",
            labels=emotion_data["labels"],
            values=emotion_data["values"],
            color_map=emotion_data["colors"],
            legend_title="Emociones",
            h=300
        )
        st.plotly_chart(fig_emotion, use_container_width=True)

with col_sentiment:
    with st.container(border=True):

        fig_sentiment = plot_pie(
            title="Análisis de sentimiento",
            labels=sentiment_data["labels"],
            values=sentiment_data["values"],
            color_map=sentiment_data["colors"],
            legend_title="Sentimiento",
            h=300
        )
        st.plotly_chart(fig_sentiment, use_container_width=True)

st.divider()

df_all_comments = queries.get_text_all_comments()
text = " ".join(df_all_comments["text"].astype(str).tolist()) 

# Definimos las stopwords
stopwords = utils.SPANISH_STOPWORDS | utils.YOUTUBE_LANGUAGE

df_highlighted = queries.get_highlighted_analyzed_comments(limit=3)
highlighted_comments = df_highlighted.to_dict("records")

col_wordcloud, col_comments_highlighted = st.columns([1, 2])

with col_wordcloud:
    with st.container(border=True, height=430): 
        fig_wordcloud = plot_wordcloud(
            text=text,
            stopwords=stopwords,
            title="Nube de palabras",
            h=350
        )
        st.plotly_chart(fig_wordcloud, use_container_width=True)

with col_comments_highlighted:
    with st.container(border=True, height=430):

        st.subheader("Comentarios destacados")

        for comment in highlighted_comments:
            comment_card(comment, 200)

