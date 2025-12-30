"""
Ming Qimen - BaZi Calculator Page
Version: 4.0
Features:
- Birth date + hour + minute selection
- "Unknown birth time" skip option
- Full Four Pillars calculation
- Save to session state (user_profile)
"""

import streamlit as st
from datetime import datetime, date

# ============================================================
# CONSTANTS
# ============================================================

STEMS = ["Jia 甲", "Yi 乙", "Bing 丙", "Ding 丁", "Wu 戊", 
         "Ji 己", "Geng 庚", "Xin 辛", "Ren 壬", "Gui 癸"]

BRANCHES = ["Zi 子", "Chou 丑", "Yin 寅", "Mao 卯", "Chen 辰", "Si 巳",
            "Wu 午", "Wei 未", "Shen 申", "You 酉", "Xu 戌", "Hai 亥"]

STEM_ELEMENTS = {
    "Jia": "Wood", "Yi": "Wood", "Bing": "Fire", "Ding": "Fire",
    "Wu": "Earth", "Ji": "Earth", "Geng": "Metal", "Xin": "Metal",
    "Ren": "Water", "Gui": "Water"
}

STEM_POLARITY = {
    "Jia": "Yang", "Yi": "Yin", "Bing": "Yang", "Ding": "Yin",
    "Wu": "Yang", "Ji": "Yin", "Geng": "Yang", "Xin": "Yin",
    "Ren": "Yang", "Gui": "Yin"
}

BRANCH_ELEMENTS = {
    "Zi": "Water", "Chou": "Earth", "Yin": "Wood", "Mao": "Wood",
    "Chen": "Earth", "Si": "Fire", "Wu": "Fire", "Wei": "Earth",
    "Shen": "Metal", "You": "Metal", "Xu": "Earth", "Hai": "Water"
}

# Hidden Stems in each Branch
HIDDEN_STEMS = {
    "Zi": ["Gui"],
    "Chou": ["Ji", "Gui", "Xin"],
    "Yin": ["Jia", "Bing", "Wu"],
    "Mao": ["Yi"],
    "Chen": ["Wu", "Yi", "Gui"],
    "Si": ["Bing", "Wu", "Geng"],
    "Wu": ["Ding", "Ji"],
    "Wei": ["Ji", "Ding", "Yi"],
    "Shen": ["Geng", "Ren", "Wu"],
    "You": ["Xin"],
    "Xu": ["Wu", "Xin", "Ding"],
    "Hai": ["Ren", "Jia"]
}

