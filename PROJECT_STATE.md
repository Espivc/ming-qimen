# 🌟 MING QIMEN 明奇门 - PROJECT STATE TRACKER
Last Updated: 2025-12-29
Version: 5.0 (Phase 5 - Enhanced BaZi Calculator)
Status: 🟡 READY FOR DEPLOYMENT

---

## 🌟 BRAND IDENTITY
- **Name:** Ming Qimen 明奇门
- **Tagline:** "Clarity for the People"
- **Sub-tagline:** "Ancient Wisdom, Made Bright and Simple"
- **Promise:** "Guiding you first, because your peace of mind matters."

---

## 📊 PROJECT OVERVIEW
- **Purpose:** Beginner-friendly QMDJ + BaZi guidance system
- **Target User:** First-timers, non-experts, anyone seeking direction
- **Deployment:** Streamlit Cloud
- **Repository:** https://github.com/Espivc/ming-qimen

---

## ✅ WHAT'S NEW IN V5.0 (Phase 5)

### 🎂 Birth Date Calculator
- ✅ Enter birth date & time → Auto-calculate Four Pillars
- ✅ Visual Four Pillars display (年月日时)
- ✅ Day Master extraction with strength analysis
- ✅ Auto-determine Useful Gods based on DM strength
- ✅ Profile type detection (Pioneer, Warrior, etc.)

### 🔮 BaZi Engine (`core/bazi_engine.py`)
- ✅ Four Pillars calculation (Year/Month/Day/Hour)
- ✅ Hidden stems extraction (藏干)
- ✅ Ten Gods mapping (十神)
- ✅ Day Master strength scoring
- ✅ Useful Gods determination
- ✅ Special structures detection (Wealth Vault, Nobleman)

### 📊 Enhanced Settings Page
- ✅ Tab 1: Birth Date Calculator (NEW!)
- ✅ Tab 2: Manual Profile Entry
- ✅ Tab 3: Preferences
- ✅ Beautiful Four Pillars visualization
- ✅ Ten Gods mapping display
- ✅ Auto-save to user profile

---

## 📁 FILE STRUCTURE
```
ming-qimen/
├── .streamlit/
│   └── config.toml
├── assets/
│   └── style.css
├── core/
│   ├── __init__.py
│   ├── qmdj_engine.py      ← Phase 4: QMDJ calculations
│   └── bazi_engine.py      ← Phase 5: BaZi calculations (NEW!)
├── pages/
│   ├── 1_Chart.py
│   ├── 2_Export.py
│   ├── 3_History.py
│   ├── 4_Settings.py       ← Enhanced with Birth Calculator
│   └── 5_Help.py
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── PROJECT_STATE.md
```

---

## 🔧 BAZI ENGINE FEATURES

### Four Pillars Calculation
```python
calculate_bazi_profile(year, month, day, hour)
# Returns:
# - four_pillars (Year/Month/Day/Hour with stems & branches)
# - day_master (element, polarity, strength)
# - ten_gods (relationships to Day Master)
# - useful_gods (favorable/unfavorable elements)
# - special_structures (Wealth Vault, Nobleman)
# - profile (dominant Ten God, profile type)
```

### Ten Gods Mapping
| Relationship | Yang | Yin |
|--------------|------|-----|
| Same Element | 比肩 Friend | 劫财 Rob Wealth |
| DM Produces | 食神 Eating God | 伤官 Hurting Officer |
| DM Controls | 偏财 Indirect Wealth | 正财 Direct Wealth |
| Controls DM | 七杀 7 Killings | 正官 Direct Officer |
| Produces DM | 偏印 Indirect Resource | 正印 Direct Resource |

### Profile Types
| Ten God | Profile |
|---------|---------|
| Friend | Networker |
| Rob Wealth | Competitor |
| Eating God | Philosopher |
| Hurting Officer | Artist |
| Indirect Wealth | Pioneer |
| Direct Wealth | Leader |
| 7 Killings | Warrior |
| Direct Officer | Director |
| Indirect Resource | Strategist |
| Direct Resource | Diplomat |

---

## 📋 DEPLOYMENT CHECKLIST

### Files to Update on GitHub:
1. `core/__init__.py` - Updated with BaZi imports
2. `core/bazi_engine.py` - NEW FILE
3. `pages/4_Settings.py` - Enhanced with calculator
4. `PROJECT_STATE.md` - Updated

### After Upload:
1. Wait 2-3 minutes for Streamlit rebuild
2. Test: Go to Settings → Birth Date Calculator tab
3. Test: Enter a birth date/time → Click Calculate
4. Test: Verify Four Pillars display correctly
5. Test: Check Day Master strength and Useful Gods
6. Test: Verify profile auto-saves

---

## 🎯 USER FLOW (Phase 5)

```
New User Journey:
1. Open App → See Dashboard with recommendations
2. Go to Settings → Birth Date Calculator
3. Enter birth date & time
4. Click "Calculate My BaZi"
5. See Four Pillars, Day Master, Useful Gods
6. Profile auto-saved!
7. Go to Chart → Generate Reading
8. Reading now personalized with BaZi profile
9. Export → JSON includes full BaZi data
```

---

## 🚀 FUTURE PHASES

### Phase 6: Advanced Features
- [ ] Formation identification (#64/#73 books)
- [ ] BaZi-QMDJ cross-reference scoring
- [ ] Luck Pillar calculations
- [ ] Annual influence analysis
- [ ] Multiple user profiles
- [ ] History analytics dashboard

---

## 🧭 CONTINUITY INSTRUCTIONS

### Starting New Chat:
```
Continue Ming Qimen (明奇门) development.
Check PROJECT_STATE.md in Espivc/ming-qimen.
Current: Phase 5 complete (BaZi Calculator).
I want to [your request here].
```

---

**END OF PROJECT STATE**
Last updated: 2025-12-29
🌟 Ming Qimen 明奇门 | Clarity for the People
