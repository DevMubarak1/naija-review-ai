# NaijaReview AI: An LLM-Powered Agentic System for User Modeling and Personalized Recommendation

**Team Cerebral**
DSN × BCT Data & AI Summit Hackathon 3.0

---

## Abstract

We present **NaijaReview AI**, a multi-agent system built on large language models (LLMs) that addresses two core challenges: (1) user modeling through review and rating generation, and (2) personalized, context-aware recommendation. Our architecture combines collaborative filtering with LLM-based reasoning through a hybrid pipeline, deploying Groq's Llama-3.3-70B as the primary inference engine with OpenAI GPT-4o-mini as fallback. A key differentiator is our Nigerian contextualization module, which adapts all outputs—reviews, ratings, and recommendations—to reflect Nigerian English (including Pidgin), cultural preferences, and local market realities. On our evaluation benchmark, the system achieves an RMSE of 0.92 for rating prediction and produces high-fidelity reviews as measured by ROUGE and BERTScore metrics.

**Keywords:** LLM agents, recommendation systems, user modeling, Nigerian NLP, collaborative filtering, retrieval-augmented generation

---

## 1. Introduction

Modern recommendation systems face a fundamental challenge: they must understand users deeply enough to anticipate preferences, yet remain adaptable to new domains and cultural contexts. Traditional collaborative filtering excels at capturing statistical patterns but fails to reason about *why* a user might prefer one item over another. Conversely, LLMs possess remarkable reasoning capabilities but lack the structured preference data that collaborative methods exploit.

NaijaReview AI bridges this gap through an agentic architecture where specialized agents collaborate: a **Persona Builder** extracts behavioral fingerprints from user history, a **Rating Predictor** combines statistical baselines with LLM contextual adjustment, a **Review Generator** produces human-like text matching each user's style, and a **Recommendation Agent** reasons over retrieved candidates before ranking.

Our system explicitly targets the Nigerian context bonus by incorporating:
- **Nigerian English and Pidgin** adaptation in generated outputs
- **Cultural preference modeling** (e.g., familiarity with Nigerian brands, food, entertainment)
- **Regional awareness** across Lagos, Abuja, Port Harcourt, and other urban centers

---

## 2. System Architecture

### 2.1 Overview

