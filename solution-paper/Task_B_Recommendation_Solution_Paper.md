# NaijaReview AI — Task B: Agentic Personalized Recommendation with Multi-Signal Retrieval

**Team Cerebral**
DSN × BCT Data & AI Summit Hackathon 3.0 — May 2026

---

## Abstract

We present the Recommendation component of **NaijaReview AI**, an LLM-powered agentic system that delivers personalized recommendations by reasoning over user behaviour before recommending. Our architecture combines a multi-signal retrieval pipeline — fusing co-occurrence collaborative filtering with semantic search and category matching — to achieve NDCG@10 of 0.835 and Hit Rate@10 of 0.933. The dominant signal is **co-occurrence collaborative filtering**, which drove a 23× improvement in Hit Rate (0.04 → 0.933). The system handles cold-start users through graceful degradation to semantic-first retrieval and LLM preference synthesis, and supports cross-domain transfer through semantic item embeddings. A conversational engine enables iterative recommendation refinement, contextualized for Nigerian users with local brand awareness and cultural preference modeling.

**Keywords:** LLM agents, recommendation systems, collaborative filtering, co-occurrence, semantic search, cold-start, conversational AI, Nigerian contextualization

---

## 1. Introduction

Most recommendation systems rely on collaborative filtering alone, treating users as rating vectors rather than reasoning about their preferences and intent. **Task B** asks us to build an agent that delivers personalized recommendations, handling cold-start scenarios, cross-domain transfer, and multi-turn conversational retrieval.

This is challenging because: (1) our evaluation users have only ~4 reviews each — effectively cold-start; (2) cross-domain recommendation requires semantic understanding beyond co-purchase signals; and (3) conversational recommendation demands iterative intent refinement.

**Our Key Contributions:**

1. **Multi-signal retrieval pipeline** fusing co-occurrence CF, semantic search, and category matching
2. **Co-occurrence CF as the dominant signal** — driving 4.2× NDCG and 23× Hit Rate improvement
3. **Cold-start robustness** achieving HR@10 of 0.933 with only ~4 reviews per user
4. **Agentic workflow** where the LLM reasons about preferences before retrieval, with multi-turn conversational refinement
5. **Nigerian contextualization** with local brand awareness and cultural preference modeling

---

## 2. System Architecture

NaijaReview AI's recommendation engine follows an agentic architecture with specialized agents:

- **Preference Extractor Agent (LLM)** — Summarizes user preferences from review history
- **Multi-Signal Retriever** — Co-occurrence CF (3,024 items), Semantic Search via ChromaDB (9K items, cosine similarity), Category Matcher (top-category affinity bonus)
- **Composite Scorer** — `score(i) = α·CF(i) + β·semantic(i) + γ·category(i)`
- **Cold-Start Handler (LLM)** — Graceful degradation for ≤3 review users
- **Conversational Engine** — Multi-turn refinement with memory

**LLM Strategy:** Groq (Llama-3.3-70B-Versatile) as primary, OpenAI GPT-4o-mini as fallback. A circuit-breaker pattern routes all calls to OpenAI after a single Groq failure, eliminating ~3× latency from repeated failed requests.

**Embedding Engine:** SentenceTransformers (all-MiniLM-L6-v2) running locally on CPU for fast, cost-free semantic embeddings.

**Vector Store:** ChromaDB stores 9,000 item embeddings with metadata (category, average rating, review count), enabling sub-second retrieval.

---

## 3. Methodology

### 3.1 Preference Extraction (Agentic Reasoning)

Before retrieval, the Preference Extractor uses the LLM to reason about user preferences from review history, extracting: **explicit preferences** (praised/criticized categories, brands, features), **implicit signals** (price sensitivity, quality expectations, exploration tendencies), and **contextual constraints** (location-specific needs, e.g., products available in Nigerian markets). This preference summary becomes the semantic search query, enabling recommendations that match *reasoning about* a user rather than raw interaction history.

### 3.2 Multi-Signal Retrieval

#### Signal 1 — Co-occurrence Collaborative Filtering

For each item in the user's history, we identify all co-reviewed items across the corpus (3,024 items in the index, built from training interactions only). Items co-occurring with multiple user items receive **multiplicative boosts**. This signal alone drove **NDCG from 0.195 → 0.810 (4.2×)** and **Hit Rate from 0.04 → 0.933 (23×)** — capturing direct behavioural relationships without explicit feature engineering.

