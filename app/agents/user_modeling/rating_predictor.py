"""
Hybrid rating predictor combining SVD collaborative filtering with
Combines collaborative filtering, XGBoost with richer features, and LLM reasoning.
Optimized for lower RMSE (target: ≤0.75).
"""

import pickle
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
from loguru import logger
from sklearn.model_selection import train_test_split

from app.core.config import settings
from app.core.llm import llm_client
from app.core.memory import UserProfile


class RatingPredictor:
    """
    Hybrid rating prediction combining:
    1. Statistical baseline (user/item average bias with Bayesian shrinkage)
    2. SVD collaborative filtering (latent user-item factors)
    3. XGBoost with rich engineered features (kept for training analysis)
    """

    def __init__(self):
        self.global_mean = 3.5
        self.user_biases = {}
        self.item_biases = {}
        self.user_counts = {}
        self.item_counts = {}
        self.category_means = {}
        self.user_category_means = {}  # user × category interaction
        self.xgb_model = None
        self.is_trained = False
        self.model_path = settings.processed_data_dir / "rating_model.pkl"
        # SVD collaborative filtering
        self.svd_user_factors = {}   # user_id → latent vector
        self.svd_item_factors = {}   # item_id → latent vector
        self.svd_trained = False

    def train(self, df: pd.DataFrame):
        """Train the rating prediction model on historical data."""
        logger.info(f"Training rating predictor on {len(df)} reviews...")
        self.global_mean = df["rating"].mean()

        # ── Bayesian shrinkage for user/item biases ──
        # Light shrinkage to handle sparse users/items
        shrinkage_strength = 10  # reduced from 25 to preserve signal

        user_groups = df.groupby("user_id")["rating"]
        for uid, group in user_groups:
            n = len(group)
            raw_mean = group.mean()
            # Bayesian shrinkage: blend raw mean toward global mean
            shrunk = (n * raw_mean + shrinkage_strength * self.global_mean) / (n + shrinkage_strength)
            self.user_biases[uid] = shrunk - self.global_mean
            self.user_counts[uid] = n

        item_groups = df.groupby("item_id")["rating"]
        for iid, group in item_groups:
            n = len(group)
            raw_mean = group.mean()
            shrunk = (n * raw_mean + shrinkage_strength * self.global_mean) / (n + shrinkage_strength)
            self.item_biases[iid] = shrunk - self.global_mean
            self.item_counts[iid] = n

        # Category means
        if "category" in df.columns:
            self.category_means = df.groupby("category")["rating"].mean().to_dict()

            # User × category interaction
            for (uid, cat), group in df.groupby(["user_id", "category"]):
                n = len(group)
                if n >= 2:
                    self.user_category_means[(uid, cat)] = group["rating"].mean()

        self._train_xgboost(df)
        self._train_svd(df)
        self.is_trained = True
        self._save_model()
        logger.info(f"Trained. Global mean: {self.global_mean:.2f}")

    def _train_xgboost(self, df: pd.DataFrame):
        """Train XGBoost model on rich engineered features."""
        try:
            import xgboost as xgb
        except ImportError:
            logger.warning("XGBoost not installed, using baseline only")
            return

        features = self._engineer_features(df)
        if features.empty:
            return

        X = features.drop("rating", axis=1)
        y = features["rating"]
        self._xgb_columns = list(X.columns)  # Save for inference
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

        # Optimized hyperparameters for lower RMSE
        self.xgb_model = xgb.XGBRegressor(
            n_estimators=500,
            max_depth=4,
            learning_rate=0.05,
            reg_alpha=0.1,
            reg_lambda=1.0,
            subsample=0.8,
            colsample_bytree=0.8,
            min_child_weight=5,
            objective="reg:squarederror",
            random_state=42,
            n_jobs=-1,
        )
        self.xgb_model.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            verbose=False,
        )

        val_pred = self.xgb_model.predict(X_val)
        rmse = np.sqrt(np.mean((val_pred - y_val) ** 2))
        logger.info(f"XGBoost validation RMSE: {rmse:.4f} ({len(self._xgb_columns)} features)")

    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create rich features for XGBoost."""
        features = pd.DataFrame()
        features["rating"] = df["rating"]
        features["user_bias"] = df["user_id"].map(self.user_biases).fillna(0)
        features["item_bias"] = df["item_id"].map(self.item_biases).fillna(0)

        # User stats
        user_stats = df.groupby("user_id").agg(
            user_review_count=("rating", "count"),
            user_avg_rating=("rating", "mean"),
            user_std_rating=("rating", "std"),
            user_median_rating=("rating", "median"),
        ).fillna(0)
        features = features.join(df[["user_id"]].join(user_stats, on="user_id").drop("user_id", axis=1))

        # Item stats
        item_stats = df.groupby("item_id").agg(
            item_review_count=("rating", "count"),
            item_avg_rating=("rating", "mean"),
            item_std_rating=("rating", "std"),
        ).fillna(0)
        features = features.join(df[["item_id"]].join(item_stats, on="item_id").drop("item_id", axis=1))

        # Review text features
        features["review_length"] = df["review_text"].str.split().str.len().fillna(0)
        features["review_char_count"] = df["review_text"].str.len().fillna(0)
        features["exclamation_count"] = df["review_text"].str.count("!").fillna(0)
        features["question_count"] = df["review_text"].str.count(r"\?").fillna(0)
        features["uppercase_ratio"] = df["review_text"].apply(
            lambda x: sum(1 for c in str(x) if c.isupper()) / max(len(str(x)), 1)
        )

        # Sentiment proxy features (word-level)
        pos_words = {"great", "good", "excellent", "love", "amazing", "best", "perfect", "fantastic", "awesome", "wonderful"}
        neg_words = {"bad", "terrible", "worst", "hate", "awful", "poor", "horrible", "disappointing", "waste", "broken"}
        features["positive_word_count"] = df["review_text"].apply(
            lambda x: sum(1 for w in str(x).lower().split() if w in pos_words)
        )
        features["negative_word_count"] = df["review_text"].apply(
            lambda x: sum(1 for w in str(x).lower().split() if w in neg_words)
        )
        features["sentiment_ratio"] = (features["positive_word_count"] + 1) / (features["negative_word_count"] + 1)

        # Category encoding
        if "category" in df.columns:
            features["category_mean"] = df["category"].map(self.category_means).fillna(self.global_mean)
            category_dummies = pd.get_dummies(df["category"], prefix="cat")
            features = pd.concat([features, category_dummies], axis=1)

        # User-Item interaction: deviation from user mean
        features["user_item_diff"] = features["item_avg_rating"] - features["user_avg_rating"]

        return features.dropna()

    def _train_svd(self, df: pd.DataFrame, n_factors: int = 50):
        """Train SVD collaborative filtering on the user-item matrix."""
        from scipy.sparse import csr_matrix
        from sklearn.decomposition import TruncatedSVD

        try:
            # Build user/item index mappings
            user_ids = sorted(df["user_id"].unique())
            item_ids = sorted(df["item_id"].unique())
            user_idx = {uid: i for i, uid in enumerate(user_ids)}
            item_idx = {iid: i for i, iid in enumerate(item_ids)}

            # Build sparse residual matrix (rating - global_mean - user_bias - item_bias)
            rows, cols, vals = [], [], []
            for _, row in df.iterrows():
                uid, iid, rating = row["user_id"], row["item_id"], row["rating"]
                residual = rating - self.global_mean - self.user_biases.get(uid, 0) - self.item_biases.get(iid, 0)
                rows.append(user_idx[uid])
                cols.append(item_idx[iid])
                vals.append(residual)

            matrix = csr_matrix((vals, (rows, cols)),
                                shape=(len(user_ids), len(item_ids)))

            # Truncated SVD
            svd = TruncatedSVD(n_components=min(n_factors, min(matrix.shape) - 1),
                               random_state=42)
            user_factors = svd.fit_transform(matrix)  # (n_users, k)
            item_factors = svd.components_.T            # (n_items, k)

            # Store as dicts for fast lookup
            for uid, i in user_idx.items():
                self.svd_user_factors[uid] = user_factors[i]
            for iid, i in item_idx.items():
                self.svd_item_factors[iid] = item_factors[i]

            self.svd_trained = True
            logger.info(f"SVD trained: {n_factors} factors, "
                        f"{len(user_ids)} users, {len(item_ids)} items")
        except Exception as e:
            logger.warning(f"SVD training failed, using baseline only: {e}")
            self.svd_trained = False

    def _predict_svd(self, user_id: str, item_id: str) -> Optional[float]:
        """Predict residual rating via SVD latent factor dot product."""
        if not self.svd_trained:
            return None
        u_vec = self.svd_user_factors.get(user_id)
        i_vec = self.svd_item_factors.get(item_id)
        if u_vec is None or i_vec is None:
            return None
        # Reconstruct residual, add back bias
        residual = float(np.dot(u_vec, i_vec))
        pred = self.global_mean + self.user_biases.get(user_id, 0) + \
               self.item_biases.get(item_id, 0) + residual
        return float(np.clip(pred, 1.0, 5.0))

    def predict(self, user_profile: UserProfile, item_id: str = "",
                item_name: str = "", item_category: str = "",
                item_description: str = "", use_llm: bool = True) -> dict:
        """Predict rating using SVD + Bayesian bias blend.
        
        SVD captures latent user-item interaction patterns that pure bias
        misses. XGBoost is excluded from inference due to feature distribution
        mismatch between training (per-review text) and inference (averaged).
        """
        user_bias = self.user_biases.get(user_profile.user_id, 0)
        item_bias = self.item_biases.get(item_id, 0)

        # Bayesian bias baseline
        baseline = self.global_mean + user_bias + item_bias

        # Light category interaction blend (only when data exists)
        cat_key = (user_profile.user_id, item_category)
        if cat_key in self.user_category_means:
            cat_mean = self.user_category_means[cat_key]
            baseline = 0.2 * cat_mean + 0.8 * baseline

        baseline = float(np.clip(baseline, 1.0, 5.0))

        # SVD collaborative filtering — captures user-item latent interactions
        svd_pred = self._predict_svd(user_profile.user_id, item_id)
        if svd_pred is not None:
            # Blend SVD with bias baseline
            final = 0.4 * svd_pred + 0.6 * baseline
            method = "svd+bias"
        else:
            final = baseline
            method = "baseline"

        final = round(float(np.clip(final, 1.0, 5.0)), 1)

        confidence = min(0.95, 0.3 +
                        0.1 * min(self.user_counts.get(user_profile.user_id, 0), 5) +
                        0.05 * min(self.item_counts.get(item_id, 0), 5))

        return {
            "predicted_rating": final,
            "baseline_rating": round(baseline, 2),
            "llm_adjustment": 0.0,
            "confidence": round(confidence, 2),
            "method": method,
        }




    def _predict_xgboost(self, user_profile: UserProfile, item_id: str, item_category: str) -> float:
        """Construct feature vector and predict with trained XGBoost model."""
        import xgboost as xgb

        # Build feature dict matching training features
        user_id = user_profile.user_id
        user_bias = self.user_biases.get(user_id, 0)
        item_bias = self.item_biases.get(item_id, 0)

        user_count = self.user_counts.get(user_id, 1)
        item_count = self.item_counts.get(item_id, 1)

        # User stats from profile
        avg_rating = user_profile.data.get("avg_rating", self.global_mean)
        reviews = user_profile.get_sample_reviews(10)
        user_std = np.std([r.get("rating", 3) for r in reviews]) if reviews else 0.5
        user_median = np.median([r.get("rating", 3) for r in reviews]) if reviews else avg_rating

        # Compute REAL sentiment features from user's category reviews
        # This was the bug — hardcoded values caused all predictions to cluster at the mean
        pos_words = {"great", "good", "excellent", "love", "amazing", "best", "perfect", "fantastic", "awesome", "wonderful"}
        neg_words = {"bad", "terrible", "worst", "hate", "awful", "poor", "horrible", "disappointing", "waste", "broken"}

        # Use category-matching reviews if available, else all reviews
        cat_reviews = [r for r in reviews if r.get("category", "").lower() == item_category.lower()]
        ref_reviews = cat_reviews if cat_reviews else reviews

        # Compute average text features from user's reviews
        total_excl, total_q, total_upper_ratio = 0, 0, 0.0
        total_pos, total_neg, total_len, total_chars = 0, 0, 0, 0
        n_refs = max(len(ref_reviews), 1)

        for r in ref_reviews:
            text = str(r.get("review_text", ""))
            words = text.lower().split()
            total_len += len(words)
            total_chars += len(text)
            total_excl += text.count("!")
            total_q += text.count("?")
            total_upper_ratio += sum(1 for c in text if c.isupper()) / max(len(text), 1)
            total_pos += sum(1 for w in words if w in pos_words)
            total_neg += sum(1 for w in words if w in neg_words)

        # Item stats — use item bias magnitude as variance proxy
        item_avg = self.global_mean + item_bias
        item_std = abs(item_bias) * 0.5 + 0.3  # higher bias → higher variance

        features = {
            "user_bias": user_bias,
            "item_bias": item_bias,
            "user_review_count": user_count,
            "user_avg_rating": avg_rating,
            "user_std_rating": user_std,
            "user_median_rating": user_median,
            "item_review_count": item_count,
            "item_avg_rating": item_avg,
            "item_std_rating": item_std,
            "review_length": total_len / n_refs,
            "review_char_count": total_chars / n_refs,
            "exclamation_count": total_excl / n_refs,
            "question_count": total_q / n_refs,
            "uppercase_ratio": total_upper_ratio / n_refs,
            "positive_word_count": total_pos / n_refs,
            "negative_word_count": total_neg / n_refs,
            "sentiment_ratio": (total_pos + 1) / (total_neg + 1),
            "user_item_diff": item_avg - avg_rating,
        }

        # Category features
        if item_category and item_category in self.category_means:
            features["category_mean"] = self.category_means[item_category]
        else:
            features["category_mean"] = self.global_mean

        # Build DataFrame matching training columns
        feat_df = pd.DataFrame([features])

        # Add category dummies (must match training columns)
        if hasattr(self, '_xgb_columns'):
            for col in self._xgb_columns:
                if col not in feat_df.columns:
                    feat_df[col] = 0
            feat_df = feat_df[self._xgb_columns]

        pred = self.xgb_model.predict(feat_df)[0]
        return float(np.clip(pred, 1.0, 5.0))

    def _get_llm_adjustment(self, user_profile, item_name, item_category, item_description, baseline):
        """Ask LLM to adjust baseline rating based on deep context analysis."""
        # Extract user's rating pattern for this category
        sample_reviews = user_profile.get_sample_reviews(5)
        category_reviews = [r for r in sample_reviews if r.get("category", "").lower() == item_category.lower()]

        reviews_context = ""
        if category_reviews:
            reviews_context = f"\nUser's {item_category} reviews: " + ", ".join(
                f'{r.get("item_name","?")} ({r.get("rating","?")}/5)' for r in category_reviews[:3]
            )
        elif sample_reviews:
            reviews_context = f"\nUser's recent reviews: " + ", ".join(
                f'{r.get("item_name","?")} ({r.get("rating","?")}/5)' for r in sample_reviews[:3]
            )

        prompt = f"""USER: {user_profile.get_summary()}{reviews_context}
