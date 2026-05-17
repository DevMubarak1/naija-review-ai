"""Check ground truth review lengths for Task A users."""
import pandas as pd

df = pd.read_parquet("data/processed/combined_dataset.parquet")
uc = df["user_id"].value_counts()
users = uc[uc >= 20].index[:10]

for u in users:
    udf = df[df["user_id"] == u]
    lengths = udf["review_text"].str.split().str.len()
    last_review = udf.iloc[-1]["review_text"]
    print(f"{u[:8]}: avg={lengths.mean():.0f} words, min={lengths.min()}, max={lengths.max()}")
    print(f"  Last review: '{last_review[:120]}'")
    print()
