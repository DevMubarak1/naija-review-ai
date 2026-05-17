"""NaijaReview AI — Dashboard (persistent chats, delete, spacing fixed)"""
import json, os, uuid, requests, streamlit as st
from app.styles import CSS, LOGO, LOGO_SM, AV_USER, AV_AI, STOP_IC, IC, nav_html

st.set_page_config(page_title="NaijaReview AI", page_icon="🇳🇬", layout="wide",
                   initial_sidebar_state="expanded")
st.markdown(CSS, unsafe_allow_html=True)

API = "http://localhost:8000"
HIST_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "chat_history.json")

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
if "search_open" not in st.session_state:
    st.session_state.search_open = False
if "more_open" not in st.session_state:
    st.session_state.more_open = False
if "history" not in st.session_state:
    st.session_state.history = _load_history() or [
        {"title": "Samsung Galaxy Buds review", "mode": "review", "msgs": []},
        {"title": "Restaurant recommendations Lagos", "mode": "recommend", "msgs": []},
        {"title": "Book ratings analysis", "mode": "chat", "msgs": []},
    ]
if "prefs" not in st.session_state:
    st.session_state.prefs = {"nigerian_mode": True, "region": "Lagos",
                               "default_category": "Electronics", "top_k": 8}


def api_ok():
    try:
        return requests.get(f"{API}/health", timeout=3).ok
    except Exception:
        return False


def smart_chat(msg, sid):
    try:
        r = requests.post(f"{API}/task-b/chat", json={
            "user_id": "demo_user_001", "message": msg,
            "session_id": sid,
            "is_nigerian": st.session_state.prefs["nigerian_mode"],
        }, timeout=90)
        if r.ok:
            return r.json().get("response", "I couldn't process that.")
        return f"API Error ({r.status_code})"
    except requests.exceptions.ConnectionError:
        return "Cannot reach the API. Make sure FastAPI is running on port 8000."
    except Exception as e:
        return f"Error: {str(e)[:150]}"


def nav_btn(icon_key, label, key, mode_check=None):
    """HTML label + invisible overlay button."""
    active = (mode_check is not None and st.session_state.mode == mode_check)
    st.markdown(nav_html(icon_key, label, active=active), unsafe_allow_html=True)
    return st.button(label, key=key, use_container_width=True)


# ══════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════
with st.sidebar:
    # Logo — fixed at top via sticky CSS
    st.markdown(f'''<div class="sidebar-logo-fixed">
        {LOGO}<span style="font-size:.93rem;font-weight:700;color:#111827;">NaijaReview AI</span>
    </div>''', unsafe_allow_html=True)

    # New Chat
    if st.button("New chat", key="new_chat", type="primary", use_container_width=True):
        st.session_state.mode = "home"
        st.session_state.result = None
        st.session_state.msgs = []
        st.session_state.sid = str(uuid.uuid4())
        st.rerun()

    # Search
    if nav_btn("search", "Search chats", "search_btn"):
        st.session_state.search_open = not st.session_state.search_open
    if st.session_state.search_open:
        sq = st.text_input("s", placeholder="Search history...",
                           label_visibility="collapsed", key="sq")
        if sq:
            matches = [h for h in st.session_state.history if sq.lower() in h["title"].lower()]
            for j, h in enumerate(matches[:5]):
                st.markdown(nav_html("chat", h["title"][:28]), unsafe_allow_html=True)
                if st.button(h["title"][:28], key=f"sr_{j}", use_container_width=True):
                    st.session_state.mode = h.get("mode", "chat")
                    st.session_state.msgs = h.get("msgs", [])
                    st.session_state.search_open = False
                    st.rerun()
            if not matches:
                st.caption("No results found.")

    # More
    if nav_btn("more", "More", "more_btn"):
        st.session_state.more_open = not st.session_state.more_open
    if st.session_state.more_open:
        if nav_btn("trash", "Clear all chats", "clear_all"):
            st.session_state.history = []
            st.session_state.msgs = []
            st.session_state.more_open = False
            _save_history()
            st.rerun()
        if nav_btn("info", "System info", "sys_btn", "system_info"):
            st.session_state.mode = "system_info"
            st.session_state.more_open = False
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
    if nav_btn("clock", "History", "nav_hist", "history_view"):
        st.session_state.mode = "history_view"; st.rerun()

    # ── Recents (with delete) ──
    st.markdown('<div class="nav-sec">Recents</div>', unsafe_allow_html=True)
    for i, h in enumerate(st.session_state.history[:5]):
        # Row: icon + title + delete
        col_title, col_del = st.columns([0.85, 0.15])
        with col_title:
            st.markdown(nav_html("chat", h["title"][:26]), unsafe_allow_html=True)
            if st.button(h["title"][:26], key=f"rc_{i}", use_container_width=True):
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

    # Bottom spacer + fixed user card
    st.markdown('<div style="height:70px;"></div>', unsafe_allow_html=True)
    st.markdown(f'''<div class="user-fixed">
        <div class="user-av">RM</div>
        <div><div class="user-nm">Raji Mubarak</div>
        <div class="user-pl">Team Cerebral</div></div>
    </div>''', unsafe_allow_html=True)


