import streamlit as st
from db import queries
from utils.utils import SENTIMENT_UI_TO_DB, EMOTION_UI_TO_DB
from cards.comment_card import comment_card
from components.pagination import render_pagination
from services.pagination_service import paginate
from services.filters_service import init_filters, get_filters
from components.filters import render_filters_for_comments


HEIGHT = 200
PAGE_SIZE = 10

STATE_KEY = "commentsPage"
PARAM_NAME = "commentsPage"

FILTERS_STATE_KEY = "comments_filters"
FILTERS_PARAM_NAME = "filters"

FILTER_COMMENTS_DEFAULTS = {
    "search": "",
    "sentiment": "",
    "emotion": "",
}


st.set_page_config(page_title="YouTube Comments Analyzer - Comentarios",layout="wide")

st.title("Comentarios")
st.divider()

raw_page = st.query_params.get(PARAM_NAME) # Leemos el parámetro de la URL

try:
    page_from_url = int(raw_page) # Pasamos de string a int
except (TypeError, ValueError):
    page_from_url = 1 # Por defecto, será 1

page_from_url = max(1, page_from_url) # Se evita pag = 0 o -3, p.ej

if STATE_KEY not in st.session_state:
    st.session_state[STATE_KEY] = page_from_url # Evitar que cada rerun vuelva a la pag 1


init_filters(FILTERS_STATE_KEY, FILTER_COMMENTS_DEFAULTS) # Inicializamos los filtros 

# Renderizamos la barra de filtros
render_filters_for_comments(
    state_key=FILTERS_STATE_KEY,
    defaults=FILTER_COMMENTS_DEFAULTS,
    param_name=FILTERS_PARAM_NAME,
    page_state_key=STATE_KEY,
)

st.divider()

# Nos quedamos con los filtros introducidos para hacer la búsqueda de comentarios
filters = get_filters(FILTERS_STATE_KEY)

# Traducimos los filtros introducidos en la vista para que se correspondan con los de la BD
db_filters = {
    "search": filters["search"],
    "sentiment": SENTIMENT_UI_TO_DB.get(filters["sentiment"], ""),
    "emotion": EMOTION_UI_TO_DB.get(filters["emotion"], ""),
}

# Obtenemos el total de comentarios con los filtros aplicados para saber cuantas pags hay
total_comments = queries.count_comments(search=db_filters["search"], sentiment=db_filters["sentiment"], emotion=db_filters["emotion"])

# Calculamos la paginación
pagination = paginate(
    total_items=total_comments,
    page=st.session_state[STATE_KEY],
    page_size=PAGE_SIZE,
)

# Pedimos a la BD solo los comentarios de esa página
comments_df = queries.get_comments_paginated(
    limit=pagination["limit"],
    offset=pagination["offset"],
    search=db_filters["search"],
    sentiment=db_filters["sentiment"],
    emotion=db_filters["emotion"]
)

# Convertimos df a lista de diccionarios
comments_page = comments_df.to_dict("records")

# Renderizamos la barra de paginación
render_pagination(
    page=pagination["page"],
    total_pages=pagination["total_pages"],
    state_key=STATE_KEY,
    param_name=PARAM_NAME,
)

st.divider()

# Si con la búsqueda de comentarios no se han encontrado, avisamos al usuario
if len(comments_page) == 0:
    st.info("No hay comentarios disponibles")

# Renderizamos los comentarios en dos columnas
col1, col2 = st.columns(2)

for idx, comment in enumerate(comments_page):
    with col1 if idx % 2 == 0 else col2:
        comment_card(comment, HEIGHT) # Renderizamos cada comentario


