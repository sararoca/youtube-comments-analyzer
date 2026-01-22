import plotly.express as px

def plot_pie(title, labels, values, color_map, legend_title, h):

    fig = px.pie(
        names=labels,
        values=values,
        hole=0.4,
        color=labels.astype(str),
        color_discrete_map=color_map
    )

    fig.update_layout(
        height=h,
        margin=dict(t=60, b=10, l=0, r=0),
        title={
            "text": title,
            "x": 0.01,
            "xanchor": "left",
            "font": {
                "size": 24,
            }
        },
        legend_title_text=legend_title
    )

    fig.update_traces(
        textinfo="percent",
        textposition="inside",
        hovertemplate="<b>%{label}</b><br>%{value} comentarios"
    )

    return fig