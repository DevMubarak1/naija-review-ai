"""
NaijaReview AI — Premium Dashboard
Dark luxe aesthetic with Nigerian-inspired gold accents.
"""

import uuid
import requests
import streamlit as st
from app.styles import CUSTOM_CSS

st.set_page_config(
    page_title="NaijaReview AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
API_URL = "http://localhost:8000"


def api_healthy():
    try:
        r = requests.get(f"{API_URL}/health", timeout=3)
        return r.json() if r.ok else None
    except Exception:
        return None


# ── HERO ──
st.markdown("""
<div class="hero-banner">
    <h1>NaijaReview AI</h1>
    <div class="hero-subtitle">LLM-Powered User Modeling & Personalized Recommendation Engine</div>
    <div class="hero-team">Team Cerebral · DSN × BCT Hackathon 3.0</div>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown('<div class="section-label">Configuration</div>', unsafe_allow_html=True)
    is_nigerian = st.toggle("🇳🇬 Nigerian Mode", value=True)
    region = ""
    if is_nigerian:
        region = st.selectbox("Region", ["Lagos", "Abuja", "Port Harcourt", "Kano", "Ibadan"])

    st.markdown("---")
    st.markdown('<div class="section-label">System</div>', unsafe_allow_html=True)
    health = api_healthy()
    if health:
        st.markdown('<div class="status-online">API Online</div>', unsafe_allow_html=True)
        trained = health.get("models_trained", False)
        st.caption(f"Models: {'Trained ✓' if trained else 'Not trained'}")
    else:
        st.error("API offline")

    st.markdown("---")
    st.markdown('<div class="section-label">Training</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    amz = c1.number_input("Amazon", value=20000, step=5000)
    ylp = c2.number_input("Yelp", value=15000, step=5000)
    gdr = st.number_input("Goodreads", value=10000, step=5000)
    if st.button("Train Models", use_container_width=True, type="primary"):
        with st.spinner("Training…"):
            try:
                r = requests.post(f"{API_URL}/train", json={
                    "amazon_max": amz, "yelp_max": ylp, "goodreads_max": gdr
                }, timeout=600)
                if r.ok:
                    d = r.json()
                    st.success(f"{d['total_reviews']:,} reviews · {d['total_users']:,} users")
                else:
                    st.error(r.text[:200])
            except Exception as e:
                st.error(str(e)[:200])

# ── TABS ──
tab_a, tab_b, tab_c = st.tabs(["✦  User Modeling", "◉  Recommendations", "◈  Conversation"])

# ════════════════════════════════════════
# TAB A — USER MODELING
# ════════════════════════════════════════
with tab_a:
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="section-label">User Persona</div>', unsafe_allow_html=True)
        user_id_a = st.text_input("User ID", "demo_user_001", key="ua")
        use_sample = st.checkbox("Use sample history", True)

        if use_sample:
            user_reviews = [
                {"rating": 5, "review_text": "Absolutely fantastic! Best purchase this year. Quality is top-notch.", "item_name": "Wireless Headphones", "category": "Electronics"},
                {"rating": 4, "review_text": "Pretty good overall. Does what it promises. Minor packaging issue.", "item_name": "Phone Case", "category": "Electronics"},
                {"rating": 2, "review_text": "Disappointed. Doesn't match the description. Returning.", "item_name": "USB Cable", "category": "Electronics"},
                {"rating": 5, "review_text": "The jollof rice was the best in Lagos! Will come back.", "item_name": "Mama Put Restaurant", "category": "Restaurants"},
                {"rating": 3, "review_text": "Okay book. Started strong but lost me mid-chapters.", "item_name": "Half of a Yellow Sun", "category": "Books"},
            ]
        else:
            raw = st.text_area("Paste review JSON", height=150, key="rev_json")
            try:
                user_reviews = eval(raw) if raw else []
            except Exception:
                user_reviews = []

        st.markdown('<div class="section-label">Product Details</div>', unsafe_allow_html=True)
        item_name = st.text_input("Item Name", "Samsung Galaxy Buds3 Pro")
        item_cat = st.selectbox("Category", ["Electronics", "Restaurants", "Books", "Movies", "Fashion"])
        item_desc = st.text_area("Description", "Premium wireless earbuds with ANC and 360 Audio.", height=80)

    with right:
        st.markdown('<div class="section-label">Generated Output</div>', unsafe_allow_html=True)

        if st.button("Generate Review", use_container_width=True, type="primary", key="gen"):
            with st.spinner("Agent reasoning…"):
                try:
                    r = requests.post(f"{API_URL}/task-a/generate", json={
                        "user_id": user_id_a, "item_name": item_name,
                        "item_category": item_cat, "item_description": item_desc,
                        "user_reviews": user_reviews, "is_nigerian": is_nigerian, "region": region,
                    }, timeout=120)

                    if r.ok:
                        d = r.json()
                        st.session_state["task_a_result"] = d
                    else:
                        st.error(f"Error: {r.text[:200]}")
                except Exception as e:
                    st.error(str(e)[:200])

        if "task_a_result" in st.session_state:
            d = st.session_state["task_a_result"]
            c1, c2, c3 = st.columns(3)
            c1.markdown(f'<div class="metric-card"><div class="metric-value">{d["rating"]}★</div><div class="metric-label">Rating</div></div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="metric-card"><div class="metric-value">{d["confidence"]:.0%}</div><div class="metric-label">Confidence</div></div>', unsafe_allow_html=True)
            wc = len(d["review_text"].split())
            c3.markdown(f'<div class="metric-card"><div class="metric-value">{wc}</div><div class="metric-label">Words</div></div>', unsafe_allow_html=True)

            st.markdown(f'<div class="review-block">{d["review_text"]}</div>', unsafe_allow_html=True)

            with st.expander("Agent Reasoning"):
                st.write(d.get("reasoning", "—"))
            with st.expander("User Profile"):
                st.write(d.get("user_profile_summary", "—"))

# ════════════════════════════════════════
# TAB B — RECOMMENDATIONS
# ════════════════════════════════════════
with tab_b:
    left, right = st.columns([2, 3], gap="large")

    with left:
        st.markdown('<div class="section-label">Query</div>', unsafe_allow_html=True)
        user_id_b = st.text_input("User ID", "demo_user_001", key="ub")
        query = st.text_input("What are you looking for?", placeholder="Good earbuds for Lagos traffic")
        top_k = st.slider("Results", 3, 15, 8)
        cat_filter = st.selectbox("Category", [None, "Electronics", "Restaurants", "Books"], key="cf")

        if st.button("Get Recommendations", use_container_width=True, type="primary", key="rec"):
            with st.spinner("Searching & ranking…"):
                try:
                    payload = {
                        "user_id": user_id_b, "query": query, "top_k": top_k,
                        "is_nigerian": is_nigerian, "category_filter": cat_filter,
                        "user_reviews": [
                            {"rating": 5, "review_text": "Love this!", "item_name": "JBL Speaker", "category": "Electronics"},
                            {"rating": 4, "review_text": "Great read", "item_name": "Things Fall Apart", "category": "Books"},
                        ]
                    }
                    r = requests.post(f"{API_URL}/task-b/recommend", json=payload, timeout=120)
                    if r.ok:
                        st.session_state["recs"] = r.json()
                    else:
                        st.error(r.text[:200])
                except Exception as e:
                    st.error(str(e)[:200])

    with right:
        st.markdown('<div class="section-label">Results</div>', unsafe_allow_html=True)
        if "recs" in st.session_state:
            data = st.session_state["recs"]
            st.caption(f"{data.get('total_candidates_considered', 0)} candidates evaluated")
            for rec in data.get("recommendations", []):
                st.markdown(f"""
                <div class="rec-card">
                    <div class="rec-rank">{rec['rank']}</div>
                    <div style="flex:1;">
                        <div class="rec-name">{rec['item_name']}</div>
                        <span class="rec-category">{rec.get('category','—')}</span>
                        <div class="rec-explanation">{rec.get('explanation','')[:180]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ════════════════════════════════════════
# TAB C — CONVERSATION
# ════════════════════════════════════════
with tab_c:
    st.markdown('<div class="section-label">Chat with NaijaReview AI</div>', unsafe_allow_html=True)
    user_id_c = st.text_input("User ID", "demo_user_001", key="uc")

    if "chat_sid" not in st.session_state:
        st.session_state["chat_sid"] = str(uuid.uuid4())
    if "chat_msgs" not in st.session_state:
        st.session_state["chat_msgs"] = []

    for m in st.session_state["chat_msgs"]:
        with st.chat_message(m["role"]):
            st.write(m["content"])

    if prompt := st.chat_input("Ask for recommendations…"):
        st.session_state["chat_msgs"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                try:
                    r = requests.post(f"{API_URL}/task-b/chat", json={
                        "user_id": user_id_c, "message": prompt,
                        "session_id": st.session_state["chat_sid"],
                        "is_nigerian": is_nigerian,
                    }, timeout=60)
                    if r.ok:
                        resp = r.json()["response"]
                        st.write(resp)
                        st.session_state["chat_msgs"].append({"role": "assistant", "content": resp})
                    else:
                        st.error(r.text[:200])
                except Exception as e:
                    st.error(str(e)[:200])

    if st.button("Clear Chat", key="clr"):
        st.session_state["chat_msgs"] = []
        st.session_state["chat_sid"] = str(uuid.uuid4())
        st.rerun()
