# -*- coding: utf-8 -*-
"""
Ming Qimen 明奇门 - BaZi Engine v1.0
Phase 5: Enhanced BaZi with Four Pillars Calculator

This module provides:
1. Four Pillars calculation from birth date/time
2. Day Master extraction and strength analysis
3. Ten Gods mapping
4. Useful Gods determination
5. Special structures detection
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple, Any

# Singapore timezone
SGT = timezone(timedelta(hours=8))

# ============================================================================
# CONSTANTS
# ============================================================================

# Ten Heavenly Stems (天干)
HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
STEMS_PINYIN = ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]
STEMS_ELEMENT = ["Wood", "Wood", "Fire", "Fire", "Earth", "Earth", "Metal", "Metal", "Water", "Water"]
STEMS_POLARITY = ["Yang", "Yin", "Yang", "Yin", "Yang", "Yin", "Yang", "Yin", "Yang", "Yin"]

# Twelve Earthly Branches (地支)
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
BRANCHES_PINYIN = ["Zi", "Chou", "Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai"]
BRANCHES_ANIMAL = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]
BRANCHES_ELEMENT = ["Water", "Earth", "Wood", "Wood", "Earth", "Fire", "Fire", "Earth", "Metal", "Metal", "Earth", "Water"]

# Hidden Stems in Branches (地支藏干)
HIDDEN_STEMS = {
    "子": ["癸"],
    "丑": ["己", "癸", "辛"],
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"],
    "辰": ["戊", "乙", "癸"],
    "巳": ["丙", "庚", "戊"],
    "午": ["丁", "己"],
    "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"],
    "戌": ["戊", "辛", "丁"],
    "亥": ["壬", "甲"]
}

# Month Branch by Solar Term (节气)
# Each month starts around the 4th-8th of the Western month
MONTH_BRANCHES = {
    1: 2,   # 寅 (Tiger) - starts around Feb 4 (立春)
    2: 3,   # 卯 (Rabbit) - starts around Mar 6 (惊蛰)
    3: 4,   # 辰 (Dragon) - starts around Apr 5 (清明)
    4: 5,   # 巳 (Snake) - starts around May 6 (立夏)
    5: 6,   # 午 (Horse) - starts around Jun 6 (芒种)
    6: 7,   # 未 (Goat) - starts around Jul 7 (小暑)
    7: 8,   # 申 (Monkey) - starts around Aug 8 (立秋)
    8: 9,   # 酉 (Rooster) - starts around Sep 8 (白露)
    9: 10,  # 戌 (Dog) - starts around Oct 8 (寒露)
    10: 11, # 亥 (Pig) - starts around Nov 7 (立冬)
    11: 0,  # 子 (Rat) - starts around Dec 7 (大雪)
    12: 1   # 丑 (Ox) - starts around Jan 6 (小寒)
}

# Solar term approximate start days (for month boundary)
SOLAR_TERM_DAYS = {
    1: 6,   # 小寒 around Jan 6
    2: 4,   # 立春 around Feb 4
    3: 6,   # 惊蛰 around Mar 6
    4: 5,   # 清明 around Apr 5
    5: 6,   # 立夏 around May 6
    6: 6,   # 芒种 around Jun 6
    7: 7,   # 小暑 around Jul 7
    8: 8,   # 立秋 around Aug 8
    9: 8,   # 白露 around Sep 8
    10: 8,  # 寒露 around Oct 8
    11: 7,  # 立冬 around Nov 7
    12: 7   # 大雪 around Dec 7
}

# Hour Branch mapping (Chinese 2-hour periods)
HOUR_BRANCHES = {
    (23, 1): 0,   # 子 Zi
    (1, 3): 1,    # 丑 Chou
    (3, 5): 2,    # 寅 Yin
    (5, 7): 3,    # 卯 Mao
    (7, 9): 4,    # 辰 Chen
    (9, 11): 5,   # 巳 Si
    (11, 13): 6,  # 午 Wu
    (13, 15): 7,  # 未 Wei
    (15, 17): 8,  # 申 Shen
    (17, 19): 9,  # 酉 You
    (19, 21): 10, # 戌 Xu
    (21, 23): 11  # 亥 Hai
}

# Ten Gods (十神) - relationship from Day Master perspective
TEN_GODS = {
    "same_yang": "比肩",      # Companion (Friend)
    "same_yin": "劫财",       # Rob Wealth
    "produces_yang": "食神",   # Eating God
    "produces_yin": "伤官",    # Hurting Officer
    "controlled_yang": "偏财", # Indirect Wealth
    "controlled_yin": "正财",  # Direct Wealth
    "controls_yang": "七杀",   # Seven Killings
    "controls_yin": "正官",    # Direct Officer
    "produced_by_yang": "偏印", # Indirect Resource
    "produced_by_yin": "正印"   # Direct Resource
}

TEN_GODS_ENGLISH = {
    "比肩": "Friend",
    "劫财": "Rob Wealth",
    "食神": "Eating God",
    "伤官": "Hurting Officer",
    "偏财": "Indirect Wealth",
    "正财": "Direct Wealth",
    "七杀": "7 Killings",
    "正官": "Direct Officer",
    "偏印": "Indirect Resource",
    "正印": "Direct Resource"
}

# Profile types based on dominant Ten God
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

# Element production cycle
ELEMENT_PRODUCES = {
    "Wood": "Fire",
    "Fire": "Earth",
    "Earth": "Metal",
    "Metal": "Water",
    "Water": "Wood"
}

# Element control cycle
ELEMENT_CONTROLS = {
    "Wood": "Earth",
    "Fire": "Metal",
    "Earth": "Water",
    "Metal": "Wood",
    "Water": "Fire"
}

# Reverse lookups
ELEMENT_PRODUCED_BY = {v: k for k, v in ELEMENT_PRODUCES.items()}
ELEMENT_CONTROLLED_BY = {v: k for k, v in ELEMENT_CONTROLS.items()}


# ============================================================================
# CALCULATION FUNCTIONS
# ============================================================================

def get_stem_index(stem: str) -> int:
    """Get index of Heavenly Stem"""
    if stem in HEAVENLY_STEMS:
        return HEAVENLY_STEMS.index(stem)
    if stem in STEMS_PINYIN:
        return STEMS_PINYIN.index(stem)
    return 0


def get_branch_index(branch: str) -> int:
    """Get index of Earthly Branch"""
    if branch in EARTHLY_BRANCHES:
        return EARTHLY_BRANCHES.index(branch)
    if branch in BRANCHES_PINYIN:
        return BRANCHES_PINYIN.index(branch)
    return 0


def calculate_year_pillar(year: int) -> Tuple[int, int]:
    """
    Calculate Year Pillar stem and branch indices.
    Based on the 60-year cycle (六十甲子).
    Year starts at 立春 (Feb 4 approx), but we simplify to Jan 1 here.
    """
    # The cycle: 1984 was 甲子 (Jia-Zi) year
    # Stem cycles every 10, Branch cycles every 12
    base_year = 1984
    diff = year - base_year
    
    stem_idx = diff % 10
    branch_idx = diff % 12
    
    return stem_idx, branch_idx


def calculate_month_pillar(year: int, month: int, day: int) -> Tuple[int, int]:
    """
    Calculate Month Pillar stem and branch indices.
    Month changes at solar terms, not calendar months.
    """
    # Determine the Chinese month based on solar terms
    solar_term_day = SOLAR_TERM_DAYS.get(month, 6)
    
    # Adjust month if before solar term
    if day < solar_term_day:
        month = month - 1 if month > 1 else 12
        if month == 12:
            year -= 1
    
    # Get branch for this Chinese month
    # Chinese month 1 (寅) starts around Feb 4
    chinese_month = ((month - 2) % 12) + 1 if month >= 2 else ((month + 10) % 12) + 1
    branch_idx = (chinese_month + 1) % 12  # 寅=2 for month 1
    
    # Simplified: Month 1 (寅 month) branch index is 2
    branch_idx = (month + 1) % 12 if month >= 2 else (month + 13) % 12
    
    # Calculate stem based on year stem
    # Rule: 甲己年起丙寅, 乙庚年起戊寅, etc.
    year_stem_idx, _ = calculate_year_pillar(year)
    year_stem_group = year_stem_idx % 5  # 甲己=0, 乙庚=1, 丙辛=2, 丁壬=3, 戊癸=4
    
    # Starting stem for 寅 month based on year stem
    month_stem_starts = [2, 4, 6, 8, 0]  # 丙, 戊, 庚, 壬, 甲
    start_stem = month_stem_starts[year_stem_group]
    
    # Calculate this month's stem
    month_offset = (month - 2) % 12 if month >= 2 else (month + 10) % 12
    stem_idx = (start_stem + month_offset) % 10
    
    return stem_idx, branch_idx


def calculate_day_pillar(year: int, month: int, day: int) -> Tuple[int, int]:
    """
    Calculate Day Pillar stem and branch indices.
    Uses the day count from a known reference date.
    """
    # Reference: Jan 1, 1900 was 甲戌 (Jia-Xu) day
    # Stem index: 0 (甲), Branch index: 10 (戌)
    from datetime import date
    
    ref_date = date(1900, 1, 1)
    ref_stem = 0   # 甲
    ref_branch = 10  # 戌
    
    target_date = date(year, month, day)
    days_diff = (target_date - ref_date).days
    
    stem_idx = (ref_stem + days_diff) % 10
    branch_idx = (ref_branch + days_diff) % 12
    
    return stem_idx, branch_idx


def calculate_hour_pillar(year: int, month: int, day: int, hour: int) -> Tuple[int, int]:
    """
    Calculate Hour Pillar stem and branch indices.
    """
    # Get hour branch
    branch_idx = 0
    if hour == 23 or hour < 1:
        branch_idx = 0  # 子
    else:
        branch_idx = ((hour + 1) // 2) % 12
    
    # Calculate hour stem based on day stem
    # Rule: 甲己日起甲子时, 乙庚日起丙子时, etc.
    day_stem_idx, _ = calculate_day_pillar(year, month, day)
    day_stem_group = day_stem_idx % 5  # 甲己=0, 乙庚=1, 丙辛=2, 丁壬=3, 戊癸=4
    
    # Starting stem for 子 hour based on day stem
    hour_stem_starts = [0, 2, 4, 6, 8]  # 甲, 丙, 戊, 庚, 壬
    start_stem = hour_stem_starts[day_stem_group]
    
    stem_idx = (start_stem + branch_idx) % 10
    
    return stem_idx, branch_idx


def get_pillar_info(stem_idx: int, branch_idx: int) -> Dict:
    """Get detailed info for a pillar"""
    stem = HEAVENLY_STEMS[stem_idx]
    branch = EARTHLY_BRANCHES[branch_idx]
    
    return {
        "stem": {
            "chinese": stem,
            "pinyin": STEMS_PINYIN[stem_idx],
            "element": STEMS_ELEMENT[stem_idx],
            "polarity": STEMS_POLARITY[stem_idx]
        },
        "branch": {
            "chinese": branch,
            "pinyin": BRANCHES_PINYIN[branch_idx],
            "element": BRANCHES_ELEMENT[branch_idx],
            "animal": BRANCHES_ANIMAL[branch_idx]
        },
        "hidden_stems": HIDDEN_STEMS.get(branch, []),
        "display": f"{stem}{branch}",
        "display_pinyin": f"{STEMS_PINYIN[stem_idx]}-{BRANCHES_PINYIN[branch_idx]}"
    }


def calculate_four_pillars(year: int, month: int, day: int, hour: int) -> Dict:
    """
    Calculate complete Four Pillars (八字/四柱).
    
    Returns:
        Dict with year, month, day, hour pillars and metadata
    """
    year_stem, year_branch = calculate_year_pillar(year)
    month_stem, month_branch = calculate_month_pillar(year, month, day)
    day_stem, day_branch = calculate_day_pillar(year, month, day)
    hour_stem, hour_branch = calculate_hour_pillar(year, month, day, hour)
    
    return {
        "year": get_pillar_info(year_stem, year_branch),
        "month": get_pillar_info(month_stem, month_branch),
        "day": get_pillar_info(day_stem, day_branch),
        "hour": get_pillar_info(hour_stem, hour_branch),
        "day_master": {
            "chinese": HEAVENLY_STEMS[day_stem],
            "pinyin": STEMS_PINYIN[day_stem],
            "element": STEMS_ELEMENT[day_stem],
            "polarity": STEMS_POLARITY[day_stem]
        }
    }


def get_ten_god(day_master_element: str, day_master_polarity: str, 
                target_element: str, target_polarity: str) -> str:
    """
    Determine the Ten God relationship between Day Master and another element.
    """
    dm_elem = day_master_element
    dm_pol = day_master_polarity
    t_elem = target_element
    t_pol = target_polarity
    
    same_polarity = (dm_pol == t_pol)
    
    # Same element
    if dm_elem == t_elem:
        return "比肩" if same_polarity else "劫财"
    
    # Day Master produces target
    if ELEMENT_PRODUCES.get(dm_elem) == t_elem:
        return "食神" if same_polarity else "伤官"
    
    # Day Master controls target (target is wealth)
    if ELEMENT_CONTROLS.get(dm_elem) == t_elem:
        return "偏财" if same_polarity else "正财"
    
    # Target controls Day Master (target is authority)
    if ELEMENT_CONTROLS.get(t_elem) == dm_elem:
        return "七杀" if same_polarity else "正官"
    
    # Target produces Day Master (target is resource)
    if ELEMENT_PRODUCES.get(t_elem) == dm_elem:
        return "偏印" if same_polarity else "正印"
    
    return "Unknown"


def analyze_ten_gods(four_pillars: Dict) -> Dict:
    """
    Analyze Ten Gods throughout the chart.
    """
    dm = four_pillars["day_master"]
    dm_elem = dm["element"]
    dm_pol = dm["polarity"]
    
    ten_gods = {
        "year_stem": "",
        "month_stem": "",
        "hour_stem": "",
        "hidden_stems": []
    }
    
    # Analyze visible stems
    for pillar_name in ["year", "month", "hour"]:
        pillar = four_pillars[pillar_name]
        stem = pillar["stem"]
        god = get_ten_god(dm_elem, dm_pol, stem["element"], stem["polarity"])
        ten_gods[f"{pillar_name}_stem"] = {
            "chinese": god,
            "english": TEN_GODS_ENGLISH.get(god, god),
            "stem": stem["chinese"]
        }
    
    # Analyze hidden stems
    for pillar_name in ["year", "month", "day", "hour"]:
        pillar = four_pillars[pillar_name]
        branch = pillar["branch"]["chinese"]
        hidden = HIDDEN_STEMS.get(branch, [])
        
        for h_stem in hidden:
            h_idx = HEAVENLY_STEMS.index(h_stem)
            h_elem = STEMS_ELEMENT[h_idx]
            h_pol = STEMS_POLARITY[h_idx]
            god = get_ten_god(dm_elem, dm_pol, h_elem, h_pol)
            
            ten_gods["hidden_stems"].append({
                "pillar": pillar_name,
                "branch": branch,
                "stem": h_stem,
                "element": h_elem,
                "ten_god_chinese": god,
                "ten_god_english": TEN_GODS_ENGLISH.get(god, god)
            })
    
    return ten_gods


def count_elements(four_pillars: Dict) -> Dict:
    """
    Count elements in the chart (stems and branches).
    """
    counts = {"Wood": 0, "Fire": 0, "Earth": 0, "Metal": 0, "Water": 0}
    
    for pillar_name in ["year", "month", "day", "hour"]:
        pillar = four_pillars[pillar_name]
        
        # Count stem element
        stem_elem = pillar["stem"]["element"]
        counts[stem_elem] = counts.get(stem_elem, 0) + 1
        
        # Count branch element
        branch_elem = pillar["branch"]["element"]
        counts[branch_elem] = counts.get(branch_elem, 0) + 1
    
    return counts


def calculate_day_master_strength(four_pillars: Dict) -> Dict:
    """
    Calculate Day Master strength based on:
    1. Season (month branch)
    2. Support from other elements
    3. Hidden stems
    
    Returns strength assessment.
    """
    dm = four_pillars["day_master"]
    dm_elem = dm["element"]
    
    # Element counts
    elem_counts = count_elements(four_pillars)
    
    # Count support
    support_score = 0
    
    # Same element supports
    support_score += elem_counts.get(dm_elem, 0) * 2
    
    # Resource element supports
    resource_elem = ELEMENT_PRODUCED_BY.get(dm_elem, "")
    support_score += elem_counts.get(resource_elem, 0) * 1.5
    
    # Opposition elements weaken
    control_elem = ELEMENT_CONTROLLED_BY.get(dm_elem, "")  # What controls DM
    wealth_elem = ELEMENT_CONTROLS.get(dm_elem, "")  # What DM controls (drains)
    output_elem = ELEMENT_PRODUCES.get(dm_elem, "")  # What DM produces (drains)
    
    support_score -= elem_counts.get(control_elem, 0) * 1.5
    support_score -= elem_counts.get(wealth_elem, 0) * 0.5
    support_score -= elem_counts.get(output_elem, 0) * 0.5
    
    # Month branch (season) influence
    month_branch_elem = four_pillars["month"]["branch"]["element"]
    if month_branch_elem == dm_elem:
        support_score += 3  # In season
    elif month_branch_elem == resource_elem:
        support_score += 2  # Supported by season
    elif month_branch_elem == control_elem:
        support_score -= 2  # Controlled by season
    
    # Determine strength category
    if support_score >= 6:
        strength = "Extremely Strong"
        strength_score = 9
    elif support_score >= 3:
        strength = "Strong"
        strength_score = 7
    elif support_score >= 0:
        strength = "Balanced"
        strength_score = 5
    elif support_score >= -3:
        strength = "Weak"
        strength_score = 3
    else:
        strength = "Extremely Weak"
        strength_score = 1
    
    return {
        "strength": strength,
        "strength_score": strength_score,
        "support_score": round(support_score, 1),
        "element_counts": elem_counts,
        "analysis": {
            "same_element": elem_counts.get(dm_elem, 0),
            "resource_element": elem_counts.get(resource_elem, 0),
            "control_element": elem_counts.get(control_elem, 0),
            "month_support": month_branch_elem == dm_elem or month_branch_elem == resource_elem
        }
    }


def determine_useful_gods(dm_element: str, strength: str) -> Dict:
    """
    Determine Useful Gods (用神) based on Day Master element and strength.
    
    General rules:
    - Weak DM needs: Resource (produces DM) and Companion (same element)
    - Strong DM needs: Output, Wealth, Authority (to drain/control)
    """
    resource = ELEMENT_PRODUCED_BY.get(dm_element, "")
    companion = dm_element
    output = ELEMENT_PRODUCES.get(dm_element, "")
    wealth = ELEMENT_CONTROLS.get(dm_element, "")
    authority = ELEMENT_CONTROLLED_BY.get(dm_element, "")
    
    if strength in ["Weak", "Extremely Weak"]:
        return {
            "primary": resource,
            "secondary": companion,
            "favorable": [resource, companion],
            "unfavorable": [authority, wealth],
            "reasoning": f"Weak {dm_element} Day Master needs support from {resource} (Resource) and {companion} (Companion). Avoid {authority} (pressure) and excessive {wealth} (drain)."
        }
    elif strength in ["Strong", "Extremely Strong"]:
        return {
            "primary": wealth,
            "secondary": output,
            "favorable": [wealth, output, authority],
            "unfavorable": [resource, companion],
            "reasoning": f"Strong {dm_element} Day Master needs to be drained by {output} (Output) and {wealth} (Wealth). Controlled by {authority} brings balance. Avoid more {resource} and {companion}."
        }
    else:  # Balanced
        return {
            "primary": wealth,
            "secondary": output,
            "favorable": [wealth, output],
            "unfavorable": [],
            "reasoning": f"Balanced {dm_element} Day Master is flexible. {wealth} (Wealth) and {output} (Output) are generally favorable."
        }


def detect_special_structures(four_pillars: Dict, ten_gods: Dict) -> Dict:
    """
    Detect special structures in the BaZi chart.
    """
    structures = {
        "wealth_vault": False,
        "wealth_vault_location": "",
        "nobleman_present": False,
        "nobleman_location": "",
        "other_structures": []
    }
    
    dm = four_pillars["day_master"]
    dm_elem = dm["element"]
    
    # Check for Wealth Vault (财库)
    # Wealth element's storage branch
    wealth_elem = ELEMENT_CONTROLS.get(dm_elem, "")
    vault_branches = {
        "Wood": "未",  # Wood stored in Wei
        "Fire": "戌",  # Fire stored in Xu
        "Earth": "戌", # Earth stored in Xu
        "Metal": "丑", # Metal stored in Chou
        "Water": "辰"  # Water stored in Chen
    }
    
    wealth_vault_branch = vault_branches.get(wealth_elem, "")
    
    for pillar_name in ["year", "month", "day", "hour"]:
        branch = four_pillars[pillar_name]["branch"]["chinese"]
        if branch == wealth_vault_branch:
            structures["wealth_vault"] = True
            structures["wealth_vault_location"] = f"{pillar_name.title()} Pillar ({branch})"
            break
    
    # Check for Nobleman (天乙贵人)
    # Simplified: based on Day Master
    nobleman_map = {
        "甲": ["丑", "未"], "戊": ["丑", "未"],
        "乙": ["子", "申"], "己": ["子", "申"],
        "丙": ["亥", "酉"], "丁": ["亥", "酉"],
        "庚": ["丑", "未"], "辛": ["寅", "午"],
        "壬": ["卯", "巳"], "癸": ["卯", "巳"]
    }
    
    dm_chinese = dm["chinese"]
    noble_branches = nobleman_map.get(dm_chinese, [])
    
    for pillar_name in ["year", "month", "day", "hour"]:
        branch = four_pillars[pillar_name]["branch"]["chinese"]
        if branch in noble_branches:
            structures["nobleman_present"] = True
            structures["nobleman_location"] = f"{pillar_name.title()} Pillar ({branch})"
            break
    
    return structures


def get_dominant_ten_god(ten_gods: Dict) -> Dict:
    """
    Determine the dominant Ten God in the chart.
    """
    god_counts = {}
    
    # Count from visible stems
    for key in ["year_stem", "month_stem", "hour_stem"]:
        if key in ten_gods and ten_gods[key]:
            god = ten_gods[key].get("english", "")
            if god:
                god_counts[god] = god_counts.get(god, 0) + 2  # Visible stems count more
    
    # Count from hidden stems
    for hidden in ten_gods.get("hidden_stems", []):
        god = hidden.get("ten_god_english", "")
        if god:
            god_counts[god] = god_counts.get(god, 0) + 1
    
    if not god_counts:
        return {"god": "Unknown", "profile": "Unknown"}
    
    dominant = max(god_counts, key=god_counts.get)
    
    return {
        "god": dominant,
        "god_chinese": [k for k, v in TEN_GODS_ENGLISH.items() if v == dominant][0] if dominant in TEN_GODS_ENGLISH.values() else "",
        "profile": PROFILE_TYPES.get(dominant, "Unknown"),
        "counts": god_counts
    }


# ============================================================================
# MAIN INTERFACE
# ============================================================================

def calculate_bazi_profile(year: int, month: int, day: int, hour: int) -> Dict:
    """
    Main function to calculate complete BaZi profile from birth data.
    
    Args:
        year: Birth year
        month: Birth month (1-12)
        day: Birth day (1-31)
        hour: Birth hour (0-23)
    
    Returns:
        Complete BaZi profile with Four Pillars, Day Master, Ten Gods, etc.
    """
    # Calculate Four Pillars
    four_pillars = calculate_four_pillars(year, month, day, hour)
    
    # Analyze Ten Gods
    ten_gods = analyze_ten_gods(four_pillars)
    
    # Calculate Day Master strength
    dm_strength = calculate_day_master_strength(four_pillars)
    
    # Determine Useful Gods
    dm_elem = four_pillars["day_master"]["element"]
    useful_gods = determine_useful_gods(dm_elem, dm_strength["strength"])
    
    # Detect special structures
    special_structures = detect_special_structures(four_pillars, ten_gods)
    
    # Get dominant Ten God
    dominant = get_dominant_ten_god(ten_gods)
    
    # Build profile
    profile = {
        "birth_data": {
            "year": year,
            "month": month,
            "day": day,
            "hour": hour
        },
        "four_pillars": four_pillars,
        "day_master": {
            **four_pillars["day_master"],
            "strength": dm_strength["strength"],
            "strength_score": dm_strength["strength_score"]
        },
        "ten_gods": ten_gods,
        "ten_gods_mapping": {
            "Wood": get_ten_god(dm_elem, four_pillars["day_master"]["polarity"], "Wood", "Yang"),
            "Fire": get_ten_god(dm_elem, four_pillars["day_master"]["polarity"], "Fire", "Yang"),
            "Earth": get_ten_god(dm_elem, four_pillars["day_master"]["polarity"], "Earth", "Yang"),
            "Metal": get_ten_god(dm_elem, four_pillars["day_master"]["polarity"], "Metal", "Yang"),
            "Water": get_ten_god(dm_elem, four_pillars["day_master"]["polarity"], "Water", "Yang")
        },
        "useful_gods": useful_gods,
        "special_structures": special_structures,
        "profile": {
            "dominant_god": dominant["god"],
            "dominant_god_chinese": dominant.get("god_chinese", ""),
            "type": dominant["profile"],
            "type_chinese": f"{dominant['profile']} ({dominant.get('god_chinese', '')})"
        },
        "element_analysis": dm_strength
    }
    
    return profile


def format_pillars_display(profile: Dict) -> str:
    """Format Four Pillars for display"""
    fp = profile["four_pillars"]
    
    lines = []
    lines.append("        年柱      月柱      日柱      时柱")
    lines.append("       Year     Month      Day      Hour")
    lines.append("      ─────    ─────    ─────    ─────")
    lines.append(f"天干   {fp['year']['stem']['chinese']}        {fp['month']['stem']['chinese']}        {fp['day']['stem']['chinese']}        {fp['hour']['stem']['chinese']}")
    lines.append(f"地支   {fp['year']['branch']['chinese']}        {fp['month']['branch']['chinese']}        {fp['day']['branch']['chinese']}        {fp['hour']['branch']['chinese']}")
    lines.append(f"      ({fp['year']['branch']['animal'][:3]})    ({fp['month']['branch']['animal'][:3]})    ({fp['day']['branch']['animal'][:3]})    ({fp['hour']['branch']['animal'][:3]})")
    
    return "\n".join(lines)


# ============================================================================
# TEST
# ============================================================================

if __name__ == "__main__":
    # Test with a sample birth date
    # Example: 1990-05-15, 10:00
    print("=" * 60)
    print("BaZi Calculator Test")
    print("=" * 60)
    
    profile = calculate_bazi_profile(1990, 5, 15, 10)
    
    print("\nFour Pillars:")
    print(format_pillars_display(profile))
    
    print(f"\nDay Master: {profile['day_master']['chinese']} {profile['day_master']['pinyin']}")
    print(f"Element: {profile['day_master']['element']} ({profile['day_master']['polarity']})")
    print(f"Strength: {profile['day_master']['strength']} (Score: {profile['day_master']['strength_score']})")
    
    print(f"\nUseful Gods: {', '.join(profile['useful_gods']['favorable'])}")
    print(f"Unfavorable: {', '.join(profile['useful_gods']['unfavorable'])}")
    
    print(f"\nProfile Type: {profile['profile']['type']} ({profile['profile']['dominant_god']})")
    
    print(f"\nWealth Vault: {profile['special_structures']['wealth_vault']}")
    print(f"Nobleman: {profile['special_structures']['nobleman_present']}")
