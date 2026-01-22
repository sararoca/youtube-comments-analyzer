import streamlit as st
from services.filters_service import set_filter, clear_filters


def render_filters_for_comments(state_key: str, defaults: dict, param_name: str | None = None, page_state_key: str | None = None):

    filters = st.session_state[state_key]


    fSearch, fSentiment, fEmotion, clear = st.columns([3, 2, 2, 1])

    # Filtro de búsque
    with fSearch:
        st.text_input(
            "Buscar palabra clave en comentario",
            value=filters.get("search", ""),
            key=f"{state_key}_search",
            on_change=set_filter,
            args=(
                state_key,
                "search",
                f"{state_key}_search",
                param_name,
                page_state_key,
            ),
        )

    # Filtro de sentimiento
    with fSentiment:
        options = ["", "Positivo", "Neutral", "Negativo"]
        st.selectbox(
            "Sentimiento",
            options,
            index=options.index(filters.get("sentiment", "")),
            key=f"{state_key}_sentiment",
            on_change=set_filter,
            args=(
                state_key,
                "sentiment",
                f"{state_key}_sentiment",
                param_name,
                page_state_key,
            ),
        )

    # Filtro de emocion
    with fEmotion:
        options = ["", "Alegría", "Tristeza", "Ira", "Asco", "Miedo", "Sorpresa", "Neutral", "Otros"]
        st.selectbox(
            "Emoción",
            options,
            index=options.index(filters.get("emotion", "")),
            key=f"{state_key}_emotion",
            on_change=set_filter,
            args=(
                state_key,
                "emotion",
                f"{state_key}_emotion",
                param_name,
                page_state_key,
            ),
        )

    # Limpiar los filtros de los comentarios
    with clear:
        st.markdown("")
        st.markdown("")
        filtros = "comments"
        st.button(
            "Limpiar filtros",
            use_container_width=True,
            on_click=clear_filters,
            args=(
                state_key,
                defaults,
                filtros,
                param_name,
                page_state_key,
            ),
        )

def render_filters_for_videos(
    state_key: str,
    defaults: dict,
    param_name: str | None = None,
    page_state_key: str | None = None,
):
    filters = st.session_state[state_key]

    fTitle, fChannel, fLikes, clear = st.columns([3, 3, 2, 1])

    # Título del vídeo
    with fTitle:
        st.text_input(
            "Buscar por título",
            value=filters.get("title", ""),
            key=f"{state_key}_title",
            on_change=set_filter,
            args=(
                state_key,
                "title",
                f"{state_key}_title",
                param_name,
                page_state_key,
            ),
        )

    # Canal
    with fChannel:
        st.text_input(
            "Buscar por canal",
            value=filters.get("channel", ""),
            key=f"{state_key}_channel",
            on_change=set_filter,
            args=(
                state_key,
                "channel",
                f"{state_key}_channel",
                param_name,
                page_state_key,
            ),
        )

    # Likes mínimos
    with fLikes:
        st.number_input(
            "Likes mínimos",
            min_value=0,
            step=100,
            value=filters.get("min_likes") or 0,
            key=f"{state_key}_min_likes",
            on_change=set_filter,
            args=(
                state_key,
                "min_likes",
                f"{state_key}_min_likes",
                param_name,
                page_state_key,
            ),
        )

    # Limpiar filtros de los videos
    with clear:
        st.markdown("")
        st.markdown("")
        filtros = "videos"
        st.button(
            "Limpiar filtros",
            use_container_width=True,
            on_click=clear_filters,
            args=(
                state_key,
                defaults,
                filtros,
                param_name,
                page_state_key,
            ),
        )

def render_filters_for_channels(
    state_key: str,
    defaults: dict,
    param_name: str | None = None,
    page_state_key: str | None = None,
):
    filters = st.session_state[state_key]

    fName, fViews, fSubs, clear = st.columns([3, 2, 2, 1])

    with fName:
        st.text_input(
            "Nombre del canal",
            value=filters.get("name", ""),
            key=f"{state_key}_name",
            on_change=set_filter,
            args=(state_key, "name", f"{state_key}_name", param_name, page_state_key),
        )

    with fViews:
        st.number_input(
            "Visualizaciones mínimas",
            min_value=0,
            step=1_000,
            value=filters.get("min_views") or 0,
            key=f"{state_key}_min_views",
            on_change=set_filter,
            args=(state_key, "min_views", f"{state_key}_min_views", param_name, page_state_key),
        )

    with fSubs:
        st.number_input(
            "Suscriptores mínimos",
            min_value=0,
            step=1_000,
            value=filters.get("min_subscribers") or 0,
            key=f"{state_key}_min_subscribers",
            on_change=set_filter,
            args=(state_key, "min_subscribers", f"{state_key}_min_subscribers", param_name, page_state_key),
        )

    with clear:
        st.markdown("")
        st.markdown("")
        filtros = "canales"
        st.button(
            "Limpiar filtros",
            use_container_width=True,
            on_click=clear_filters,
            args=(state_key, defaults, filtros, param_name, page_state_key),
        )
