import pandas as pd

def prepare_sentiment_pie(df, label_map, color_map):
   
   df = df.copy()
   
   df["label_mapped"] = df["sentiment"].map(
        lambda x: label_map.get(x, x)
    )
   
   return {
        "labels": df["label_mapped"],
        "values": df["total_comments"],
        "colors": {
            label_map.get(k, k): v for k, v in color_map.items()
        }

    }
