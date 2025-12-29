"""
Ming Qimen 明奇门 - Settings Page v3.2
Phase 5: Fixed birth date persistence
"""

import streamlit as st
from datetime import datetime, timedelta, timezone, date
import sys
import os

# Add core module to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.bazi_engine import (
        calculate_bazi_profile,
        HEAVENLY_STEMS,
        STEMS_PINYIN,
        TEN_GODS_ENGLISH,
        PROFILE_TYPES
    )
    BAZI_ENGINE_AVAILABLE = True
except ImportError:
    BAZI_ENGINE_AVAILABLE = False

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

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

if 'bazi_calculated' not in st.session_state:
    st.session_state.bazi_calculated = None

# Birth date persistence - use session state to remember values
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

# Tabs
tab1, tab2, tab3 = st.tabs(["🎂 Birth Date Calculator", "👤 Manual Profile", "🎨 Preferences"])

# ============================================================================
# TAB 1: BIRTH DATE CALCULATOR
# ============================================================================

with tab1:
    st.markdown("### 🎂 Calculate Your BaZi from Birth Date")
    st.markdown("Enter your birth details and we'll calculate your Four Pillars automatically!")
    
    if not BAZI_ENGINE_AVAILABLE:
        st.error("❌ BaZi engine not available. Please check core/bazi_engine.py is installed.")
    else:
        st.info("ℹ️ **Tip:** If you don't know your exact birth time, use 12:00 noon as an approximation. The Day Master will still be accurate.")
        
        # Birth data input - use session state for persistence
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            # Create date from session state values
            try:
                default_date = date(
                    st.session_state.birth_year,
                    st.session_state.birth_month,
                    st.session_state.birth_day
                )
            except:
                default_date = date(1990, 1, 1)
            
            birth_date = st.date_input(
                "📅 Birth Date 出生日期",
                value=default_date,
                min_value=date(1900, 1, 1),
                max_value=date.today(),
                help="Select your date of birth"
            )
            
            # Update session state when date changes
            st.session_state.birth_year = birth_date.year
            st.session_state.birth_month = birth_date.month
            st.session_state.birth_day = birth_date.day
        
        with col2:
            birth_hour = st.number_input(
                "🕐 Hour 时",
                min_value=0,
                max_value=23,
                value=st.session_state.birth_hour,
                help="Birth hour (0-23)",
                key="hour_input"
            )
            st.session_state.birth_hour = birth_hour
        
        with col3:
            birth_minute = st.number_input(
                "Minute 分",
                min_value=0,
                max_value=59,
                value=st.session_state.birth_minute,
                help="Birth minute (0-59)",
                key="minute_input"
            )
            st.session_state.birth_minute = birth_minute
        
        st.caption("⚠️ Note: Chinese BaZi uses solar calendar. Month boundaries are based on solar terms, not calendar months.")
        
        # Calculate button
        if st.button("🔮 Calculate My BaZi", use_container_width=True, type="primary"):
            with st.spinner("Calculating your Four Pillars..."):
                profile = calculate_bazi_profile(
                    year=birth_date.year,
                    month=birth_date.month,
                    day=birth_date.day,
                    hour=birth_hour
                )
                st.session_state.bazi_calculated = profile
                
                # Auto-save to user profile
                st.session_state.user_profile = {
                    'birth_date': birth_date.isoformat(),
                    'birth_time': f"{birth_hour:02d}:{birth_minute:02d}",
                    'day_master': f"{profile['day_master']['pinyin']} {profile['day_master']['chinese']}",
                    'element': profile['day_master']['element'],
                    'polarity': profile['day_master']['polarity'],
                    'strength': profile['day_master']['strength'],
                    'strength_score': profile['day_master']['strength_score'],
                    'profile': f"{profile['profile']['type']} ({profile['profile']['dominant_god']})",
                    'dominant_god': profile['profile']['dominant_god'],
                    'useful_gods': profile['useful_gods']['favorable'],
                    'useful_gods_reasoning': profile['useful_gods']['reasoning'],
                    'unfavorable': profile['useful_gods']['unfavorable'],
                    'wealth_vault': profile['special_structures']['wealth_vault'],
                    'wealth_vault_location': profile['special_structures']['wealth_vault_location'],
                    'nobleman': profile['special_structures']['nobleman_present'],
                    'nobleman_location': profile['special_structures']['nobleman_location'],
                    'four_pillars': profile['four_pillars'],
                    'ten_gods_mapping': profile.get('ten_gods_mapping', {})
                }
                
                st.success("✅ BaZi calculated and saved to your profile!")
                st.rerun()
        
        # Display results if calculated
        if st.session_state.bazi_calculated:
            profile = st.session_state.bazi_calculated
            fp = profile['four_pillars']
            dm = profile['day_master']
            
            st.markdown("---")
            st.markdown("## 📊 Your BaZi Chart 你的八字")
            
            # Show saved birth info
            saved_profile = st.session_state.user_profile
            st.caption(f"📅 Birth: {saved_profile.get('birth_date', 'N/A')} at {saved_profile.get('birth_time', 'N/A')}")
            
            # Four Pillars Display
            st.markdown("### 四柱 Four Pillars")
            
            pillar_cols = st.columns(4)
            pillar_names = [
                ("year", "年柱", "Year"),
                ("month", "月柱", "Month"),
                ("day", "日柱", "Day"),
                ("hour", "时柱", "Hour")
            ]
            
            for i, (key, chinese, english) in enumerate(pillar_names):
                with pillar_cols[i]:
                    pillar = fp[key]
                    is_day = key == "day"
                    
                    # Highlight Day Pillar
                    border = "3px solid #FFD700" if is_day else "1px solid #444"
                    bg = "linear-gradient(135deg, #1a237e 0%, #0d47a1 100%)" if is_day else "#1e1e2e"
                    
                    st.markdown(f"""
                    <div style="background: {bg}; border: {border}; border-radius: 12px; padding: 15px; text-align: center; min-height: 180px;">
                        <div style="color: #888; font-size: 0.8em;">{english}</div>
                        <div style="color: #FFD700; font-weight: bold; font-size: 1em; margin-bottom: 10px;">{chinese}</div>
                        <div style="font-size: 2.5em; color: #fff; margin: 10px 0;">
                            {pillar['stem']['chinese']}
                        </div>
                        <div style="font-size: 2em; color: #90CAF9; margin: 10px 0;">
                            {pillar['branch']['chinese']}
                        </div>
                        <div style="color: #888; font-size: 0.75em;">
                            {pillar['stem']['pinyin']}-{pillar['branch']['pinyin']}
                        </div>
                        <div style="color: #666; font-size: 0.7em;">
                            {pillar['branch']['animal']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if is_day:
                        st.caption("👆 Day Master")
            
            st.markdown("---")
            
            # Day Master Analysis
            st.markdown("### 🌟 Day Master Analysis 日主分析")
            
            dm_col1, dm_col2, dm_col3 = st.columns(3)
            
            with dm_col1:
                st.markdown("#### Day Master 日主")
                st.markdown(f"### {dm['chinese']} {dm['pinyin']}")
                st.markdown(f"**Element:** {dm['element']} ({dm['polarity']})")
                
                # Strength indicator
                strength = dm['strength']
                score = dm['strength_score']
                
                if score >= 7:
                    st.success(f"**Strength:** {strength} ({score}/10)")
                elif score >= 4:
                    st.info(f"**Strength:** {strength} ({score}/10)")
                else:
                    st.warning(f"**Strength:** {strength} ({score}/10)")
            
            with dm_col2:
                st.markdown("#### Helpful Elements 用神")
                useful = profile['useful_gods']
                
                for elem in useful['favorable']:
                    st.markdown(f"✅ **{elem}**")
                
                st.markdown("#### Unfavorable Elements")
                for elem in useful['unfavorable']:
                    st.markdown(f"❌ {elem}")
            
            with dm_col3:
                st.markdown("#### Profile Type 命格")
                st.markdown(f"### {profile['profile']['type']}")
                st.markdown(f"**Dominant God:** {profile['profile']['dominant_god']}")
            
            st.markdown("---")
            
            # Special Structures
            st.markdown("### 🏛️ Special Structures 特殊格局")
            
            struct_col1, struct_col2 = st.columns(2)
            
            with struct_col1:
                if profile['special_structures']['wealth_vault']:
                    st.success(f"💰 **Wealth Vault Present** - {profile['special_structures']['wealth_vault_location']}")
                else:
                    st.info("💰 Wealth Vault: Not present")
            
            with struct_col2:
                if profile['special_structures']['nobleman_present']:
                    st.success(f"👑 **Nobleman Present** - {profile['special_structures']['nobleman_location']}")
                else:
                    st.info("👑 Nobleman: Not present")
            
            # Reasoning
            with st.expander("📖 Why These Useful Gods?"):
                st.markdown(profile['useful_gods']['reasoning'])

# ============================================================================
# TAB 2: MANUAL PROFILE
# ============================================================================

with tab2:
    st.markdown("### 👤 Manual BaZi Profile")
    st.markdown("If you already know your BaZi, enter it manually here.")
    
    profile = st.session_state.user_profile
    
    with st.form("bazi_form"):
        st.markdown("#### Day Master 日主")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            day_masters = [''] + [f"{STEMS_PINYIN[i]} {HEAVENLY_STEMS[i]}" for i in range(10)] if BAZI_ENGINE_AVAILABLE else ['']
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
            profiles = [''] + [f"{v} ({k})" for k, v in PROFILE_TYPES.items()] if BAZI_ENGINE_AVAILABLE else ['']
            
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
        st.markdown("#### Current Profile Summary")
        
        p = st.session_state.user_profile
        
        info_cols = st.columns(3)
        with info_cols[0]:
            st.metric("Day Master", p.get('day_master', 'Not set'))
        with info_cols[1]:
            st.metric("Strength", p.get('strength', 'Not set'))
        with info_cols[2]:
            profile_str = p.get('profile', 'Not set')
            st.metric("Profile", profile_str[:15] + "..." if len(profile_str) > 15 else profile_str)
        
        st.markdown(f"**Favorable Elements:** {', '.join(p.get('useful_gods', []))}")
        st.markdown(f"**Unfavorable:** {', '.join(p.get('unfavorable', []))}")
    
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
st.caption("🌟 Ming Qimen 明奇门 | Settings v3.2")
