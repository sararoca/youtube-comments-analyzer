import streamlit as st


def init_filters(state_key: str, defaults: dict):
    if state_key not in st.session_state:
        st.session_state[state_key] = defaults.copy()


def set_filter(
    state_key: str,
    key: str,
    input_key: str,
    param_name: str | None = None,
    page_state_key: str | None = None,
):
    value = st.session_state.get(input_key)
    st.session_state[state_key][key] = value

    if page_state_key:
        st.session_state[page_state_key] = 1  # reset page
        st.query_params[page_state_key] = "1"

    if param_name:
        st.query_params[f"{param_name}_{key}"] = value


def clear_filters(
    state_key: str,
    defaults: dict,
    filtros: str,
    param_name: str | None = None,
    page_state_key: str | None = None

):
    st.session_state[state_key] = defaults.copy()


    # Resetear los inputs del UI
    if filtros == "comments":
        st.session_state[f"{state_key}_search"] = ""
        st.session_state[f"{state_key}_sentiment"] = ""
        st.session_state[f"{state_key}_emotion"] = ""

    elif filtros == "videos":
        st.session_state[f"{state_key}_title"] = ""
        st.session_state[f"{state_key}_channel"] = ""
        st.session_state[f"{state_key}_min_likes"] = 0

    else:
        st.session_state[f"{state_key}_name"] = ""
        st.session_state[f"{state_key}_min_views"] = 0
        st.session_state[f"{state_key}_min_subscribers"] = 0
                
    if page_state_key:
        st.session_state[page_state_key] = 1
        st.query_params[page_state_key] = "1"

    if param_name:
        for k in defaults.keys():
            st.query_params.pop(f"{param_name}_{k}", None)


def get_filters(state_key: str) -> dict:
    return st.session_state.get(state_key, {})
