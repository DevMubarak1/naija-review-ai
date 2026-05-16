"""NaijaReview AI — Styles (ChatGPT-inspired, white/green theme)"""

# SVG Logo for NaijaReview AI
LOGO_SVG = '''<svg width="36" height="36" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="36" height="36" rx="10" fill="#1a7a4c"/>
  <path d="M8 12 L18 8 L28 12 L28 24 L18 28 L8 24Z" fill="none" stroke="white" stroke-width="1.5" stroke-linejoin="round"/>
  <path d="M18 8 L18 28" stroke="white" stroke-width="1.2" opacity="0.4"/>
  <path d="M8 12 L28 12" stroke="white" stroke-width="1.2" opacity="0.4"/>
  <circle cx="18" cy="17" r="4" fill="white" opacity="0.9"/>
  <path d="M16 17 L17.5 18.5 L20 15.5" stroke="#1a7a4c" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="12" cy="22" r="1.5" fill="white" opacity="0.5"/>
  <circle cx="24" cy="22" r="1.5" fill="white" opacity="0.5"/>
</svg>'''

LOGO_SVG_SMALL = '''<svg width="28" height="28" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="36" height="36" rx="10" fill="#1a7a4c"/>
  <path d="M8 12 L18 8 L28 12 L28 24 L18 28 L8 24Z" fill="none" stroke="white" stroke-width="1.5" stroke-linejoin="round"/>
  <circle cx="18" cy="17" r="4" fill="white" opacity="0.9"/>
  <path d="M16 17 L17.5 18.5 L20 15.5" stroke="#1a7a4c" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''

# SVG Icons (inline, no external deps)
ICON = {
    "plus": '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 3v10M3 8h10" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
    "search": '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="7" cy="7" r="4.5" stroke="currentColor" stroke-width="1.5"/><path d="M10.5 10.5L14 14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
    "chat": '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M2 3h12v8H5l-3 3V3z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>',
    "pencil": '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M11.5 2.5l2 2L5 13H3v-2l8.5-8.5z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>',
    "star": '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 2l1.8 3.6L14 6.2l-3 2.9.7 4.1L8 11.4l-3.7 1.8.7-4.1-3-2.9 4.2-.6z" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/></svg>',
    "target": '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.3"/><circle cx="8" cy="8" r="3" stroke="currentColor" stroke-width="1.3"/><circle cx="8" cy="8" r="1" fill="currentColor"/></svg>',
    "globe": '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.3"/><path d="M2 8h12M8 2c2 2 2.5 4 2.5 6s-.5 4-2.5 6M8 2c-2 2-2.5 4-2.5 6s.5 4 2.5 6" stroke="currentColor" stroke-width="1.2"/></svg>',
    "folder": '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M2 4h4l2 2h6v7H2V4z" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/></svg>',
    "settings": '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="2.5" stroke="currentColor" stroke-width="1.3"/><path d="M8 1v2M8 13v2M1 8h2M13 8h2M3.05 3.05l1.41 1.41M11.54 11.54l1.41 1.41M3.05 12.95l1.41-1.41M11.54 4.46l1.41-1.41" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>',
    "dots": '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="3" cy="8" r="1.2" fill="currentColor"/><circle cx="8" cy="8" r="1.2" fill="currentColor"/><circle cx="13" cy="8" r="1.2" fill="currentColor"/></svg>',
    "history": '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.3"/><path d="M8 4v4l3 2" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "send": '<svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M3 9l12-6-6 12-1-5-5-1z" fill="currentColor"/></svg>',
    "mic": '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><rect x="6" y="2" width="4" height="8" rx="2" stroke="currentColor" stroke-width="1.3"/><path d="M4 8a4 4 0 008 0M8 12v2" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>',
    "user": '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="5" r="3" stroke="currentColor" stroke-width="1.3"/><path d="M2 14c0-3 2.5-5 6-5s6 2 6 5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>',
}

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg: #ffffff;
    --bg-sidebar: #f9fafb;
    --green: #1a7a4c;
    --green-hover: #15633e;
    --green-light: #e8f5ee;
    --green-badge: #dcf5e7;
    --text: #111827;
    --text-mid: #4b5563;
    --text-light: #9ca3af;
    --border: #e5e7eb;
    --border-light: #f3f4f6;
    --input-bg: #f3f4f6;
    --radius: 24px;
    --radius-sm: 12px;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main {
    background: var(--bg) !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
}
.block-container { padding: 0 !important; max-width: 100% !important; }
h1,h2,h3,h4,h5,h6,p,span,label,div,li,a,button {
    font-family: 'Inter', -apple-system, sans-serif !important;
}

/* Hide Streamlit chrome */
header[data-testid="stHeader"] { display: none !important; }
#MainMenu { display: none !important; }
footer { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border) !important;
    width: 260px !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] .block-container { padding: 12px !important; }
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }

.sidebar-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 8px 4px 16px;
}
.sidebar-logo {
    display: flex; align-items: center; gap: 8px;
    font-size: 0.92rem; font-weight: 600; color: var(--text);
}

/* Nav buttons */
.nav-btn {
    display: flex; align-items: center; gap: 10px;
    padding: 8px 10px; border-radius: 8px;
    font-size: 0.85rem; color: var(--text-mid);
    cursor: pointer; transition: background 0.15s;
    text-decoration: none; margin-bottom: 1px;
}
.nav-btn:hover { background: var(--green-light); color: var(--green); }
.nav-btn-active {
    background: var(--green) !important;
    color: white !important;
}
.nav-btn svg { flex-shrink: 0; }

.nav-section {
    font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.08em;
    color: var(--text-light); font-weight: 600;
    padding: 16px 10px 6px; margin-top: 4px;
}

.recent-item {
    display: block; padding: 6px 10px; border-radius: 6px;
    font-size: 0.82rem; color: var(--text-mid);
    cursor: pointer; transition: background 0.15s;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    margin-bottom: 1px;
}
.recent-item:hover { background: var(--border-light); }

.sidebar-footer {
    border-top: 1px solid var(--border);
    padding: 12px 10px; margin-top: auto;
    display: flex; align-items: center; gap: 8px;
}
.user-avatar {
    width: 32px; height: 32px; border-radius: 50%;
    background: var(--green-light); color: var(--green);
    display: flex; align-items: center; justify-content: center;
    font-weight: 600; font-size: 0.75rem;
}
.user-name { font-size: 0.82rem; font-weight: 500; color: var(--text); }
.user-plan { font-size: 0.68rem; color: var(--text-light); }

/* ── Main Content (centered like ChatGPT) ── */
.main-center {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    min-height: 75vh; padding: 2rem;
}

.greeting {
    font-size: 1.6rem; font-weight: 500; color: var(--text);
    margin-bottom: 1.5rem; text-align: center;
}

/* Input bar */
.input-bar {
    width: 100%; max-width: 640px;
    background: var(--input-bg); border-radius: var(--radius);
    display: flex; align-items: center; gap: 8px;
    padding: 12px 16px; border: 1px solid var(--border);
    transition: border-color 0.2s, box-shadow 0.2s;
}
.input-bar:focus-within {
    border-color: var(--green);
    box-shadow: 0 0 0 3px rgba(26,122,76,0.08);
}
.input-bar-plus {
    width: 28px; height: 28px; border-radius: 50%;
    background: none; border: 1.5px solid var(--text-light);
    display: flex; align-items: center; justify-content: center;
    color: var(--text-light); cursor: pointer; flex-shrink: 0;
}
.input-bar-icons {
    display: flex; align-items: center; gap: 6px; margin-left: auto;
    color: var(--text-light);
}
.input-bar-icons > * { cursor: pointer; }

/* Action chips */
.action-chips {
    display: flex; gap: 8px; margin-top: 16px;
    flex-wrap: wrap; justify-content: center;
}
.chip {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 8px 16px; border-radius: 20px;
    border: 1px solid var(--border); background: var(--bg);
    font-size: 0.82rem; color: var(--text-mid);
    cursor: pointer; transition: all 0.15s;
    font-weight: 500;
}
.chip:hover {
    border-color: var(--green); color: var(--green);
    background: var(--green-light);
}
.chip svg { color: var(--text-light); }
.chip:hover svg { color: var(--green); }

/* ── Chat/Response Area ── */
.response-card {
    width: 100%; max-width: 700px;
    background: var(--bg); border: 1px solid var(--border);
    border-radius: var(--radius-sm); padding: 1.5rem;
    margin-top: 1.5rem;
}

.review-output {
    background: var(--border-light);
    border-left: 3px solid var(--green);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    padding: 1.2rem 1.5rem;
    font-size: 0.92rem; line-height: 1.75;
    color: var(--text); margin: 1rem 0;
}

.metric-row {
    display: flex; gap: 12px; margin: 1rem 0;
}
.metric-box {
    flex: 1; text-align: center;
    padding: 12px; border-radius: 10px;
    background: var(--green-light);
}
.metric-val { font-size: 1.3rem; font-weight: 700; color: var(--green); }
.metric-lbl { font-size: 0.7rem; color: var(--text-mid); margin-top: 2px; }

/* Rec cards */
.rec-item {
    display: flex; align-items: flex-start; gap: 12px;
    padding: 12px; border-radius: 10px;
    border: 1px solid var(--border); margin-bottom: 6px;
    transition: border-color 0.15s;
}
.rec-item:hover { border-color: var(--green); }
.rec-rank {
    width: 30px; height: 30px; min-width: 30px; border-radius: 8px;
    background: var(--green); color: white;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.78rem;
}
.rec-name { font-weight: 600; font-size: 0.88rem; color: var(--text); }
.rec-cat {
    display: inline-block; padding: 1px 8px; border-radius: 4px;
    background: var(--green-badge); color: var(--green);
    font-size: 0.68rem; font-weight: 600;
}
.rec-why { font-size: 0.8rem; color: var(--text-mid); margin-top: 4px; line-height: 1.4; }

/* Streamlit overrides */
[data-testid="stTextInput"] input {
    background: transparent !important; border: none !important;
    box-shadow: none !important; padding: 0 !important;
    font-size: 0.92rem !important;
}
[data-testid="stTextInput"] > div { border: none !important; }
[data-testid="stTextInput"] label { display: none !important; }

[data-testid="stButton"] button[kind="primary"] {
    background: var(--green) !important; color: white !important;
    border: none !important; border-radius: 20px !important;
    font-weight: 600 !important; padding: 8px 20px !important;
}
[data-testid="stButton"] button[kind="primary"]:hover {
    background: var(--green-hover) !important;
}
[data-testid="stButton"] button[kind="secondary"] {
    background: transparent !important; border: 1px solid var(--border) !important;
    border-radius: 20px !important; color: var(--text-mid) !important;
}

[data-testid="stChatMessage"] {
    background: transparent !important; border: none !important;
    max-width: 700px; margin: 0 auto;
}

[data-testid="stSelectbox"] > div > div {
    border-radius: 10px !important;
}

hr { display: none !important; }

/* Radio as hidden (we use custom nav) */
[data-testid="stRadio"] { display: none !important; }
</style>
"""
