"""
Ming Qimen 明奇门 - Export Page v2.1
Phase 4: Integrated with real QMDJ engine
"""

import streamlit as st
from datetime import datetime, timedelta, timezone
import json
import csv
import io
import sys
import os

# Add core module to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.qmdj_engine import (
    calculate_strength,
    strength_to_friendly,
    STEMS,
    PALACE_INFO,
    PALACE_TOPICS,
    STAR_MAPPING,
    DOOR_MAPPING,
    DEITY_MAPPING,
    ELEMENT_PRODUCES,
    ELEMENT_CONTROLS
)

st.set_page_config(
    page_title="Export | Ming Qimen",
    page_icon="📤",
    layout="wide"
)

# Singapore timezone
SGT = timezone(timedelta(hours=8))

def get_singapore_time():
    return datetime.now(SGT)


def convert_to_universal_schema(chart):
    """
    Convert Ming Qimen chart to Universal Schema v2.0
    Full alignment with Universal_Data_Schema_v2.json spec
    """
    user_profile = st.session_state.get('user_profile', {})
    
    # Extract data from chart
    palace = chart.get('palace', {})
    meta = chart.get('metadata', {})
    comp = chart.get('components', {})
    scores = chart.get('scores', {})
    guidance = chart.get('guidance', {})
    
    # Build Universal Schema
    universal = {
        "schema_version": "2.0",
        "schema_name": "QMDJ_BaZi_Integrated_Data_Schema",
        
        "metadata": {
            "date_time": f"{meta.get('date', '')} {meta.get('time', '')}".strip(),
            "timezone": "SGT (UTC+8)",
            "method": meta.get('method', 'Chai Bu'),
            "purpose": palace.get('topic', 'Forecasting'),
            "analysis_type": "QMDJ_BAZI_INTEGRATED" if user_profile else "QMDJ_ONLY",
            "generated_by": "Ming Qimen 明奇门 v2.0",
            "chinese_hour": meta.get('chinese_hour', '')
        },
        
        "qmdj_data": {
            "chart_type": "Hour",
            "structure": meta.get('structure', ''),
            "ju_number": meta.get('ju_number', 0),
            
            "palace_analyzed": {
                "name": palace.get('name', ''),
                "number": palace.get('number', 0),
                "direction": palace.get('direction', ''),
                "palace_element": palace.get('element', ''),
                "topic": palace.get('topic', '')
            },
            
            "components": {
                "heaven_stem": {
                    "character": comp.get('heaven_stem', {}).get('character', ''),
                    "element": comp.get('heaven_stem', {}).get('element', 'Unknown'),
                    "polarity": comp.get('heaven_stem', {}).get('polarity', 'Unknown'),
                    "strength_in_palace": comp.get('heaven_stem', {}).get('strength_in_palace', 'Unknown'),
                    "strength_score": comp.get('heaven_stem', {}).get('strength_score', 0)
                },
                "earth_stem": {
                    "character": comp.get('earth_stem', {}).get('character', ''),
                    "element": comp.get('earth_stem', {}).get('element', 'Unknown'),
                    "polarity": comp.get('earth_stem', {}).get('polarity', 'Unknown'),
                    "strength_in_palace": comp.get('earth_stem', {}).get('strength_in_palace', 'Unknown'),
                    "strength_score": comp.get('earth_stem', {}).get('strength_score', 0)
                },
                "door": {
                    "name": comp.get('door', {}).get('name', ''),
                    "chinese": comp.get('door', {}).get('chinese', ''),
                    "element": comp.get('door', {}).get('element', 'Unknown'),
                    "category": comp.get('door', {}).get('nature', 'Unknown'),
                    "strength_in_palace": comp.get('door', {}).get('strength_in_palace', 'Unknown'),
                    "strength_score": comp.get('door', {}).get('strength_score', 0)
                },
                "star": {
                    "name": comp.get('star', {}).get('name', ''),
                    "chinese": comp.get('star', {}).get('chinese', ''),
                    "element": comp.get('star', {}).get('element', 'Unknown'),
                    "category": comp.get('star', {}).get('nature', 'Unknown'),
                    "strength_in_palace": comp.get('star', {}).get('strength_in_palace', 'Unknown'),
                    "strength_score": comp.get('star', {}).get('strength_score', 0)
                },
                "deity": {
                    "name": comp.get('deity', {}).get('name', ''),
                    "chinese": comp.get('deity', {}).get('chinese', ''),
                    "nature": comp.get('deity', {}).get('nature', 'Unknown'),
                    "function": comp.get('deity', {}).get('function', '')
                }
            },
            
            "formation": {
                "primary_formation": {
                    "name": "Not Identified",
                    "category": "Unknown",
                    "source_book": "",
                    "outcome_pattern": ""
                },
                "secondary_formations": []
            }
        },
        
        "bazi_data": {
            "chart_source": "User Profile" if user_profile else "Not Provided",
            "day_master": {
                "stem": user_profile.get('day_master', 'Unknown'),
                "element": user_profile.get('element', 'Unknown'),
                "polarity": user_profile.get('polarity', 'Unknown'),
                "strength": user_profile.get('strength', 'Unknown'),
                "strength_score": user_profile.get('strength_score', 5)
            },
            "useful_gods": {
                "primary": user_profile.get('useful_gods', ['Unknown'])[0] if user_profile.get('useful_gods') else 'Unknown',
                "secondary": user_profile.get('useful_gods', ['Unknown', 'Unknown'])[1] if len(user_profile.get('useful_gods', [])) > 1 else 'Unknown',
                "reasoning": user_profile.get('useful_gods_reasoning', '')
            },
            "unfavorable_elements": {
                "primary": user_profile.get('unfavorable', ['Unknown'])[0] if user_profile.get('unfavorable') else 'Unknown',
                "reasoning": user_profile.get('unfavorable_reasoning', '')
            },
            "ten_god_profile": {
                "dominant_god": user_profile.get('dominant_god', 'Unknown'),
                "profile_name": user_profile.get('profile', 'Unknown'),
                "behavioral_traits": user_profile.get('traits', [])
            },
            "special_structures": {
                "wealth_vault": user_profile.get('wealth_vault', False),
                "nobleman_present": user_profile.get('nobleman', False),
                "other_structures": user_profile.get('structures', [])
            }
        },
        
        "synthesis": {
            "qmdj_score": {
                "component_total": scores.get('component_total', 0),
                "formation_modifier": 0,
                "final_qmdj_score": scores.get('normalized', 5)
            },
            "bazi_alignment_score": {
                "useful_god_activation": 0,
                "dm_support": 0,
                "profile_alignment": 0,
                "clash_penalty": 0,
                "final_bazi_score": 5,
                "reasoning": ""
            },
            "combined_verdict_score": scores.get('normalized', 5),
            "verdict": scores.get('verdict', 'Neutral'),
            "confidence": "HIGH" if scores.get('normalized', 5) >= 7 or scores.get('normalized', 5) <= 3 else "MEDIUM",
            "primary_action": guidance.get('advice', ''),
            "summary": guidance.get('summary', ''),
            "timing_recommendation": {
                "optimal_hour": "",
                "avoid_hour": "",
                "source": "#72"
            }
        },
        
        "tracking": {
            "generated_at": get_singapore_time().isoformat(),
            "outcome_status": "PENDING",
            "outcome_notes": "",
            "feedback_date": ""
        }
    }
    
    return universal


