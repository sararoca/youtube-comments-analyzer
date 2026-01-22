import streamlit as st


def set_page(state_key: str, page: int, param_name: str | None):
    st.session_state[state_key] = page
    if param_name:
        st.query_params[param_name] = page


def prev_page(state_key: str, page: int, param_name: str | None):
    set_page(state_key, page - 1, param_name)


def next_page(state_key: str, page: int, param_name: str | None):
    set_page(state_key, page + 1, param_name)


def first_page(state_key: str, param_name: str | None):
    set_page(state_key, 1, param_name)


def last_page(state_key: str, total_pages: int, param_name: str | None):
    set_page(state_key, total_pages, param_name)


def render_pagination(
    page: int,
    total_pages: int,
    state_key: str,
    param_name: str | None = None,
):
    col_first, col_prev, col_center, col_next, col_last = st.columns(
        [1, 1, 2, 1, 1]
    )

    with col_first:
        st.button(
            "Primera",
            disabled=page <= 1,
            use_container_width=True,
            key=f"{state_key}_first",
            on_click=first_page,
            args=(state_key, param_name),
        )

    with col_prev:
        st.button(
            "Anterior",
            disabled=page <= 1,
            use_container_width=True,
            key=f"{state_key}_prev",
            on_click=prev_page,
            args=(state_key, page, param_name),
        )

    with col_center:
        st.markdown(
            f"""
            <div style="text-align:center; padding-top:6px;">
                Página {page} de {total_pages}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_next:
        st.button(
            "Siguiente",
            disabled=page >= total_pages,
            use_container_width=True,
            key=f"{state_key}_next",
            on_click=next_page,
            args=(state_key, page, param_name),
        )

    with col_last:
        st.button(
            "Última",
            disabled=page >= total_pages,
            use_container_width=True,
            key=f"{state_key}_last",
            on_click=last_page,
            args=(state_key, total_pages, param_name),
        )

