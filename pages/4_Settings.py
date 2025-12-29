"""
Ming Qimen 明奇门 - Settings Page v2.0
"""

import streamlit as st
from datetime import datetime, timedelta, timezone

st.set_page_config(
    page_title="Settings | Ming Qimen",
    page_icon="⚙️",
    layout="wide"
)

SGT = timezone(timedelta(hours=8))

# Load CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

st.title("⚙️ Settings 设置")

# Initialize
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

# Tabs
tab1, tab2 = st.tabs(["👤 BaZi Profile", "🎨 Preferences"])

# ============================================================================
# TAB 1: BAZI PROFILE
# ============================================================================

with tab1:
    st.markdown("### 👤 Your BaZi Profile")
    st.markdown("Configure your personal BaZi for integrated QMDJ analysis")
    st.caption("ℹ️ This helps us personalize guidance based on your Day Master and favorable elements")
    
    profile = st.session_state.user_profile
    
    with st.form("bazi_form"):
        st.markdown("#### Day Master 日主")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            day_masters = ['', 'Jia 甲', 'Yi 乙', 'Bing 丙', 'Ding 丁', 'Wu 戊', 
                          'Ji 己', 'Geng 庚', 'Xin 辛', 'Ren 壬', 'Gui 癸']
            current_dm = profile.get('day_master', '')
            dm_idx = day_masters.index(current_dm) if current_dm in day_masters else 0
            
            day_master = st.selectbox(
                "Day Master Stem",
                options=day_masters,
                index=dm_idx,
                help="Your Day Master from your BaZi chart"
            )
        
        with col2:
            strengths = ['', 'Strong', 'Weak', 'Extremely Strong', 'Extremely Weak', 'Balanced']
            current_str = profile.get('strength', '')
            str_idx = strengths.index(current_str) if current_str in strengths else 0
            
            strength = st.selectbox(
                "Day Master Strength",
                options=strengths,
                index=str_idx,
                help="How strong is your Day Master?"
            )
        
        with col3:
            profiles = ['', 'Pioneer (Indirect Wealth)', 'Philosopher (Eating God)', 
                       'Director (Direct Officer)', 'Warrior (7 Killings)', 
                       'Leader (Direct Wealth)', 'Diplomat (Direct Resource)',
                       'Artist (Hurting Officer)', 'Networker (Friend)',
                       'Strategist (Indirect Resource)', 'Competitor (Rob Wealth)']
            
            profile_type = st.selectbox(
                "10 God Profile",
                options=profiles,
                help="Your dominant Ten God profile"
            )
        
        st.markdown("#### Helpful Elements 用神")
        st.caption("ℹ️ Elements that support your Day Master")
        
        ug_col1, ug_col2 = st.columns(2)
        
        with ug_col1:
            useful_gods = st.multiselect(
                "Favorable Elements (Useful Gods)",
                options=['Wood', 'Fire', 'Earth', 'Metal', 'Water'],
                default=profile.get('useful_gods', []),
                help="Elements that support your weak Day Master"
            )
        
        with ug_col2:
            unfavorable = st.multiselect(
                "Unfavorable Elements",
                options=['Wood', 'Fire', 'Earth', 'Metal', 'Water'],
                default=profile.get('unfavorable', []),
                help="Elements that weaken your Day Master"
            )
        
        st.markdown("#### Special Structures 特殊格局")
        
        struct_col1, struct_col2 = st.columns(2)
        
        with struct_col1:
            wealth_vault = st.checkbox(
                "Wealth Vault Present",
                value=profile.get('wealth_vault', False),
                help="Do you have a Wealth Vault (财库) in your chart?"
            )
        
        with struct_col2:
            nobleman = st.checkbox(
                "Nobleman Present",
                value=profile.get('nobleman', False),
                help="Do you have a Nobleman (贵人) in your chart?"
            )
        
        submitted = st.form_submit_button("💾 Save Profile", use_container_width=True, type="primary")
        
        if submitted:
            # Extract element from day master
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
    
    # Current profile display
    if st.session_state.user_profile.get('day_master'):
        st.markdown("---")
        st.markdown("#### Current Profile")
        st.json(st.session_state.user_profile)
    
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
                'useful_gods_reasoning': 'Earth produces Metal (Resource), Metal supports (Companion)',
                'unfavorable': ['Fire'],
                'unfavorable_reasoning': 'Fire controls Metal excessively for weak DM',
                'wealth_vault': True,
                'nobleman': False,
                'traits': ['Risk-tolerant', 'Opportunity-focused', 'Quick decision-making']
            }
            st.success("✅ Geng Metal Pioneer profile loaded!")
            st.rerun()

# ============================================================================
# TAB 2: PREFERENCES
# ============================================================================

with tab2:
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
        index=0,
        help="Choose beginner-friendly or traditional QMDJ terms"
    )
    
    st.markdown("#### Calculation Method")
    default_method = st.radio(
        "Default Method",
        options=["Chai Bu 拆補 (Recommended)", "Zhi Run 置閏"],
        index=0
    )
    
    st.info("ℹ️ Preferences will be applied in future updates.")

st.markdown("---")
st.caption("🌟 Ming Qimen 明奇门 | Settings v2.0")
