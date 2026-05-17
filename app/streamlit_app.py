"""Streamlit dashboard with direct pipeline support and FastAPI fallback."""
import json, os, sys, uuid, traceback, streamlit as st

# Ensure project root is on sys.path for imports
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from app.styles import CSS, LOGO, LOGO_SM, AV_USER, AV_AI, STOP_IC, IC, nav_html, SUGGESTIONS

st.set_page_config(page_title="NaijaReview AI", page_icon="🇳🇬", layout="wide",
                   initial_sidebar_state="expanded")
st.markdown(CSS, unsafe_allow_html=True)

HIST_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "chat_history.json")

# ── Try to import local pipeline modules for direct calls ──
_DIRECT_MODE = False
try:
    from app.agents.user_modeling.pipeline import user_modeling_pipeline
    from app.agents.recommendation.pipeline import recommendation_pipeline
    _DIRECT_MODE = True
except Exception:
    pass

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


# ══════════════════════════════════════════
# SMART API — tries direct first, then FastAPI
# ══════════════════════════════════════════
def api_ok():
    """Check if backend is available (direct or API)."""
    if _DIRECT_MODE:
        return True
    try:
        import requests
        return requests.get(f"{API}/health", timeout=3).ok
    except Exception:
        return False


def smart_chat(msg, sid):
    """Multi-turn conversational recommendation."""
    # Try direct pipeline first
    if _DIRECT_MODE:
        try:
            result = recommendation_pipeline.conversational_recommend(
                user_id="demo_user_001",
                message=msg,
                session_id=sid,
                is_nigerian=st.session_state.prefs["nigerian_mode"],
            )
            return result.get("response", "I couldn't process that.")
        except Exception as e:
            return f"Error: {str(e)[:200]}"

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
            result = user_modeling_pipeline.run(
                user_id=uid, item_name=item, item_category=cat,
                item_description=desc, reviews=reviews,
                is_nigerian=is_ng, region=region,
            )
            return result
        except Exception as e:
            return {"error": str(e)[:300]}

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
            result = recommendation_pipeline.recommend(
                user_id=uid, query=query, user_reviews=reviews,
                top_k=top_k, is_nigerian=is_ng, category_filter=cat_filter,
            )
            return result
        except Exception as e:
            return {"error": str(e)[:300]}

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
with st.sidebar:
    # Logo
    st.markdown(f'''<div class="sidebar-logo">
        {LOGO}<span>NaijaReview AI</span>
    </div>''', unsafe_allow_html=True)

    # New Chat
    if st.button("✦  New chat", key="new_chat", type="primary", use_container_width=True):
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
        for i, h in enumerate(st.session_state.history[:6]):
            col_title, col_del = st.columns([0.85, 0.15])
            with col_title:
                st.markdown(nav_html("chat", h["title"][:28]), unsafe_allow_html=True)
                if st.button(h["title"][:28], key=f"rc_{i}", use_container_width=True):
                    st.session_state.mode = h.get("mode", "chat")
                    st.session_state.msgs = h.get("msgs", [])
                    st.session_state.result = None
                    st.rerun()
            with col_del:
                st.markdown(f'<div class="del-btn" style="margin-top:4px;">{IC["x"]}</div>',
                            unsafe_allow_html=True)
                if st.button("x", key=f"del_{i}", use_container_width=True):
                    st.session_state.history.pop(i)
                    _save_history()
                    st.rerun()

    # Bottom spacer + user card
    st.markdown('<div style="height:70px;"></div>', unsafe_allow_html=True)
    st.markdown(f'''<div class="user-card">
        <div class="user-av">RM</div>
        <div><div class="user-nm">Raji Mubarak</div>
        <div class="user-pl">Team Cerebral</div></div>
    </div>''', unsafe_allow_html=True)


# ══════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════
online = api_ok()

# Backend mode indicator
_mode_label = "Direct" if _DIRECT_MODE else ("API" if online else "Offline")
_mode_color = "#22c55e" if (_DIRECT_MODE or online) else "#ef4444"

# Top bar (shown on all modes except home)
if st.session_state.mode != "home":
    st.markdown(f'''<div class="top-bar">
        <div class="top-bar-l">{LOGO_SM}<span>NaijaReview AI</span></div>
        <span style="font-size:.78rem;color:{_mode_color};font-weight:500;">
            <span class="dot" style="background:{_mode_color};"></span>
            {_mode_label}
        </span>
    </div>''', unsafe_allow_html=True)


