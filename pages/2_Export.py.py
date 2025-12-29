"""
Enhanced Export Page - Universal Schema v2.0
=============================================
Complete BaZi integration for Ming Qimen Project 2
"""

import streamlit as st
from datetime import datetime, timezone, timedelta
import json
from typing import Dict, List

st.set_page_config(page_title="Export | 导出", page_icon="📤", layout="wide")

# Singapore timezone
SGT = timezone(timedelta(hours=8))

# Element relationships
ELEMENT_PRODUCES = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal", "Metal": "Water", "Water": "Wood"}
ELEMENT_PRODUCED_BY = {"Wood": "Water", "Fire": "Wood", "Earth": "Fire", "Metal": "Earth", "Water": "Metal"}
ELEMENT_CONTROLLED_BY = {"Wood": "Metal", "Fire": "Water", "Earth": "Wood", "Metal": "Fire", "Water": "Earth"}

def calculate_bazi_alignment_score(bazi_data: Dict, qmdj_components: Dict) -> Dict:
    """Calculate BaZi alignment score based on QMDJ components"""
    score = 5.0
    breakdown = []
    
    useful_gods = bazi_data.get("useful_gods", {})
    primary_ug = useful_gods.get("primary", "")
    secondary_ug = useful_gods.get("secondary", "")
    unfavorable = useful_gods.get("unfavorable", [])
    if isinstance(unfavorable, str):
        unfavorable = [unfavorable]
    
    weights = {"heaven_stem": 1.5, "earth_stem": 1.0, "door": 1.5, "star": 1.0, "deity": 0.5}
    
    for component, element in qmdj_components.items():
        if not element:
            continue
        weight = weights.get(component, 1.0)
        
        if element == primary_ug:
            score += weight
            breakdown.append({"component": component, "element": element, "status": "Primary UG", "modifier": f"+{weight}"})
        elif element == secondary_ug:
            score += weight * 0.7
            breakdown.append({"component": component, "element": element, "status": "Secondary UG", "modifier": f"+{round(weight*0.7,1)}"})
        elif element in unfavorable:
            score -= weight
            breakdown.append({"component": component, "element": element, "status": "Unfavorable", "modifier": f"-{weight}"})
        else:
            breakdown.append({"component": component, "element": element, "status": "Neutral", "modifier": "0"})
    
    special = bazi_data.get("special_structures", {})
    if special.get("wealth_vault"):
        score += 0.5
        breakdown.append({"component": "wealth_vault", "element": "-", "status": "Bonus", "modifier": "+0.5"})
    if special.get("nobleman_present"):
        score += 0.5
        breakdown.append({"component": "nobleman", "element": "-", "status": "Bonus", "modifier": "+0.5"})
    
    final_score = round(max(0, min(10, score)), 1)
    
    if final_score >= 8: verdict = "Excellent Alignment"
    elif final_score >= 6: verdict = "Good Alignment"
    elif final_score >= 4: verdict = "Mixed Alignment"
    elif final_score >= 2: verdict = "Poor Alignment"
    else: verdict = "Conflicting Alignment"
    
    return {"base_score": 5.0, "final_score": final_score, "verdict": verdict, "breakdown": breakdown}

def get_strength_score(strength: str) -> int:
    return {"Timely": 2, "Prosperous": 3, "Resting": 0, "Confined": -2, "Dead": -3}.get(strength, 0)

def get_verdict(score: float) -> str:
    if score >= 8: return "Highly Auspicious"
    elif score >= 6: return "Auspicious"
    elif score >= 4: return "Neutral"
    elif score >= 2: return "Challenging"
    else: return "Very Challenging"

