"""
NaijaReview AI — Streamlit Web Application
Interactive UI for both Task A (User Modeling) and Task B (Recommendation).
"""

import uuid
import requests
import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="NaijaReview AI — DSN x BCT Hackathon",
    page_icon="🇳🇬",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = "http://localhost:8000"

# ============================================================
# CUSTOM STYLING
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    .main-header h1 { margin: 0; font-size: 2.5rem; }
    .main-header p { margin: 0.5rem 0 0; opacity: 0.8; font-size: 1.1rem; }

    .task-card {
        background: linear-gradient(145deg, #ffffff 0%, #f0f4ff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e0e7ff;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    .review-output {
        background: #f8fafc;
        border-left: 4px solid #10b981;
        padding: 1.5rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
        font-size: 1.05rem;
        line-height: 1.7;
    }

    .recommendation-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        transition: transform 0.2s;
    }
    .recommendation-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }

    .rating-stars { color: #f59e0b; font-size: 1.3rem; }
    .confidence-badge {
        display: inline-block; padding: 0.2rem 0.6rem; border-radius: 12px;
        font-size: 0.8rem; font-weight: 600;
    }
    .confidence-high { background: #dcfce7; color: #166534; }
    .confidence-med { background: #fef3c7; color: #92400e; }
    .confidence-low { background: #fee2e2; color: #991b1b; }

    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; padding: 1.2rem; border-radius: 12px; text-align: center;
    }
    .metric-card h3 { margin: 0; font-size: 1.8rem; }
    .metric-card p { margin: 0.3rem 0 0; opacity: 0.9; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="main-header">
    <h1>🇳🇬 NaijaReview AI</h1>
    <p>LLM Agent for User Modeling & Personalized Recommendation</p>
    <p style="font-size: 0.9rem; opacity: 0.6;">Team Cerebral — DSN × BCT Data & AI Summit Hackathon 3.0</p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## ⚙️ Settings")

    is_nigerian = st.toggle("🇳🇬 Nigerian Mode", value=True,
                            help="Enable Nigerian English/Pidgin contextualization")

    region = ""
    if is_nigerian:
        region = st.selectbox("Region", ["Lagos", "Abuja", "Port Harcourt", "Kano", "Ibadan", "Other"])

    st.divider()

    # System status
    st.markdown("## 📊 System Status")
    try:
        health = requests.get(f"{API_URL}/health", timeout=3).json()
        st.success(f"API: {health['status']} ✓")
        st.info(f"Models trained: {'Yes ✓' if health['models_trained'] else 'No — click Train below'}")
    except Exception:
        st.error("API not running. Start with: `uvicorn app.main:app`")

    st.divider()

    # Training button
    st.markdown("## 🎓 Train Models")
    col1, col2 = st.columns(2)
    amazon_max = col1.number_input("Amazon reviews", value=50000, step=10000)
    yelp_max = col2.number_input("Yelp reviews", value=30000, step=10000)
    goodreads_max = st.number_input("Goodreads reviews", value=20000, step=10000)

    if st.button("🚀 Train All Models", use_container_width=True, type="primary"):
        with st.spinner("Training models... (this may take several minutes)"):
            try:
                resp = requests.post(f"{API_URL}/train", json={
                    "amazon_max": amazon_max, "yelp_max": yelp_max, "goodreads_max": goodreads_max,
                }, timeout=600)
                if resp.status_code == 200:
                    data = resp.json()
                    st.success(f"✅ Trained on {data['total_reviews']} reviews, "
                               f"{data['total_users']} users, {data['total_items']} items")
                else:
                    st.error(f"Training failed: {resp.text}")
            except Exception as e:
                st.error(f"Error: {e}")


# ============================================================
# MAIN TABS
# ============================================================
tab1, tab2, tab3 = st.tabs(["📝 Task A: User Modeling", "🎯 Task B: Recommendations", "💬 Chat"])


# ============================================================
# TAB 1: TASK A — USER MODELING
# ============================================================
with tab1:
    st.markdown("### Generate Reviews & Ratings")
    st.markdown("Enter a user persona and product details. The agent will generate a realistic review in the user's style.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 👤 User Persona")
        user_id_a = st.text_input("User ID", value="demo_user_001", key="user_id_a")

        st.markdown("**Sample Review History** (paste or use defaults)")
        use_sample = st.checkbox("Use sample user history", value=True)

        if use_sample:
            user_reviews = [
                {"rating": 5, "review_text": "Absolutely fantastic product! Best purchase I've made this year. The quality is top-notch and delivery was swift.", "item_name": "Wireless Headphones", "category": "Electronics"},
                {"rating": 4, "review_text": "Pretty good overall. Does what it promises. Minor issue with the packaging but the product itself is solid.", "item_name": "Phone Case", "category": "Electronics"},
                {"rating": 2, "review_text": "Disappointed. The product doesn't match the description at all. Returning this.", "item_name": "USB Cable", "category": "Electronics"},
                {"rating": 5, "review_text": "Amazing restaurant! The jollof rice was the best I've had in Lagos. Will definitely come back.", "item_name": "Mama Put Restaurant", "category": "Restaurants"},
                {"rating": 3, "review_text": "The book was okay. Started strong but lost me in the middle chapters. Decent ending though.", "item_name": "Half of a Yellow Sun", "category": "Books"},
            ]
            st.json(user_reviews)
        else:
            user_reviews_str = st.text_area("Review history (JSON)", height=200)
            try:
                user_reviews = eval(user_reviews_str) if user_reviews_str else []
            except Exception:
                user_reviews = []

    with col2:
        st.markdown("#### 📦 Product Details")
        item_name = st.text_input("Item Name", value="Samsung Galaxy Buds3 Pro")
        item_category = st.selectbox("Category", ["Electronics", "Restaurants", "Books", "Movies", "Fashion", "General"])
        item_description = st.text_area("Description (optional)", value="Premium wireless earbuds with active noise cancellation, 360 Audio, and enhanced call quality.")

    if st.button("🚀 Generate Review", use_container_width=True, type="primary", key="gen_review"):
        with st.spinner("Agent is analyzing user persona and generating review..."):
            try:
                resp = requests.post(f"{API_URL}/task-a/generate", json={
                    "user_id": user_id_a, "item_name": item_name,
                    "item_category": item_category, "item_description": item_description,
                    "user_reviews": user_reviews, "is_nigerian": is_nigerian, "region": region,
                }, timeout=120)

                if resp.status_code == 200:
                    data = resp.json()

                    # Display results
                    st.markdown("---")
                    st.markdown("### 📄 Generated Output")

                    mcol1, mcol2, mcol3 = st.columns(3)
                    with mcol1:
                        stars = "⭐" * int(data["rating"])
                        st.markdown(f'<div class="metric-card"><h3>{data["rating"]}★</h3><p>Predicted Rating</p></div>', unsafe_allow_html=True)
                    with mcol2:
                        conf = data["confidence"]
                        cls = "high" if conf > 0.7 else ("med" if conf > 0.4 else "low")
                        st.markdown(f'<div class="metric-card"><h3>{conf:.0%}</h3><p>Confidence</p></div>', unsafe_allow_html=True)
                    with mcol3:
                        wc = len(data["review_text"].split())
                        st.markdown(f'<div class="metric-card"><h3>{wc}</h3><p>Words</p></div>', unsafe_allow_html=True)

                    st.markdown(f'<div class="review-output">{data["review_text"]}</div>', unsafe_allow_html=True)

                    with st.expander("🔍 Agent Reasoning"):
                        st.write(data.get("reasoning", "N/A"))
                    with st.expander("👤 User Profile Summary"):
                        st.write(data.get("user_profile_summary", "N/A"))
                else:
                    st.error(f"API Error: {resp.text}")
            except Exception as e:
                st.error(f"Error: {e}")


# ============================================================
# TAB 2: TASK B — RECOMMENDATIONS
# ============================================================
with tab2:
    st.markdown("### Personalized Recommendations")
    st.markdown("Enter a user persona to receive personalized product/service recommendations.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("#### 👤 User Input")
        user_id_b = st.text_input("User ID", value="demo_user_001", key="user_id_b")
        query = st.text_input("What are you looking for?", placeholder="e.g., Good earbuds for commuting in Lagos traffic")
        top_k = st.slider("Number of recommendations", 3, 20, 10)
        category_filter = st.selectbox("Category filter", [None, "Electronics", "Restaurants", "Books", "Movies"], key="cat_filter")

        use_sample_b = st.checkbox("Use sample user history", value=True, key="sample_b")

        if st.button("🎯 Get Recommendations", use_container_width=True, type="primary"):
            with st.spinner("Agent is analyzing your preferences..."):
                try:
                    payload = {
                        "user_id": user_id_b, "query": query, "top_k": top_k,
                        "is_nigerian": is_nigerian, "category_filter": category_filter,
                    }
                    if use_sample_b:
                        payload["user_reviews"] = [
                            {"rating": 5, "review_text": "Love this product!", "item_name": "Wireless Headphones", "category": "Electronics"},
                            {"rating": 4, "review_text": "Great book, really enjoyed it", "item_name": "Things Fall Apart", "category": "Books"},
                            {"rating": 5, "review_text": "Best restaurant in Lekki!", "item_name": "The Place", "category": "Restaurants"},
                        ]

                    resp = requests.post(f"{API_URL}/task-b/recommend", json=payload, timeout=120)

                    if resp.status_code == 200:
                        st.session_state["recommendations"] = resp.json()
                    else:
                        st.error(f"Error: {resp.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

    with col2:
        if "recommendations" in st.session_state:
            data = st.session_state["recommendations"]
            st.markdown(f"#### 🎯 Top {len(data['recommendations'])} Recommendations")
            st.caption(f"Considered {data.get('total_candidates_considered', 'N/A')} candidates")

            for rec in data["recommendations"]:
                with st.container():
                    st.markdown(f"""
                    <div class="recommendation-card">
                        <strong>#{rec['rank']}. {rec['item_name']}</strong>
                        <span style="float:right; background:#e0e7ff; padding:2px 8px; border-radius:8px; font-size:0.8rem;">
                            {rec.get('category', 'N/A')}
                        </span>
                        <br><span style="color:#666; font-size:0.9rem;">Score: {rec.get('score', 0):.2f}</span>
                        <p style="margin:0.5rem 0 0; color:#444;">{rec.get('explanation', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)


# ============================================================
# TAB 3: CONVERSATIONAL RECOMMENDATION
# ============================================================
with tab3:
    st.markdown("### 💬 Chat with NaijaReview AI")
    st.markdown("Have a conversation to discover personalized recommendations.")

    user_id_c = st.text_input("User ID", value="demo_user_001", key="user_id_c")

    if "chat_session" not in st.session_state:
        st.session_state["chat_session"] = str(uuid.uuid4())
    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = []

    # Display chat
    for msg in st.session_state["chat_messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask for recommendations..."):
        st.session_state["chat_messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    resp = requests.post(f"{API_URL}/task-b/chat", json={
                        "user_id": user_id_c, "message": prompt,
                        "session_id": st.session_state["chat_session"],
                        "is_nigerian": is_nigerian,
                    }, timeout=60)

                    if resp.status_code == 200:
                        data = resp.json()
                        st.write(data["response"])
                        st.session_state["chat_messages"].append(
                            {"role": "assistant", "content": data["response"]}
                        )
                    else:
                        st.error(f"Error: {resp.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")

    if st.button("🗑️ Clear Chat"):
        st.session_state["chat_messages"] = []
        st.session_state["chat_session"] = str(uuid.uuid4())
        st.rerun()