# Ten Gods mapping (from Day Master perspective)
TEN_GODS = {
    ("Wood", "Wood", "Yang", "Yang"): "Friend 比肩",
    ("Wood", "Wood", "Yang", "Yin"): "Rob Wealth 劫财",
    ("Wood", "Fire", "Yang", "Yang"): "Eating God 食神",
    ("Wood", "Fire", "Yang", "Yin"): "Hurting Officer 伤官",
    ("Wood", "Earth", "Yang", "Yang"): "Indirect Wealth 偏财",
    ("Wood", "Earth", "Yang", "Yin"): "Direct Wealth 正财",
    ("Wood", "Metal", "Yang", "Yang"): "7 Killings 七杀",
    ("Wood", "Metal", "Yang", "Yin"): "Direct Officer 正官",
    ("Wood", "Water", "Yang", "Yang"): "Indirect Resource 偏印",
    ("Wood", "Water", "Yang", "Yin"): "Direct Resource 正印",
    # Fire Day Master
    ("Fire", "Fire", "Yang", "Yang"): "Friend 比肩",
    ("Fire", "Fire", "Yang", "Yin"): "Rob Wealth 劫财",
    ("Fire", "Earth", "Yang", "Yang"): "Eating God 食神",
    ("Fire", "Earth", "Yang", "Yin"): "Hurting Officer 伤官",
    ("Fire", "Metal", "Yang", "Yang"): "Indirect Wealth 偏财",
    ("Fire", "Metal", "Yang", "Yin"): "Direct Wealth 正财",
    ("Fire", "Water", "Yang", "Yang"): "7 Killings 七杀",
    ("Fire", "Water", "Yang", "Yin"): "Direct Officer 正官",
    ("Fire", "Wood", "Yang", "Yang"): "Indirect Resource 偏印",
    ("Fire", "Wood", "Yang", "Yin"): "Direct Resource 正印",
    # Earth Day Master
    ("Earth", "Earth", "Yang", "Yang"): "Friend 比肩",
    ("Earth", "Earth", "Yang", "Yin"): "Rob Wealth 劫财",
    ("Earth", "Metal", "Yang", "Yang"): "Eating God 食神",
    ("Earth", "Metal", "Yang", "Yin"): "Hurting Officer 伤官",
    ("Earth", "Water", "Yang", "Yang"): "Indirect Wealth 偏财",
    ("Earth", "Water", "Yang", "Yin"): "Direct Wealth 正财",
    ("Earth", "Wood", "Yang", "Yang"): "7 Killings 七杀",
    ("Earth", "Wood", "Yang", "Yin"): "Direct Officer 正官",
    ("Earth", "Fire", "Yang", "Yang"): "Indirect Resource 偏印",
    ("Earth", "Fire", "Yang", "Yin"): "Direct Resource 正印",
    # Metal Day Master
    ("Metal", "Metal", "Yang", "Yang"): "Friend 比肩",
    ("Metal", "Metal", "Yang", "Yin"): "Rob Wealth 劫财",
    ("Metal", "Water", "Yang", "Yang"): "Eating God 食神",
    ("Metal", "Water", "Yang", "Yin"): "Hurting Officer 伤官",
    ("Metal", "Wood", "Yang", "Yang"): "Indirect Wealth 偏财",
    ("Metal", "Wood", "Yang", "Yin"): "Direct Wealth 正财",
    ("Metal", "Fire", "Yang", "Yang"): "7 Killings 七杀",
    ("Metal", "Fire", "Yang", "Yin"): "Direct Officer 正官",
    ("Metal", "Earth", "Yang", "Yang"): "Indirect Resource 偏印",
    ("Metal", "Earth", "Yang", "Yin"): "Direct Resource 正印",
    # Water Day Master
    ("Water", "Water", "Yang", "Yang"): "Friend 比肩",
    ("Water", "Water", "Yang", "Yin"): "Rob Wealth 劫财",
    ("Water", "Wood", "Yang", "Yang"): "Eating God 食神",
    ("Water", "Wood", "Yang", "Yin"): "Hurting Officer 伤官",
    ("Water", "Fire", "Yang", "Yang"): "Indirect Wealth 偏财",
    ("Water", "Fire", "Yang", "Yin"): "Direct Wealth 正财",
    ("Water", "Earth", "Yang", "Yang"): "7 Killings 七杀",
    ("Water", "Earth", "Yang", "Yin"): "Direct Officer 正官",
    ("Water", "Metal", "Yang", "Yang"): "Indirect Resource 偏印",
    ("Water", "Metal", "Yang", "Yin"): "Direct Resource 正印",
}

# Profile types based on dominant Ten God
PROFILE_TYPES = {
    "Direct Wealth": "Diplomat 正财格",
    "Indirect Wealth": "Pioneer 偏财格",
    "Direct Officer": "Director 正官格",
    "7 Killings": "Warrior 七杀格",
    "Direct Resource": "Analyzer 正印格",
    "Indirect Resource": "Philosopher 偏印格",
    "Eating God": "Artist 食神格",
    "Hurting Officer": "Performer 伤官格",
    "Friend": "Leader 比肩格",
    "Rob Wealth": "Competitor 劫财格"
}

# Hour branch mapping (using Chinese double-hour system)
HOUR_BRANCHES = {
    (23, 1): "Zi 子",
    (1, 3): "Chou 丑",
    (3, 5): "Yin 寅",
    (5, 7): "Mao 卯",
    (7, 9): "Chen 辰",
    (9, 11): "Si 巳",
    (11, 13): "Wu 午",
    (13, 15): "Wei 未",
    (15, 17): "Shen 申",
    (17, 19): "You 酉",
    (19, 21): "Xu 戌",
    (21, 23): "Hai 亥"
}

# Simplified Solar Terms (approximate dates for month pillar)
SOLAR_TERMS = [
    (2, 4),   # Li Chun - Start of Yin month
    (3, 6),   # Jing Zhe - Start of Mao month
    (4, 5),   # Qing Ming - Start of Chen month
    (5, 6),   # Li Xia - Start of Si month
    (6, 6),   # Mang Zhong - Start of Wu month
    (7, 7),   # Xiao Shu - Start of Wei month
    (8, 8),   # Li Qiu - Start of Shen month
    (9, 8),   # Bai Lu - Start of You month
    (10, 8),  # Han Lu - Start of Xu month
    (11, 7),  # Li Dong - Start of Hai month
    (12, 7),  # Da Xue - Start of Zi month
    (1, 6),   # Xiao Han - Start of Chou month
]


