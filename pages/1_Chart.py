"""
Ming Qimen 明奇门 - Chart Page v2.0
Phase 4: Real QMDJ calculations with kinqimen integration
"""

import streamlit as st
from datetime import datetime, timedelta, timezone, date, time
import sys
import os

# Add core module to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.qmdj_engine import (
    generate_qmdj_reading,
    get_all_palaces_summary,
    PALACE_INFO,
    PALACE_TOPICS,
    strength_to_friendly
)

st.set_page_config(
    page_title="Chart | Ming Qimen",
    page_icon="📊",
    layout="wide"
)

# Singapore timezone
SGT = timezone(timedelta(hours=8))

def get_singapore_time():
    return datetime.now(SGT)

# Load CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

# ============================================================================
# SESSION STATE
# ============================================================================

if 'current_chart' not in st.session_state:
    st.session_state.current_chart = None

if 'analyses' not in st.session_state:
    st.session_state.analyses = []

# Sync time from dashboard if available
if 'shared_date' not in st.session_state:
    st.session_state.shared_date = get_singapore_time().date()
    
if 'shared_time' not in st.session_state:
    st.session_state.shared_time = get_singapore_time().strftime("%H:%M")

if 'selected_palace' not in st.session_state:
    st.session_state.selected_palace = 5

# ============================================================================
# PAGE HEADER
# ============================================================================

st.title("📊 Chart 排盤")
st.markdown("*Generate your Qi Men Dun Jia reading*")

# ============================================================================
# INPUT SECTION
# ============================================================================

st.markdown("### 🕐 Select Date & Time")

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    input_date = st.date_input(
        "Date 日期",
        value=st.session_state.shared_date,
        help="Select the date for your reading"
    )
    st.session_state.shared_date = input_date

with col2:
    # Parse current time
    try:
        current_time_parts = st.session_state.shared_time.split(":")
        default_time = time(int(current_time_parts[0]), int(current_time_parts[1]))
    except:
        default_time = get_singapore_time().time()
    
    input_time = st.time_input(
        "Time 時間",
        value=default_time,
        help="Select the time for your reading (Singapore Time)"
    )
    st.session_state.shared_time = input_time.strftime("%H:%M")

with col3:
    if st.button("📍 Now", use_container_width=True, help="Set to current time"):
        now = get_singapore_time()
        st.session_state.shared_date = now.date()
        st.session_state.shared_time = now.strftime("%H:%M")
        st.rerun()

# Combine date and time
reading_datetime = datetime.combine(input_date, input_time)
reading_datetime = reading_datetime.replace(tzinfo=SGT)

st.markdown("---")

# ============================================================================
# TOPIC/PALACE SELECTION
# ============================================================================

st.markdown("### 🎯 Select Topic")
st.caption("Choose what you want guidance on")

# Topic grid
topic_cols = st.columns(3)
topic_options = list(PALACE_TOPICS.items())

selected_topic = st.session_state.selected_palace

for idx, (palace_num, info) in enumerate(topic_options):
    col_idx = idx % 3
    with topic_cols[col_idx]:
        is_selected = palace_num == selected_topic
        button_type = "primary" if is_selected else "secondary"
        
        if st.button(
            f"{info['icon']} {info['topic']}", 
            key=f"topic_{palace_num}",
            use_container_width=True,
            type=button_type
        ):
            st.session_state.selected_palace = palace_num
            selected_topic = palace_num
            st.rerun()

# Show selected topic description
if selected_topic:
    topic_info = PALACE_TOPICS[selected_topic]
    palace_info = PALACE_INFO[selected_topic]
    st.info(f"**{topic_info['icon']} {topic_info['topic']}** - {topic_info['description']} | Palace {selected_topic} ({palace_info['name']}) | {palace_info['direction']} | {palace_info['element']}")

st.markdown("---")

# ============================================================================
# GENERATE READING
# ============================================================================

st.markdown("### 📈 Generate Reading")

method_col, gen_col = st.columns([1, 2])

with method_col:
    method = st.radio(
        "Method 排盤法",
        options=[1, 2],
        format_func=lambda x: "拆補 Chai Bu" if x == 1 else "置閏 Zhi Run",
        help="Chai Bu is the most commonly used method"
    )

with gen_col:
    generate_clicked = st.button(
        "🔮 Get Your Reading",
        use_container_width=True,
        type="primary"
    )

# ============================================================================
# SHOW READING
# ============================================================================

if generate_clicked:
    with st.spinner("Calculating your Qi Men chart..."):
        reading = generate_qmdj_reading(
            date=reading_datetime,
            palace=selected_topic,
            method=method
        )
        st.session_state.current_chart = reading
        
        # Add to history
        history_entry = {
            "date": reading["metadata"]["date"],
            "time": reading["metadata"]["time"],
            "palace": reading["palace"]["number"],
            "topic": reading["palace"]["topic"],
            "score": reading["scores"]["normalized"],
            "verdict": reading["scores"]["verdict"],
            "door": reading["components"]["door"]["name"],
            "star": reading["components"]["star"]["name"]
        }
        st.session_state.analyses.append(history_entry)

