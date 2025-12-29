# -*- coding: utf-8 -*-
"""
Ming Qimen 明奇门 - QMDJ Engine v1.0
Phase 4: Real QMDJ calculations with kinqimen integration

This module provides:
1. Integration with kinqimen library (when available)
2. Fallback pure-Python calculations
3. Joey Yap terminology mapping
4. Universal Schema v2.0 compliant output
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple, Any
import json

# Singapore timezone
SGT = timezone(timedelta(hours=8))

# ============================================================================
# CONSTANTS & MAPPINGS
# ============================================================================

# Luo Shu Magic Square - Palace Numbers to Trigram/Direction
PALACE_INFO = {
    1: {"name": "Kan", "chinese": "坎", "direction": "N", "element": "Water"},
    2: {"name": "Kun", "chinese": "坤", "direction": "SW", "element": "Earth"},
    3: {"name": "Zhen", "chinese": "震", "direction": "E", "element": "Wood"},
    4: {"name": "Xun", "chinese": "巽", "direction": "SE", "element": "Wood"},
    5: {"name": "Center", "chinese": "中", "direction": "Center", "element": "Earth"},
    6: {"name": "Qian", "chinese": "乾", "direction": "NW", "element": "Metal"},
    7: {"name": "Dui", "chinese": "兌", "direction": "W", "element": "Metal"},
    8: {"name": "Gen", "chinese": "艮", "direction": "NE", "element": "Earth"},
    9: {"name": "Li", "chinese": "離", "direction": "S", "element": "Fire"}
}

# Topic mapping (Ming Qimen user-friendly topics)
PALACE_TOPICS = {
    1: {"topic": "Career", "icon": "💼", "description": "Job, business, life path"},
    2: {"topic": "Relations", "icon": "💕", "description": "Marriage, partnerships"},
    3: {"topic": "Health", "icon": "💪", "description": "Health, family, new starts"},
    4: {"topic": "Wealth", "icon": "💰", "description": "Money, investments"},
    5: {"topic": "Self", "icon": "🎯", "description": "General, yourself"},
    6: {"topic": "Mentor", "icon": "🤝", "description": "Helpful people, travel"},
    7: {"topic": "Children", "icon": "👶", "description": "Creativity, joy, projects"},
    8: {"topic": "Knowledge", "icon": "📚", "description": "Education, skills"},
    9: {"topic": "Fame", "icon": "🌟", "description": "Recognition, reputation"}
}

# Ten Heavenly Stems
STEMS = {
    "甲": {"pinyin": "Jia", "element": "Wood", "polarity": "Yang"},
    "乙": {"pinyin": "Yi", "element": "Wood", "polarity": "Yin"},
    "丙": {"pinyin": "Bing", "element": "Fire", "polarity": "Yang"},
    "丁": {"pinyin": "Ding", "element": "Fire", "polarity": "Yin"},
    "戊": {"pinyin": "Wu", "element": "Earth", "polarity": "Yang"},
    "己": {"pinyin": "Ji", "element": "Earth", "polarity": "Yin"},
    "庚": {"pinyin": "Geng", "element": "Metal", "polarity": "Yang"},
    "辛": {"pinyin": "Xin", "element": "Metal", "polarity": "Yin"},
    "壬": {"pinyin": "Ren", "element": "Water", "polarity": "Yang"},
    "癸": {"pinyin": "Gui", "element": "Water", "polarity": "Yin"}
}

# Twelve Earthly Branches
BRANCHES = {
    "子": {"pinyin": "Zi", "element": "Water", "animal": "Rat"},
    "丑": {"pinyin": "Chou", "element": "Earth", "animal": "Ox"},
    "寅": {"pinyin": "Yin", "element": "Wood", "animal": "Tiger"},
    "卯": {"pinyin": "Mao", "element": "Wood", "animal": "Rabbit"},
    "辰": {"pinyin": "Chen", "element": "Earth", "animal": "Dragon"},
    "巳": {"pinyin": "Si", "element": "Fire", "animal": "Snake"},
    "午": {"pinyin": "Wu", "element": "Fire", "animal": "Horse"},
    "未": {"pinyin": "Wei", "element": "Earth", "animal": "Goat"},
    "申": {"pinyin": "Shen", "element": "Metal", "animal": "Monkey"},
    "酉": {"pinyin": "You", "element": "Metal", "animal": "Rooster"},
    "戌": {"pinyin": "Xu", "element": "Earth", "animal": "Dog"},
    "亥": {"pinyin": "Hai", "element": "Water", "animal": "Pig"}
}

# Chinese Hour (Shichen) mapping
CHINESE_HOURS = {
    (23, 1): ("子", "Zi", "Rat"),
    (1, 3): ("丑", "Chou", "Ox"),
    (3, 5): ("寅", "Yin", "Tiger"),
    (5, 7): ("卯", "Mao", "Rabbit"),
    (7, 9): ("辰", "Chen", "Dragon"),
    (9, 11): ("巳", "Si", "Snake"),
    (11, 13): ("午", "Wu", "Horse"),
    (13, 15): ("未", "Wei", "Goat"),
    (15, 17): ("申", "Shen", "Monkey"),
    (17, 19): ("酉", "You", "Rooster"),
    (19, 21): ("戌", "Xu", "Dog"),
    (21, 23): ("亥", "Hai", "Pig")
}

# Nine Stars - kinqimen Chinese → Joey Yap English
STAR_MAPPING = {
    "蓬": {"english": "Canopy", "chinese": "天蓬", "element": "Water", "nature": "Inauspicious"},
    "芮": {"english": "Grass", "chinese": "天芮", "element": "Earth", "nature": "Inauspicious"},
    "沖": {"english": "Impulse", "chinese": "天沖", "element": "Wood", "nature": "Neutral"},
    "輔": {"english": "Assistant", "chinese": "天輔", "element": "Wood", "nature": "Auspicious"},
    "禽": {"english": "Connect", "chinese": "天禽", "element": "Earth", "nature": "Auspicious"},
    "心": {"english": "Heart", "chinese": "天心", "element": "Metal", "nature": "Auspicious"},
    "柱": {"english": "Pillar", "chinese": "天柱", "element": "Metal", "nature": "Inauspicious"},
    "任": {"english": "Ren", "chinese": "天任", "element": "Earth", "nature": "Auspicious"},
    "英": {"english": "Hero", "chinese": "天英", "element": "Fire", "nature": "Auspicious"}
}

# Eight Doors - kinqimen Chinese → Joey Yap English
DOOR_MAPPING = {
    "開": {"english": "Open", "chinese": "開門", "element": "Metal", "nature": "Auspicious"},
    "休": {"english": "Rest", "chinese": "休門", "element": "Water", "nature": "Auspicious"},
    "生": {"english": "Life", "chinese": "生門", "element": "Earth", "nature": "Auspicious"},
    "傷": {"english": "Harm", "chinese": "傷門", "element": "Wood", "nature": "Inauspicious"},
    "杜": {"english": "Delusion", "chinese": "杜門", "element": "Wood", "nature": "Neutral"},
    "景": {"english": "Scenery", "chinese": "景門", "element": "Fire", "nature": "Neutral"},
    "死": {"english": "Death", "chinese": "死門", "element": "Earth", "nature": "Inauspicious"},
    "驚": {"english": "Fear", "chinese": "驚門", "element": "Metal", "nature": "Inauspicious"},
    "开": {"english": "Open", "chinese": "開門", "element": "Metal", "nature": "Auspicious"},
    "生": {"english": "Life", "chinese": "生門", "element": "Earth", "nature": "Auspicious"},
    "伤": {"english": "Harm", "chinese": "傷門", "element": "Wood", "nature": "Inauspicious"},
    "杜": {"english": "Delusion", "chinese": "杜門", "element": "Wood", "nature": "Neutral"},
    "景": {"english": "Scenery", "chinese": "景門", "element": "Fire", "nature": "Neutral"},
    "惊": {"english": "Fear", "chinese": "驚門", "element": "Metal", "nature": "Inauspicious"}
}

# Ming Qimen friendly door names
DOOR_FRIENDLY = {
    "Death": "Stillness",
    "Fear": "Surprise"
}

# Eight Deities - kinqimen Chinese → Joey Yap English
DEITY_MAPPING = {
    "符": {"english": "Chief", "chinese": "值符", "nature": "Auspicious", "function": "Leadership, authority, protection"},
    "蛇": {"english": "Serpent", "chinese": "螣蛇", "nature": "Inauspicious", "function": "Deception, anxiety, obstacles"},
    "陰": {"english": "Moon", "chinese": "太陰", "nature": "Auspicious", "function": "Hidden support, secrets, intuition"},
    "合": {"english": "Six Harmony", "chinese": "六合", "nature": "Auspicious", "function": "Relationships, partnerships, agreements"},
    "勾": {"english": "Hook", "chinese": "勾陳", "nature": "Inauspicious", "function": "Entanglement, disputes, legal issues"},
    "雀": {"english": "Bird", "chinese": "朱雀", "nature": "Inauspicious", "function": "Arguments, gossip, communication issues"},
    "虎": {"english": "Tiger", "chinese": "白虎", "nature": "Inauspicious", "function": "Violence, accidents, loss"},
    "玄": {"english": "Emptiness", "chinese": "玄武", "nature": "Neutral", "function": "Theft, deception, hidden matters"},
    "地": {"english": "Nine Earth", "chinese": "九地", "nature": "Auspicious", "function": "Stability, grounding, real estate"},
    "天": {"english": "Nine Heaven", "chinese": "九天", "nature": "Auspicious", "function": "Expansion, promotion, flying high"}
}

# Element production and control cycles
ELEMENT_PRODUCES = {
    'Water': 'Wood', 'Wood': 'Fire', 'Fire': 'Earth',
    'Earth': 'Metal', 'Metal': 'Water'
}

ELEMENT_CONTROLS = {
    'Water': 'Fire', 'Fire': 'Metal', 'Metal': 'Wood',
    'Wood': 'Earth', 'Earth': 'Water'
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_chinese_hour(hour: int) -> Tuple[str, str, str]:
    """Convert Western hour (0-23) to Chinese hour (Shichen)"""
    for (start, end), (chinese, pinyin, animal) in CHINESE_HOURS.items():
        if start == 23:  # Special case for Zi hour spanning midnight
            if hour >= 23 or hour < 1:
                return chinese, pinyin, animal
        elif start <= hour < end:
            return chinese, pinyin, animal
    return "子", "Zi", "Rat"  # Default


def calculate_strength(component_element: str, palace_element: str) -> Tuple[str, int]:
    """
    Calculate component strength based on palace element relationship.
    
    Returns (strength_status, strength_score):
    - Timely: +2 (Same element as Palace)
    - Prosperous: +3 (Produced by Palace element)
    - Resting: 0 (Produces Palace element)
    - Confined: -2 (Controlled by Palace element)
    - Dead: -3 (Controls Palace = exhausted)
    """
    if not component_element or not palace_element:
        return "Unknown", 0
    
    if component_element == palace_element:
        return "Timely", 2
    
    if ELEMENT_PRODUCES.get(palace_element) == component_element:
        return "Prosperous", 3
    
    if ELEMENT_CONTROLS.get(palace_element) == component_element:
        return "Confined", -2
    
    if ELEMENT_CONTROLS.get(component_element) == palace_element:
        return "Dead", -3
    
    return "Resting", 0


def strength_to_friendly(strength: str, score: int) -> Tuple[str, str]:
    """Convert technical strength terms to Ming Qimen friendly terms"""
    friendly_map = {
        "Timely": ("🔥 High Energy", "Take Action!"),
        "Prosperous": ("✨ Good Energy", "Favorable"),
        "Resting": ("😐 Balanced", "Proceed Normally"),
        "Confined": ("🌙 Low Energy", "Be Patient"),
        "Dead": ("💤 Rest Energy", "Wait & Reflect"),
        "Unknown": ("❓ Unknown", "Assess Carefully")
    }
    return friendly_map.get(strength, ("❓ Unknown", "Assess Carefully"))


def get_stem_info(stem_char: str) -> Dict:
    """Get detailed info for a Heavenly Stem"""
    if stem_char in STEMS:
        info = STEMS[stem_char].copy()
        info["chinese"] = stem_char
        return info
    
    # Try to find by pinyin
    for chinese, info in STEMS.items():
        if info["pinyin"].lower() == stem_char.lower():
            result = info.copy()
            result["chinese"] = chinese
            return result
    
    return {"chinese": stem_char, "pinyin": "Unknown", "element": "Unknown", "polarity": "Unknown"}


# ============================================================================
# KINQIMEN WRAPPER
# ============================================================================

class QMDJEngine:
    """
    Qi Men Dun Jia calculation engine.
    Wraps kinqimen library with fallback to mock calculations.
    """
    
    def __init__(self):
        self.kinqimen_available = False
        self._try_import_kinqimen()
    
    def _try_import_kinqimen(self):
        """Attempt to import kinqimen library"""
        try:
            from kinqimen import kinqimen
            self.kinqimen = kinqimen
            self.kinqimen_available = True
        except ImportError as e:
            self.kinqimen = None
            self.kinqimen_available = False
            print(f"kinqimen not available: {e}. Using fallback calculations.")
    
    def get_chart(self, year: int, month: int, day: int, hour: int, 
                  minute: int = 0, method: int = 1) -> Dict:
        """
        Generate QMDJ chart for given datetime.
        
        Args:
            year, month, day, hour, minute: DateTime components
            method: 1 = Chai Bu (拆補), 2 = Zhi Run (置閏)
        
        Returns:
            Dict with full chart data in kinqimen format
        """
        if self.kinqimen_available:
            try:
                qm = self.kinqimen.Qimen(year, month, day, hour, minute)
                return qm.pan(method)
            except Exception as e:
                print(f"kinqimen error: {e}. Using fallback.")
        
        return self._fallback_chart(year, month, day, hour, minute, method)
    
    def _fallback_chart(self, year: int, month: int, day: int, 
                        hour: int, minute: int, method: int) -> Dict:
        """
        Generate fallback chart when kinqimen is unavailable.
        Uses simplified calculations for demonstration.
        """
        # Simplified Ju calculation based on date
        # In reality, this requires solar term calculations
        day_num = (year * 365 + month * 30 + day + hour) % 9 + 1
        is_yang = (month <= 6)  # Simplified: first half = Yang Dun
        
        structure = "陽遁" if is_yang else "陰遁"
        ju_num = day_num if is_yang else (10 - day_num) % 9 or 9
        
        # Generate palace arrangements based on Ju number
        earth_plate = self._generate_earth_plate(ju_num, is_yang)
        sky_plate = self._generate_sky_plate(ju_num, is_yang, hour)
        stars = self._generate_stars(ju_num, hour)
        doors = self._generate_doors(ju_num, hour)
        deities = self._generate_deities(ju_num, hour)
        
        # Get Chinese hour
        chinese_hour, hour_pinyin, hour_animal = get_chinese_hour(hour)
        
        return {
            "排盤方式": {1: "拆補", 2: "置閏"}.get(method, "拆補"),
            "干支": f"{year}年{month}月{day}日{hour}時",
            "旬首": "甲子",  # Simplified
            "旬空": "戌亥",  # Simplified
            "局日": "甲己日",  # Simplified
            "排局": f"{structure}第{ju_num}局",
            "節氣": self._get_solar_term(month, day),
            "值符值使": {
                "值符天干": ["甲子", "戊"],
                "值符星宮": ["心", "乾"],
                "值使門宮": ["開", "乾"]
            },
            "天乙": "乾",
            "天盤": sky_plate,
            "地盤": earth_plate,
            "門": doors,
            "星": stars,
            "神": deities,
            "馬星": {
                "天馬": "申",
                "丁馬": "巳",
                "驛馬": "寅"
            },
            "長生運": {},
            "_metadata": {
                "calculation_mode": "fallback",
                "structure": structure,
                "ju_number": ju_num,
                "chinese_hour": f"{chinese_hour}時 ({hour_pinyin})"
            }
        }
    
    def _generate_earth_plate(self, ju_num: int, is_yang: bool) -> Dict:
        """Generate Earth Plate stem arrangement"""
        stems_yang = list("戊己庚辛壬癸丁丙乙")
        stems_yin = list("戊乙丙丁癸壬辛庚己")
        stems = stems_yang if is_yang else stems_yin
        
        # Rotate based on Ju number
        start_idx = (ju_num - 1) % 9
        rotated = stems[start_idx:] + stems[:start_idx]
        
        palaces = ["坎", "坤", "震", "巽", "中", "乾", "兌", "艮", "離"]
        return dict(zip(palaces, rotated))
    
    def _generate_sky_plate(self, ju_num: int, is_yang: bool, hour: int) -> Dict:
        """Generate Heaven Plate stem arrangement"""
        # Simplified: rotate earth plate by hour offset
        earth = self._generate_earth_plate(ju_num, is_yang)
        stems = list(earth.values())
        offset = hour % 9
        rotated = stems[offset:] + stems[:offset]
        return dict(zip(earth.keys(), rotated))
    
    def _generate_stars(self, ju_num: int, hour: int) -> Dict:
        """Generate Nine Stars arrangement"""
        stars_order = list("蓬芮沖輔禽心柱任英")
        palaces = ["坎", "坤", "震", "巽", "中", "乾", "兌", "艮", "離"]
        
        # Rotate based on ju and hour
        offset = (ju_num + hour) % 9
        rotated = stars_order[offset:] + stars_order[:offset]
        return dict(zip(palaces, rotated))
    
    def _generate_doors(self, ju_num: int, hour: int) -> Dict:
        """Generate Eight Doors arrangement"""
        doors_order = list("休死傷杜中開驚生景")
        palaces = ["坎", "坤", "震", "巽", "中", "乾", "兌", "艮", "離"]
        
        offset = (ju_num + hour) % 9
        rotated = doors_order[offset:] + doors_order[:offset]
        return dict(zip(palaces, rotated))
    
    def _generate_deities(self, ju_num: int, hour: int) -> Dict:
        """Generate Eight Deities arrangement"""
        deities_yang = list("符蛇陰合勾雀地天")
        deities_yin = list("符蛇陰合虎玄地天")
        palaces = ["坎", "坤", "震", "巽", "乾", "兌", "艮", "離"]  # No center
        
        is_yang = ju_num <= 5
        deities = deities_yang if is_yang else deities_yin
        
        offset = (ju_num + hour) % 8
        rotated = deities[offset:] + deities[:offset]
        return dict(zip(palaces, rotated))
    
    def _get_solar_term(self, month: int, day: int) -> str:
        """Get approximate solar term"""
        solar_terms = [
            "小寒", "大寒", "立春", "雨水", "驚蟄", "春分",
            "清明", "穀雨", "立夏", "小滿", "芒種", "夏至",
            "小暑", "大暑", "立秋", "處暑", "白露", "秋分",
            "寒露", "霜降", "立冬", "小雪", "大雪", "冬至"
        ]
        idx = ((month - 1) * 2 + (1 if day > 15 else 0)) % 24
        return solar_terms[idx]


# ============================================================================
# CHART PROCESSOR - Convert raw kinqimen to Universal Schema
# ============================================================================

class ChartProcessor:
    """Process raw kinqimen output into Ming Qimen format"""
    
    def __init__(self, raw_chart: Dict, selected_palace: int = 5):
        self.raw = raw_chart
        self.palace_num = selected_palace
        self.palace_info = PALACE_INFO[selected_palace]
        self.palace_element = self.palace_info["element"]
    
    def get_palace_name(self) -> str:
        """Get palace name in Chinese"""
        return self.palace_info["chinese"]
    
    def get_heaven_stem(self) -> Dict:
        """Extract and process Heaven Stem for selected palace"""
        palace_name = self.get_palace_name()
        sky_plate = self.raw.get("天盤", {})
        stem_char = sky_plate.get(palace_name, "戊")
        
        stem_info = get_stem_info(stem_char)
        strength, score = calculate_strength(stem_info["element"], self.palace_element)
        friendly, advice = strength_to_friendly(strength, score)
        
        return {
            "character": stem_char,
            "pinyin": stem_info["pinyin"],
            "chinese": stem_info["chinese"],
            "element": stem_info["element"],
            "polarity": stem_info["polarity"],
            "strength_in_palace": strength,
            "strength_score": score,
            "friendly_strength": friendly,
            "advice": advice
        }
    
    def get_earth_stem(self) -> Dict:
        """Extract and process Earth Stem for selected palace"""
        palace_name = self.get_palace_name()
        earth_plate = self.raw.get("地盤", {})
        stem_char = earth_plate.get(palace_name, "戊")
        
        stem_info = get_stem_info(stem_char)
        strength, score = calculate_strength(stem_info["element"], self.palace_element)
        friendly, advice = strength_to_friendly(strength, score)
        
        return {
            "character": stem_char,
            "pinyin": stem_info["pinyin"],
            "chinese": stem_info["chinese"],
            "element": stem_info["element"],
            "polarity": stem_info["polarity"],
            "strength_in_palace": strength,
            "strength_score": score,
            "friendly_strength": friendly,
            "advice": advice
        }
    
    def get_star(self) -> Dict:
        """Extract and process Star for selected palace"""
        palace_name = self.get_palace_name()
        stars = self.raw.get("星", {})
        star_char = stars.get(palace_name, "心")
        
        star_info = STAR_MAPPING.get(star_char, {
            "english": "Unknown",
            "chinese": f"天{star_char}",
            "element": "Earth",
            "nature": "Neutral"
        })
        
        strength, score = calculate_strength(star_info["element"], self.palace_element)
        friendly, advice = strength_to_friendly(strength, score)
        
        return {
            "name": star_info["english"],
            "chinese": star_info["chinese"],
            "element": star_info["element"],
            "nature": star_info["nature"],
            "strength_in_palace": strength,
            "strength_score": score,
            "friendly_strength": friendly,
            "advice": advice
        }
    
    def get_door(self) -> Dict:
        """Extract and process Door for selected palace"""
        palace_name = self.get_palace_name()
        doors = self.raw.get("門", {})
        door_char = doors.get(palace_name, "開")
        
        door_info = DOOR_MAPPING.get(door_char, {
            "english": "Unknown",
            "chinese": f"{door_char}門",
            "element": "Earth",
            "nature": "Neutral"
        })
        
        # Apply friendly name substitution
        english_name = door_info["english"]
        friendly_name = DOOR_FRIENDLY.get(english_name, english_name)
        
        strength, score = calculate_strength(door_info["element"], self.palace_element)
        friendly_strength, advice = strength_to_friendly(strength, score)
        
        return {
            "name": english_name,
            "friendly_name": friendly_name,
            "chinese": door_info["chinese"],
            "element": door_info["element"],
            "nature": door_info["nature"],
            "strength_in_palace": strength,
            "strength_score": score,
            "friendly_strength": friendly_strength,
            "advice": advice
        }
    
    def get_deity(self) -> Dict:
        """Extract and process Deity for selected palace"""
        palace_name = self.get_palace_name()
        deities = self.raw.get("神", {})
        deity_char = deities.get(palace_name, "符")
        
        deity_info = DEITY_MAPPING.get(deity_char, {
            "english": "Unknown",
            "chinese": deity_char,
            "nature": "Neutral",
            "function": ""
        })
        
        return {
            "name": deity_info["english"],
            "chinese": deity_info["chinese"],
            "nature": deity_info["nature"],
            "function": deity_info["function"]
        }
    
    def get_structure_info(self) -> Dict:
        """Extract chart structure info"""
        paiju = self.raw.get("排局", "")
        
        is_yang = "陽" in paiju
        structure = "Yang Dun" if is_yang else "Yin Dun"
        structure_chinese = "陽遁" if is_yang else "陰遁"
        
        # Extract Ju number
        import re
        ju_match = re.search(r'(\d+)', paiju)
        ju_num = int(ju_match.group(1)) if ju_match else 1
        
        return {
            "structure": structure,
            "structure_chinese": structure_chinese,
            "ju_number": ju_num,
            "method": self.raw.get("排盤方式", "拆補"),
            "solar_term": self.raw.get("節氣", ""),
            "gangzhi": self.raw.get("干支", "")
        }
    
    def get_full_palace_data(self) -> Dict:
        """Get complete processed data for selected palace"""
        topic_info = PALACE_TOPICS[self.palace_num]
        structure = self.get_structure_info()
        
        heaven_stem = self.get_heaven_stem()
        earth_stem = self.get_earth_stem()
        star = self.get_star()
        door = self.get_door()
        deity = self.get_deity()
        
        # Calculate total component score
        total_score = (
            heaven_stem["strength_score"] +
            earth_stem["strength_score"] +
            star["strength_score"] +
            door["strength_score"]
        )
        
        # Normalize to 1-10 scale
        normalized_score = round(((total_score + 12) / 24) * 9 + 1, 1)
        normalized_score = max(1, min(10, normalized_score))
        
        # Generate verdict
        if normalized_score >= 8:
            verdict = "Very Favorable"
            verdict_type = "success"
        elif normalized_score >= 6:
            verdict = "Favorable"
            verdict_type = "success"
        elif normalized_score >= 4:
            verdict = "Neutral"
            verdict_type = "info"
        elif normalized_score >= 2:
            verdict = "Challenging"
            verdict_type = "warning"
        else:
            verdict = "Very Challenging"
            verdict_type = "warning"
        
        # Generate summary and advice
        summary = self._generate_summary(heaven_stem, door, star, deity)
        advice = self._generate_advice(door, star, normalized_score)
        
        return {
            "palace": {
                "number": self.palace_num,
                "name": self.palace_info["name"],
                "chinese": self.palace_info["chinese"],
                "direction": self.palace_info["direction"],
                "element": self.palace_element,
                "topic": topic_info["topic"],
                "icon": topic_info["icon"],
                "description": topic_info["description"]
            },
            "metadata": {
                "date": "",  # To be filled by caller
                "time": "",  # To be filled by caller
                "chinese_hour": self.raw.get("_metadata", {}).get("chinese_hour", ""),
                "method": structure["method"],
                "structure": structure["structure_chinese"],
                "ju_number": structure["ju_number"],
                "solar_term": structure["solar_term"],
                "gangzhi": structure["gangzhi"]
            },
            "components": {
                "heaven_stem": heaven_stem,
                "earth_stem": earth_stem,
                "star": star,
                "door": door,
                "deity": deity
            },
            "scores": {
                "component_total": total_score,
                "normalized": normalized_score,
                "verdict": verdict,
                "verdict_type": verdict_type
            },
            "guidance": {
                "verdict": verdict,
                "type": verdict_type,
                "summary": summary,
                "advice": advice
            },
            "raw_chart": self.raw
        }
    
    def _generate_summary(self, heaven_stem: Dict, door: Dict, 
                          star: Dict, deity: Dict) -> str:
        """Generate human-readable summary"""
        door_name = door.get("friendly_name", door.get("name", "Unknown"))
        star_name = star.get("name", "Unknown")
        deity_name = deity.get("name", "Unknown")
        
        door_nature = door.get("nature", "Neutral")
        star_nature = star.get("nature", "Neutral")
        
        if door_nature == "Auspicious" and star_nature == "Auspicious":
            return f"{door_name} Door with {star_name} Star creates a favorable combination. {deity_name} Spirit adds supportive energy."
        elif door_nature == "Inauspicious" or star_nature == "Inauspicious":
            return f"{door_name} Door with {star_name} Star suggests caution. Consider timing and approach carefully."
        else:
            return f"{door_name} Door with {star_name} Star indicates balanced energy. Proceed with awareness."
    
    def _generate_advice(self, door: Dict, star: Dict, score: float) -> str:
        """Generate actionable advice"""
        door_name = door.get("friendly_name", door.get("name", ""))
        
        advice_map = {
            "Open": "Good time for new initiatives, meetings, and negotiations.",
            "Rest": "Favorable for recuperation, planning, and passive activities.",
            "Life": "Excellent for growth, investments, and new beginnings.",
            "Harm": "Avoid confrontations. Focus on self-improvement.",
            "Delusion": "Stay flexible. Things may not be as they appear.",
            "Scenery": "Good for creative work and public appearances.",
            "Stillness": "Time for reflection, not action. Wait for better timing.",
            "Surprise": "Expect the unexpected. Stay alert and adaptable."
        }
        
        base_advice = advice_map.get(door_name, "Assess the situation carefully before acting.")
        
        if score >= 7:
            return f"{base_advice} Energy strongly supports your goals."
        elif score >= 5:
            return f"{base_advice}"
        else:
            return f"{base_advice} Consider waiting for more favorable conditions."


# ============================================================================
# MAIN INTERFACE FUNCTION
# ============================================================================

def generate_qmdj_reading(
    date: datetime,
    palace: int = 5,
    method: int = 1,
    timezone_offset: int = 8
) -> Dict:
    """
    Main function to generate a complete QMDJ reading.
    
    Args:
        date: datetime object for the reading
        palace: Palace number (1-9) to analyze
        method: 1 = Chai Bu, 2 = Zhi Run
        timezone_offset: Hours offset from UTC (default 8 for Singapore)
    
    Returns:
        Complete processed chart data ready for display and export
    """
    engine = QMDJEngine()
    
    # Get raw chart
    raw_chart = engine.get_chart(
        year=date.year,
        month=date.month,
        day=date.day,
        hour=date.hour,
        minute=date.minute,
        method=method
    )
    
    # Process for selected palace
    processor = ChartProcessor(raw_chart, palace)
    result = processor.get_full_palace_data()
    
    # Add date/time metadata
    result["metadata"]["date"] = date.strftime("%Y-%m-%d")
    result["metadata"]["time"] = date.strftime("%H:%M")
    
    # Add Chinese hour if not already set
    if not result["metadata"]["chinese_hour"]:
        ch_char, ch_pinyin, ch_animal = get_chinese_hour(date.hour)
        result["metadata"]["chinese_hour"] = f"{ch_char}時 ({ch_pinyin} - {ch_animal})"
    
    return result


def get_all_palaces_summary(date: datetime, method: int = 1) -> List[Dict]:
    """
    Get summary of all 9 palaces for overview/recommendation.
    
    Returns list of palace summaries sorted by score (best first).
    """
    engine = QMDJEngine()
    raw_chart = engine.get_chart(
        year=date.year,
        month=date.month,
        day=date.day,
        hour=date.hour,
        minute=date.minute,
        method=method
    )
    
    summaries = []
    for palace_num in range(1, 10):
        processor = ChartProcessor(raw_chart, palace_num)
        data = processor.get_full_palace_data()
        
        summaries.append({
            "palace": palace_num,
            "name": data["palace"]["name"],
            "topic": data["palace"]["topic"],
            "icon": data["palace"]["icon"],
            "score": data["scores"]["normalized"],
            "verdict": data["scores"]["verdict"],
            "door": data["components"]["door"]["friendly_name"],
            "star": data["components"]["star"]["name"]
        })
    
    # Sort by score descending
    summaries.sort(key=lambda x: x["score"], reverse=True)
    return summaries


# ============================================================================
# TEST
# ============================================================================

if __name__ == "__main__":
    # Test the engine
    now = datetime.now(SGT)
    print(f"Testing QMDJ Engine for: {now}")
    print("=" * 60)
    
    reading = generate_qmdj_reading(now, palace=5)
    print(json.dumps(reading, indent=2, ensure_ascii=False, default=str))
    
    print("\n" + "=" * 60)
    print("All Palaces Summary:")
    summaries = get_all_palaces_summary(now)
    for s in summaries:
        print(f"  {s['icon']} Palace {s['palace']} ({s['topic']}): {s['score']}/10 - {s['verdict']}")
