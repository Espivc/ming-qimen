"""
BaZi Calculator Page - FIXED v3.1
====================
Ming Qimen 明奇门 - Page 6

FIXED: Now saves to st.session_state.user_profile (not user_bazi_profile)
so it syncs with sidebar and other pages.
"""

import streamlit as st
from datetime import datetime, date, time
import json
from typing import Dict, Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# =============================================================================
# CONSTANTS
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
    "Wood": "#22C55E",
    "Fire": "#EF4444",
    "Earth": "#A16207",
    "Metal": "#9CA3AF",
    "Water": "#3B82F6"
}

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

# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="BaZi Calculator | 八字计算器",
    page_icon="🎴",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background-color: #1a1a2e; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SESSION STATE
# =============================================================================

if 'bazi_calculated' not in st.session_state:
    st.session_state.bazi_calculated = False
if 'bazi_data' not in st.session_state:
    st.session_state.bazi_data = None
if 'birth_datetime' not in st.session_state:
    st.session_state.birth_datetime = None
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_stem_color(element: str) -> str:
    return ELEMENT_COLORS.get(element, "#FFFFFF")

def get_stem_by_index(index: int) -> Dict:
    return HEAVENLY_STEMS[index % 10]

def get_branch_by_index(index: int) -> Dict:
    return EARTHLY_BRANCHES[index % 12]

# =============================================================================
# FOUR PILLARS CALCULATION
# =============================================================================

def calculate_year_pillar(year: int) -> Dict:
    stem_index = (year - 4) % 10
    branch_index = (year - 4) % 12
    stem = get_stem_by_index(stem_index)
    branch = get_branch_by_index(branch_index)
    return {"stem": stem, "branch": branch, "pillar_name": "Year 年柱"}

def calculate_month_pillar(year: int, month: int, year_stem_index: int) -> Dict:
    branch_index = (month + 1) % 12
    stem_index = (year_stem_index * 2 + month) % 10
    stem = get_stem_by_index(stem_index)
    branch = get_branch_by_index(branch_index)
    return {"stem": stem, "branch": branch, "pillar_name": "Month 月柱"}

def calculate_day_pillar(year: int, month: int, day: int) -> Dict:
    from datetime import date as dt_date
    reference = dt_date(1900, 1, 1)
    target = dt_date(year, month, day)
    days_diff = (target - reference).days
    stem_index = days_diff % 10
    branch_index = days_diff % 12
    stem = get_stem_by_index(stem_index)
    branch = get_branch_by_index(branch_index)
    return {"stem": stem, "branch": branch, "pillar_name": "Day 日柱"}

