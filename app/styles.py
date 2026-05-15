"""
NaijaReview AI — Premium Dashboard Styles
Dark luxe aesthetic with Nigerian-inspired gold accents.
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: #0a0e1a;
    --bg-secondary: #111827;
    --bg-card: #1a2035;
    --bg-card-hover: #1f2847;
    --gold: #d4a843;
    --gold-dim: #b8922e;
    --gold-glow: rgba(212,168,67,0.15);
    --green-accent: #10b981;
    --green-dim: rgba(16,185,129,0.12);
    --red-accent: #ef4444;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --border: rgba(255,255,255,0.06);
    --border-gold: rgba(212,168,67,0.25);
}

html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"], .main, .block-container {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1629 0%, #0a0e1a 100%) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text-secondary) !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Playfair Display', serif !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.02em;
}

p, span, label, div {
    font-family: 'DM Sans', sans-serif !important;
}

code, pre, [data-testid="stCode"] {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Hero header */
.hero-banner {
    background: linear-gradient(135deg, #0f1629 0%, #1a1f3a 40%, #0d1520 100%);
    border: 1px solid var(--border-gold);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, var(--gold-glow) 0%, transparent 70%);
    pointer-events: none;
}

.hero-banner h1 {
    font-size: 2.4rem !important;
    background: linear-gradient(135deg, var(--gold) 0%, #f5d98a 50%, var(--gold-dim) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 !important;
    line-height: 1.2;
}

.hero-subtitle {
    color: var(--text-secondary) !important;
    font-size: 1.05rem;
    margin-top: 0.5rem;
    font-weight: 300;
    letter-spacing: 0.03em;
}

.hero-team {
    display: inline-block;
    margin-top: 1rem;
    padding: 0.35rem 1rem;
    border: 1px solid var(--border-gold);
    border-radius: 100px;
    font-size: 0.75rem;
    color: var(--gold) !important;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 600;
}

/* Cards */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
    position: relative;
    overflow: hidden;
}

.metric-card:hover {
    border-color: var(--border-gold);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

.metric-card .metric-value {
    font-family: 'Playfair Display', serif !important;
    font-size: 2rem;
    font-weight: 700;
    color: var(--gold) !important;
    line-height: 1;
}

.metric-card .metric-label {
    font-size: 0.78rem;
    color: var(--text-muted) !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.4rem;
    font-weight: 500;
}

/* Review output */
.review-block {
    background: var(--bg-card);
    border-left: 3px solid var(--gold);
    border-radius: 0 14px 14px 0;
    padding: 1.8rem 2rem;
    margin: 1.5rem 0;
    font-size: 1.02rem;
    line-height: 1.85;
    color: var(--text-primary) !important;
    position: relative;
}

.review-block::before {
    content: '"';
    position: absolute;
    top: 0.5rem;
    left: 1rem;
    font-size: 3.5rem;
    font-family: 'Playfair Display', serif;
    color: var(--gold-glow);
    line-height: 1;
}

/* Recommendation cards */
.rec-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    margin: 0.6rem 0;
    transition: all 0.25s ease;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
}

.rec-card:hover {
    border-color: var(--border-gold);
    background: var(--bg-card-hover);
}

.rec-rank {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    min-width: 36px;
    border-radius: 10px;
    background: linear-gradient(135deg, var(--gold) 0%, var(--gold-dim) 100%);
    color: #0a0e1a !important;
    font-weight: 700;
    font-size: 0.85rem;
    font-family: 'DM Sans', sans-serif;
}

.rec-name {
    font-weight: 600;
    color: var(--text-primary) !important;
    font-size: 0.95rem;
}

.rec-category {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 6px;
    font-size: 0.68rem;
    background: var(--gold-glow);
    color: var(--gold) !important;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.rec-explanation {
    color: var(--text-secondary) !important;
    font-size: 0.85rem;
    margin-top: 0.4rem;
    line-height: 1.5;
}

/* Status badges */
.status-online {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.3rem 0.8rem;
    border-radius: 100px;
    background: var(--green-dim);
    color: var(--green-accent) !important;
    font-size: 0.75rem;
    font-weight: 600;
}

.status-online::before {
    content: '';
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--green-accent);
    animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* Inputs */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px var(--gold-glow) !important;
}

/* Buttons */
[data-testid="stButton"] button[kind="primary"],
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--gold) 0%, var(--gold-dim) 100%) !important;
    color: #0a0e1a !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    letter-spacing: 0.02em;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.3s ease !important;
}

[data-testid="stButton"] button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(212,168,67,0.3) !important;
}

/* Tabs */
[data-testid="stTabs"] [role="tablist"] {
    background: var(--bg-secondary) !important;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid var(--border) !important;
}

[data-testid="stTabs"] [role="tab"] {
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500;
    color: var(--text-muted) !important;
    padding: 0.5rem 1.2rem !important;
}

[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: var(--bg-card) !important;
    color: var(--gold) !important;
    border-bottom: none !important;
}

/* Dividers */
hr {
    border-color: var(--border) !important;
}

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
    color: var(--text-primary) !important;
}

/* Toggle */
[data-testid="stToggle"] label span {
    color: var(--text-secondary) !important;
}

/* Expander */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
}

/* Spinner */
[data-testid="stSpinner"] {
    color: var(--gold) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* Section labels */
.section-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--text-muted) !important;
    font-weight: 600;
    margin-bottom: 0.8rem;
    padding-left: 2px;
}
</style>
"""
