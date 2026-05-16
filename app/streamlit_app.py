"""NaijaReview AI — Dashboard (inline SVG icons, zero emojis)"""
import uuid, requests, streamlit as st
from app.styles import (CSS, LOGO, LOGO_SM, AV_USER, AV_AI, STOP_IC,
                         IC_PLUS, IC_SEARCH, IC_MORE, IC_EDIT, IC_STAR,
                         IC_CHAT, IC_GEAR, IC_CLOCK, IC_TRASH, IC_INFO,
                         IC_SAVE, IC_SPARK)

st.set_page_config(page_title="NaijaReview AI", page_icon="🇳🇬", layout="wide",
                   initial_sidebar_state="expanded")
st.markdown(CSS, unsafe_allow_html=True)
API = "http://localhost:8000"

# ── Session defaults ──
_d = {
    "mode": "home", "msgs": [], "sid": str(uuid.uuid4()),
    "result": None, "search_open": False, "more_open": False,
    "history": [
        {"title": "Samsung Galaxy Buds review", "mode": "review"},
        {"title": "Restaurant recommendations Lagos", "mode": "recommend"},
        {"title": "Book ratings analysis", "mode": "chat"},
    ],
    "prefs": {"nigerian_mode": True, "region": "Lagos",
              "default_category": "Electronics", "top_k": 8},
}
for k, v in _d.items():
    if k not in st.session_state:
        st.session_state[k] = v


def api_ok():
    try:
        return requests.get(f"{API}/health", timeout=3).ok
    except Exception:
        return False


def smart_chat(msg, sid):
    """Send to conversational chat API — no mode required."""
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
        return "Cannot reach the API. Please make sure the FastAPI server is running on port 8000."
    except Exception as e:
        return f"Error: {str(e)[:150]}"


def sidebar_btn(svg_icon, label, key, is_primary=False):
    """Render an SVG icon + clickable button as a single row using columns."""
    c_icon, c_btn = st.columns([0.12, 0.88], gap="small")
    with c_icon:
        st.markdown(f'<div style="display:flex;align-items:center;height:36px;color:#4b5563;">{svg_icon}</div>',
                    unsafe_allow_html=True)
    with c_btn:
        return st.button(label, key=key, use_container_width=True,
                         type="primary" if is_primary else "secondary")


