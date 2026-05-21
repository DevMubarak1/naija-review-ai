"""Streamlit dashboard with direct pipeline support and FastAPI fallback."""
import json, os, sys, uuid, traceback, streamlit as st

# Ensure project root is on sys.path for imports
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from app.styles import CSS, LOGO, LOGO_SM, AV_USER, AV_AI, STOP_IC, IC, nav_html, SUGGESTIONS, SPARKLE_SVG, HOMEPAGE_CSS

st.set_page_config(page_title="NaijaReview AI", layout="wide",
                   initial_sidebar_state="expanded")
st.markdown(CSS, unsafe_allow_html=True)

HIST_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "chat_history.json")

# Check if local pipeline files exist on disk to determine if direct mode is supported.
# We avoid importing them here at the module level because importing heavy ML modules
# (e.g. PyTorch, sentence-transformers, XGBoost) takes 15+ seconds, causing Streamlit connection timeouts.
_DIRECT_MODE = (
    os.path.exists(os.path.join(_ROOT, "app", "agents", "user_modeling", "pipeline.py")) and
    os.path.exists(os.path.join(_ROOT, "app", "agents", "recommendation", "pipeline.py"))
)

def load_user_modeling_pipeline():
    from app.agents.user_modeling.pipeline import user_modeling_pipeline
    return user_modeling_pipeline

def load_recommendation_pipeline():
    from app.agents.recommendation.pipeline import recommendation_pipeline
    return recommendation_pipeline

# Also try FastAPI if available
API = os.getenv("API_URL", "http://localhost:8000")

