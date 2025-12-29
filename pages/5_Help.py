"""
Ming Qimen 明奇门 - Help & Guide v2.0
"""

import streamlit as st

st.set_page_config(
    page_title="Help | Ming Qimen",
    page_icon="❓",
    layout="wide"
)

# Load CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

st.title("❓ Help & Guide 帮助")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🌟 About Ming", "📖 What is QMDJ?", "🔮 How to Use", "📊 Understanding Signs"])

# ============================================================================
# TAB 1: ABOUT
# ============================================================================

with tab1:
    st.markdown("""
    ## 🌟 About Ming Qimen 明奇门
    
    ### *"Clarity for the People"*
    
    ---
    
    ### Our Mission
    
    I created Ming Qimen because I believe **wisdom shouldn't come with a price tag or a headache**.
    
    My name is **Beng (明)**, which means **'Brightness'**. My goal is to use that light to clear 
    the fog of ancient calculations.
    
    Too many apps are built for experts; this one is built for **you**.
    
    ---
    
    ### Our Promise
    
    ✅ **No paywalls** - Free forever
    
    ✅ **No complex data entry** - Just pick a topic and time
    
    ✅ **Clear guidance** - Actionable advice, not cryptic symbols
    
    ✅ **Beginner-friendly** - We translate the ancient into the practical
    
    ---
    
    *"Guiding you first, because your peace of mind matters."*
    
    ---
    
    ### Version 2.0 - Phase 4
    
    This version includes:
    - 🔮 Real QMDJ calculations (kinqimen engine)
    - 📊 9-Palace grid visualization
    - 💪 Component strength analysis
    - 🎯 Palace recommendations
    - 📤 Universal Schema v2.0 export
    - 👤 BaZi profile integration
    """)

# ============================================================================
# TAB 2: WHAT IS QMDJ
# ============================================================================

with tab2:
    st.markdown("""
    ## 📖 What is Qi Men Dun Jia?
    
    **Qi Men Dun Jia** (奇門遁甲) is one of the most powerful ancient Chinese divination systems.
    
    ---
    
    ### History
    
    - 📜 Over **4,000 years old**
    - 👑 Originally used by **emperors and generals**
    - ⚔️ Called the "Art of War Timing"
    - 🏛️ One of the **Three Great Divination Arts** (三式)
    
    ---
    
    ### How It Works
    
    QMDJ maps **cosmic energy patterns** onto a 3x3 grid (9 Palaces) based on:
    
    1. **Time** - Each 2-hour Chinese hour has unique energy
    2. **Solar Terms** - 24 seasonal divisions of the year
    3. **Heaven Stems** - 10 celestial energies (天干)
    4. **Stars** - 9 stars representing different qualities
    5. **Doors** - 8 doors showing outcomes
    6. **Deities** - 8 spirits adding nuance
    
    ---
    
    ### The 9 Palaces
    
    Each palace governs a life area:
    
    | Palace | Topic | Direction |
    |--------|-------|-----------|
    | 1 | Career 💼 | North |
    | 2 | Relations 💕 | Southwest |
    | 3 | Health 💪 | East |
    | 4 | Wealth 💰 | Southeast |
    | 5 | Self 🎯 | Center |
    | 6 | Mentor 🤝 | Northwest |
    | 7 | Children 👶 | West |
    | 8 | Knowledge 📚 | Northeast |
    | 9 | Fame 🌟 | South |
    
    ---
    
    ### Modern Applications
    
    Today, we use QMDJ for:
    - 💼 **Career** - Job interviews, business meetings
    - 💰 **Wealth** - Investment timing, negotiations
    - 💕 **Relationships** - Meeting someone, proposals
    - 💪 **Health** - Medical appointments
    - ✈️ **Travel** - Best directions and timing
    """)

# ============================================================================
# TAB 3: HOW TO USE
# ============================================================================