def convert_to_universal_schema_v2(chart_data: Dict, bazi_data: Dict = None) -> Dict:
    """Convert to Universal Schema v2.0 with full BaZi integration"""
    now = datetime.now(SGT)
    
    components = chart_data.get("components", {})
    palace = chart_data.get("palace", {})
    metadata = chart_data.get("metadata", {})
    
    heaven_stem = components.get("heaven_stem", {})
    earth_stem = components.get("earth_stem", {})
    door = components.get("door", {})
    star = components.get("star", {})
    deity = components.get("deity", {})
    
    qmdj_elements = {
        "heaven_stem": heaven_stem.get("element", ""),
        "earth_stem": earth_stem.get("element", ""),
        "door": door.get("element", ""),
        "star": star.get("element", ""),
        "deity": deity.get("element", "Earth")
    }
    
    component_total = sum([
        get_strength_score(heaven_stem.get("strength_in_palace", "")),
        get_strength_score(earth_stem.get("strength_in_palace", "")),
        get_strength_score(door.get("strength_in_palace", "")),
        get_strength_score(star.get("strength_in_palace", ""))
    ])
    
    qmdj_score = round(max(0, min(10, (component_total + 12) / 2.4)), 1)
    
    bazi_alignment = None
    if bazi_data and bazi_data.get("useful_gods"):
        bazi_alignment = calculate_bazi_alignment_score(bazi_data, qmdj_elements)
    
    bazi_score = bazi_alignment.get("final_score", 5) if bazi_alignment else 5
    
    return {
        "schema_version": "2.0",
        "schema_name": "QMDJ_BaZi_Integrated_Data_Schema",
        "metadata": {
            "date_time": metadata.get("date", now.strftime("%Y-%m-%d")) + " " + metadata.get("time", now.strftime("%H:%M")),
            "timezone": "SGT (UTC+8)",
            "method": metadata.get("method", "拆補"),
            "purpose": metadata.get("purpose", "Self"),
            "analysis_type": "QMDJ_BAZI_INTEGRATED" if bazi_data else "QMDJ_ONLY",
            "generated_by": "Ming Qimen 明奇门 v2.0",
            "chinese_hour": metadata.get("chinese_hour", "")
        },
        "qmdj_data": {
            "chart_type": chart_data.get("chart_type", "Hour"),
            "structure": chart_data.get("structure", ""),
            "ju_number": chart_data.get("ju_number", 0),
            "palace_analyzed": {
                "name": palace.get("name", ""),
                "number": palace.get("number", 5),
                "direction": palace.get("direction", ""),
                "palace_element": palace.get("element", ""),
                "topic": palace.get("topic", "Self")
            },
            "components": {
                "heaven_stem": {
                    "character": heaven_stem.get("character", ""),
                    "element": heaven_stem.get("element", ""),
                    "polarity": heaven_stem.get("polarity", ""),
                    "strength_in_palace": heaven_stem.get("strength_in_palace", ""),
                    "strength_score": get_strength_score(heaven_stem.get("strength_in_palace", ""))
                },
                "earth_stem": {
                    "character": earth_stem.get("character", ""),
                    "element": earth_stem.get("element", ""),
                    "polarity": earth_stem.get("polarity", ""),
                    "strength_in_palace": earth_stem.get("strength_in_palace", ""),
                    "strength_score": get_strength_score(earth_stem.get("strength_in_palace", ""))
                },
                "door": {
                    "name": door.get("name", ""),
                    "chinese": door.get("chinese", ""),
                    "element": door.get("element", ""),
                    "category": door.get("category", ""),
                    "strength_in_palace": door.get("strength_in_palace", ""),
                    "strength_score": get_strength_score(door.get("strength_in_palace", ""))
                },
                "star": {
                    "name": star.get("name", ""),
                    "chinese": star.get("chinese", ""),
                    "element": star.get("element", ""),
                    "category": star.get("category", ""),
                    "strength_in_palace": star.get("strength_in_palace", ""),
                    "strength_score": get_strength_score(star.get("strength_in_palace", ""))
                },
                "deity": {
                    "name": deity.get("name", ""),
                    "chinese": deity.get("chinese", ""),
                    "nature": deity.get("nature", ""),
                    "function": deity.get("function", "")
                }
            },
            "formation": {
                "primary_formation": {
                    "name": chart_data.get("formation", {}).get("name", "Not Identified"),
                    "category": chart_data.get("formation", {}).get("category", "Unknown"),
                    "source_book": "",
                    "outcome_pattern": ""
                },
                "secondary_formations": []
            }
        },
        "bazi_data": {
            "chart_source": bazi_data.get("chart_source", "User Profile") if bazi_data else "Not Provided",
            "day_master": bazi_data.get("day_master", {}) if bazi_data else {},
            "four_pillars": bazi_data.get("four_pillars", "Not calculated") if bazi_data else "Not calculated",
            "ten_gods_mapping": bazi_data.get("ten_gods_mapping", {}) if bazi_data else {},
            "useful_gods": bazi_data.get("useful_gods", {"primary": "", "secondary": "", "unfavorable": [], "reasoning": ""}) if bazi_data else {},
            "useful_god_activation": bazi_data.get("useful_god_activation", {}) if bazi_data else {},
            "ten_god_profile": bazi_data.get("ten_god_profile", {"dominant_god": "", "profile_name": "", "behavioral_traits": []}) if bazi_data else {},
            "special_structures": bazi_data.get("special_structures", {"wealth_vault": False, "nobleman_present": False}) if bazi_data else {}
        },
        "synthesis": {
            "qmdj_score": {"component_total": component_total, "formation_modifier": 0, "final_qmdj_score": qmdj_score},
            "bazi_alignment_score": {
                "useful_god_activation": bazi_score,
                "final_bazi_score": bazi_score,
                "breakdown": bazi_alignment.get("breakdown", []) if bazi_alignment else [],
                "reasoning": bazi_alignment.get("verdict", "") if bazi_alignment else ""
            },
            "combined_verdict_score": round((qmdj_score + bazi_score) / 2, 1),
            "verdict": get_verdict(qmdj_score),
            "confidence": "HIGH" if abs(qmdj_score - 5) > 2 else "MEDIUM",
            "primary_action": f"Based on {door.get('name', 'Unknown')} Door analysis.",
            "summary": f"Chart analysis complete. QMDJ: {qmdj_score}/10, BaZi: {bazi_score}/10"
        },
        "tracking": {
            "generated_at": now.isoformat(),
            "outcome_status": "PENDING",
            "outcome_notes": "",
            "feedback_date": ""
        }
    }

