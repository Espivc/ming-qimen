# 🌟 Ming Qimen 明奇门

> **"Clarity for the People"** - Ancient Wisdom, Made Bright and Simple

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ming-qimen.streamlit.app)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🔮 What is Ming Qimen?

Ming Qimen is a **beginner-friendly Qi Men Dun Jia (奇門遁甲)** guidance system. We take one of China's most powerful ancient divination methods and make it accessible to everyone.

**No paywalls. No complex data entry. Just clear guidance.**

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔮 **Real QMDJ Calculations** | Accurate Qi Men charts using kinqimen engine |
| 📊 **9-Palace Grid** | Visual display of all palace components |
| 🎯 **Topic Recommendations** | Best topic for any moment, ranked by score |
| 💪 **Strength Analysis** | Component energy levels (High/Good/Balanced/Low/Rest) |
| 👤 **BaZi Integration** | Personal profile for customized guidance |
| 📤 **Universal Schema Export** | JSON export for AI analysis (Project 1) |
| 📱 **Mobile Friendly** | Works on desktop and phone |

---

## 🚀 Quick Start

### Try it Online
👉 [Launch Ming Qimen](https://ming-qimen.streamlit.app)

### Run Locally
```bash
# Clone the repo
git clone https://github.com/Espivc/ming-qimen.git
cd ming-qimen

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 📖 How to Use

1. **Select a Topic** - Career, Wealth, Relationships, etc.
2. **Choose a Time** - Current or future
3. **Get Your Reading** - See the cosmic energy pattern
4. **Follow the Guidance** - Clear, actionable advice

---

## 🏛️ The 9 Topics (Palaces)

| # | Topic | What It Covers |
|---|-------|----------------|
| 1 | 💼 Career | Job, business, life path |
| 2 | 💕 Relations | Marriage, partnerships |
| 3 | 💪 Health | Wellness, family, new starts |
| 4 | 💰 Wealth | Money, investments |
| 5 | 🎯 Self | General guidance |
| 6 | 🤝 Mentor | Helpful people, travel |
| 7 | 👶 Children | Creativity, projects |
| 8 | 📚 Knowledge | Education, skills |
| 9 | 🌟 Fame | Recognition, reputation |

---

## 🔧 Technical Stack

- **Frontend:** Streamlit
- **QMDJ Engine:** kinqimen + custom fallback
- **Timezone:** Singapore (UTC+8)
- **Export Format:** Universal Schema v2.0 (JSON)

---

## 📁 Project Structure

```
ming-qimen/
├── app.py                  # Main dashboard
├── core/
│   ├── __init__.py
│   └── qmdj_engine.py      # QMDJ calculation engine
├── pages/
│   ├── 1_Chart.py          # Chart generator
│   ├── 2_Export.py         # JSON export
│   ├── 3_History.py        # Reading history
│   ├── 4_Settings.py       # BaZi profile
│   └── 5_Help.py           # Help & guide
├── assets/
│   └── style.css           # Custom styling
├── .streamlit/
│   └── config.toml         # Streamlit config
├── requirements.txt
└── PROJECT_STATE.md        # Development tracker
```

---

## 🎯 Roadmap

- [x] **Phase 3:** Ming Qimen rebrand, UX improvements
- [x] **Phase 4:** Real QMDJ calculations, 9-palace grid
- [ ] **Phase 5:** Enhanced BaZi (Four Pillars, Ten Gods)
- [ ] **Phase 6:** Formation detection, history analytics

---

## 👤 About

Created by **Beng (明)** - "Brightness"

> *"I created Ming Qimen because I believe wisdom shouldn't come with a price tag or a headache. My goal is to use that light to clear the fog of ancient calculations."*

---

## 📄 License

MIT License - Free to use, modify, and distribute.

---

## 🙏 Acknowledgments

- [kinqimen](https://github.com/kentang2017/kinqimen) - Python QMDJ library
- [Streamlit](https://streamlit.io) - App framework
- Joey Yap methodology for terminology reference

---

🌟 **Ming Qimen 明奇门** | *Guiding you first, because your peace of mind matters.*
