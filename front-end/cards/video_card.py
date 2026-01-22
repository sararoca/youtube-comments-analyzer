import streamlit as st
from st_clickable_images import clickable_images
import time

st.markdown("""
<style>
.desc-box {
    max-height: 140px;
    overflow-y: auto;
    padding-right: 0.5rem;
}
</style>
""", unsafe_allow_html=True)


def video_card(video: dict, h:int):

    with st.container(border=True, height=h):

        col_img, col_info = st.columns([1, 3])

        with col_img:
            if video.get("image"):

                clicked = clickable_images(
                    [video["image"]], 
                    titles=["Imagen #1"],
                    div_style={"display": "flex", "justify-content": "start"},
                    img_style={"margin": "5px", "height": "90px"},
                )

                time.sleep(0.1)

                if clicked == 0:

                    st.session_state["video_seleccionado"] = video["video_id"]
                    st.switch_page("pages/06_📈_Análisis_de_vídeo.py")            

        with col_info:
            
            title_col, icon_col = st.columns([4, 1])

            with title_col:
                st.subheader(video["title"])

            with icon_col:
                st.markdown(
                    f"""
                    <a href="{video["video_url"]}" target="_blank">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg"
                             width="32"
                             style="float:right; margin-top:8px;">
                    </a>
                    """,
                    unsafe_allow_html=True
                )

            fecha = video["published_at"].strftime("%d-%m-%Y")
            st.caption(f"### {video['channel_name']}")
            st.caption(f"Se publicó el {fecha}")

        with st.expander("Ver descripción", expanded=False):

            if video.get("description"):
                st.markdown(
                    f"<div class='desc-box'>{video['description']}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div class='desc-box'>No hay descripción para este vídeo.</div>",
                    unsafe_allow_html=True
                )

        spacerl, c1, c2, c3, spacerr = st.columns([0.1, 1.5, 1.5, 1.7, 0.1])
        c1.metric("Visualizaciones", video["views"])
        c2.metric("Likes", video["likes"])
        c3.metric("Comentarios", video["comments"])
