# Ming Qimen 明奇门 - Project State

## Version: 3.1 (Phase 5 UI Fixes Complete)
**Last Updated:** 2024-12-30

---

## 🎯 PROJECT OVERVIEW

Ming Qimen is a Streamlit-based QMDJ (Qi Men Dun Jia) chart generator and analyzer with full BaZi (Four Pillars) integration. It serves as the **Developer Engine (Project 2)** that generates rich data for analysis by the **Analyst Engine (Project 1)**.

**Live URL:** https://ming-qimen.streamlit.app (or current Streamlit deployment)
**Repository:** https://github.com/Espivc/ming-qimen

---

## ✅ COMPLETED FEATURES (v3.1)

### Phase 1-4: QMDJ Core (Previously Complete)
- [x] Hour/Day chart generation
- [x] 9-Palace grid visualization
- [x] Component display (Stems, Doors, Stars, Deities)
- [x] Strength calculation in palace
- [x] JSON export (Universal Schema v2.0)
- [x] Dark theme with gold accents
- [x] Mobile-friendly layout

### Phase 5: BaZi Integration (100% Complete)
- [x] **BaZi Calculator Core Engine** (`core/bazi_engine.py`)
  - Four Pillars calculation from birth date/time
  - Hidden stems extraction for all branches
  - Complete Ten Gods mapping (all 10 stems)
  - Day Master strength assessment
  - Useful Gods recommendation with reasoning
  - Special structures detection (Wealth Vault, Nobleman)
  - Profile type detection (Pioneer, Warrior, Philosopher, etc.)

- [x] **BaZi Calculator Page** (`pages/4_Settings.py` - Birth Date Calculator tab)
  - Birth date input (date picker)
  - Birth time input (exact hour/minute - number inputs)
  - Visual Four Pillars display with color-coded elements
  - Hidden stems shown under each branch
  - Strength score visualization
  - Ten Gods mapping grid with favorable/unfavorable indicators
  - Special structures detection display
  - Auto-save to session state

- [x] **Enhanced Dashboard** (`app.py`)
  - BaZi profile summary in sidebar
  - Shows: Day Master, Element, Strength, Useful Gods, Profile Type
  - Special structures indicators (💰 Wealth Vault, 👑 Nobleman)
  - Fixed HTML rendering in topic cards

- [x] **Enhanced Export** (`pages/2_Export.py`)
  - Universal Schema v2.1 compliance
  - Full Four Pillars in JSON
  - Complete Ten Gods mapping
  - Useful God activation data
  - BaZi alignment score
  - Combined QMDJ + BaZi verdict score

### Phase 5.1: UI Fixes (Just Completed)
- [x] Fixed raw HTML showing in topic grid cards
- [x] Changed birth time input from 15-min intervals to exact minute
- [x] Enhanced BaZi profile display in sidebar
- [x] App title properly set to "Ming Qimen 明奇门"

---

## 📂 PROJECT STRUCTURE

```
ming-qimen/
├── .streamlit/
│   └── config.toml              # Dark theme configuration
├── assets/
│   └── style.css                # Custom styling
├── core/
│   ├── __init__.py              # Module exports
│   ├── qmdj_engine.py           # QMDJ calculations
│   └── bazi_engine.py           # BaZi calculations (Phase 5)
├── pages/
│   ├── 1_Chart.py               # QMDJ chart generator
│   ├── 2_Export.py              # JSON export
│   ├── 3_History.py             # Reading history
│   ├── 4_Settings.py            # BaZi calculator + preferences
│   └── 5_Help.py                # Help & guide
├── .gitignore
├── LICENSE
├── PROJECT_STATE.md             # This file
├── README.md
├── app.py                       # Main dashboard
└── requirements.txt
```

---

## 📊 DATA SCHEMA: Universal Schema v2.1

### BaZi Data Structure:
```json
{
  "bazi_data": {
    "chart_source": "Birth Date Calculator",
    "birth_data": {
      "year": 1985,
      "month": 8,
      "day": 15,
      "hour": 14
    },
    "day_master": {
      "chinese": "庚",
      "pinyin": "Geng",
      "element": "Metal",
      "polarity": "Yang",
      "strength": "Weak",
      "strength_score": 4
    },
    "four_pillars": {
      "year": {"stem": {...}, "branch": {...}, "hidden_stems": [...]},
      "month": {...},
      "day": {...},
      "hour": {...}
    },
    "ten_gods_mapping": {
      "Wood": "偏财",
      "Fire": "七杀",
      "Earth": "偏印",
      "Metal": "比肩",
      "Water": "食神"
    },
    "useful_gods": {
      "primary": "Earth",
      "secondary": "Metal",
      "favorable": ["Earth", "Metal"],
      "unfavorable": ["Fire"],
      "reasoning": "Weak Metal needs Earth (Resource) and Metal (Companion) support"
    },
    "special_structures": {
      "wealth_vault": true,
      "wealth_vault_location": "Day Pillar (戌)",
      "nobleman_present": false
    },
    "profile": {
      "dominant_god": "Indirect Wealth",
      "type": "Pioneer"
    }
  }
}
```