with tab3:
    st.markdown("""
    ## 🔮 How to Use Ming Qimen
    
    ---
    
    ### Step 1: Choose Your Topic 🎯
    
    What do you need guidance on?
    
    - 💼 Career - Job, business, life path
    - 💕 Relations - Marriage, partnerships
    - 💰 Wealth - Money, investments
    - etc.
    
    ---
    
    ### Step 2: Select Time 🕐
    
    When do you need the guidance for?
    
    - **Current time** - For immediate decisions
    - **Future time** - For planned events
    
    ---
    
    ### Step 3: Generate Reading 📊
    
    Click "Get Your Reading" and we calculate:
    
    1. The cosmic energy pattern
    2. Palace components (stems, stars, doors, spirits)
    3. Strength scores
    4. Overall verdict
    
    ---
    
    ### Step 4: Understand the Guidance 💡
    
    Your reading shows:
    
    - **Score** (1-10) - Overall favorability
    - **Verdict** - Simple interpretation
    - **Components** - What energies are active
    - **Advice** - What to do
    
    ---
    
    ### Step 5: Export (Optional) 📤
    
    For advanced users:
    - Export to JSON for AI analysis
    - Track outcomes for learning
    - Build your personal database
    """)

# ============================================================================
# TAB 4: UNDERSTANDING SIGNS
# ============================================================================

with tab4:
    st.markdown("""
    ## 📊 Understanding Signs
    
    ---
    
    ### Energy Levels
    
    Components have different strengths based on their relationship with the palace element:
    
    | Level | Meaning | Advice |
    |-------|---------|--------|
    | 🔥 High Energy | Element is strong here | Take Action! |
    | ✨ Good Energy | Element is supported | Favorable |
    | 😐 Balanced | Neutral relationship | Proceed Normally |
    | 🌙 Low Energy | Element is weakened | Be Patient |
    | 💤 Rest Energy | Element is exhausted | Wait & Reflect |
    
    ---
    
    ### The 8 Doors
    
    | Door | Nature | Meaning |
    |------|--------|---------|
    | 開 Open | ✅ Auspicious | New beginnings, negotiations |
    | 休 Rest | ✅ Auspicious | Recuperation, passive gains |
    | 生 Life | ✅ Auspicious | Growth, investments, new starts |
    | 傷 Harm | ⚠️ Challenging | Conflicts, avoid confrontation |
    | 杜 Delusion | 😐 Neutral | Hidden matters, flexibility needed |
    | 景 Scenery | 😐 Neutral | Public matters, creative work |
    | 死 Stillness | ⚠️ Challenging | Wait, don't act |
    | 驚 Surprise | ⚠️ Challenging | Unexpected events, stay alert |
    
    ---
    
    ### The 9 Stars
    
    | Star | Nature | Quality |
    |------|--------|---------|
    | 天心 Heart | ✅ Good | Leadership, authority |
    | 天任 Ren | ✅ Good | Steady progress |
    | 天輔 Assistant | ✅ Good | Help from others |
    | 天禽 Connect | ✅ Good | Networking |
    | 天英 Hero | ✅ Good | Recognition |
    | 天沖 Impulse | 😐 Neutral | Quick action needed |
    | 天柱 Pillar | ⚠️ Challenging | Obstacles |
    | 天芮 Grass | ⚠️ Challenging | Health concerns |
    | 天蓬 Canopy | ⚠️ Challenging | Hidden dangers |
    
    ---
    
    ### Score Interpretation
    
    | Score | Verdict | What to Do |
    |-------|---------|------------|
    | 8-10 | Very Favorable | Great time, proceed confidently |
    | 6-7 | Favorable | Good conditions, move forward |
    | 4-5 | Neutral | Balanced, use your judgment |
    | 2-3 | Challenging | Caution advised, prepare well |
    | 1 | Very Challenging | Consider waiting, reassess |
    """)

st.markdown("---")
st.caption("🌟 Ming Qimen 明奇门 | Help v2.0")