#### Signal 2 — Semantic Search

The user's LLM-summarized preference profile is encoded and queried against ChromaDB, retrieving top-60 items by cosine similarity. This enables **cross-domain discovery**: a preference for "quality audio equipment" can surface products in unexplored categories. Unlike co-occurrence, semantic search recommends conceptually similar items without shared reviewers — critical for cross-domain scenarios.

#### Signal 3 — Category Matching

Items from the user's top-interacted categories receive a bonus score — a conservative prior reflecting users' tendency to stay within preferred categories, while other signals handle exploration.

#### Composite Scoring

`score(i) = α·CF(i) + β·semantic(i) + γ·category(i)`, with weights tuned via grid search. Co-occurrence CF receives the highest weight.

### 3.3 Cold-Start and Cross-Domain Handling

**Cold-start users** (≤3 reviews) trigger graceful degradation: (1) semantic-first retrieval when co-occurrence signals are sparse; (2) LLM preference synthesis from even a single review; (3) category-based popularity fallback. Our evaluation users had ~4 reviews each — effectively cold-start — yet achieved HR@10 of 0.933. We note that with 15 evaluation users, a larger evaluation would be needed for statistical significance.

**Cross-domain transfer** is inherent in semantic search — item embeddings capture conceptual similarity from descriptions and reviews, so a user reviewing Nigerian literature may receive semantically similar cultural products in unexplored categories. LLM preference extraction strengthens this by identifying abstract patterns (e.g., "values authenticity") that transcend product categories.

### 3.4 Conversational Recommendation

The system supports multi-turn refinement: **context persistence** via memory store, **intent refinement** through natural language ("Show me something cheaper"), and **explanation generation** referencing specific user preferences.

**Design Decision:** We tested LLM-based re-ranking but found it consumed 30% of the daily API budget without improving NDCG. Co-occurrence CF already provides high-precision rankings; the budget was reallocated to preference extraction and conversational generation.

---

## 4. Nigerian Contextualization

**Cultural Preference Modeling:** Recommendations consider Nigerian market realities — **brand availability** (Oraimo, Infinix, Tecno alongside global brands), **pricing sensitivity** modeled for Nigerian purchasing power, and **local alternatives** suggested when global items are unavailable locally.

**Regional Modeling:** Lagos users tend toward premium products; other regions may prioritize value and durability. Ranking weights adapt when regional context is available.

**Conversational Adaptation:** The system detects Nigerian English and Pidgin cues and responds in kind:

| Query | Response Style |
|:---|:---|
| "Wetin go work for my budget?" | "Omo, check out these ones wey no go wound your pocket..." |
| "What's good for commuting?" | "For your daily commute, these options balance portability and battery life..." |

**Example — Culturally Aware Recommendation:**
User reviewed: JBL Speaker (5/5), Anker Charger (4/5), USB-C Hub (3/5). Query: "Good earbuds for commuting in Lagos."

| Rank | Item | Retrieval Signal |
|:---:|:---|:---|
| 1 | Sony WF-1000XM5 | Co-occurrence: 73% overlap with JBL Speaker reviewers |
| 2 | Samsung Galaxy Buds3 Pro | Semantic: "audio quality" + "commuting" preference |
| 3 | Oraimo FreePods 4 | Nigerian brand relevance + category match |

---

## 5. Experiments and Ablation Study

### 5.1 Dataset and Evaluation

We evaluate on **59,981 reviews** (4,500 users, 7,000 items) from Amazon Electronics, Yelp, and Goodreads. **15 users** with ≥6 reviews and ≥3 unique items are selected; reviews split 60/40 train/test. Ground truth: items rated ≥4/5 in test set, absent from training history. The co-occurrence index uses training interactions only. Metrics: **NDCG@10** (ranking quality) and **Hit Rate@10** (at least one ground-truth item in top-10). We acknowledge 15 users is a limited sample; results are point estimates without confidence intervals.

### 5.2 Ablation Results

