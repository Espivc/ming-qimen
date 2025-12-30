"""
Ming Qimen - Export Center
Version: 4.0
Universal Schema v2.0 - Full BaZi Integration
Streamlined: BaZi profile shown only in sidebar
"""

import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="Export Center", page_icon="📤", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .export-title { color: #FFD700; font-size: 2.5rem; font-weight: bold; }
    .schema-badge {
        background: linear-gradient(90deg, #9B59B6, #3498DB);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        display: inline-block;
        margin-bottom: 1rem;
    }
    .json-preview {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Monaco', 'Menlo', monospace;
        font-size: 0.85rem;
        max-height: 500px;
        overflow-y: auto;
    }
    .export-card {
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
        font-size: 0.8rem;
        margin: 0.1rem;
    }
    .wood { background: #228B22; color: white; }
    .fire { background: #DC143C; color: white; }
    .earth { background: #DAA520; color: black; }
    .metal { background: #C0C0C0; color: black; }
    .water { background: #4169E1; color: white; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="export-title">📤 Export Center | 导出中心</p>', unsafe_allow_html=True)
st.markdown('<span class="schema-badge">Universal Schema v2.0 - Full BaZi Integration</span>', unsafe_allow_html=True)

st.divider()

# ============================================================
# MAIN CONTENT - TABS
# ============================================================

tab1, tab2 = st.tabs(["📊 Current Reading", "❓ How to Use"])

with tab1:
    # Check if we have a current chart
    current_chart = st.session_state.get("current_chart")
    user_profile = st.session_state.get("user_profile")
    
    if current_chart:
        st.success("✅ Chart data available for export")
        
        # Build full export data
        export_data = {
            "schema_version": "2.0",
            "schema_name": "QMDJ_BaZi_Integrated_Data_Schema",
            "metadata": {
                "date_time": current_chart.get("datetime", datetime.now().strftime("%Y-%m-%d %H:%M")),
                "timezone": "UTC+8",
                "method": "Chai Bu",
                "purpose": current_chart.get("purpose", "Forecasting"),
                "analysis_type": "QMDJ_BAZI_INTEGRATED" if user_profile else "QMDJ_ONLY",
                "exported_at": datetime.now().isoformat()
            },
            "qmdj_data": current_chart.get("qmdj_data", {}),
        }
        
        # Add BaZi data if profile exists
        if user_profile:
            export_data["bazi_data"] = {
                "chart_source": "User Profile",
                "day_master": {
                    "stem": user_profile.get("day_master", ""),
                    "element": user_profile.get("element", ""),
                    "polarity": user_profile.get("polarity", ""),
                    "strength": user_profile.get("strength", ""),
                    "strength_score": user_profile.get("strength_score", 5)
                },
                "useful_gods": {
                    "primary": user_profile.get("useful_gods", [""])[0] if user_profile.get("useful_gods") else "",
                    "secondary": user_profile.get("useful_gods", ["", ""])[1] if len(user_profile.get("useful_gods", [])) > 1 else ""
                },
                "unfavorable_elements": {
                    "primary": user_profile.get("unfavorable", [""])[0] if user_profile.get("unfavorable") else ""
                },
                "special_structures": {
                    "wealth_vault": user_profile.get("wealth_vault", False),
                    "nobleman_present": user_profile.get("nobleman", False)
                }
            }
        else:
            export_data["bazi_data"] = None
        
        # Synthesis placeholder
        export_data["synthesis"] = {
            "qmdj_score": current_chart.get("qmdj_score", 5),
            "bazi_alignment_score": current_chart.get("bazi_score", 5) if user_profile else None,
            "combined_verdict_score": current_chart.get("combined_score", 5),
            "verdict": current_chart.get("verdict", "NEUTRAL"),
            "confidence": "MEDIUM",
            "primary_action": current_chart.get("recommendation", "Assess situation before acting")
        }
        
        # Tracking
        export_data["tracking"] = {
            "db_row": f"{export_data['metadata']['date_time']},{current_chart.get('palace_number', 5)},{current_chart.get('formation', 'Unknown')},{export_data['synthesis']['qmdj_score']},{export_data['synthesis'].get('bazi_alignment_score', 'N/A')},{export_data['synthesis']['verdict']},PENDING",
            "outcome_status": "PENDING",
            "outcome_notes": "",
            "feedback_date": ""
        }
        
        # Preview
        st.subheader("📋 Export Preview")
        
        json_str = json.dumps(export_data, indent=2, ensure_ascii=False)
        st.markdown(f'<div class="json-preview"><pre>{json_str}</pre></div>', unsafe_allow_html=True)
        
        # Export buttons
        st.markdown("")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                label="📥 Download JSON",
                data=json_str,
                file_name=f"qmdj_export_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                type="primary",
                use_container_width=True
            )
        
        with col2:
            # Copy to clipboard (via text area)
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                st.code(json_str, language="json")
                st.info("Select all and copy the JSON above")
        
        with col3:
            # CSV export for ML database
            csv_row = export_data["tracking"]["db_row"]
            st.download_button(
                label="📊 Download CSV Row",
                data=f"Date,Time,Palace,Formation,QMDJ_Score,BaZi_Score,Verdict,Status\n{csv_row}",
                file_name=f"qmdj_row_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # BaZi status indicator
        st.markdown("---")
        if user_profile:
            st.success(f"✅ BaZi data included: {user_profile.get('day_master', 'Unknown')} ({user_profile.get('strength', 'Unknown')} {user_profile.get('element', '')})")
        else:
            st.warning("⚠️ No BaZi profile. Export will be QMDJ-only.")
            if st.button("🔮 Set Up BaZi Profile", use_container_width=True):
                st.switch_page("pages/6_BaZi.py")
    
    else:
        st.info("📊 No chart data to export yet.")
        st.markdown("Generate a QMDJ chart first to create exportable data.")
        
        if st.button("📊 Go to Chart Generator", type="primary", use_container_width=True):
            st.switch_page("pages/1_Chart.py")
        
        st.markdown("---")
        
        # Show BaZi status
        if user_profile:
            st.success(f"✅ BaZi profile ready: {user_profile.get('day_master', 'Unknown')}")
        else:
            st.warning("⚠️ No BaZi profile set. Exports will be QMDJ-only.")
            if st.button("🔮 Set Up BaZi Profile"):
                st.switch_page("pages/6_BaZi.py")

with tab2:
    st.subheader("❓ How to Use Export Data")
    
    st.markdown("""
    ### Universal Schema v2.0
    
    The export follows the **Universal Data Schema v2.0** format designed for:
    
    1. **AI Analysis** - Feed JSON to Claude or other LLMs for interpretation
    2. **ML Training** - CSV rows build your pattern database
    3. **Cross-Reference** - QMDJ + BaZi data in one package
    
    ### Data Sections
    
    | Section | Contents |
    |---------|----------|
    | `metadata` | Date, time, method, analysis type |
    | `qmdj_data` | Palace, components, formations |
    | `bazi_data` | Day Master, useful gods, structures |
    | `synthesis` | Scores (1-10), verdict, action |
    | `tracking` | CSV row, outcome status |
    
    ### Workflow
    
    1. **Generate Chart** → Create QMDJ reading
    2. **Export JSON** → Download or copy data
    3. **Analyze** → Send to Analyst Engine (Claude)
    4. **Track** → Record outcome in History
    """)
    
    st.markdown("---")
    
    st.markdown("### Example JSON Structure")
    
    example = {
        "schema_version": "2.0",
        "metadata": {
            "date_time": "2024-12-30 14:30",
            "analysis_type": "QMDJ_BAZI_INTEGRATED"
        },
        "qmdj_data": {
            "palace_analyzed": {"name": "Qian", "number": 6},
            "components": {"door": "Open", "star": "Heart"}
        },
        "bazi_data": {
            "day_master": {"stem": "Geng 庚", "strength": "Weak"}
        },
        "synthesis": {
            "qmdj_score": 7,
            "bazi_alignment_score": 8,
            "verdict": "AUSPICIOUS"
        }
    }
    
    st.json(example)

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
        if st.button("🔮 Set Up BaZi", key="sidebar_bazi"):
            st.switch_page("pages/6_BaZi.py")

# Footer
st.markdown("---")
st.caption("🌟 Ming Qimen 明奇门 | Export Center v4.0")