# ════════ HOME — Hero Landing ════════
if st.session_state.mode == "home":
    st.markdown('<div style="height:18vh;"></div>', unsafe_allow_html=True)

    # Hero emoji + title + subtitle
    st.markdown('<div class="hero-emoji">✦</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">NaijaReview AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Your AI-powered review generator & recommendation engine.<br>'
                'Ask anything about products, get personalized recommendations, or generate reviews.</div>',
                unsafe_allow_html=True)

    # Centered input
    _p1, cc, _p2 = st.columns([1.2, 2.5, 1.2])
    with cc:
        query = st.text_input("Ask", placeholder="Ask anything about reviews, recommendations...",
                              label_visibility="collapsed", key="home_q")

        # Suggestion pills
        st.markdown('<div class="suggestion-pills">', unsafe_allow_html=True)
        pill_cols = st.columns(len(SUGGESTIONS))
        for idx, sug in enumerate(SUGGESTIONS):
            with pill_cols[idx]:
                if st.button(f'{sug["icon"]}  {sug["label"]}', key=f"sug_{idx}", use_container_width=True):
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
        st.markdown('</div>', unsafe_allow_html=True)

        # Powered-by footer
        st.markdown(f'''<div class="powered-by">
            Powered by <a href="#">Groq Llama 3.3</a> · <a href="#">OpenAI GPT-4o-mini</a> · Team Cerebral
            <br><span style="color:{'#22c55e' if online else '#ef4444'}">● {_mode_label}</span>
        </div>''', unsafe_allow_html=True)

        if query:
            st.session_state.mode = "chat"
            st.session_state.msgs.append({"role": "user", "content": query})
            resp = smart_chat(query, st.session_state.sid)
            st.session_state.msgs.append({"role": "assistant", "content": resp})
            st.session_state.history.insert(0, {
                "title": query[:30], "mode": "chat",
                "msgs": list(st.session_state.msgs)
            })
            _save_history()
            st.rerun()


# ════════ REVIEW ════════
elif st.session_state.mode == "review":
    st.markdown(f'<div class="mode-pill">{IC["edit"]} Generate Review</div>', unsafe_allow_html=True)
    _p1, cm, _p2 = st.columns([1, 3, 1])
    with cm:
        st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
        p = st.session_state.prefs
        uid = st.text_input("User ID", "demo_user_001", key="a_uid")
        c1, c2 = st.columns(2)
        with c1:
            item = st.text_input("Product", "Samsung Galaxy Buds3 Pro")
            cat = st.selectbox("Category", ["Electronics", "Restaurants", "Books", "Fashion", "Movies"],
                               index=["Electronics", "Restaurants", "Books", "Fashion", "Movies"].index(p["default_category"]))
        with c2:
            desc = st.text_area("Description", "Premium wireless earbuds with ANC and 360 Audio.", height=100)
            is_ng = st.toggle("Nigerian Mode 🇳🇬", p["nigerian_mode"], key="a_ng")
        if st.button("Generate Review  →", type="primary", use_container_width=True, key="gen"):
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
        if st.session_state.result and st.session_state.mode == "review":
            d = st.session_state.result
            st.markdown(f'''<div class="metric-row">
                <div class="metric-card"><div class="metric-val">{d.get("rating",0):.1f}</div><div class="metric-lbl">Rating</div></div>
                <div class="metric-card"><div class="metric-val">{d.get("confidence",0):.0%}</div><div class="metric-lbl">Confidence</div></div>
                <div class="metric-card"><div class="metric-val">{len(d.get("review_text","").split())}</div><div class="metric-lbl">Words</div></div>
            </div><div class="review-box">{d.get("review_text","")}</div>''', unsafe_allow_html=True)
            with st.expander("🧠 Agent Reasoning"):
                st.write(d.get("reasoning", ""))


# ════════ RECOMMEND ════════
elif st.session_state.mode == "recommend":
    st.markdown(f'<div class="mode-pill">{IC["star"]} Get Recommendations</div>', unsafe_allow_html=True)
    _p1, cm, _p2 = st.columns([1, 3, 1])
    with cm:
        st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
        p = st.session_state.prefs
        uid = st.text_input("User ID", "demo_user_001", key="b_uid")
        q = st.text_input("What are you looking for?", placeholder="e.g. Good earbuds for Lagos traffic", key="b_q")
        c1, c2 = st.columns(2)
        with c1:
            k = st.slider("Results", 3, 15, p["top_k"])
        with c2:
            cat_f = st.selectbox("Category", [None, "Electronics", "Restaurants", "Books"], key="b_cat")
        if st.button("Get Recommendations  →", type="primary", use_container_width=True, key="rec"):
            reviews = [{"rating": 5, "review_text": "Love this!", "item_name": "JBL Speaker", "category": "Electronics"}]
            with st.spinner("Searching & ranking..."):
                result = smart_recommend(uid, q, k, p["nigerian_mode"], cat_f, reviews)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.session_state.result = result
                    st.session_state.history.insert(0, {"title": f"Recs: {q[:25]}" if q else "Recommendations", "mode": "recommend", "msgs": []})
                    _save_history()
        if st.session_state.result and st.session_state.mode == "recommend":
            data = st.session_state.result
            st.caption(f"🔍 {data.get('total_candidates_considered', 0)} candidates evaluated")
            for rec in data.get("recommendations", []):
                st.markdown(f'''<div class="rec-card">
                    <div class="rec-rank">{rec.get("rank","")}</div>
                    <div style="flex:1;">
                        <div class="rec-name">{rec.get("item_name","")}</div>
                        <span class="rec-cat">{rec.get("category","")}</span>
                        <div class="rec-desc">{rec.get("explanation","")[:200]}</div>
                    </div>
                </div>''', unsafe_allow_html=True)


