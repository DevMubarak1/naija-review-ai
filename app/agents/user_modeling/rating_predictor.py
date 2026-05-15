"""
NaijaReview AI — Rating Predictor (Hybrid)
Combines collaborative filtering signals with LLM reasoning for accurate rating prediction.
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
    1. Statistical baseline (user/item average bias)
    2. XGBoost with engineered features
    3. LLM-based contextual adjustment
    """

    def __init__(self):
        self.global_mean = 3.5
        self.user_biases = {}
        self.item_biases = {}
        self.xgb_model = None
        self.is_trained = False
        self.model_path = settings.processed_data_dir / "rating_model.pkl"

    def train(self, df: pd.DataFrame):
        """Train the rating prediction model on historical data."""
        logger.info(f"Training rating predictor on {len(df)} reviews...")
        self.global_mean = df["rating"].mean()

        user_avg = df.groupby("user_id")["rating"].mean()
        self.user_biases = (user_avg - self.global_mean).to_dict()

        item_avg = df.groupby("item_id")["rating"].mean()
        self.item_biases = (item_avg - self.global_mean).to_dict()

        self._train_xgboost(df)
        self.is_trained = True
        self._save_model()
        logger.info(f"Trained. Global mean: {self.global_mean:.2f}")

    def _train_xgboost(self, df: pd.DataFrame):
        """Train XGBoost model on engineered features."""
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
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

        self.xgb_model = xgb.XGBRegressor(
            n_estimators=200, max_depth=6, learning_rate=0.1,
            objective="reg:squarederror", random_state=42, n_jobs=-1,
        )
        self.xgb_model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)

        val_pred = self.xgb_model.predict(X_val)
        rmse = np.sqrt(np.mean((val_pred - y_val) ** 2))
        logger.info(f"XGBoost validation RMSE: {rmse:.4f}")

    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create features for XGBoost."""
        features = pd.DataFrame()
        features["rating"] = df["rating"]
        features["user_bias"] = df["user_id"].map(self.user_biases).fillna(0)
        features["item_bias"] = df["item_id"].map(self.item_biases).fillna(0)

        user_stats = df.groupby("user_id").agg(
            user_review_count=("rating", "count"),
            user_avg_rating=("rating", "mean"),
            user_std_rating=("rating", "std"),
        ).fillna(0)
        features = features.join(df[["user_id"]].join(user_stats, on="user_id").drop("user_id", axis=1))

        item_stats = df.groupby("item_id").agg(
            item_review_count=("rating", "count"),
            item_avg_rating=("rating", "mean"),
            item_std_rating=("rating", "std"),
        ).fillna(0)
        features = features.join(df[["item_id"]].join(item_stats, on="item_id").drop("item_id", axis=1))

        features["review_length"] = df["review_text"].str.split().str.len().fillna(0)

        if "category" in df.columns:
            category_dummies = pd.get_dummies(df["category"], prefix="cat")
            features = pd.concat([features, category_dummies], axis=1)

        return features.dropna()

    def predict(self, user_profile: UserProfile, item_id: str = "",
                item_name: str = "", item_category: str = "",
                item_description: str = "", use_llm: bool = True) -> dict:
        """Predict rating for a user-item pair using hybrid approach."""
        user_bias = self.user_biases.get(user_profile.user_id, 0)
        item_bias = self.item_biases.get(item_id, 0)
        baseline = max(1.0, min(5.0, self.global_mean + user_bias + item_bias))

        llm_adjustment = 0.0
        if use_llm:
            llm_adjustment = self._get_llm_adjustment(
                user_profile, item_name, item_category, item_description, baseline
            )

        has_user = user_profile.user_id in self.user_biases
        has_item = item_id in self.item_biases
        w = 0.7 if (has_user and has_item) else (0.5 if (has_user or has_item) else 0.3)

        final = max(1.0, min(5.0, w * baseline + (1 - w) * (baseline + llm_adjustment)))
        final = round(final * 2) / 2

        return {
            "predicted_rating": final, "baseline_rating": round(baseline, 2),
            "llm_adjustment": round(llm_adjustment, 2),
            "confidence": 0.8 if has_user else 0.5, "method": "hybrid" if use_llm else "baseline",
        }

    def _get_llm_adjustment(self, user_profile, item_name, item_category, item_description, baseline):
        """Ask LLM to adjust baseline rating based on context."""
        prompt = f"""USER: {user_profile.get_summary()}
PRODUCT: {item_name} ({item_category}). {item_description or ''}
BASELINE: {baseline:.1f}★

Adjust rating? Respond JSON: {{"adjustment": <-2.0 to 2.0>, "reason": "<brief>"}}"""

        try:
            result = llm_client.generate_json(prompt=prompt, temperature=0.2, max_tokens=100)
            return float(result.get("adjustment", 0))
        except Exception:
            return 0.0

    def _save_model(self):
        with open(self.model_path, "wb") as f:
            pickle.dump({"global_mean": self.global_mean, "user_biases": self.user_biases,
                         "item_biases": self.item_biases, "xgb_model": self.xgb_model}, f)

    def load_model(self):
        if self.model_path.exists():
            with open(self.model_path, "rb") as f:
                d = pickle.load(f)
            self.global_mean, self.user_biases = d["global_mean"], d["user_biases"]
            self.item_biases, self.xgb_model = d["item_biases"], d["xgb_model"]
            self.is_trained = True
            logger.info("Rating model loaded")


rating_predictor = RatingPredictor()
