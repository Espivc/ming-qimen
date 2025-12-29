"""
Ming Qimen 明奇门 - Dashboard v2.0
Phase 4: Real QMDJ calculations with kinqimen integration

"Clarity for the People" - Ancient Wisdom, Made Bright and Simple
"""

import streamlit as st
from datetime import datetime, timedelta, timezone
import sys
import os

# Add core module to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.qmdj_engine import (
    generate_qmdj_reading,
    get_all_palaces_summary,
    PALACE_INFO,
    PALACE_TOPICS,
    get_chinese_hour
)

st.set_page_config(
    page_title="Ming Qimen 明奇门",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Singapore timezone
SGT = timezone(timedelta(hours=8))

def get_singapore_time():
    return datetime.now(SGT)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    /* Dark theme base */
    .stApp {
        background: linear-gradient(180deg, #0a0a1a 0%, #1a1a2e 100%);
    }
    
    /* Gold accent headers */
    h1, h2, h3 {
        color: #FFD700 !important;
    }
    
    /* Card styling */
    .palace-card {
        background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
        border: 1px solid #FFD700;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
    }
    
    .palace-card.recommended {
        border: 3px solid #FFD700;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
    }
    
    /* Score badge */
    .score-badge {
        background: #FFD700;
        color: #000;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
    }
    
    /* Topic grid */
    .topic-button {
        background: #1e1e2e;
        border: 1px solid #444;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        transition: all 0.3s;
    }
    
    .topic-button:hover {
        border-color: #FFD700;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'shared_date' not in st.session_state:
    st.session_state.shared_date = get_singapore_time().date()

if 'shared_time' not in st.session_state:
    st.session_state.shared_time = get_singapore_time().strftime("%H:%M")

if 'selected_palace' not in st.session_state:
    st.session_state.selected_palace = 5

if 'current_chart' not in st.session_state:
    st.session_state.current_chart = None

if 'analyses' not in st.session_state:
    st.session_state.analyses = []

if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("## 🌟 Ming Qimen")
    st.markdown("*明奇门 - Clarity for the People*")
    
    st.markdown("---")
    
    # Current time display
    now = get_singapore_time()
    ch_char, ch_pinyin, ch_animal = get_chinese_hour(now.hour)
    
    st.markdown("### 🕐 Current Time")
    st.markdown(f"**{now.strftime('%Y-%m-%d %H:%M')}** SGT")
    st.markdown(f"**{ch_char}時** ({ch_pinyin} - {ch_animal})")
    
    st.markdown("---")
    
    # Quick navigation
    st.markdown("### 📍 Navigation")
    
    if st.button("📊 Generate Chart", use_container_width=True):
        st.switch_page("pages/1_Chart.py")
    
    if st.button("📤 Export Reading", use_container_width=True):
        st.switch_page("pages/2_Export.py")
    
    if st.button("📜 History", use_container_width=True):
        st.switch_page("pages/3_History.py")
    
    if st.button("⚙️ Settings", use_container_width=True):
        st.switch_page("pages/4_Settings.py")
    
    if st.button("❓ Help & Guide", use_container_width=True):
        st.switch_page("pages/5_Help.py")
    
    st.markdown("---")
    
    # User profile summary
    if st.session_state.user_profile.get('day_master'):
        profile = st.session_state.user_profile
        st.markdown("### 👤 Your Profile")
        st.markdown(f"**Day Master:** {profile.get('day_master', 'Not set')}")
        st.markdown(f"**Strength:** {profile.get('strength', 'Not set')}")
        
        useful = profile.get('useful_gods', [])
        if useful:
            st.markdown(f"**Helpful Elements:** {', '.join(useful)}")

# ============================================================================
# MAIN CONTENT
# ============================================================================

# Header
st.markdown("# 🌟 Ming Qimen 明奇门")
st.markdown("### *Clarity for the People*")
st.markdown("*Ancient Wisdom, Made Bright and Simple*")

st.markdown("---")

# ============================================================================
# CURRENT ENERGY OVERVIEW
# ============================================================================

st.markdown("## ✨ Current Energy")

now = get_singapore_time()

# Get all palace summaries
with st.spinner("Reading the cosmic energy..."):
    summaries = get_all_palaces_summary(now, method=1)

if summaries:
    # Top recommendation
    best = summaries[0]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### ⭐ Best Topic Right Now")
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%); 
                    border: 3px solid #FFD700; 
                    border-radius: 15px; 
                    padding: 25px; 
                    box-shadow: 0 0 30px rgba(255, 215, 0, 0.2);">
            <div style="font-size: 3em; text-align: center;">{best['icon']}</div>
            <div style="font-size: 1.8em; text-align: center; color: #FFD700; font-weight: bold; margin: 10px 0;">
                {best['topic']}
            </div>
            <div style="text-align: center; font-size: 1.2em; color: #90CAF9;">
                Palace {best['palace']} ({best['name']})
            </div>
            <div style="text-align: center; margin-top: 15px;">
                <span style="background: #FFD700; color: #000; padding: 8px 20px; border-radius: 20px; font-weight: bold; font-size: 1.1em;">
                    Score: {best['score']}/10 - {best['verdict']}
                </span>
            </div>
            <div style="text-align: center; margin-top: 15px; color: #aaa;">
                {best['door']} Door + {best['star']} Star
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Quick Stats")
        
        favorable = len([s for s in summaries if s['score'] >= 6])
        neutral = len([s for s in summaries if 4 <= s['score'] < 6])
        challenging = len([s for s in summaries if s['score'] < 4])
        
        st.metric("✅ Favorable Topics", f"{favorable}/9")
        st.metric("😐 Neutral Topics", f"{neutral}/9")
        st.metric("⚠️ Challenging Topics", f"{challenging}/9")
        
        st.markdown("---")
        
        st.markdown(f"**Time:** {now.strftime('%H:%M')} SGT")
        st.markdown(f"**Chinese Hour:** {ch_char}時")
    
    st.markdown("---")
    
    # ============================================================================
    # TOPIC GRID
    # ============================================================================
    
    st.markdown("## 🎯 All Topics Overview")
    st.caption("Click on a topic to get detailed guidance")
    
    # Create 3x3 grid
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            idx = row * 3 + col
            if idx < len(summaries):
                s = summaries[idx]
                
                with cols[col]:
                    # Determine styling based on score
                    if s['score'] >= 7:
                        border_color = "#4CAF50"
                        bg_alpha = "0.2"
                    elif s['score'] >= 5:
                        border_color = "#2196F3"
                        bg_alpha = "0.15"
                    elif s['score'] >= 3:
                        border_color = "#FF9800"
                        bg_alpha = "0.1"
                    else:
                        border_color = "#F44336"
                        bg_alpha = "0.1"
                    
                    rank_badge = ""
                    if idx == 0:
                        rank_badge = "⭐ BEST"
                    elif idx == 1:
                        rank_badge = "🥈 2nd"
                    elif idx == 2:
                        rank_badge = "🥉 3rd"
                    
                    st.markdown(f"""
                    <div style="background: rgba(30, 30, 50, 0.8); 
                                border: 2px solid {border_color}; 
                                border-radius: 12px; 
                                padding: 15px; 
                                margin: 5px 0;
                                min-height: 160px;">
                        <div style="text-align: right; font-size: 0.7em; color: {border_color};">
                            {rank_badge}
                        </div>
                        <div style="font-size: 2em; text-align: center;">{s['icon']}</div>
                        <div style="text-align: center; color: #FFD700; font-weight: bold; font-size: 1.1em;">
                            {s['topic']}
                        </div>
                        <div style="text-align: center; color: #888; font-size: 0.8em;">
                            Palace {s['palace']}
                        </div>
                        <div style="text-align: center; margin-top: 10px;">
                            <span style="background: {border_color}; color: #fff; padding: 3px 12px; border-radius: 15px; font-size: 0.9em;">
                                {s['score']}/10
                            </span>
                        </div>
                        <div style="text-align: center; color: #666; font-size: 0.75em; margin-top: 8px;">
                            {s['door']} + {s['star']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Analyze {s['topic']}", key=f"btn_{s['palace']}", use_container_width=True):
                        st.session_state.selected_palace = s['palace']
                        st.switch_page("pages/1_Chart.py")

# ============================================================================
# QUICK ACTIONS
# ============================================================================

st.markdown("---")
st.markdown("## 🚀 Quick Actions")

action_cols = st.columns(4)

with action_cols[0]:
    if st.button("📊 Full Chart Analysis", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Chart.py")

with action_cols[1]:
    if st.button("💼 Career Reading", use_container_width=True):
        st.session_state.selected_palace = 1
        st.switch_page("pages/1_Chart.py")

with action_cols[2]:
    if st.button("💰 Wealth Reading", use_container_width=True):
        st.session_state.selected_palace = 4
        st.switch_page("pages/1_Chart.py")

with action_cols[3]:
    if st.button("💕 Relationship Reading", use_container_width=True):
        st.session_state.selected_palace = 2
        st.switch_page("pages/1_Chart.py")

# ============================================================================
# ABOUT SECTION
# ============================================================================

st.markdown("---")

with st.expander("ℹ️ About Ming Qimen"):
    st.markdown("""
    ### 🌟 Ming Qimen 明奇门
    
    **"Clarity for the People"** - Ancient Wisdom, Made Bright and Simple
    
    ---
    
    #### Our Mission
    
    I created Ming Qimen because I believe wisdom shouldn't come with a price tag or a headache.
    
    My name is **Beng (明)**, which means **'Brightness'**. My goal is to use that light to clear 
    the fog of ancient calculations. Too many apps are built for experts; this one is built for **you**.
    
    **No paywalls. No complex data entry. Just clear guidance to help you find your way, for free.**
    
    ---
    
    #### What is Qi Men Dun Jia?
    
    Qi Men Dun Jia (奇門遁甲) is one of the most powerful ancient Chinese divination systems.
    Dating back over 4,000 years, it was originally used by emperors and military strategists 
    to time important decisions.
    
    Today, we use it for:
    - 💼 **Career** - Job changes, business decisions
    - 💰 **Wealth** - Investments, financial timing
    - 💕 **Relationships** - Love, partnerships
    - 💪 **Health** - Wellness timing
    - 🎯 **Personal** - Daily guidance
    
    ---
    
    #### How It Works
    
    1. **Select a Topic** - What do you need guidance on?
    2. **Choose a Time** - Current time or a specific moment
    3. **Get Your Reading** - We calculate the cosmic energy pattern
    4. **Receive Guidance** - Clear, actionable advice
    
    ---
    
    *"Guiding you first, because your peace of mind matters."*
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.85em;">
    🌟 <strong>Ming Qimen 明奇门</strong> v2.0 | Phase 4 - Real QMDJ Calculations<br>
    Singapore Time (UTC+8) | <em>Clarity for the People</em>
</div>
""", unsafe_allow_html=True)