# ════════ CHAT ════════
elif st.session_state.mode == "chat":
    st.markdown(f'<div class="mode-pill">{IC["chat"]} Chat with AI</div>', unsafe_allow_html=True)

    for m in st.session_state.msgs:
        av = AV_AI if m["role"] == "assistant" else AV_USER
        with st.chat_message(m["role"]):
            st.markdown(f'''<div style="display:flex;gap:12px;align-items:flex-start;">
                <div style="flex-shrink:0;margin-top:2px;">{av}</div>
                <div style="font-size:.9rem;line-height:1.7;color:#111827;">{m["content"]}</div>
            </div>''', unsafe_allow_html=True)

    if prompt := st.chat_input("Ask for recommendations, reviews, or anything..."):
        st.session_state.msgs.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(f'<div style="display:flex;gap:12px;align-items:flex-start;">'
                        f'<div style="flex-shrink:0;margin-top:2px;">{AV_USER}</div>'
                        f'<div style="font-size:.9rem;line-height:1.7;">{prompt}</div></div>',
                        unsafe_allow_html=True)
        with st.chat_message("assistant"):
            ph = st.empty()
            ph.markdown(f'<div style="display:flex;gap:12px;align-items:center;">'
                        f'<div style="flex-shrink:0;">{AV_AI}</div>'
                        f'<div style="color:#9ca3af;display:flex;align-items:center;gap:6px;">'
                        f'{STOP_IC} Thinking...</div></div>', unsafe_allow_html=True)
            resp = smart_chat(prompt, st.session_state.sid)
            ph.markdown(f'<div style="display:flex;gap:12px;align-items:flex-start;">'
                        f'<div style="flex-shrink:0;margin-top:2px;">{AV_AI}</div>'
                        f'<div style="font-size:.9rem;line-height:1.7;color:#111827;">{resp}</div></div>',
                        unsafe_allow_html=True)
            st.session_state.msgs.append({"role": "assistant", "content": resp})
            st.session_state.history.insert(0, {
                "title": prompt[:30], "mode": "chat",
                "msgs": list(st.session_state.msgs)
            })
            _save_history()


# ════════ PREFERENCES ════════
elif st.session_state.mode == "preferences":
    _p1, cm, _p2 = st.columns([1, 3, 1])
    with cm:
        st.markdown(f'<div class="sec-hd">{IC["gear"]} <span style="font-size:1.1rem;font-weight:600;">Preferences</span></div>', unsafe_allow_html=True)
        p = st.session_state.prefs
        ng = st.toggle("Nigerian Mode 🇳🇬", p["nigerian_mode"], key="pf_ng")
        region = st.selectbox("Default Region", ["Lagos", "Abuja", "Port Harcourt", "Kano", "Ibadan", "Enugu"],
                              index=["Lagos", "Abuja", "Port Harcourt", "Kano", "Ibadan", "Enugu"].index(p["region"]), key="pf_r")
        cat = st.selectbox("Default Category", ["Electronics", "Restaurants", "Books", "Fashion", "Movies"],
                           index=["Electronics", "Restaurants", "Books", "Fashion", "Movies"].index(p["default_category"]), key="pf_c")
        topk = st.slider("Default recommendations", 3, 20, p["top_k"], key="pf_k")
        if st.button("Save Preferences  ✓", type="primary", use_container_width=True, key="save_p"):
            st.session_state.prefs = {"nigerian_mode": ng, "region": region,
                                      "default_category": cat, "top_k": topk}
            st.success("✅ Preferences saved successfully.")


# ════════ SYSTEM INFO ════════
elif st.session_state.mode == "system_info":
    _p1, cm, _p2 = st.columns([1, 3, 1])
    with cm:
        st.markdown(f'<div class="sec-hd">{IC["info"]} <span style="font-size:1.1rem;font-weight:600;">System Information</span></div>', unsafe_allow_html=True)
        st.info(f"**Mode:** {'Direct Pipeline' if _DIRECT_MODE else 'FastAPI Backend'}")
        if online:
            try:
                import requests
                st.json(requests.get(f"{API}/health", timeout=3).json())
            except Exception:
                st.warning("Could not fetch API info.")
        else:
            st.warning("FastAPI backend is offline. Running in direct mode." if _DIRECT_MODE else "API is offline.")