def generate_db_row(chart, universal):
    """Generate single-line CSV for ML tracking"""
    meta = chart.get('metadata', {})
    palace = chart.get('palace', {})
    synthesis = universal.get('synthesis', {})
    
    primary_action = synthesis.get('primary_action', '').replace('"', "'")
    
    row = (
        f"{meta.get('date', '')},"
        f"{meta.get('time', '')},"
        f"{palace.get('name', '')},"
        f"N/A,"
        f"{synthesis.get('qmdj_score', {}).get('final_qmdj_score', 'N/A')},"
        f"{synthesis.get('bazi_alignment_score', {}).get('final_bazi_score', 'N/A')},"
        f"{synthesis.get('verdict', '')},"
        f'"{primary_action}",'
        f"PENDING"
    )
    return row


# Load CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

# ============================================================================
# PAGE CONTENT
# ============================================================================

st.title("📤 Export 导出")
st.markdown("Export your readings for Project 1 (AI Analyst) integration")

# Initialize
if 'export_history' not in st.session_state:
    st.session_state.export_history = []

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Current Reading", "📚 History Export", "❓ How to Use"])

# ============================================================================
# TAB 1: CURRENT CHART
# ============================================================================

with tab1:
    st.markdown("### 📊 Current Reading Data")
    
    if 'current_chart' in st.session_state and st.session_state.current_chart:
        chart = st.session_state.current_chart
        
        # Display summary
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Reading Summary")
            palace = chart.get('palace', {})
            meta = chart.get('metadata', {})
            
            st.markdown(f"**Topic:** {palace.get('icon', '')} {palace.get('topic', 'N/A')}")
            st.markdown(f"**Palace:** #{palace.get('number', 'N/A')} {palace.get('name', '')}")
            st.markdown(f"**Direction:** {palace.get('direction', 'N/A')}")
            st.markdown(f"**Element:** {palace.get('element', 'N/A')}")
            st.markdown(f"**Date:** {meta.get('date', 'N/A')}")
            st.markdown(f"**Time:** {meta.get('time', 'N/A')} (SGT)")
            st.markdown(f"**Chinese Hour:** {meta.get('chinese_hour', 'N/A')}")
        
        with col2:
            st.markdown("#### Guidance")
            guidance = chart.get('guidance', {})
            scores = chart.get('scores', {})
            
            if scores.get('verdict_type') == 'success':
                st.success(f"**{scores.get('verdict', 'N/A')}** ({scores.get('normalized', 'N/A')}/10)")
            elif scores.get('verdict_type') == 'warning':
                st.warning(f"**{scores.get('verdict', 'N/A')}** ({scores.get('normalized', 'N/A')}/10)")
            else:
                st.info(f"**{scores.get('verdict', 'N/A')}** ({scores.get('normalized', 'N/A')}/10)")
            
            st.markdown(f"*{guidance.get('summary', '')}*")
            st.markdown(f"💡 {guidance.get('advice', '')}")
        
        st.markdown("---")
        
        # Components
        st.markdown("#### Components & Strength")
        
        comp = chart.get('components', {})
        comp_cols = st.columns(5)
        
        with comp_cols[0]:
            hs = comp.get('heaven_stem', {})
            st.markdown("**Heaven Stem**")
            st.markdown(f"{hs.get('character', '?')}")
            st.caption(f"{hs.get('element', '?')} | {hs.get('strength_in_palace', '?')}")
            st.caption(f"Score: {hs.get('strength_score', 0):+d}")
        
        with comp_cols[1]:
            es = comp.get('earth_stem', {})
            st.markdown("**Earth Stem**")
            st.markdown(f"{es.get('character', '?')}")
            st.caption(f"{es.get('element', '?')} | {es.get('strength_in_palace', '?')}")
            st.caption(f"Score: {es.get('strength_score', 0):+d}")
        
        with comp_cols[2]:
            star = comp.get('star', {})
            st.markdown("**Star**")
            st.markdown(f"{star.get('chinese', '?')}")
            st.caption(f"{star.get('name', '?')} | {star.get('nature', '?')}")
            st.caption(f"Score: {star.get('strength_score', 0):+d}")
        
        with comp_cols[3]:
            door = comp.get('door', {})
            st.markdown("**Door**")
            st.markdown(f"{door.get('chinese', '?')}")
            st.caption(f"{door.get('friendly_name', door.get('name', '?'))} | {door.get('nature', '?')}")
            st.caption(f"Score: {door.get('strength_score', 0):+d}")
        
        with comp_cols[4]:
            deity = comp.get('deity', {})
            st.markdown("**Spirit**")
            st.markdown(f"{deity.get('chinese', '?')}")
            st.caption(f"{deity.get('name', '?')} | {deity.get('nature', '?')}")
        
        st.markdown("---")
        
        # Export section
        st.markdown("### 🚀 Export for Project 1")
        
        universal = convert_to_universal_schema(chart)
        universal_json = json.dumps(universal, indent=2, ensure_ascii=False, default=str)
        
        # Score summary
        synthesis = universal.get('synthesis', {})
        score_cols = st.columns(3)
        
        with score_cols[0]:
            st.metric("QMDJ Score", f"{synthesis.get('qmdj_score', {}).get('final_qmdj_score', 'N/A')}/10")
        
        with score_cols[1]:
            st.metric("Combined Score", f"{synthesis.get('combined_verdict_score', 'N/A')}/10")
        
        with score_cols[2]:
            st.metric("Verdict", synthesis.get('verdict', 'N/A'))
        
        st.markdown("---")
        
        # Copy section
        st.markdown("#### 📋 Copy to Clipboard")
        st.code(universal_json, language="json")
        
        # Download buttons
        st.markdown("#### 📥 Download Options")
        
        dl_cols = st.columns(3)
        
        with dl_cols[0]:
            st.download_button(
                "📥 Universal Schema (JSON)",
                data=universal_json,
                file_name=f"ming_qimen_{meta.get('date', 'reading').replace('-', '')}.json",
                mime="application/json",
                use_container_width=True,
                type="primary"
            )
        
        with dl_cols[1]:
            raw_json = json.dumps(chart, indent=2, ensure_ascii=False, default=str)
            st.download_button(
                "📥 Raw Chart (JSON)",
                data=raw_json,
                file_name=f"ming_qimen_raw_{meta.get('date', 'reading').replace('-', '')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with dl_cols[2]:
            db_row = generate_db_row(chart, universal)
            header = "Date,Time,Palace,Formation,QMDJ_Score,BaZi_Score,Verdict,Primary_Action,Outcome"
            st.download_button(
                "📥 Tracking Row (CSV)",
                data=f"{header}\n{db_row}",
                file_name=f"ming_qimen_tracking_{meta.get('date', 'reading').replace('-', '')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
    else:
        st.info("📭 No reading available. Generate a reading from the **Chart** page first.")
        
        if st.button("📊 Go to Chart", use_container_width=True):
            st.switch_page("pages/1_Chart.py")

# ============================================================================
# TAB 2: HISTORY
# ============================================================================

with tab2:
    st.markdown("### 📚 Export History")
    
    if 'analyses' in st.session_state and st.session_state.analyses:
        analyses = st.session_state.analyses
        st.markdown(f"**Total Readings:** {len(analyses)}")
        
        for i, analysis in enumerate(reversed(analyses[-10:])):
            with st.expander(f"📊 {analysis.get('date', 'N/A')} {analysis.get('time', '')} - {analysis.get('topic', 'N/A')}"):
                st.json(analysis)
        
        st.markdown("---")
        
        json_str = json.dumps(analyses, indent=2, ensure_ascii=False, default=str)
        st.download_button(
            "📥 Export All History (JSON)",
            data=json_str,
            file_name=f"ming_qimen_history_{get_singapore_time().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )
    else:
        st.info("📭 No history available yet.")

# ============================================================================
# TAB 3: HOW TO USE
# ============================================================================

with tab3:
    st.markdown("""
    ### ❓ How to Export to Project 1
    
    **Step 1:** Generate a reading on the Chart page
    
    **Step 2:** Come to this Export page
    
    **Step 3:** Copy the JSON from the code block (click the copy icon)
    
    **Step 4:** Paste into Project 1 (AI Analyst)
    
    ---
    
    #### What Gets Exported?
    
    | Section | Data |
    |---------|------|
    | Metadata | Date, time, method, Chinese hour |
    | QMDJ Data | Palace, components with strength scores |
    | BaZi Data | Day Master, useful gods (if configured) |
    | Synthesis | QMDJ score, verdict, guidance |
    | Tracking | Timestamps for ML feedback loop |
    
    ---
    
    #### Pro Tips
    
    - Configure your BaZi profile in Settings for integrated scoring
    - Use the Tracking CSV for building your ML dataset
    - History Export lets you batch export all readings
    """)

# Footer
st.markdown("---")
st.caption("🌟 Ming Qimen 明奇门 | Export v2.1 | Singapore Time (UTC+8)")