PRODUCT: {item_name} ({item_category}). {item_description or ''}
BASELINE PREDICTION: {baseline:.2f}/5

Based on how well this product matches this user's preferences, should the rating be adjusted?
Consider: Does the user typically rate {item_category} items higher or lower? Does this specific product match their taste profile?

Respond JSON: {{"adjustment": <float between -1.5 and 1.5>, "reason": "<brief>"}}"""

        try:
            result = llm_client.generate_json(prompt=prompt, temperature=0.15, max_tokens=100)
            adj = float(result.get("adjustment", 0))
            return max(-1.5, min(1.5, adj))  # Clamp adjustment
        except Exception:
            return 0.0

    def _save_model(self):
        with open(self.model_path, "wb") as f:
            pickle.dump({
                "global_mean": self.global_mean,
                "user_biases": self.user_biases,
                "item_biases": self.item_biases,
                "user_counts": self.user_counts,
                "item_counts": self.item_counts,
                "category_means": self.category_means,
                "user_category_means": self.user_category_means,
                "xgb_model": self.xgb_model,
            }, f)

    def load_model(self):
        if self.model_path.exists():
            with open(self.model_path, "rb") as f:
                d = pickle.load(f)
            self.global_mean = d["global_mean"]
            self.user_biases = d["user_biases"]
            self.item_biases = d["item_biases"]
            self.user_counts = d.get("user_counts", {})
            self.item_counts = d.get("item_counts", {})
            self.category_means = d.get("category_means", {})
            self.user_category_means = d.get("user_category_means", {})
            self.xgb_model = d.get("xgb_model")
            self.is_trained = True
            logger.info("Rating model loaded")


rating_predictor = RatingPredictor()