def calculate_hour_pillar(hour: int, day_stem_index: int) -> Dict:
    if hour == 23 or hour == 0:
        branch_index = 0
    else:
        branch_index = ((hour + 1) // 2) % 12
    stem_index = (day_stem_index * 2 + branch_index) % 10
    stem = get_stem_by_index(stem_index)
    branch = get_branch_by_index(branch_index)
    return {"stem": stem, "branch": branch, "pillar_name": "Hour 时柱"}

def calculate_four_pillars(birth_dt: datetime) -> Dict:
    year_pillar = calculate_year_pillar(birth_dt.year)
    month_pillar = calculate_month_pillar(birth_dt.year, birth_dt.month, year_pillar["stem"]["index"])
    day_pillar = calculate_day_pillar(birth_dt.year, birth_dt.month, birth_dt.day)
    hour_pillar = calculate_hour_pillar(birth_dt.hour, day_pillar["stem"]["index"])
    return {
        "year": year_pillar,
        "month": month_pillar,
        "day": day_pillar,
        "hour": hour_pillar,
        "day_master": day_pillar["stem"]
    }

# =============================================================================
# TEN GODS
# =============================================================================

def calculate_ten_god(dm_element: str, dm_polarity: str, target_element: str, target_polarity: str) -> tuple:
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
    mapping = {}
    for stem in HEAVENLY_STEMS:
        god_en, god_cn = calculate_ten_god(dm_stem["element"], dm_stem["polarity"], stem["element"], stem["polarity"])
        mapping[stem["chinese"]] = {"stem_chinese": stem["chinese"], "stem_pinyin": stem["pinyin"], 
                                     "element": stem["element"], "ten_god_en": god_en, "ten_god_cn": god_cn}
    return mapping

# =============================================================================
# STRENGTH & USEFUL GODS
# =============================================================================

def assess_strength(dm_element: str, month_branch: Dict, pillars: Dict) -> Dict:
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
    
    support = 0
    drain = 0
    for pillar_name in ["year", "month", "day", "hour"]:
        if pillar_name in pillars:
            stem_el = pillars[pillar_name]["stem"]["element"]
            if stem_el == dm_element or ELEMENT_PRODUCED_BY[dm_element] == stem_el:
                support += 1
            elif ELEMENT_PRODUCES[dm_element] == stem_el or ELEMENT_CONTROLS[dm_element] == stem_el:
                drain += 1
    
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
    
    return {"seasonal_strength": seasonal, "support_count": support, "drain_count": drain, 
            "score": round(score, 1), "category": category}

def calculate_useful_gods(dm_element: str, strength_category: str) -> Dict:
    resource = ELEMENT_PRODUCED_BY[dm_element]
    companion = dm_element
    output = ELEMENT_PRODUCES[dm_element]
    wealth = ELEMENT_CONTROLS[dm_element]
    authority = ELEMENT_CONTROLLED_BY[dm_element]
    
    if "Weak" in strength_category or "Dead" in strength_category:
        return {"primary": resource, "secondary": companion, "unfavorable": [output, wealth],
                "reasoning": f"Weak {dm_element} needs {resource} (Resource) and {companion} (Companion)."}
    elif "Strong" in strength_category:
        return {"primary": output, "secondary": wealth, "unfavorable": [resource, companion],
                "reasoning": f"Strong {dm_element} needs {output} (Output) and {wealth} (Wealth)."}
    else:
        return {"primary": output, "secondary": wealth, "unfavorable": [],
                "reasoning": f"Balanced {dm_element} benefits from most elements."}

def detect_structures(pillars: Dict, dm_stem: Dict) -> Dict:
    structures = {"wealth_vault": False, "nobleman_present": False, "nobleman_branches": []}
    branches = [pillars[pn]["branch"]["chinese"] for pn in ["year", "month", "day", "hour"] if pn in pillars]
    
    vault_map = {"Wood": "未", "Fire": "戌", "Earth": "辰", "Metal": "丑", "Water": "辰"}
    vault = vault_map.get(dm_stem["element"])
    if vault and vault in branches:
        structures["wealth_vault"] = True
    
    nobleman_map = {"甲": ["丑", "未"], "戊": ["丑", "未"], "庚": ["丑", "未"],
                    "乙": ["子", "申"], "己": ["子", "申"], "丙": ["亥", "酉"], "丁": ["亥", "酉"],
                    "辛": ["寅", "午"], "壬": ["卯", "巳"], "癸": ["卯", "巳"]}
    nobles = nobleman_map.get(dm_stem["chinese"], [])
    for n in nobles:
        if n in branches:
            structures["nobleman_present"] = True
            structures["nobleman_branches"].append(n)
    return structures

# =============================================================================
# MAIN UI
# =============================================================================

st.title("🎴 BaZi Calculator | 八字计算器")
st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📅 Birth Information")
    birth_date = st.date_input("Birth Date 出生日期", value=date(1990, 1, 15), 
                                min_value=date(1900, 1, 1), max_value=date.today())
    birth_time = st.time_input("Birth Time 出生时间", value=time(12, 0))
    st.warning("⚠️ Note: For accurate results, use actual local birth time.")
    calculate_btn = st.button("🔮 Calculate BaZi | 计算八字", type="primary", use_container_width=True)

if calculate_btn:
    birth_dt = datetime.combine(birth_date, birth_time)
    pillars = calculate_four_pillars(birth_dt)
    st.session_state.bazi_calculated = True
    st.session_state.birth_datetime = birth_dt
    st.session_state.pillars = pillars

if st.session_state.bazi_calculated and 'pillars' in st.session_state:
    pillars = st.session_state.pillars
    dm = pillars["day_master"]
    
    with col2:
        st.subheader("🎴 Four Pillars | 四柱")
        p_cols = st.columns(4)
        
        for i, pillar_name in enumerate(["hour", "day", "month", "year"]):
            pillar = pillars[pillar_name]
            with p_cols[i]:
                stem = pillar["stem"]
                branch = pillar["branch"]
                titles = {"year": "Year 年柱", "month": "Month 月柱", "day": "Day 日柱 ★", "hour": "Hour 时柱"}
                st.markdown(f"**{titles[pillar_name]}**")
                
                st.markdown(f"""
                <div style='text-align: center; padding: 10px; background: linear-gradient(135deg, #2d2d44, #1a1a2e);
                            border: 1px solid {get_stem_color(stem["element"])}; border-radius: 8px; margin: 5px 0;'>
                    <div style='font-size: 32px; color: {get_stem_color(stem["element"])};'>{stem["chinese"]}</div>
                    <div style='font-size: 12px; color: #888;'>{stem["pinyin"]} {stem["element"]}</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style='text-align: center; padding: 10px; background: linear-gradient(135deg, #2d2d44, #1a1a2e);
                            border: 1px solid {get_stem_color(branch["element"])}; border-radius: 8px; margin: 5px 0;'>
                    <div style='font-size: 32px; color: {get_stem_color(branch["element"])};'>{branch["chinese"]}</div>
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
        <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #2d2d44, #1a1a2e);
                    border: 2px solid #d4af37; border-radius: 12px;'>
            <div style='font-size: 48px; color: {get_stem_color(dm["element"])};'>{dm["chinese"]}</div>
            <div style='font-size: 18px; color: #d4af37;'>{dm["pinyin"]}</div>
            <div style='font-size: 14px; color: #fff;'>{dm["polarity"]} {dm["element"]}</div>
        </div>
        """, unsafe_allow_html=True)
    
    strength = assess_strength(dm["element"], pillars["month"]["branch"], pillars)
    
    with dm_col2:
        st.markdown("**Strength Assessment | 强弱分析**")
        st.metric("Seasonal 季节", strength["seasonal_strength"])
        st.metric("Category 类别", strength["category"])
        score_pct = (strength["score"] / 10) * 100
        bar_color = "#22C55E" if strength["score"] >= 5 else "#EF4444"
        st.markdown(f"""
        <div style='background: #333; border-radius: 10px; height: 20px; overflow: hidden;'>
            <div style='background: {bar_color}; width: {score_pct}%; height: 100%;'></div>
        </div>
        <div style='text-align: center; color: #888;'>Score: {strength["score"]}/10</div>
        """, unsafe_allow_html=True)
    
    useful = calculate_useful_gods(dm["element"], strength["category"])
    
    with dm_col3:
        st.markdown("**Useful Gods | 用神**")
        st.success(f"✅ Primary 主用神: **{useful['primary']}**")
        st.info(f"📌 Secondary 辅用神: **{useful['secondary']}**")
        if useful.get("unfavorable"):
            st.error(f"⛔ Avoid 忌神: **{', '.join(useful['unfavorable'])}**")
    
    st.markdown("---")
    
    # Ten Gods
    st.subheader("🔟 Ten Gods Mapping | 十神映射")
    ten_gods = generate_ten_gods_mapping(dm)
    tg_cols = st.columns(5)
    for i, stem in enumerate(HEAVENLY_STEMS):
        with tg_cols[i % 5]:
            god_data = ten_gods[stem["chinese"]]
            st.markdown(f"""
            <div style='text-align: center; padding: 8px; background: #2d2d44; border-radius: 8px;
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
    
    struct_cols = st.columns(2)
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
    
    st.markdown("---")
    
    # =========================================================================
    # SAVE TO PROFILE - FIXED! Now saves to user_profile
    # =========================================================================
    
    st.subheader("💾 Save Profile")
    
    if st.button("💾 Save to Profile | 保存到档案", type="primary", use_container_width=True):
        # Save to the CORRECT session state that sidebar uses
        st.session_state.user_profile = {
            'day_master': f"{dm['pinyin']} {dm['chinese']}",
            'element': dm['element'],
            'polarity': dm['polarity'],
            'strength': strength['category'],
            'strength_score': strength['score'],
            'profile': f"BaZi Calculated",
            'useful_gods': [useful['primary'], useful['secondary']],
            'unfavorable': useful.get('unfavorable', []),
            'wealth_vault': structures['wealth_vault'],
            'nobleman': structures['nobleman_present'],
            'birth_date': st.session_state.birth_datetime.strftime("%Y-%m-%d"),
            'birth_time': st.session_state.birth_datetime.strftime("%H:%M")
        }
        st.success("✅ Profile saved! Now visible in sidebar on all pages.")
        st.balloons()
    
    # Show current profile status
    if st.session_state.user_profile.get('day_master'):
        st.info(f"📋 Current profile: {st.session_state.user_profile.get('day_master')} | "
                f"Strength: {st.session_state.user_profile.get('strength')}")
    
    st.markdown("---")
    
    # Export JSON
    with st.expander("📤 Export JSON"):
        export_data = {
            "day_master": {"chinese": dm["chinese"], "pinyin": dm["pinyin"], 
                          "element": dm["element"], "polarity": dm["polarity"],
                          "strength": strength["category"], "score": strength["score"]},
            "four_pillars": {k: {"stem": v["stem"], "branch": v["branch"]} 
                           for k, v in pillars.items() if k != "day_master"},
            "useful_gods": useful,
            "special_structures": structures,
            "ten_gods_mapping": ten_gods
        }
        st.code(json.dumps(export_data, indent=2, ensure_ascii=False, default=str), language="json")
        st.download_button("⬇️ Download JSON", json.dumps(export_data, indent=2, ensure_ascii=False, default=str),
                          f"bazi_{birth_date}.json", "application/json", use_container_width=True)
