import streamlit as st
from components.pagination import render_pagination
from services.pagination_service import paginate
from cards.channel_card import channel_card
from services.filters_service import init_filters, get_filters
from components.filters import render_filters_for_channels
from db import queries


HEIGHT = 350
PAGE_SIZE = 6

STATE_KEY = "channelsPage"
PARAM_NAME = "channelsPage"

FILTERS_STATE_KEY = "channels_filters"
FILTERS_PARAM_NAME = "filters"

FILTER_CHANNELS_DEFAULTS = {
    "name": "",
    "min_views": None,
    "min_subscribers": None,
}


st.set_page_config(page_title="YouTube Comments Analyzer - Canales", layout="wide")

st.title("Canales")
st.divider()

raw_page = st.query_params.get(PARAM_NAME) # Leemos el parámetro de la URL

try:
    page_from_url = int(raw_page) # Pasamos de string a int
except (TypeError, ValueError):
    page_from_url = 1 # Por defecto, será 1

page_from_url = max(1, page_from_url) # Se evita pag = 0 o -3, p.ej

if STATE_KEY not in st.session_state:
    st.session_state[STATE_KEY] = page_from_url # Evitar que cada rerun vuelva a la pag 1


init_filters(FILTERS_STATE_KEY, FILTER_CHANNELS_DEFAULTS) # Inicializamos los filtros 

# Renderizamos la barra de filtros
render_filters_for_channels(
    state_key=FILTERS_STATE_KEY,
    defaults=FILTER_CHANNELS_DEFAULTS,
    param_name=FILTERS_PARAM_NAME,
    page_state_key=STATE_KEY,
)

st.divider()

# Nos quedamos con los filtros introducidos para hacer la búsqueda de canales
filters = get_filters(FILTERS_STATE_KEY)


total_channels = queries.count_channnels(name=filters["name"], min_views=filters["min_views"], min_subscribers=filters["min_subscribers"])


pagination = paginate(
    total_items=total_channels,
    page=st.session_state[STATE_KEY],
    page_size=PAGE_SIZE
)

channels_df = queries.get_channels_paginated(
    limit=pagination["limit"],
    offset=pagination["offset"],
    name=filters["name"], 
    min_views=filters["min_views"], 
    min_subscribers=filters["min_subscribers"]
)

channels_page = channels_df.to_dict("records")

# Renderizamos la barra de paginación
render_pagination(
    page=pagination["page"],
    total_pages=pagination["total_pages"],
    state_key=STATE_KEY,
    param_name=PARAM_NAME,
)

st.divider()

# Si con la búsqueda de canales no se han encontrado, avisamos al usuario
if len(channels_page) == 0:
    st.info("No hay canales disponibles")

col1, col2 = st.columns(2)

for idx, channel in enumerate(channels_page):
    with col1 if idx % 2 == 0 else col2:
        channel_card(channel, HEIGHT) # Renderizamos cada canal
