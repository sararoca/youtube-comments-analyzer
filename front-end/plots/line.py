import plotly.express as px

def plot_line(title, x, y, h, color=None, labels=None, x_ticks_vals=None, x_tick_labels=None, hovermode="x unified"):

    fig = px.line(
        x=x,
        y=y,
        color=color,
        markers=True,
        labels=labels,
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    fig.update_layout(
        height=h,
        margin=dict(l=0, r=0, t=60, b=10),
        title={
            "text": title,
            "x": 0.01,
            "xanchor": "left",
            "y": 0.95,
            "yanchor": "top",
            "font": {"size": 26}
        },
        hovermode=hovermode
    )

    if x_ticks_vals is not None and x_tick_labels is not None:
        fig.update_xaxes(
            tickmode="array",
            tickvals=x_ticks_vals,
            ticktext=x_tick_labels
        )

    return fig
