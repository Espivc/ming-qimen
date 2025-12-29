"""
Ming Qimen 明奇门 - History Page v2.0
"""

import streamlit as st
from datetime import datetime, timedelta, timezone
import json

st.set_page_config(
    page_title="History | Ming Qimen",
    page_icon="📜",
    layout="wide"
)

SGT = timezone(timedelta(hours=8))

def get_singapore_time():
    return datetime.now(SGT)

# Load CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

st.title("📜 History 历史")
st.markdown("View your past readings")

if 'analyses' not in st.session_state:
    st.session_state.analyses = []

if st.session_state.analyses:
    analyses = st.session_state.analyses
    
    st.markdown(f"### Total Readings: {len(analyses)}")
    
    # Summary stats
    col1, col2, col3 = st.columns(3)
    
    scores = [a.get('score', 5) for a in analyses if a.get('score')]
    
    with col1:
        if scores:
            avg_score = sum(scores) / len(scores)
            st.metric("Average Score", f"{avg_score:.1f}/10")
    
    with col2:
        favorable = len([s for s in scores if s >= 6])
        st.metric("Favorable Readings", f"{favorable}/{len(scores)}")
    
    with col3:
        topics = [a.get('topic', 'Unknown') for a in analyses]
        most_common = max(set(topics), key=topics.count) if topics else "N/A"
        st.metric("Most Queried Topic", most_common)
    
    st.markdown("---")
    
    # History list
    st.markdown("### Recent Readings")
    
    for i, analysis in enumerate(reversed(analyses)):
        score = analysis.get('score', 5)
        
        if score >= 6:
            icon = "✅"
        elif score >= 4:
            icon = "😐"
        else:
            icon = "⚠️"
        
        with st.expander(f"{icon} {analysis.get('date', 'N/A')} {analysis.get('time', '')} - {analysis.get('topic', 'Unknown')} ({score}/10)"):
            st.markdown(f"**Palace:** {analysis.get('palace', 'N/A')}")
            st.markdown(f"**Door:** {analysis.get('door', 'N/A')}")
            st.markdown(f"**Star:** {analysis.get('star', 'N/A')}")
            st.markdown(f"**Verdict:** {analysis.get('verdict', 'N/A')}")
            
            st.markdown("---")
            st.json(analysis)
    
    st.markdown("---")
    
    # Actions
    col1, col2 = st.columns(2)
    
    with col1:
        json_str = json.dumps(analyses, indent=2, ensure_ascii=False, default=str)
        st.download_button(
            "📥 Export History (JSON)",
            data=json_str,
            file_name=f"ming_qimen_history_{get_singapore_time().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.analyses = []
            st.rerun()

else:
    st.info("📭 No readings yet. Generate your first reading from the Chart page!")
    
    if st.button("📊 Go to Chart", use_container_width=True):
        st.switch_page("pages/1_Chart.py")

st.markdown("---")
st.caption("🌟 Ming Qimen 明奇门 | History v2.0")
