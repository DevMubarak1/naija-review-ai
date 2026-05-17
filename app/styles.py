"""NaijaReview AI — Styles & SVG Assets"""

# ── Logos ──
LOGO = '<svg width="28" height="28" viewBox="0 0 36 36" fill="none"><rect width="36" height="36" rx="10" fill="#1a7a4c"/><path d="M8 12L18 8l10 4v12l-10 4-10-4Z" fill="none" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/><circle cx="18" cy="17" r="4" fill="#fff" opacity=".9"/><path d="M16 17l1.5 1.5L20 15.5" stroke="#1a7a4c" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
LOGO_SM = '<svg width="22" height="22" viewBox="0 0 36 36" fill="none"><rect width="36" height="36" rx="10" fill="#1a7a4c"/><circle cx="18" cy="17" r="4" fill="#fff" opacity=".9"/><path d="M16 17l1.5 1.5L20 15.5" stroke="#1a7a4c" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# ── Chat avatars ──
AV_USER = '<svg width="28" height="28" viewBox="0 0 28 28"><circle cx="14" cy="14" r="14" fill="#e8f5ee"/><circle cx="14" cy="10" r="4.5" fill="#1a7a4c"/><path d="M5 24c0-5 4-9 9-9s9 4 9 9" fill="#1a7a4c"/></svg>'
AV_AI = '<svg width="28" height="28" viewBox="0 0 28 28"><circle cx="14" cy="14" r="14" fill="#1a7a4c"/><circle cx="14" cy="12" r="3.5" fill="#fff" opacity=".9"/><path d="M12 12l1.2 1.2L15 11" stroke="#1a7a4c" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"/><rect x="8" y="19" width="12" height="2" rx="1" fill="#fff" opacity=".4"/></svg>'
STOP_IC = '<svg width="14" height="14" viewBox="0 0 14 14"><rect x="2" y="2" width="10" height="10" rx="2" fill="#9ca3af"/></svg>'

# ── SVG icons — all 16x16 ──
def _ic(d):
    return f'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{d}</svg>'

IC = {
    "plus": _ic('<path d="M12 5v14M5 12h14"/>'),
    "search": _ic('<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.35-4.35"/>'),
    "more": '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><circle cx="5" cy="12" r="1.5"/><circle cx="12" cy="12" r="1.5"/><circle cx="19" cy="12" r="1.5"/></svg>',
    "edit": _ic('<path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.12 2.12 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>'),
    "star": _ic('<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>'),
    "chat": _ic('<path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>'),
    "gear": _ic('<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 01-2.83 2.83l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 012.83-2.83l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z"/>'),
    "clock": _ic('<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>'),
    "trash": _ic('<path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/>'),
    "info": _ic('<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>'),
    "x": _ic('<path d="M18 6L6 18M6 6l12 12"/>'),
    "menu": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1a7a4c" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>',
}


def nav_html(icon_key, label, active=False):
    """Single HTML nav item with inline SVG + label."""
    bg = "background:#e8f5ee;color:#1a7a4c;" if active else ""
    ic_color = "color:#1a7a4c;" if active else "color:#6b7280;"
    fw = "font-weight:600;" if active else "font-weight:500;"
    return f'''<div style="display:flex;align-items:center;gap:10px;padding:7px 12px;
        border-radius:8px;{bg}">
        <span style="flex-shrink:0;display:flex;align-items:center;{ic_color}">{IC[icon_key]}</span>
        <span style="font-size:0.84rem;{fw}color:{'#1a7a4c' if active else '#374151'};">{label}</span>
    </div>'''




CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
:root{
    --bg:#fff;--bg2:#f9fafb;--g:#1a7a4c;--gh:#15633e;--gl:#e8f5ee;--gb:#dcf5e7;
    --t:#111827;--tm:#4b5563;--tl:#9ca3af;--b:#e5e7eb;--bl:#f3f4f6;--ib:#f3f4f6;
    --r:32px;--rs:12px;
}
html,body,[data-testid="stAppViewContainer"],[data-testid="stApp"],.main{
    background:var(--bg)!important;font-family:'Inter',sans-serif!important;
    padding-top:0!important;margin-top:0!important;
}
.block-container{padding:0!important;max-width:100%!important;}

/* Show Streamlit header and reserve space for it */
header[data-testid="stHeader"], #MainMenu, footer, [data-testid="stToolbar"],
[data-testid="stDecoration"]{display:block!important;height:auto!important;padding:0!important;margin:0!important}

