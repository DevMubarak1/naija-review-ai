"""Styles and SVG assets for the NaijaReview AI Streamlit dashboard."""

# ── Logos ──
LOGO = '<svg width="28" height="28" viewBox="0 0 36 36" fill="none"><rect width="36" height="36" rx="10" fill="#1a7a4c"/><path d="M8 12L18 8l10 4v12l-10 4-10-4Z" fill="none" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/><circle cx="18" cy="17" r="4" fill="#fff" opacity=".9"/><path d="M16 17l1.5 1.5L20 15.5" stroke="#1a7a4c" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
LOGO_SM = '<svg width="22" height="22" viewBox="0 0 36 36" fill="none"><rect width="36" height="36" rx="10" fill="#1a7a4c"/><circle cx="18" cy="17" r="4" fill="#fff" opacity=".9"/><path d="M16 17l1.5 1.5L20 15.5" stroke="#1a7a4c" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# ── Chat avatars ──
AV_USER = '<svg width="28" height="28" viewBox="0 0 28 28"><rect width="28" height="28" rx="8" fill="#e8f5ee"/><circle cx="14" cy="10" r="4.5" fill="#1a7a4c"/><path d="M5 24c0-5 4-9 9-9s9 4 9 9" fill="#1a7a4c"/></svg>'
AV_AI = '<svg width="28" height="28" viewBox="0 0 28 28"><rect width="28" height="28" rx="8" fill="#1a7a4c"/><circle cx="14" cy="12" r="3.5" fill="#fff" opacity=".9"/><path d="M12 12l1.2 1.2L15 11" stroke="#1a7a4c" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"/><rect x="8" y="19" width="12" height="2" rx="1" fill="#fff" opacity=".4"/></svg>'
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
    "refresh": _ic('<path d="M23 4v6h-6M1 20v-6h6"/><path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15"/>'),
    "send": _ic('<path d="M22 2L11 13M22 2l-7 20-4-9-9-4z"/>'),
    "user": _ic('<path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/>'),
    "zap": _ic('<path d="M13 2L3 14h9l-1 10 10-12h-9l1-10z"/>'),
    "menu": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1a7a4c" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>',
}


def nav_html(icon_key, label, active=False):
    """Single HTML nav item with inline SVG + label."""
    bg = "background:#e8f5ee;color:#1a7a4c;" if active else ""
    ic_color = "color:#1a7a4c;" if active else "color:#6b7280;"
    fw = "font-weight:600;" if active else "font-weight:500;"
    return f'''<div style="display:flex;align-items:center;gap:10px;padding:8px 14px;
        border-radius:10px;{bg}transition:all .15s ease;cursor:pointer;">
        <span style="flex-shrink:0;display:flex;align-items:center;{ic_color}">{IC[icon_key]}</span>
        <span style="font-size:0.84rem;{fw}color:{'#1a7a4c' if active else '#374151'};">{label}</span>
    </div>'''


# ── Suggestion pill data ──
SUGGESTIONS = [
    {"icon": ":material/rate_review:", "color": "#1a7a4c", "label": "Generate a product review", "mode": "review"},
    {"icon": ":material/recommend:", "color": "#e67e22", "label": "Get recommendations for me", "mode": "recommend"},
    {"icon": ":material/forum:", "color": "#3b82f6", "label": "Chat about reviews & products", "mode": "chat"},
    {"icon": ":material/language:", "color": "#9b59b6", "label": "Try Nigerian Pidgin mode", "mode": "chat"},
]


# ── Sparkle SVG for hero ──
SPARKLE_SVG = """
<svg width="64" height="64" viewBox="0 0 24 24" fill="none" class="sparkle-star" style="filter: drop-shadow(0 0 12px rgba(46, 204, 113, 0.45));">
  <path d="M12 2Q12 12 22 12Q12 12 12 22Q12 12 2 12Q12 12 12 2Z" fill="url(#sparkle-grad)"/>
  <defs>
    <linearGradient id="sparkle-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2ecc71" />
      <stop offset="100%" stop-color="#1a7a4c" />
    </linearGradient>
  </defs>
</svg>
"""


