"""NaijaReview AI — Dashboard Styles (Clean Light Theme)"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #f8f9fb;
    --white: #ffffff;
    --green-primary: #1a7a4c;
    --green-dark: #145f3b;
    --green-light: #e8f5ee;
    --green-badge: #dcf5e7;
    --text-dark: #1a1d21;
    --text-mid: #4a5568;
    --text-light: #8492a6;
    --border: #e8ecf1;
    --border-light: #f0f3f7;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.04);
    --shadow-md: 0 4px 12px rgba(0,0,0,0.06);
    --radius: 12px;
    --radius-sm: 8px;
}

html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"], .main {
    background-color: var(--bg) !important;
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
}

.block-container {
    padding: 1.5rem 2rem !important;
    max-width: 1200px !important;
}

h1,h2,h3,h4,h5,h6,p,span,label,div,li,a {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 1px solid var(--border) !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] .block-container { padding: 0.5rem 1rem !important; }

/* ── Top bar ── */
.top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.8rem 0;
    margin-bottom: 0.5rem;
}
.top-bar-left h2 { margin:0; font-size:1.5rem; font-weight:700; color:var(--text-dark); }
.top-bar-left p { margin:0.2rem 0 0; color:var(--text-light); font-size:0.9rem; }
.status-pill {
    display:inline-flex; align-items:center; gap:6px;
    padding:6px 14px; border-radius:100px;
    border:1px solid var(--border);
    font-size:0.78rem; font-weight:600; color:var(--text-mid);
    background:var(--white);
}
.status-pill .dot { width:7px;height:7px;border-radius:50%;background:#22c55e; }

/* ── Task Cards ── */
.task-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.2s, border-color 0.2s;
}
.task-card:hover {
    border-color: var(--green-primary);
    box-shadow: var(--shadow-md);
}
.task-card h3 {
    margin:0 0 0.4rem; font-size:1.05rem; font-weight:700; color:var(--text-dark);
}
.task-card p { margin:0; font-size:0.85rem; color:var(--text-mid); line-height:1.5; }
.task-icon {
    width:48px; height:48px; border-radius:12px;
    display:flex; align-items:center; justify-content:center;
    font-size:1.4rem; margin-bottom:0.8rem;
}
.task-icon-a { background:var(--green-light); }
.task-icon-b { background:#fff7e6; }

/* ── Profile Card ── */
.profile-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
}
.profile-card h4 { margin:0 0 1rem; font-size:0.95rem; font-weight:700; color:var(--text-dark); }
.profile-avatar {
    width:44px; height:44px; border-radius:50%;
    background: var(--green-primary); color:white;
    display:inline-flex; align-items:center; justify-content:center;
    font-weight:700; font-size:0.9rem; margin-right:10px;
}
.profile-name { font-weight:700; font-size:0.95rem; color:var(--text-dark); }
.profile-location {
    display:inline-block; padding:2px 8px; border-radius:4px;
    background:var(--green-badge); color:var(--green-primary);
    font-size:0.7rem; font-weight:600; margin-left:6px;
}
.stat-row {
    display:flex; gap:1.5rem; margin-top:1.2rem;
    padding-top:1rem; border-top:1px solid var(--border-light);
}
.stat-item { text-align:center; flex:1; }
.stat-value { font-size:1.3rem; font-weight:700; color:var(--text-dark); }
.stat-label { font-size:0.7rem; color:var(--text-light); margin-top:2px; }

/* ── Activity Feed ── */
.activity-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
}
.activity-item {
    display:flex; align-items:center; justify-content:space-between;
    padding:0.7rem 0; border-bottom:1px solid var(--border-light);
}
.activity-item:last-child { border-bottom:none; }
.activity-text { font-size:0.85rem; color:var(--text-mid); }
.activity-time { font-size:0.75rem; color:var(--text-light); white-space:nowrap; }

/* ── Tags ── */
.tag {
    display:inline-block; padding:4px 12px; border-radius:100px;
    background:var(--green-badge); color:var(--green-primary);
    font-size:0.75rem; font-weight:600; margin:3px 4px 3px 0;
}

/* ── Chat Bar ── */
.chat-bar {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem 1.5rem;
    margin-top: 1rem;
    box-shadow: var(--shadow-sm);
}
.chat-bar h4 { margin:0; font-size:0.95rem; font-weight:700; color:var(--text-dark); }
.chat-bar p { margin:0.2rem 0 0; font-size:0.8rem; color:var(--text-light); }
.suggestion-chip {
    display:inline-block; padding:5px 14px; border-radius:100px;
    border:1px solid var(--border); background:var(--white);
    font-size:0.78rem; color:var(--text-mid); margin:4px 4px 0 0;
    cursor:pointer; transition:all 0.15s;
}
.suggestion-chip:hover { border-color:var(--green-primary); color:var(--green-primary); }

/* ── Review Output ── */
.review-output {
    background: var(--white);
    border: 1px solid var(--border);
    border-left: 3px solid var(--green-primary);
    border-radius: 0 var(--radius) var(--radius) 0;
    padding: 1.5rem;
    font-size:0.92rem; line-height:1.75;
    color: var(--text-dark);
}

/* ── Rec Card ── */
.rec-item {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 1rem 1.2rem;
    margin-bottom: 0.5rem;
    display:flex; align-items:flex-start; gap:12px;
    transition: border-color 0.15s;
}
.rec-item:hover { border-color: var(--green-primary); }
.rec-rank {
    width:32px; height:32px; min-width:32px;
    border-radius:8px; background:var(--green-primary); color:white;
    display:flex; align-items:center; justify-content:center;
    font-weight:700; font-size:0.8rem;
}
.rec-name { font-weight:600; font-size:0.9rem; color:var(--text-dark); }
.rec-cat {
    display:inline-block; padding:2px 8px; border-radius:4px;
    background:var(--green-badge); color:var(--green-primary);
    font-size:0.68rem; font-weight:600;
}
.rec-why { font-size:0.8rem; color:var(--text-mid); margin-top:4px; line-height:1.4; }

/* ── Buttons ── */
[data-testid="stButton"] button[kind="primary"] {
    background: var(--green-primary) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    padding: 0.55rem 1.5rem !important;
}
[data-testid="stButton"] button[kind="primary"]:hover {
    background: var(--green-dark) !important;
}

/* ── Inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    border-radius: var(--radius-sm) !important;
    border: 1px solid var(--border) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--green-primary) !important;
    box-shadow: 0 0 0 2px rgba(26,122,76,0.1) !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    gap: 0; border-bottom: 1px solid var(--border) !important;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 500; font-size: 0.9rem;
    color: var(--text-light) !important;
    border-bottom: 2px solid transparent !important;
    padding: 0.6rem 1.2rem !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: var(--green-primary) !important;
    border-bottom: 2px solid var(--green-primary) !important;
}

/* ── Misc ── */
hr { border-color: var(--border-light) !important; }
[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
}
[data-testid="stChatMessage"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    background: var(--white) !important;
}

/* ── Nav Items in Sidebar ── */
.nav-item {
    display:flex; align-items:center; gap:10px;
    padding:0.6rem 0.8rem; border-radius:var(--radius-sm);
    font-size:0.88rem; color:var(--text-mid); cursor:pointer;
    transition:all 0.15s; margin-bottom:2px;
}
.nav-item:hover { background:var(--green-light); color:var(--green-primary); }
.nav-active {
    background:var(--green-primary) !important;
    color:white !important; font-weight:600;
}
.nav-sub { font-size:0.72rem; color:var(--text-light); }

.section-sep { font-size:0.68rem; text-transform:uppercase; letter-spacing:0.1em;
    color:var(--text-light); font-weight:600; padding:0.8rem 0.8rem 0.3rem; }
</style>
"""
