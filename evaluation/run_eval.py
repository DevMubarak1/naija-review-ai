"""
NaijaReview AI — Full Evaluation Runner
Runs end-to-end evaluation on held-out data for both Task A and Task B.
"""

import json
import time
from pathlib import Path

import pandas as pd
from loguru import logger

from app.core.config import settings
from app.agents.user_modeling.pipeline import user_modeling_pipeline
from app.agents.user_modeling.rating_predictor import rating_predictor
from app.agents.recommendation.pipeline import recommendation_pipeline
from app.data.loader import load_all_datasets, get_user_data
from evaluation.metrics import (
    run_task_a_evaluation, run_task_b_evaluation,
    compute_rmse, compute_rouge_scores,
)


def run_full_evaluation(
    n_users_a: int = 20,
    n_users_b: int = 15,
    top_k: int = 10,
    save_results: bool = True,
) -> dict:
    """Run full evaluation pipeline."""
    logger.info("=" * 60)
    logger.info("STARTING FULL EVALUATION")
    logger.info("=" * 60)

    # Load data
    df = load_all_datasets()
    if not rating_predictor.is_trained:
        rating_predictor.train(df)

    results = {}

    # ── TASK A EVALUATION ──
    logger.info("\n--- Task A: User Modeling Evaluation ---")
    results["task_a"] = _evaluate_task_a(df, n_users_a)

    # ── TASK B EVALUATION ──
    logger.info("\n--- Task B: Recommendation Evaluation ---")
    results["task_b"] = _evaluate_task_b(df, n_users_b, top_k)

    # ── SUMMARY ──
    logger.info("\n" + "=" * 60)
    logger.info("EVALUATION SUMMARY")
    logger.info("=" * 60)

    if "task_a" in results and results["task_a"]:
        a = results["task_a"]
        logger.info(f"Task A — RMSE: {a.get('rmse', 'N/A'):.4f}")
        logger.info(f"Task A — ROUGE-1: {a.get('rouge', {}).get('rouge1', 0):.4f}")
        logger.info(f"Task A — ROUGE-L: {a.get('rouge', {}).get('rougeL', 0):.4f}")

    if "task_b" in results and results["task_b"]:
        b = results["task_b"]
        logger.info(f"Task B — NDCG@{top_k}: {b.get(f'ndcg@{top_k}', 0):.4f}")
        logger.info(f"Task B — Hit Rate@{top_k}: {b.get(f'hit_rate@{top_k}', 0):.4f}")

    if save_results:
        out_path = settings.processed_data_dir / "evaluation_results.json"
        with open(out_path, "w") as f:
            json.dump(results, f, indent=2, default=str)
        logger.info(f"Results saved to {out_path}")

    return results


def _evaluate_task_a(df: pd.DataFrame, n_users: int) -> dict:
    """Evaluate Task A on held-out reviews."""
    # Select users with enough reviews
    user_counts = df["user_id"].value_counts()
    eligible = user_counts[user_counts >= 5].index.tolist()[:n_users]

    generated = []
    ground_truth = []
    rating_preds = []
    rating_actuals = []

    for uid in eligible:
        user_df = df[df["user_id"] == uid]
        # Use first N-1 reviews as history, last as test
        history = user_df.iloc[:-1].to_dict("records")
        test_row = user_df.iloc[-1]

        try:
            result = user_modeling_pipeline.run(
                user_id=uid,
                item_name=test_row.get("item_name", "Unknown"),
                item_category=test_row.get("category", "General"),
                item_description="",
                item_id=str(test_row.get("item_id", "")),
                reviews=history,
                is_nigerian=False,
            )
            generated.append({
                "rating": result["rating"],
                "review_text": result["review_text"],
            })
            ground_truth.append({
                "rating": float(test_row["rating"]),
                "review_text": str(test_row["review_text"]),
            })
            rating_preds.append(result["rating"])
            rating_actuals.append(float(test_row["rating"]))

            logger.info(f"  User {uid[:8]}: pred={result['rating']:.1f} actual={test_row['rating']}")
        except Exception as e:
            logger.warning(f"  User {uid[:8]} failed: {e}")
            continue

        # Rate limit
        time.sleep(0.5)

    if not generated:
        logger.error("No Task A evaluations completed")
        return {}

    return run_task_a_evaluation(generated, ground_truth)


def _evaluate_task_b(df: pd.DataFrame, n_users: int, top_k: int) -> dict:
    """Evaluate Task B recommendations with proper train/test separation."""
    # Select users with most unique items (not most reviews) for meaningful eval
    user_item_counts = df.groupby("user_id")["item_name"].nunique()
    user_review_counts = df["user_id"].value_counts()
    # Need >= 6 reviews AND >= 3 unique items for meaningful eval
    eligible_users = user_item_counts[
        (user_item_counts >= 3) & (user_review_counts[user_item_counts.index] >= 6)
    ].sort_values(ascending=False).index.tolist()

    rec_results = []
    gt_items = []
    evaluated = 0

    for uid in eligible_users:
        if evaluated >= n_users:
            break

        user_df = df[df["user_id"] == uid]
        # Split: history = first 60%, test = last 40%
        split = int(len(user_df) * 0.6)
        history = user_df.iloc[:split].to_dict("records")
        test = user_df.iloc[split:]

        # Items already seen in history
        history_items = set(r.get("item_name", "").lower().strip() for r in history)

        # Ground truth: ONLY genuinely new items rated >= 4 (not in history)
        test_liked = test[test["rating"] >= 4]["item_name"].tolist()
        relevant = list(dict.fromkeys(  # Deduplicate
            item for item in test_liked
            if item.lower().strip() not in history_items
        ))

        if not relevant:
            continue  # Skip users with no new items in test

        evaluated += 1

        try:
            result = recommendation_pipeline.recommend(
                user_id=uid,
                user_reviews=history,
                top_k=top_k,
                is_nigerian=False,
            )
            rec_results.append(result)
            gt_items.append(relevant)

            recs = [r["item_name"] for r in result.get("recommendations", [])]
            logger.info(f"  User {uid[:8]}: {len(recs)} recs, {len(relevant)} new relevant items")
        except Exception as e:
            logger.warning(f"  User {uid[:8]} failed: {e}")

        time.sleep(0.5)

    if not rec_results:
        logger.error("No Task B evaluations completed")
        return {}

    return run_task_b_evaluation(rec_results, gt_items, top_k)


if __name__ == "__main__":
    results = run_full_evaluation(n_users_a=10, n_users_b=8, top_k=10)
    print(json.dumps(results, indent=2, default=str))