# ── Home-specific scoped CSS ──
HOMEPAGE_CSS = """
<style>
/* Suggestion cards styling */
.main div:has(.suggestion-anchor) ~ [data-testid="stHorizontalBlock"] [data-testid="stButton"] button,
.main div:has(.suggestion-anchor) ~ div [data-testid="stHorizontalBlock"] [data-testid="stButton"] button {
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    text-align: left !important;
    background-color: #ffffff !important;
    border: 1.5px solid #e5e7eb !important;
    border-radius: 16px !important;
    padding: 20px 24px !important;
    min-height: 84px !important;
    height: auto !important;
    width: 100% !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
}

/* Enforce button text wraps correctly and has consistent spacing */
.main div:has(.suggestion-anchor) ~ [data-testid="stHorizontalBlock"] [data-testid="stButton"] button p,
.main div:has(.suggestion-anchor) ~ div [data-testid="stButton"] button p {
    color: #1f2937 !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    margin: 0 !important;
    white-space: normal !important;
    word-break: break-word !important;
    line-height: 1.45 !important;
}

/* Large and styled icons */
.main div:has(.suggestion-anchor) ~ [data-testid="stHorizontalBlock"] [data-testid="stButton"] button span[data-testid="stWidgetIcon"],
.main div:has(.suggestion-anchor) ~ div [data-testid="stButton"] button span[data-testid="stWidgetIcon"] {
    font-size: 1.6rem !important;
    margin-right: 14px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0 !important;
}

/* Align items inside the input row vertically centered */
.main div:has(.search-bar-anchor) + [data-testid="stHorizontalBlock"],
.main div:has(.search-bar-anchor) + div > [data-testid="stHorizontalBlock"] {
    align-items: center !important;
}

/* Homepage Send Button Styling */
.main div:has(.search-bar-anchor) + [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(2) [data-testid="stButton"] button,
.main div:has(.search-bar-anchor) + div > [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(2) [data-testid="stButton"] button {
    background-color: var(--green) !important;
    border: none !important;
    border-radius: 24px !important;
    height: 48px !important;
    min-height: 48px !important;
    width: 48px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin: 0 auto !important;
    padding: 0 !important;
    color: #ffffff !important;
    box-shadow: var(--shadow-sm) !important;
    transition: var(--transition) !important;
}

.main div:has(.search-bar-anchor) + [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(2) [data-testid="stButton"] button:hover,
.main div:has(.search-bar-anchor) + div > [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(2) [data-testid="stButton"] button:hover {
    background-color: var(--green-hover) !important;
    transform: scale(1.05) !important;
    box-shadow: 0 4px 10px rgba(26,122,76,.2) !important;
}

.main div:has(.search-bar-anchor) + [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(2) [data-testid="stButton"] button p,
.main div:has(.search-bar-anchor) + div > [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(2) [data-testid="stButton"] button p {
    display: none !important;
}

.main div:has(.search-bar-anchor) + [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(2) [data-testid="stButton"] button span[data-testid="stWidgetIcon"],
.main div:has(.search-bar-anchor) + div > [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(2) [data-testid="stButton"] button span[data-testid="stWidgetIcon"] {
    color: #ffffff !important;
    font-size: 1.4rem !important;
    margin-right: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* Individual card hover states and color coordination */
/* Card 1: Review (Green) */
.main div:has(.suggestion-anchor) + [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(1) [data-testid="stButton"] button span[data-testid="stWidgetIcon"],
.main div:has(.suggestion-anchor) + div > [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(1) [data-testid="stButton"] button span[data-testid="stWidgetIcon"] {
    color: #1a7a4c !important;
}
.main div:has(.suggestion-anchor) + [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(1) [data-testid="stButton"] button:hover,
.main div:has(.suggestion-anchor) + div > [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(1) [data-testid="stButton"] button:hover {
    border-color: #1a7a4c !important;
    background-color: #f4fbf7 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 15px -3px rgba(26, 122, 76, 0.1), 0 4px 6px -2px rgba(26, 122, 76, 0.05) !important;
}

/* Card 2: Recommend (Orange) */
.main div:has(.suggestion-anchor) + [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(2) [data-testid="stButton"] button span[data-testid="stWidgetIcon"],
.main div:has(.suggestion-anchor) + div > [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(2) [data-testid="stButton"] button span[data-testid="stWidgetIcon"] {
    color: #e67e22 !important;
}
.main div:has(.suggestion-anchor) + [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(2) [data-testid="stButton"] button:hover,
.main div:has(.suggestion-anchor) + div > [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(2) [data-testid="stButton"] button:hover {
    border-color: #e67e22 !important;
    background-color: #fef8f3 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 15px -3px rgba(230, 126, 34, 0.1), 0 4px 6px -2px rgba(230, 126, 34, 0.05) !important;
}

/* Card 3: Chat (Blue) */
.main div:has(.suggestion-anchor) + [data-testid="stHorizontalBlock"] + [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(1) [data-testid="stButton"] button span[data-testid="stWidgetIcon"],
.main div:has(.suggestion-anchor) + div > [data-testid="stHorizontalBlock"] + div > [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(1) [data-testid="stButton"] button span[data-testid="stWidgetIcon"] {
    color: #3b82f6 !important;
}
.main div:has(.suggestion-anchor) + [data-testid="stHorizontalBlock"] + [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(1) [data-testid="stButton"] button:hover,
.main div:has(.suggestion-anchor) + div > [data-testid="stHorizontalBlock"] + div > [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(1) [data-testid="stButton"] button:hover {
    border-color: #3b82f6 !important;
    background-color: #f4f8ff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.1), 0 4px 6px -2px rgba(59, 130, 246, 0.05) !important;
}

/* Card 4: Pidgin (Purple) */
.main div:has(.suggestion-anchor) + [data-testid="stHorizontalBlock"] + [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(2) [data-testid="stButton"] button span[data-testid="stWidgetIcon"],
.main div:has(.suggestion-anchor) + div > [data-testid="stHorizontalBlock"] + div > [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(2) [data-testid="stButton"] button span[data-testid="stWidgetIcon"] {
    color: #9b59b6 !important;
}
.main div:has(.suggestion-anchor) + [data-testid="stHorizontalBlock"] + [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(2) [data-testid="stButton"] button:hover,
.main div:has(.suggestion-anchor) + div > [data-testid="stHorizontalBlock"] + div > [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(2) [data-testid="stButton"] button:hover {
    border-color: #9b59b6 !important;
    background-color: #faf5fc !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 15px -3px rgba(155, 89, 182, 0.1), 0 4px 6px -2px rgba(155, 89, 182, 0.05) !important;
}

/* Floating animation for hero sparkle */
@keyframes float {
    0% { transform: translateY(0px) rotate(0deg) scale(1); }
    50% { transform: translateY(-8px) rotate(8deg) scale(1.05); }
    100% { transform: translateY(0px) rotate(0deg) scale(1); }
}
.hero-icon svg {
    animation: float 4s ease-in-out infinite;
}

/* Mobile responsive layout overrides */
@media (max-width: 768px) {
    /* Keep homepage search row side-by-side on mobile */
    .main div:has(.search-bar-anchor) + [data-testid="stHorizontalBlock"],
    .main div:has(.search-bar-anchor) + div > [data-testid="stHorizontalBlock"] {
        flex-direction: row !important;
        align-items: center !important;
        gap: 8px !important;
    }
    .main div:has(.search-bar-anchor) + [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-of-type(1),
    .main div:has(.search-bar-anchor) + div > [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-of-type(1) {
        width: calc(100% - 52px) !important;
        min-width: calc(100% - 52px) !important;
        max-width: calc(100% - 52px) !important;
        flex: 0 0 calc(100% - 52px) !important;
    }
    .main div:has(.search-bar-anchor) + [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-of-type(2),
    .main div:has(.search-bar-anchor) + div > [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-of-type(2) {
        width: 44px !important;
        min-width: 44px !important;
        max-width: 44px !important;
        flex: 0 0 44px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    .main div:has(.search-bar-anchor) + [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(2) [data-testid="stButton"] button,
    .main div:has(.search-bar-anchor) + div > [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(2) [data-testid="stButton"] button {
        height: 44px !important;
        min-height: 44px !important;
        width: 44px !important;
        border-radius: 22px !important;
    }

    /* Stack suggestion columns vertically on mobile */
    .main div:has(.suggestion-anchor) + [data-testid="stHorizontalBlock"],
    .main div:has(.suggestion-anchor) + div > [data-testid="stHorizontalBlock"],
    .main div:has(.suggestion-anchor) + [data-testid="stHorizontalBlock"] + [data-testid="stHorizontalBlock"],
    .main div:has(.suggestion-anchor) + div > [data-testid="stHorizontalBlock"] + div > [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
        gap: 12px !important;
    }
    .main div:has(.suggestion-anchor) ~ [data-testid="stHorizontalBlock"] [data-testid="column"],
    .main div:has(.suggestion-anchor) ~ div [data-testid="stHorizontalBlock"] [data-testid="column"] {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 100% !important;
    }
    .main div:has(.suggestion-anchor) ~ [data-testid="stHorizontalBlock"] [data-testid="column"] [data-testid="stButton"] button,
    .main div:has(.suggestion-anchor) ~ div [data-testid="stHorizontalBlock"] [data-testid="column"] [data-testid="stButton"] button {
        min-height: 72px !important;
        padding: 16px 20px !important;
    }
}
</style>
"""""


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ═══════════════════════════════════════════
   CSS VARIABLES
   ═══════════════════════════════════════════ */
