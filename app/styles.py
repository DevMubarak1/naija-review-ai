"""NaijaReview AI — Styles (ChatGPT-inspired, white/green theme)"""

# SVG Logo for NaijaReview AI
LOGO_SVG = '''<svg width="32" height="32" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="36" height="36" rx="10" fill="#1a7a4c"/>
  <path d="M8 12 L18 8 L28 12 L28 24 L18 28 L8 24Z" fill="none" stroke="white" stroke-width="1.5" stroke-linejoin="round"/>
  <path d="M18 8 L18 28" stroke="white" stroke-width="1.2" opacity="0.4"/>
  <path d="M8 12 L28 12" stroke="white" stroke-width="1.2" opacity="0.4"/>
  <circle cx="18" cy="17" r="4" fill="white" opacity="0.9"/>
  <path d="M16 17 L17.5 18.5 L20 15.5" stroke="#1a7a4c" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="12" cy="22" r="1.5" fill="white" opacity="0.5"/>
  <circle cx="24" cy="22" r="1.5" fill="white" opacity="0.5"/>
</svg>'''

LOGO_SVG_SMALL = '''<svg width="26" height="26" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="36" height="36" rx="10" fill="#1a7a4c"/>
  <path d="M8 12 L18 8 L28 12 L28 24 L18 28 L8 24Z" fill="none" stroke="white" stroke-width="1.5" stroke-linejoin="round"/>
  <circle cx="18" cy="17" r="4" fill="white" opacity="0.9"/>
  <path d="M16 17 L17.5 18.5 L20 15.5" stroke="#1a7a4c" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''

# SVG Icons — clean, properly sized
ICON = {
    "new_chat": '<svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M9 3v12M3 9h12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    "search": '<svg width="18" height="18" viewBox="0 0 18 18" fill="none"><circle cx="8" cy="8" r="5" stroke="currentColor" stroke-width="1.6"/><path d="M12 12l3.5 3.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
    "more": '<svg width="18" height="18" viewBox="0 0 18 18" fill="none"><circle cx="4" cy="9" r="1.3" fill="currentColor"/><circle cx="9" cy="9" r="1.3" fill="currentColor"/><circle cx="14" cy="9" r="1.3" fill="currentColor"/></svg>',
    "pencil": '<svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M13 2.5l2.5 2.5L6 14.5H3.5V12L13 2.5z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><path d="M11 4.5l2.5 2.5" stroke="currentColor" stroke-width="1.5"/></svg>',
    "target": '<svg width="18" height="18" viewBox="0 0 18 18" fill="none"><circle cx="9" cy="9" r="7" stroke="currentColor" stroke-width="1.5"/><circle cx="9" cy="9" r="3.5" stroke="currentColor" stroke-width="1.5"/><circle cx="9" cy="9" r="1" fill="currentColor"/></svg>',
    "chat": '<svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M3 4h12a1 1 0 011 1v7a1 1 0 01-1 1H7l-4 3V5a1 1 0 011-1z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>',
    "settings": '<svg width="18" height="18" viewBox="0 0 18 18" fill="none"><circle cx="9" cy="9" r="2.5" stroke="currentColor" stroke-width="1.5"/><path d="M9 1.5v2M9 14.5v2M1.5 9h2M14.5 9h2M3.7 3.7l1.4 1.4M12.9 12.9l1.4 1.4M3.7 14.3l1.4-1.4M12.9 5.1l1.4-1.4" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>',
    "history": '<svg width="18" height="18" viewBox="0 0 18 18" fill="none"><circle cx="9" cy="9" r="6.5" stroke="currentColor" stroke-width="1.5"/><path d="M9 5v4l3 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "user": '<svg width="18" height="18" viewBox="0 0 18 18" fill="none"><circle cx="9" cy="6" r="3" stroke="currentColor" stroke-width="1.5"/><path d="M3 16c0-3.3 2.7-6 6-6s6 2.7 6 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
    "collapse": '<svg width="18" height="18" viewBox="0 0 18 18" fill="none"><rect x="2" y="2" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5"/><path d="M7 2v14" stroke="currentColor" stroke-width="1.5"/><path d="M10.5 7.5L13 9l-2.5 1.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    # Mode chip icons (bigger, more detailed)
    "chip_review": '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><rect x="4" y="2" width="12" height="16" rx="2" stroke="currentColor" stroke-width="1.4"/><path d="M7 6h6M7 9h6M7 12h4" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/><circle cx="14" cy="14" r="3.5" fill="white" stroke="currentColor" stroke-width="1.3"/><path d="M13 14l1 1 2-2" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "chip_recommend": '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 2l2.2 4.4 4.8.7-3.5 3.4.8 4.8L10 13l-4.3 2.3.8-4.8L3 7.1l4.8-.7L10 2z" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/></svg>',
    "chip_chat": '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M3 4h14a1 1 0 011 1v8a1 1 0 01-1 1H8l-5 4V5a1 1 0 011-1z" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/><circle cx="7" cy="9" r="1" fill="currentColor"/><circle cx="10" cy="9" r="1" fill="currentColor"/><circle cx="13" cy="9" r="1" fill="currentColor"/></svg>',
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
    --radius: 32px;
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

/* ═══ Hide ALL Streamlit chrome ═══ */
header[data-testid="stHeader"] { display: none !important; }
#MainMenu { display: none !important; }
footer { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

/* KILL the "keyboard_double_arrow_left" collapse button text */
[data-testid="stSidebar"] button[kind="header"],
[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"],
button[data-testid="stSidebarCollapse"],
[data-testid="stSidebarContent"] > div:first-child > button,
.stSidebar button[kind="headerNoPadding"],
section[data-testid="stSidebar"] > div > div > div > button {
    display: none !important;
}
/* Also hide any Material icon text that leaks */
[data-testid="stSidebar"] span.material-symbols-outlined,
[data-testid="stSidebar"] .material-icons {
    display: none !important;
}

/* ═══ Sidebar ═══ */
[data-testid="stSidebar"] {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border) !important;
    width: 260px !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] .block-container { padding: 0 !important; }
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }
[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {
    padding: 0 !important;
}

/* Sidebar inner scroll container */
section[data-testid="stSidebar"] > div {
    display: flex !important;
    flex-direction: column !important;
    height: 100vh !important;
    overflow: hidden !important;
}
section[data-testid="stSidebar"] > div > div:first-child {
    flex: 1 !important;
    overflow-y: auto !important;
    padding: 12px 12px 0 !important;
}

/* ═══ Sidebar buttons (Streamlit native) ═══ */
[data-testid="stSidebar"] [data-testid="stButton"] button {
    width: 100% !important;
    text-align: left !important;
    background: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    font-size: 0.86rem !important;
    color: var(--text-mid) !important;
    font-weight: 500 !important;
    justify-content: flex-start !important;
    transition: background 0.15s !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] button:hover {
    background: var(--green-light) !important;
    color: var(--green) !important;
}
/* Primary button in sidebar (New chat) */
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"] {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    font-weight: 600 !important;
    justify-content: center !important;
    border-radius: 20px !important;
    margin-bottom: 8px !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"]:hover {
    background: var(--green-light) !important;
    border-color: var(--green) !important;
    color: var(--green) !important;
}

/* Fixed bottom user card */
.user-card-fixed {
    position: fixed !important;
    bottom: 0; left: 0; width: 260px;
    background: var(--bg-sidebar);
    border-top: 1px solid var(--border);
    border-right: 1px solid var(--border);
    padding: 12px 16px;
    display: flex; align-items: center; gap: 10px;
    z-index: 999;
}
.user-avatar {
    width: 34px; height: 34px; border-radius: 50%;
    background: var(--green-light); color: var(--green);
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.75rem; flex-shrink: 0;
}
.user-name { font-size: 0.85rem; font-weight: 600; color: var(--text); line-height: 1.2; }
.user-plan { font-size: 0.7rem; color: var(--text-light); }

/* ═══ Main center area (ChatGPT-style) ═══ */
.main-center {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    min-height: calc(100vh - 120px);
    padding: 0 1rem;
    margin-top: -4rem;
}
.greeting {
    font-size: 1.55rem; font-weight: 500; color: var(--text);
    margin-bottom: 2rem; text-align: center;
}

/* ═══ Input bar ═══ */
[data-testid="stTextInput"] input {
    background: var(--input-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 14px 20px !important;
    font-size: 0.92rem !important;
    box-shadow: none !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--green) !important;
    box-shadow: 0 0 0 3px rgba(26,122,76,0.08) !important;
}
[data-testid="stTextInput"] > div {
    border: none !important; background: transparent !important;
}
[data-testid="stTextInput"] label { display: none !important; }

/* Chat input at bottom */
[data-testid="stChatInput"] {
    max-width: 700px !important;
    margin: 0 auto !important;
}
[data-testid="stChatInput"] textarea {
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
    background: var(--input-bg) !important;
}

/* ═══ Mode chips ═══ */
.action-chips {
    display: flex; gap: 10px; margin-top: 12px;
    flex-wrap: wrap; justify-content: center;
}
/* Override Streamlit buttons to look like chips */
.chip-row [data-testid="stButton"] button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    border-radius: 22px !important;
    color: var(--text-mid) !important;
    font-size: 0.84rem !important;
    font-weight: 500 !important;
    padding: 9px 18px !important;
    white-space: nowrap !important;
    transition: all 0.15s !important;
}
.chip-row [data-testid="stButton"] button:hover {
    border-color: var(--green) !important;
    color: var(--green) !important;
    background: var(--green-light) !important;
}

/* ═══ Top bar ═══ */
.top-bar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 10px 24px; border-bottom: 1px solid var(--border-light);
}
.top-bar-left {
    display: flex; align-items: center; gap: 8px;
    font-size: 0.92rem; font-weight: 600; color: var(--text);
}
.status-dot {
    width: 7px; height: 7px; border-radius: 50%;
    display: inline-block; margin-right: 4px;
}

/* ═══ Content cards ═══ */
.review-output {
    background: var(--border-light);
    border-left: 3px solid var(--green);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    padding: 1.2rem 1.5rem;
    font-size: 0.92rem; line-height: 1.75; color: var(--text);
    margin: 1rem 0;
}
.metric-row { display: flex; gap: 12px; margin: 1rem 0; }
.metric-box {
    flex: 1; text-align: center; padding: 14px;
    border-radius: 12px; background: var(--green-light);
}
.metric-val { font-size: 1.3rem; font-weight: 700; color: var(--green); }
.metric-lbl { font-size: 0.7rem; color: var(--text-mid); margin-top: 2px; }

.rec-item {
    display: flex; align-items: flex-start; gap: 12px;
    padding: 14px; border-radius: 12px;
    border: 1px solid var(--border); margin-bottom: 6px;
    transition: border-color 0.15s;
}
.rec-item:hover { border-color: var(--green); }
.rec-rank {
    width: 32px; height: 32px; min-width: 32px; border-radius: 8px;
    background: var(--green); color: white;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.8rem;
}
.rec-name { font-weight: 600; font-size: 0.9rem; color: var(--text); }
.rec-cat {
    display: inline-block; padding: 2px 8px; border-radius: 4px;
    background: var(--green-badge); color: var(--green);
    font-size: 0.7rem; font-weight: 600;
}
.rec-why { font-size: 0.8rem; color: var(--text-mid); margin-top: 4px; line-height: 1.4; }

/* Section header */
.section-header {
    display: flex; align-items: center; gap: 10px;
    margin: 1.5rem 0 1rem; color: var(--text);
}
.section-header svg { color: var(--green); }

/* ═══ GLOBAL button/toggle/slider green overrides ═══ */
[data-testid="stButton"] button[kind="primary"],
button[kind="primary"] {
    background: var(--green) !important; color: white !important;
    border: none !important; border-radius: 22px !important;
    font-weight: 600 !important; padding: 10px 24px !important;
}
[data-testid="stButton"] button[kind="primary"]:hover,
button[kind="primary"]:hover {
    background: var(--green-hover) !important;
}

/* Toggle switch green */
[data-testid="stToggle"] [role="checkbox"][aria-checked="true"] {
    background-color: var(--green) !important;
}
[data-testid="stToggle"] span[data-checked="true"] {
    background-color: var(--green) !important;
}
label[data-testid="stWidgetLabel"] + div [role="checkbox"][aria-checked="true"] {
    background-color: var(--green) !important;
}
div[data-baseweb="toggle"] > div:first-child {
    background-color: var(--green) !important;
}

/* Slider green */
[data-testid="stSlider"] [role="slider"] {
    background-color: var(--green) !important;
}
[data-testid="stSlider"] div[data-testid="stTickBar"] > div {
    background-color: var(--green) !important;
}
[data-baseweb="slider"] div[role="slider"] {
    background-color: var(--green) !important; border-color: var(--green) !important;
}
[data-baseweb="slider"] div[data-testid*="Track"] > div:first-child {
    background-color: var(--green) !important;
}
.stSlider > div > div > div > div {
    background-color: var(--green) !important;
}

/* ═══ Sidebar section labels ═══ */
.nav-section {
    font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.1em;
    color: var(--text-light); font-weight: 600;
    padding: 14px 12px 4px; margin-top: 4px;
}

/* ═══ Chat messages ═══ */
[data-testid="stChatMessage"] {
    max-width: 700px; margin: 0 auto;
    background: transparent !important; border: none !important;
}

/* ═══ Radio hide ═══ */
[data-testid="stRadio"] { display: none !important; }
/* Selectbox styling */
[data-testid="stSelectbox"] > div > div {
    border-radius: 10px !important;
}

/* Sidebar bottom padding so content doesn't go under fixed user card */
.sidebar-bottom-spacer { height: 70px; }

/* Preference panel */
.pref-card {
    background: var(--bg); border: 1px solid var(--border);
    border-radius: var(--radius-sm); padding: 1.5rem;
}

hr { display: none !important; }

/* Streamlit toggle internal override */
[data-testid="stCheckbox"] input:checked + div,
.st-emotion-cache-1gulkj5,
.st-emotion-cache-q16mip {
    background-color: var(--green) !important;
}

/* Number input */
[data-testid="stNumberInput"] input {
    border-radius: 10px !important;
}

/* Active sidebar button highlight */
[data-testid="stSidebar"] [data-testid="stButton"] button:active,
[data-testid="stSidebar"] [data-testid="stButton"] button:focus {
    background: var(--green-light) !important;
    color: var(--green) !important;
}
</style>
"""