# ══════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════
with st.sidebar:
    # Logo — flush top
    st.markdown(f'<div style="display:flex;align-items:center;gap:9px;padding:8px 10px 6px;">'
                f'{LOGO}<span style="font-size:.93rem;font-weight:700;color:#111827;">NaijaReview AI</span></div>',
                unsafe_allow_html=True)

    # New Chat
    if sidebar_btn(IC_PLUS, "New chat", "new_chat", is_primary=True):
        st.session_state.mode = "home"
        st.session_state.result = None
        st.session_state.msgs = []
        st.session_state.sid = str(uuid.uuid4())
        st.rerun()

    # Search
    if sidebar_btn(IC_SEARCH, "Search chats", "search_btn"):
        st.session_state.search_open = not st.session_state.search_open
    if st.session_state.search_open:
        sq = st.text_input("s", placeholder="Search history...",
                           label_visibility="collapsed", key="sq")
        if sq:
            for h in st.session_state.history:
                if sq.lower() in h["title"].lower():
                    st.caption(h["title"])

    # More
    if sidebar_btn(IC_MORE, "More", "more_btn"):
        st.session_state.more_open = not st.session_state.more_open
    if st.session_state.more_open:
        if sidebar_btn(IC_TRASH, "Clear all chats", "clear_all"):
            st.session_state.history = []; st.session_state.msgs = []
            st.session_state.more_open = False; st.rerun()
        if sidebar_btn(IC_INFO, "System info", "sys_btn"):
            st.session_state.mode = "system_info"
            st.session_state.more_open = False; st.rerun()

    # Modes
    st.markdown('<div class="nav-sec">Modes</div>', unsafe_allow_html=True)
    if sidebar_btn(IC_EDIT, "Generate Review", "nav_rev"):
        st.session_state.mode = "review"; st.session_state.result = None; st.rerun()
    if sidebar_btn(IC_STAR, "Get Recommendations", "nav_rec"):
        st.session_state.mode = "recommend"; st.session_state.result = None; st.rerun()
    if sidebar_btn(IC_CHAT, "Chat with AI", "nav_chat"):
        st.session_state.mode = "chat"; st.rerun()

    # Settings
    st.markdown('<div class="nav-sec">Settings</div>', unsafe_allow_html=True)
    if sidebar_btn(IC_GEAR, "Preferences", "nav_pref"):
        st.session_state.mode = "preferences"; st.rerun()
    if sidebar_btn(IC_CLOCK, "History", "nav_hist"):
        st.session_state.mode = "history_view"; st.rerun()

    # Recents
    st.markdown('<div class="nav-sec">Recents</div>', unsafe_allow_html=True)
    for i, h in enumerate(st.session_state.history[:5]):
        if sidebar_btn(IC_CHAT, h["title"][:28], f"rc_{i}"):
            st.session_state.mode = h["mode"]
            st.session_state.result = None; st.rerun()

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
        st.markdown('<div class="chip-row">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Generate Review", key="c_rev"):
                st.session_state.mode = "review"; st.rerun()
        with c2:
            if st.button("Get Recommendations", key="c_rec"):
                st.session_state.mode = "recommend"; st.rerun()
        with c3:
            if st.button("Chat with AI", key="c_chat"):
                st.session_state.mode = "chat"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        if query:
            st.session_state.mode = "chat"
            st.session_state.msgs.append({"role": "user", "content": query})
            resp = smart_chat(query, st.session_state.sid)
            st.session_state.msgs.append({"role": "assistant", "content": resp})
            st.session_state.history.insert(0, {"title": query[:30], "mode": "chat"})
            st.rerun()


# ════════ REVIEW ════════
elif st.session_state.mode == "review":
    _p1, cm, _p2 = st.columns([1, 3, 1])
    with cm:
        st.markdown(f'<div class="sec-hd">{IC_EDIT} <span style="font-size:1.1rem;font-weight:600;">Generate Review & Rating</span></div>', unsafe_allow_html=True)
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
                {"rating": 5, "review_text": "Best jollof in Lagos!", "item_name": "Mama Put", "category": "Restaurants"},
                {"rating": 3, "review_text": "Okay book.", "item_name": "Half of a Yellow Sun", "category": "Books"},
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
                        st.session_state.history.insert(0, {"title": f"{item} review", "mode": "review"})
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
    _p1, cm, _p2 = st.columns([1, 3, 1])
    with cm:
        st.markdown(f'<div class="sec-hd">{IC_STAR} <span style="font-size:1.1rem;font-weight:600;">Get Recommendations</span></div>', unsafe_allow_html=True)
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
                        "user_reviews": [
                            {"rating": 5, "review_text": "Love this!", "item_name": "JBL Speaker", "category": "Electronics"},
                            {"rating": 4, "review_text": "Great read", "item_name": "Things Fall Apart", "category": "Books"},
                        ]
                    }, timeout=120)
                    if r.ok:
                        st.session_state.result = r.json()
                        st.session_state.history.insert(0, {"title": f"Recs: {q[:25]}" if q else "Recs", "mode": "recommend"})
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
    for m in st.session_state.msgs:
        av = AV_AI if m["role"] == "assistant" else AV_USER
        with st.chat_message(m["role"]):
            st.markdown(f'''<div style="display:flex;gap:10px;align-items:flex-start;">
                <div style="flex-shrink:0;">{av}</div>
                <div style="font-size:.9rem;line-height:1.6;color:#111827;">{m["content"]}</div>
            </div>''', unsafe_allow_html=True)
    if prompt := st.chat_input("Ask for recommendations, reviews, or anything..."):
        st.session_state.msgs.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(f'<div style="display:flex;gap:10px;align-items:flex-start;"><div style="flex-shrink:0;">{AV_USER}</div><div style="font-size:.9rem;line-height:1.6;">{prompt}</div></div>', unsafe_allow_html=True)
        with st.chat_message("assistant"):
            ph = st.empty()
            ph.markdown(f'<div style="display:flex;gap:10px;align-items:center;"><div style="flex-shrink:0;">{AV_AI}</div><div style="color:#9ca3af;display:flex;align-items:center;gap:6px;">{STOP_IC} Thinking...</div></div>', unsafe_allow_html=True)
            resp = smart_chat(prompt, st.session_state.sid)
            ph.markdown(f'<div style="display:flex;gap:10px;align-items:flex-start;"><div style="flex-shrink:0;">{AV_AI}</div><div style="font-size:.9rem;line-height:1.6;color:#111827;">{resp}</div></div>', unsafe_allow_html=True)
            st.session_state.msgs.append({"role": "assistant", "content": resp})
            st.session_state.history.insert(0, {"title": prompt[:30], "mode": "chat"})


# ════════ PREFERENCES ════════
elif st.session_state.mode == "preferences":
    _p1, cm, _p2 = st.columns([1, 3, 1])
    with cm:
        st.markdown(f'<div class="sec-hd">{IC_GEAR} <span style="font-size:1.1rem;font-weight:600;">Preferences</span></div>', unsafe_allow_html=True)
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
        st.markdown(f'<div class="sec-hd">{IC_CLOCK} <span style="font-size:1.1rem;font-weight:600;">Chat History</span></div>', unsafe_allow_html=True)
        if not st.session_state.history:
            st.info("No history yet.")
        else:
            for i, h in enumerate(st.session_state.history):
                ic = {"review": IC_EDIT, "recommend": IC_STAR, "chat": IC_CHAT}.get(h["mode"], IC_CHAT)
                c1, c2 = st.columns([5, 1])
                with c1:
                    if st.button(h["title"], key=f"h_{i}", use_container_width=True):
                        st.session_state.mode = h["mode"]
                        st.session_state.result = None; st.rerun()
                with c2:
                    if st.button("Del", key=f"d_{i}"):
                        st.session_state.history.pop(i); st.rerun()


# ════════ SYSTEM INFO ════════
elif st.session_state.mode == "system_info":
    _p1, cm, _p2 = st.columns([1, 3, 1])
    with cm:
        st.markdown(f'<div class="sec-hd">{IC_INFO} <span style="font-size:1.1rem;font-weight:600;">System Information</span></div>', unsafe_allow_html=True)
        if online:
            try:
                st.json(requests.get(f"{API}/health", timeout=3).json())
            except Exception:
                st.warning("Could not fetch info.")
        else:
            st.warning("API is offline.")
