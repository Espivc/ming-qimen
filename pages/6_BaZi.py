"""
BaZi Calculator Page
====================
Ming Qimen 明奇门 v3.0 - Page 6

Features:
- Birth date/time input
- Four Pillars calculation with hidden stems
- Ten Gods complete mapping
- Day Master strength assessment
- Useful Gods recommendation
- Special structures detection
- Integration with QMDJ charts
"""

import streamlit as st
from datetime import datetime, date, time
import json
from typing import Dict, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import from core module, fallback to inline if not available
try:
    from core.bazi_calculator_core import (
        HEAVENLY_STEMS, EARTHLY_BRANCHES, 
        generate_complete_ten_gods_mapping,
        assess_day_master_strength,
        calculate_useful_gods,
        detect_special_structures,
        calculate_activation_percentage,
        get_stem_by_chinese
    )
    CORE_IMPORTED = True
except ImportError:
    CORE_IMPORTED = False
    # Fallback: use inline constants (defined below)

# =============================================================================
# CONSTANTS (Inline for standalone operation)
# =============================================================================

HEAVENLY_STEMS = [
    {"chinese": "甲", "pinyin": "Jia", "element": "Wood", "polarity": "Yang", "index": 0},
    {"chinese": "乙", "pinyin": "Yi", "element": "Wood", "polarity": "Yin", "index": 1},
    {"chinese": "丙", "pinyin": "Bing", "element": "Fire", "polarity": "Yang", "index": 2},
    {"chinese": "丁", "pinyin": "Ding", "element": "Fire", "polarity": "Yin", "index": 3},
    {"chinese": "戊", "pinyin": "Wu", "element": "Earth", "polarity": "Yang", "index": 4},
    {"chinese": "己", "pinyin": "Ji", "element": "Earth", "polarity": "Yin", "index": 5},
    {"chinese": "庚", "pinyin": "Geng", "element": "Metal", "polarity": "Yang", "index": 6},
    {"chinese": "辛", "pinyin": "Xin", "element": "Metal", "polarity": "Yin", "index": 7},
    {"chinese": "壬", "pinyin": "Ren", "element": "Water", "polarity": "Yang", "index": 8},
    {"chinese": "癸", "pinyin": "Gui", "element": "Water", "polarity": "Yin", "index": 9},
]

EARTHLY_BRANCHES = [
    {"chinese": "子", "pinyin": "Zi", "animal": "Rat", "element": "Water", "polarity": "Yang", 
     "hidden_stems": ["癸"], "index": 0},
    {"chinese": "丑", "pinyin": "Chou", "animal": "Ox", "element": "Earth", "polarity": "Yin",
     "hidden_stems": ["己", "癸", "辛"], "index": 1},
    {"chinese": "寅", "pinyin": "Yin", "animal": "Tiger", "element": "Wood", "polarity": "Yang",
     "hidden_stems": ["甲", "丙", "戊"], "index": 2},
    {"chinese": "卯", "pinyin": "Mao", "animal": "Rabbit", "element": "Wood", "polarity": "Yin",
     "hidden_stems": ["乙"], "index": 3},
    {"chinese": "辰", "pinyin": "Chen", "animal": "Dragon", "element": "Earth", "polarity": "Yang",
     "hidden_stems": ["戊", "乙", "癸"], "index": 4},
    {"chinese": "巳", "pinyin": "Si", "animal": "Snake", "element": "Fire", "polarity": "Yin",
     "hidden_stems": ["丙", "庚", "戊"], "index": 5},
    {"chinese": "午", "pinyin": "Wu", "animal": "Horse", "element": "Fire", "polarity": "Yang",
     "hidden_stems": ["丁", "己"], "index": 6},
    {"chinese": "未", "pinyin": "Wei", "animal": "Goat", "element": "Earth", "polarity": "Yin",
     "hidden_stems": ["己", "丁", "乙"], "index": 7},
    {"chinese": "申", "pinyin": "Shen", "animal": "Monkey", "element": "Metal", "polarity": "Yang",
     "hidden_stems": ["庚", "壬", "戊"], "index": 8},
    {"chinese": "酉", "pinyin": "You", "animal": "Rooster", "element": "Metal", "polarity": "Yin",
     "hidden_stems": ["辛"], "index": 9},
    {"chinese": "戌", "pinyin": "Xu", "animal": "Dog", "element": "Earth", "polarity": "Yang",
     "hidden_stems": ["戊", "辛", "丁"], "index": 10},
    {"chinese": "亥", "pinyin": "Hai", "animal": "Pig", "element": "Water", "polarity": "Yin",
     "hidden_stems": ["壬", "甲"], "index": 11},
]

