"""
Ming Qimen 明奇门 - Dashboard v3.5
Fixed with correct page file names
"""

import streamlit as st
from datetime import datetime, timedelta, timezone
import sys
import os

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

SGT = timezone(timedelta(hours=8))

def get_singapore_time():
    return datetime.now(SGT)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0a0a1a 0%, #1a1a2e 100%);
    }
    h1, h2, h3 {
        color: #FFD700 !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d20 0%, #1a1a30 100%);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================

if 'selected_palace' not in st.session_state:
    st.session_state.selected_palace = 5
if 'current_chart' not in st.session_state:
    st.session_state.current_chart = None
if 'analyses' not in st.session_state:
    st.session_state.analyses = []
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}
if 'bazi_calculated' not in st.session_state:
    st.session_state.bazi_calculated = None
if 'birth_year' not in st.session_state:
    st.session_state.birth_year = 1990
if 'birth_month' not in st.session_state:
    st.session_state.birth_month = 1
if 'birth_day' not in st.session_state:
    st.session_state.birth_day = 1
if 'birth_hour' not in st.session_state:
    st.session_state.birth_hour = 12
if 'birth_minute' not in st.session_state:
    st.session_state.birth_minute = 0

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    now = get_singapore_time()
    ch_char, ch_pinyin, ch_animal = get_chinese_hour(now.hour)
    
    st.markdown(f"**{ch_char}時** ({ch_pinyin} - {ch_animal})")
    st.markdown("---")
    
    st.markdown("### 📍 Navigation")
    
    # CORRECT PAGE NAMES matching your GitHub repo:
    # 1_Chart.py, 2_Export.py, 3_History.py, 4_Settings.py, 5_Help.py, 6_BaZi.py
    
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
    
    # BaZi Profile Display
    if st.session_state.user_profile.get('day_master'):
        profile = st.session_state.user_profile
        st.markdown("### 👤 Your BaZi")
        
        dm = profile.get('day_master', 'Not set')
        element = profile.get('element', '')
        
        element_colors = {
            'Wood': '#4CAF50', 'Fire': '#F44336', 
            'Earth': '#FF9800', 'Metal': '#9E9E9E', 'Water': '#2196F3'
        }
        elem_color = element_colors.get(element, '#888')
        
        st.markdown(f"**Day Master:** <span style='color:{elem_color};font-weight:bold'>{dm}</span>", unsafe_allow_html=True)
        st.markdown(f"**Element:** {element} ({profile.get('polarity', '')})")
        st.markdown(f"**Strength:** {profile.get('strength', '')}")
        
        useful = profile.get('useful_gods', [])
        if useful:
            st.markdown(f"**Helpful:** ✅ {', '.join(useful)}")
        
        unfav = profile.get('unfavorable', [])
        if unfav:
            st.markdown(f"**Avoid:** ❌ {', '.join(unfav)}")
        
        profile_type = profile.get('profile', '')
        if profile_type:
            short_profile = profile_type[:25] + "..." if len(profile_type) > 25 else profile_type
            st.markdown(f"**Type:** {short_profile}")
        
        if profile.get('wealth_vault'):
            st.markdown("💰 **Wealth Vault**")
        if profile.get('nobleman'):
            st.markdown("👑 **Nobleman**")
    else:
        st.markdown("### 👤 Profile")
        st.caption("No BaZi profile set")
        if st.button("🎂 Calculate BaZi", use_container_width=True, key="sidebar_bazi"):
            st.switch_page("pages/4_Settings.py")

# ============================================================================
# MAIN CONTENT
# ============================================================================

st.markdown("# 🌟 Ming Qimen 明奇门")
st.markdown("### *Clarity for the People*")
st.markdown("*Ancient Wisdom, Made Bright and Simple*")
st.markdown("---")

st.markdown("## ✨ Current Energy")

now = get_singapore_time()

with st.spinner("Reading the cosmic energy..."):
    summaries = get_all_palaces_summary(now, method=1)

if summaries:
    best = summaries[0]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### ⭐ Best Topic Right Now")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%); 
                    border: 3px solid #FFD700; border-radius: 15px; padding: 25px;">
            <div style="font-size: 3em; text-align: center;">{best['icon']}</div>
            <div style="font-size: 1.8em; text-align: center; color: #FFD700; font-weight: bold; margin: 10px 0;">
                {best['topic']}
            </div>
            <div style="text-align: center; font-size: 1.2em; color: #90CAF9;">
                Palace {best['palace']} ({best['name']})
            </div>
            <div style="text-align: center; margin-top: 15px;">
                <span style="background: #FFD700; color: #000; padding: 8px 20px; border-radius: 20px; font-weight: bold;">
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
    
    # TOPIC GRID
    st.markdown("## 🎯 All Topics Overview")
    st.caption("Click on a topic to get detailed guidance")
    
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            idx = row * 3 + col
            if idx < len(summaries):
                s = summaries[idx]
                
                with cols[col]:
                    if s['score'] >= 7:
                        border_color = "#4CAF50"
                    elif s['score'] >= 5:
                        border_color = "#2196F3"
                    elif s['score'] >= 3:
                        border_color = "#FF9800"
                    else:
                        border_color = "#F44336"
                    
                    rank_badge = ""
                    if idx == 0:
                        rank_badge = "⭐ BEST"
                    elif idx == 1:
                        rank_badge = "🥈 2nd"
                    elif idx == 2:
                        rank_badge = "🥉 3rd"
                    
                    st.markdown(
                        f'<div style="background: rgba(30, 30, 50, 0.8); '
                        f'border: 2px solid {border_color}; border-radius: 12px; '
                        f'padding: 15px; margin: 5px 0; min-height: 160px; text-align: center;">'
                        f'<div style="text-align: right; font-size: 0.7em; color: {border_color}; height: 18px;">{rank_badge}</div>'
                        f'<div style="font-size: 2em;">{s["icon"]}</div>'
                        f'<div style="color: #FFD700; font-weight: bold; font-size: 1.1em;">{s["topic"]}</div>'
                        f'<div style="color: #888; font-size: 0.8em;">Palace {s["palace"]}</div>'
                        f'<div style="margin-top: 10px;">'
                        f'<span style="background: {border_color}; color: #fff; padding: 3px 12px; border-radius: 15px; font-size: 0.9em;">'
                        f'{s["score"]}/10</span></div>'
                        f'<div style="color: #666; font-size: 0.75em; margin-top: 8px;">{s["door"]} + {s["star"]}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                    
                    if st.button(f"Analyze {s['topic']}", key=f"btn_{s['palace']}", use_container_width=True):
                        st.session_state.selected_palace = s['palace']
                        st.switch_page("pages/1_Chart.py")

# QUICK ACTIONS
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

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.85em;">
    🌟 <strong>Ming Qimen 明奇门</strong> v3.5 | <em>Clarity for the People</em>
</div>
""", unsafe_allow_html=True)
