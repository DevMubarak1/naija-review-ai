# 🇳🇬 NaijaReview AI

**LLM Agent for User Modeling & Personalized Recommendation**

> Team Cerebral — DSN × BCT Data & AI Summit Hackathon 3.0

---

## 🏆 Overview

NaijaReview AI is an agentic AI system that deeply understands users as dynamic, context-sensitive individuals and generates culturally-aware reviews and hyper-personalized recommendations. The system is contextualized for Nigerian users, incorporating Nigerian English (Pidgin), cultural references, and local preferences.

### Key Features

- **Task A — User Modeling**: Generates realistic reviews and ratings by learning each user's writing style, tone, and rating behavior
- **Task B — Recommendation**: Delivers personalized recommendations using RAG, agentic reasoning, and cross-domain understanding
- **Nigerian Contextualization**: Authentic Nigerian English/Pidgin adaptation with cultural references
- **Multi-turn Conversation**: Interactive chat interface for discovering recommendations
- **Cold-Start Handling**: Works even for new users with minimal history

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                 Streamlit Web UI                │
├─────────────────────────────────────────────────┤
│                  FastAPI Backend                │
├────────────────────┬────────────────────────────┤
│   Task A Agent     │      Task B Agent          │
│  ┌──────────────┐  │  ┌──────────────────────┐  │
│  │Persona Builder│  │  │Preference Extractor  │  │
│  │Review Generator│ │  │Candidate Retriever   │  │
│  │Rating Predictor│ │  │Reasoning Re-Ranker   │  │
│  │Naija Localizer│  │  │Cold-Start Handler    │  │
│  └──────────────┘  │  │Conversational Engine │  │
│                    │  └──────────────────────┘  │
├────────────────────┴────────────────────────────┤
│          Shared Infrastructure                  │
│  ChromaDB │ Embeddings │ Memory │ LLM Client    │
└─────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# 1. Clone the repo
git clone https://github.com/DevMubarak1/naija-review-ai.git
cd naija-review-ai

# 2. Configure API keys
cp .env.example .env
# Edit .env and add your Groq/OpenAI API keys

# 3. Run with Docker
docker-compose up --build

# 4. Access the app
# Web UI:  http://localhost:8501
# API:     http://localhost:8000/docs
```

### Option 2: Local Development

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API keys
cp .env.example .env
# Edit .env

# 4. Start the API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 5. Start the UI (in another terminal)
streamlit run app/streamlit_app.py
```

### Training Models

After starting the app, you need to train the models on the datasets:

```bash
# Via API
curl -X POST http://localhost:8000/train

# Or use the Streamlit sidebar "Train All Models" button
```

## 📡 API Endpoints

| Endpoint | Method | Description |
|:---|:---:|:---|
| `/health` | GET | System health check |
| `/train` | POST | Download datasets and train models |
| `/task-a/generate` | POST | Generate review + rating for a user-item pair |
| `/task-b/recommend` | POST | Get personalized recommendations |
| `/task-b/chat` | POST | Conversational recommendation |
| `/users` | GET | List all modeled users |
| `/users/{id}` | GET | Get user profile |

## 🛠️ Tech Stack

| Component | Technology |
|:---|:---|
| LLM | Groq (Llama-3.1-70B) + OpenAI (GPT-4o-mini) fallback |
| Orchestration | LangGraph-style agentic workflows |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector Store | ChromaDB |
| Backend | FastAPI |
| Frontend | Streamlit |
| Rating Model | SVD + Bayesian Bias + Collaborative Filtering |
| Container | Docker + Docker Compose |

## 📊 Datasets

- **Amazon Reviews 2023** (McAuley Lab) — Electronics
- **Yelp Reviews** — Restaurants & Services
- **Goodreads** — Books

## 👥 Team Cerebral

DSN × BCT Data & AI Summit Hackathon 3.0

## 📄 License

MIT License
