import plotly.graph_objects as go


def plot_kpis_row(title, kpis, h): 

    fig = go.Figure()

    n = len(kpis)

    for i, (label, value) in enumerate(kpis):

        fig.add_trace(
            go.Indicator(
                mode="number",
                value=value,
                title={"text": label, "font": {"size": 14}},
                number={"font": {"size": 34}},
                domain={"x": [i / n, (i + 1) / n], "y": [0, 1]}
            )
        )

    fig.update_layout(
        height=h,
        margin=dict(l=10, r=10, t=50, b=0),
        title={
            "text": title,
            "x": 0.01,
            "xanchor": "left",
            "font": {
                "size": 24,
            }
        }
    )

    return fig


def plot_mini_kpi(title, value, h):
    
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            mode="number",
            value=value,
            number={"font": {"size": 36}},
            domain={"x": [0, 0.35], "y": [0.35, 1]}
        )
    )

    fig.update_layout(
        height=h,
        margin=dict(l=10, r=10, t=40, b=0),
        title={
            "text": title,
            "x": 0.01,
            "xanchor": "left",
            "y": 0.95,
            "yanchor": "top",
            "font": {"size": 22}
        }
    )

    return fig