# ============= MAIN UI =============
st.title("📤 Export Center | 导出中心")
st.markdown("**Universal Schema v2.0 - Full BaZi Integration**")
st.markdown("---")

chart_data = st.session_state.get("current_chart", {})
bazi_data = st.session_state.get("bazi_data", {}) or st.session_state.get("user_bazi_profile", {})

tab1, tab2, tab3 = st.tabs(["📊 Current Reading", "🎴 BaZi Profile", "❓ How to Use"])

with tab1:
    if not chart_data:
        st.warning("⚠️ No QMDJ chart data. Generate a chart first.")
    else:
        universal_data = convert_to_universal_schema_v2(chart_data, bazi_data)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            score = universal_data["synthesis"]["combined_verdict_score"]
            color = "🟢" if score >= 6 else ("🟡" if score >= 4 else "🔴")
            st.metric("Combined Score", f"{color} {score}/10")
        with col2:
            st.metric("QMDJ Score", f"{universal_data['synthesis']['qmdj_score']['final_qmdj_score']}/10")
        with col3:
            st.metric("BaZi Alignment", f"{universal_data['synthesis']['bazi_alignment_score']['final_bazi_score']}/10")
        
        if bazi_data and universal_data["synthesis"]["bazi_alignment_score"]["breakdown"]:
            with st.expander("📊 Alignment Breakdown"):
                for item in universal_data["synthesis"]["bazi_alignment_score"]["breakdown"]:
                    status = item.get("status", "")
                    if "Primary" in status or "Bonus" in status:
                        st.success(f"✅ {item['component']}: {item['element']} ({item['modifier']})")
                    elif "Unfavorable" in status:
                        st.error(f"❌ {item['component']}: {item['element']} ({item['modifier']})")
        
        st.markdown("---")
        universal_json = json.dumps(universal_data, indent=2, ensure_ascii=False, default=str)
        st.code(universal_json, language="json")
        
        st.download_button("⬇️ Download JSON", universal_json, 
                          f"qmdj_bazi_{datetime.now().strftime('%Y%m%d_%H%M')}.json", "application/json")

with tab2:
    if not bazi_data:
        st.warning("⚠️ No BaZi profile. Use BaZi Calculator or Settings.")
    else:
        dm = bazi_data.get("day_master", {})
        st.metric("Day Master", f"{dm.get('stem_chinese', '')} {dm.get('element', '')} ({dm.get('strength', '')})")
        
        ug = bazi_data.get("useful_gods", {})
        st.success(f"✅ Primary: {ug.get('primary', 'N/A')}")
        st.info(f"📌 Secondary: {ug.get('secondary', 'N/A')}")
        
        if bazi_data.get("four_pillars") and bazi_data["four_pillars"] != "Not calculated":
            st.markdown("**Four Pillars:**")
            fp = bazi_data["four_pillars"]
            cols = st.columns(4)
            for i, pn in enumerate(["year", "month", "day", "hour"]):
                if pn in fp:
                    with cols[i]:
                        st.write(f"{pn.title()}: {fp[pn]['stem']['chinese']}{fp[pn]['branch']['chinese']}")

with tab3:
    st.markdown("""
    ### Workflow
    1. Generate QMDJ chart
    2. Calculate BaZi (or set in Settings)
    3. Export JSON here
    4. Paste in Project 1
    5. Say: **"Analyze and output as bilingual docx report"**
    
    ### Score Guide
    - **8-10**: Highly Auspicious
    - **6-7.9**: Auspicious  
    - **4-5.9**: Neutral
    - **2-3.9**: Challenging
    - **0-1.9**: Very Challenging
    """)
