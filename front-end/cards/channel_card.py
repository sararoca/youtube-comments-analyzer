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


def channel_card(channel: dict, h: int):
    
    youtube_url = f"https://www.youtube.com/channel/{channel['yt_channel_id']}"

    with st.container(border=True, height=h):

        left, right = st.columns([1.2, 4.8])

        with left:
            if channel.get("image"):

                clicked = clickable_images(
                    [channel["image"]], 
                    titles=["Imagen #1"],
                    div_style={"display": "flex", "justify-content": "start"},
                    img_style={"margin": "5px", "height": "90px"},
                    key=channel.get("image")
                )

                time.sleep(0.1)

                if clicked == 0:

                    st.session_state["canal_seleccionado"] = channel["channel_id"]
                    st.switch_page("pages/05_📈_Análisis_de_canal.py")   

        with right:

            title_col, icon_col = st.columns([4, 1])

            with title_col:
                st.subheader(channel["name"])

            with icon_col:
                st.markdown(
                    f"""
                    <a href="{youtube_url}" target="_blank">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg"
                             width="32"
                             style="float:right; margin-top:8px;">
                    </a>
                    """,
                    unsafe_allow_html=True
                )

            fecha = channel["created_at"].strftime("%d-%m-%Y")
            st.caption(f"Canal creado el {fecha}")

        with st.expander("Ver descripción", expanded=False):
            if channel.get("description"):
                st.markdown(
                    f"<div class='desc-box'>{channel['description']}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div class='desc-box'>No hay descripción para este canal.</div>",
                    unsafe_allow_html=True
                )

        spacerl, c1, c2, c3, spacerr = st.columns([0.1, 1, 2.2, 1.7, 0.1])
        c1.metric("Vídeos", channel["videos"])
        c2.metric("Visualizaciones", f"{channel['views']:,}")
        c3.metric("Suscriptores", f"{channel['subscribers']:,}")

