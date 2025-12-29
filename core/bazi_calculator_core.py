"""
BaZi Calculator Core Engine
============================
Complete Four Pillars calculation with Ten Gods mapping
For Ming Qimen Project 2 (Streamlit Developer Engine)

Features:
- Four Pillars calculation from birth date/time
- Hidden Stems extraction
- Ten Gods complete mapping
- Useful Gods recommendation
- Special structures detection
- Day Master strength assessment
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json

# =============================================================================
# CONSTANTS: HEAVENLY STEMS (天干)
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

# =============================================================================
# CONSTANTS: EARTHLY BRANCHES (地支)
# =============================================================================

EARTHLY_BRANCHES = [
    {"chinese": "子", "pinyin": "Zi", "animal": "Rat", "element": "Water", "polarity": "Yang", 
     "hidden_stems": ["癸"], "month": 11, "hours": (23, 1), "index": 0},
    {"chinese": "丑", "pinyin": "Chou", "animal": "Ox", "element": "Earth", "polarity": "Yin",
     "hidden_stems": ["己", "癸", "辛"], "month": 12, "hours": (1, 3), "index": 1},
    {"chinese": "寅", "pinyin": "Yin", "animal": "Tiger", "element": "Wood", "polarity": "Yang",
     "hidden_stems": ["甲", "丙", "戊"], "month": 1, "hours": (3, 5), "index": 2},
    {"chinese": "卯", "pinyin": "Mao", "animal": "Rabbit", "element": "Wood", "polarity": "Yin",
     "hidden_stems": ["乙"], "month": 2, "hours": (5, 7), "index": 3},
    {"chinese": "辰", "pinyin": "Chen", "animal": "Dragon", "element": "Earth", "polarity": "Yang",
     "hidden_stems": ["戊", "乙", "癸"], "month": 3, "hours": (7, 9), "index": 4},
    {"chinese": "巳", "pinyin": "Si", "animal": "Snake", "element": "Fire", "polarity": "Yin",
     "hidden_stems": ["丙", "庚", "戊"], "month": 4, "hours": (9, 11), "index": 5},
    {"chinese": "午", "pinyin": "Wu", "animal": "Horse", "element": "Fire", "polarity": "Yang",
     "hidden_stems": ["丁", "己"], "month": 5, "hours": (11, 13), "index": 6},
    {"chinese": "未", "pinyin": "Wei", "animal": "Goat", "element": "Earth", "polarity": "Yin",
     "hidden_stems": ["己", "丁", "乙"], "month": 7, "hours": (13, 15), "index": 7},
    {"chinese": "申", "pinyin": "Shen", "animal": "Monkey", "element": "Metal", "polarity": "Yang",
     "hidden_stems": ["庚", "壬", "戊"], "month": 7, "hours": (15, 17), "index": 8},
    {"chinese": "酉", "pinyin": "You", "animal": "Rooster", "element": "Metal", "polarity": "Yin",
     "hidden_stems": ["辛"], "month": 8, "hours": (17, 19), "index": 9},
    {"chinese": "戌", "pinyin": "Xu", "animal": "Dog", "element": "Earth", "polarity": "Yang",
     "hidden_stems": ["戊", "辛", "丁"], "month": 9, "hours": (19, 21), "index": 10},
    {"chinese": "亥", "pinyin": "Hai", "animal": "Pig", "element": "Water", "polarity": "Yin",
     "hidden_stems": ["壬", "甲"], "month": 10, "hours": (21, 23), "index": 11},
]

# =============================================================================
# CONSTANTS: ELEMENT RELATIONSHIPS
# =============================================================================

ELEMENT_PRODUCES = {
    "Wood": "Fire", "Fire": "Earth", "Earth": "Metal", "Metal": "Water", "Water": "Wood"
}

ELEMENT_CONTROLS = {
    "Wood": "Earth", "Fire": "Metal", "Earth": "Water", "Metal": "Wood", "Water": "Fire"
}

ELEMENT_PRODUCED_BY = {
    "Wood": "Water", "Fire": "Wood", "Earth": "Fire", "Metal": "Earth", "Water": "Metal"
}

ELEMENT_CONTROLLED_BY = {
    "Wood": "Metal", "Fire": "Water", "Earth": "Wood", "Metal": "Fire", "Water": "Earth"
}

# =============================================================================
# CONSTANTS: TEN GODS MAPPING
# =============================================================================

TEN_GODS = {
    "same_element_same_polarity": {"name": "Rob Wealth", "chinese": "劫财", "pinyin": "Jie Cai"},
    "same_element_diff_polarity": {"name": "Friend", "chinese": "比肩", "pinyin": "Bi Jian"},
    "produces_dm_same_polarity": {"name": "Indirect Resource", "chinese": "偏印", "pinyin": "Pian Yin"},
    "produces_dm_diff_polarity": {"name": "Direct Resource", "chinese": "正印", "pinyin": "Zheng Yin"},
    "dm_produces_same_polarity": {"name": "Hurting Officer", "chinese": "伤官", "pinyin": "Shang Guan"},
    "dm_produces_diff_polarity": {"name": "Eating God", "chinese": "食神", "pinyin": "Shi Shen"},
    "dm_controls_same_polarity": {"name": "Indirect Wealth", "chinese": "偏财", "pinyin": "Pian Cai"},
    "dm_controls_diff_polarity": {"name": "Direct Wealth", "chinese": "正财", "pinyin": "Zheng Cai"},
    "controls_dm_same_polarity": {"name": "7 Killings", "chinese": "七杀", "pinyin": "Qi Sha"},
    "controls_dm_diff_polarity": {"name": "Direct Officer", "chinese": "正官", "pinyin": "Zheng Guan"},
}

# Ten God Profile Descriptions
TEN_GOD_PROFILES = {
    "Rob Wealth": {
        "profile_name": "Competitor",
        "traits": ["Competitive", "Independent", "Self-reliant", "Aggressive in pursuit"],
        "strengths": ["Self-motivation", "Resilience", "Determination"],
        "challenges": ["Sharing", "Collaboration", "Trust issues"]
    },
    "Friend": {
        "profile_name": "Companion",
        "traits": ["Loyal", "Supportive", "Team-oriented", "Consistent"],
        "strengths": ["Reliability", "Friendship", "Stability"],
        "challenges": ["Standing out", "Taking initiative", "Independence"]
    },
    "Indirect Resource": {
        "profile_name": "Strategist",
        "traits": ["Analytical", "Strategic", "Unconventional thinker", "Reserved"],
        "strengths": ["Problem-solving", "Innovation", "Deep thinking"],
        "challenges": ["Overthinking", "Isolation", "Communication"]
    },
    "Direct Resource": {
        "profile_name": "Nurturer",
        "traits": ["Caring", "Supportive", "Traditional", "Patient"],
        "strengths": ["Teaching", "Patience", "Emotional support"],
        "challenges": ["Boundaries", "Self-care", "Dependency"]
    },
    "Hurting Officer": {
        "profile_name": "Maverick",
        "traits": ["Creative", "Rebellious", "Outspoken", "Innovative"],
        "strengths": ["Creativity", "Breaking conventions", "Expression"],
        "challenges": ["Authority conflicts", "Diplomacy", "Patience"]
    },
    "Eating God": {
        "profile_name": "Artist",
        "traits": ["Creative", "Gentle", "Pleasure-seeking", "Expressive"],
        "strengths": ["Artistic ability", "Enjoyment of life", "Charm"],
        "challenges": ["Discipline", "Focus", "Practical matters"]
    },
    "Indirect Wealth": {
        "profile_name": "Pioneer",
        "traits": ["Risk-taking", "Opportunity-seeking", "Unconventional", "Bold"],
        "strengths": ["Spotting opportunities", "Quick decisions", "Networking"],
        "challenges": ["Impulsivity", "Long-term planning", "Saving"]
    },
    "Direct Wealth": {
        "profile_name": "Manager",
        "traits": ["Practical", "Hardworking", "Responsible", "Methodical"],
        "strengths": ["Financial management", "Reliability", "Steady growth"],
        "challenges": ["Risk-taking", "Flexibility", "Innovation"]
    },
    "7 Killings": {
        "profile_name": "Warrior",
        "traits": ["Ambitious", "Driven", "Competitive", "Intense"],
        "strengths": ["Leadership under pressure", "Courage", "Transformation"],
        "challenges": ["Aggression", "Conflict", "Burnout"]
    },
    "Direct Officer": {
        "profile_name": "Leader",
        "traits": ["Responsible", "Principled", "Authoritative", "Structured"],
        "strengths": ["Leadership", "Organization", "Ethics"],
        "challenges": ["Flexibility", "Creativity", "Relaxation"]
    }
}

# =============================================================================
# CONSTANTS: SEASONAL STRENGTH
# =============================================================================

SEASON_MONTHS = {
    "Spring": [1, 2, 3],      # Tiger, Rabbit, Dragon months (Feb-Apr)
    "Summer": [4, 5, 6],      # Snake, Horse, Goat months (May-Jul)
    "Autumn": [7, 8, 9],      # Monkey, Rooster, Dog months (Aug-Oct)
    "Winter": [10, 11, 12]    # Pig, Rat, Ox months (Nov-Jan)
}

# Element strength by season
ELEMENT_SEASONAL_STRENGTH = {
    "Wood":  {"Spring": "Prosperous", "Summer": "Weak", "Autumn": "Dead", "Winter": "Strong"},
    "Fire":  {"Spring": "Strong", "Summer": "Prosperous", "Autumn": "Weak", "Winter": "Dead"},
    "Earth": {"Spring": "Dead", "Summer": "Strong", "Autumn": "Prosperous", "Winter": "Weak"},
    "Metal": {"Spring": "Dead", "Summer": "Weak", "Autumn": "Prosperous", "Winter": "Strong"},
    "Water": {"Spring": "Weak", "Summer": "Dead", "Autumn": "Strong", "Winter": "Prosperous"}
}

# =============================================================================
# CONSTANTS: SPECIAL STRUCTURES
# =============================================================================

# Six Combinations (六合)
SIX_COMBINATIONS = [
    (0, 1),   # 子丑合 Zi-Chou → Earth
    (2, 11),  # 寅亥合 Yin-Hai → Wood
    (3, 10),  # 卯戌合 Mao-Xu → Fire
    (4, 9),   # 辰酉合 Chen-You → Metal
    (5, 8),   # 巳申合 Si-Shen → Water
    (6, 7),   # 午未合 Wu-Wei → Fire/Earth
]

# Six Clashes (六冲)
SIX_CLASHES = [
    (0, 6),   # 子午冲 Zi-Wu
    (1, 7),   # 丑未冲 Chou-Wei
    (2, 8),   # 寅申冲 Yin-Shen
    (3, 9),   # 卯酉冲 Mao-You
    (4, 10),  # 辰戌冲 Chen-Xu
    (5, 11),  # 巳亥冲 Si-Hai
]

# Three Harmony Frames (三合局)
THREE_HARMONIES = {
    "Wood": [2, 6, 10],    # 寅午戌 Yin-Wu-Xu → Fire Frame (produces Fire)
    "Fire": [5, 9, 1],     # 巳酉丑 Si-You-Chou → Metal Frame
    "Metal": [8, 0, 4],    # 申子辰 Shen-Zi-Chen → Water Frame
    "Water": [11, 3, 7],   # 亥卯未 Hai-Mao-Wei → Wood Frame
}

# Nobleman Stars (贵人)
NOBLEMAN_LOOKUP = {
    "甲": ["丑", "未"], "戊": ["丑", "未"],  # Jia/Wu → Chou/Wei
    "乙": ["子", "申"], "己": ["子", "申"],  # Yi/Ji → Zi/Shen
    "丙": ["亥", "酉"], "丁": ["亥", "酉"],  # Bing/Ding → Hai/You
    "庚": ["丑", "未"],                      # Geng → Chou/Wei
    "辛": ["寅", "午"],                      # Xin → Yin/Wu
    "壬": ["卯", "巳"], "癸": ["卯", "巳"],  # Ren/Gui → Mao/Si
}

# Wealth Vault (财库) - Earth branches store wealth for each DM
WEALTH_VAULT = {
    "Wood": "未",   # Wood controls Earth, Wei is Earth storage
    "Fire": "戌",   # Fire controls Metal, Xu stores Metal
    "Earth": "辰",  # Earth controls Water, Chen stores Water (actually 丑 for some)
    "Metal": "丑",  # Metal controls Wood, Chou stores Wood
    "Water": "辰",  # Water controls Fire, Chen stores Fire
}


# =============================================================================
# CORE CALCULATION FUNCTIONS
# =============================================================================

def get_stem_by_chinese(chinese: str) -> Optional[Dict]:
    """Get stem data by Chinese character"""
    for stem in HEAVENLY_STEMS:
        if stem["chinese"] == chinese:
            return stem
    return None

def get_stem_by_pinyin(pinyin: str) -> Optional[Dict]:
    """Get stem data by pinyin"""
    for stem in HEAVENLY_STEMS:
        if stem["pinyin"].lower() == pinyin.lower():
            return stem
    return None

def get_branch_by_chinese(chinese: str) -> Optional[Dict]:
    """Get branch data by Chinese character"""
    for branch in EARTHLY_BRANCHES:
        if branch["chinese"] == chinese:
            return branch
    return None

def get_branch_by_pinyin(pinyin: str) -> Optional[Dict]:
    """Get branch data by pinyin"""
    for branch in EARTHLY_BRANCHES:
        if branch["pinyin"].lower() == pinyin.lower():
            return branch
    return None

def get_hour_branch(hour: int) -> Dict:
    """Get earthly branch for a given hour (0-23)"""
    # Zi hour: 23:00-00:59
    if hour == 23 or hour == 0:
        return EARTHLY_BRANCHES[0]  # Zi
    # Other hours
    branch_index = ((hour + 1) // 2) % 12
    return EARTHLY_BRANCHES[branch_index]

def get_season(month_branch_index: int) -> str:
    """Get season from month branch index"""
    if month_branch_index in [2, 3, 4]:    # Yin, Mao, Chen
        return "Spring"
    elif month_branch_index in [5, 6, 7]:  # Si, Wu, Wei
        return "Summer"
    elif month_branch_index in [8, 9, 10]: # Shen, You, Xu
        return "Autumn"
    else:                                   # Hai, Zi, Chou
        return "Winter"


# =============================================================================
# TEN GODS CALCULATION
# =============================================================================

def calculate_ten_god(dm_element: str, dm_polarity: str, 
                      target_element: str, target_polarity: str) -> Dict:
    """
    Calculate the Ten God relationship between Day Master and target stem
    
    Returns dict with: name, chinese, pinyin, category
    """
    same_polarity = (dm_polarity == target_polarity)
    
    # Same element = Companion category
    if dm_element == target_element:
        if same_polarity:
            return {**TEN_GODS["same_element_same_polarity"], "category": "Companion"}
        else:
            return {**TEN_GODS["same_element_diff_polarity"], "category": "Companion"}
    
    # Element that produces DM = Resource category
    if ELEMENT_PRODUCED_BY[dm_element] == target_element:
        if same_polarity:
            return {**TEN_GODS["produces_dm_same_polarity"], "category": "Resource"}
        else:
            return {**TEN_GODS["produces_dm_diff_polarity"], "category": "Resource"}
    
    # Element DM produces = Output category
    if ELEMENT_PRODUCES[dm_element] == target_element:
        if same_polarity:
            return {**TEN_GODS["dm_produces_same_polarity"], "category": "Output"}
        else:
            return {**TEN_GODS["dm_produces_diff_polarity"], "category": "Output"}
    
    # Element DM controls = Wealth category
    if ELEMENT_CONTROLS[dm_element] == target_element:
        if same_polarity:
            return {**TEN_GODS["dm_controls_same_polarity"], "category": "Wealth"}
        else:
            return {**TEN_GODS["dm_controls_diff_polarity"], "category": "Wealth"}
    
    # Element that controls DM = Authority category
    if ELEMENT_CONTROLLED_BY[dm_element] == target_element:
        if same_polarity:
            return {**TEN_GODS["controls_dm_same_polarity"], "category": "Authority"}
        else:
            return {**TEN_GODS["controls_dm_diff_polarity"], "category": "Authority"}
    
    return {"name": "Unknown", "chinese": "?", "pinyin": "?", "category": "Unknown"}


def generate_complete_ten_gods_mapping(dm_stem: Dict) -> Dict:
    """
    Generate complete Ten Gods mapping for all stems from Day Master perspective
    
    Returns: Dict mapping each stem to its Ten God relationship
    """
    dm_element = dm_stem["element"]
    dm_polarity = dm_stem["polarity"]
    
    mapping = {}
    for stem in HEAVENLY_STEMS:
        ten_god = calculate_ten_god(dm_element, dm_polarity, 
                                    stem["element"], stem["polarity"])
        mapping[stem["chinese"]] = {
            "stem_chinese": stem["chinese"],
            "stem_pinyin": stem["pinyin"],
            "stem_element": stem["element"],
            "stem_polarity": stem["polarity"],
            "ten_god_name": ten_god["name"],
            "ten_god_chinese": ten_god["chinese"],
            "ten_god_category": ten_god["category"]
        }
    
    return mapping


# =============================================================================
# STRENGTH ASSESSMENT
# =============================================================================

def assess_day_master_strength(dm_element: str, month_branch_index: int,
                                pillars: Dict, ten_gods_in_chart: List[str]) -> Dict:
    """
    Assess Day Master strength based on:
    1. Seasonal strength (月令)
    2. Support from other pillars
    3. Ten Gods balance
    
    Returns: Dict with strength assessment
    """
    season = get_season(month_branch_index)
    seasonal_strength = ELEMENT_SEASONAL_STRENGTH[dm_element][season]
    
    # Count supporting vs draining elements
    support_count = 0  # Resource + Companion
    drain_count = 0    # Output + Wealth + Authority
    
    for god in ten_gods_in_chart:
        if god in ["Friend", "Rob Wealth", "Direct Resource", "Indirect Resource"]:
            support_count += 1
        elif god in ["Eating God", "Hurting Officer", "Direct Wealth", "Indirect Wealth",
                     "Direct Officer", "7 Killings"]:
            drain_count += 1
    
    # Calculate strength score (1-10)
    base_score = {"Prosperous": 8, "Strong": 6, "Weak": 4, "Dead": 2}[seasonal_strength]
    
    # Adjust for support/drain balance
    balance_modifier = (support_count - drain_count) * 0.5
    strength_score = max(1, min(10, base_score + balance_modifier))
    
    # Determine strength category
    if strength_score >= 7:
        if strength_score >= 9:
            strength_category = "Extremely Strong"
        else:
            strength_category = "Strong"
    elif strength_score >= 4:
        strength_category = "Balanced"
    else:
        if strength_score <= 2:
            strength_category = "Extremely Weak"
        else:
            strength_category = "Weak"
    
    return {
        "season": season,
        "seasonal_strength": seasonal_strength,
        "support_count": support_count,
        "drain_count": drain_count,
        "strength_score": round(strength_score, 1),
        "strength_category": strength_category
    }


# =============================================================================
# USEFUL GODS CALCULATION
# =============================================================================

def calculate_useful_gods(dm_element: str, strength_category: str) -> Dict:
    """
    Calculate Useful Gods based on Day Master element and strength
    
    Weak DM → Need Resource (produces DM) + Companion (same element)
    Strong DM → Need Output (DM produces) + Wealth (DM controls) + Authority (controls DM)
    """
    resource_element = ELEMENT_PRODUCED_BY[dm_element]
    companion_element = dm_element
    output_element = ELEMENT_PRODUCES[dm_element]
    wealth_element = ELEMENT_CONTROLS[dm_element]
    authority_element = ELEMENT_CONTROLLED_BY[dm_element]
    
    if "Weak" in strength_category:
        return {
            "primary": resource_element,
            "secondary": companion_element,
            "tertiary": None,
            "unfavorable": [output_element, wealth_element],
            "reasoning": f"Weak {dm_element} Day Master needs strengthening. "
                        f"{resource_element} (Resource) produces and supports {dm_element}. "
                        f"More {companion_element} (Companion) provides peer support. "
                        f"Avoid {output_element}/{wealth_element} which drain energy."
        }
    elif "Strong" in strength_category:
        return {
            "primary": output_element,
            "secondary": wealth_element,
            "tertiary": authority_element,
            "unfavorable": [resource_element, companion_element],
            "reasoning": f"Strong {dm_element} Day Master needs draining/balancing. "
                        f"{output_element} (Output) channels excess energy productively. "
                        f"{wealth_element} (Wealth) gives purpose. "
                        f"{authority_element} (Authority) provides discipline. "
                        f"Avoid more {resource_element}/{companion_element} which over-strengthen."
        }
    else:  # Balanced
        return {
            "primary": output_element,
            "secondary": wealth_element,
            "tertiary": resource_element,
            "unfavorable": [],
            "reasoning": f"Balanced {dm_element} Day Master can benefit from most elements. "
                        f"{output_element} for creativity, {wealth_element} for prosperity, "
                        f"{resource_element} for support when needed."
        }


# =============================================================================
# SPECIAL STRUCTURES DETECTION
# =============================================================================

def detect_special_structures(pillars: Dict, dm_stem: Dict) -> Dict:
    """
    Detect special BaZi structures
    
    Returns: Dict of detected structures
    """
    structures = {
        "wealth_vault": False,
        "wealth_vault_branch": None,
        "nobleman_present": False,
        "nobleman_branches": [],
        "six_combinations": [],
        "six_clashes": [],
        "three_harmonies": [],
        "other_structures": []
    }
    
    # Collect all branches in chart
    branches = []
    for pillar_name in ["year", "month", "day", "hour"]:
        if pillar_name in pillars and "branch" in pillars[pillar_name]:
            branches.append(pillars[pillar_name]["branch"]["chinese"])
    
    branch_indices = []
    for b in branches:
        branch_data = get_branch_by_chinese(b)
        if branch_data:
            branch_indices.append(branch_data["index"])
    
    # Check Wealth Vault
    dm_element = dm_stem["element"]
    wealth_vault_branch = WEALTH_VAULT.get(dm_element)
    if wealth_vault_branch and wealth_vault_branch in branches:
        structures["wealth_vault"] = True
        structures["wealth_vault_branch"] = wealth_vault_branch
    
    # Check Nobleman Stars
    dm_chinese = dm_stem["chinese"]
    if dm_chinese in NOBLEMAN_LOOKUP:
        nobleman_branches = NOBLEMAN_LOOKUP[dm_chinese]
        for nb in nobleman_branches:
            if nb in branches:
                structures["nobleman_present"] = True
                structures["nobleman_branches"].append(nb)
    
    # Check Six Combinations
    for combo in SIX_COMBINATIONS:
        if combo[0] in branch_indices and combo[1] in branch_indices:
            b1 = EARTHLY_BRANCHES[combo[0]]["chinese"]
            b2 = EARTHLY_BRANCHES[combo[1]]["chinese"]
            structures["six_combinations"].append(f"{b1}{b2}合")
    
    # Check Six Clashes
    for clash in SIX_CLASHES:
        if clash[0] in branch_indices and clash[1] in branch_indices:
            b1 = EARTHLY_BRANCHES[clash[0]]["chinese"]
            b2 = EARTHLY_BRANCHES[clash[1]]["chinese"]
            structures["six_clashes"].append(f"{b1}{b2}冲")
    
    # Check Three Harmonies
    for frame_name, frame_branches in THREE_HARMONIES.items():
        matches = sum(1 for fb in frame_branches if fb in branch_indices)
        if matches >= 2:
            structures["three_harmonies"].append({
                "frame": frame_name,
                "complete": matches == 3,
                "produces": ELEMENT_PRODUCES.get(frame_name, frame_name)
            })
    
    return structures


# =============================================================================
# ACTIVATION PERCENTAGE CALCULATION
# =============================================================================

def calculate_activation_percentage(useful_gods: Dict, elements_in_chart: Dict) -> Dict:
    """
    Calculate what percentage of useful gods are activated in the chart
    
    elements_in_chart: Dict with element counts {"Wood": 2, "Fire": 1, ...}
    """
    total_elements = sum(elements_in_chart.values())
    if total_elements == 0:
        total_elements = 1  # Avoid division by zero
    
    activation = {}
    
    # Primary useful god activation
    primary = useful_gods.get("primary")
    if primary:
        count = elements_in_chart.get(primary, 0)
        activation["primary_element"] = primary
        activation["primary_count"] = count
        activation["primary_percentage"] = round((count / total_elements) * 100, 1)
    
    # Secondary useful god activation
    secondary = useful_gods.get("secondary")
    if secondary:
        count = elements_in_chart.get(secondary, 0)
        activation["secondary_element"] = secondary
        activation["secondary_count"] = count
        activation["secondary_percentage"] = round((count / total_elements) * 100, 1)
    
    # Unfavorable elements
    unfavorable = useful_gods.get("unfavorable", [])
    unfavorable_count = sum(elements_in_chart.get(e, 0) for e in unfavorable)
    activation["unfavorable_count"] = unfavorable_count
    activation["unfavorable_percentage"] = round((unfavorable_count / total_elements) * 100, 1)
    
    # Overall activation score (0-10)
    primary_pct = activation.get("primary_percentage", 0)
    secondary_pct = activation.get("secondary_percentage", 0)
    unfavorable_pct = activation.get("unfavorable_percentage", 0)
    
    score = ((primary_pct * 0.5) + (secondary_pct * 0.3) - (unfavorable_pct * 0.2)) / 10
    activation["activation_score"] = round(max(0, min(10, score)), 1)
    
    return activation


# =============================================================================
# BAZI ALIGNMENT SCORE CALCULATION
# =============================================================================

def calculate_bazi_alignment_score(useful_gods: Dict, 
                                   qmdj_elements: Dict,
                                   special_structures: Dict,
                                   dm_strength: Dict) -> Dict:
    """
    Calculate BaZi alignment score for QMDJ integration
    
    qmdj_elements: Dict of elements present in QMDJ chart
                   e.g., {"heaven_stem": "Wood", "earth_stem": "Water", 
                          "door": "Wood", "star": "Wood", "deity": "Earth"}
    """
    score = 5.0  # Base score
    breakdown = []
    
    primary_ug = useful_gods.get("primary")
    secondary_ug = useful_gods.get("secondary")
    unfavorable = useful_gods.get("unfavorable", [])
    
    # Check each QMDJ component
    for component, element in qmdj_elements.items():
        if element == primary_ug:
            score += 1.5
            breakdown.append(f"+1.5: {component} ({element}) = Primary Useful God")
        elif element == secondary_ug:
            score += 1.0
            breakdown.append(f"+1.0: {component} ({element}) = Secondary Useful God")
        elif element in unfavorable:
            score -= 1.0
            breakdown.append(f"-1.0: {component} ({element}) = Unfavorable Element")
    
    # Special structures bonus
    if special_structures.get("wealth_vault"):
        score += 0.5
        breakdown.append("+0.5: Wealth Vault present")
    
    if special_structures.get("nobleman_present"):
        score += 0.5
        breakdown.append("+0.5: Nobleman Star present")
    
    if special_structures.get("six_clashes"):
        score -= 1.0
        breakdown.append("-1.0: Six Clash present (conflict)")
    
    # Cap score between 0-10
    final_score = round(max(0, min(10, score)), 1)
    
    return {
        "base_score": 5.0,
        "final_score": final_score,
        "breakdown": breakdown,
        "verdict": get_alignment_verdict(final_score)
    }


def get_alignment_verdict(score: float) -> str:
    """Get alignment verdict from score"""
    if score >= 8:
        return "Excellent Alignment"
    elif score >= 6:
        return "Good Alignment"
    elif score >= 4:
        return "Mixed Alignment"
    elif score >= 2:
        return "Poor Alignment"
    else:
        return "Conflicting Alignment"


# =============================================================================
# EXPORT FUNCTION: COMPLETE BAZI DATA
# =============================================================================

def generate_complete_bazi_export(dm_stem_input: str, 
                                   pillars: Dict = None,
                                   qmdj_elements: Dict = None) -> Dict:
    """
    Generate complete BaZi data for JSON export
    
    dm_stem_input: Chinese character or pinyin of Day Master stem
    pillars: Dict of Four Pillars (optional, for full analysis)
    qmdj_elements: Dict of QMDJ chart elements (optional, for alignment score)
    
    Returns: Complete BaZi data structure for Universal Schema v2.0
    """
    # Get Day Master stem data
    dm_stem = get_stem_by_chinese(dm_stem_input) or get_stem_by_pinyin(dm_stem_input)
    if not dm_stem:
        return {"error": f"Unknown Day Master: {dm_stem_input}"}
    
    # Generate Ten Gods mapping
    ten_gods_mapping = generate_complete_ten_gods_mapping(dm_stem)
    
    # Default pillars if not provided
    if pillars is None:
        pillars = {}
    
    # Collect Ten Gods in chart (from pillars)
    ten_gods_in_chart = []
    elements_in_chart = {"Wood": 0, "Fire": 0, "Earth": 0, "Metal": 0, "Water": 0}
    
    for pillar_name in ["year", "month", "day", "hour"]:
        if pillar_name in pillars:
            pillar = pillars[pillar_name]
            if "stem" in pillar:
                stem_chinese = pillar["stem"].get("chinese", "")
                if stem_chinese in ten_gods_mapping:
                    god_name = ten_gods_mapping[stem_chinese]["ten_god_name"]
                    ten_gods_in_chart.append(god_name)
                    elements_in_chart[pillar["stem"]["element"]] += 1
            if "branch" in pillar:
                elements_in_chart[pillar["branch"]["element"]] += 1
    
    # Get month branch index (default to current if not provided)
    month_branch_index = 0
    if "month" in pillars and "branch" in pillars["month"]:
        month_branch_index = pillars["month"]["branch"].get("index", 0)
    
    # Assess strength
    strength = assess_day_master_strength(
        dm_stem["element"], 
        month_branch_index,
        pillars,
        ten_gods_in_chart
    )
    
    # Calculate useful gods
    useful_gods = calculate_useful_gods(dm_stem["element"], strength["strength_category"])
    
    # Detect special structures
    special_structures = detect_special_structures(pillars, dm_stem)
    
    # Calculate activation percentage
    activation = calculate_activation_percentage(useful_gods, elements_in_chart)
    
    # Calculate BaZi alignment score (if QMDJ elements provided)
    alignment_score = None
    if qmdj_elements:
        alignment_score = calculate_bazi_alignment_score(
            useful_gods, qmdj_elements, special_structures, strength
        )
    
    # Determine dominant Ten God (most frequent in chart)
    from collections import Counter
    god_counts = Counter(ten_gods_in_chart)
    dominant_god = god_counts.most_common(1)[0][0] if god_counts else "Unknown"
    profile = TEN_GOD_PROFILES.get(dominant_god, {})
    
    # Build complete export structure
    return {
        "chart_source": "BaZi Calculator",
        "day_master": {
            "stem_chinese": dm_stem["chinese"],
            "stem_pinyin": dm_stem["pinyin"],
            "element": dm_stem["element"],
            "polarity": dm_stem["polarity"],
            "strength": strength["strength_category"],
            "strength_score": strength["strength_score"],
            "season": strength["season"],
            "seasonal_strength": strength["seasonal_strength"]
        },
        "four_pillars": pillars if pillars else "Not calculated",
        "ten_gods_mapping": ten_gods_mapping,
        "ten_gods_in_chart": ten_gods_in_chart,
        "useful_gods": {
            "primary": useful_gods["primary"],
            "secondary": useful_gods["secondary"],
            "tertiary": useful_gods.get("tertiary"),
            "unfavorable": useful_gods["unfavorable"],
            "reasoning": useful_gods["reasoning"]
        },
        "useful_god_activation": activation,
        "ten_god_profile": {
            "dominant_god": dominant_god,
            "profile_name": profile.get("profile_name", "Unknown"),
            "behavioral_traits": profile.get("traits", []),
            "strengths": profile.get("strengths", []),
            "challenges": profile.get("challenges", [])
        },
        "special_structures": special_structures,
        "bazi_alignment_score": alignment_score
    }


# =============================================================================
# TEST / DEMO
# =============================================================================

if __name__ == "__main__":
    # Demo: Geng Metal Day Master analysis
    print("=" * 60)
    print("BaZi Calculator Demo: Geng Metal Day Master")
    print("=" * 60)
    
    # Example pillars (simplified)
    example_pillars = {
        "year": {
            "stem": {"chinese": "甲", "pinyin": "Jia", "element": "Wood", "polarity": "Yang"},
            "branch": {"chinese": "子", "pinyin": "Zi", "element": "Water", "index": 0}
        },
        "month": {
            "stem": {"chinese": "丙", "pinyin": "Bing", "element": "Fire", "polarity": "Yang"},
            "branch": {"chinese": "午", "pinyin": "Wu", "element": "Fire", "index": 6}
        },
        "day": {
            "stem": {"chinese": "庚", "pinyin": "Geng", "element": "Metal", "polarity": "Yang"},
            "branch": {"chinese": "寅", "pinyin": "Yin", "element": "Wood", "index": 2}
        },
        "hour": {
            "stem": {"chinese": "戊", "pinyin": "Wu", "element": "Earth", "polarity": "Yang"},
            "branch": {"chinese": "戌", "pinyin": "Xu", "element": "Earth", "index": 10}
        }
    }
    
    # Example QMDJ elements (from a chart)
    qmdj_elements = {
        "heaven_stem": "Wood",
        "earth_stem": "Water",
        "door": "Wood",
        "star": "Wood",
        "deity": "Earth"
    }
    
    result = generate_complete_bazi_export("庚", example_pillars, qmdj_elements)
    print(json.dumps(result, indent=2, ensure_ascii=False))