# ============================================================
# CALCULATION FUNCTIONS
# ============================================================

def get_stem_index(stem_str):
    """Get index of stem (0-9)"""
    for i, s in enumerate(STEMS):
        if stem_str in s or s.split()[0] == stem_str:
            return i
    return 0

def get_branch_index(branch_str):
    """Get index of branch (0-11)"""
    for i, b in enumerate(BRANCHES):
        if branch_str in b or b.split()[0] == branch_str:
            return i
    return 0

def calculate_year_pillar(year):
    """Calculate Year Pillar stem and branch"""
    # Year stem: (year - 4) % 10
    stem_index = (year - 4) % 10
    # Year branch: (year - 4) % 12
    branch_index = (year - 4) % 12
    return STEMS[stem_index], BRANCHES[branch_index]

def calculate_month_pillar(year, month, day):
    """Calculate Month Pillar using solar terms"""
    # Determine solar month (Yin = 0, Mao = 1, etc.)
    solar_month = month - 2  # Default
    
    # Check if before or after solar term for the month
    for i, (term_month, term_day) in enumerate(SOLAR_TERMS):
        if month == term_month and day < term_day:
            solar_month = (i - 1) % 12
            break
        elif month == term_month and day >= term_day:
            solar_month = i
            break
    
    # Adjust for Yin as first month
    solar_month = (month - 2) % 12
    if day < SOLAR_TERMS[solar_month % 12][1]:
        solar_month = (solar_month - 1) % 12
    
    # Month branch
    branch_index = (solar_month + 2) % 12  # Yin = index 2
    
    # Month stem depends on year stem
    year_stem, _ = calculate_year_pillar(year)
    year_stem_index = get_stem_index(year_stem)
    
    # Formula: (year_stem_index % 5) * 2 + solar_month + 2
    stem_index = ((year_stem_index % 5) * 2 + solar_month + 2) % 10
    
    return STEMS[stem_index], BRANCHES[branch_index]

def calculate_day_pillar(year, month, day):
    """Calculate Day Pillar using simplified formula"""
    # Reference date: Jan 1, 1900 was Jia Chen (stem=0, branch=4)
    from datetime import date as dt
    ref_date = dt(1900, 1, 1)
    target_date = dt(year, month, day)
    days_diff = (target_date - ref_date).days
    
    # Jan 1, 1900 = Jia Chen (stem 0, branch 4)
    stem_index = (days_diff + 0) % 10
    branch_index = (days_diff + 4) % 12
    
    return STEMS[stem_index], BRANCHES[branch_index]

def calculate_hour_pillar(day_stem, hour, minute=0):
    """Calculate Hour Pillar from day stem and birth hour"""
    if hour is None:
        return None, None
    
    # Adjust for minute (if >= 30 min, could affect boundary hours)
    adjusted_hour = hour
    
    # Get hour branch
    hour_branch = None
    for (start, end), branch in HOUR_BRANCHES.items():
        if start == 23:
            if hour >= 23 or hour < end:
                hour_branch = branch
                break
        elif start <= hour < end:
            hour_branch = branch
            break
    
    if not hour_branch:
        hour_branch = BRANCHES[0]  # Default to Zi
    
    # Hour stem depends on day stem
    day_stem_index = get_stem_index(day_stem)
    hour_branch_index = get_branch_index(hour_branch)
    
    # Formula: (day_stem_index % 5) * 2 + hour_branch_index
    stem_index = ((day_stem_index % 5) * 2 + hour_branch_index) % 10
    
    return STEMS[stem_index], hour_branch

def get_ten_god(dm_element, dm_polarity, target_element, target_polarity):
    """Get Ten God relationship"""
    # Simplify polarity matching - same polarity = indirect, different = direct
    polarity_match = "Yang" if dm_polarity == target_polarity else "Yin"
    
    key = (dm_element, target_element, "Yang", polarity_match)
    return TEN_GODS.get(key, "Unknown")

