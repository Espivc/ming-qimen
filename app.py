"""
Ming Qimen 明奇门 - Main Dashboard
Version: 4.0
"Clarity for the People"

Features:
- Current cosmic energy display
- Quick navigation
- Streamlined BaZi profile in sidebar (single location)
"""

import streamlit as st
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Ming Qimen 明奇门",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    /* Main title */
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        color: #888;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Cards */
    .energy-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 2px solid #FFD700;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .nav-card {
        background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .nav-card:hover {
        border-color: #FFD700;
        transform: translateY(-2px);
    }
    
    /* Sidebar profile */
    .sidebar-profile {
        background: linear-gradient(135deg, #1a472a 0%, #0d2818 100%);
        border: 1px solid #2ecc71;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .sidebar-profile-empty {
        background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
        border: 1px solid #555;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Element badges */
    .element-badge {
        display: inline-block;
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        margin: 0.1rem;
    }
    .wood { background: #228B22; color: white; }
    .fire { background: #DC143C; color: white; }
    .earth { background: #DAA520; color: black; }
    .metal { background: #C0C0C0; color: black; }
    .water { background: #4169E1; color: white; }
    
    /* Time display */
    .time-display {
        font-size: 1.5rem;
        color: #FFD700;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR - Single BaZi Profile Location
# ============================================================
with st.sidebar:
    st.markdown("## 🌟 Ming Qimen")
    st.caption("明奇门 • Clarity for the People")
    
    st.markdown("---")
    
    # BaZi Profile Display (THE ONLY PLACE it shows)
    st.markdown("### 👤 Your Profile")
    
    if st.session_state.get("user_profile"):
        profile = st.session_state.user_profile
        
        st.markdown(f"""
        <div class="sidebar-profile">
            <strong style="color: #FFD700; font-size: 1.1rem;">{profile.get('day_master', 'Unknown')}</strong><br>
            <span style="color: #9B59B6;">{profile.get('polarity', '')} {profile.get('element', '')}</span><br>
            <span style="color: {'#2ecc71' if profile.get('strength') == 'Strong' else '#e74c3c' if profile.get('strength') == 'Weak' else '#f39c12'};">
                {profile.get('strength', '')} ({profile.get('strength_score', 'N/A')}/10)
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Useful Gods (compact display)
        useful = profile.get('useful_gods', [])
        if useful:
            st.markdown("**Useful:**")
            badges_html = " ".join([f'<span class="element-badge {g.lower()}">{g}</span>' for g in useful])
            st.markdown(badges_html, unsafe_allow_html=True)
        
        # Special structures (compact)
        structures = []
        if profile.get('wealth_vault'):
            structures.append("💰 Vault")
        if profile.get('nobleman'):
            structures.append("👑 Noble")
        if structures:
            st.caption(" • ".join(structures))
        
        # Edit link
        if st.button("✏️ Edit Profile", use_container_width=True, key="sidebar_edit"):
            st.switch_page("pages/6_BaZi.py")
    
    else:
        st.markdown("""
        <div class="sidebar-profile-empty">
            <span style="color: #888;">No BaZi profile set</span><br>
            <span style="color: #666; font-size: 0.85rem;">Calculate your Four Pillars</span>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔮 Set Up BaZi", type="primary", use_container_width=True, key="sidebar_setup"):
            st.switch_page("pages/6_BaZi.py")
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("### 📊 Quick Stats")
    charts_generated = st.session_state.get("charts_count", 0)
    st.metric("Charts Generated", charts_generated)
    
    # Current Time
    now = datetime.now()
    st.caption(f"🕐 {now.strftime('%H:%M')} • {now.strftime('%Y-%m-%d')}")

# ============================================================
# MAIN CONTENT
# ============================================================

st.markdown('<h1 class="main-title">🌟 Ming Qimen 明奇门</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Qi Men Dun Jia Analysis System • 奇门遁甲分析系统</p>', unsafe_allow_html=True)

# Current cosmic energy card
now = datetime.now()
hour_str = now.strftime("%H:%M")
date_str = now.strftime("%A, %B %d, %Y")

st.markdown(f"""
<div class="energy-card">
    <div style="color: #888; font-size: 1rem;">CURRENT COSMIC ENERGY</div>
    <div class="time-display">{hour_str}</div>
    <div style="color: #666;">{date_str}</div>
    <div style="margin-top: 1rem; color: #FFD700;">
        Generate a chart to see today's formation →
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# Quick navigation cards
st.subheader("🚀 Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="nav-card">
        <div style="font-size: 2rem;">📊</div>
        <div style="color: #FFD700; font-weight: bold;">Chart</div>
        <div style="color: #666; font-size: 0.85rem;">Generate QMDJ reading</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Chart →", key="nav_chart", use_container_width=True):
        st.switch_page("pages/1_Chart.py")

with col2:
    st.markdown("""
    <div class="nav-card">
        <div style="font-size: 2rem;">📤</div>
        <div style="color: #FFD700; font-weight: bold;">Export</div>
        <div style="color: #666; font-size: 0.85rem;">Download JSON data</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Export →", key="nav_export", use_container_width=True):
        st.switch_page("pages/2_Export.py")

with col3:
    st.markdown("""
    <div class="nav-card">
        <div style="font-size: 2rem;">🎂</div>
        <div style="color: #FFD700; font-weight: bold;">BaZi</div>
        <div style="color: #666; font-size: 0.85rem;">Calculate Four Pillars</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open BaZi →", key="nav_bazi", use_container_width=True):
        st.switch_page("pages/6_BaZi.py")

st.markdown("")

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="nav-card">
        <div style="font-size: 2rem;">📜</div>
        <div style="color: #FFD700; font-weight: bold;">History</div>
        <div style="color: #666; font-size: 0.85rem;">Past readings</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open History →", key="nav_history", use_container_width=True):
        st.switch_page("pages/3_History.py")

with col5:
    st.markdown("""
    <div class="nav-card">
        <div style="font-size: 2rem;">⚙️</div>
        <div style="color: #FFD700; font-weight: bold;">Settings</div>
        <div style="color: #666; font-size: 0.85rem;">Configure app</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Settings →", key="nav_settings", use_container_width=True):
        st.switch_page("pages/4_Settings.py")

with col6:
    st.markdown("""
    <div class="nav-card">
        <div style="font-size: 2rem;">❓</div>
        <div style="color: #FFD700; font-weight: bold;">Help</div>
        <div style="color: #666; font-size: 0.85rem;">Learn QMDJ</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Help →", key="nav_help", use_container_width=True):
        st.switch_page("pages/5_Help.py")

# ============================================================
# INFO SECTION
# ============================================================
st.markdown("---")

with st.expander("ℹ️ About Ming Qimen"):
    st.markdown("""
    **Ming Qimen 明奇门** is a professional Qi Men Dun Jia analysis system designed for:
    
    - 📊 **Accurate QMDJ Charts** - Using Chai Bu (拆補) method via kinqimen library
    - 🎂 **BaZi Integration** - Four Pillars calculation and cross-reference
    - 📤 **Data Export** - Universal Schema v2.0 JSON for AI analysis
    - 📱 **Mobile Friendly** - Works on desktop and iPhone
    
    **Developer Engine (Project 2)** - Generates structured data for the Analyst Engine (Project 1)
    
    *Version 4.0 • Built with Streamlit*
    """)

# Footer
st.caption("🌟 Ming Qimen 明奇门 | Developer Engine v4.0 | Universal Schema v2.0")
