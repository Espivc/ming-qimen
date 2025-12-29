"""
Ming Qimen 明奇门 - Settings Page v3.0
Phase 5: Enhanced BaZi with Birth Date Calculator
"""

import streamlit as st
from datetime import datetime, timedelta, timezone, date, time
import sys
import os

# Add core module to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.bazi_engine import (
    calculate_bazi_profile,
    format_pillars_display,
    HEAVENLY_STEMS,
    STEMS_PINYIN,
    BRANCHES_ANIMAL,
    TEN_GODS_ENGLISH,
    PROFILE_TYPES
)

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

if 'bazi_calculated' not in st.session_state:
    st.session_state.bazi_calculated = None

# Tabs
tab1, tab2, tab3 = st.tabs(["🎂 Birth Date Calculator", "👤 Manual Profile", "🎨 Preferences"])

# ============================================================================
# TAB 1: BIRTH DATE CALCULATOR (NEW!)
# ============================================================================

with tab1:
    st.markdown("### 🎂 Calculate Your BaZi from Birth Date")
    st.markdown("Enter your birth details and we'll calculate your Four Pillars automatically!")
    
    st.info("ℹ️ **Tip:** If you don't know your exact birth time, use 12:00 noon as an approximation. The Day Master will still be accurate.")
    
    # Birth data input
    col1, col2 = st.columns(2)
    
    with col1:
        birth_date = st.date_input(
            "📅 Birth Date 出生日期",
            value=date(1990, 1, 1),
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            help="Select your date of birth"
        )
    
    with col2:
        birth_time = st.time_input(
            "🕐 Birth Time 出生时间",
            value=time(12, 0),
            help="Select your time of birth (use 12:00 if unknown)"
        )
    
    st.caption("⚠️ Note: Chinese BaZi uses solar calendar. Month boundaries are based on solar terms, not calendar months.")
    
    # Calculate button
    if st.button("🔮 Calculate My BaZi", use_container_width=True, type="primary"):
        with st.spinner("Calculating your Four Pillars..."):
            profile = calculate_bazi_profile(
                year=birth_date.year,
                month=birth_date.month,
                day=birth_date.day,
                hour=birth_time.hour
            )
            st.session_state.bazi_calculated = profile
            
            # Auto-save to user profile
            st.session_state.user_profile = {
                'birth_date': birth_date.isoformat(),
                'birth_time': birth_time.strftime("%H:%M"),
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
                'ten_gods_mapping': profile['ten_gods_mapping']
            }
            
            st.success("✅ BaZi calculated and saved to your profile!")
    
    # Display results
    if st.session_state.bazi_calculated:
        profile = st.session_state.bazi_calculated
        fp = profile['four_pillars']
        dm = profile['day_master']
        
        st.markdown("---")
        st.markdown("## 📊 Your BaZi Chart 你的八字")
        
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
                <div style="background: {bg}; border: {border}; border-radius: 12px; padding: 15px; text-align: center; min-height: 200px;">
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
            st.caption(profile['profile'].get('dominant_god_chinese', ''))
        
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
        
        st.markdown("---")
        
        # Ten Gods Mapping
        st.markdown("### 🔮 Ten Gods Mapping 十神对照")
        st.caption("How each element relates to your Day Master")
        
        tg_cols = st.columns(5)
        elements = ["Wood", "Fire", "Earth", "Metal", "Water"]
        element_icons = {"Wood": "🌳", "Fire": "🔥", "Earth": "�ite🏔️", "Metal": "⚔️", "Water": "💧"}
        
        for i, elem in enumerate(elements):
            with tg_cols[i]:
                god_chinese = profile['ten_gods_mapping'].get(elem, "")
                god_english = TEN_GODS_ENGLISH.get(god_chinese, god_chinese)
                
                # Color based on favorable/unfavorable
                if elem in useful['favorable']:
                    color = "#4CAF50"
                    icon = "✅"
                elif elem in useful['unfavorable']:
                    color = "#F44336"
                    icon = "❌"
                else:
                    color = "#888"
                    icon = "○"
                
                st.markdown(f"""
                <div style="background: #1e1e2e; border: 1px solid {color}; border-radius: 8px; padding: 10px; text-align: center;">
                    <div style="font-size: 1.5em;">{element_icons.get(elem, '●')}</div>
                    <div style="color: {color}; font-weight: bold;">{elem}</div>
                    <div style="color: #888; font-size: 0.8em;">{god_chinese}</div>
                    <div style="color: #aaa; font-size: 0.75em;">{god_english}</div>
                    <div>{icon}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Reasoning
        with st.expander("📖 Why These Useful Gods?"):
            st.markdown(profile['useful_gods']['reasoning'])
        
        # Raw data
        with st.expander("🔧 Technical Details"):
            st.json(profile)

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
            st.metric("Profile", p.get('profile', 'Not set')[:20])
        
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
st.caption("🌟 Ming Qimen 明奇门 | Settings v3.0 - Phase 5 | Enhanced BaZi Calculator")
