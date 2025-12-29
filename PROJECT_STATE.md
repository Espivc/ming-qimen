# 🌟 MING QIMEN 明奇门 - PROJECT STATE TRACKER
Last Updated: 2025-12-29
Version: 4.0 (Phase 4 - Real QMDJ Calculations)
Status: 🟡 READY FOR DEPLOYMENT

---

## 🌟 BRAND IDENTITY
- **Name:** Ming Qimen 明奇门
- **Tagline:** "Clarity for the People"
- **Sub-tagline:** "Ancient Wisdom, Made Bright and Simple"
- **Promise:** "Guiding you first, because your peace of mind matters."

---

## 📊 PROJECT OVERVIEW
- **Purpose:** Beginner-friendly QMDJ guidance system with real calculations
- **Target User:** First-timers, non-experts, anyone seeking direction
- **Deployment:** Streamlit Cloud
- **Live URL:** https://qimen-pro-qfvejjsappeenzfeuretzw9.streamlit.app/
- **Repository:** https://github.com/Espivc/qimen-pro

---

## ✅ WHAT'S NEW IN V4.0 (Phase 4)

### 🔮 Real QMDJ Engine
- ✅ Created `core/qmdj_engine.py` - Complete QMDJ calculation module
- ✅ kinqimen library integration with graceful fallback
- ✅ Joey Yap terminology mapping (Chinese → English)
- ✅ Strength calculations (Timely/Prosperous/Resting/Confined/Dead)
- ✅ Component scoring system (-3 to +3)
- ✅ Palace-based analysis

### 📊 9-Palace Grid
- ✅ Visual grid in Luo Shu arrangement
- ✅ Real-time component display per palace
- ✅ Highlighted selected palace
- ✅ Heaven/Earth stems, Star, Door, Deity visible

### 🎯 Palace Recommendations
- ✅ `get_all_palaces_summary()` - Ranks all 9 palaces
- ✅ Best topic recommendation on dashboard
- ✅ Score-based sorting (1-10 scale)
- ✅ Door + Star combination display

### 📤 Universal Schema v2.0 Export
- ✅ Full schema compliance
- ✅ Component strength scores included
- ✅ BaZi profile integration
- ✅ ML tracking CSV generation
- ✅ One-click JSON copy

### 👤 BaZi Integration
- ✅ Profile storage in session state
- ✅ Quick preset for Geng Metal Pioneer
- ✅ Useful gods configuration
- ✅ Special structures (Wealth Vault, Nobleman)

---

## 📁 FILE STRUCTURE
```
ming-qimen/
├── .streamlit/
│   └── config.toml
├── assets/
│   └── style.css
├── core/                    ← NEW
│   ├── __init__.py
│   └── qmdj_engine.py       ← QMDJ calculation engine
├── pages/
│   ├── 1_Chart.py           ← Real QMDJ calculations
│   ├── 2_Export.py          ← Universal Schema export
│   ├── 3_History.py
│   ├── 4_Settings.py        ← BaZi profile
│   └── 5_Help.py
├── app.py                   ← Dashboard with recommendations
├── requirements.txt
└── PROJECT_STATE.md
```

---

## 🔧 TECHNICAL FEATURES

### QMDJ Engine (`core/qmdj_engine.py`)
```python
# Key classes
QMDJEngine          # kinqimen wrapper with fallback
ChartProcessor      # Raw chart → processed data

# Key functions
generate_qmdj_reading(date, palace, method)  # Single reading
get_all_palaces_summary(date, method)        # All 9 palaces ranked

# Constants
PALACE_INFO         # Palace number → name/element/direction
PALACE_TOPICS       # Palace number → topic/icon
STAR_MAPPING        # Chinese → Joey Yap English
DOOR_MAPPING        # Chinese → Joey Yap English
DEITY_MAPPING       # Chinese → Joey Yap English
```

### Strength Calculation
```python
def calculate_strength(component_element, palace_element):
    # Same element → Timely (+2)
    # Palace produces component → Prosperous (+3)
    # Component produces palace → Resting (0)
    # Palace controls component → Confined (-2)
    # Component controls palace → Dead (-3)
```

### Score Normalization
```python
# Component total: -12 to +12
# Normalized: ((total + 12) / 24) * 9 + 1 → 1-10 scale
```

---

## 🎯 BEGINNER-FRIENDLY TERMINOLOGY

### Energy Levels
| Technical | Friendly | Advice |
|-----------|----------|--------|
| Timely (+2) | 🔥 High Energy | Take Action! |
| Prosperous (+3) | ✨ Good Energy | Favorable |
| Resting (0) | 😐 Balanced | Proceed Normally |
| Confined (-2) | 🌙 Low Energy | Be Patient |
| Dead (-3) | 💤 Rest Energy | Wait & Reflect |

### Door Names
| Original | Friendly |
|----------|----------|
| Death 死门 | Stillness |
| Fear 惊门 | Surprise |

---

## 📋 DEPLOYMENT CHECKLIST

### Files to Upload to GitHub:
1. `app.py` - Main dashboard
2. `core/__init__.py` - Module init
3. `core/qmdj_engine.py` - QMDJ engine
4. `pages/1_Chart.py` - Chart page
5. `pages/2_Export.py` - Export page
6. `pages/3_History.py` - History page
7. `pages/4_Settings.py` - Settings page
8. `pages/5_Help.py` - Help page
9. `assets/style.css` - Styles
10. `.streamlit/config.toml` - Config
11. `requirements.txt` - Dependencies
12. `PROJECT_STATE.md` - This file

### After Upload:
1. Wait 2-3 minutes for Streamlit rebuild
2. Test: Dashboard shows palace recommendations
3. Test: Chart generates with 9-palace grid
4. Test: Export produces Universal Schema JSON
5. Test: BaZi profile saves in Settings

---

## ⚠️ KNOWN ISSUES

### kinqimen Compatibility
- kinqimen has Python version compatibility issues (ephem library)
- Fallback calculations work correctly
- Real kinqimen may work on Streamlit Cloud with different Python version

### To Fix Later
- [ ] Test kinqimen on Streamlit Cloud
- [ ] Add formation detection (Phase 5)
- [ ] Enhanced BaZi with Four Pillars (Phase 5)

---

## 🚀 FUTURE PHASES

### Phase 5: Enhanced BaZi
- Full Four Pillars calculation
- Hidden stems extraction
- Ten Gods mapping
- Useful God activation percentage
- Luck Pillar integration

### Phase 6: Advanced Features
- Formation identification (#64/#73)
- Multiple user profiles
- History analytics
- Export to calendar
- Mobile app wrapper

---

## 🧭 CONTINUITY INSTRUCTIONS

### Starting New Chat:
```
Continue Ming Qimen (明奇门) development.
Check PROJECT_STATE.md in Espivc/qimen-pro.
Current: Phase 4 complete, ready for deployment.
I want to [your request here].
```

---

**END OF PROJECT STATE**
Last updated: 2025-12-29
🌟 Ming Qimen 明奇门 | Clarity for the People
