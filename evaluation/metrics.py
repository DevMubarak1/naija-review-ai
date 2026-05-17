"""
NaijaReview AI — Evaluation Metrics (Optimized)
Computes ROUGE, BERTScore, RMSE for Task A and NDCG@10, Hit Rate for Task B.
Uses fuzzy matching for item name comparison in Task B.
"""

import numpy as np
from loguru import logger


def compute_rmse(predicted: list[float], actual: list[float]) -> float:
    """Compute Root Mean Squared Error for rating predictions."""
    predicted = np.array(predicted)
    actual = np.array(actual)
    return float(np.sqrt(np.mean((predicted - actual) ** 2)))


def compute_mae(predicted: list[float], actual: list[float]) -> float:
    """Compute Mean Absolute Error for rating predictions."""
    return float(np.mean(np.abs(np.array(predicted) - np.array(actual))))


def compute_rouge_scores(predictions: list[str], references: list[str]) -> dict:
    """Compute ROUGE-1, ROUGE-2, ROUGE-L scores."""
    from rouge_score import rouge_scorer
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)

    scores = {"rouge1": [], "rouge2": [], "rougeL": []}
    for pred, ref in zip(predictions, references):
        if not pred or not ref:
            continue
        result = scorer.score(ref, pred)
        for key in scores:
            scores[key].append(result[key].fmeasure)

    return {k: float(np.mean(v)) if v else 0.0 for k, v in scores.items()}


def compute_bertscore(predictions: list[str], references: list[str]) -> dict:
    """Compute BERTScore (Precision, Recall, F1)."""
    from bert_score import score as bert_score

    P, R, F1 = bert_score(predictions, references, lang="en", verbose=False)
    return {
        "precision": float(P.mean()),
        "recall": float(R.mean()),
        "f1": float(F1.mean()),
    }


def _fuzzy_match(name_a: str, name_b: str) -> bool:
    """Check if two item names are a fuzzy match."""
    a = name_a.lower().strip()
    b = name_b.lower().strip()

    # Exact match
    if a == b:
        return True

    # Containment match (one is a substring of the other)
    if a in b or b in a:
        return True

    # Token overlap: if >=70% of words match
    tokens_a = set(a.split())
    tokens_b = set(b.split())
    if not tokens_a or not tokens_b:
        return False

    overlap = len(tokens_a & tokens_b)
    min_len = min(len(tokens_a), len(tokens_b))
    if min_len > 0 and overlap / min_len >= 0.7:
        return True

    return False


def _item_in_relevant(item: str, relevant_items: list[str]) -> bool:
    """Check if an item fuzzy-matches any relevant item."""
    return any(_fuzzy_match(item, r) for r in relevant_items)


def compute_ndcg(recommended_items: list[str], relevant_items: list[str], k: int = 10) -> float:
    """Compute NDCG@k with fuzzy item name matching."""
    # Deduplicate relevant items (dataset has repeat reviews)
    unique_relevant = list(dict.fromkeys(relevant_items))
    recommended = recommended_items[:k]
    dcg = sum(
        1.0 / np.log2(i + 2) for i, item in enumerate(recommended)
        if _item_in_relevant(item, unique_relevant)
    )
    ideal = sorted(
        [1.0 / np.log2(i + 2) for i in range(min(len(unique_relevant), k))],
        reverse=True,
    )
    idcg = sum(ideal)
    return min(1.0, float(dcg / idcg)) if idcg > 0 else 0.0


def compute_hit_rate(recommended_items: list[str], relevant_items: list[str], k: int = 10) -> float:
    """Compute Hit Rate@k with fuzzy matching. Binary: 1 if ANY relevant item in top-k, else 0."""
    unique_relevant = list(dict.fromkeys(relevant_items))
    has_hit = any(
        _item_in_relevant(item, unique_relevant)
        for item in recommended_items[:k]
    )
    return 1.0 if has_hit else 0.0


def run_task_a_evaluation(
    generated_reviews: list[dict],
    ground_truth: list[dict],
) -> dict:
    """
    Full Task A evaluation.
    Each entry should have: rating, review_text
    """
    logger.info(f"Evaluating Task A on {len(generated_reviews)} reviews...")

    predictions_text = [r["review_text"] for r in generated_reviews]
    references_text = [r["review_text"] for r in ground_truth]
    predictions_rating = [r["rating"] for r in generated_reviews]
    actual_rating = [r["rating"] for r in ground_truth]

    results = {
        "rmse": compute_rmse(predictions_rating, actual_rating),
        "mae": compute_mae(predictions_rating, actual_rating),
        "rouge": compute_rouge_scores(predictions_text, references_text),
    }

    try:
        results["bertscore"] = compute_bertscore(predictions_text, references_text)
    except Exception as e:
        logger.warning(f"BERTScore failed: {e}")
        results["bertscore"] = {"precision": 0, "recall": 0, "f1": 0}

    logger.info(f"Task A Results: RMSE={results['rmse']:.4f}, "
                f"ROUGE-1={results['rouge']['rouge1']:.4f}, "
                f"ROUGE-L={results['rouge']['rougeL']:.4f}, "
                f"BERTScore-F1={results['bertscore']['f1']:.4f}")

    return results


def run_task_b_evaluation(
    recommendation_results: list[dict],
    ground_truth_items: list[list[str]],
    k: int = 10,
) -> dict:
    """
    Full Task B evaluation with fuzzy matching.
    """
    logger.info(f"Evaluating Task B on {len(recommendation_results)} users...")

    ndcg_scores = []
    hit_rates = []

    for result, relevant in zip(recommendation_results, ground_truth_items):
        recs = result.get("recommendations", [])
        rec_items = [r.get("item_name", "") for r in recs]

        ndcg = compute_ndcg(rec_items, relevant, k)
        hr = compute_hit_rate(rec_items, relevant, k)
        ndcg_scores.append(ndcg)
        hit_rates.append(hr)

        # Log individual matches for debugging
        matches = [item for item in rec_items if _item_in_relevant(item, relevant)]
        if matches:
            logger.info(f"  Matched items: {matches}")

    results = {
        f"ndcg@{k}": float(np.mean(ndcg_scores)) if ndcg_scores else 0.0,
        f"hit_rate@{k}": float(np.mean(hit_rates)) if hit_rates else 0.0,
    }

    logger.info(f"Task B Results: NDCG@{k}={results[f'ndcg@{k}']:.4f}, "
                f"HitRate@{k}={results[f'hit_rate@{k}']:.4f}")

    return results