def assess_dm_strength(pillars, dm_element):
    """Assess Day Master strength (simplified)"""
    support_count = 0
    weaken_count = 0
    
    # Element relationships
    produces = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal", 
                "Metal": "Water", "Water": "Wood"}
    produced_by = {v: k for k, v in produces.items()}
    
    for pillar_name, (stem, branch) in pillars.items():
        if stem and branch:
            stem_name = stem.split()[0]
            branch_name = branch.split()[0]
            
            stem_element = STEM_ELEMENTS.get(stem_name, "")
            branch_element = BRANCH_ELEMENTS.get(branch_name, "")
            
            # Check support (same element or produces DM)
            for elem in [stem_element, branch_element]:
                if elem == dm_element:
                    support_count += 1
                elif produced_by.get(dm_element) == elem:
                    support_count += 1
                elif produces.get(dm_element) == elem:
                    weaken_count += 1
                elif produces.get(elem) == dm_element:
                    weaken_count += 0.5  # Controlling element
    
    # Calculate strength score (1-10)
    total = support_count + weaken_count
    if total == 0:
        strength_score = 5
    else:
        ratio = support_count / total
        strength_score = int(ratio * 10)
        strength_score = max(1, min(10, strength_score))
    
    # Determine strength label
    if strength_score >= 7:
        strength = "Strong"
    elif strength_score >= 4:
        strength = "Balanced"
    else:
        strength = "Weak"
    
    return strength, strength_score

def get_useful_gods(dm_element, strength):
    """Determine useful gods based on DM and strength"""
    produces = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal", 
                "Metal": "Water", "Water": "Wood"}
    produced_by = {v: k for k, v in produces.items()}
    controls = {"Wood": "Earth", "Fire": "Metal", "Earth": "Water",
                "Metal": "Wood", "Water": "Fire"}
    
    if strength == "Weak":
        # Weak DM needs support - same element and resource
        useful = [dm_element, produced_by.get(dm_element, "")]
        unfavorable = [produces.get(dm_element, "")]
    else:
        # Strong DM needs output/control
        useful = [produces.get(dm_element, ""), controls.get(dm_element, "")]
        unfavorable = [dm_element, produced_by.get(dm_element, "")]
    
    return [u for u in useful if u], [u for u in unfavorable if u]

def detect_special_structures(pillars, dm_element):
    """Detect special BaZi structures"""
    structures = {
        "wealth_vault": False,
        "nobleman": False,
        "other": []
    }
    
    # Check for Wealth Vault (Chen, Xu, Chou, Wei)
    vault_branches = ["Chen", "Xu", "Chou", "Wei"]
    for pillar_name, (stem, branch) in pillars.items():
        if branch:
            branch_name = branch.split()[0]
            if branch_name in vault_branches:
                structures["wealth_vault"] = True
                break
    
    # Check for Nobleman (Yi-Zi/Shen, Jia-Chou/Wei, etc.) - simplified
    dm_stem = pillars.get("Day", (None, None))[0]
    if dm_stem:
        dm_name = dm_stem.split()[0]
        nobleman_map = {
            "Jia": ["Chou", "Wei"], "Wu": ["Chou", "Wei"],
            "Yi": ["Zi", "Shen"], "Ji": ["Zi", "Shen"],
            "Bing": ["Hai", "You"], "Ding": ["Hai", "You"],
            "Geng": ["Chou", "Wei"], "Xin": ["Yin", "Wu"],
            "Ren": ["Mao", "Si"], "Gui": ["Mao", "Si"]
        }
        nobleman_branches = nobleman_map.get(dm_name, [])
        for pillar_name, (stem, branch) in pillars.items():
            if branch:
                branch_name = branch.split()[0]
                if branch_name in nobleman_branches:
                    structures["nobleman"] = True
                    break
    
    return structures


# ============================================================
# PAGE UI
# ============================================================