:root{
    --bg: #ffffff;
    --bg2: #f8f9fa;
    --bg3: #f3f4f6;
    --green: #1a7a4c;
    --green-hover: #15633e;
    --green-light: #e8f5ee;
    --green-lighter: #dcf5e7;
    --green-glow: rgba(26,122,76,.08);
    --text: #111827;
    --text-mid: #4b5563;
    --text-light: #9ca3af;
    --border: #e5e7eb;
    --border-light: #f3f4f6;
    --radius: 32px;
    --radius-sm: 12px;
    --radius-md: 16px;
    --shadow-sm: 0 1px 3px rgba(0,0,0,.04);
    --shadow-md: 0 2px 8px rgba(0,0,0,.06);
    --shadow-green: 0 2px 8px rgba(26,122,76,.12);
    --transition: all .2s ease;
}

/* ═══════════════════════════════════════════
   BASE & RESET
   ═══════════════════════════════════════════ */
html,body,[data-testid="stAppViewContainer"],[data-testid="stApp"],.main{
    background:var(--bg)!important;
    font-family:'Inter',system-ui,-apple-system,sans-serif!important;
    padding-top:0!important;margin-top:0!important;
}
.block-container{padding:0!important;max-width:100%!important;}
*{-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;}

/* ═══════════════════════════════════════════
   HIDE STREAMLIT CHROME
   ═══════════════════════════════════════════ */