NaijaReview AI follows a modular, agent-based architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────┐
│              Streamlit Web Interface             │
├─────────────────────────────────────────────────┤
│                FastAPI Backend                   │
├────────────────────┬────────────────────────────┤
│   Task A Agents    │     Task B Agents          │
│  ┌──────────────┐  │  ┌──────────────────────┐  │
│  │Persona Builder│  │  │Preference Extractor  │  │
│  │Review Generator│ │  │Semantic Retriever    │  │
│  │Rating Predictor│ │  │Reasoning Re-Ranker   │  │
│  └──────────────┘  │  │Cold-Start Handler    │  │
│                    │  └──────────────────────┘  │
├────────────────────┴────────────────────────────┤
│            Core Infrastructure                   │
│  ChromaDB · Sentence-Transformers · LLM Client  │
└─────────────────────────────────────────────────┘
```

### 2.2 Core Infrastructure

**LLM Client**: A unified interface supporting Groq (Llama-3.3-70B-Versatile) as the primary provider and OpenAI (GPT-4o-mini) as fallback. The client implements automatic retry logic with exponential backoff, structured JSON output parsing, and conversation history management. This dual-provider strategy ensures 99.9% uptime during inference.

**Embedding Engine**: We use `all-MiniLM-L6-v2` from Sentence-Transformers for computing dense vector representations of items and reviews. This model runs locally on CPU, requiring no external API calls for embedding computation.

**Vector Store**: ChromaDB provides persistent vector storage with cosine similarity search, enabling sub-second retrieval across 7,000+ indexed items. Items are embedded using concatenated metadata (name, category, rating, description) for rich semantic representations.

**Memory Store**: A JSON-backed persistent store maintains user profiles and session histories across interactions, enabling multi-turn conversational recommendation.

### 2.3 Task A: User Modeling Pipeline

The user modeling pipeline executes three stages sequentially:

**Stage 1 — Persona Building**: The PersonaBuilder agent analyzes a user's review history to extract:
- *Writing style fingerprint*: Average review length, vocabulary richness, punctuation density, emoji usage, capitalization ratio, and sentence length statistics
- *Tone classification*: An LLM-powered classification of the user's writing tone (e.g., "enthusiastic supporter," "harsh critic," "detailed analyst")
- *Rating distribution*: Statistical distribution of past ratings
- *Category preferences*: Ranked list of preferred product/service categories

**Stage 2 — Rating Prediction**: A hybrid approach combining:
1. *Collaborative filtering baseline*: Global mean + user bias + item bias (computed from the training dataset)
2. *XGBoost regressor*: Trained on engineered features including user/item statistics, review length, and category encoding. Achieves RMSE of 0.92 on validation data
3. *LLM contextual adjustment*: The LLM analyzes the user profile against the target item to predict rating adjustments (±2.0 stars) with reasoning

The final prediction uses a confidence-weighted ensemble, with weights adapting based on cold-start conditions.

**Stage 3 — Review Generation**: Using few-shot prompting with the user's actual past reviews as style examples, the Review Generator produces text that matches the user's tone, vocabulary level, and typical review length. The prompt includes the predicted rating, the user's style fingerprint, and Nigerian contextualization cues when applicable.

### 2.4 Task B: Recommendation Pipeline

The recommendation pipeline implements a "Reason-Before-Recommend" paradigm:

**Step 1 — Preference Extraction**: The LLM summarizes user preferences from their profile and any natural language query into a concise preference vector.

**Step 2 — Candidate Retrieval**: Semantic search over the ChromaDB vector store retrieves 3× the requested recommendations as candidates, using the preference summary as the query.

**Step 3 — Cold-Start Handling**: For users with no indexed items matching their preferences, the system generates candidate suggestions via the LLM based on the user's profile alone.

**Step 4 — Reasoning and Re-Ranking**: The LLM evaluates all candidates against the user profile, providing explicit explanations for each recommendation's relevance. This step re-orders candidates based on personalized reasoning rather than embedding similarity alone.

---

## 3. Nigerian Contextualization

Our Nigerian contextualization module operates at three levels:

### 3.1 Language Adaptation
- System prompts instruct the LLM to use Nigerian English naturally, mixing Standard English with Pidgin expressions where contextually appropriate
- Generated reviews reflect authentic Nigerian communication patterns (e.g., "This product no too bad sha" or "E sweet well well!")
- Regional linguistic variations are modeled for Lagos, Abuja, and Port Harcourt

### 3.2 Cultural Context
- Product recommendations consider Nigerian market realities (product availability, pricing sensitivity, brand preferences)
- Restaurant recommendations reference Nigerian cuisine (jollof rice, suya, amala) and popular chains (Chicken Republic, The Place, Kilimanjaro)
- Book recommendations include Nigerian literature (Achebe, Adichie, Oyeyemi)

### 3.3 Persona Templates
- Pre-built personas include "Lagos Professional," "Abuja Government Worker," "University Student," and "Market Trader"
- Each persona carries implicit preferences and communication styles that enrich the generation pipeline

---

## 4. Datasets and Training

We train on three datasets:
1. **Amazon Reviews 2023** (McAuley Lab): Electronics category — product reviews with ratings
2. **Yelp Reviews**: Restaurant and service reviews with 1-5 star ratings
3. **Goodreads**: Book reviews for cross-domain recommendation

Combined training set: **59,981 reviews** from **4,500 users** across **7,000 items**.

The XGBoost rating predictor is trained with 80/20 train-validation split, achieving:
- Training RMSE: 0.85
- Validation RMSE: 0.92

---

## 5. Evaluation

### 5.1 Metrics

**Task A** is evaluated using:
- **RMSE** (Root Mean Squared Error): Measures rating prediction accuracy
- **ROUGE-1, ROUGE-2, ROUGE-L**: Measures n-gram overlap between generated and reference reviews
- **BERTScore**: Measures semantic similarity using contextual embeddings

**Task B** is evaluated using:
- **NDCG@10** (Normalized Discounted Cumulative Gain): Measures ranking quality of recommendations
- **Hit Rate@10**: Measures whether relevant items appear in the top-10

### 5.2 Results

| Metric | Score |
|:---|:---:|
| Rating RMSE | 0.92 |
| ROUGE-1 | 0.28 |
| ROUGE-L | 0.22 |
| BERTScore F1 | 0.85 |
| NDCG@10 | 0.45 |
| Hit Rate@10 | 0.52 |

---

## 6. Technical Stack

| Component | Technology |
|:---|:---|
| Primary LLM | Groq — Llama-3.3-70B-Versatile |
| Fallback LLM | OpenAI — GPT-4o-mini |
| Embeddings | Sentence-Transformers (all-MiniLM-L6-v2) |
| Vector Store | ChromaDB 1.5.9 |
| Rating Model | XGBoost + Collaborative Filtering |
| Backend | FastAPI |
| Frontend | Streamlit |
| Containerization | Docker + Docker Compose |
| Language | Python 3.11+ |

---

## 7. Deployment

NaijaReview AI is fully containerized for one-command deployment:

```bash
docker-compose up --build
```

This starts:
- **FastAPI API** on port 8000 (with interactive docs at `/docs`)
- **Streamlit UI** on port 8501

The system requires only API keys for Groq and/or OpenAI, configured via environment variables.

---

## 8. Conclusion

NaijaReview AI demonstrates that agentic LLM architectures can effectively bridge the gap between statistical recommendation methods and contextual understanding. By combining collaborative filtering signals with LLM reasoning, our system produces personalized reviews and recommendations that are both statistically grounded and contextually aware. The Nigerian contextualization module shows how LLM agents can be adapted to serve specific cultural and linguistic communities without requiring dedicated training data.

---

## References

1. McAuley, J. et al. "Amazon Reviews 2023." HuggingFace Datasets.
2. Zhang, T. et al. "BERTScore: Evaluating Text Generation with BERT." ICLR 2020.
3. Lin, C.Y. "ROUGE: A Package for Automatic Evaluation of Summaries." ACL 2004.
4. Chen, T. & Guestrin, C. "XGBoost: A Scalable Tree Boosting System." KDD 2016.
5. Reimers, N. & Gurevych, I. "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks." EMNLP 2019.
6. Koren, Y. et al. "Matrix Factorization Techniques for Recommender Systems." IEEE Computer, 2009.
