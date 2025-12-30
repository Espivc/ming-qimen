# Ming Qimen 明奇门 - Project State

## Version: 4.0 (UX Streamlined)
**Last Updated:** 2024-12-30

---

## 🎯 PROJECT OVERVIEW

Ming Qimen is a Streamlit-based QMDJ (Qi Men Dun Jia) chart generator and analyzer with full BaZi (Four Pillars) integration. It serves as the **Developer Engine (Project 2)** that generates rich data for analysis by the **Analyst Engine (Project 1)**.

**Live URL:** Streamlit Cloud deployment
**Repository:** https://github.com/Espivc/ming-qimen

---

## ✅ COMPLETED FEATURES (v4.0)

### Core Features
- [x] QMDJ Hour/Day chart generation
- [x] 9-Palace grid visualization
- [x] Component display (Stems, Doors, Stars, Deities)
- [x] Strength calculation in palace
- [x] JSON export (Universal Schema v2.0)
- [x] Dark theme with gold accents

### BaZi Integration (Phase 5)
- [x] Four Pillars calculation from birth date/time
- [x] Hidden stems extraction
- [x] Ten Gods mapping (all 10 stems)
- [x] Day Master strength assessment
- [x] Useful Gods recommendation
- [x] Special structures detection (Wealth Vault, Nobleman)

### v4.0 UX Improvements (Just Completed)
- [x] **NEW:** Minute input for precise birth time
- [x] **NEW:** "Unknown birth time" skip option
- [x] **FIX:** Settings page now displays BaZi profile correctly
- [x] **FIX:** Consolidated BaZi profile to SIDEBAR ONLY
- [x] **REMOVED:** Duplicate BaZi displays from Settings, Export tabs
- [x] **IMPROVED:** Cleaner navigation flow

---

## 📂 PROJECT STRUCTURE

```
ming-qimen/
├── .streamlit/
│   └── config.toml
├── core/
│   ├── __init__.py
│   ├── qmdj_engine.py
│   └── bazi_calculator_core.py (optional)
├── pages/
│   ├── 1_Chart.py
│   ├── 2_Export.py          ← Streamlined v4.0
│   ├── 3_History.py
│   ├── 4_Settings.py        ← Streamlined v4.0
│   ├── 5_Help.py
│   └── 6_BaZi.py            ← Enhanced v4.0 (minute, unknown time)
├── app.py                    ← Streamlined v4.0
├── requirements.txt
├── README.md
└── PROJECT_STATE.md
```

---

## 🔧 KEY SESSION STATE VARIABLES

```python
# User BaZi Profile (SINGLE SOURCE OF TRUTH)
st.session_state.user_profile = {
    'day_master': 'Geng 庚',
    'element': 'Metal',
    'polarity': 'Yang',
    'strength': 'Weak',
    'strength_score': 4,
    'useful_gods': ['Earth', 'Metal'],
    'unfavorable': ['Fire'],
    'wealth_vault': True,
    'nobleman': False,
    'birth_date': '1988-01-06',
    'birth_time': '12:30',        # Now includes minutes
    'unknown_time': False         # NEW: skip hour pillar flag
}

# BaZi calculation state
st.session_state.bazi_calculated = True/False
st.session_state.pillars = {...}  # Four Pillars data
st.session_state.bazi_result = {...}  # Pre-save calculation

# QMDJ state
st.session_state.current_chart = {...}
st.session_state.selected_palace = 1-9
```

---

## 📋 PAGE FILE NAMES (IMPORTANT!)

The pages folder uses **numbered prefixes**:

| File Name | Sidebar Shows |
|-----------|---------------|
| `1_Chart.py` | Chart |
| `2_Export.py` | Export |
| `3_History.py` | History |
| `4_Settings.py` | Settings |
| `5_Help.py` | Help |
| `6_BaZi.py` | BaZi |

**Navigation code must use:**
```python
st.switch_page("pages/1_Chart.py")  # Correct ✅
st.switch_page("pages/Chart.py")    # Wrong ❌
```