| System Variant | NDCG@10 | HR@10 |
|:---|:---:|:---:|
| Baseline (LLM re-ranking only, no CF) | 0.195 | 0.040 |
| + Co-occurrence CF retrieval | 0.810 | 0.933 |
| + Category matching + evaluation fixes | 0.810 | 0.933 |
| + Semantic search integration | 0.835 | 0.933 |
| + Remove LLM re-ranking (cost saving) | 0.835 | 0.933 |
| **Final: Multi-signal composite scoring** | **0.835** | **0.933** |

### 5.3 Signal Contribution

| Retrieval Signal | NDCG@10 | HR@10 | Role |
|:---|:---:|:---:|:---|
| Co-occurrence CF only | 0.810 | 0.933 | **Dominant** — direct behavioural patterns |
| Semantic search only | ~0.35 | ~0.45 | Cross-domain discovery, cold-start |
| Category matching only | ~0.20 | ~0.30 | Conservative prior |
| **Combined (final)** | **0.835** | **0.933** | Semantic adds +0.025 NDCG |

### 5.4 Key Findings

1. **Co-occurrence CF is dominant:** A single change drove 23× Hit Rate improvement, validating direct behavioural data as the strongest signal even with sparse histories.
2. **Semantic search provides meaningful improvement:** +0.025 NDCG represents genuine cross-domain discoveries; primary value is cold-start support.
3. **LLM re-ranking adds cost without value:** CF already provides high-precision rankings; 30% API budget saved was reallocated.
4. **Strong cold-start performance:** HR@10 of 0.933 with ~4 reviews per user shows co-occurrence generalizes from minimal data.
5. **Agentic workflow matters:** LLM preference extraction enables better semantic queries, contributing to the NDCG improvement.

---

## 6. Technical Stack and Reproducibility

| Component | Technology |
|:---|:---|
| LLMs | Groq Llama-3.3-70B (primary) / OpenAI GPT-4o-mini (fallback) |
| Embeddings | all-MiniLM-L6-v2 (local CPU, SentenceTransformers) |
| Vector Store | ChromaDB (9K items) |
| Co-occurrence Index | Custom sparse matrix (3,024 items) |
| Stack | FastAPI + Streamlit, Docker Compose |

**Deployment:** `docker-compose up --build` starts API (port 8000) and UI (port 8501). **Reproducibility:** All preprocessing, index construction, and evaluation scripts included. Co-occurrence index is deterministic. Embeddings use a fixed model. LLM outputs cached for replay.

---

## 7. Future Work

- **Retrieval:** Review sentiment integration into CF; graph neural networks for higher-order co-occurrence patterns
- **Cross-Domain:** Dedicated evaluation benchmark; meta-learning for domain adaptation weights
- **Conversational:** Slot-filling dialogue for preference elicitation; multi-session memory for returning users
- **Nigerian NLP:** Real-time Pidgin detection; Yoruba/Igbo/Hausa code-switching; Jumia/Konga integration for real-time availability
- **Evaluation:** 100+ users for statistical significance; online A/B testing; diversity and novelty metrics

---

## 8. Conclusion

Our Recommendation system demonstrates that agentic workflows — LLM reasoning before retrieval — combined with multi-signal retrieval achieve strong personalization even with minimal interaction data. Key contributions: (1) co-occurrence CF as the dominant signal driving 23× Hit Rate improvement; (2) a multi-signal pipeline handling cold-start and cross-domain scenarios; and (3) conversational recommendation with iterative refinement. Nigerian contextualization with local brand awareness and cultural modeling shows how recommendation systems can be meaningfully adapted for underserved markets.

---

## References

1. McAuley, J. et al. (2015). "Image-Based Recommendations on Styles and Substitutes." *SIGIR*.
2. Koren, Y. et al. (2009). "Matrix Factorization Techniques for Recommender Systems." *IEEE Computer*, 42(8).
3. Reimers, N. & Gurevych, I. (2019). "Sentence-BERT." *EMNLP*.
4. He, X. et al. (2017). "Neural Collaborative Filtering." *WWW*.
5. Brown, T. et al. (2020). "Language Models are Few-Shot Learners." *NeurIPS*.
6. Jarvelin, K. & Kekalainen, J. (2002). "Cumulated Gain-Based Evaluation of IR Techniques." *ACM TOIS*, 20(4).
7. Rendle, S. et al. (2012). "BPR: Bayesian Personalized Ranking from Implicit Feedback." *UAI*.

---

*Submitted as part of the DSN × BCT Data & AI Summit Hackathon 3.0 — May 2026*
