def get_kpis_global_and_avg_row(df):
    
    row = df.iloc[0] # La tabla solo tiene una fila

    return {
        "global": [
            ("Visualizaciones", int(row.total_views)),
            ("Likes", int(row.total_likes)),
            ("Comentarios", int(row.total_comments)),
        ],
        "avg": [
            ("Visualizaciones", int(row.avg_views)),
            ("Likes", int(row.avg_likes)),
            ("Comentarios", int(row.avg_comments)),
        ]
    }

def get_global_count_row(df):
    row = df.iloc[0] # La tabla solo tiene una fila

    return {
        "total_videos": int(row.total_videos),
        "total_comments": int(row.total_comments),
        "total_channels": int(row.total_channels),
    }