# ══════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════
online = api_ok()
st.markdown(f'''<div class="top-bar">
    <div class="top-bar-l">{LOGO_SM}<span>NaijaReview AI</span></div>
    <span style="font-size:.78rem;color:{'#22c55e' if online else '#ef4444'};font-weight:500;">
        <span class="dot" style="background:{'#22c55e' if online else '#ef4444'};"></span>
        {'Online' if online else 'Offline'}
    </span>
</div>''', unsafe_allow_html=True)


# ════════ HOME ════════
if st.session_state.mode == "home":
    st.markdown('<div style="height:25vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;font-size:1.5rem;font-weight:500;'
                'color:#111827;margin-bottom:1.5rem;">Good to see you, Dev Mubarak.</div>',
                unsafe_allow_html=True)
    _p1, cc, _p2 = st.columns([1.2, 2.5, 1.2])
    with cc:
        query = st.text_input("Ask", placeholder="Ask anything about reviews, recommendations...",
                              label_visibility="collapsed", key="home_q")
        # Chip buttons — wrapped in styled container
        st.markdown('<div class="home-chips-area">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Generate Review", key="c_rev", use_container_width=True):
                st.session_state.mode = "review"; st.rerun()
        with c2:
            if st.button("Get Recommendations", key="c_rec", use_container_width=True):
                st.session_state.mode = "recommend"; st.rerun()
        with c3:
            if st.button("Chat with AI", key="c_chat", use_container_width=True):
                st.session_state.mode = "chat"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
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
        p = st.session_state.prefs
        uid = st.text_input("User ID", "demo_user_001", key="a_uid")
        c1, c2 = st.columns(2)
        with c1:
            item = st.text_input("Product", "Samsung Galaxy Buds3 Pro")
            cat = st.selectbox("Category", ["Electronics", "Restaurants", "Books", "Fashion", "Movies"],
                               index=["Electronics", "Restaurants", "Books", "Fashion", "Movies"].index(p["default_category"]))
        with c2:
            desc = st.text_area("Description", "Premium wireless earbuds with ANC and 360 Audio.", height=100)
            is_ng = st.toggle("Nigerian Mode", p["nigerian_mode"], key="a_ng")
        if st.button("Generate Review", type="primary", use_container_width=True, key="gen"):
            reviews = [
                {"rating": 5, "review_text": "Amazing!", "item_name": "Headphones", "category": "Electronics"},
                {"rating": 4, "review_text": "Good value.", "item_name": "Phone Case", "category": "Electronics"},
                {"rating": 2, "review_text": "Disappointed.", "item_name": "USB Cable", "category": "Electronics"},
            ]
            with st.spinner("Agent reasoning..."):
                try:
                    r = requests.post(f"{API}/task-a/generate", json={
                        "user_id": uid, "item_name": item, "item_category": cat,
                        "item_description": desc, "user_reviews": reviews,
                        "is_nigerian": is_ng, "region": p["region"],
                    }, timeout=120)
                    if r.ok:
                        st.session_state.result = r.json()
                        st.session_state.history.insert(0, {"title": f"{item} review", "mode": "review", "msgs": []})
                        _save_history()
                    else:
                        st.error(r.text[:200])
                except Exception as e:
                    st.error(str(e)[:200])
        if st.session_state.result and st.session_state.mode == "review":
            d = st.session_state.result
            st.markdown(f'''<div class="m-row">
                <div class="m-box"><div class="m-val">{d.get("rating",0):.1f}</div><div class="m-lbl">Rating</div></div>
                <div class="m-box"><div class="m-val">{d.get("confidence",0):.0%}</div><div class="m-lbl">Confidence</div></div>
                <div class="m-box"><div class="m-val">{len(d.get("review_text","").split())}</div><div class="m-lbl">Words</div></div>
            </div><div class="review-out">{d.get("review_text","")}</div>''', unsafe_allow_html=True)
            with st.expander("Agent Reasoning"):
                st.write(d.get("reasoning", ""))


# ════════ RECOMMEND ════════
elif st.session_state.mode == "recommend":
    st.markdown(f'<div class="mode-pill">{IC["star"]} Get Recommendations</div>', unsafe_allow_html=True)
    _p1, cm, _p2 = st.columns([1, 3, 1])
    with cm:
        p = st.session_state.prefs
        uid = st.text_input("User ID", "demo_user_001", key="b_uid")
        q = st.text_input("What are you looking for?", placeholder="e.g. Good earbuds for Lagos traffic", key="b_q")
        c1, c2 = st.columns(2)
        with c1:
            k = st.slider("Results", 3, 15, p["top_k"])
        with c2:
            cat_f = st.selectbox("Category", [None, "Electronics", "Restaurants", "Books"], key="b_cat")
        if st.button("Get Recommendations", type="primary", use_container_width=True, key="rec"):
            with st.spinner("Searching & ranking..."):
                try:
                    r = requests.post(f"{API}/task-b/recommend", json={
                        "user_id": uid, "query": q, "top_k": k,
                        "is_nigerian": p["nigerian_mode"], "category_filter": cat_f,
                        "user_reviews": [{"rating": 5, "review_text": "Love this!", "item_name": "JBL Speaker", "category": "Electronics"}]
                    }, timeout=120)
                    if r.ok:
                        st.session_state.result = r.json()
                        st.session_state.history.insert(0, {"title": f"Recs: {q[:25]}" if q else "Recs", "mode": "recommend", "msgs": []})
                        _save_history()
                    else:
                        st.error(r.text[:200])
                except Exception as e:
                    st.error(str(e)[:200])
        if st.session_state.result and st.session_state.mode == "recommend":
            data = st.session_state.result
            st.caption(f"{data.get('total_candidates_considered', 0)} candidates evaluated")
            for rec in data.get("recommendations", []):
                st.markdown(f'''<div class="rec-it">
                    <div class="rec-rk">{rec.get("rank","")}</div>
                    <div style="flex:1;"><div style="font-weight:600;font-size:.9rem;color:#111827;">{rec.get("item_name","")}</div>
                    <span style="display:inline-block;padding:2px 8px;border-radius:4px;background:#dcf5e7;color:#1a7a4c;font-size:.7rem;font-weight:600;">{rec.get("category","")}</span>
                    <div style="font-size:.8rem;color:#4b5563;margin-top:4px;line-height:1.4;">{rec.get("explanation","")[:200]}</div></div>
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
            # Save to history + persist to disk
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
        ng = st.toggle("Nigerian Mode", p["nigerian_mode"], key="pf_ng")
        region = st.selectbox("Default Region", ["Lagos", "Abuja", "Port Harcourt", "Kano", "Ibadan", "Enugu"],
                              index=["Lagos", "Abuja", "Port Harcourt", "Kano", "Ibadan", "Enugu"].index(p["region"]), key="pf_r")
        cat = st.selectbox("Default Category", ["Electronics", "Restaurants", "Books", "Fashion", "Movies"],
                           index=["Electronics", "Restaurants", "Books", "Fashion", "Movies"].index(p["default_category"]), key="pf_c")
        topk = st.slider("Default recommendations", 3, 20, p["top_k"], key="pf_k")
        if st.button("Save Preferences", type="primary", use_container_width=True, key="save_p"):
            st.session_state.prefs = {"nigerian_mode": ng, "region": region,
                                      "default_category": cat, "top_k": topk}
            st.success("Preferences saved.")


# ════════ HISTORY ════════
elif st.session_state.mode == "history_view":
    _p1, cm, _p2 = st.columns([1, 3, 1])
    with cm:
        st.markdown(f'<div class="sec-hd">{IC["clock"]} <span style="font-size:1.1rem;font-weight:600;">Chat History</span></div>', unsafe_allow_html=True)
        if not st.session_state.history:
            st.info("No history yet.")
        else:
            for i, h in enumerate(st.session_state.history):
                c1, c2 = st.columns([5, 1])
                with c1:
                    if st.button(h["title"], key=f"h_{i}", use_container_width=True):
                        st.session_state.mode = h.get("mode", "chat")
                        st.session_state.msgs = h.get("msgs", [])
                        st.session_state.result = None
                        st.rerun()
                with c2:
                    if st.button("Del", key=f"d_{i}"):
                        st.session_state.history.pop(i)
                        _save_history()
                        st.rerun()


# ════════ SYSTEM INFO ════════
elif st.session_state.mode == "system_info":
    _p1, cm, _p2 = st.columns([1, 3, 1])
    with cm:
        st.markdown(f'<div class="sec-hd">{IC["info"]} <span style="font-size:1.1rem;font-weight:600;">System Information</span></div>', unsafe_allow_html=True)
        if online:
            try:
                st.json(requests.get(f"{API}/health", timeout=3).json())
            except Exception:
                st.warning("Could not fetch info.")
        else:
            st.warning("API is offline.")