# Display current chart
if st.session_state.current_chart:
    reading = st.session_state.current_chart
    
    st.markdown("---")
    st.markdown("## 📋 Your Reading")
    
    # Header info
    meta = reading["metadata"]
    palace = reading["palace"]
    
    header_cols = st.columns([2, 2, 1])
    
    with header_cols[0]:
        st.markdown(f"**{palace['icon']} {palace['topic']}** - Palace {palace['number']} ({palace['name']})")
        st.caption(f"{meta['date']} {meta['time']} SGT | {meta['chinese_hour']}")
    
    with header_cols[1]:
        st.markdown(f"**Structure:** {meta['structure']} Ju {meta['ju_number']}")
        st.caption(f"Method: {meta['method']} | {meta['solar_term']}")
    
    with header_cols[2]:
        scores = reading["scores"]
        if scores["verdict_type"] == "success":
            st.success(f"**{scores['normalized']}/10**")
        elif scores["verdict_type"] == "warning":
            st.warning(f"**{scores['normalized']}/10**")
        else:
            st.info(f"**{scores['normalized']}/10**")
        st.caption(scores["verdict"])
    
    st.markdown("---")
    
    # ============================================================================
    # 9-PALACE GRID
    # ============================================================================
    
    st.markdown("### 🏛️ Nine Palace Grid")
    
    # Build grid data
    raw_chart = reading.get("raw_chart", {})
    
    # Luo Shu arrangement: [4,9,2], [3,5,7], [8,1,6]
    grid_layout = [
        [4, 9, 2],
        [3, 5, 7],
        [8, 1, 6]
    ]
    
    for row in grid_layout:
        cols = st.columns(3)
        for col_idx, palace_num in enumerate(row):
            with cols[col_idx]:
                p_info = PALACE_INFO[palace_num]
                t_info = PALACE_TOPICS[palace_num]
                
                # Get palace components from raw chart
                palace_chinese = p_info["chinese"]
                sky = raw_chart.get("天盤", {}).get(palace_chinese, "?")
                earth = raw_chart.get("地盤", {}).get(palace_chinese, "?")
                star = raw_chart.get("星", {}).get(palace_chinese, "?")
                door = raw_chart.get("門", {}).get(palace_chinese, "?")
                deity = raw_chart.get("神", {}).get(palace_chinese, "?") if palace_chinese != "中" else "-"
                
                # Highlight selected palace
                is_selected = palace_num == selected_topic
                border_style = "border: 3px solid #FFD700;" if is_selected else "border: 1px solid #444;"
                bg_color = "background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);" if is_selected else "background: #1e1e1e;"
                
                st.markdown(f"""
                <div style="{bg_color} {border_style} border-radius: 10px; padding: 10px; margin: 5px 0; min-height: 180px;">
                    <div style="text-align: center; font-weight: bold; color: #FFD700; font-size: 0.9em;">
                        {t_info['icon']} {p_info['name']} ({palace_num})
                    </div>
                    <div style="text-align: center; color: #888; font-size: 0.7em; margin-bottom: 8px;">
                        {p_info['direction']} | {p_info['element']}
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 4px; font-size: 0.85em;">
                        <div style="text-align: center;">
                            <span style="color: #90CAF9;">天</span> <span style="color: #fff;">{sky}</span>
                        </div>
                        <div style="text-align: center;">
                            <span style="color: #A5D6A7;">神</span> <span style="color: #fff;">{deity}</span>
                        </div>
                        <div style="text-align: center;">
                            <span style="color: #FFCC80;">星</span> <span style="color: #fff;">{star}</span>
                        </div>
                        <div style="text-align: center;">
                            <span style="color: #CE93D8;">門</span> <span style="color: #fff;">{door}</span>
                        </div>
                    </div>
                    <div style="text-align: center; margin-top: 8px;">
                        <span style="color: #EF9A9A;">地</span> <span style="color: #fff;">{earth}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ============================================================================
    # SELECTED PALACE DETAIL
    # ============================================================================
    
    st.markdown(f"### 🔍 {palace['icon']} {palace['topic']} Analysis")
    
    comp = reading["components"]
    
    # Component cards
    comp_cols = st.columns(5)
    
    with comp_cols[0]:
        hs = comp["heaven_stem"]
        st.markdown("**Heaven Stem 天干**")
        st.markdown(f"### {hs['character']}")
        st.caption(f"{hs['pinyin']} | {hs['element']}")
        
        color = "#4CAF50" if hs["strength_score"] > 0 else "#F44336" if hs["strength_score"] < 0 else "#9E9E9E"
        st.markdown(f"<span style='color:{color}'>{hs['friendly_strength']}</span>", unsafe_allow_html=True)
        st.caption(f"Score: {hs['strength_score']:+d}")
    
    with comp_cols[1]:
        es = comp["earth_stem"]
        st.markdown("**Earth Stem 地干**")
        st.markdown(f"### {es['character']}")
        st.caption(f"{es['pinyin']} | {es['element']}")
        
        color = "#4CAF50" if es["strength_score"] > 0 else "#F44336" if es["strength_score"] < 0 else "#9E9E9E"
        st.markdown(f"<span style='color:{color}'>{es['friendly_strength']}</span>", unsafe_allow_html=True)
        st.caption(f"Score: {es['strength_score']:+d}")
    
    with comp_cols[2]:
        star = comp["star"]
        st.markdown("**Star 九星**")
        st.markdown(f"### {star['chinese']}")
        st.caption(f"{star['name']} | {star['element']}")
        
        nature_color = "#4CAF50" if star["nature"] == "Auspicious" else "#F44336" if star["nature"] == "Inauspicious" else "#9E9E9E"
        st.markdown(f"<span style='color:{nature_color}'>{star['nature']}</span>", unsafe_allow_html=True)
        
        color = "#4CAF50" if star["strength_score"] > 0 else "#F44336" if star["strength_score"] < 0 else "#9E9E9E"
        st.caption(f"Score: {star['strength_score']:+d}")
    
    with comp_cols[3]:
        door = comp["door"]
        st.markdown("**Door 八門**")
        st.markdown(f"### {door['chinese']}")
        st.caption(f"{door['friendly_name']} | {door['element']}")
        
        nature_color = "#4CAF50" if door["nature"] == "Auspicious" else "#F44336" if door["nature"] == "Inauspicious" else "#9E9E9E"
        st.markdown(f"<span style='color:{nature_color}'>{door['nature']}</span>", unsafe_allow_html=True)
        
        color = "#4CAF50" if door["strength_score"] > 0 else "#F44336" if door["strength_score"] < 0 else "#9E9E9E"
        st.caption(f"Score: {door['strength_score']:+d}")
    
    with comp_cols[4]:
        deity = comp["deity"]
        st.markdown("**Spirit 八神**")
        st.markdown(f"### {deity['chinese']}")
        st.caption(f"{deity['name']}")
        
        nature_color = "#4CAF50" if deity["nature"] == "Auspicious" else "#F44336" if deity["nature"] == "Inauspicious" else "#9E9E9E"
        st.markdown(f"<span style='color:{nature_color}'>{deity['nature']}</span>", unsafe_allow_html=True)
        st.caption(deity.get('function', '')[:30] + "..." if len(deity.get('function', '')) > 30 else deity.get('function', ''))
    
    st.markdown("---")
    
    # ============================================================================
    # GUIDANCE
    # ============================================================================
    
    st.markdown("### 💡 Guidance")
    
    guidance = reading["guidance"]
    
    if guidance["type"] == "success":
        st.success(f"**{guidance['verdict']}** - {guidance['summary']}")
    elif guidance["type"] == "warning":
        st.warning(f"**{guidance['verdict']}** - {guidance['summary']}")
    else:
        st.info(f"**{guidance['verdict']}** - {guidance['summary']}")
    
    st.markdown(f"**💡 Advice:** {guidance['advice']}")
    
    # ============================================================================
    # PALACE RECOMMENDATIONS
    # ============================================================================
    
    st.markdown("---")
    st.markdown("### ⭐ Best Topics Right Now")
    
    with st.spinner("Analyzing all palaces..."):
        summaries = get_all_palaces_summary(reading_datetime, method)
    
    rec_cols = st.columns(3)
    
    for i, s in enumerate(summaries[:3]):
        with rec_cols[i]:
            rank_emoji = ["🥇", "🥈", "🥉"][i]
            
            if s["score"] >= 6:
                st.success(f"{rank_emoji} **{s['icon']} {s['topic']}**")
            elif s["score"] >= 4:
                st.info(f"{rank_emoji} **{s['icon']} {s['topic']}**")
            else:
                st.warning(f"{rank_emoji} **{s['icon']} {s['topic']}**")
            
            st.caption(f"Score: {s['score']}/10 | {s['door']} + {s['star']}")
    
    # ============================================================================
    # ACTIONS
    # ============================================================================
    
    st.markdown("---")
    
    action_cols = st.columns(3)
    
    with action_cols[0]:
        if st.button("📤 Export Reading", use_container_width=True):
            st.switch_page("pages/2_Export.py")
    
    with action_cols[1]:
        if st.button("📜 View History", use_container_width=True):
            st.switch_page("pages/3_History.py")
    
    with action_cols[2]:
        if st.button("🔄 New Reading", use_container_width=True):
            st.session_state.current_chart = None
            st.rerun()

else:
    # No chart yet - show instructions
    st.info("👆 Select a topic and click **Get Your Reading** to generate your Qi Men chart")
    
    # Show quick recommendation
    st.markdown("### ⭐ Quick Recommendation")
    st.caption("Based on current time")
    
    now = get_singapore_time()
    with st.spinner("Checking best topics..."):
        summaries = get_all_palaces_summary(now, method=1)
    
    if summaries:
        best = summaries[0]
        st.success(f"**Best topic right now:** {best['icon']} {best['topic']} (Score: {best['score']}/10)")
        st.caption(f"{best['door']} Door + {best['star']} Star")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.caption("🌟 Ming Qimen 明奇门 | Chart v2.0 | Singapore Time (UTC+8)")
