"""NaijaReview AI — ChatGPT-style Dashboard (All buttons functional)"""
import uuid, requests, streamlit as st
from app.styles import CUSTOM_CSS, LOGO_SVG, LOGO_SVG_SMALL, ICON

st.set_page_config(page_title="NaijaReview AI", page_icon="🇳🇬", layout="wide", initial_sidebar_state="expanded")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
API = "http://localhost:8000"

# ── Session defaults ──
for key, val in {
    "mode": "home", "msgs": [], "sid": str(uuid.uuid4()),
    "result": None, "search_open": False, "more_open": False,
    "history": [
        {"title": "Samsung Galaxy Buds review", "mode": "review"},
        {"title": "Restaurant recommendations Lagos", "mode": "recommend"},
        {"title": "Book ratings analysis", "mode": "chat"},
    ],
    "preferences": {
        "nigerian_mode": True,
        "region": "Lagos",
        "default_category": "Electronics",
        "top_k": 8,
    }
}.items():
    if key not in st.session_state:
        st.session_state[key] = val


def api_health():
    try:
        return requests.get(f"{API}/health", timeout=3).json()
    except Exception:
        return None


# ══════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════
with st.sidebar:
    # ── Logo at very top ──
    st.markdown(f'''
    <div style="display:flex;align-items:center;gap:9px;padding:14px 12px 12px;">
        {LOGO_SVG}
        <span style="font-size:0.95rem;font-weight:700;color:#111827;">NaijaReview AI</span>
    </div>
    ''', unsafe_allow_html=True)

    # ── New Chat ──
    if st.button("➕  New chat", key="new_chat", type="primary", use_container_width=True):
        st.session_state.mode = "home"
        st.session_state.result = None
        st.session_state.msgs = []
        st.session_state.sid = str(uuid.uuid4())
        st.rerun()

    # ── Search ──
    if st.button(f"🔍  Search chats", key="search_btn", use_container_width=True):
        st.session_state.search_open = not st.session_state.search_open

    if st.session_state.search_open:
        sq = st.text_input("Search", placeholder="Search your history...", label_visibility="collapsed", key="search_q")
        if sq:
            matches = [h for h in st.session_state.history if sq.lower() in h["title"].lower()]
            for m in matches:
                st.caption(f"📄 {m['title']}")

    # ── More ──
    if st.button("•••  More", key="more_btn", use_container_width=True):
        st.session_state.more_open = not st.session_state.more_open

    if st.session_state.more_open:
        st.markdown('<div style="padding:4px 12px;">', unsafe_allow_html=True)
        if st.button("🗑️  Clear all chats", key="clear_all", use_container_width=True):
            st.session_state.history = []
            st.session_state.msgs = []
            st.session_state.more_open = False
            st.rerun()
        if st.button("📊  System info", key="sys_info_btn", use_container_width=True):
            st.session_state.mode = "system_info"
            st.session_state.more_open = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── MODES ──
    st.markdown('<div class="nav-section">Modes</div>', unsafe_allow_html=True)

    if st.button("✏️  Generate Review", key="nav_review", use_container_width=True):
        st.session_state.mode = "review"
        st.session_state.result = None
        st.rerun()
    if st.button("⭐  Get Recommendations", key="nav_recommend", use_container_width=True):
        st.session_state.mode = "recommend"
        st.session_state.result = None
        st.rerun()
    if st.button("💬  Chat with AI", key="nav_chat", use_container_width=True):
        st.session_state.mode = "chat"
        st.rerun()

    # ── SETTINGS ──
    st.markdown('<div class="nav-section">Settings</div>', unsafe_allow_html=True)

    if st.button("⚙️  Preferences", key="nav_prefs", use_container_width=True):
        st.session_state.mode = "preferences"
        st.rerun()
    if st.button("🕐  History", key="nav_history", use_container_width=True):
        st.session_state.mode = "history_view"
        st.rerun()

    # ── RECENTS ──
    st.markdown('<div class="nav-section">Recents</div>', unsafe_allow_html=True)
    for i, h in enumerate(st.session_state.history[:5]):
        if st.button(f"💬 {h['title'][:28]}{'...' if len(h['title'])>28 else ''}", key=f"recent_{i}", use_container_width=True):
            st.session_state.mode = h["mode"]
            st.session_state.result = None
            st.rerun()

    # ── Bottom spacer ──
    st.markdown('<div class="sidebar-bottom-spacer"></div>', unsafe_allow_html=True)

    # ── Fixed user card at bottom ──
    st.markdown('''
    <div class="user-card-fixed">
        <div class="user-avatar">RM</div>
        <div>
            <div class="user-name">Raji Mubarak</div>
            <div class="user-plan">Team Cerebral</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


# ══════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════
h = api_health()

# Top bar
st.markdown(f'''
<div class="top-bar">
    <div class="top-bar-left">
        {LOGO_SVG_SMALL}
        <span>NaijaReview AI</span>
        <span style="font-size:0.7rem;color:#9ca3af;font-weight:400;">▾</span>
    </div>
    <div style="display:flex;align-items:center;gap:12px;">
        <span style="font-size:0.78rem;color:{'#22c55e' if h else '#ef4444'};font-weight:500;">
            <span class="status-dot" style="background:{'#22c55e' if h else '#ef4444'};"></span>
            {'Online' if h else 'Offline'}
        </span>
    </div>
</div>
''', unsafe_allow_html=True)


# ════════════════════════════════════════
# HOME — ChatGPT welcome
# ════════════════════════════════════════
if st.session_state.mode == "home":
    # Vertical spacer to push greeting to center
    st.markdown('<div style="height:28vh;"></div>', unsafe_allow_html=True)

    # Greeting
    st.markdown('<div style="text-align:center;font-size:1.55rem;font-weight:500;color:#111827;margin-bottom:2rem;">Good to see you, Dev Mubarak. 👋</div>', unsafe_allow_html=True)

    # Centered input + chips
    _p1, col_center, _p2 = st.columns([1.2, 2.5, 1.2])
    with col_center:
        query = st.text_input("Ask anything", placeholder="Ask anything about reviews, recommendations...",
                              label_visibility="collapsed", key="home_input")

        # Mode chips
        st.markdown('<div class="chip-row">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("✏️  Generate Review", key="chip_review"):
                st.session_state.mode = "review"
                st.rerun()
        with c2:
            if st.button("⭐  Get Recommendations", key="chip_rec"):
                st.session_state.mode = "recommend"
                st.rerun()
        with c3:
            if st.button("💬  Chat with AI", key="chip_chat"):
                st.session_state.mode = "chat"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        if query:
            st.session_state.mode = "chat"
            st.session_state.msgs.append({"role": "user", "content": query})
            st.rerun()


# ════════════════════════════════════════
# GENERATE REVIEW (Task A)
# ════════════════════════════════════════
elif st.session_state.mode == "review":
    _p1, col_main, _p2 = st.columns([1, 3, 1])
    with col_main:
        st.markdown(f'<div class="section-header">{ICON["pencil"]}<span style="font-size:1.1rem;font-weight:600;">Generate Review & Rating</span></div>', unsafe_allow_html=True)

        prefs = st.session_state.preferences
        uid = st.text_input("User ID", "demo_user_001", key="a_uid")
        c1, c2 = st.columns(2)
        with c1:
            item = st.text_input("Product / Item", "Samsung Galaxy Buds3 Pro")
            cat = st.selectbox("Category", ["Electronics", "Restaurants", "Books", "Fashion", "Movies"],
                               index=["Electronics", "Restaurants", "Books", "Fashion", "Movies"].index(prefs["default_category"]))
        with c2:
            desc = st.text_area("Description", "Premium wireless earbuds with ANC and 360 Audio.", height=100)
            is_ng = st.toggle("🇳🇬 Nigerian Mode", prefs["nigerian_mode"], key="a_ng")

        if st.button("Generate Review →", type="primary", use_container_width=True, key="gen_btn"):
            sample_reviews = [
                {"rating": 5, "review_text": "Amazing! Best purchase this year.", "item_name": "Wireless Headphones", "category": "Electronics"},
                {"rating": 4, "review_text": "Pretty good value for money.", "item_name": "Phone Case", "category": "Electronics"},
                {"rating": 2, "review_text": "Disappointed. Returning it.", "item_name": "USB Cable", "category": "Electronics"},
                {"rating": 5, "review_text": "Best jollof in Lagos no cap!", "item_name": "Mama Put", "category": "Restaurants"},
                {"rating": 3, "review_text": "Okay book. Lost me mid-way.", "item_name": "Half of a Yellow Sun", "category": "Books"},
            ]
            with st.spinner("Agent reasoning..."):
                try:
                    r = requests.post(f"{API}/task-a/generate", json={
                        "user_id": uid, "item_name": item, "item_category": cat,
                        "item_description": desc, "user_reviews": sample_reviews,
                        "is_nigerian": is_ng, "region": prefs["region"],
                    }, timeout=120)
                    if r.ok:
                        st.session_state.result = r.json()
                        st.session_state.history.insert(0, {"title": f"{item} review", "mode": "review"})
                    else:
                        st.error(f"Error: {r.text[:200]}")
                except Exception as e:
                    st.error(str(e)[:200])

        if st.session_state.result and st.session_state.mode == "review":
            d = st.session_state.result
            st.markdown(f'''
            <div class="metric-row">
                <div class="metric-box"><div class="metric-val">{d.get("rating", 0):.1f}★</div><div class="metric-lbl">Rating</div></div>
                <div class="metric-box"><div class="metric-val">{d.get("confidence", 0):.0%}</div><div class="metric-lbl">Confidence</div></div>
                <div class="metric-box"><div class="metric-val">{len(d.get("review_text", "").split())}</div><div class="metric-lbl">Words</div></div>
            </div>
            <div class="review-output">{d.get("review_text", "")}</div>
            ''', unsafe_allow_html=True)
            with st.expander("🧠 Agent Reasoning"):
                st.write(d.get("reasoning", "—"))
            with st.expander("👤 Persona"):
                st.json(d.get("persona", {}))


# ════════════════════════════════════════
# RECOMMENDATIONS (Task B)
# ════════════════════════════════════════
elif st.session_state.mode == "recommend":
    _p1, col_main, _p2 = st.columns([1, 3, 1])
    with col_main:
        st.markdown(f'<div class="section-header">{ICON["target"]}<span style="font-size:1.1rem;font-weight:600;">Get Recommendations</span></div>', unsafe_allow_html=True)

        prefs = st.session_state.preferences
        uid = st.text_input("User ID", "demo_user_001", key="b_uid")
        q = st.text_input("What are you looking for?", placeholder="e.g. Good earbuds for Lagos traffic", key="b_query")
        c1, c2 = st.columns(2)
        with c1:
            k = st.slider("Results", 3, 15, prefs["top_k"])
        with c2:
            cat_filter = st.selectbox("Category", [None, "Electronics", "Restaurants", "Books"], key="b_cat")

        if st.button("Get Recommendations →", type="primary", use_container_width=True, key="rec_btn"):
            with st.spinner("Searching & ranking..."):
                try:
                    r = requests.post(f"{API}/task-b/recommend", json={
                        "user_id": uid, "query": q, "top_k": k,
                        "is_nigerian": prefs["nigerian_mode"],
                        "category_filter": cat_filter,
                        "user_reviews": [
                            {"rating": 5, "review_text": "Love this!", "item_name": "JBL Speaker", "category": "Electronics"},
                            {"rating": 4, "review_text": "Great read", "item_name": "Things Fall Apart", "category": "Books"},
                        ]
                    }, timeout=120)
                    if r.ok:
                        st.session_state.result = r.json()
                        st.session_state.history.insert(0, {"title": f"Recs: {q[:25]}" if q else "Recommendations", "mode": "recommend"})
                    else:
                        st.error(r.text[:200])
                except Exception as e:
                    st.error(str(e)[:200])

        if st.session_state.result and st.session_state.mode == "recommend":
            data = st.session_state.result
            st.caption(f"✨ {data.get('total_candidates_considered', 0)} candidates evaluated")
            for rec in data.get("recommendations", []):
                st.markdown(f'''<div class="rec-item">
                    <div class="rec-rank">{rec.get("rank", "")}</div>
                    <div style="flex:1;">
                        <div class="rec-name">{rec.get("item_name", "")}</div>
                        <span class="rec-cat">{rec.get("category", "—")}</span>
                        <div class="rec-why">{rec.get("explanation", "")[:200]}</div>
                    </div>
                </div>''', unsafe_allow_html=True)


# ════════════════════════════════════════
# CHAT
# ════════════════════════════════════════
elif st.session_state.mode == "chat":
    for m in st.session_state.msgs:
        with st.chat_message(m["role"]):
            st.write(m["content"])

    if prompt := st.chat_input("Ask for recommendations, reviews, or anything..."):
        st.session_state.msgs.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    r = requests.post(f"{API}/task-b/chat", json={
                        "user_id": "demo_user_001",
                        "message": prompt,
                        "session_id": st.session_state.sid,
                        "is_nigerian": st.session_state.preferences["nigerian_mode"],
                    }, timeout=60)
                    if r.ok:
                        resp = r.json().get("response", "")
                        st.write(resp)
                        st.session_state.msgs.append({"role": "assistant", "content": resp})
                        st.session_state.history.insert(0, {"title": prompt[:30], "mode": "chat"})
                    else:
                        st.error(r.text[:200])
                except Exception as e:
                    st.error(str(e)[:200])


# ════════════════════════════════════════
# PREFERENCES
# ════════════════════════════════════════
elif st.session_state.mode == "preferences":
    _p1, col_main, _p2 = st.columns([1, 3, 1])
    with col_main:
        st.markdown(f'<div class="section-header">{ICON["settings"]}<span style="font-size:1.1rem;font-weight:600;">Preferences</span></div>', unsafe_allow_html=True)

        prefs = st.session_state.preferences
        ng = st.toggle("🇳🇬 Nigerian Mode", prefs["nigerian_mode"], key="pref_ng")
        region = st.selectbox("Default Region", ["Lagos", "Abuja", "Port Harcourt", "Kano", "Ibadan", "Enugu"],
                              index=["Lagos", "Abuja", "Port Harcourt", "Kano", "Ibadan", "Enugu"].index(prefs["region"]),
                              key="pref_region")
        cat = st.selectbox("Default Category", ["Electronics", "Restaurants", "Books", "Fashion", "Movies"],
                           index=["Electronics", "Restaurants", "Books", "Fashion", "Movies"].index(prefs["default_category"]),
                           key="pref_cat")
        topk = st.slider("Default number of recommendations", 3, 20, prefs["top_k"], key="pref_k")

        if st.button("Save Preferences", type="primary", use_container_width=True, key="save_prefs"):
            st.session_state.preferences = {
                "nigerian_mode": ng,
                "region": region,
                "default_category": cat,
                "top_k": topk,
            }
            st.success("✅ Preferences saved!")

        st.markdown("---")
        st.markdown("#### Training")
        tc1, tc2, tc3 = st.columns(3)
        amz = tc1.number_input("Amazon", 20000, step=5000)
        ylp = tc2.number_input("Yelp", 15000, step=5000)
        gdr = tc3.number_input("Goodreads", 10000, step=5000)
        if st.button("Train All Models", type="primary", use_container_width=True, key="train_btn"):
            with st.spinner("Training..."):
                try:
                    r = requests.post(f"{API}/train", json={"amazon_max": amz, "yelp_max": ylp, "goodreads_max": gdr}, timeout=600)
                    if r.ok:
                        d = r.json()
                        st.success(f"✅ {d['total_reviews']:,} reviews · {d['total_users']:,} users · {d['total_items']:,} items")
                    else:
                        st.error(r.text[:200])
                except Exception as e:
                    st.error(str(e)[:200])


# ════════════════════════════════════════
# HISTORY
# ════════════════════════════════════════
elif st.session_state.mode == "history_view":
    _p1, col_main, _p2 = st.columns([1, 3, 1])
    with col_main:
        st.markdown(f'<div class="section-header">{ICON["history"]}<span style="font-size:1.1rem;font-weight:600;">Chat History</span></div>', unsafe_allow_html=True)

        if not st.session_state.history:
            st.info("No history yet. Start chatting or generating reviews!")
        else:
            for i, h in enumerate(st.session_state.history):
                icon = {"review": "✏️", "recommend": "⭐", "chat": "💬"}.get(h["mode"], "📄")
                c1, c2 = st.columns([5, 1])
                with c1:
                    if st.button(f"{icon}  {h['title']}", key=f"hist_{i}", use_container_width=True):
                        st.session_state.mode = h["mode"]
                        st.session_state.result = None
                        st.rerun()
                with c2:
                    if st.button("🗑️", key=f"del_{i}"):
                        st.session_state.history.pop(i)
                        st.rerun()


# ════════════════════════════════════════
# SYSTEM INFO
# ════════════════════════════════════════
elif st.session_state.mode == "system_info":
    _p1, col_main, _p2 = st.columns([1, 3, 1])
    with col_main:
        st.markdown(f'<div class="section-header">{ICON["more"]}<span style="font-size:1.1rem;font-weight:600;">System Information</span></div>', unsafe_allow_html=True)
        if h:
            st.json(h)
        else:
            st.warning("API is offline. Start the FastAPI server first.")