ELEMENT_COLORS = {
    "Wood": "#22C55E",   # Green
    "Fire": "#EF4444",   # Red
    "Earth": "#A16207",  # Brown
    "Metal": "#9CA3AF",  # Gray/Silver
    "Water": "#3B82F6"   # Blue
}

# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="BaZi Calculator | 八字计算器",
    page_icon="🎴",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #1a1a2e;
    }
    .pillar-card {
        background: linear-gradient(135deg, #2d2d44 0%, #1a1a2e 100%);
        border: 1px solid #d4af37;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin: 5px;
    }
    .pillar-title {
        color: #d4af37;
        font-size: 14px;
        margin-bottom: 10px;
    }
    .stem-display {
        font-size: 36px;
        font-weight: bold;
        margin: 5px 0;
    }
    .branch-display {
        font-size: 36px;
        font-weight: bold;
        margin: 5px 0;
    }
    .element-tag {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
        margin: 2px;
    }
    .hidden-stems {
        font-size: 11px;
        color: #888;
        margin-top: 5px;
    }
    .ten-god-badge {
        background: #d4af37;
        color: #1a1a2e;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
    .strength-bar {
        height: 20px;
        border-radius: 10px;
        background: #333;
        overflow: hidden;
    }
    .strength-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    .useful-god-card {
        background: #2d2d44;
        border-left: 4px solid #22C55E;
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 0 8px 8px 0;
    }
    .unfavorable-card {
        background: #2d2d44;
        border-left: 4px solid #EF4444;
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 0 8px 8px 0;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

if 'bazi_calculated' not in st.session_state:
    st.session_state.bazi_calculated = False
if 'bazi_data' not in st.session_state:
    st.session_state.bazi_data = None
if 'birth_datetime' not in st.session_state:
    st.session_state.birth_datetime = None


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_stem_color(element: str) -> str:
    return ELEMENT_COLORS.get(element, "#FFFFFF")

def get_stem_by_index(index: int) -> Dict:
    return HEAVENLY_STEMS[index % 10]

def get_branch_by_index(index: int) -> Dict:
    return EARTHLY_BRANCHES[index % 12]

def get_stem_by_chinese(chinese: str) -> Optional[Dict]:
    for stem in HEAVENLY_STEMS:
        if stem["chinese"] == chinese:
            return stem
    return None


# =============================================================================
# FOUR PILLARS CALCULATION (Simplified Algorithm)
# =============================================================================

def calculate_year_pillar(year: int) -> Dict:
    """Calculate Year Pillar from year"""
    # Stem: (year - 4) % 10
    stem_index = (year - 4) % 10
    # Branch: (year - 4) % 12
    branch_index = (year - 4) % 12
    
    stem = get_stem_by_index(stem_index)
    branch = get_branch_by_index(branch_index)
    
    return {
        "stem": stem,
        "branch": branch,
        "pillar_name": "Year 年柱",
        "pillar_chinese": f"{stem['chinese']}{branch['chinese']}",
        "pillar_pinyin": f"{stem['pinyin']} {branch['pinyin']}"
    }

def calculate_month_pillar(year: int, month: int, year_stem_index: int) -> Dict:
    """
    Calculate Month Pillar
    Note: This is simplified. Full calculation requires solar terms (节气)
    """
    # Month branch: Tiger (寅) = Month 1 (Feb), etc.
    branch_index = (month + 1) % 12
    
    # Month stem follows a pattern based on year stem
    # Formula: (year_stem_index * 2 + month) % 10
    stem_index = (year_stem_index * 2 + month) % 10
    
    stem = get_stem_by_index(stem_index)
    branch = get_branch_by_index(branch_index)
    
    return {
        "stem": stem,
        "branch": branch,
        "pillar_name": "Month 月柱",
        "pillar_chinese": f"{stem['chinese']}{branch['chinese']}",
        "pillar_pinyin": f"{stem['pinyin']} {branch['pinyin']}"
    }

def calculate_day_pillar(year: int, month: int, day: int) -> Dict:
    """
    Calculate Day Pillar using the standard formula
    This is a simplified version - production should use a lookup table
    """
    # Using a simplified calculation
    # In production, use a proper Ten Thousand Year Calendar lookup
    
    # Reference point: Jan 1, 1900 = 甲子 (Jia Zi)
    from datetime import date as dt_date
    reference = dt_date(1900, 1, 1)
    target = dt_date(year, month, day)
    days_diff = (target - reference).days
    
    stem_index = days_diff % 10
    branch_index = days_diff % 12
    
    stem = get_stem_by_index(stem_index)
    branch = get_branch_by_index(branch_index)
    
    return {
        "stem": stem,
        "branch": branch,
        "pillar_name": "Day 日柱",
        "pillar_chinese": f"{stem['chinese']}{branch['chinese']}",
        "pillar_pinyin": f"{stem['pinyin']} {branch['pinyin']}"
    }

def calculate_hour_pillar(hour: int, day_stem_index: int) -> Dict:
    """Calculate Hour Pillar"""
    # Hour branch
    if hour == 23 or hour == 0:
        branch_index = 0  # Zi
    else:
        branch_index = ((hour + 1) // 2) % 12
    
    # Hour stem follows pattern based on day stem
    # Formula: (day_stem_index * 2 + branch_index) % 10
    stem_index = (day_stem_index * 2 + branch_index) % 10
    
    stem = get_stem_by_index(stem_index)
    branch = get_branch_by_index(branch_index)
    
    return {
        "stem": stem,
        "branch": branch,
        "pillar_name": "Hour 时柱",
        "pillar_chinese": f"{stem['chinese']}{branch['chinese']}",
        "pillar_pinyin": f"{stem['pinyin']} {branch['pinyin']}"
    }

def calculate_four_pillars(birth_dt: datetime) -> Dict:
    """Calculate complete Four Pillars"""
    year = birth_dt.year
    month = birth_dt.month
    day = birth_dt.day
    hour = birth_dt.hour
    
    year_pillar = calculate_year_pillar(year)
    month_pillar = calculate_month_pillar(year, month, year_pillar["stem"]["index"])
    day_pillar = calculate_day_pillar(year, month, day)
    hour_pillar = calculate_hour_pillar(hour, day_pillar["stem"]["index"])
    
    return {
        "year": year_pillar,
        "month": month_pillar,
        "day": day_pillar,
        "hour": hour_pillar,
        "day_master": day_pillar["stem"]
    }


# =============================================================================
# TEN GODS CALCULATION
# =============================================================================

ELEMENT_PRODUCES = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal", "Metal": "Water", "Water": "Wood"}
ELEMENT_CONTROLS = {"Wood": "Earth", "Fire": "Metal", "Earth": "Water", "Metal": "Wood", "Water": "Fire"}
ELEMENT_PRODUCED_BY = {"Wood": "Water", "Fire": "Wood", "Earth": "Fire", "Metal": "Earth", "Water": "Metal"}
ELEMENT_CONTROLLED_BY = {"Wood": "Metal", "Fire": "Water", "Earth": "Wood", "Metal": "Fire", "Water": "Earth"}

TEN_GODS_NAMES = {
    "same_same": ("Rob Wealth", "劫财"),
    "same_diff": ("Friend", "比肩"),
    "resource_same": ("Indirect Resource", "偏印"),
    "resource_diff": ("Direct Resource", "正印"),
    "output_same": ("Hurting Officer", "伤官"),
    "output_diff": ("Eating God", "食神"),
    "wealth_same": ("Indirect Wealth", "偏财"),
    "wealth_diff": ("Direct Wealth", "正财"),
    "authority_same": ("7 Killings", "七杀"),
    "authority_diff": ("Direct Officer", "正官"),
}

def calculate_ten_god(dm_element: str, dm_polarity: str, 
                      target_element: str, target_polarity: str) -> tuple:
    """Calculate Ten God relationship"""
    same_polarity = (dm_polarity == target_polarity)
    
    if dm_element == target_element:
        return TEN_GODS_NAMES["same_same" if same_polarity else "same_diff"]
    elif ELEMENT_PRODUCED_BY[dm_element] == target_element:
        return TEN_GODS_NAMES["resource_same" if same_polarity else "resource_diff"]
    elif ELEMENT_PRODUCES[dm_element] == target_element:
        return TEN_GODS_NAMES["output_same" if same_polarity else "output_diff"]
    elif ELEMENT_CONTROLS[dm_element] == target_element:
        return TEN_GODS_NAMES["wealth_same" if same_polarity else "wealth_diff"]
    elif ELEMENT_CONTROLLED_BY[dm_element] == target_element:
        return TEN_GODS_NAMES["authority_same" if same_polarity else "authority_diff"]
    
    return ("Unknown", "?")

def generate_ten_gods_mapping(dm_stem: Dict) -> Dict:
    """Generate complete Ten Gods mapping"""
    mapping = {}
    for stem in HEAVENLY_STEMS:
        god_en, god_cn = calculate_ten_god(
            dm_stem["element"], dm_stem["polarity"],
            stem["element"], stem["polarity"]
        )
        mapping[stem["chinese"]] = {
            "stem_chinese": stem["chinese"],
            "stem_pinyin": stem["pinyin"],
            "element": stem["element"],
            "ten_god_en": god_en,
            "ten_god_cn": god_cn
        }
    return mapping


# =============================================================================
# STRENGTH & USEFUL GODS
# =============================================================================

def assess_strength(dm_element: str, month_branch: Dict, pillars: Dict) -> Dict:
    """Assess Day Master strength"""
    # Seasonal strength
    season_map = {
        "Wood": {0: "Strong", 1: "Strong", 2: "Strong", 3: "Weak", 4: "Weak", 5: "Weak",
                 6: "Dead", 7: "Dead", 8: "Dead", 9: "Weak", 10: "Weak", 11: "Strong"},
        "Fire": {0: "Dead", 1: "Weak", 2: "Strong", 3: "Strong", 4: "Strong", 5: "Prosperous",
                 6: "Prosperous", 7: "Weak", 8: "Dead", 9: "Dead", 10: "Weak", 11: "Dead"},
        "Earth": {0: "Weak", 1: "Strong", 2: "Dead", 3: "Dead", 4: "Strong", 5: "Strong",
                  6: "Strong", 7: "Prosperous", 8: "Weak", 9: "Weak", 10: "Prosperous", 11: "Weak"},
        "Metal": {0: "Strong", 1: "Weak", 2: "Dead", 3: "Dead", 4: "Weak", 5: "Weak",
                  6: "Weak", 7: "Strong", 8: "Prosperous", 9: "Prosperous", 10: "Strong", 11: "Strong"},
        "Water": {0: "Prosperous", 1: "Strong", 2: "Weak", 3: "Weak", 4: "Weak", 5: "Dead",
                  6: "Dead", 7: "Dead", 8: "Strong", 9: "Strong", 10: "Weak", 11: "Prosperous"}
    }
    
    branch_index = month_branch["index"]
    seasonal = season_map.get(dm_element, {}).get(branch_index, "Balanced")
    
    # Count supports
    support = 0
    drain = 0
    for pillar_name in ["year", "month", "day", "hour"]:
        if pillar_name in pillars:
            p = pillars[pillar_name]
            stem_el = p["stem"]["element"]
            if stem_el == dm_element or ELEMENT_PRODUCED_BY[dm_element] == stem_el:
                support += 1
            elif ELEMENT_PRODUCES[dm_element] == stem_el or ELEMENT_CONTROLS[dm_element] == stem_el:
                drain += 1
    
    # Calculate score
    base_scores = {"Prosperous": 8, "Strong": 7, "Balanced": 5, "Weak": 3, "Dead": 2}
    score = base_scores.get(seasonal, 5) + (support - drain) * 0.5
    score = max(1, min(10, score))
    
    if score >= 8:
        category = "Extremely Strong"
    elif score >= 6:
        category = "Strong"
    elif score >= 4:
        category = "Balanced"
    elif score >= 2:
        category = "Weak"
    else:
        category = "Extremely Weak"
    
    return {
        "seasonal_strength": seasonal,
        "support_count": support,
        "drain_count": drain,
        "score": round(score, 1),
        "category": category
    }

def calculate_useful_gods(dm_element: str, strength_category: str) -> Dict:
    """Calculate Useful Gods"""
    resource = ELEMENT_PRODUCED_BY[dm_element]
    companion = dm_element
    output = ELEMENT_PRODUCES[dm_element]
    wealth = ELEMENT_CONTROLS[dm_element]
    authority = ELEMENT_CONTROLLED_BY[dm_element]
    
    if "Weak" in strength_category or "Dead" in strength_category:
        return {
            "primary": resource,
            "secondary": companion,
            "tertiary": None,
            "unfavorable": [output, wealth],
            "reasoning": f"Weak {dm_element} needs {resource} (Resource) to strengthen and {companion} (Companion) for support."
        }
    elif "Strong" in strength_category:
        return {
            "primary": output,
            "secondary": wealth,
            "tertiary": authority,
            "unfavorable": [resource, companion],
            "reasoning": f"Strong {dm_element} needs {output} (Output) to drain energy and {wealth} (Wealth) for purpose."
        }
    else:
        return {
            "primary": output,
            "secondary": wealth,
            "tertiary": resource,
            "unfavorable": [],
            "reasoning": f"Balanced {dm_element} benefits from most elements."
        }


# =============================================================================
# SPECIAL STRUCTURES
# =============================================================================

def detect_structures(pillars: Dict, dm_stem: Dict) -> Dict:
    """Detect special structures"""
    structures = {
        "wealth_vault": False,
        "nobleman_present": False,
        "nobleman_branches": [],
        "six_combinations": [],
        "six_clashes": []
    }
    
    # Collect branches
    branches = []
    for pn in ["year", "month", "day", "hour"]:
        if pn in pillars:
            branches.append(pillars[pn]["branch"]["chinese"])
    
    # Wealth Vault
    vault_map = {"Wood": "未", "Fire": "戌", "Earth": "辰", "Metal": "丑", "Water": "辰"}
    vault = vault_map.get(dm_stem["element"])
    if vault and vault in branches:
        structures["wealth_vault"] = True
    
    # Nobleman
    nobleman_map = {
        "甲": ["丑", "未"], "戊": ["丑", "未"], "庚": ["丑", "未"],
        "乙": ["子", "申"], "己": ["子", "申"],
        "丙": ["亥", "酉"], "丁": ["亥", "酉"],
        "辛": ["寅", "午"],
        "壬": ["卯", "巳"], "癸": ["卯", "巳"]
    }
    nobles = nobleman_map.get(dm_stem["chinese"], [])
    for n in nobles:
        if n in branches:
            structures["nobleman_present"] = True
            structures["nobleman_branches"].append(n)
    
    return structures


# =============================================================================
# ACTIVATION PERCENTAGE
# =============================================================================

def calculate_activation(useful_gods: Dict, pillars: Dict) -> Dict:
    """Calculate useful god activation percentage"""
    elements = {"Wood": 0, "Fire": 0, "Earth": 0, "Metal": 0, "Water": 0}
    
    for pn in ["year", "month", "day", "hour"]:
        if pn in pillars:
            elements[pillars[pn]["stem"]["element"]] += 1
            elements[pillars[pn]["branch"]["element"]] += 1
    
    total = sum(elements.values())
    if total == 0:
        total = 1
    
    primary = useful_gods.get("primary", "")
    secondary = useful_gods.get("secondary", "")
    unfavorable = useful_gods.get("unfavorable", [])
    
    primary_pct = round((elements.get(primary, 0) / total) * 100, 1)
    secondary_pct = round((elements.get(secondary, 0) / total) * 100, 1)
    unfav_count = sum(elements.get(e, 0) for e in unfavorable)
    unfav_pct = round((unfav_count / total) * 100, 1)
    
    # Activation score
    score = ((primary_pct * 0.5) + (secondary_pct * 0.3) - (unfav_pct * 0.2)) / 10
    score = round(max(0, min(10, score + 5)), 1)
    
    return {
        "primary_element": primary,
        "primary_percentage": primary_pct,
        "secondary_element": secondary,
        "secondary_percentage": secondary_pct,
        "unfavorable_percentage": unfav_pct,
        "activation_score": score
    }


# =============================================================================
# MAIN PAGE UI
# =============================================================================

st.title("🎴 BaZi Calculator | 八字计算器")
st.markdown("---")

# Input Section
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📅 Birth Information")
    
    birth_date = st.date_input(
        "Birth Date 出生日期",
        value=date(1990, 1, 15),
        min_value=date(1900, 1, 1),
        max_value=date.today()
    )
    
    birth_time = st.time_input(
        "Birth Time 出生时间",
        value=time(12, 0)
    )
    
    st.info("⚠️ Note: For accurate results, birth time should be the actual local time at birthplace.")
    
    calculate_btn = st.button("🔮 Calculate BaZi | 计算八字", type="primary", use_container_width=True)

# Calculate when button pressed
if calculate_btn:
    birth_dt = datetime.combine(birth_date, birth_time)
    pillars = calculate_four_pillars(birth_dt)
    
    # Store in session
    st.session_state.bazi_calculated = True
    st.session_state.birth_datetime = birth_dt
    st.session_state.pillars = pillars

# Display Results
if st.session_state.bazi_calculated and 'pillars' in st.session_state:
    pillars = st.session_state.pillars
    dm = pillars["day_master"]
    
    with col2:
        st.subheader("🎴 Four Pillars | 四柱")
        
        # Four Pillars Display
        p_cols = st.columns(4)
        
        for i, pillar_name in enumerate(["hour", "day", "month", "year"]):
            pillar = pillars[pillar_name]
            with p_cols[i]:
                stem = pillar["stem"]
                branch = pillar["branch"]
                
                # Pillar title
                titles = {"year": "Year 年柱", "month": "Month 月柱", 
                          "day": "Day 日柱 ★", "hour": "Hour 时柱"}
                st.markdown(f"**{titles[pillar_name]}**")
                
                # Stem
                st.markdown(f"""
                <div style='text-align: center; padding: 10px; 
                            background: linear-gradient(135deg, #2d2d44, #1a1a2e);
                            border: 1px solid {get_stem_color(stem["element"])};
                            border-radius: 8px; margin: 5px 0;'>
                    <div style='font-size: 32px; color: {get_stem_color(stem["element"])};'>
                        {stem["chinese"]}
                    </div>
                    <div style='font-size: 12px; color: #888;'>{stem["pinyin"]} {stem["element"]}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Branch
                st.markdown(f"""
                <div style='text-align: center; padding: 10px;
                            background: linear-gradient(135deg, #2d2d44, #1a1a2e);
                            border: 1px solid {get_stem_color(branch["element"])};
                            border-radius: 8px; margin: 5px 0;'>
                    <div style='font-size: 32px; color: {get_stem_color(branch["element"])};'>
                        {branch["chinese"]}
                    </div>
                    <div style='font-size: 12px; color: #888;'>{branch["pinyin"]} {branch["animal"]}</div>
                    <div style='font-size: 10px; color: #666;'>藏干: {" ".join(branch["hidden_stems"])}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Day Master Analysis
    st.subheader(f"👤 Day Master Analysis | 日主分析: {dm['chinese']} {dm['pinyin']}")
    
    dm_col1, dm_col2, dm_col3 = st.columns(3)
    
    with dm_col1:
        st.markdown(f"""
        <div style='text-align: center; padding: 20px;
                    background: linear-gradient(135deg, #2d2d44, #1a1a2e);
                    border: 2px solid #d4af37; border-radius: 12px;'>
            <div style='font-size: 48px; color: {get_stem_color(dm["element"])};'>{dm["chinese"]}</div>
            <div style='font-size: 18px; color: #d4af37;'>{dm["pinyin"]}</div>
            <div style='font-size: 14px; color: #fff;'>{dm["polarity"]} {dm["element"]}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Strength Assessment
    strength = assess_strength(dm["element"], pillars["month"]["branch"], pillars)
    
    with dm_col2:
        st.markdown("**Strength Assessment | 强弱分析**")
        st.metric("Seasonal 季节", strength["seasonal_strength"])
        st.metric("Category 类别", strength["category"])
        
        # Strength bar
        score_pct = (strength["score"] / 10) * 100
        bar_color = "#22C55E" if strength["score"] >= 5 else "#EF4444"
        st.markdown(f"""
        <div style='background: #333; border-radius: 10px; height: 20px; overflow: hidden;'>
            <div style='background: {bar_color}; width: {score_pct}%; height: 100%;'></div>
        </div>
        <div style='text-align: center; color: #888;'>Score: {strength["score"]}/10</div>
        """, unsafe_allow_html=True)
    
    # Useful Gods
    useful = calculate_useful_gods(dm["element"], strength["category"])
    
    with dm_col3:
        st.markdown("**Useful Gods | 用神**")
        st.success(f"✅ Primary 主用神: **{useful['primary']}**")
        st.info(f"📌 Secondary 辅用神: **{useful['secondary']}**")
        if useful.get("unfavorable"):
            st.error(f"⛔ Avoid 忌神: **{', '.join(useful['unfavorable'])}**")
    
    st.markdown("---")
    
    # Ten Gods Mapping
    st.subheader("🔟 Ten Gods Mapping | 十神映射")
    
    ten_gods = generate_ten_gods_mapping(dm)
    
    tg_cols = st.columns(5)
    for i, stem in enumerate(HEAVENLY_STEMS):
        with tg_cols[i % 5]:
            god_data = ten_gods[stem["chinese"]]
            st.markdown(f"""
            <div style='text-align: center; padding: 8px;
                        background: #2d2d44; border-radius: 8px;
                        border: 1px solid {get_stem_color(stem["element"])}; margin: 3px 0;'>
                <div style='font-size: 20px; color: {get_stem_color(stem["element"])};'>{stem["chinese"]}</div>
                <div style='font-size: 10px; color: #888;'>{stem["pinyin"]}</div>
                <div style='font-size: 11px; color: #d4af37;'>{god_data["ten_god_cn"]}</div>
                <div style='font-size: 9px; color: #666;'>{god_data["ten_god_en"]}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Special Structures
    st.subheader("⭐ Special Structures | 特殊格局")
    
    structures = detect_structures(pillars, dm)
    
    struct_cols = st.columns(3)
    with struct_cols[0]:
        if structures["wealth_vault"]:
            st.success("💰 Wealth Vault Present | 财库存在")
        else:
            st.info("💰 No Wealth Vault | 无财库")
    
    with struct_cols[1]:
        if structures["nobleman_present"]:
            st.success(f"🌟 Nobleman Present | 贵人存在: {', '.join(structures['nobleman_branches'])}")
        else:
            st.info("🌟 No Nobleman | 无贵人")
    
    with struct_cols[2]:
        activation = calculate_activation(useful, pillars)
        st.metric("Activation Score | 激活分数", f"{activation['activation_score']}/10")
    
    st.markdown("---")
    
    # Export Section
    st.subheader("📤 Export BaZi Data | 导出八字数据")
    
    # Build export data
    export_data = {
        "chart_source": "BaZi Calculator",
        "calculated_at": datetime.now().isoformat(),
        "birth_datetime": st.session_state.birth_datetime.isoformat(),
        "day_master": {
            "stem_chinese": dm["chinese"],
            "stem_pinyin": dm["pinyin"],
            "element": dm["element"],
            "polarity": dm["polarity"],
            "strength": strength["category"],
            "strength_score": strength["score"]
        },
        "four_pillars": {
            "year": {
                "stem": pillars["year"]["stem"],
                "branch": {k: v for k, v in pillars["year"]["branch"].items() if k != "hidden_stems"},
                "hidden_stems": pillars["year"]["branch"]["hidden_stems"]
            },
            "month": {
                "stem": pillars["month"]["stem"],
                "branch": {k: v for k, v in pillars["month"]["branch"].items() if k != "hidden_stems"},
                "hidden_stems": pillars["month"]["branch"]["hidden_stems"]
            },
            "day": {
                "stem": pillars["day"]["stem"],
                "branch": {k: v for k, v in pillars["day"]["branch"].items() if k != "hidden_stems"},
                "hidden_stems": pillars["day"]["branch"]["hidden_stems"]
            },
            "hour": {
                "stem": pillars["hour"]["stem"],
                "branch": {k: v for k, v in pillars["hour"]["branch"].items() if k != "hidden_stems"},
                "hidden_stems": pillars["hour"]["branch"]["hidden_stems"]
            }
        },
        "ten_gods_mapping": ten_gods,
        "useful_gods": useful,
        "useful_god_activation": activation,
        "special_structures": structures,
        "ten_god_profile": {
            "dominant_god": "To be calculated",
            "profile_name": "To be calculated"
        }
    }
    
    # Store for other pages
    st.session_state.bazi_data = export_data
    
    # Display JSON
    with st.expander("📋 View JSON Export"):
        st.code(json.dumps(export_data, indent=2, ensure_ascii=False, default=str), language="json")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.download_button(
            label="⬇️ Download JSON",
            data=json.dumps(export_data, indent=2, ensure_ascii=False, default=str),
            file_name=f"bazi_chart_{birth_date}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col_b:
        if st.button("💾 Save to Profile | 保存到档案", use_container_width=True):
            st.session_state.user_bazi_profile = export_data
            st.success("✅ Saved to session! Available on all pages.")
