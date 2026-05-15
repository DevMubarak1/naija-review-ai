"""
NaijaReview AI — FastAPI Backend
RESTful API for both Task A (User Modeling) and Task B (Recommendation).
"""

import uuid
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger


# ============================================================
# REQUEST/RESPONSE MODELS
# ============================================================

class TaskARequest(BaseModel):
    """Request for Task A: Generate review + rating."""
    user_id: str = Field(..., description="User identifier")
    item_name: str = Field(..., description="Product/service name")
    item_category: str = Field(default="General", description="Product category")
    item_description: str = Field(default="", description="Product description")
    item_id: str = Field(default="", description="Item ID for collaborative filtering")
    user_reviews: Optional[list[dict]] = Field(default=None, description="User review history")
    is_nigerian: bool = Field(default=False, description="Nigerian contextualization")
    region: str = Field(default="", description="Nigerian region")


class TaskAResponse(BaseModel):
    """Response for Task A."""
    user_id: str
    item_name: str
    rating: float
    review_text: str
    confidence: float
    reasoning: str
    user_profile_summary: str
    is_nigerian: bool


class TaskBRequest(BaseModel):
    """Request for Task B: Get recommendations."""
    user_id: str = Field(..., description="User identifier")
    query: str = Field(default="", description="Natural language query")
    user_reviews: Optional[list[dict]] = Field(default=None, description="User review history")
    top_k: int = Field(default=10, description="Number of recommendations")
    is_nigerian: bool = Field(default=False, description="Nigerian contextualization")
    category_filter: Optional[str] = Field(default=None, description="Category filter")


class TaskBResponse(BaseModel):
    """Response for Task B."""
    user_id: str
    recommendations: list[dict]
    user_summary: str
    query: str
    total_candidates_considered: int


class ConversationRequest(BaseModel):
    """Request for conversational recommendation."""
    user_id: str
    message: str
    session_id: str = Field(default="", description="Session ID for multi-turn")
    is_nigerian: bool = False


class ConversationResponse(BaseModel):
    """Response for conversational recommendation."""
    response: str
    session_id: str
    turn: int


class TrainRequest(BaseModel):
    """Request to train models on datasets."""
    amazon_max: int = Field(default=50000, description="Max Amazon reviews")
    yelp_max: int = Field(default=30000, description="Max Yelp reviews")
    goodreads_max: int = Field(default=20000, description="Max Goodreads reviews")


class HealthResponse(BaseModel):
    status: str
    version: str
    models_trained: bool


# ============================================================
# APP SETUP
# ============================================================

_models_trained = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic."""
    global _models_trained
    logger.info("🚀 NaijaReview AI starting up...")

    # Try to load pre-trained models
    try:
        from app.agents.user_modeling.rating_predictor import rating_predictor
        rating_predictor.load_model()
        if rating_predictor.is_trained:
            _models_trained = True
            logger.info("Pre-trained rating model loaded ✓")
    except Exception as e:
        logger.info(f"No pre-trained model found: {e}")

    yield
    logger.info("NaijaReview AI shutting down...")


app = FastAPI(
    title="NaijaReview AI",
    description="LLM Agent for User Modeling & Personalized Recommendation — DSN x BCT Hackathon 3.0",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ENDPOINTS
# ============================================================

@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy", version="1.0.0", models_trained=_models_trained,
    )


@app.post("/train", tags=["System"])
async def train_models(req: TrainRequest):
    """Download datasets and train all models."""
    global _models_trained
    logger.info("Starting model training pipeline...")

    try:
        from app.data.loader import load_all_datasets
        from app.agents.user_modeling.rating_predictor import rating_predictor
        from app.agents.recommendation.pipeline import recommendation_pipeline

        # Load data
        df = load_all_datasets(
            amazon_max=req.amazon_max, yelp_max=req.yelp_max, goodreads_max=req.goodreads_max,
        )

        # Train rating predictor
        rating_predictor.train(df)

        # Index items for recommendations
        items_df = df.groupby("item_id").agg(
            item_name=("item_name", "first"),
            category=("category", "first"),
            avg_rating=("rating", "mean"),
            review_count=("rating", "count"),
            source=("source", "first") if "source" in df.columns else ("category", "first"),
        ).reset_index()

        items = items_df.to_dict("records")
        recommendation_pipeline.index_items(items)

        _models_trained = True
        return {
            "status": "success",
            "total_reviews": len(df),
            "total_users": df["user_id"].nunique(),
            "total_items": df["item_id"].nunique(),
            "items_indexed": len(items),
        }
    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/task-a/generate", response_model=TaskAResponse, tags=["Task A — User Modeling"])
async def generate_review(req: TaskARequest):
    """Task A: Generate a review and rating for a user-item pair."""
    try:
        from app.agents.user_modeling.pipeline import user_modeling_pipeline

        result = user_modeling_pipeline.run(
            user_id=req.user_id,
            item_name=req.item_name,
            item_category=req.item_category,
            item_description=req.item_description,
            item_id=req.item_id,
            reviews=req.user_reviews,
            is_nigerian=req.is_nigerian,
            region=req.region,
        )
        return TaskAResponse(**result)
    except Exception as e:
        logger.error(f"Task A failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/task-b/recommend", response_model=TaskBResponse, tags=["Task B — Recommendation"])
async def get_recommendations(req: TaskBRequest):
    """Task B: Get personalized recommendations for a user."""
    try:
        from app.agents.recommendation.pipeline import recommendation_pipeline

        result = recommendation_pipeline.recommend(
            user_id=req.user_id,
            query=req.query,
            user_reviews=req.user_reviews,
            top_k=req.top_k,
            is_nigerian=req.is_nigerian,
            category_filter=req.category_filter,
        )
        return TaskBResponse(**result)
    except Exception as e:
        logger.error(f"Task B failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/task-b/chat", response_model=ConversationResponse, tags=["Task B — Recommendation"])
async def conversational_recommend(req: ConversationRequest):
    """Task B: Multi-turn conversational recommendation."""
    try:
        from app.agents.recommendation.pipeline import recommendation_pipeline

        session_id = req.session_id or str(uuid.uuid4())
        result = recommendation_pipeline.conversational_recommend(
            user_id=req.user_id,
            message=req.message,
            session_id=session_id,
            is_nigerian=req.is_nigerian,
        )
        return ConversationResponse(**result)
    except Exception as e:
        logger.error(f"Chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users", tags=["Data"])
async def list_users():
    """List all modeled user profiles."""
    from app.core.memory import memory_store
    profiles = memory_store.list_profiles()
    return {"users": profiles, "count": len(profiles)}


@app.get("/users/{user_id}", tags=["Data"])
async def get_user_profile(user_id: str):
    """Get a specific user profile."""
    from app.core.memory import memory_store
    profile = memory_store.load_profile(user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return profile.to_dict()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