header[data-testid="stHeader"],[data-testid="stToolbar"],
[data-testid="stDecoration"],footer,#MainMenu{display:none!important;height:0!important;}
[data-testid="stRadio"]{display:none!important;}
hr{display:none!important;}

/* ═══════════════════════════════════════════
   SIDEBAR — COLLAPSE / EXPAND BUTTONS
   ═══════════════════════════════════════════ */
[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"]{
    display:flex!important;position:absolute!important;top:10px;right:10px;z-index:2000000!important;
    margin-top:0!important;padding:0!important;
}
[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button{
    background:transparent!important;border:none!important;color:var(--text-light)!important;
    padding:4px!important;min-height:0!important;width:28px!important;height:28px!important;
    border-radius:8px!important;opacity:1!important;position:relative!important;margin-top:0!important;
}
[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button:hover{
    background:var(--bg3)!important;color:var(--text)!important;
}
[data-testid="collapsedControl"]{display:flex!important;position:fixed!important;top:12px;left:12px;z-index:2000001!important;transform:none!important;}
[data-testid="collapsedControl"] button{
    background:var(--bg)!important;border:1px solid var(--border)!important;color:var(--green)!important;
    padding:6px!important;border-radius:10px!important;box-shadow:var(--shadow-md)!important;
    min-height:0!important;width:36px!important;height:36px!important;
    display:flex!important;align-items:center!important;justify-content:center!important;
}
[data-testid="collapsedControl"] button:hover{background:var(--green-light)!important;border-color:var(--green)!important;}
[data-testid="stExpandSidebarButton"],[data-testid="stExpandSidebarButton"] button{
    position:fixed!important;left:12px!important;top:12px!important;z-index:2000002!important;display:flex!important;
    width:36px!important;height:36px!important;padding:6px!important;
    align-items:center!important;justify-content:center!important;
    background:var(--bg)!important;border:1px solid var(--border)!important;
    border-radius:10px!important;box-shadow:var(--shadow-md)!important;color:var(--green)!important;
}

/* ═══════════════════════════════════════════
   SIDEBAR — BODY
   ═══════════════════════════════════════════ */
[data-testid="stSidebar"]{
    background:var(--bg2)!important;border-right:1px solid var(--border)!important;
    width:280px!important;padding:0!important;
    transition:margin-left .25s ease,transform .25s ease!important;
}
[data-testid="stSidebarUserContent"],[data-testid="stSidebarContent"],
[data-testid="stSidebar"]>div,[data-testid="stSidebar"]>div>div,
[data-testid="stSidebar"]>div:first-child,
section[data-testid="stSidebar"]>div>div,
section[data-testid="stSidebar"]>div>div>div{
    padding-top:0!important;margin-top:0!important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"]{padding:0!important;margin:0!important;}
[data-testid="stSidebar"] .stVerticalBlock{gap:0!important;}
section[data-testid="stSidebar"]>div{height:100vh!important;overflow-y:auto!important;padding:0 12px 90px!important;}
section[data-testid="stSidebar"]{padding-top:0!important;margin-top:0!important}

/* Sidebar logo */
.sidebar-logo{
    position:sticky!important;top:0;z-index:100000!important;
    background:var(--bg2);padding:16px 14px 14px;
    display:flex;align-items:center;gap:10px;
    border-bottom:1px solid var(--border);margin-top:0!important;margin-bottom:6px!important;
}
.sidebar-logo span{font-size:.92rem;font-weight:700;color:var(--text);}
.status-dot{width:8px;height:8px;border-radius:50%;margin-left:auto;flex-shrink:0;}

/* New Chat button */
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"]{
    opacity:1!important;height:auto!important;position:relative!important;margin-top:0!important;
    background:transparent!important;border:1.5px solid var(--border)!important;color:var(--text)!important;
    font-weight:600!important;border-radius:22px!important;padding:10px 18px!important;
    justify-content:center!important;font-size:.84rem!important;
    transition:var(--transition)!important;
}
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"]:hover{
    background:var(--green-light)!important;border-color:var(--green)!important;color:var(--green)!important;
}

/* Sidebar nav buttons — invisible overlay technique */
[data-testid="stSidebar"] [data-testid="stButton"]{margin:0!important;padding:0!important;}
[data-testid="stSidebar"] [data-testid="stButton"] button{
    width:100%!important;background:transparent!important;border:none!important;
    padding:0!important;margin:0!important;min-height:0!important;height:34px!important;
    opacity:0!important;cursor:pointer!important;position:relative!important;
    margin-top:-34px!important;z-index:2!important;
}

/* Section headers */
.nav-sec{
    font-size:.65rem;text-transform:uppercase;letter-spacing:.12em;
    color:var(--text-light);font-weight:600;padding:22px 14px 8px;margin:0;
}

/* Fixed user card */
.user-card{
    position:fixed!important;bottom:0;left:0;width:280px;
    background:var(--bg2);border-top:1px solid var(--border);border-right:1px solid var(--border);
    padding:14px 16px;display:flex;align-items:center;gap:10px;z-index:999;
}
.user-av{
    width:36px;height:36px;border-radius:50%;background:var(--green-light);color:var(--green);
    display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.78rem;flex-shrink:0;
}
.user-nm{font-size:.84rem;font-weight:600;color:var(--text);line-height:1.3;}
.user-pl{font-size:.68rem;color:var(--text-light);}

/* Delete button in recents */
.del-btn{
    display:flex;align-items:center;justify-content:center;width:24px;height:24px;
    border-radius:6px;cursor:pointer;color:var(--text-light);transition:var(--transition);
    margin-top:5px;
}
.del-btn:hover{background:#fef2f2;color:#ef4444;}

/* ═══════════════════════════════════════════
   HERO — LANDING PAGE
   ═══════════════════════════════════════════ */
.hero-spacer{height:16vh;}
.hero-section{
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    padding: 0 20px !important;
    width: 100% !important;
}
.hero-icon{font-size:4rem;line-height:1;margin-bottom:8px;color:var(--green);}
.hero-title{
    font-size:1.8rem;font-weight:700;color:var(--text);margin:0 0 8px;line-height:1.3;
    text-align:center !important;
}
.hero-sub, .hero-section p{
    font-size:.92rem !important;color:var(--text-mid) !important;line-height:1.6 !important;
    max-width:500px !important;margin:0 auto 28px !important;
    text-align:center !important;
}


/* Powered-by footer */
.powered-by{text-align:center;font-size:.72rem;color:var(--text-light);padding:10px 0;margin-top:12px;}
.powered-by a{color:var(--green);text-decoration:none;font-weight:500;}

/* ═══════════════════════════════════════════
   TOP BAR
   ═══════════════════════════════════════════ */
.top-bar{
    display:flex;align-items:center;justify-content:space-between;
    padding:14px 28px;border-bottom:1px solid var(--border-light);background:var(--bg);
}
.top-bar-l{display:flex;align-items:center;gap:10px;font-size:.92rem;font-weight:600;color:var(--text);}
.mode-indicator{display:flex;align-items:center;gap:6px;font-size:.78rem;font-weight:500;}
.dot{width:7px;height:7px;border-radius:50%;display:inline-block;}

/* Mode pill badge */
.mode-pill{
    display:inline-flex;align-items:center;gap:6px;padding:6px 16px;
    border-radius:20px;background:var(--green-light);color:var(--green);font-size:.78rem;
    font-weight:600;margin:12px 0 0 28px;
}

/* ═══════════════════════════════════════════
   FORM CONTAINER
   ═══════════════════════════════════════════ */
.form-container{padding:8px 0 24px;}

/* ═══════════════════════════════════════════
   TEXT INPUT — PILL STYLE
   ═══════════════════════════════════════════ */
[data-testid="stTextInput"] input{
    background:var(--bg3)!important;border:1.5px solid var(--border)!important;
    border-radius:var(--radius)!important;padding:14px 22px!important;font-size:.92rem!important;
    box-shadow:var(--shadow-sm)!important;transition:var(--transition)!important;
    color:var(--text)!important;
}
[data-testid="stTextInput"] input:focus{
    border-color:var(--green)!important;box-shadow:0 0 0 3px var(--green-glow)!important;
    background:var(--bg)!important;
}
[data-testid="stTextInput"]>div{border:none!important;background:transparent!important;}
[data-testid="stTextInput"] label{display:none!important;}

/* Text area */
[data-testid="stTextArea"] textarea{
    background:var(--bg3)!important;border:1.5px solid var(--border)!important;
    border-radius:var(--radius-sm)!important;padding:14px 18px!important;font-size:.88rem!important;
    transition:var(--transition)!important;
}
[data-testid="stTextArea"] textarea:focus{
    border-color:var(--green)!important;box-shadow:0 0 0 3px var(--green-glow)!important;
}
[data-testid="stTextArea"] label{color:var(--text-mid)!important;font-weight:500!important;font-size:.82rem!important;}

/* Select box */
[data-testid="stSelectbox"] label{color:var(--text-mid)!important;font-weight:500!important;font-size:.82rem!important;}
[data-testid="stSelectbox"]>div>div{
    border-radius:var(--radius-sm)!important;border-color:var(--border)!important;
}

/* ═══════════════════════════════════════════
   GREEN PRIMARY BUTTONS
   ═══════════════════════════════════════════ */
.main [data-testid="stButton"] button[kind="primary"]{
    background:var(--green)!important;color:#fff!important;border:none!important;
    border-radius:22px!important;font-weight:600!important;padding:11px 24px!important;
    opacity:1!important;height:auto!important;position:relative!important;margin-top:0!important;
    box-shadow:var(--shadow-green)!important;transition:var(--transition)!important;
    font-size:.88rem!important;letter-spacing:.01em!important;
}
.main [data-testid="stButton"] button[kind="primary"]:hover{
    background:var(--green-hover)!important;
    box-shadow:0 4px 14px rgba(26,122,76,.2)!important;
    transform:translateY(-1px)!important;
}
.main [data-testid="stButton"] button{
    opacity:1!important;height:auto!important;position:relative!important;margin-top:0!important;
}

/* ═══════════════════════════════════════════
   RESULT CARDS — METRICS
   ═══════════════════════════════════════════ */
.metric-row{display:flex;gap:14px;margin:1rem 0;}
.metric-card{
    flex:1;text-align:center;padding:20px 16px;border-radius:var(--radius-md);
    background:var(--green-light);border:1px solid var(--green-lighter);
    transition:var(--transition);
}
.metric-card:hover{transform:translateY(-2px);box-shadow:var(--shadow-green);}
.metric-val{font-size:1.4rem;font-weight:700;color:var(--green);}
.metric-lbl{font-size:.72rem;color:var(--text-mid);margin-top:4px;font-weight:500;text-transform:uppercase;letter-spacing:.04em;}

/* Review box */
.review-box{
    background:var(--bg3);border-left:4px solid var(--green);
    border-radius:0 var(--radius-sm) var(--radius-sm) 0;
    padding:1.4rem 1.8rem;font-size:.92rem;line-height:1.8;color:var(--text);margin:1rem 0;
    font-style:italic;position:relative;
}
.review-quote{
    font-size:2rem;color:var(--green);opacity:.3;position:absolute;top:8px;left:12px;
    font-style:normal;line-height:1;
}

/* ═══════════════════════════════════════════
   RECOMMENDATION CARDS
   ═══════════════════════════════════════════ */
.results-header{
    display:flex;align-items:center;gap:8px;padding:4px 0 12px;
    font-size:.82rem;color:var(--text-light);font-weight:500;
}
.rec-card{
    display:flex;align-items:flex-start;gap:14px;padding:18px;border-radius:var(--radius-md);
    border:1.5px solid var(--border);margin-bottom:10px;
    transition:var(--transition);background:var(--bg);
}
.rec-card:hover{border-color:var(--green);box-shadow:0 4px 16px rgba(26,122,76,.06);transform:translateY(-1px);}
.rec-rank{
    width:36px;height:36px;min-width:36px;border-radius:10px;background:var(--green);
    color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.84rem;
    flex-shrink:0;
}
.rec-body{flex:1;min-width:0;}
.rec-header{display:flex;align-items:center;gap:10px;flex-wrap:wrap;}
.rec-name{font-weight:600;font-size:.92rem;color:var(--text);}
.rec-cat{
    display:inline-block;padding:2px 10px;border-radius:6px;background:var(--green-lighter);
    color:var(--green);font-size:.7rem;font-weight:600;
}
.rec-desc{font-size:.82rem;color:var(--text-mid);margin-top:6px;line-height:1.6;}

/* ═══════════════════════════════════════════
   CHAT MESSAGES
   ═══════════════════════════════════════════ */
[data-testid="stChatMessage"]{
    max-width:800px;
    margin:0 auto;
    background:transparent!important;
    border:none!important;
    padding:6px 0!important;
}
[data-testid="stChatMessage"] [data-testid="stChatMessageAvatarCustom"],
[data-testid="stChatMessage"] [data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessage"] [data-testid="stChatMessageAvatarAssistant"],
[data-testid="stChatMessage"]>div:first-child>div:first-child{display:none!important;}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}

.chat-msg {
    display: flex;
    gap: 12px;
    align-items: flex-end; /* Align avatars with the bottom of the bubbles for a standard chat feel */
    margin-bottom: 8px;
    width: 100%;
    animation: slideUp 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.msg-user {
    flex-direction: row-reverse;
    justify-content: flex-start;
}

.msg-ai {
    flex-direction: row;
    justify-content: flex-start;
}

.chat-avatar {
    flex-shrink: 0;
    margin-bottom: 2px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    box-shadow: var(--shadow-sm);
    transition: var(--transition);
}

.chat-avatar:hover {
    transform: scale(1.08);
}

.chat-text {
    font-size: 0.92rem;
    line-height: 1.6;
    padding: 12px 18px;
    border-radius: 18px;
    max-width: 78%;
    box-shadow: var(--shadow-sm);
    word-break: break-word;
}
.chat-text p {
    margin: 0 0 8px 0 !important;
}
.chat-text p:last-child {
    margin-bottom: 0 !important;
}
.chat-text ul, .chat-text ol {
    margin: 4px 0 !important;
    padding-left: 20px !important;
}
.chat-text li {
    margin-bottom: 4px !important;
}
.chat-text a {
    color: var(--green) !important;
    text-decoration: underline !important;
    font-weight: 500 !important;
}
.msg-user .chat-text a {
    color: var(--green-hover) !important;
}

.msg-user .chat-text {
    background-color: var(--green-light);
    color: var(--green-hover);
    border: 1.5px solid var(--green-lighter);
    border-bottom-right-radius: 4px;
}

.msg-ai .chat-text {
    background-color: #f3f4f6;
    color: var(--text);
    border: 1.5px solid var(--border);
    border-bottom-left-radius: 4px;
}

.chat-thinking {
    padding: 12px 18px;
    border-radius: 18px;
    border-bottom-left-radius: 4px;
    background-color: #f3f4f6;
    border: 1.5px solid var(--border);
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: var(--text-mid);
    font-size: 0.88rem;
    box-shadow: var(--shadow-sm);
}

.thinking-dots {
    display: flex;
    gap: 4px;
    align-items: center;
}

.thinking-dots span {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--green);
    opacity: 0.4;
    animation: dotPulse 1.4s infinite ease-in-out;
}

.thinking-dots span:nth-child(2) { animation-delay: 0.2s; }
.thinking-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes dotPulse {
    0%, 80%, 100% { opacity: 0.4; transform: scale(1); }
    40% { opacity: 1; transform: scale(1.2); }
}

/* Chat empty state */
.chat-empty{text-align:center;padding:60px 20px;color:var(--text-light);}
.chat-empty-icon{font-size:3rem;margin-bottom:12px;opacity:.5;}
.chat-empty-title{font-size:1.1rem;font-weight:600;color:var(--text-mid);margin-bottom:6px;}
.chat-empty-sub{font-size:.85rem;max-width:360px;margin:0 auto;line-height:1.5;}

/* Chat input — premium capsule */
[data-testid="stChatInput"]{max-width:740px!important;margin:0 auto!important;padding:0 16px 16px!important;}
[data-testid="stChatInput"] textarea{
    border-radius:24px!important;border:1.5px solid var(--border)!important;
    background:var(--bg)!important;font-size:.9rem!important;
    padding:13px 20px!important;min-height:44px!important;
    box-shadow:var(--shadow-sm)!important;
    transition:var(--transition)!important;
}
[data-testid="stChatInput"] textarea:focus{
    border-color:var(--green)!important;box-shadow:0 0 0 3px var(--green-glow)!important;
}
[data-testid="stChatInput"]>div{border:none!important;background:transparent!important;border-radius:24px!important;}
[data-testid="stChatInput"] button{
    background:var(--green)!important;color:#fff!important;border:none!important;
    border-radius:50%!important;width:34px!important;height:34px!important;min-width:34px!important;
    transition:var(--transition)!important;
}
[data-testid="stChatInput"] button:hover{background:var(--green-hover)!important;}
[data-testid="stBottom"]{background:var(--bg)!important;border-top:1px solid var(--border-light)!important;}
[data-testid="stBottomBlockContainer"]{padding:0!important;max-width:100%!important;}

/* ═══════════════════════════════════════════
   PREFERENCES PAGE
   ═══════════════════════════════════════════ */
.pref-header{
    display:flex;align-items:center;gap:10px;margin:1.5rem 0 .5rem;
    color:var(--text);font-size:1.1rem;font-weight:600;
}
.pref-section{
    font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;
    color:var(--text-light);font-weight:600;margin:24px 0 8px;padding-bottom:4px;
    border-bottom:1px solid var(--border-light);
}

/* ═══════════════════════════════════════════
   EXPANDER
   ═══════════════════════════════════════════ */
[data-testid="stExpander"]{
    border:1px solid var(--border)!important;border-radius:var(--radius-sm)!important;
    overflow:hidden;
}
[data-testid="stExpander"] summary{
    padding:12px 16px!important;font-size:.88rem!important;font-weight:500!important;
}

/* ═══════════════════════════════════════════
   MOBILE RESPONSIVE — TABLET
   ═══════════════════════════════════════════ */
@media(max-width:768px){
    [data-testid="stSidebar"]{width:260px!important;}
    .user-card{width:260px;}

    [data-testid="stChatInput"]{max-width:100%!important;padding:0 10px 12px!important;}
    [data-testid="stChatMessage"]{max-width:100%!important;padding:2px 4px!important;}

    .chat-text{
        max-width:86%!important;
        font-size:0.88rem!important;
        padding:10px 14px!important;
    }
    .chat-msg{
        gap:8px!important;
    }

    .hero-spacer{height:10vh;}
    .hero-icon{font-size:3rem;}
    .hero-title{font-size:1.4rem;}
    .hero-sub{font-size:.84rem;padding:0 12px;}


    .main [data-testid="stHorizontalBlock"]{
        flex-direction:column!important;gap:8px!important;
    }

    .top-bar{padding:10px 14px;}
    .top-bar-l span{font-size:.84rem;}
    .mode-pill{margin:6px 0 0 14px;font-size:.72rem;}

    .metric-row{flex-direction:row;gap:8px;}
    .metric-card{padding:14px 10px;}
    .metric-val{font-size:1.1rem;}
    .rec-card{padding:14px;}
    .rec-rank{width:30px;height:30px;min-width:30px;font-size:.76rem;}
    .review-box{padding:1rem 1.2rem;font-size:.86rem;}

    [data-testid="stTextInput"] input{padding:12px 16px!important;font-size:.86rem!important;}
}

/* ═══════════════════════════════════════════
   MOBILE RESPONSIVE — PHONE
   ═══════════════════════════════════════════ */
@media(max-width:480px){
    .hero-spacer{height:6vh;}
    .hero-icon{font-size:2.5rem;}
    .hero-title{font-size:1.15rem;}
    .hero-sub{font-size:.78rem;}
    .metric-row{flex-direction:column;gap:6px;}
    .metric-card{padding:10px;}

    .top-bar-l span{display:none;}
    .rec-card{flex-direction:column;gap:10px;}
    .chat-text{font-size:.84rem;}
}
</style>
"""