# ── Persist helpers ──
def _load_history():
    try:
        if os.path.exists(HIST_FILE):
            with open(HIST_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return []

def _save_history():
    try:
        os.makedirs(os.path.dirname(HIST_FILE), exist_ok=True)
        with open(HIST_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.history, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

# ── Session defaults ──
if "mode" not in st.session_state:
    st.session_state.mode = "home"
if "msgs" not in st.session_state:
    st.session_state.msgs = []
if "sid" not in st.session_state:
    st.session_state.sid = str(uuid.uuid4())
if "result" not in st.session_state:
    st.session_state.result = None
if "history" not in st.session_state:
    st.session_state.history = _load_history() or []
if "prefs" not in st.session_state:
    st.session_state.prefs = {"nigerian_mode": True, "region": "Lagos",
                               "default_category": "Electronics", "top_k": 8}
if "sending" not in st.session_state:
    st.session_state.sending = False
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None


# ══════════════════════════════════════════
# SMART API — tries direct first, then FastAPI
# ══════════════════════════════════════════
@st.cache_data(show_spinner=False, ttl=10)
def check_api_health(api_url):
    try:
        import requests
        r = requests.get(f"{api_url}/health", timeout=1.0)
        return r.ok
    except Exception:
        return False

def api_ok():
    """Check if backend is available (direct or API)."""
    if _DIRECT_MODE:
        return True
    return check_api_health(API)


def smart_chat(msg, sid):
    """Multi-turn conversational recommendation."""
    # Try direct pipeline first
    if _DIRECT_MODE:
        try:
            pipeline = load_recommendation_pipeline()
            result = pipeline.conversational_recommend(
                user_id="demo_user_001",
                message=msg,
                session_id=sid,
                is_nigerian=st.session_state.prefs["nigerian_mode"],
            )
            return result.get("response", "I couldn't process that.")
        except Exception as e:
            # Log and fallback to API
            print(f"Direct mode chat failed: {e}", file=sys.stderr)

    # Fallback to FastAPI
    try:
        import requests
        r = requests.post(f"{API}/task-b/chat", json={
            "user_id": "demo_user_001", "message": msg,
            "session_id": sid,
            "is_nigerian": st.session_state.prefs["nigerian_mode"],
        }, timeout=90)
        if r.ok:
            return r.json().get("response", "I couldn't process that.")
        return f"API Error ({r.status_code})"
    except Exception as e:
        return f"Cannot reach backend. {str(e)[:150]}"


def smart_generate_review(uid, item, cat, desc, is_ng, region, reviews):
    """Task A: Generate review."""
    if _DIRECT_MODE:
        try:
            pipeline = load_user_modeling_pipeline()
            result = pipeline.run(
                user_id=uid, item_name=item, item_category=cat,
                item_description=desc, reviews=reviews,
                is_nigerian=is_ng, region=region,
            )
            return result
        except Exception as e:
            # Log and fallback to API
            print(f"Direct mode generate review failed: {e}", file=sys.stderr)

    try:
        import requests
        r = requests.post(f"{API}/task-a/generate", json={
            "user_id": uid, "item_name": item, "item_category": cat,
            "item_description": desc, "user_reviews": reviews,
            "is_nigerian": is_ng, "region": region,
        }, timeout=120)
        if r.ok:
            return r.json()
        return {"error": r.text[:200]}
    except Exception as e:
        return {"error": str(e)[:200]}


def smart_recommend(uid, query, top_k, is_ng, cat_filter, reviews):
    """Task B: Get recommendations."""
    if _DIRECT_MODE:
        try:
            pipeline = load_recommendation_pipeline()
            result = pipeline.recommend(
                user_id=uid, query=query, user_reviews=reviews,
                top_k=top_k, is_nigerian=is_ng, category_filter=cat_filter,
            )
            return result
        except Exception as e:
            # Log and fallback to API
            print(f"Direct mode recommendation failed: {e}", file=sys.stderr)

    try:
        import requests
        r = requests.post(f"{API}/task-b/recommend", json={
            "user_id": uid, "query": query, "top_k": top_k,
            "is_nigerian": is_ng, "category_filter": cat_filter,
            "user_reviews": reviews,
        }, timeout=120)
        if r.ok:
            return r.json()
        return {"error": r.text[:200]}
    except Exception as e:
        return {"error": str(e)[:200]}


def nav_btn(icon_key, label, key, mode_check=None):
    """HTML label + invisible overlay button."""
    active = (mode_check is not None and st.session_state.mode == mode_check)
    st.markdown(nav_html(icon_key, label, active=active), unsafe_allow_html=True)
    return st.button(label, key=key, use_container_width=True)


# ══════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════
online = api_ok()
_mode_label = "Direct" if _DIRECT_MODE else ("API" if online else "Offline")
_mode_color = "#22c55e" if (_DIRECT_MODE or online) else "#ef4444"

with st.sidebar:
    # Logo
    st.markdown(f'''<div class="sidebar-logo">
        {LOGO}<span>NaijaReview AI</span>
        <span class="status-dot" style="background:{_mode_color};"></span>
    </div>''', unsafe_allow_html=True)

    # New Chat
    if st.button("New chat", key="new_chat", type="primary", use_container_width=True, icon=":material/add:"):
        st.session_state.mode = "home"
        st.session_state.result = None
        st.session_state.msgs = []
        st.session_state.sid = str(uuid.uuid4())
        st.rerun()

    # ── Modes ──
    st.markdown('<div class="nav-sec">Modes</div>', unsafe_allow_html=True)
    if nav_btn("edit", "Generate Review", "nav_rev", "review"):
        st.session_state.mode = "review"; st.session_state.result = None; st.rerun()
    if nav_btn("star", "Get Recommendations", "nav_rec", "recommend"):
        st.session_state.mode = "recommend"; st.session_state.result = None; st.rerun()
    if nav_btn("chat", "Chat with AI", "nav_chat", "chat"):
        st.session_state.mode = "chat"; st.rerun()

    # ── Settings ──
    st.markdown('<div class="nav-sec">Settings</div>', unsafe_allow_html=True)
    if nav_btn("gear", "Preferences", "nav_pref", "preferences"):
        st.session_state.mode = "preferences"; st.rerun()

    # ── Recents ──
    if st.session_state.history:
        st.markdown('<div class="nav-sec">Recents</div>', unsafe_allow_html=True)
        for i, h in enumerate(st.session_state.history[:8]):
            col_title, col_del = st.columns([0.85, 0.15])
            with col_title:
                icon = "edit" if h.get("mode") == "review" else ("star" if h.get("mode") == "recommend" else "chat")
                st.markdown(nav_html(icon, h["title"][:30]), unsafe_allow_html=True)
                if st.button(h["title"][:30], key=f"rc_{i}", use_container_width=True):
                    st.session_state.mode = h.get("mode", "chat")
                    st.session_state.msgs = h.get("msgs", [])
                    st.session_state.result = None
                    st.rerun()
            with col_del:
                st.markdown(f'<div class="del-btn">{IC["x"]}</div>',
                            unsafe_allow_html=True)
                if st.button("x", key=f"del_{i}", use_container_width=True):
                    st.session_state.history.pop(i)
                    _save_history()
                    st.rerun()

    # Bottom spacer + user card
    st.markdown('<div style="height:80px;"></div>', unsafe_allow_html=True)
    st.markdown(f'''<div class="user-card">
        <div class="user-av">TC</div>
        <div>
            <div class="user-nm">Team Cerebral</div>
            <div class="user-pl">DSN × BCT Hackathon 3.0</div>
        </div>
    </div>''', unsafe_allow_html=True)


# ══════════════════════════════════════════
# MAIN CONTENT AREA
# ══════════════════════════════════════════

# ════════ HOME — Hero Landing ════════
if st.session_state.mode == "home":
    # Inject home-page specific CSS scoping rules to turn suggestion buttons into premium cards
    st.markdown(HOMEPAGE_CSS, unsafe_allow_html=True)

    # Vertical spacing to center content
    st.markdown('<div class="hero-spacer"></div>', unsafe_allow_html=True)

    # Greeting + branding
    st.markdown(f'''<div class="hero-section">
        <div class="hero-icon">{SPARKLE_SVG}</div>
        <h1 class="hero-title">NaijaReview AI</h1>
        <p class="hero-sub">
            Your AI-powered review generator &amp; recommendation engine.<br>
            Generate reviews, get personalized recommendations, or chat about products.
        </p>
    </div>''', unsafe_allow_html=True)

    # Centered input area
    _p1, cc, _p2 = st.columns([1.2, 2.5, 1.2])
    with cc:
        st.markdown('<div class="search-bar-anchor"></div>', unsafe_allow_html=True)
        in_col, btn_col = st.columns([0.88, 0.12])
        with in_col:
            query = st.text_input("Ask", placeholder="Ask anything about reviews, recommendations...",
                                   label_visibility="collapsed", key="home_q", disabled=st.session_state.sending)
        with btn_col:
            btn_icon = ":material/square:" if st.session_state.sending else ":material/send:"
            send_clicked = st.button("", icon=btn_icon, key="home_send_btn", disabled=st.session_state.sending, use_container_width=True)

        # Trigger submission on enter or click
        if (query and query.strip() and not st.session_state.sending) or (send_clicked and st.session_state.home_q and st.session_state.home_q.strip()):
            q_text = st.session_state.home_q.strip()
            st.session_state.sending = True
            st.session_state.pending_query = q_text
            st.rerun()

        # Suggestion cards (2x2 grid)
        st.markdown('<div class="suggestion-anchor"></div>', unsafe_allow_html=True)
        r1_c1, r1_c2 = st.columns(2)
        r2_c1, r2_c2 = st.columns(2)
        grid_cols = [r1_c1, r1_c2, r2_c1, r2_c2]
        for idx, sug in enumerate(SUGGESTIONS):
            with grid_cols[idx]:
                if st.button(sug["label"], key=f"sug_{idx}", use_container_width=True, icon=sug["icon"], disabled=st.session_state.sending):
                    if sug["mode"] == "chat":
                        st.session_state.mode = "chat"
                        if "Pidgin" in sug["label"]:
                            st.session_state.msgs.append({"role": "user", "content": "Switch to Nigerian Pidgin mode and recommend products for me"})
                            resp = smart_chat("Switch to Nigerian Pidgin mode and recommend products for me", st.session_state.sid)
                            st.session_state.msgs.append({"role": "assistant", "content": resp})
                            st.session_state.history.insert(0, {"title": "Pidgin mode chat", "mode": "chat", "msgs": list(st.session_state.msgs)})
                            _save_history()
                    else:
                        st.session_state.mode = sug["mode"]
                        st.session_state.result = None
                    st.rerun()

        # Footer
        st.markdown(f'''<div class="powered-by">
            Powered by <a href="#">Groq Llama 3.3</a> · <a href="#">OpenAI GPT-4o-mini</a> · Team Cerebral
            <br><span style="color:{_mode_color}">● {_mode_label}</span>
        </div>''', unsafe_allow_html=True)

        if st.session_state.sending and st.session_state.pending_query:
            q_text = st.session_state.pending_query
            resp = smart_chat(q_text, st.session_state.sid)
            st.session_state.msgs.append({"role": "user", "content": q_text})
            st.session_state.msgs.append({"role": "assistant", "content": resp})
            st.session_state.history.insert(0, {
                "title": q_text[:30], "mode": "chat",
                "msgs": list(st.session_state.msgs)
            })
            _save_history()
            
            # Reset sending state and transition to chat page
            st.session_state.sending = False
            st.session_state.pending_query = None
            st.session_state.mode = "chat"
            st.rerun()


# ════════ REVIEW ════════
elif st.session_state.mode == "review":
    # Top bar
    st.markdown(f'''<div class="top-bar">
        <div class="top-bar-l">{LOGO_SM}<span>NaijaReview AI</span></div>
        <div class="mode-indicator">
            <span class="dot" style="background:{_mode_color};"></span>
            <span style="color:{_mode_color};">{_mode_label}</span>
        </div>
    </div>''', unsafe_allow_html=True)

    # Mode badge
    st.markdown(f'<div class="mode-pill">{IC["edit"]} Generate Review</div>', unsafe_allow_html=True)

    # Centered form
    _p1, cm, _p2 = st.columns([1, 3, 1])
    with cm:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        p = st.session_state.prefs

        # User ID
        uid = st.text_input("User ID", "demo_user_001", key="a_uid")

        # Two-column form
        c1, c2 = st.columns(2)
        with c1:
            item = st.text_input("Product Name", "Samsung Galaxy Buds3 Pro")
            cat = st.selectbox("Category", ["Electronics", "Restaurants", "Books", "Fashion", "Movies"],
                               index=["Electronics", "Restaurants", "Books", "Fashion", "Movies"].index(p["default_category"]))
        with c2:
            desc = st.text_area("Product Description", "Premium wireless earbuds with ANC and 360 Audio.", height=100)
            is_ng = st.toggle("Nigerian Mode", p["nigerian_mode"], key="a_ng")

        # Generate button
        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
        if st.button("Generate Review", type="primary", use_container_width=True, key="gen", icon=":material/arrow_forward:"):
            reviews = [
                {"rating": 5, "review_text": "Amazing!", "item_name": "Headphones", "category": "Electronics"},
                {"rating": 4, "review_text": "Good value.", "item_name": "Phone Case", "category": "Electronics"},
                {"rating": 2, "review_text": "Disappointed.", "item_name": "USB Cable", "category": "Electronics"},
            ]
            with st.spinner("Agent reasoning..."):
                result = smart_generate_review(uid, item, cat, desc, is_ng, p["region"], reviews)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.session_state.result = result
                    st.session_state.history.insert(0, {"title": f"{item} review", "mode": "review", "msgs": []})
                    _save_history()

        # Results
        if st.session_state.result and st.session_state.mode == "review":
            d = st.session_state.result
            st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)

            # Metrics row
            st.markdown(f'''<div class="metric-row">
                <div class="metric-card">
                    <div class="metric-val">{d.get('rating',0):.1f} <svg width="18" height="18" viewBox="0 0 24 24" fill="#1a7a4c" style="display:inline-block;vertical-align:middle;margin-top:-4px;margin-left:2px;"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg></div>
                    <div class="metric-lbl">Predicted Rating</div>
                </div>
                <div class="metric-card">
                    <div class="metric-val">{d.get("confidence",0):.0%}</div>
                    <div class="metric-lbl">Confidence</div>
                </div>
                <div class="metric-card">
                    <div class="metric-val">{len(d.get("review_text","").split())}</div>
                    <div class="metric-lbl">Word Count</div>
                </div>
            </div>''', unsafe_allow_html=True)

            # Generated review
            st.markdown(f'''<div class="review-box">
                <div class="review-quote">❝</div>
                {d.get("review_text","")}
            </div>''', unsafe_allow_html=True)

            with st.expander("Agent Reasoning", icon=":material/psychology:"):
                st.write(d.get("reasoning", ""))

        st.markdown('</div>', unsafe_allow_html=True)


# ════════ RECOMMEND ════════
elif st.session_state.mode == "recommend":
    # Top bar
    st.markdown(f'''<div class="top-bar">
        <div class="top-bar-l">{LOGO_SM}<span>NaijaReview AI</span></div>
        <div class="mode-indicator">
            <span class="dot" style="background:{_mode_color};"></span>
            <span style="color:{_mode_color};">{_mode_label}</span>
        </div>
    </div>''', unsafe_allow_html=True)

    # Mode badge
    st.markdown(f'<div class="mode-pill">{IC["star"]} Get Recommendations</div>', unsafe_allow_html=True)

    # Centered form
    _p1, cm, _p2 = st.columns([1, 3, 1])
    with cm:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        p = st.session_state.prefs

        uid = st.text_input("User ID", "demo_user_001", key="b_uid")
        q = st.text_input("What are you looking for?", placeholder="e.g. Good earbuds for Lagos traffic", key="b_q")

        c1, c2 = st.columns(2)
        with c1:
            k = st.slider("Number of results", 3, 15, p["top_k"])
        with c2:
            cat_f = st.selectbox("Category filter", [None, "Electronics", "Restaurants", "Books"], key="b_cat")

        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
        if st.button("Get Recommendations", type="primary", use_container_width=True, key="rec", icon=":material/arrow_forward:"):
            reviews = [{"rating": 5, "review_text": "Love this!", "item_name": "JBL Speaker", "category": "Electronics"}]
            with st.spinner("Searching & ranking..."):
                result = smart_recommend(uid, q, k, p["nigerian_mode"], cat_f, reviews)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.session_state.result = result
                    st.session_state.history.insert(0, {"title": f"Recs: {q[:25]}" if q else "Recommendations", "mode": "recommend", "msgs": []})
                    _save_history()

        # Results
        if st.session_state.result and st.session_state.mode == "recommend":
            data = st.session_state.result
            st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
            st.markdown(f'''<div class="results-header">
                {IC["search"]} <span>{data.get('total_candidates_considered', 0)} candidates evaluated</span>
            </div>''', unsafe_allow_html=True)

            for rec in data.get("recommendations", []):
                score_pct = rec.get("score", 0)
                if isinstance(score_pct, (int, float)) and score_pct <= 1:
                    score_pct = f"{score_pct:.0%}"
                else:
                    score_pct = f"{score_pct}"

                st.markdown(f'''<div class="rec-card">
                    <div class="rec-rank">{rec.get("rank","")}</div>
                    <div class="rec-body">
                        <div class="rec-header">
                            <div class="rec-name">{rec.get("item_name","")}</div>
                            <span class="rec-cat">{rec.get("category","")}</span>
                        </div>
                        <div class="rec-desc">{rec.get("explanation","")[:220]}</div>
                    </div>
                </div>''', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# ════════ CHAT ════════
elif st.session_state.mode == "chat":
    # Top bar
    st.markdown(f'''<div class="top-bar">
        <div class="top-bar-l">{LOGO_SM}<span>NaijaReview AI</span></div>
        <div class="mode-indicator">
            <span class="dot" style="background:{_mode_color};"></span>
            <span style="color:{_mode_color};">{_mode_label}</span>
        </div>
    </div>''', unsafe_allow_html=True)

    # Show empty state if no messages
    if not st.session_state.msgs:
        st.markdown(f'''<div class="chat-empty">
            <div class="chat-empty-icon" style="color:#1a7a4c;">{IC["chat"]}</div>
            <div class="chat-empty-title">Start a conversation</div>
            <div class="chat-empty-sub">Ask about products, get recommendations, or chat in Nigerian Pidgin.</div>
        </div>''', unsafe_allow_html=True)

    # Render existing messages
    for m in st.session_state.msgs:
        av = AV_AI if m["role"] == "assistant" else AV_USER
        role_class = "msg-ai" if m["role"] == "assistant" else "msg-user"
        with st.chat_message(m["role"]):
            st.markdown(f'''<div class="chat-msg {role_class}">
                <div class="chat-avatar">{av}</div>
                <div class="chat-text">{m["content"]}</div>
            </div>''', unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("Ask for recommendations, reviews, or anything..."):
        st.session_state.msgs.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(f'''<div class="chat-msg msg-user">
                <div class="chat-avatar">{AV_USER}</div>
                <div class="chat-text">{prompt}</div>
            </div>''', unsafe_allow_html=True)

        with st.chat_message("assistant"):
            ph = st.empty()
            ph.markdown(f'''<div class="chat-msg msg-ai">
                <div class="chat-avatar">{AV_AI}</div>
                <div class="chat-thinking">
                    <div class="thinking-dots">
                        <span></span><span></span><span></span>
                    </div>
                    Thinking...
                </div>
            </div>''', unsafe_allow_html=True)

            resp = smart_chat(prompt, st.session_state.sid)

            ph.markdown(f'''<div class="chat-msg msg-ai">
                <div class="chat-avatar">{AV_AI}</div>
                <div class="chat-text">{resp}</div>
            </div>''', unsafe_allow_html=True)

            st.session_state.msgs.append({"role": "assistant", "content": resp})
            st.session_state.history.insert(0, {
                "title": prompt[:30], "mode": "chat",
                "msgs": list(st.session_state.msgs)
            })
            _save_history()


# ════════ PREFERENCES ════════
elif st.session_state.mode == "preferences":
    # Top bar
    st.markdown(f'''<div class="top-bar">
        <div class="top-bar-l">{LOGO_SM}<span>NaijaReview AI</span></div>
        <div class="mode-indicator">
            <span class="dot" style="background:{_mode_color};"></span>
            <span style="color:{_mode_color};">{_mode_label}</span>
        </div>
    </div>''', unsafe_allow_html=True)

    _p1, cm, _p2 = st.columns([1, 3, 1])
    with cm:
        st.markdown(f'''<div class="pref-header">
            {IC["gear"]}
            <span>Preferences</span>
        </div>''', unsafe_allow_html=True)

        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        p = st.session_state.prefs

        # Nigerian mode toggle
        st.markdown('<div class="pref-section">Language & Region</div>', unsafe_allow_html=True)
        ng = st.toggle("Nigerian Mode", p["nigerian_mode"], key="pf_ng")
        region = st.selectbox("Default Region", ["Lagos", "Abuja", "Port Harcourt", "Kano", "Ibadan", "Enugu"],
                              index=["Lagos", "Abuja", "Port Harcourt", "Kano", "Ibadan", "Enugu"].index(p["region"]), key="pf_r")

        st.markdown('<div class="pref-section">Defaults</div>', unsafe_allow_html=True)
        cat = st.selectbox("Default Category", ["Electronics", "Restaurants", "Books", "Fashion", "Movies"],
                           index=["Electronics", "Restaurants", "Books", "Fashion", "Movies"].index(p["default_category"]), key="pf_c")
        topk = st.slider("Default number of recommendations", 3, 20, p["top_k"], key="pf_k")

        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
        if st.button("Save Preferences", type="primary", use_container_width=True, key="save_p", icon=":material/check:"):
            st.session_state.prefs = {"nigerian_mode": ng, "region": region,
                                      "default_category": cat, "top_k": topk}
            st.success("Preferences saved successfully.")

        st.markdown('</div>', unsafe_allow_html=True)


# ════════ SYSTEM INFO ════════
elif st.session_state.mode == "system_info":
    st.markdown(f'''<div class="top-bar">
        <div class="top-bar-l">{LOGO_SM}<span>NaijaReview AI</span></div>
        <div class="mode-indicator">
            <span class="dot" style="background:{_mode_color};"></span>
            <span style="color:{_mode_color};">{_mode_label}</span>
        </div>
    </div>''', unsafe_allow_html=True)

    _p1, cm, _p2 = st.columns([1, 3, 1])
    with cm:
        st.markdown(f'<div class="pref-header">{IC["info"]} <span>System Information</span></div>', unsafe_allow_html=True)
        st.info(f"**Mode:** {'Direct Pipeline' if _DIRECT_MODE else 'FastAPI Backend'}")
        if online:
            try:
                import requests
                st.json(requests.get(f"{API}/health", timeout=3).json())
            except Exception:
                st.warning("Could not fetch API info.")
        else:
            st.warning("FastAPI backend is offline. Running in direct mode." if _DIRECT_MODE else "API is offline.")
