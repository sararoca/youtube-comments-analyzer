from wordcloud import WordCloud
import plotly.express as px

def plot_wordcloud(text, stopwords, title, h):

    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color=None,
        mode="RGBA",
        colormap="tab10",
        stopwords=stopwords,
        max_words=30,
        collocations=False,
        prefer_horizontal=1.0,
        min_word_length=3
    ).generate(text)

    fig = px.imshow(wordcloud.to_array())

    fig.update_layout(
        height=h,
        margin=dict(l=0, r=0, t=10, b=0),
        title={
            "text": title,
            "x": 0.01,
            "y": 0.98,          
            "xanchor": "left",
            "yanchor": "top",
            "pad": {"t": 0},   
            "font": {"size": 26}
        },
        xaxis_visible=False,
        yaxis_visible=False,
        hovermode=False
    )

    return fig