---

## 🔄 WORKFLOW: Project 2 → Project 1

```
┌─────────────────────────────────────────────────────────────┐
│                    PROJECT 2 (Ming Qimen)                   │
│                    Developer Engine                         │
├─────────────────────────────────────────────────────────────┤
│  1. Calculate BaZi Profile (Settings → Birth Date Calculator)│
│  2. Generate QMDJ Chart (Chart page)                        │
│  3. Export Universal Schema v2.1 JSON (Export page)         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼ Copy JSON
┌─────────────────────────────────────────────────────────────┐
│                    PROJECT 1 (Claude)                       │
│                    Analyst Engine                           │
├─────────────────────────────────────────────────────────────┤
│  1. Paste JSON data                                        │
│  2. Say: "Analyze and output as bilingual docx report"     │
│  3. Receive: Formation ID, Strategic Actions, Synthesis    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 USER JOURNEY (v3.1)

```
New User:
1. Open Ming Qimen → See Dashboard with current energy
2. Go to Settings → Birth Date Calculator tab
3. Enter birth date & exact time (hour + minute)
4. Click "Calculate My BaZi"
5. See Four Pillars, Day Master, Strength, Useful Gods
6. Profile auto-saved (visible in sidebar!)
7. Go to Chart → Generate QMDJ reading
8. See personalized guidance based on BaZi profile
9. Go to Export → Download JSON for Project 1 analysis
```

---

## 📝 PENDING / FUTURE ENHANCEMENTS

### Phase 6: Advanced Features (Planned)
- [ ] Solar Terms (节气) for accurate month pillar boundary
- [ ] Ten Thousand Year Calendar lookup for precise day pillar
- [ ] Luck Pillars (大运) calculation
- [ ] Annual Pillars (流年) overlay
- [ ] Formation identification (#64/#73 books)
- [ ] Chart comparison tool

### Phase 7: ML Integration (Planned)
- [ ] Outcome tracking database
- [ ] Pattern recognition from history
- [ ] Accuracy scoring
- [ ] Automated insights generation

---

## 🔧 TECHNICAL NOTES

### Requirements:
```
streamlit>=1.28.0
kinqimen>=0.0.6  # With fallback if unavailable
sxtwl>=2.0.0    # With fallback if unavailable
```

### BaZi Calculator: 
- Pure Python implementation (no external dependencies)
- Fallback calculations when kinqimen unavailable
- Simplified solar term boundaries (approximation)

### Known Limitations:
- Month pillar uses simplified solar term dates (±1-2 days from actual)
- kinqimen library may have Python version compatibility issues
- Fallback QMDJ calculations are simplified

---

## 📋 TRIGGER PHRASES FOR PROJECT 1

When using the JSON export in Project 1, these phrases activate specific outputs:

| Phrase | Output |
|--------|--------|
| "Analyze and output as bilingual docx report" | Full 8-section formatted document |
| "Quick verdict" | Executive summary only |
| "Strategic actions" | 3 recommended actions with timing |
| "BaZi synthesis" | Focus on BaZi-QMDJ alignment analysis |

---

## 🏷️ VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12 | Initial QMDJ chart generator |
| 2.0 | 2024-12 | Added export, history, settings |
| 3.0 | 2024-12-30 | Full BaZi integration - Calculator, Ten Gods, Alignment Score |
| **3.1** | **2024-12-30** | **UI Fixes** - Exact time input, HTML rendering fix, enhanced sidebar |

---

## 🧭 CONTINUITY INSTRUCTIONS

### Starting New Chat:
```
Continue Ming Qimen (明奇门) development.
Check PROJECT_STATE.md in Espivc/ming-qimen repo.
Current: v3.1 - Phase 5 complete with UI fixes.
I want to [your request here].
```

### Key Memory Points:
- Project 2 = Ming Qimen (Developer Engine)
- Project 1 = Claude Analyst (receives JSON)
- BaZi calculator: Birth Date → Four Pillars → Day Master → Useful Gods
- Universal Schema v2.1 for data exchange

---

## 📞 CROSS-PROJECT REFERENCES

- **Project 1 System Prompt:** QI MEN + BAZI STRATEGIC INTELLIGENCE ENGINE v2.0
- **Universal Schema:** v2.1 (QMDJ + BaZi integrated)
- **User Profile:** Weak Geng Metal, Pioneer (Indirect Wealth), Wealth Vault

---

*Ming Qimen 明奇门 - "Clarity for the People" - Illuminating the Hidden Doors*
