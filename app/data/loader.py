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
    min_reviews_per_user: int = 3,
) -> pd.DataFrame:
    """
    Load Amazon Reviews from HuggingFace datasets.

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

    try:
        # Try the newer format first
        dataset = load_dataset(
            "McAuley-Lab/Amazon-Reviews-2023",
            f"raw_review_{category}",
            split="full",
            streaming=True,
        )
    except Exception as e1:
        logger.warning(f"McAuley dataset failed: {e1}")
        try:
            # Fallback to amazon_us_reviews
            dataset = load_dataset(
                "amazon_us_reviews",
                category,
                split="train",
                streaming=True,
            )
        except Exception as e2:
            logger.warning(f"amazon_us_reviews failed: {e2}")
            # Final fallback: generate synthetic Amazon-like data
            logger.info("Generating synthetic Amazon review data...")
            return _generate_synthetic_reviews("amazon", category, max_reviews, min_reviews_per_user)

    reviews = []
    for i, item in enumerate(dataset):
        if i >= max_reviews:
            break
        # Handle different field names across dataset versions
        review_text = (item.get("text", "") or item.get("review_body", "") or
                       item.get("reviewText", "") or "")
        if not review_text or len(review_text) < 10:
            continue

        rating = item.get("rating", item.get("star_rating", 3))
        try:
            rating = float(rating)
        except (ValueError, TypeError):
            rating = 3.0

        reviews.append({
            "user_id": _hash_user_id(str(item.get("user_id", item.get("customer_id", i)))),
            "item_id": str(item.get("parent_asin", item.get("asin", item.get("product_id", i)))),
            "rating": min(max(rating, 1.0), 5.0),
            "review_text": review_text[:2000],
            "item_name": str(item.get("title", item.get("product_title", f"Product #{i}")))[:200],
            "category": category,
            "timestamp": item.get("timestamp", 0),
        })

        if (i + 1) % 5000 == 0:
            logger.info(f"  Loaded {len(reviews)}/{max_reviews} Amazon reviews...")

    df = pd.DataFrame(reviews)

    # Filter to users with enough reviews
    user_counts = df["user_id"].value_counts()
    active_users = user_counts[user_counts >= min_reviews_per_user].index
    df = df[df["user_id"].isin(active_users)]

    logger.info(
        f"Amazon {category}: {len(df)} reviews from {df['user_id'].nunique()} users "
        f"across {df['item_id'].nunique()} items"
    )

    df.to_parquet(cache_path, index=False)
    return df


def load_yelp_reviews(
    max_reviews: int = 50000,
    min_reviews_per_user: int = 3,
) -> pd.DataFrame:
    """Load Yelp reviews from HuggingFace datasets."""
    cache_path = settings.processed_data_dir / f"yelp_{max_reviews}.parquet"
    if cache_path.exists():
        logger.info(f"Loading cached Yelp data from {cache_path}")
        return pd.read_parquet(cache_path)

    logger.info(f"Downloading Yelp Reviews (up to {max_reviews})...")

    from datasets import load_dataset

    try:
        dataset = load_dataset(
            "Yelp/yelp_review_full",
            split="train",
            streaming=True,
        )
    except Exception as e:
        logger.warning(f"Yelp dataset failed: {e}")
        try:
            dataset = load_dataset("yelp_review_full", split="train", streaming=True)
        except Exception:
            logger.info("Generating synthetic Yelp data...")
            return _generate_synthetic_reviews("yelp", "Restaurants", max_reviews, min_reviews_per_user)

    reviews = []
    for i, item in enumerate(dataset):
        if i >= max_reviews:
            break

        text = item.get("text", "")
        if not text or len(text) < 10:
            continue

        # yelp_review_full uses 'label' (0-4) instead of star ratings
        label = item.get("label", 2)
        rating = float(label) + 1.0  # 0-4 → 1-5

        # Simulate user grouping (real Yelp data doesn't have user IDs in this dataset)
        user_group = i % 2500
        reviews.append({
            "user_id": _hash_user_id(f"yelp_user_{user_group}"),
            "item_id": f"yelp_biz_{i % 3000}",
            "rating": rating,
            "review_text": text[:2000],
            "item_name": f"Business #{i % 3000}",
            "category": "Restaurants",
            "timestamp": 0,
        })

        if (i + 1) % 5000 == 0:
            logger.info(f"  Loaded {len(reviews)}/{max_reviews} Yelp reviews...")

    df = pd.DataFrame(reviews)

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
    min_reviews_per_user: int = 3,
) -> pd.DataFrame:
    """Load Goodreads book reviews from HuggingFace datasets."""
    cache_path = settings.processed_data_dir / f"goodreads_{max_reviews}.parquet"
    if cache_path.exists():
        logger.info(f"Loading cached Goodreads data from {cache_path}")
        return pd.read_parquet(cache_path)

    logger.info(f"Downloading Goodreads Reviews (up to {max_reviews})...")

    from datasets import load_dataset

    try:
        dataset = load_dataset(
            "mohamedemam/Goodreads_book_reviews_dedup",
            split="train",
            streaming=True,
        )
    except Exception as e:
        logger.warning(f"Goodreads dataset failed: {e}")
        logger.info("Generating synthetic Goodreads data...")
        return _generate_synthetic_reviews("goodreads", "Books", max_reviews, min_reviews_per_user)

    reviews = []
    for i, item in enumerate(dataset):
        if i >= max_reviews:
            break

        rating = item.get("rating", item.get("review/score", 3))
        try:
            rating = float(rating)
        except (ValueError, TypeError):
            rating = 3.0

        review_text = str(item.get("review_text", item.get("review/text", "")))
        if not review_text or len(review_text) < 10:
            continue

        reviews.append({
            "user_id": _hash_user_id(str(item.get("user_id", item.get("review/userId", i)))),
            "item_id": str(item.get("book_id", item.get("Id", i))),
            "rating": min(max(rating, 1.0), 5.0),
            "review_text": review_text[:2000],
            "item_name": str(item.get("title", item.get("Title", f"Book #{i}")))[:200],
            "category": "Books",
            "timestamp": 0,
        })

        if (i + 1) % 5000 == 0:
            logger.info(f"  Loaded {len(reviews)}/{max_reviews} Goodreads reviews...")

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


def _generate_synthetic_reviews(
    source: str,
    category: str,
    max_reviews: int,
    min_reviews_per_user: int,
) -> pd.DataFrame:
    """
    Generate synthetic review data when real datasets can't be downloaded.
    Creates realistic-looking data for training and demonstration.
    """
    import numpy as np

    logger.info(f"Generating {max_reviews} synthetic {source} reviews...")

    np.random.seed(42)

    n_users = max(max_reviews // 20, 100)
    n_items = max(max_reviews // 10, 200)

    # Realistic product/business names by category
    item_names = {
        "Electronics": [
            "Samsung Galaxy Buds Pro", "iPhone 15 Case", "Anker USB-C Cable",
            "JBL Flip 6 Speaker", "Logitech MX Master Mouse", "HP LaserJet Printer",
            "Sony WH-1000XM5", "Apple AirPods Pro", "Oraimo Power Bank 20000mAh",
            "Xiaomi Redmi Buds", "Infinix Smart TV 43\"", "Samsung 256GB SD Card",
        ],
        "Restaurants": [
            "Mama Cass Restaurant", "The Place", "Chicken Republic",
            "Kilimanjaro Restaurant", "Sweet Sensation", "Mr Biggs",
            "Domino's Pizza Lekki", "Bukka Hut", "Amala Zone",
            "Yakoyo Suya Spot", "Cafe Neo", "Terra Kulture",
        ],
        "Books": [
            "Things Fall Apart", "Half of a Yellow Sun", "Purple Hibiscus",
            "The Secret Lives of Baba Segi's Wives", "My Sister the Serial Killer",
            "Stay With Me", "An American Marriage", "Americanah",
            "The Fishermen", "Behold the Dreamers", "Children of Blood and Bone",
            "The Death of Vivek Oji",
        ],
    }

    names = item_names.get(category, item_names["Electronics"])

    # Sample review templates
    review_templates = {
        5: [
            "Absolutely amazing product! Best purchase I've made this year.",
            "Exceeded all expectations. Would highly recommend to anyone.",
            "Top quality, fast delivery. Very satisfied with this purchase.",
            "Perfect! Exactly what I needed. Five stars all the way.",
            "Outstanding quality and great value for money. Love it!",
        ],
        4: [
            "Really good product overall. Minor issues but nothing major.",
            "Great quality for the price. Would buy again.",
            "Very satisfied. Works as described, good build quality.",
            "Solid product, does what it promises. Happy with purchase.",
            "Good value, reliable performance. Recommended.",
        ],
        3: [
            "Decent product, nothing special. Gets the job done.",
            "Average quality. It's okay but I expected more for the price.",
            "It works, but there are better options out there.",
            "Mixed feelings. Some features are good, others need improvement.",
            "Okay product. Not bad, not great either.",
        ],
        2: [
            "Disappointed with the quality. Expected much better.",
            "Not worth the money. There are better alternatives.",
            "Below average. Had issues from the first day.",
            "Poor quality compared to what was advertised.",
            "Wouldn't recommend. Had multiple problems.",
        ],
        1: [
            "Terrible product. Complete waste of money.",
            "Worst purchase ever. Broke within a week.",
            "Do not buy this. Total scam.",
            "Absolutely horrible. Returning immediately.",
            "Zero stars if I could. Total disappointment.",
        ],
    }

    reviews = []
    for i in range(max_reviews):
        user_id = _hash_user_id(f"{source}_user_{i % n_users}")
        item_idx = i % n_items
        item_name = names[item_idx % len(names)]

        # Rating distribution: skewed towards positive (realistic)
        rating = int(np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.1, 0.15, 0.35, 0.35]))
        templates = review_templates[rating]
        review_text = templates[i % len(templates)]

        reviews.append({
            "user_id": user_id,
            "item_id": f"{source}_item_{item_idx}",
            "rating": float(rating),
            "review_text": review_text,
            "item_name": item_name,
            "category": category,
            "timestamp": 0,
        })

    df = pd.DataFrame(reviews)

    user_counts = df["user_id"].value_counts()
    active_users = user_counts[user_counts >= min_reviews_per_user].index
    df = df[df["user_id"].isin(active_users)]

    cache_path = settings.processed_data_dir / f"{source}_{max_reviews}.parquet"
    df.to_parquet(cache_path, index=False)

    logger.info(
        f"Synthetic {source}: {len(df)} reviews, "
        f"{df['user_id'].nunique()} users, {df['item_id'].nunique()} items"
    )
    return df


def load_all_datasets(
    amazon_max: int = 50000,
    yelp_max: int = 30000,
    goodreads_max: int = 20000,
) -> pd.DataFrame:
    """Load and combine all three datasets into a unified DataFrame."""
    cache_path = settings.processed_data_dir / "combined_dataset.parquet"
    if cache_path.exists():
        logger.info(f"Loading cached combined dataset from {cache_path}")
        return pd.read_parquet(cache_path)

    dfs = []

    for name, loader, max_n in [
        ("Amazon", load_amazon_reviews, amazon_max),
        ("Yelp", load_yelp_reviews, yelp_max),
        ("Goodreads", load_goodreads_reviews, goodreads_max),
    ]:
        try:
            df = loader(max_reviews=max_n)
            df["source"] = name.lower()
            dfs.append(df)
        except Exception as e:
            logger.error(f"Failed to load {name} data: {e}")

    if not dfs:
        raise RuntimeError("No datasets could be loaded!")

    combined = pd.concat(dfs, ignore_index=True)
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
    """Extract all data for a specific user."""
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
