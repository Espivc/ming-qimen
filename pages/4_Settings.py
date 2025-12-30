"""
Ming Qimen 明奇门 - Settings Page v4.0
Fixed to work with existing BaZi calculator
"""

import streamlit as st
from datetime import datetime, timedelta, timezone, date
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="Settings | Ming Qimen",
    page_icon="⚙️",
    layout="wide"
)

SGT = timezone(timedelta(hours=8))

st.title("⚙️ Settings 设置")

# ============================================================================
# SESSION STATE
# ============================================================================

if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

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
# TABS
# ============================================================================

tab1, tab2, tab3 = st.tabs(["🎂 BaZi Profile", "👤 Manual Profile", "🎨 Preferences"])

# ============================================================================
# TAB 1: BAZI PROFILE - Links to 6_BaZi.py
# ============================================================================

with tab1:
    st.markdown("### 🎂 Your BaZi Profile")
    
    # Check if profile exists
    if st.session_state.user_profile.get('day_master'):
        profile = st.session_state.user_profile
        
        st.success("✅ BaZi profile is set!")
        
        # Display current profile
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Day Master 日主")
            dm = profile.get('day_master', 'Not set')
            element = profile.get('element', '')
            
            element_colors = {
                'Wood': '#4CAF50', 'Fire': '#F44336', 
                'Earth': '#FF9800', 'Metal': '#9E9E9E', 'Water': '#2196F3'
            }
            elem_color = element_colors.get(element, '#888')
            
            st.markdown(f"<span style='font-size:2em;color:{elem_color};font-weight:bold'>{dm}</span>", unsafe_allow_html=True)
            st.markdown(f"**Element:** {element} ({profile.get('polarity', '')})")
            st.markdown(f"**Strength:** {profile.get('strength', 'Not set')}")
        
        with col2:
            st.markdown("#### Useful Gods 用神")
            useful = profile.get('useful_gods', [])
            if useful:
                for elem in useful:
                    st.markdown(f"✅ **{elem}**")
            else:
                st.caption("Not set")
            
            st.markdown("#### Unfavorable")
            unfav = profile.get('unfavorable', [])
            if unfav:
                for elem in unfav:
                    st.markdown(f"❌ {elem}")
            else:
                st.caption("Not set")
        
        with col3:
            st.markdown("#### Profile Type 命格")
            profile_type = profile.get('profile', 'Not set')
            st.markdown(f"**{profile_type}**")
            
            st.markdown("#### Special Structures")
            if profile.get('wealth_vault'):
                st.markdown("💰 **Wealth Vault**")
            if profile.get('nobleman'):
                st.markdown("👑 **Nobleman**")
            if not profile.get('wealth_vault') and not profile.get('nobleman'):
                st.caption("None detected")
        
        st.markdown("---")
        
        # Button to recalculate
        if st.button("🔄 Recalculate BaZi", use_container_width=True):
            st.switch_page("pages/6_BaZi.py")
        
        # Button to clear profile
        if st.button("🗑️ Clear Profile", use_container_width=True):
            st.session_state.user_profile = {}
            st.rerun()
    
    else:
        st.info("No BaZi profile set yet. Use the BaZi Calculator to calculate your Four Pillars.")
        
        st.markdown("---")
        
        if st.button("🔮 Go to BaZi Calculator", use_container_width=True, type="primary"):
            st.switch_page("pages/6_BaZi.py")
        
        st.markdown("---")
        st.markdown("#### Or enter manually below")
        st.caption("If you already know your BaZi, use the Manual Profile tab →")

# ============================================================================
# TAB 2: MANUAL PROFILE
# ============================================================================

