import pandas as pd

def prepare_monthly_trend(df, month_map):

    if df.empty:
        return None

    df = df.copy()
    df["month"] = df["month"].astype(int)

    return {
        "x": df["month"],
        "y": df["total_comments"],
        "color": df["year"],
        "labels": {
            "x": "Mes",
            "y": "Nº de comentarios",
            "color": "Año"
        },
        "x_ticks_vals": list(month_map.keys()),
        "x_tick_labels": list(month_map.values())
    }

def prepare_video_growth_timeseries(df):

    if df.empty:
        return None

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%d-%m-%Y")


    df_melted = df.melt(
        id_vars="date",
        value_vars=["views", "likes", "comments"],
        var_name="metric",
        value_name="value"
    )

    df_melted["metric"] = df_melted["metric"].map({
        "views": "Visualizaciones",
        "likes": "Likes",
        "comments": "Comentarios"
    })

    df_melted["value"] = df_melted["value"].astype(int)

    return {
        "x": df_melted["date"],
        "y": df_melted["value"],
        "color": df_melted["metric"],
        "labels": {
            "x": "Fecha",
            "y": "Cantidad",
            "color": "Métrica"
        }
    }


def prepare_channel_growth_timeseries(df):

    if df.empty:
        return None

    df = df.copy()

    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%d-%m-%Y")

    df_melted = df.melt(
        id_vars="date",
        value_vars=["subscribers", "views", "videos"],
        var_name="metric",
        value_name="value"
    )

    df_melted["metric"] = df_melted["metric"].map({
        "subscribers": "Suscriptores",
        "views": "Visualizaciones",
        "videos": "Vídeos"
    })

    df_melted["value"] = df_melted["value"].astype(int)

    return {
        "x": df_melted["date"],
        "y": df_melted["value"],
        "color": df_melted["metric"],
        "labels": {
            "x": "Fecha",
            "y": "Cantidad",
            "color": "Métrica"
        }
    }
