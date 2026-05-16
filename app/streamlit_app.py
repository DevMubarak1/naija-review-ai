"""NaijaReview AI — ChatGPT-style Dashboard"""
import uuid, requests, streamlit as st
from app.styles import CUSTOM_CSS, LOGO_SVG, LOGO_SVG_SMALL, ICON

st.set_page_config(page_title="NaijaReview AI", page_icon="🇳🇬", layout="wide", initial_sidebar_state="expanded")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
API = "http://localhost:8000"

# Session defaults
if "mode" not in st.session_state:
    st.session_state.mode = "home"
if "msgs" not in st.session_state:
    st.session_state.msgs = []
if "sid" not in st.session_state:
    st.session_state.sid = str(uuid.uuid4())
if "result" not in st.session_state:
    st.session_state.result = None


def api_health():
    try:
        return requests.get(f"{API}/health", timeout=3).json()
    except Exception:
        return None


# ══════════════════════════════════════════
# SIDEBAR (ChatGPT style)
# ══════════════════════════════════════════
with st.sidebar:
    # Logo + title
    st.markdown(f'''
    <div class="sidebar-header">
        <div class="sidebar-logo">{LOGO_SVG_SMALL} NaijaReview AI</div>
    </div>
    ''', unsafe_allow_html=True)

    # New chat button
    if st.button("➕  New chat", key="new_chat", use_container_width=True):
        st.session_state.mode = "home"
        st.session_state.result = None
        st.session_state.msgs = []
        st.session_state.sid = str(uuid.uuid4())
        st.rerun()

    # Nav items
    st.markdown(f'''
    <div class="nav-btn" onclick="void(0)">{ICON["search"]} Search chats</div>
    <div class="nav-btn" onclick="void(0)">{ICON["dots"]} More</div>
    ''', unsafe_allow_html=True)

    # Modes section
    st.markdown('<div class="nav-section">Modes</div>', unsafe_allow_html=True)

    mode_labels = {
        "review": "✏️ Generate Review",
        "recommend": "🎯 Get Recommendations",
        "chat": "💬 Chat with AI",
    }
    mode = st.radio("Mode", list(mode_labels.keys()),
                     format_func=lambda x: mode_labels[x],
                     label_visibility="collapsed", key="mode_radio")
    # Render custom nav buttons for modes
    for k, v in mode_labels.items():
        icon_key = {"review": "pencil", "recommend": "target", "chat": "chat"}[k]
        active = "nav-btn-active" if st.session_state.mode == k else ""
        st.markdown(f'<div class="nav-btn {active}" id="nav-{k}">{ICON[icon_key]} {v.split(" ", 1)[1] if " " in v else v}</div>',
                    unsafe_allow_html=True)

    # Settings
    st.markdown(f'''
    <div class="nav-section">Settings</div>
    <div class="nav-btn">{ICON["settings"]} Preferences</div>
    <div class="nav-btn">{ICON["history"]} History</div>
    ''', unsafe_allow_html=True)

    # Recents
    st.markdown('<div class="nav-section">Recents</div>', unsafe_allow_html=True)
    recents = [
        "Samsung Galaxy Buds review",
        "Restaurant recommendations Lagos",
        "Book ratings analysis",
    ]
    for r in recents:
        st.markdown(f'<div class="recent-item">{ICON["chat"]} {r}</div>', unsafe_allow_html=True)

    # Footer
    st.markdown('''
    <div class="sidebar-footer">
        <div class="user-avatar">RM</div>
        <div>
            <div class="user-name">Raji Mubarak</div>
            <div class="user-plan">Team Cerebral</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Actual mode selector (hidden radio syncs with buttons)
    selected = st.radio("_mode", ["home", "review", "recommend", "chat"],
                        label_visibility="collapsed", key="_mode_sel")
    if selected != st.session_state.mode:
        st.session_state.mode = selected


# ══════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════
h = api_health()

# Top bar (minimal)
st.markdown(f'''
<div style="display:flex;align-items:center;justify-content:space-between;padding:12px 24px 0;">
    <div style="display:flex;align-items:center;gap:8px;font-size:0.92rem;font-weight:600;color:#111827;">
        {LOGO_SVG_SMALL}
        <span>NaijaReview AI</span>
        <span style="font-size:0.7rem;color:#9ca3af;font-weight:400;">▾</span>
    </div>
    <div style="display:flex;align-items:center;gap:12px;">
        <span style="display:inline-flex;align-items:center;gap:4px;font-size:0.75rem;color:{'#22c55e' if h else '#ef4444'};font-weight:500;">
            <span style="width:6px;height:6px;border-radius:50%;background:{'#22c55e' if h else '#ef4444'};display:inline-block;"></span>
            {'Online' if h else 'Offline'}
        </span>
    </div>
</div>
''', unsafe_allow_html=True)


# ════════════════════════════════════════
# HOME (ChatGPT welcome screen)
# ════════════════════════════════════════
if st.session_state.mode == "home":
    st.markdown('''
    <div class="main-center">
        <div class="greeting">Good to see you, Dev Mubarak. 👋</div>
    </div>
    ''', unsafe_allow_html=True)

    # Input bar
    col_pad1, col_input, col_pad2 = st.columns([1, 3, 1])
    with col_input:
        query = st.text_input("Ask anything", placeholder="Ask anything about reviews, recommendations...",
                              label_visibility="collapsed", key="home_input")

        # Action chips (mode selectors)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("✏️  Generate Review", key="chip_review", use_container_width=True):
                st.session_state.mode = "review"
                st.rerun()
        with c2:
            if st.button("🎯  Get Recommendations", key="chip_rec", use_container_width=True):
                st.session_state.mode = "recommend"
                st.rerun()
        with c3:
            if st.button("💬  Chat with AI", key="chip_chat", use_container_width=True):
                st.session_state.mode = "chat"
                st.rerun()

        # If they typed something in the home input, go to chat
        if query:
            st.session_state.mode = "chat"
            st.session_state.msgs.append({"role": "user", "content": query})
            st.rerun()


# ════════════════════════════════════════
# GENERATE REVIEW (Task A)
# ════════════════════════════════════════
elif st.session_state.mode == "review":
    col_pad1, col_main, col_pad2 = st.columns([1, 3, 1])
    with col_main:
        st.markdown(f'''
        <div style="display:flex;align-items:center;gap:10px;margin:1.5rem 0 1rem;">
            {ICON["pencil"]}
            <span style="font-size:1.1rem;font-weight:600;color:#111827;">Generate Review (Task A)</span>
        </div>
        ''', unsafe_allow_html=True)

        uid = st.text_input("User ID", "demo_user_001", key="a_uid")
        c1, c2 = st.columns(2)
        with c1:
            item = st.text_input("Product / Item", "Samsung Galaxy Buds3 Pro")
            cat = st.selectbox("Category", ["Electronics", "Restaurants", "Books", "Fashion", "Movies"])
        with c2:
            desc = st.text_area("Description (optional)", "Premium wireless earbuds with ANC and 360 Audio.", height=100)
            is_ng = st.toggle("🇳🇬 Nigerian Mode", True, key="a_ng")

        if st.button("Generate Review →", type="primary", use_container_width=True, key="gen_btn"):
            sample_reviews = [
                {"rating": 5, "review_text": "Amazing! Best purchase this year.", "item_name": "Wireless Headphones", "category": "Electronics"},
                {"rating": 4, "review_text": "Pretty good. Minor packaging issue.", "item_name": "Phone Case", "category": "Electronics"},
                {"rating": 2, "review_text": "Disappointed. Returning.", "item_name": "USB Cable", "category": "Electronics"},
                {"rating": 5, "review_text": "Best jollof in Lagos no cap!", "item_name": "Mama Put", "category": "Restaurants"},
                {"rating": 3, "review_text": "Okay book. Lost me mid-chapters.", "item_name": "Half of a Yellow Sun", "category": "Books"},
            ]
            with st.spinner("Generating review..."):
                try:
                    r = requests.post(f"{API}/task-a/generate", json={
                        "user_id": uid, "item_name": item, "item_category": cat,
                        "item_description": desc, "user_reviews": sample_reviews,
                        "is_nigerian": is_ng, "region": "Lagos",
                    }, timeout=120)
                    if r.ok:
                        st.session_state.result = r.json()
                    else:
                        st.error(f"Error: {r.text[:200]}")
                except Exception as e:
                    st.error(str(e)[:200])

        # Show result
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
    col_pad1, col_main, col_pad2 = st.columns([1, 3, 1])
    with col_main:
        st.markdown(f'''
        <div style="display:flex;align-items:center;gap:10px;margin:1.5rem 0 1rem;">
            {ICON["target"]}
            <span style="font-size:1.1rem;font-weight:600;color:#111827;">Get Recommendations (Task B)</span>
        </div>
        ''', unsafe_allow_html=True)

        uid = st.text_input("User ID", "demo_user_001", key="b_uid")
        query = st.text_input("What are you looking for?", placeholder="e.g. Good earbuds for Lagos traffic", key="b_query")
        c1, c2 = st.columns(2)
        with c1:
            k = st.slider("Number of results", 3, 15, 8)
        with c2:
            cat_filter = st.selectbox("Category filter", [None, "Electronics", "Restaurants", "Books"], key="b_cat")

        if st.button("Get Recommendations →", type="primary", use_container_width=True, key="rec_btn"):
            with st.spinner("Searching & ranking..."):
                try:
                    r = requests.post(f"{API}/task-b/recommend", json={
                        "user_id": uid, "query": query, "top_k": k,
                        "is_nigerian": True, "category_filter": cat_filter,
                        "user_reviews": [
                            {"rating": 5, "review_text": "Love this!", "item_name": "JBL Speaker", "category": "Electronics"},
                            {"rating": 4, "review_text": "Great read", "item_name": "Things Fall Apart", "category": "Books"},
                        ]
                    }, timeout=120)
                    if r.ok:
                        st.session_state.result = r.json()
                    else:
                        st.error(r.text[:200])
                except Exception as e:
                    st.error(str(e)[:200])

        if st.session_state.result and st.session_state.mode == "recommend":
            data = st.session_state.result
            st.caption(f"{data.get('total_candidates_considered', 0)} candidates evaluated")
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
# CHAT (Conversational)
# ════════════════════════════════════════
elif st.session_state.mode == "chat":
    # Chat history
    for m in st.session_state.msgs:
        with st.chat_message(m["role"]):
            st.write(m["content"])

    # Chat input
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
                        "is_nigerian": True,
                    }, timeout=60)
                    if r.ok:
                        resp = r.json().get("response", "")
                        st.write(resp)
                        st.session_state.msgs.append({"role": "assistant", "content": resp})
                    else:
                        st.error(r.text[:200])
                except Exception as e:
                    st.error(str(e)[:200])
