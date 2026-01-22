
import streamlit as st
from components.pagination import render_pagination
from services.pagination_service import paginate
from cards.video_card import video_card
from services.filters_service import init_filters, get_filters
from components.filters import render_filters_for_videos
from db import queries


HEIGHT = 400
PAGE_SIZE = 4

STATE_KEY = "videosPage"
PARAM_NAME = "videosPage"

FILTERS_STATE_KEY = "videos_filters"
FILTERS_PARAM_NAME = "filters"

FILTER_VIDEOS_DEFAULTS = {
    "title": "",
    "channel": "",
    "min_likes": None,
}


st.set_page_config(page_title="YouTube Comments Analyzer - Vídeos", layout="wide",)

st.title("Vídeos")
st.divider()

raw_page = st.query_params.get(PARAM_NAME) # Leemos el parámetro de la URL

try:
    page_from_url = int(raw_page) # Pasamos de string a int
except (TypeError, ValueError):
    page_from_url = 1

page_from_url = max(1, page_from_url) # Por defecto, será 1

if STATE_KEY not in st.session_state:
    st.session_state[STATE_KEY] = page_from_url # Evitar que cada rerun vuelva a la pag 1


init_filters(FILTERS_STATE_KEY, FILTER_VIDEOS_DEFAULTS)  # Inicializamos los filtros 

# Renderizamos la barra de filtros
render_filters_for_videos(
    state_key=FILTERS_STATE_KEY,
    defaults=FILTER_VIDEOS_DEFAULTS,
    param_name=FILTERS_PARAM_NAME,
    page_state_key=STATE_KEY,
)

st.divider()

# Nos quedamos con los filtros introducidos para hacer la búsqueda de videos
filters = get_filters(FILTERS_STATE_KEY) 

total_videos = queries.count_videos(title=filters["title"], channel=filters["channel"], min_likes=filters["min_likes"])

pagination = paginate(
    total_items=total_videos,
    page=st.session_state[STATE_KEY],
    page_size=PAGE_SIZE,
)

videos_df = queries.get_videos_paginated(
    limit=pagination["limit"],
    offset=pagination["offset"],
    title=filters["title"], 
    channel=filters["channel"], 
    min_likes=filters["min_likes"]
)

videos_page = videos_df.to_dict("records")


# Renderizamos la barra de paginación
render_pagination(
    page=pagination["page"],
    total_pages=pagination["total_pages"],
    state_key=STATE_KEY,
    param_name=PARAM_NAME,
)

st.divider()

# Si con la búsqueda de videos no se han encontrado, avisamos al usuario
if len(videos_page) == 0:
    st.info("No hay vídeos disponibles")

col1, col2 = st.columns(2)

for idx, video in enumerate(videos_page):
    with col1 if idx % 2 == 0 else col2:
        video_card(video, HEIGHT) # Renderizamos cada comentario
