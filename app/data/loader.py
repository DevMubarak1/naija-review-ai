"""
NaijaReview AI — Dataset Loader
Downloads and preprocesses subsets of Yelp, Amazon Reviews, and Goodreads.
Uses HuggingFace Datasets for efficient streaming to save disk space.
"""

import json
import hashlib
from pathlib import Path
from typing import Optional

import pandas as pd
from loguru import logger

from app.core.config import settings


def _hash_user_id(user_id: str) -> str:
    """Create a short hash for user IDs."""
    return hashlib.md5(user_id.encode()).hexdigest()[:12]


def load_amazon_reviews(
    category: str = "Electronics",
    max_reviews: int = 50000,
    min_reviews_per_user: int = 5,
) -> pd.DataFrame:
    """
    Load Amazon Reviews from HuggingFace datasets.
    Filters to active users with enough reviews for modeling.

    Args:
        category: Product category (Electronics, Books, Movies_and_TV, etc.)
        max_reviews: Maximum number of reviews to load
        min_reviews_per_user: Minimum reviews a user must have to be included

    Returns:
        DataFrame with columns: user_id, item_id, rating, review_text,
                                item_name, category, timestamp
    """
    cache_path = settings.processed_data_dir / f"amazon_{category}_{max_reviews}.parquet"
    if cache_path.exists():
        logger.info(f"Loading cached Amazon {category} data from {cache_path}")
        return pd.read_parquet(cache_path)

    logger.info(f"Downloading Amazon Reviews — {category} (up to {max_reviews} reviews)...")

    from datasets import load_dataset

    # Use the McAuley Lab Amazon Reviews 2023 dataset
    dataset = load_dataset(
        "McAuley-Lab/Amazon-Reviews-2023",
        f"raw_review_{category}",
        split="full",
        streaming=True,
        trust_remote_code=True,
    )

    reviews = []
    for i, item in enumerate(dataset):
        if i >= max_reviews:
            break
        reviews.append({
            "user_id": _hash_user_id(item.get("user_id", str(i))),
            "item_id": item.get("parent_asin", item.get("asin", str(i))),
            "rating": float(item.get("rating", 3)),
            "review_text": item.get("text", ""),
            "item_name": item.get("title", "Unknown Product"),
            "category": category,
            "timestamp": item.get("timestamp", 0),
            "helpful_vote": item.get("helpful_vote", 0),
            "verified_purchase": item.get("verified_purchase", False),
        })

        if (i + 1) % 10000 == 0:
            logger.info(f"  Loaded {i + 1}/{max_reviews} reviews...")

    df = pd.DataFrame(reviews)

    # Filter to users with enough reviews for meaningful modeling
    user_counts = df["user_id"].value_counts()
    active_users = user_counts[user_counts >= min_reviews_per_user].index
    df = df[df["user_id"].isin(active_users)]

    logger.info(
        f"Amazon {category}: {len(df)} reviews from {df['user_id'].nunique()} users "
        f"across {df['item_id'].nunique()} items"
    )

    # Cache to disk
    df.to_parquet(cache_path, index=False)
    return df