/* Fix header to top and reserve 56px at top of app container so app content sits below it */
[data-testid="stHeader"], header[data-testid="stHeader"]{display:flex!important;position:fixed!important;top:0;left:0;right:0;height:56px!important;padding:8px 12px!important;margin:0!important;z-index:0!important;align-items:center;background:var(--bg)!important;border-bottom:1px solid var(--b)!important}
[data-testid="stAppViewContainer"] > header{height:56px!important;padding:0!important;margin:0!important}
[data-testid="stAppViewContainer"] > div:first-child{padding-top:56px!important;margin-top:0!important}

/* Hide any remaining banner/toolbar elements Streamlit may inject */
[role="banner"], [role="banner"] *{display:none!important;height:0!important;padding:0!important;margin:0!important}

/* Force app container to no top padding */
[data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] > div, [data-testid="stAppViewContainer"] > div > div{padding-top:0!important;margin-top:0!important}

/* ── Sidebar CLOSE button (X inside sidebar top-right) ── */
[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"]{
    display:flex!important;
    position:absolute!important;top:8px;right:8px;z-index:2000000!important;
    margin-top:0!important;padding:0!important;
}
[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button{
    background:transparent!important;border:none!important;
    color:var(--tl)!important;padding:4px!important;
    min-height:0!important;width:28px!important;height:28px!important;
    border-radius:6px!important;opacity:1!important;
    position:relative!important;margin-top:0!important;
}
[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button:hover{
    background:var(--bl)!important;color:var(--t)!important;
}

/* ── Sidebar OPEN button (hamburger when collapsed) ── */
[data-testid="collapsedControl"]{
    display:flex!important;
    position:fixed!important;
    top:6px;left:8px;z-index:2000001!important;transform:none!important;
}
[data-testid="collapsedControl"] button{
    background:var(--bg)!important;border:1px solid var(--b)!important;
    color:var(--g)!important;padding:6px!important;
    border-radius:8px!important;box-shadow:0 2px 8px rgba(0,0,0,.08)!important;
    min-height:0!important;width:36px!important;height:36px!important;
    display:flex!important;align-items:center!important;justify-content:center!important;
}
[data-testid="collapsedControl"] button:hover{
    background:var(--gl)!important;border-color:var(--g)!important;
}

/* Some Streamlit versions render the expand control inside the header
   (data-testid="stExpandSidebarButton"). Make that button fixed and above
   the header so it's always visible and clickable. */
[data-testid="stExpandSidebarButton"],
[data-testid="stExpandSidebarButton"] button{
    position:fixed!important;left:8px!important;top:8px!important;
    z-index:2000002!important;display:flex!important;
    width:36px!important;height:36px!important;padding:6px!important;
    align-items:center!important;justify-content:center!important;
    background:var(--bg)!important;border:1px solid var(--b)!important;
    border-radius:8px!important;box-shadow:0 2px 8px rgba(0,0,0,.08)!important;
    color:var(--g)!important;
}

/* Ensure header does not sit above the fixed expand button */
header[data-testid="stHeader"]{z-index:1!important}

/* ═══ SIDEBAR — kill the top gap ═══ */
[data-testid="stSidebar"]{
    background:var(--bg2)!important;border-right:1px solid var(--b)!important;
    width:260px!important;padding:0!important;
    transition:margin-left .25s ease, transform .25s ease!important;
}
/* THE FIX: target stSidebarUserContent which has the 1rem padding-top */
[data-testid="stSidebarUserContent"],
[data-testid="stSidebarContent"],
[data-testid="stSidebar"]>div,
[data-testid="stSidebar"]>div>div,
[data-testid="stSidebar"]>div:first-child,
section[data-testid="stSidebar"]>div>div,
section[data-testid="stSidebar"]>div>div>div{
    padding-top:0!important;margin-top:0!important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"]{padding:0!important;margin:0!important;}
[data-testid="stSidebar"] .stVerticalBlock{gap:0!important;}
section[data-testid="stSidebar"]>div{
    height:100vh!important;overflow-y:auto!important;
    padding:0 8px 80px!important;
}

/* ── Fixed logo at sidebar top ── */
.sidebar-logo-fixed{
    position:sticky!important;top:0;z-index:100000!important;
    background:var(--bg2);padding:4px 12px 8px;
    display:flex;align-items:center;gap:9px;
    border-bottom:1px solid var(--b);
    margin-top:0!important;
    margin-bottom:40px!important;
}


/* Additional sidebar container targets for newer Streamlit versions */
section[data-testid="stSidebar"]{padding-top:0!important;margin-top:0!important}
section[data-testid="stSidebar"]>div{padding-top:0!important;margin-top:0!important}
section[data-testid="stSidebar"]>div>div{padding-top:0!important;margin-top:0!important}

/* Make sure collapse button is above everything and clearly visible */
[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button{
    opacity:1!important;display:flex!important;align-items:center;justify-content:center!important;
    color:var(--g)!important;background:transparent!important;border:none!important;
}

/* Extra catch-all: some Streamlit builds render the collapsed control without the data-testid
   so also target any fixed button near the left edge that looks like the collapsed control */
button[aria-label][style*="position:fixed"]{z-index:1000002!important}

/* If the collapsed control is present but off-screen, force it into view */
[data-testid="collapsedControl"], [data-testid="collapsedControl"] *{left:8px!important;right:auto!important}

/* If the main menu/button uses headerNoPadding variant, ensure it's visible when used as collapsed control */
.st-emotion-cache-syskd6{opacity:1!important;z-index:2000003!important}

/* Sidebar buttons — invisible overlay for click handling */
[data-testid="stSidebar"] [data-testid="stButton"]{margin:0!important;padding:0!important;}
[data-testid="stSidebar"] [data-testid="stButton"] button{
    width:100%!important;background:transparent!important;
    border:none!important;padding:0!important;margin:0!important;
    min-height:0!important;height:32px!important;
    opacity:0!important;cursor:pointer!important;
    position:relative!important;margin-top:-32px!important;z-index:2!important;
}
/* New chat — visible pill */
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"]{
    opacity:1!important;height:auto!important;position:relative!important;
    margin-top:0!important;background:transparent!important;
    border:1px solid var(--b)!important;color:var(--t)!important;
    font-weight:600!important;border-radius:20px!important;
    padding:8px 14px!important;justify-content:center!important;
    font-size:.84rem!important;
}
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"]:hover{
    background:var(--gl)!important;border-color:var(--g)!important;color:var(--g)!important;
}

/* Fixed user card */
.user-fixed{position:fixed!important;bottom:0;left:0;width:260px;
    background:var(--bg2);border-top:1px solid var(--b);border-right:1px solid var(--b);
    padding:10px 14px;display:flex;align-items:center;gap:10px;z-index:999;}
.user-av{width:34px;height:34px;border-radius:50%;background:var(--gl);color:var(--g);
    display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.75rem;flex-shrink:0;}
.user-nm{font-size:.84rem;font-weight:600;color:var(--t);line-height:1.2;}
.user-pl{font-size:.68rem;color:var(--tl);}

/* Section headers — generous spacing */
.nav-sec{font-size:.65rem;text-transform:uppercase;letter-spacing:.1em;
    color:var(--tl);font-weight:600;padding:18px 12px 8px;margin:0;}

/* ═══ CHAT INPUT — premium styling ═══ */
[data-testid="stChatInput"]{
    max-width:720px!important;margin:0 auto!important;
    padding:0 16px 16px!important;
}
[data-testid="stChatInput"] textarea{
    border-radius:24px!important;border:1.5px solid var(--b)!important;
    background:var(--bg)!important;font-size:.9rem!important;
    padding:12px 20px!important;min-height:44px!important;
    box-shadow:0 1px 6px rgba(0,0,0,.04)!important;
    transition:border-color .2s,box-shadow .2s!important;
}
[data-testid="stChatInput"] textarea:focus{
    border-color:var(--g)!important;box-shadow:0 0 0 3px rgba(26,122,76,.08)!important;
}
[data-testid="stChatInput"]>div{
    border:none!important;background:transparent!important;
    border-radius:24px!important;
}
[data-testid="stChatInput"] button{
    background:var(--g)!important;color:#fff!important;border:none!important;
    border-radius:50%!important;width:32px!important;height:32px!important;
    min-width:32px!important;
}
/* The whole bottom container */
[data-testid="stBottom"]{background:var(--bg)!important;border-top:1px solid var(--bl)!important;}
[data-testid="stBottomBlockContainer"]{padding:0!important;max-width:100%!important;}

/* ═══ TEXT INPUT (home page) ═══ */
[data-testid="stTextInput"] input{
    background:var(--ib)!important;border:1px solid var(--b)!important;
    border-radius:var(--r)!important;padding:14px 20px!important;font-size:.92rem!important;
    box-shadow:none!important;transition:border-color .2s,box-shadow .2s!important;
}
[data-testid="stTextInput"] input:focus{
    border-color:var(--g)!important;box-shadow:0 0 0 3px rgba(26,122,76,.08)!important;
}
[data-testid="stTextInput"]>div{border:none!important;background:transparent!important;}
[data-testid="stTextInput"] label{display:none!important;}

/* ═══ HOME CHIP BUTTONS — horizontal row ═══ */
.home-chips-area [data-testid="stHorizontalBlock"]{
    display:flex!important;gap:10px!important;justify-content:center!important;
    margin-top:8px!important;
}
.home-chips-area [data-testid="stButton"] button{
    background:transparent!important;border:1px solid var(--b)!important;
    border-radius:22px!important;color:var(--tm)!important;font-size:.82rem!important;
    font-weight:500!important;padding:8px 16px!important;white-space:nowrap!important;
    justify-content:center!important;transition:all .15s!important;
    opacity:1!important;height:auto!important;position:relative!important;margin-top:0!important;
}
.home-chips-area [data-testid="stButton"] button:hover{
    border-color:var(--g)!important;color:var(--g)!important;background:var(--gl)!important;
}

/* Green primary buttons (main content) */
.main [data-testid="stButton"] button[kind="primary"]{
    background:var(--g)!important;color:#fff!important;border:none!important;
    border-radius:22px!important;font-weight:600!important;padding:10px 24px!important;
    opacity:1!important;height:auto!important;position:relative!important;margin-top:0!important;
}
.main [data-testid="stButton"] button[kind="primary"]:hover{background:var(--gh)!important;}
.main [data-testid="stButton"] button{
    opacity:1!important;height:auto!important;position:relative!important;margin-top:0!important;
}

/* Top bar */
.top-bar{display:flex;align-items:center;justify-content:space-between;
    padding:8px 24px;border-bottom:1px solid var(--bl);}
.top-bar-l{display:flex;align-items:center;gap:8px;font-size:.9rem;font-weight:600;color:var(--t);}
.dot{width:7px;height:7px;border-radius:50%;display:inline-block;margin-right:4px;}

/* Cards / Review */
.review-out{background:var(--bl);border-left:3px solid var(--g);border-radius:0 var(--rs) var(--rs) 0;
    padding:1.2rem 1.5rem;font-size:.92rem;line-height:1.75;color:var(--t);margin:1rem 0;}
.m-row{display:flex;gap:12px;margin:1rem 0;}
.m-box{flex:1;text-align:center;padding:14px;border-radius:12px;background:var(--gl);}
.m-val{font-size:1.3rem;font-weight:700;color:var(--g);}
.m-lbl{font-size:.7rem;color:var(--tm);margin-top:2px;}
.rec-it{display:flex;align-items:flex-start;gap:12px;padding:14px;border-radius:12px;
    border:1px solid var(--b);margin-bottom:6px;transition:border-color .15s;}
.rec-it:hover{border-color:var(--g);}
.rec-rk{width:32px;height:32px;min-width:32px;border-radius:8px;background:var(--g);
    color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.8rem;}
.sec-hd{display:flex;align-items:center;gap:10px;margin:1.5rem 0 1rem;color:var(--t);}

/* Chat — hide Streamlit default avatar */
[data-testid="stChatMessage"]{max-width:720px;margin:0 auto;background:transparent!important;border:none!important;}
[data-testid="stChatMessage"] [data-testid="stChatMessageAvatarCustom"],
[data-testid="stChatMessage"] [data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessage"] [data-testid="stChatMessageAvatarAssistant"],
[data-testid="stChatMessage"]>div:first-child>div:first-child{display:none!important;}

/* Mode pill */
.mode-pill{display:inline-flex;align-items:center;gap:6px;padding:4px 12px;
    border-radius:16px;background:var(--gl);color:var(--g);font-size:.75rem;
    font-weight:600;margin:4px 0 0 24px;}

[data-testid="stRadio"]{display:none!important;}
hr{display:none!important;}

/* Delete button in recents */
.del-btn{display:flex;align-items:center;justify-content:center;width:22px;height:22px;
    border-radius:4px;cursor:pointer;color:var(--tl);transition:all .15s;flex-shrink:0;}
.del-btn:hover{background:#fef2f2;color:#ef4444;}

/* Responsive */
@media(max-width:768px){
    [data-testid="stSidebar"]{width:220px!important;}
    .user-fixed{width:220px;}
    [data-testid="stChatInput"]{max-width:100%!important;}
}
</style>
"""