---

## 🐛 BUGS FIXED IN v4.0

| Bug | Cause | Fix |
|-----|-------|-----|
| Settings page not showing profile | Was looking for wrong fields | Now reads `user_profile` correctly |
| BaZi in too many places | UX clutter | Consolidated to sidebar ONLY |
| No minute selection | Missing feature | Added minute dropdown |
| Unknown birth time forces error | No skip option | Added "I don't know" checkbox |
| Export BaZi tab empty | Complex tab structure | Removed tab, inline status |

---

## 🎯 USER FLOW (v4.0)

```
1. Open App → Dashboard with sidebar profile
2. If no profile → Sidebar shows "Set Up BaZi" button
3. Go to BaZi page (6_BaZi.py)
   a. Enter birth date
   b. Enter hour + minute OR check "unknown time"
   c. Click "Calculate BaZi"
   d. Review results
   e. Click "Save to Profile"
4. ✅ Profile now visible in sidebar (everywhere!)
5. Go to Chart → Generate QMDJ reading
6. Go to Export → JSON includes BaZi data automatically
```

---

## 🏠 WHERE BAZI PROFILE SHOWS (v4.0)

**ONLY in sidebar** - appears on ALL pages once saved:
- app.py sidebar ✅
- 1_Chart.py sidebar ✅
- 2_Export.py sidebar ✅
- 3_History.py sidebar ✅
- 4_Settings.py sidebar ✅
- 5_Help.py sidebar ✅
- 6_BaZi.py sidebar ✅

**REMOVED from:**
- Settings BaZi Profile tab (now just links to calculator)
- Export BaZi Profile tab (removed entire tab)
- Export page main content

---

## 📝 PENDING / FUTURE ENHANCEMENTS

### Phase 6: Advanced Features (Planned)
- [ ] Solar Terms (节气) for accurate month pillar
- [ ] Formation identification (#64/#73 books)
- [ ] BaZi-QMDJ cross-reference scoring
- [ ] Luck Pillars (大运) calculation
- [ ] Annual Pillars (流年) overlay

### Known Limitations
- Month pillar uses simplified solar term dates (±1-2 days)
- BaZi calculator is simplified (production should use Ten Thousand Year Calendar)
- Session state resets on browser refresh (Streamlit limitation)

---

## 🧭 CONTINUITY INSTRUCTIONS

### Starting New Chat:
```
Continue Ming Qimen (明奇门) development.
Repository: https://github.com/Espivc/ming-qimen
Current: v4.0 - UX streamlined, minute input added.
Check PROJECT_STATE.md for details.

Key info:
- Page files are numbered: 1_Chart.py, 2_Export.py, etc.
- BaZi saves to st.session_state.user_profile
- BaZi profile displays ONLY in sidebar (all pages)
- User: Ben (Geng Metal, Weak, Pioneer, Wealth Vault)

I want to [your request here].
```

### Key Memory Points:
- Project 2 = Ming Qimen (Developer Engine)
- Project 1 = Claude Analyst (receives JSON)
- Session state key: `user_profile` (not `user_bazi_profile`)
- BaZi profile: SIDEBAR ONLY (consolidated in v4.0)
- Page names have number prefixes

---

## 👤 USER PROFILE (Ben)

```
Day Master: Geng 庚 (Yang Metal)
Strength: Weak
Profile: Pioneer (Indirect Wealth)
Useful Gods: Earth, Metal
Unfavorable: Fire
Special: Wealth Vault present
```

---

## 🏷️ VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12 | Initial QMDJ chart generator |
| 2.0 | 2024-12 | Added export, history, settings |
| 3.0 | 2024-12-30 | Full BaZi integration |
| 3.5 | 2024-12-30 | Session state fix, page navigation fix |
| **4.0** | **2024-12-30** | **UX streamlined: minute input, unknown time option, sidebar-only profile, removed duplicates** |

---

*Ming Qimen 明奇门 - "Clarity for the People"*