def load_yelp_reviews(
    max_reviews: int = 50000,
    min_reviews_per_user: int = 5,
) -> pd.DataFrame:
    """
    Load Yelp reviews from HuggingFace datasets.

    Returns:
        DataFrame with columns: user_id, item_id, rating, review_text,
                                item_name, category, timestamp
    """
    cache_path = settings.processed_data_dir / f"yelp_{max_reviews}.parquet"
    if cache_path.exists():
        logger.info(f"Loading cached Yelp data from {cache_path}")
        return pd.read_parquet(cache_path)

    logger.info(f"Downloading Yelp Reviews (up to {max_reviews})...")

    from datasets import load_dataset

    dataset = load_dataset(
        "Yelp/yelp_review_full",
        split="train",
        streaming=True,
        trust_remote_code=True,
    )

    reviews = []
    for i, item in enumerate(dataset):
        if i >= max_reviews:
            break
        reviews.append({
            "user_id": _hash_user_id(str(i // 20)),  # Simulate user grouping
            "item_id": f"yelp_biz_{i % 5000}",
            "rating": float(item.get("label", 2)) + 1,  # 0-4 → 1-5
            "review_text": item.get("text", ""),
            "item_name": f"Business #{i % 5000}",
            "category": "Restaurants",
            "timestamp": 0,
        })

        if (i + 1) % 10000 == 0:
            logger.info(f"  Loaded {i + 1}/{max_reviews} Yelp reviews...")

    df = pd.DataFrame(reviews)

    # Filter to active users
    user_counts = df["user_id"].value_counts()
    active_users = user_counts[user_counts >= min_reviews_per_user].index
    df = df[df["user_id"].isin(active_users)]

    logger.info(
        f"Yelp: {len(df)} reviews from {df['user_id'].nunique()} users "
        f"across {df['item_id'].nunique()} businesses"
    )

    df.to_parquet(cache_path, index=False)
    return df


def load_goodreads_reviews(
    max_reviews: int = 30000,
    min_reviews_per_user: int = 5,
) -> pd.DataFrame:
    """
    Load Goodreads book reviews from HuggingFace datasets.

    Returns:
        DataFrame with same schema as other loaders.
    """
    cache_path = settings.processed_data_dir / f"goodreads_{max_reviews}.parquet"
    if cache_path.exists():
        logger.info(f"Loading cached Goodreads data from {cache_path}")
        return pd.read_parquet(cache_path)

    logger.info(f"Downloading Goodreads Reviews (up to {max_reviews})...")

    from datasets import load_dataset

    dataset = load_dataset(
        "mohamedemam/Goodreads_book_reviews_dedup",
        split="train",
        streaming=True,
        trust_remote_code=True,
    )

    reviews = []
    for i, item in enumerate(dataset):
        if i >= max_reviews:
            break

        rating = item.get("rating", item.get("review/score", 3))
        try:
            rating = float(rating)
        except (ValueError, TypeError):
            rating = 3.0

        review_text = item.get("review_text", item.get("review/text", ""))
        if not review_text or len(str(review_text)) < 10:
            continue

        reviews.append({
            "user_id": _hash_user_id(str(item.get("user_id", item.get("review/userId", i)))),
            "item_id": str(item.get("book_id", item.get("Id", i))),
            "rating": min(max(rating, 1.0), 5.0),
            "review_text": str(review_text),
            "item_name": str(item.get("title", item.get("Title", f"Book #{i}"))),
            "category": "Books",
            "timestamp": 0,
        })

        if (i + 1) % 10000 == 0:
            logger.info(f"  Loaded {i + 1}/{max_reviews} Goodreads reviews...")

    df = pd.DataFrame(reviews)

    user_counts = df["user_id"].value_counts()
    active_users = user_counts[user_counts >= min_reviews_per_user].index
    df = df[df["user_id"].isin(active_users)]

    logger.info(
        f"Goodreads: {len(df)} reviews from {df['user_id'].nunique()} users "
        f"across {df['item_id'].nunique()} books"
    )

    df.to_parquet(cache_path, index=False)
    return df


def load_all_datasets(
    amazon_max: int = 50000,
    yelp_max: int = 30000,
    goodreads_max: int = 20000,
) -> pd.DataFrame:
    """
    Load and combine all three datasets into a unified DataFrame.
    Each row has: user_id, item_id, rating, review_text, item_name, category, source
    """
    cache_path = settings.processed_data_dir / "combined_dataset.parquet"
    if cache_path.exists():
        logger.info(f"Loading cached combined dataset from {cache_path}")
        return pd.read_parquet(cache_path)

    dfs = []

    # Amazon
    try:
        amazon_df = load_amazon_reviews(max_reviews=amazon_max)
        amazon_df["source"] = "amazon"
        dfs.append(amazon_df)
    except Exception as e:
        logger.error(f"Failed to load Amazon data: {e}")

    # Yelp
    try:
        yelp_df = load_yelp_reviews(max_reviews=yelp_max)
        yelp_df["source"] = "yelp"
        dfs.append(yelp_df)
    except Exception as e:
        logger.error(f"Failed to load Yelp data: {e}")

    # Goodreads
    try:
        goodreads_df = load_goodreads_reviews(max_reviews=goodreads_max)
        goodreads_df["source"] = "goodreads"
        dfs.append(goodreads_df)
    except Exception as e:
        logger.error(f"Failed to load Goodreads data: {e}")

    if not dfs:
        raise RuntimeError("No datasets could be loaded!")

    combined = pd.concat(dfs, ignore_index=True)

    # Clean text
    combined["review_text"] = combined["review_text"].fillna("").astype(str)
    combined = combined[combined["review_text"].str.len() > 10]

    logger.info(
        f"Combined dataset: {len(combined)} reviews, "
        f"{combined['user_id'].nunique()} users, "
        f"{combined['item_id'].nunique()} items, "
        f"Sources: {combined['source'].value_counts().to_dict()}"
    )

    combined.to_parquet(cache_path, index=False)
    return combined


def get_user_data(df: pd.DataFrame, user_id: str) -> dict:
    """
    Extract all data for a specific user.

    Returns dict with:
        - reviews: list of review dicts
        - rating_distribution: dict of rating counts
        - categories: list of preferred categories
        - avg_rating: float
        - avg_review_length: float
    """
    user_df = df[df["user_id"] == user_id]
    if user_df.empty:
        return None

    reviews = user_df.to_dict("records")
    ratings = user_df["rating"].value_counts().to_dict()
    categories = user_df["category"].value_counts().head(5).index.tolist()

    return {
        "user_id": user_id,
        "reviews": reviews,
        "rating_distribution": {str(int(k)): int(v) for k, v in ratings.items()},
        "categories": categories,
        "avg_rating": float(user_df["rating"].mean()),
        "avg_review_length": float(user_df["review_text"].str.split().str.len().mean()),
        "total_reviews": len(reviews),
    }