st.set_page_config(page_title="BaZi Calculator", page_icon="🎂", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .bazi-title { color: #FFD700; font-size: 2.5rem; font-weight: bold; }
    .pillar-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 2px solid #FFD700;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem;
    }
    .pillar-stem { color: #FFD700; font-size: 1.5rem; font-weight: bold; }
    .pillar-branch { color: #87CEEB; font-size: 1.3rem; }
    .pillar-label { color: #888; font-size: 0.9rem; margin-bottom: 0.5rem; }
    .element-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.8rem;
        margin-top: 0.5rem;
    }
    .wood { background: #228B22; color: white; }
    .fire { background: #DC143C; color: white; }
    .earth { background: #DAA520; color: black; }
    .metal { background: #C0C0C0; color: black; }
    .water { background: #4169E1; color: white; }
    .save-success {
        background: #1a472a;
        border: 1px solid #2ecc71;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .dm-highlight {
        background: linear-gradient(135deg, #2d1f3d 0%, #1a1a2e 100%);
        border: 2px solid #9B59B6;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="bazi-title">🎂 BaZi Calculator 八字计算器</p>', unsafe_allow_html=True)
st.caption("Calculate your Four Pillars of Destiny")

st.divider()

# ============================================================
# BIRTH DATA INPUT
# ============================================================

st.subheader("📅 Enter Birth Information")

col1, col2 = st.columns(2)

with col1:
    birth_date = st.date_input(
        "Birth Date",
        value=date(1988, 1, 6),  # Default to Ben's birthday
        min_value=date(1900, 1, 1),
        max_value=date.today(),
        help="Select your birth date"
    )

with col2:
    # Unknown time checkbox
    unknown_time = st.checkbox(
        "⏰ I don't know my birth time",
        value=False,
        help="Check this if you don't know your exact birth hour. Hour Pillar will be skipped."
    )

# Time inputs (only show if birth time is known)
if not unknown_time:
    time_col1, time_col2 = st.columns(2)
    
    with time_col1:
        birth_hour = st.selectbox(
            "Birth Hour (24h)",
            options=list(range(0, 24)),
            index=12,
            format_func=lambda x: f"{x:02d}:00 - {(x+1)%24:02d}:00",
            help="Select the hour you were born"
        )
    
    with time_col2:
        birth_minute = st.selectbox(
            "Birth Minute",
            options=[0, 15, 30, 45],
            index=0,
            format_func=lambda x: f":{x:02d}",
            help="Select approximate minute (optional for accuracy)"
        )
else:
    birth_hour = None
    birth_minute = None
    st.info("💡 Without birth time, the Hour Pillar cannot be calculated. This affects accuracy of analysis.")

st.divider()

# ============================================================
# CALCULATE BUTTON
# ============================================================

if st.button("🔮 Calculate BaZi", type="primary", use_container_width=True):
    with st.spinner("Calculating your Four Pillars..."):
        year = birth_date.year
        month = birth_date.month
        day = birth_date.day
        
        # Calculate pillars
        year_stem, year_branch = calculate_year_pillar(year)
        month_stem, month_branch = calculate_month_pillar(year, month, day)
        day_stem, day_branch = calculate_day_pillar(year, month, day)
        
        if not unknown_time:
            hour_stem, hour_branch = calculate_hour_pillar(day_stem, birth_hour, birth_minute)
        else:
            hour_stem, hour_branch = None, None
        
        # Store pillars
        pillars = {
            "Year": (year_stem, year_branch),
            "Month": (month_stem, month_branch),
            "Day": (day_stem, day_branch),
            "Hour": (hour_stem, hour_branch)
        }
        
        # Get Day Master info
        dm_stem = day_stem.split()[0]
        dm_element = STEM_ELEMENTS[dm_stem]
        dm_polarity = STEM_POLARITY[dm_stem]
        
        # Assess strength
        strength, strength_score = assess_dm_strength(pillars, dm_element)
        
        # Get useful gods
        useful, unfavorable = get_useful_gods(dm_element, strength)
        
        # Detect structures
        structures = detect_special_structures(pillars, dm_element)
        
        # Store in session state
        st.session_state.bazi_calculated = True
        st.session_state.pillars = pillars
        st.session_state.bazi_result = {
            "day_master": day_stem,
            "element": dm_element,
            "polarity": dm_polarity,
            "strength": strength,
            "strength_score": strength_score,
            "useful_gods": useful,
            "unfavorable": unfavorable,
            "wealth_vault": structures["wealth_vault"],
            "nobleman": structures["nobleman"],
            "birth_date": birth_date.isoformat(),
            "birth_time": f"{birth_hour:02d}:{birth_minute:02d}" if birth_hour is not None else "Unknown",
            "unknown_time": unknown_time
        }
        
        st.success("✅ BaZi calculated successfully!")

# ============================================================
# DISPLAY RESULTS
# ============================================================

if st.session_state.get("bazi_calculated"):
    pillars = st.session_state.pillars
    result = st.session_state.bazi_result
    
    st.subheader("🏛️ Your Four Pillars 四柱")
    
    # Display Four Pillars
    cols = st.columns(4)
    pillar_names = ["Hour", "Day", "Month", "Year"]
    pillar_labels = ["时柱", "日柱", "月柱", "年柱"]
    
    for i, (name, label) in enumerate(zip(pillar_names, pillar_labels)):
        with cols[i]:
            stem, branch = pillars[name]
            
            if stem and branch:
                stem_name = stem.split()[0]
                branch_name = branch.split()[0]
                stem_element = STEM_ELEMENTS.get(stem_name, "")
                branch_element = BRANCH_ELEMENTS.get(branch_name, "")
                
                st.markdown(f"""
                <div class="pillar-card">
                    <div class="pillar-label">{name} {label}</div>
                    <div class="pillar-stem">{stem}</div>
                    <div class="pillar-branch">{branch}</div>
                    <div>
                        <span class="element-badge {stem_element.lower()}">{stem_element}</span>
                        <span class="element-badge {branch_element.lower()}">{branch_element}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="pillar-card" style="opacity: 0.5;">
                    <div class="pillar-label">{name} {label}</div>
                    <div class="pillar-stem">--</div>
                    <div class="pillar-branch">Unknown</div>
                    <div><span class="element-badge">No Time</span></div>
                </div>
                """, unsafe_allow_html=True)
    
    st.divider()
    
    # Day Master Analysis
    st.subheader("👤 Day Master Analysis")
    
    dm_col1, dm_col2 = st.columns(2)
    
    with dm_col1:
        st.markdown(f"""
        <div class="dm-highlight">
            <h3 style="color: #FFD700; margin: 0;">🌟 {result['day_master']}</h3>
            <p style="color: #9B59B6; font-size: 1.2rem;">{result['polarity']} {result['element']}</p>
            <p style="color: #888;">Strength: <strong style="color: {'#2ecc71' if result['strength'] == 'Strong' else '#e74c3c' if result['strength'] == 'Weak' else '#f39c12'}">{result['strength']}</strong> ({result['strength_score']}/10)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with dm_col2:
        st.markdown("**✅ Useful Gods (有用神)**")
        for god in result['useful_gods']:
            element_class = god.lower()
            st.markdown(f'<span class="element-badge {element_class}">{god}</span>', unsafe_allow_html=True)
        
        st.markdown("**❌ Unfavorable (忌神)**")
        for god in result['unfavorable']:
            element_class = god.lower()
            st.markdown(f'<span class="element-badge {element_class}">{god}</span>', unsafe_allow_html=True)
    
    # Special Structures
    st.markdown("**🏆 Special Structures**")
    structures_found = []
    if result['wealth_vault']:
        structures_found.append("💰 Wealth Vault (财库)")
    if result['nobleman']:
        structures_found.append("👑 Nobleman (贵人)")
    
    if structures_found:
        for s in structures_found:
            st.success(s)
    else:
        st.info("No special structures detected")
    
    st.divider()
    
    # ============================================================
    # SAVE TO PROFILE BUTTON
    # ============================================================
    
    st.subheader("💾 Save to Profile")
    
    if st.button("📥 Save BaZi to Profile", type="primary", use_container_width=True):
        # Save to user_profile (the correct session state key)
        st.session_state.user_profile = {
            'day_master': result['day_master'],
            'element': result['element'],
            'polarity': result['polarity'],
            'strength': result['strength'],
            'strength_score': result['strength_score'],
            'useful_gods': result['useful_gods'],
            'unfavorable': result['unfavorable'],
            'wealth_vault': result['wealth_vault'],
            'nobleman': result['nobleman'],
            'birth_date': result['birth_date'],
            'birth_time': result['birth_time'],
            'unknown_time': result.get('unknown_time', False)
        }
        
        st.markdown("""
        <div class="save-success">
            ✅ <strong>BaZi profile saved successfully!</strong><br>
            Your profile is now available in the sidebar and will be included in QMDJ exports.
        </div>
        """, unsafe_allow_html=True)
        
        st.balloons()
        st.rerun()  # Refresh to show in sidebar

# ============================================================
# SIDEBAR PROFILE DISPLAY
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
st.caption("🌟 Ming Qimen 明奇门 | BaZi Calculator v4.0")
