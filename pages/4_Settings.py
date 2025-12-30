"""
Ming Qimen - Settings Page
Version: 4.0
Streamlined - BaZi profile shows in sidebar only
Manual profile entry for users who know their BaZi
"""

import streamlit as st

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .settings-title { color: #FFD700; font-size: 2.5rem; font-weight: bold; }
    .section-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .element-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.85rem;
        margin: 0.2rem;
    }
    .wood { background: #228B22; color: white; }
    .fire { background: #DC143C; color: white; }
    .earth { background: #DAA520; color: black; }
    .metal { background: #C0C0C0; color: black; }
    .water { background: #4169E1; color: white; }
    .profile-display {
        background: linear-gradient(135deg, #1a472a 0%, #1a1a2e 100%);
        border: 2px solid #2ecc71;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .no-profile {
        background: linear-gradient(135deg, #2d1f1f 0%, #1a1a2e 100%);
        border: 2px solid #e74c3c;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="settings-title">⚙️ Settings 设置</p>', unsafe_allow_html=True)

# Tabs for different settings
tab1, tab2, tab3 = st.tabs(["🎂 BaZi Profile", "👤 Manual Profile", "🎨 Preferences"])

# ============================================================
# TAB 1: BaZi Profile (Display Only + Link to Calculator)
# ============================================================
with tab1:
    st.subheader("🎂 Your BaZi Profile")
    
    if st.session_state.get("user_profile"):
        profile = st.session_state.user_profile
        
        st.markdown(f"""
        <div class="profile-display">
            <h3 style="color: #FFD700; margin: 0 0 1rem 0;">✅ Profile Active</h3>
            <p><strong>Day Master:</strong> {profile.get('day_master', 'N/A')}</p>
            <p><strong>Element:</strong> {profile.get('polarity', '')} {profile.get('element', 'N/A')}</p>
            <p><strong>Strength:</strong> {profile.get('strength', 'N/A')} ({profile.get('strength_score', 'N/A')}/10)</p>
            <p><strong>Birth:</strong> {profile.get('birth_date', 'N/A')} @ {profile.get('birth_time', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Useful Gods display
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**✅ Useful Gods**")
            useful = profile.get('useful_gods', [])
            if useful:
                for god in useful:
                    st.markdown(f'<span class="element-badge {god.lower()}">{god}</span>', unsafe_allow_html=True)
            else:
                st.caption("Not set")
        
        with col2:
            st.markdown("**❌ Unfavorable**")
            unfavorable = profile.get('unfavorable', [])
            if unfavorable:
                for god in unfavorable:
                    st.markdown(f'<span class="element-badge {god.lower()}">{god}</span>', unsafe_allow_html=True)
            else:
                st.caption("Not set")
        
        # Special structures
        st.markdown("**🏆 Special Structures**")
        structures = []
        if profile.get('wealth_vault'):
            structures.append("💰 Wealth Vault")
        if profile.get('nobleman'):
            structures.append("👑 Nobleman")
        
        if structures:
            st.success(" • ".join(structures))
        else:
            st.info("None detected")
        
        st.divider()
        
        # Recalculate button
        if st.button("🔄 Recalculate BaZi", use_container_width=True):
            st.switch_page("pages/6_BaZi.py")
        
        # Clear profile button
        if st.button("🗑️ Clear Profile", use_container_width=True, type="secondary"):
            if st.session_state.get("user_profile"):
                del st.session_state.user_profile
                st.session_state.bazi_calculated = False
                st.success("Profile cleared!")
                st.rerun()
    
    else:
        st.markdown("""
        <div class="no-profile">
            <h3 style="color: #e74c3c; margin: 0 0 1rem 0;">⚠️ No BaZi Profile Set</h3>
            <p style="color: #888;">Use the BaZi Calculator to calculate your Four Pillars, or enter your profile manually.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        
        # Link to BaZi Calculator
        if st.button("🔮 Go to BaZi Calculator", type="primary", use_container_width=True):
            st.switch_page("pages/6_BaZi.py")
        
        st.markdown("")
        st.markdown("**Or enter manually below**")
        st.caption("If you already know your BaZi, use the Manual Profile tab →")

# ============================================================
# TAB 2: Manual Profile Entry
# ============================================================
with tab2:
    st.subheader("👤 Manual Profile Entry")
    st.caption("Enter your BaZi details if you already know them")
    
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    STEMS = ["Jia 甲", "Yi 乙", "Bing 丙", "Ding 丁", "Wu 戊", 
             "Ji 己", "Geng 庚", "Xin 辛", "Ren 壬", "Gui 癸"]
    
    ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]
    
    with col1:
        # Get current profile values as defaults
        current = st.session_state.get("user_profile", {})
        
        # Day Master
        dm_options = STEMS
        dm_default = 0
        if current.get('day_master'):
            for i, s in enumerate(STEMS):
                if current['day_master'] in s:
                    dm_default = i
                    break
        
        day_master = st.selectbox(
            "Day Master (日主)",
            options=STEMS,
            index=dm_default
        )
        
        # Element (auto-filled based on stem)
        stem_to_element = {
            "Jia": "Wood", "Yi": "Wood", "Bing": "Fire", "Ding": "Fire",
            "Wu": "Earth", "Ji": "Earth", "Geng": "Metal", "Xin": "Metal",
            "Ren": "Water", "Gui": "Water"
        }
        stem_name = day_master.split()[0]
        element = stem_to_element.get(stem_name, "Wood")
        st.info(f"Element: **{element}**")
        
        # Polarity (auto-filled)
        stem_to_polarity = {
            "Jia": "Yang", "Yi": "Yin", "Bing": "Yang", "Ding": "Yin",
            "Wu": "Yang", "Ji": "Yin", "Geng": "Yang", "Xin": "Yin",
            "Ren": "Yang", "Gui": "Yin"
        }
        polarity = stem_to_polarity.get(stem_name, "Yang")
        st.info(f"Polarity: **{polarity}**")
    
    with col2:
        # Strength
        strength = st.selectbox(
            "Day Master Strength",
            options=["Weak", "Balanced", "Strong"],
            index=["Weak", "Balanced", "Strong"].index(current.get('strength', 'Weak'))
        )
        
        # Strength score
        strength_score = st.slider(
            "Strength Score",
            min_value=1,
            max_value=10,
            value=current.get('strength_score', 4)
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Useful Gods
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("**Useful Gods (有用神)**")
    
    useful_col1, useful_col2 = st.columns(2)
    
    with useful_col1:
        useful_gods = st.multiselect(
            "Select Useful Elements",
            options=ELEMENTS,
            default=current.get('useful_gods', ['Earth', 'Metal'])
        )
    
    with useful_col2:
        unfavorable = st.multiselect(
            "Select Unfavorable Elements",
            options=ELEMENTS,
            default=current.get('unfavorable', ['Fire'])
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Special Structures
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("**Special Structures**")
    
    struct_col1, struct_col2 = st.columns(2)
    
    with struct_col1:
        wealth_vault = st.checkbox(
            "💰 Wealth Vault (财库)",
            value=current.get('wealth_vault', True)
        )
    
    with struct_col2:
        nobleman = st.checkbox(
            "👑 Nobleman (贵人)",
            value=current.get('nobleman', False)
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Save Manual Profile
    st.divider()
    
    if st.button("💾 Save Manual Profile", type="primary", use_container_width=True):
        st.session_state.user_profile = {
            'day_master': day_master,
            'element': element,
            'polarity': polarity,
            'strength': strength,
            'strength_score': strength_score,
            'useful_gods': useful_gods,
            'unfavorable': unfavorable,
            'wealth_vault': wealth_vault,
            'nobleman': nobleman,
            'birth_date': current.get('birth_date', 'Manual Entry'),
            'birth_time': current.get('birth_time', 'Manual Entry'),
            'manual_entry': True
        }
        st.success("✅ Manual profile saved successfully!")
        st.balloons()
        st.rerun()

# ============================================================
# TAB 3: Preferences
# ============================================================
with tab3:
    st.subheader("🎨 Display Preferences")
    
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    
    # Language preference
    language = st.selectbox(
        "Language / 语言",
        options=["English with Chinese", "English Only", "Chinese Only"],
        index=0
    )
    
    # Chart display
    show_chinese = st.checkbox(
        "Show Chinese characters in charts",
        value=True
    )
    
    # Theme (informational only - Streamlit handles this)
    st.info("💡 Theme is controlled by Streamlit settings. Click the menu (⋮) → Settings → Theme")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("**Export Preferences**")
    
    # Default export format
    export_format = st.selectbox(
        "Default Export Format",
        options=["JSON (Universal Schema v2.0)", "CSV", "Both"],
        index=0
    )
    
    # Include BaZi in exports
    include_bazi = st.checkbox(
        "Always include BaZi data in exports",
        value=True
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Save preferences
    if st.button("💾 Save Preferences", use_container_width=True):
        st.session_state.preferences = {
            'language': language,
            'show_chinese': show_chinese,
            'export_format': export_format,
            'include_bazi': include_bazi
        }
        st.success("✅ Preferences saved!")

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("---")
    if st.session_state.get("user_profile"):
        profile = st.session_state.user_profile
        st.markdown("### 👤 Your BaZi")
        st.markdown(f"**{profile['day_master']}**")
        st.markdown(f"{profile['polarity']} {profile['element']} • {profile['strength']}")
        if profile.get('useful_gods'):
            st.caption(f"Useful: {', '.join(profile['useful_gods'])}")
    else:
        st.info("No BaZi profile set")

# Footer
st.markdown("---")
st.caption("🌟 Ming Qimen 明奇门 | Settings v4.0")
