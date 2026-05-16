"""NaijaReview AI — Clean Dashboard (Light Theme)"""
import uuid, requests, streamlit as st
from app.styles import CUSTOM_CSS

st.set_page_config(page_title="NaijaReview AI", page_icon="🇳🇬", layout="wide", initial_sidebar_state="expanded")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
API = "http://localhost:8000"

def health():
    try: return requests.get(f"{API}/health", timeout=3).json()
    except: return None

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0.5rem 0.5rem;">
        <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:36px;height:36px;border-radius:10px;background:#1a7a4c;color:white;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:0.85rem;">NR</div>
            <div><div style="font-weight:700;font-size:1rem;color:#1a1d21;">NaijaReview AI</div>
            <div style="font-size:0.72rem;color:#8492a6;">AI that understands Naija you</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio("", ["🏠  Dashboard", "✏️  User Modeling", "🎯  Recommendations", "💬  Conversations", "⚙️  Settings"],
                     label_visibility="collapsed")

    st.markdown("---")
    st.markdown("""
    <div style="background:#f8f9fb;border-radius:10px;padding:1rem;margin-top:auto;">
        <div style="font-weight:700;font-size:0.82rem;color:#1a7a4c;">About NaijaReview AI</div>
        <div style="font-size:0.75rem;color:#8492a6;margin-top:4px;line-height:1.5;">
            Agentic AI system that understands Nigerian context, language, and preferences to generate reviews and personalized recommendations.
        </div>
        <div style="margin-top:8px;">
            <span style="display:inline-block;width:14px;height:14px;background:#1a7a4c;border-radius:3px;margin-right:4px;"></span>
            <span style="display:inline-block;width:14px;height:14px;background:#145f3b;border-radius:3px;"></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── TOP BAR ──
h = health()
tc1, tc2 = st.columns([4, 1])
with tc1:
    st.markdown('<div class="top-bar-left"><h2>Welcome back! 👋</h2><p>What would you like to do today?</p></div>', unsafe_allow_html=True)
with tc2:
    if h:
        st.markdown('<div class="status-pill"><span class="dot"></span> System Online</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-pill" style="color:#ef4444;"><span class="dot" style="background:#ef4444;"></span> Offline</div>', unsafe_allow_html=True)

# ════════════════════════════════════════
# DASHBOARD PAGE
# ════════════════════════════════════════
if "Dashboard" in page:
    # Task Cards
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.markdown("""
        <div class="task-card">
            <div class="task-icon task-icon-a">📝</div>
            <h3>Generate Review (Task A)</h3>
            <p>Generate a personalized review and rating for any product or service.</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Generate Review →", type="primary", key="go_a"):
            st.session_state["_page"] = "modeling"
    with c2:
        st.markdown("""
        <div class="task-card">
            <div class="task-icon task-icon-b">🎯</div>
            <h3>Get Recommendations (Task B)</h3>
            <p>Get AI-powered recommendations tailored to your preferences.</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Get Recommendations →", type="primary", key="go_b"):
            st.session_state["_page"] = "recs"

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # Profile + Activity
    c1, c2 = st.columns([3, 2], gap="medium")
    with c1:
        st.markdown("""
        <div class="profile-card">
            <h4>👤 Your Profile Summary</h4>
            <div style="display:flex;align-items:center;">
                <div class="profile-avatar">NR</div>
                <div>
                    <span class="profile-name">Naija Reviewer</span>
                    <span class="profile-location">Lagos, Nigeria</span>
                    <div style="font-size:0.75rem;color:#8492a6;margin-top:2px;">Active since May 2026</div>
                </div>
            </div>
            <div class="stat-row">
                <div class="stat-item"><div class="stat-value">23</div><div class="stat-label">Reviews Written</div></div>
                <div class="stat-item"><div class="stat-value">4.2</div><div class="stat-label">Avg Rating</div></div>
                <div class="stat-item"><div class="stat-value">12</div><div class="stat-label">Categories</div></div>
                <div class="stat-item"><div class="stat-value">156</div><div class="stat-label">Items Explored</div></div>
            </div>
            <div style="margin-top:1rem;padding-top:0.8rem;border-top:1px solid #f0f3f7;">
                <div style="font-size:0.82rem;font-weight:600;color:#1a7a4c;margin-bottom:6px;">✨ Your Taste Profile</div>
                <div style="font-size:0.82rem;color:#4a5568;margin-bottom:8px;">You love trying new spots, especially Nigerian food 🍛, and you're big on honest reviews.</div>
                <span class="tag">Foodie</span><span class="tag">Honest Reviewer</span><span class="tag">Loves Local</span><span class="tag">Explores Often</span>
            </div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="activity-card">
            <h4 style="margin:0 0 0.8rem;font-size:0.95rem;font-weight:700;">🕐 Recent Activity</h4>
            <div class="activity-item"><span class="activity-text">💬 Generated review for Jollof Spot, Lekki</span><span class="activity-time">2 mins ago</span></div>
            <div class="activity-item"><span class="activity-text">⭐ Rated "Atomic Habits" by James Clear</span><span class="activity-time">1 hour ago</span></div>
            <div class="activity-item"><span class="activity-text">💬 Asked for book recommendations</span><span class="activity-time">3 hours ago</span></div>
            <div class="activity-item"><span class="activity-text">🎯 Got recommendations for tech gadgets</span><span class="activity-time">5 hours ago</span></div>
            <div class="activity-item"><span class="activity-text">✅ Generated review for Nike Air Max 270</span><span class="activity-time">1 day ago</span></div>
        </div>""", unsafe_allow_html=True)

    # Chat Bar
    st.markdown("""
    <div class="chat-bar">
        <h4>💬 Chat with NaijaReview AI</h4>
        <p>Ask anything about products, get recommendations, or refine your preferences.</p>
    </div>""", unsafe_allow_html=True)
    chat_q = st.text_input("Chat", placeholder="E.g., Abeg recommend good suya spot in Abuja...", label_visibility="collapsed", key="dash_chat")
    st.markdown("""
    <div style="margin-top:4px;">
        <span style="font-size:0.78rem;font-weight:600;color:#8492a6;">Try asking:</span>
        <span class="suggestion-chip">Recommend a good restaurant in VI</span>
        <span class="suggestion-chip">Books like Rich Dad Poor Dad</span>
        <span class="suggestion-chip">Best headphones under 50k</span>
        <span class="suggestion-chip">Why did you recommend this?</span>
    </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════
# USER MODELING PAGE
# ════════════════════════════════════════
elif "Modeling" in page:
    st.markdown("### ✏️ Generate Review & Rating")
    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        uid = st.text_input("User ID", "demo_user_001", key="m_uid")
        st.checkbox("Use sample review history", True, key="m_sample")
        item = st.text_input("Item Name", "Samsung Galaxy Buds3 Pro")
        cat = st.selectbox("Category", ["Electronics","Restaurants","Books","Movies","Fashion"])
        desc = st.text_area("Description", "Premium wireless earbuds with ANC and 360 Audio.", height=80)
        is_ng = st.toggle("🇳🇬 Nigerian Mode", True)
        region = st.selectbox("Region", ["Lagos","Abuja","Port Harcourt","Kano"]) if is_ng else ""

    with c2:
        if st.button("Generate Review →", type="primary", use_container_width=True, key="gen"):
            reviews = [
                {"rating":5,"review_text":"Amazing! Best purchase this year.","item_name":"Wireless Headphones","category":"Electronics"},
                {"rating":4,"review_text":"Pretty good. Minor packaging issue.","item_name":"Phone Case","category":"Electronics"},
                {"rating":2,"review_text":"Disappointed. Returning.","item_name":"USB Cable","category":"Electronics"},
                {"rating":5,"review_text":"Best jollof in Lagos!","item_name":"Mama Put","category":"Restaurants"},
                {"rating":3,"review_text":"Okay book. Lost me mid-chapters.","item_name":"Half of a Yellow Sun","category":"Books"},
            ] if st.session_state.get("m_sample") else []
            with st.spinner("Agent reasoning..."):
                try:
                    r = requests.post(f"{API}/task-a/generate", json={
                        "user_id":uid,"item_name":item,"item_category":cat,
                        "item_description":desc,"user_reviews":reviews,
                        "is_nigerian":is_ng,"region":region,
                    }, timeout=120)
                    if r.ok: st.session_state["a_out"] = r.json()
                    else: st.error(r.text[:200])
                except Exception as e: st.error(str(e)[:200])

        if "a_out" in st.session_state:
            d = st.session_state["a_out"]
            mc = st.columns(3)
            mc[0].metric("Rating", f"{d['rating']}★")
            mc[1].metric("Confidence", f"{d['confidence']:.0%}")
            mc[2].metric("Words", len(d["review_text"].split()))
            st.markdown(f'<div class="review-output">{d["review_text"]}</div>', unsafe_allow_html=True)
            with st.expander("Agent Reasoning"): st.write(d.get("reasoning","—"))

# ════════════════════════════════════════
# RECOMMENDATIONS PAGE
# ════════════════════════════════════════
elif "Recommendations" in page:
    st.markdown("### 🎯 Personalized Recommendations")
    c1, c2 = st.columns([2, 3], gap="large")
    with c1:
        uid = st.text_input("User ID", "demo_user_001", key="r_uid")
        q = st.text_input("What are you looking for?", placeholder="Good earbuds for Lagos traffic")
        k = st.slider("Results", 3, 15, 8)
        cf = st.selectbox("Category filter", [None,"Electronics","Restaurants","Books"], key="r_cf")
        if st.button("Get Recommendations →", type="primary", use_container_width=True, key="rec"):
            with st.spinner("Searching & ranking..."):
                try:
                    r = requests.post(f"{API}/task-b/recommend", json={
                        "user_id":uid,"query":q,"top_k":k,"is_nigerian":True,"category_filter":cf,
                        "user_reviews":[
                            {"rating":5,"review_text":"Love this!","item_name":"JBL Speaker","category":"Electronics"},
                            {"rating":4,"review_text":"Great read","item_name":"Things Fall Apart","category":"Books"},
                        ]
                    }, timeout=120)
                    if r.ok: st.session_state["recs"] = r.json()
                    else: st.error(r.text[:200])
                except Exception as e: st.error(str(e)[:200])
    with c2:
        if "recs" in st.session_state:
            data = st.session_state["recs"]
            st.caption(f"{data.get('total_candidates_considered',0)} candidates evaluated")
            for rec in data.get("recommendations",[]):
                st.markdown(f"""<div class="rec-item">
                    <div class="rec-rank">{rec['rank']}</div>
                    <div style="flex:1;">
                        <div class="rec-name">{rec['item_name']}</div>
                        <span class="rec-cat">{rec.get('category','—')}</span>
                        <div class="rec-why">{rec.get('explanation','')[:180]}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════
# CONVERSATIONS PAGE
# ════════════════════════════════════════
elif "Conversations" in page:
    st.markdown("### 💬 Chat with NaijaReview AI")
    uid = st.text_input("User ID", "demo_user_001", key="c_uid")
    if "sid" not in st.session_state: st.session_state["sid"] = str(uuid.uuid4())
    if "msgs" not in st.session_state: st.session_state["msgs"] = []
    for m in st.session_state["msgs"]:
        with st.chat_message(m["role"]): st.write(m["content"])
    if p := st.chat_input("Ask for recommendations..."):
        st.session_state["msgs"].append({"role":"user","content":p})
        with st.chat_message("user"): st.write(p)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    r = requests.post(f"{API}/task-b/chat", json={
                        "user_id":uid,"message":p,"session_id":st.session_state["sid"],"is_nigerian":True
                    }, timeout=60)
                    if r.ok:
                        resp = r.json()["response"]; st.write(resp)
                        st.session_state["msgs"].append({"role":"assistant","content":resp})
                    else: st.error(r.text[:200])
                except Exception as e: st.error(str(e)[:200])

# ════════════════════════════════════════
# SETTINGS PAGE
# ════════════════════════════════════════
elif "Settings" in page:
    st.markdown("### ⚙️ Settings")
    st.markdown("#### Training")
    c1, c2, c3 = st.columns(3)
    amz = c1.number_input("Amazon reviews", 20000, step=5000)
    ylp = c2.number_input("Yelp reviews", 15000, step=5000)
    gdr = c3.number_input("Goodreads reviews", 10000, step=5000)
    if st.button("Train All Models", type="primary"):
        with st.spinner("Training..."):
            try:
                r = requests.post(f"{API}/train", json={"amazon_max":amz,"yelp_max":ylp,"goodreads_max":gdr}, timeout=600)
                if r.ok:
                    d = r.json()
                    st.success(f"✅ {d['total_reviews']:,} reviews · {d['total_users']:,} users · {d['total_items']:,} items")
                else: st.error(r.text[:200])
            except Exception as e: st.error(str(e)[:200])
    st.markdown("#### System Info")
    if h:
        st.json(h)