with tab2:
    st.markdown("### 👤 Manual BaZi Profile")
    st.markdown("If you already know your BaZi, enter it manually here.")
    
    profile = st.session_state.user_profile
    
    HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    STEMS_PINYIN = ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]
    
    PROFILE_TYPES = {
        "Friend": "Networker",
        "Rob Wealth": "Competitor",
        "Eating God": "Philosopher",
        "Hurting Officer": "Artist",
        "Indirect Wealth": "Pioneer",
        "Direct Wealth": "Leader",
        "7 Killings": "Warrior",
        "Direct Officer": "Director",
        "Indirect Resource": "Strategist",
        "Direct Resource": "Diplomat"
    }
    
    with st.form("bazi_form"):
        st.markdown("#### Day Master 日主")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            day_masters = [''] + [f"{STEMS_PINYIN[i]} {HEAVENLY_STEMS[i]}" for i in range(10)]
            current_dm = profile.get('day_master', '')
            dm_idx = day_masters.index(current_dm) if current_dm in day_masters else 0
            
            day_master = st.selectbox(
                "Day Master Stem",
                options=day_masters,
                index=dm_idx
            )
        
        with col2:
            strengths = ['', 'Extremely Strong', 'Strong', 'Balanced', 'Weak', 'Extremely Weak']
            current_str = profile.get('strength', '')
            str_idx = strengths.index(current_str) if current_str in strengths else 0
            
            strength = st.selectbox(
                "Day Master Strength",
                options=strengths,
                index=str_idx
            )
        
        with col3:
            profiles = [''] + [f"{v} ({k})" for k, v in PROFILE_TYPES.items()]
            
            profile_type = st.selectbox(
                "10 God Profile",
                options=profiles
            )
        
        st.markdown("#### Helpful Elements 用神")
        
        ug_col1, ug_col2 = st.columns(2)
        
        with ug_col1:
            useful_gods = st.multiselect(
                "Favorable Elements",
                options=['Wood', 'Fire', 'Earth', 'Metal', 'Water'],
                default=profile.get('useful_gods', [])
            )
        
        with ug_col2:
            unfavorable = st.multiselect(
                "Unfavorable Elements",
                options=['Wood', 'Fire', 'Earth', 'Metal', 'Water'],
                default=profile.get('unfavorable', [])
            )
        
        st.markdown("#### Special Structures 特殊格局")
        
        struct_col1, struct_col2 = st.columns(2)
        
        with struct_col1:
            wealth_vault = st.checkbox(
                "Wealth Vault Present 财库",
                value=profile.get('wealth_vault', False)
            )
        
        with struct_col2:
            nobleman = st.checkbox(
                "Nobleman Present 贵人",
                value=profile.get('nobleman', False)
            )
        
        submitted = st.form_submit_button("💾 Save Profile", use_container_width=True, type="primary")
        
        if submitted:
            dm_element_map = {
                'Jia': 'Wood', 'Yi': 'Wood',
                'Bing': 'Fire', 'Ding': 'Fire',
                'Wu': 'Earth', 'Ji': 'Earth',
                'Geng': 'Metal', 'Xin': 'Metal',
                'Ren': 'Water', 'Gui': 'Water'
            }
            
            dm_element = ''
            dm_polarity = ''
            if day_master:
                dm_name = day_master.split()[0]
                dm_element = dm_element_map.get(dm_name, '')
                dm_polarity = 'Yang' if dm_name in ['Jia', 'Bing', 'Wu', 'Geng', 'Ren'] else 'Yin'
            
            st.session_state.user_profile = {
                'day_master': day_master,
                'element': dm_element,
                'polarity': dm_polarity,
                'strength': strength,
                'profile': profile_type,
                'useful_gods': useful_gods,
                'unfavorable': unfavorable,
                'wealth_vault': wealth_vault,
                'nobleman': nobleman
            }
            
            st.success("✅ Profile saved!")
            st.rerun()
    
    # Quick preset
    st.markdown("---")
    with st.expander("🎯 Quick Presets"):
        if st.button("Load Geng Metal Pioneer (Ben's Profile)", use_container_width=True):
            st.session_state.user_profile = {
                'day_master': 'Geng 庚',
                'element': 'Metal',
                'polarity': 'Yang',
                'strength': 'Weak',
                'strength_score': 4,
                'profile': 'Pioneer (Indirect Wealth)',
                'dominant_god': 'Indirect Wealth',
                'useful_gods': ['Earth', 'Metal'],
                'unfavorable': ['Fire'],
                'wealth_vault': True,
                'nobleman': False
            }
            st.success("✅ Geng Metal Pioneer profile loaded!")
            st.rerun()

# ============================================================================
# TAB 3: PREFERENCES
# ============================================================================

with tab3:
    st.markdown("### 🎨 Display Preferences")
    
    st.markdown("#### Language")
    lang = st.radio(
        "Display Language",
        options=["English with Chinese", "English Only", "Chinese Only"],
        index=0
    )
    
    st.markdown("#### Terminology")
    terminology = st.radio(
        "Door Names",
        options=["Friendly (Stillness, Surprise)", "Traditional (Death, Fear)"],
        index=0
    )
    
    st.markdown("#### Calculation Method")
    default_method = st.radio(
        "Default QMDJ Method",
        options=["Chai Bu 拆補 (Recommended)", "Zhi Run 置閏"],
        index=0
    )
    
    st.info("ℹ️ Preferences will be applied in future updates.")

# Footer
st.markdown("---")
st.caption("🌟 Ming Qimen 明奇门 | Settings v4.0")
