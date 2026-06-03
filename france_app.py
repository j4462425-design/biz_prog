# ============================================================
# Mots Clés - 프랑스어 학습 웹앱 (Premium Edition)
# 설명: 한국인 대학생을 위한 프랑스어 단어 학습 플랫폼
# 보안 참고: 로컬 JSON 저장 방식, 인증 없음 (단일 사용자용)
# TODO(security): 멀티유저 환경에서는 인증 및 세션 관리 필요
# ============================================================

import streamlit as st
import json
import random
import os
import re
import uuid
from datetime import datetime, date
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ─────────────────────────────────────────
# 보안: 고정된 파일 경로만 사용 (경로 순회 방지)
# ─────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "sample_words.json")

# ─────────────────────────────────────────
# 기본 제공 단어 데이터 (Streamlit Cloud 환경 대응 내장 데이터)
# ─────────────────────────────────────────
DEFAULT_WORDS = {
  "words": [
    {
      "id": "w001",
      "french": "bonjour",
      "korean": "안녕하세요",
      "example": "Bonjour, comment ça va?",
      "example_kr": "안녕하세요, 어떻게 지내세요?",
      "category": "일상생활",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w002",
      "french": "merci",
      "korean": "감사합니다",
      "example": "Merci beaucoup pour votre aide.",
      "example_kr": "도움 주셔서 정말 감사합니다.",
      "category": "일상생활",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w003",
      "french": "s'il vous plaît",
      "korean": "부탁합니다",
      "example": "Un café, s'il vous plaît.",
      "example_kr": "커피 한 잔 부탁합니다.",
      "category": "일상생활",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w004",
      "french": "au revoir",
      "korean": "안녕히 가세요",
      "example": "Au revoir, à bientôt!",
      "example_kr": "안녕히 가세요, 곧 봐요!",
      "category": "일상생활",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w005",
      "french": "excusez-moi",
      "korean": "실례합니다",
      "example": "Excusez-moi, où est la gare?",
      "example_kr": "실례합니다, 기차역이 어디에 있나요?",
      "category": "일상생활",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w006",
      "french": "l'aéroport",
      "korean": "공항",
      "example": "Je dois aller à l'aéroport demain.",
      "example_kr": "나는 내일 공항에 가야 해.",
      "category": "여행",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w007",
      "french": "l'hôtel",
      "korean": "호텔",
      "example": "L'hôtel est très confortable.",
      "example_kr": "호텔이 매우 편안합니다.",
      "category": "여행",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w008",
      "french": "le billet",
      "korean": "티켓, 표",
      "example": "J'ai acheté un billet de train.",
      "example_kr": "나는 기차표를 샀어.",
      "category": "여행",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w009",
      "french": "la valise",
      "korean": "여행 가방",
      "example": "Ma valise est trop lourde.",
      "example_kr": "내 여행 가방이 너무 무거워.",
      "category": "여행",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w010",
      "french": "le passeport",
      "korean": "여권",
      "example": "N'oublie pas ton passeport!",
      "example_kr": "여권을 잊지 마!",
      "category": "여행",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w011",
      "french": "le pain",
      "korean": "빵",
      "example": "Je mange du pain chaque matin.",
      "example_kr": "나는 매일 아침 빵을 먹어.",
      "category": "음식",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w012",
      "french": "le fromage",
      "korean": "치즈",
      "example": "Le fromage français est délicieux.",
      "example_kr": "프랑스 치즈는 맛있어.",
      "category": "음식",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w013",
      "french": "le vin",
      "korean": "와인",
      "example": "Un verre de vin, s'il vous plaît.",
      "example_kr": "와인 한 잔 부탁합니다.",
      "category": "음식",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w014",
      "french": "le restaurant",
      "korean": "식당, 레스토랑",
      "example": "Ce restaurant est excellent.",
      "example_kr": "이 식당은 훌륭해.",
      "category": "음식",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w015",
      "french": "délicieux",
      "korean": "맛있는",
      "example": "Ce gâteau est délicieux!",
      "example_kr": "이 케이크는 정말 맛있어!",
      "category": "음식",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w016",
      "french": "l'université",
      "korean": "대학교",
      "example": "Je vais à l'université de Paris.",
      "example_kr": "나는 파리 대학교에 다녀.",
      "category": "학교",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w017",
      "french": "le cours",
      "korean": "수업",
      "example": "Le cours de français commence à 9h.",
      "example_kr": "프랑스어 수업은 9시에 시작해.",
      "category": "학교",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w018",
      "french": "les devoirs",
      "korean": "숙제",
      "example": "J'ai beaucoup de devoirs aujourd'hui.",
      "example_kr": "오늘 숙제가 많아.",
      "category": "학교",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w019",
      "french": "l'examen",
      "korean": "시험",
      "example": "L'examen final est la semaine prochaine.",
      "example_kr": "기말고사는 다음 주야.",
      "category": "학교",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w020",
      "french": "le professeur",
      "korean": "교수, 선생님",
      "example": "Mon professeur est très sympa.",
      "example_kr": "내 교수님은 매우 친절해.",
      "category": "학교",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w021",
      "french": "je m'appelle",
      "korean": "내 이름은 ~입니다",
      "example": "Je m'appelle Marie.",
      "example_kr": "제 이름은 마리입니다.",
      "category": "DELF A1",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w022",
      "french": "avoir",
      "korean": "가지다, ~이다",
      "example": "J'ai vingt ans.",
      "example_kr": "나는 스무 살이야.",
      "category": "DELF A1",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w023",
      "french": "être",
      "korean": "있다, ~이다",
      "example": "Je suis étudiant.",
      "example_kr": "나는 학생이야.",
      "category": "DELF A1",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w024",
      "french": "aller",
      "korean": "가다",
      "example": "Je vais au marché.",
      "example_kr": "나는 시장에 가.",
      "category": "DELF A1",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w025",
      "french": "habiter",
      "korean": "살다, 거주하다",
      "example": "J'habite à Séoul.",
      "example_kr": "나는 서울에 살아.",
      "category": "DELF A1",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w026",
      "french": "travailler",
      "korean": "일하다",
      "example": "Elle travaille dans un bureau.",
      "example_kr": "그녀는 사무실에서 일해.",
      "category": "DELF A2",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w027",
      "french": "comprendre",
      "korean": "이해하다",
      "example": "Je comprends un peu le français.",
      "example_kr": "나는 프랑스어를 조금 이해해.",
      "category": "DELF A2",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w028",
      "french": "choisir",
      "korean": "선택하다",
      "example": "Tu peux choisir entre les deux.",
      "example_kr": "너는 둘 중에서 선택할 수 있어.",
      "category": "DELF A2",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w029",
      "french": "se souvenir",
      "korean": "기억하다",
      "example": "Je me souviens de toi.",
      "example_kr": "나는 너를 기억해.",
      "category": "DELF A2",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    },
    {
      "id": "w030",
      "french": "cependant",
      "korean": "그러나, 하지만",
      "example": "Il est gentil, cependant un peu timide.",
      "example_kr": "그는 친절하지만 약간 수줍음이 많아.",
      "category": "DELF A2",
      "favorited": False,
      "memorized": False,
      "quiz_correct": 0,
      "quiz_wrong": 0
    }
  ],
  "stats": {
    "total_quiz_sessions": 0,
    "total_correct": 0,
    "total_wrong": 0,
    "xp": 0,
    "level": 1,
    "achievements": [],
    "daily_word_date": "",
    "daily_word_id": "",
    "study_days": []
  }
}

# ─────────────────────────────────────────
# 상수
# ─────────────────────────────────────────
CATEGORIES = ["전체", "일상생활", "여행", "음식", "학교", "DELF A1", "DELF A2"]

LEVELS = {
    1: {"name": "초보자",       "icon": "🌱", "min_xp": 0,    "max_xp": 100,  "color": "#34d399"},
    2: {"name": "탐험가",       "icon": "🗺️", "min_xp": 100,  "max_xp": 300,  "color": "#60a5fa"},
    3: {"name": "학습자",       "icon": "📚", "min_xp": 300,  "max_xp": 600,  "color": "#a78bfa"},
    4: {"name": "고급 학습자",  "icon": "⭐", "min_xp": 600,  "max_xp": 1000, "color": "#fbbf24"},
    5: {"name": "프랑스어 마스터","icon": "🏆","min_xp": 1000, "max_xp": 99999,"color": "#f87171"},
}

ACHIEVEMENTS = {
    "first_word":  {"name": "첫 단어 등록",    "desc": "첫 번째 단어를 등록했어요!",           "icon": "✏️",  "xp": 10},
    "words_10":    {"name": "단어 10개 달성",   "desc": "단어장에 10개를 등록했어요!",          "icon": "📖",  "xp": 20},
    "words_50":    {"name": "단어 50개 달성",   "desc": "단어장에 50개를 등록했어요!",          "icon": "📚",  "xp": 50},
    "quiz_10":     {"name": "퀴즈 10문제 정답", "desc": "퀴즈에서 10문제를 맞혔어요!",         "icon": "🎯",  "xp": 30},
    "quiz_50":     {"name": "퀴즈 50문제 정답", "desc": "퀴즈에서 50문제를 맞혔어요!",         "icon": "🎖️", "xp": 80},
    "accuracy_80": {"name": "정답률 80% 달성",  "desc": "퀴즈 정답률 80%를 달성했어요!",       "icon": "🎊",  "xp": 50},
    "memorized_10":{"name": "단어 10개 암기",   "desc": "플래시카드로 10개를 암기했어요!",      "icon": "🧠",  "xp": 25},
    "favorite_5":  {"name": "즐겨찾기 5개",     "desc": "5개의 단어를 즐겨찾기에 추가했어요!", "icon": "⭐",  "xp": 15},
}

CAT_COLORS = {
    "일상생활": "#3b82f6",
    "여행":     "#10b981",
    "음식":     "#f59e0b",
    "학교":     "#8b5cf6",
    "DELF A1":  "#ef4444",
    "DELF A2":  "#ec4899",
}

# ─────────────────────────────────────────
# 보안: 입력 검증
# ─────────────────────────────────────────
def sanitize_text(text: str, max_length: int = 500) -> str:
    if not isinstance(text, str):
        return ""
    text = text[:max_length]
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    return text.strip()

def validate_word_input(french: str, korean: str):
    if not french or not korean:
        return False, "프랑스어 단어와 한국어 뜻은 필수입니다."
    if len(french) > 200 or len(korean) > 200:
        return False, "단어는 200자 이하여야 합니다."
    return True, ""

# ─────────────────────────────────────────
# 데이터 I/O
# ─────────────────────────────────────────
def load_data() -> dict:
    if "app_data" in st.session_state:
        return st.session_state.app_data

    data = None
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
    except Exception:
        pass

    if not data or not isinstance(data, dict):
        import copy
        data = copy.deepcopy(DEFAULT_WORDS)
    else:
        data.setdefault("words", [])
        data.setdefault("stats", _default_stats())

    st.session_state.app_data = data
    return data

def save_data(data: dict) -> bool:
    st.session_state.app_data = data
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    return True

def _default_stats() -> dict:
    return {
        "total_quiz_sessions": 0,
        "total_correct": 0,
        "total_wrong": 0,
        "xp": 0,
        "level": 1,
        "achievements": [],
        "daily_word_date": "",
        "daily_word_id": "",
    }

# ─────────────────────────────────────────
# XP / 레벨 / 업적
# ─────────────────────────────────────────
def get_level_info(xp: int) -> dict:
    for lv in sorted(LEVELS.keys(), reverse=True):
        if xp >= LEVELS[lv]["min_xp"]:
            return {**LEVELS[lv], "level": lv}
    return {**LEVELS[1], "level": 1}

def check_achievements(data: dict) -> dict:
    achieved = data["stats"].get("achievements", [])
    words    = data["words"]
    stats    = data["stats"]
    newly    = []

    def unlock(key, xp_reward):
        if key not in achieved:
            achieved.append(key)
            newly.append(key)
            data["stats"]["xp"] = data["stats"].get("xp", 0) + xp_reward

    word_count = len(words)
    if word_count >= 1:  unlock("first_word",   ACHIEVEMENTS["first_word"]["xp"])
    if word_count >= 10: unlock("words_10",      ACHIEVEMENTS["words_10"]["xp"])
    if word_count >= 50: unlock("words_50",      ACHIEVEMENTS["words_50"]["xp"])

    total_correct = stats.get("total_correct", 0)
    if total_correct >= 10: unlock("quiz_10", ACHIEVEMENTS["quiz_10"]["xp"])
    if total_correct >= 50: unlock("quiz_50", ACHIEVEMENTS["quiz_50"]["xp"])

    total_q = stats.get("total_correct", 0) + stats.get("total_wrong", 0)
    if total_q >= 10 and (stats.get("total_correct", 0) / total_q * 100) >= 80:
        unlock("accuracy_80", ACHIEVEMENTS["accuracy_80"]["xp"])

    memorized_count = sum(1 for w in words if w.get("memorized", False))
    if memorized_count >= 10: unlock("memorized_10", ACHIEVEMENTS["memorized_10"]["xp"])

    fav_count = sum(1 for w in words if w.get("favorited", False))
    if fav_count >= 5: unlock("favorite_5", ACHIEVEMENTS["favorite_5"]["xp"])

    data["stats"]["achievements"] = achieved
    lv_info = get_level_info(data["stats"]["xp"])
    old_lv  = data["stats"].get("level", 1)
    data["stats"]["level"] = lv_info["level"]
    if lv_info["level"] > old_lv:
        st.balloons()
        st.toast(f"🎉 레벨 업! {lv_info['icon']} {lv_info['name']}이 되었습니다!", icon="🏆")

    for key in newly:
        st.toast(f"{ACHIEVEMENTS[key]['icon']} 업적: {ACHIEVEMENTS[key]['name']} (+{ACHIEVEMENTS[key]['xp']} XP)", icon="🏅")

    return data

# ─────────────────────────────────────────
# CSS 주입 (Premium Design)
# ─────────────────────────────────────────
def inject_css():
    st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:ital,wght@0,700;0,800;1,700&display=swap');

/* ── Root Variables ── */
:root {
  --blue:   #0055A4;
  --red:    #EF4135;
  --white:  #FFFFFF;
  --bg:     #07091a;
  --surface:#0d1230;
  --card:   rgba(255,255,255,0.04);
  --border: rgba(255,255,255,0.08);
  --text:   #e2e8f8;
  --muted:  #64748b;
  --accent: #3b82f6;
  --green:  #10b981;
  --radius: 16px;
}

/* ── Global ── */
html, body, .stApp {
  font-family: 'Inter', sans-serif;
  background: var(--bg) !important;
  color: var(--text) !important;
}
.main .block-container {
  padding: 2rem 2.5rem 4rem;
  max-width: 1140px;
}
* { box-sizing: border-box; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #070b1f 0%, #0d1535 100%) !important;
  border-right: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] > div { padding-top: 0 !important; }
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stRadio label span { color: #94a3b8 !important; }

/* sidebar radio selected */
[data-testid="stSidebar"] [data-baseweb="radio"] label[data-checked="true"] span,
[data-testid="stSidebar"] [aria-checked="true"] span { color: white !important; }

/* ── Headings ── */
h1,h2,h3,h4 {
  font-family: 'Playfair Display', serif !important;
  color: #f1f5f9 !important;
  letter-spacing: -0.02em;
}

/* ── Page title ── */
.page-title {
  font-family: 'Playfair Display', serif;
  font-size: 2rem;
  font-weight: 800;
  color: #f1f5f9;
  margin-bottom: 0.25rem;
}
.page-subtitle {
  font-size: 0.9rem;
  color: var(--muted);
  margin-bottom: 2rem;
}

/* ── Stat Card ── */
.scard {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 22px 20px;
  text-align: center;
  transition: transform .2s, box-shadow .2s;
  backdrop-filter: blur(12px);
}
.scard:hover { transform: translateY(-3px); box-shadow: 0 12px 40px rgba(0,0,0,.4); }
.scard-num {
  font-size: 2.2rem;
  font-weight: 900;
  background: linear-gradient(135deg, var(--blue), var(--red));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1;
}
.scard-label { font-size: .78rem; color: var(--muted); margin-top: 6px; letter-spacing: .05em; text-transform: uppercase; }

/* ── Glass Card ── */
.glass {
  background: rgba(255,255,255,0.035);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: var(--radius);
  padding: 20px;
  backdrop-filter: blur(20px);
  transition: all .25s ease;
}
.glass:hover {
  border-color: rgba(59,130,246,0.35);
  background: rgba(59,130,246,0.06);
  box-shadow: 0 8px 30px rgba(59,130,246,0.15);
}

/* ── Word Row ── */
.word-row {
  display: flex;
  align-items: center;
  gap: 14px;
  background: rgba(255,255,255,0.025);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px;
  padding: 14px 18px;
  margin-bottom: 8px;
  transition: all .2s;
}
.word-row:hover { border-color: rgba(59,130,246,.3); background: rgba(59,130,246,.05); }

/* ── Badge ── */
.badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: .72rem;
  font-weight: 600;
  letter-spacing: .03em;
}

/* ── Level Bar ── */
.lvbar-wrap { background: rgba(255,255,255,.07); border-radius: 99px; height: 6px; overflow: hidden; }
.lvbar-fill { height: 100%; border-radius: 99px; background: linear-gradient(90deg, var(--blue), var(--red)); transition: width .6s cubic-bezier(.4,0,.2,1); }

/* ── Daily Word Card ── */
.daily-card {
  background: linear-gradient(135deg, #0a1a4a 0%, #1a0a1e 50%, #2a0a0a 100%);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 24px;
  padding: 36px 32px;
  position: relative;
  overflow: hidden;
}
.daily-card::before {
  content: '🇫🇷';
  position: absolute;
  right: 24px;
  top: 20px;
  font-size: 3rem;
  opacity: .15;
}
.daily-card .label { font-size: .75rem; text-transform: uppercase; letter-spacing: .12em; color: #94a3b8; margin-bottom: 14px; }
.daily-card .word  { font-family: 'Playfair Display', serif; font-size: 2.6rem; font-weight: 800; color: #fff; margin-bottom: 8px; }
.daily-card .meaning { font-size: 1.1rem; color: #cbd5e1; margin-bottom: 14px; }
.daily-card .example { font-size: .9rem; color: #94a3b8; font-style: italic; border-left: 3px solid rgba(0,85,164,.6); padding-left: 12px; }

/* ── Flashcard 3D ── */
.fc-scene { perspective: 900px; width: 100%; }
.fc-card  {
  position: relative;
  width: 100%;
  min-height: 260px;
  transform-style: preserve-3d;
  transition: transform .55s cubic-bezier(.4,0,.2,1);
  cursor: pointer;
  border-radius: 24px;
}
.fc-card.flipped { transform: rotateY(180deg); }
.fc-front, .fc-back {
  position: absolute;
  width: 100%;
  min-height: 260px;
  border-radius: 24px;
  backface-visibility: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  text-align: center;
  padding: 40px 32px;
}
.fc-front {
  background: linear-gradient(145deg, #0f2a6e, #1e0a2e);
  border: 1px solid rgba(255,255,255,0.12);
}
.fc-back {
  background: linear-gradient(145deg, #0d3326, #0a2010);
  border: 1px solid rgba(16,185,129,0.25);
  transform: rotateY(180deg);
}

/* ── Quiz ── */
.quiz-q-card {
  background: linear-gradient(145deg, rgba(0,85,164,.15), rgba(0,85,164,.04));
  border: 1px solid rgba(0,85,164,.3);
  border-radius: 20px;
  padding: 36px;
  text-align: center;
  margin-bottom: 24px;
}
.quiz-q-card .q-label { font-size: .8rem; text-transform: uppercase; letter-spacing: .1em; color: var(--muted); margin-bottom: 14px; }
.quiz-q-card .q-word  { font-family: 'Playfair Display', serif; font-size: 2.4rem; font-weight: 800; color: #fff; }

/* ── Achievement ── */
.ach-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  border-radius: 14px;
  margin-bottom: 8px;
  transition: all .2s;
}
.ach-card.unlocked { background: rgba(251,191,36,.06); border: 1px solid rgba(251,191,36,.2); }
.ach-card.locked   { background: rgba(255,255,255,.02); border: 1px solid rgba(255,255,255,.06); opacity: .45; }

/* ── Tabs ── */
[data-baseweb="tab-list"] {
  background: rgba(255,255,255,.03) !important;
  border-radius: 12px !important;
  padding: 4px !important;
  gap: 2px !important;
}
[data-baseweb="tab"] {
  border-radius: 9px !important;
  font-weight: 500 !important;
  color: var(--muted) !important;
  font-size: .9rem !important;
}
[aria-selected="true"][data-baseweb="tab"] {
  background: rgba(59,130,246,.18) !important;
  color: #93c5fd !important;
}

/* ── Buttons ── */
.stButton > button {
  background: linear-gradient(135deg, #0055A4, #003d80) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 10px !important;
  font-weight: 600 !important;
  font-size: .9rem !important;
  padding: .55rem 1.2rem !important;
  transition: all .2s !important;
}
.stButton > button:hover {
  background: linear-gradient(135deg, #0066cc, #0055A4) !important;
  box-shadow: 0 4px 18px rgba(0,85,164,.45) !important;
  transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea {
  background: rgba(255,255,255,.04) !important;
  border: 1px solid rgba(255,255,255,.1) !important;
  border-radius: 10px !important;
  color: #e2e8f8 !important;
  font-family: 'Inter', sans-serif !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
  border-color: rgba(59,130,246,.5) !important;
  box-shadow: 0 0 0 3px rgba(59,130,246,.12) !important;
}
.stSelectbox > div > div {
  background: rgba(255,255,255,.04) !important;
  border: 1px solid rgba(255,255,255,.1) !important;
  border-radius: 10px !important;
  color: #e2e8f8 !important;
}

/* ── Progress bar ── */
.stProgress > div > div { background: linear-gradient(90deg, var(--blue), var(--red)) !important; border-radius: 99px !important; }
.stProgress > div { background: rgba(255,255,255,.06) !important; border-radius: 99px !important; }

/* ── Checkbox ── */
.stCheckbox label span { color: #94a3b8 !important; }

/* ── Form ── */
[data-testid="stForm"] {
  background: rgba(255,255,255,.02);
  border: 1px solid rgba(255,255,255,.06);
  border-radius: 20px;
  padding: 24px;
}

/* ── Divider ── */
hr { border-color: rgba(255,255,255,.07) !important; }

/* ── Toast ── */
[data-testid="stToast"] { border-radius: 12px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,.4); border-radius: 99px; }

/* ── Alert/Info ── */
[data-testid="stAlert"] { border-radius: 12px !important; }

/* ── Metric ── */
[data-testid="stMetricValue"] { color: #f1f5f9 !important; }
[data-testid="stMetricLabel"] { color: var(--muted) !important; }

/* ── Plotly bg ── */
.js-plotly-plot .plotly { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# 헬퍼 HTML 컴포넌트
# ─────────────────────────────────────────
def badge(text: str, category: str = "") -> str:
    color = CAT_COLORS.get(category, "#3b82f6")
    bg    = color + "22"
    return f"<span class='badge' style='background:{bg};color:{color};border:1px solid {color}44;'>{text}</span>"

def section_header(title: str, subtitle: str = ""):
    sub = f"<p class='page-subtitle'>{subtitle}</p>" if subtitle else ""
    st.markdown(f"<p class='page-title'>{title}</p>{sub}", unsafe_allow_html=True)

def divider():
    st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────
# 사이드바
# ─────────────────────────────────────────
def render_sidebar(data: dict):
    with st.sidebar:
        # ── 로고
        st.markdown("""
<div style='padding:28px 20px 16px; text-align:center;'>
  <div style='font-size:2.8rem; line-height:1;'>🇫🇷</div>
  <div style='font-family:"Playfair Display",serif; font-size:1.55rem; font-weight:800;
              color:#f1f5f9; margin-top:8px; letter-spacing:-.02em;'>Mots Clés</div>
  <div style='font-size:.75rem; color:#475569; margin-top:4px; letter-spacing:.08em;'>
    FRENCH LEARNING PLATFORM
  </div>
</div>
""", unsafe_allow_html=True)

        # ── 레벨 위젯
        stats    = data["stats"]
        xp       = stats.get("xp", 0)
        lv_info  = get_level_info(xp)
        lv_num   = lv_info["level"]
        next_xp  = LEVELS.get(lv_num + 1, {}).get("min_xp", xp) if lv_num < 5 else xp
        curr_xp  = LEVELS[lv_num]["min_xp"]
        prog     = min((xp - curr_xp) / max(next_xp - curr_xp, 1), 1.0) if lv_num < 5 else 1.0
        pct      = int(prog * 100)

        st.markdown(f"""
<div style='margin:0 12px 16px; background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.08);
            border-radius:14px; padding:14px 16px;'>
  <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;'>
    <div style='display:flex; align-items:center; gap:8px;'>
      <span style='font-size:1.4rem;'>{lv_info['icon']}</span>
      <div>
        <div style='color:#f1f5f9; font-weight:700; font-size:.9rem;'>{lv_info['name']}</div>
        <div style='color:#475569; font-size:.72rem;'>레벨 {lv_num}</div>
      </div>
    </div>
    <div style='text-align:right;'>
      <div style='color:{lv_info["color"]}; font-weight:800; font-size:1rem;'>{xp}</div>
      <div style='color:#475569; font-size:.72rem;'>XP</div>
    </div>
  </div>
  <div class='lvbar-wrap'><div class='lvbar-fill' style='width:{pct}%;'></div></div>
  <div style='color:#334155; font-size:.68rem; text-align:right; margin-top:5px;'>
    {'🏆 마스터 달성!' if lv_num >= 5 else f'{next_xp - xp} XP까지 레벨업'}
  </div>
</div>
""", unsafe_allow_html=True)

        # ── 메뉴
        menu = st.radio(
            "nav",
            ["🏠  홈", "📖  단어장", "🃏  플래시카드", "🎯  퀴즈 게임",
             "📝  오답노트", "📊  학습 통계", "⭐  즐겨찾기", "🏆  업적"],
            label_visibility="collapsed",
        )

        # ── 하단 빠른 통계
        words     = data["words"]
        memorized = sum(1 for w in words if w.get("memorized"))
        ach_cnt   = len(stats.get("achievements", []))
        st.markdown(f"""
<div style='margin:16px 12px 0; padding-top:16px; border-top:1px solid rgba(255,255,255,.06);'>
  <div style='color:#334155; font-size:.68rem; text-transform:uppercase; letter-spacing:.08em; margin-bottom:10px;'>빠른 통계</div>
  <div style='display:flex; flex-direction:column; gap:7px;'>
    <div style='display:flex; justify-content:space-between; font-size:.83rem;'>
      <span style='color:#64748b;'>📚 등록 단어</span>
      <strong style='color:#e2e8f8;'>{len(words)}</strong>
    </div>
    <div style='display:flex; justify-content:space-between; font-size:.83rem;'>
      <span style='color:#64748b;'>✅ 암기 완료</span>
      <strong style='color:#10b981;'>{memorized}</strong>
    </div>
    <div style='display:flex; justify-content:space-between; font-size:.83rem;'>
      <span style='color:#64748b;'>🏆 업적</span>
      <strong style='color:#fbbf24;'>{ach_cnt}/{len(ACHIEVEMENTS)}</strong>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    return menu

# ─────────────────────────────────────────
# 홈 페이지
# ─────────────────────────────────────────
def page_home(data: dict):
    stats = data["stats"]
    words = data["words"]

    # 오늘의 단어 갱신
    today = str(date.today())
    if words and stats.get("daily_word_date") != today:
        dw = random.choice(words)
        stats["daily_word_date"] = today
        stats["daily_word_id"]   = dw["id"]
        data["stats"] = stats
        save_data(data)

    # 히어로 배너
    st.markdown("""
<div style='text-align:center; padding:40px 0 32px;'>
  <div style='font-size:3.2rem; margin-bottom:12px; line-height:1;'>🇫🇷</div>
  <h1 style='font-family:"Playfair Display",serif; font-size:3rem; font-weight:800;
             background:linear-gradient(135deg,#f1f5f9 0%,#93c5fd 60%,#fca5a5 100%);
             -webkit-background-clip:text; -webkit-text-fill-color:transparent;
             margin:0 0 10px;'>Bienvenue!</h1>
  <p style='color:#64748b; font-size:1rem; margin:0;'>매일 조금씩, 프랑스어를 내 것으로 만들어가세요</p>
</div>
""", unsafe_allow_html=True)

    # 통계 카드
    total_q  = stats.get("total_correct", 0) + stats.get("total_wrong", 0)
    accuracy = round(stats.get("total_correct", 0) / total_q * 100) if total_q > 0 else 0
    memorized= sum(1 for w in words if w.get("memorized"))
    lv_info  = get_level_info(stats.get("xp", 0))

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "📚", str(len(words)), "등록 단어"),
        (c2, "✅", str(memorized),  "암기 완료"),
        (c3, "🎯", f"{accuracy}%",  "퀴즈 정답률"),
        (c4, lv_info["icon"], lv_info["name"], "현재 레벨"),
    ]
    for col, ico, num, lbl in cards:
        with col:
            st.markdown(f"""
<div class='scard'>
  <div style='font-size:1.6rem; margin-bottom:6px;'>{ico}</div>
  <div class='scard-num'>{num}</div>
  <div class='scard-label'>{lbl}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns([3, 2])

    # 오늘의 단어
    with col_l:
        daily_id = stats.get("daily_word_id", "")
        dw = next((w for w in words if w["id"] == daily_id), None) or (words[0] if words else None)
        if dw:
            st.markdown(f"""
<div class='daily-card'>
  <div class='label'>✨ 오늘의 단어 · {today}</div>
  <div class='word'>{dw['french']}</div>
  <div class='meaning'>{dw['korean']}</div>
  <div class='example'>"{dw.get('example','')}"<br>
    <span style='color:#64748b; font-size:.82rem;'>{dw.get('example_kr','')}</span>
  </div>
  <div style='margin-top:16px;'>{badge(dw.get('category',''), dw.get('category',''))}</div>
</div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
<div class='daily-card' style='text-align:center; padding:60px;'>
  <div style='color:#475569;'>단어를 추가하면 오늘의 단어가 표시됩니다.</div>
</div>""", unsafe_allow_html=True)

    # 최근 단어
    with col_r:
        st.markdown("<div style='color:#94a3b8; font-size:.78rem; text-transform:uppercase; letter-spacing:.08em; margin-bottom:12px;'>📝 최근 추가된 단어</div>", unsafe_allow_html=True)
        recent = list(reversed(words[-6:])) if words else []
        if recent:
            for w in recent:
                st.markdown(f"""
<div style='display:flex; align-items:center; gap:10px; padding:10px 14px;
            background:rgba(255,255,255,.025); border:1px solid rgba(255,255,255,.06);
            border-radius:10px; margin-bottom:6px;'>
  <div style='flex:1; min-width:0;'>
    <div style='color:#e2e8f8; font-weight:600; font-size:.9rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;'>{w['french']}</div>
    <div style='color:#64748b; font-size:.78rem;'>{w['korean']}</div>
  </div>
  {badge(w.get('category',''), w.get('category',''))}
</div>""", unsafe_allow_html=True)
        else:
            st.markdown("<div style='color:#475569; font-size:.85rem; padding:20px 0;'>아직 단어가 없습니다.</div>", unsafe_allow_html=True)

        # 업적 미리보기
        if stats.get("achievements"):
            st.markdown("<div style='color:#94a3b8; font-size:.78rem; text-transform:uppercase; letter-spacing:.08em; margin: 20px 0 10px;'>🏅 최근 업적</div>", unsafe_allow_html=True)
            for key in list(reversed(stats["achievements"]))[:3]:
                a = ACHIEVEMENTS.get(key, {})
                st.markdown(f"""
<div style='display:flex; align-items:center; gap:8px; padding:8px 12px;
            background:rgba(251,191,36,.06); border:1px solid rgba(251,191,36,.15);
            border-radius:10px; margin-bottom:5px;'>
  <span style='font-size:1.1rem;'>{a.get('icon','🏅')}</span>
  <div style='font-size:.82rem; color:#fde68a;'>{a.get('name','')}</div>
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# 단어장
# ─────────────────────────────────────────
def page_vocabulary(data: dict):
    section_header("📖 단어장", "나만의 프랑스어 단어를 관리하세요")
    words = data["words"]

    tab1, tab2 = st.tabs(["  📚 단어 목록  ", "  ➕ 단어 추가  "])

    # ── 목록
    with tab1:
        c1, c2 = st.columns([3, 1])
        with c1:
            search = st.text_input("검색어", label_visibility="collapsed", placeholder="🔍  단어 검색 (프랑스어 또는 한국어)…", key="v_search")
        with c2:
            cat = st.selectbox("카테고리 필터", CATEGORIES, label_visibility="collapsed", key="v_cat")

        filtered = words
        if search:
            q = sanitize_text(search, 100).lower()
            filtered = [w for w in words if q in w.get("french","").lower() or q in w.get("korean","").lower()]
        if cat != "전체":
            filtered = [w for w in filtered if w.get("category") == cat]

        st.markdown(f"<div style='color:#475569; font-size:.8rem; margin-bottom:14px;'>총 {len(filtered)}개의 단어</div>", unsafe_allow_html=True)

        if not filtered:
            st.markdown("""
<div style='text-align:center; padding:60px; color:#334155;'>
  <div style='font-size:2.5rem; margin-bottom:12px;'>🔍</div>
  <div>검색 결과가 없습니다.</div>
</div>""", unsafe_allow_html=True)
        else:
            for i, w in enumerate(filtered):
                c1, c2, c3, c4, c5 = st.columns([2.5, 3, 1.5, 1, 1])
                with c1:
                    mem = "✅" if w.get("memorized") else ""
                    st.markdown(f"""
<div>
  <span style='color:#f1f5f9; font-weight:700; font-size:.95rem;'>{w['french']}</span> {mem}<br>
  <span style='font-size:.75rem; margin-top:3px; display:inline-block;'>{badge(w.get('category',''), w.get('category',''))}</span>
</div>""", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"""
<div>
  <span style='color:#cbd5e1; font-size:.9rem;'>{w['korean']}</span><br>
  <span style='color:#475569; font-size:.78rem; font-style:italic;'>{w.get('example','')[:45]}{'…' if len(w.get('example',''))>45 else ''}</span>
</div>""", unsafe_allow_html=True)
                with c3:
                    total_q = w.get("quiz_correct",0) + w.get("quiz_wrong",0)
                    acc = f"{round(w.get('quiz_correct',0)/total_q*100)}%" if total_q else "-"
                    color = "#10b981" if total_q and int(acc[:-1])>=70 else "#f87171" if total_q else "#475569"
                    st.markdown(f"<div style='text-align:center; margin-top:4px;'><span style='color:{color}; font-size:.85rem; font-weight:600;'>🎯 {acc}</span></div>", unsafe_allow_html=True)
                with c4:
                    fav_lbl = "⭐" if w.get("favorited") else "☆"
                    if st.button(fav_lbl, key=f"fav_{w['id']}_{i}"):
                        w["favorited"] = not w.get("favorited", False)
                        data = check_achievements(data)
                        save_data(data); st.rerun()
                with c5:
                    if st.button("🗑️", key=f"del_{w['id']}_{i}"):
                        data["words"] = [x for x in data["words"] if x["id"] != w["id"]]
                        save_data(data); st.rerun()

                st.markdown("<div style='height:1px; background:rgba(255,255,255,.04); margin:4px 0;'></div>", unsafe_allow_html=True)

    # ── 추가 폼
    with tab2:
        st.markdown("<div style='color:#94a3b8; font-size:.85rem; margin-bottom:16px;'>새로운 프랑스어 단어를 나만의 단어장에 추가하세요.</div>", unsafe_allow_html=True)
        with st.form("add_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                nf  = st.text_input("🇫🇷 프랑스어 단어 *", placeholder="예: bonjour")
                nex = st.text_area("📝 예문 (프랑스어)", placeholder="예: Bonjour, comment ça va?", height=90)
            with c2:
                nk  = st.text_input("🇰🇷 한국어 뜻 *", placeholder="예: 안녕하세요")
                nexk= st.text_area("📝 예문 번역 (한국어)", placeholder="예: 안녕하세요, 어떻게 지내세요?", height=90)
            nc = st.selectbox("📂 카테고리", CATEGORIES[1:])
            submitted = st.form_submit_button("✨ 단어 추가하기", use_container_width=True)

            if submitted:
                sf, sk = sanitize_text(nf, 200), sanitize_text(nk, 200)
                sex, sexk = sanitize_text(nex, 500), sanitize_text(nexk, 500)
                ok, err = validate_word_input(sf, sk)
                if not ok:
                    st.error(err)
                else:
                    data["words"].append({
                        "id": str(uuid.uuid4()), "french": sf, "korean": sk,
                        "example": sex, "example_kr": sexk, "category": nc,
                        "favorited": False, "memorized": False,
                        "quiz_correct": 0, "quiz_wrong": 0,
                    })
                    data = check_achievements(data)
                    if save_data(data):
                        st.success(f"✅ '{sf}' 단어가 추가되었습니다!")
                        st.rerun()
                    else:
                        st.error("저장 중 오류가 발생했습니다.")

# ─────────────────────────────────────────
# 플래시카드
# ─────────────────────────────────────────
def page_flashcard(data: dict):
    section_header("🃏 플래시카드", "카드를 뒤집어 한국어 뜻과 예문을 확인하세요")
    words = data["words"]

    if not words:
        st.warning("단어를 먼저 추가해 주세요.")
        return

    c1, c2 = st.columns([2, 1])
    with c1:
        fc_cat = st.selectbox("카테고리", CATEGORIES, key="fc_cat")
    with c2:
        only_mem = st.checkbox("미암기 단어만", value=False)

    pool = words if fc_cat == "전체" else [w for w in words if w.get("category") == fc_cat]
    if only_mem:
        pool = [w for w in pool if not w.get("memorized")]

    if not pool:
        st.info("해당 조건의 단어가 없습니다.")
        return

    # 세션 초기화
    pool_key = f"{fc_cat}_{only_mem}_{len(pool)}"
    if st.session_state.get("fc_pool_key") != pool_key:
        st.session_state.fc_pool_key = pool_key
        st.session_state.fc_idx     = 0
        st.session_state.fc_flipped = False
        order = list(range(len(pool)))
        random.shuffle(order)
        st.session_state.fc_order = order

    idx     = st.session_state.fc_idx % len(pool)
    word    = pool[st.session_state.fc_order[idx]]
    flipped = st.session_state.get("fc_flipped", False)

    # 진행률
    mem_cnt = sum(1 for w in pool if w.get("memorized"))
    st.markdown(f"""
<div style='display:flex; justify-content:space-between; color:#475569; font-size:.8rem; margin-bottom:8px;'>
  <span>카드 {idx+1} / {len(pool)}</span>
  <span>암기 완료 {mem_cnt} / {len(pool)}</span>
</div>""", unsafe_allow_html=True)
    st.progress((idx + 1) / len(pool))
    st.markdown("<br>", unsafe_allow_html=True)

    # 카드 (CSS 3D flip)
    flip_cls = "flipped" if flipped else ""
    if not flipped:
        st.markdown(f"""
<div class='fc-scene'>
  <div class='fc-card {flip_cls}'>
    <div class='fc-front'>
      <div style='color:#64748b; font-size:.8rem; text-transform:uppercase; letter-spacing:.1em; margin-bottom:18px;'>🇫🇷 프랑스어</div>
      <div style='font-family:"Playfair Display",serif; font-size:2.8rem; font-weight:800; color:#f1f5f9; margin-bottom:12px;'>{word['french']}</div>
      <div style='color:#334155; font-size:.85rem; margin-top:12px;'>↓ 뒤집기 버튼을 눌러보세요</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
<div class='fc-scene'>
  <div class='fc-card {flip_cls}'>
    <div class='fc-back'>
      <div style='color:#64748b; font-size:.8rem; text-transform:uppercase; letter-spacing:.1em; margin-bottom:16px;'>🇰🇷 한국어</div>
      <div style='font-size:2rem; font-weight:800; color:#f1f5f9; margin-bottom:14px;'>{word['korean']}</div>
      <div style='color:#94a3b8; font-size:.9rem; font-style:italic; border-left:3px solid rgba(16,185,129,.5); padding-left:12px; text-align:left;'>
        "{word.get('example','')}"<br>
        <span style='color:#64748b; font-size:.82rem;'>{word.get('example_kr','')}</span>
      </div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 컨트롤
    r1c1, r1c2, r1c3, r1c4 = st.columns(4)
    with r1c1:
        if st.button("🔄 뒤집기", use_container_width=True):
            st.session_state.fc_flipped = not flipped; st.rerun()
    with r1c2:
        if st.button("⬅️ 이전", use_container_width=True):
            st.session_state.fc_idx = max(0, st.session_state.fc_idx - 1)
            st.session_state.fc_flipped = False; st.rerun()
    with r1c3:
        if st.button("➡️ 다음", use_container_width=True):
            st.session_state.fc_idx += 1
            st.session_state.fc_flipped = False; st.rerun()
    with r1c4:
        mem_lbl = "↩️ 암기 취소" if word.get("memorized") else "✅ 암기 완료"
        if st.button(mem_lbl, use_container_width=True):
            for w in data["words"]:
                if w["id"] == word["id"]:
                    w["memorized"] = not w.get("memorized", False)
            data = check_achievements(data)
            save_data(data); st.rerun()

    if st.button("🔀 카드 섞기", use_container_width=True):
        st.session_state.fc_pool_key = ""  # 강제 초기화
        st.rerun()

# ─────────────────────────────────────────
# 퀴즈
# ─────────────────────────────────────────
def page_quiz(data: dict):
    section_header("🎯 퀴즈 게임", "프랑스어 단어를 맞혀 XP와 레벨을 올려보세요")
    words = data["words"]

    if len(words) < 4:
        st.warning("퀴즈를 진행하려면 최소 4개의 단어가 필요합니다.")
        return

    if not st.session_state.get("quiz_active"):
        _quiz_start_screen(data, words)
    else:
        _quiz_question(data)

def _quiz_start_screen(data, words):
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("""
<div style='background:linear-gradient(145deg,rgba(0,85,164,.2),rgba(239,65,53,.1));
            border:1px solid rgba(0,85,164,.3); border-radius:20px; padding:40px 24px; text-align:center;'>
  <div style='font-size:3.5rem;'>🎯</div>
  <div style='font-family:"Playfair Display",serif; font-size:1.4rem; color:#f1f5f9; margin:12px 0 6px;'>퀴즈 시작</div>
  <div style='color:#64748b; font-size:.85rem;'>4지선다 객관식</div>
</div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("<div style='font-size:.85rem; color:#94a3b8; margin-bottom:16px;'>퀴즈 설정</div>", unsafe_allow_html=True)
        q_cat   = st.selectbox("카테고리", CATEGORIES)
        q_cnt   = st.select_slider("문제 수", [5, 10, 15, 20], value=10)
        q_type  = st.radio("퀴즈 유형", ["🇫🇷 프랑스어 → 한국어", "🇰🇷 한국어 → 프랑스어"], horizontal=True)
        if st.button("🚀 퀴즈 시작!", use_container_width=True):
            pool = words if q_cat == "전체" else [w for w in words if w.get("category") == q_cat]
            if len(pool) < 4:
                st.error("해당 카테고리에 단어가 4개 이상 필요합니다.")
            else:
                quiz_ws = random.sample(pool, min(q_cnt, len(pool)))
                st.session_state.update({
                    "quiz_active": True, "quiz_words": quiz_ws,
                    "quiz_index": 0, "quiz_score": 0,
                    "quiz_answered": False, "quiz_selected": None,
                    "quiz_type": q_type, "quiz_all_words": words,
                    "quiz_wrong_words": [],
                })
                st.rerun()

def _quiz_question(data):
    quiz_ws = st.session_state.quiz_words
    idx     = st.session_state.quiz_index
    total   = len(quiz_ws)

    # 완료 화면
    if idx >= total:
        score = st.session_state.quiz_score
        pct   = round(score / total * 100)
        grade = "🏆" if pct >= 90 else "🎉" if pct >= 70 else "📊"
        msg   = "완벽해요!" if pct >= 90 else "잘 했어요!" if pct >= 70 else "조금 더 연습해봐요!"

        st.markdown(f"""
<div style='text-align:center; padding:40px 20px;'>
  <div style='font-size:4rem; margin-bottom:16px;'>{grade}</div>
  <div style='font-family:"Playfair Display",serif; font-size:2rem; color:#f1f5f9; margin-bottom:6px;'>퀴즈 완료!</div>
  <div style='color:#64748b; margin-bottom:24px;'>{msg}</div>
  <div style='display:flex; justify-content:center; gap:32px; margin-bottom:32px;'>
    <div style='text-align:center;'>
      <div style='font-size:2.5rem; font-weight:900;
                  background:linear-gradient(135deg,#0055A4,#EF4135);
                  -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>{pct}%</div>
      <div style='color:#64748b; font-size:.8rem;'>정답률</div>
    </div>
    <div style='text-align:center;'>
      <div style='font-size:2.5rem; font-weight:900; color:#10b981;'>{score}</div>
      <div style='color:#64748b; font-size:.8rem;'>정답</div>
    </div>
    <div style='text-align:center;'>
      <div style='font-size:2.5rem; font-weight:900; color:#f87171;'>{total-score}</div>
      <div style='color:#64748b; font-size:.8rem;'>오답</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

        # 통계 업데이트
        data["stats"]["total_correct"]       = data["stats"].get("total_correct", 0) + score
        data["stats"]["total_wrong"]         = data["stats"].get("total_wrong", 0) + (total - score)
        data["stats"]["total_quiz_sessions"] = data["stats"].get("total_quiz_sessions", 0) + 1
        data["stats"]["xp"]                  = data["stats"].get("xp", 0) + score * 5
        for ww in st.session_state.get("quiz_wrong_words", []):
            for w in data["words"]:
                if w["id"] == ww["id"]:
                    w["quiz_wrong"] = w.get("quiz_wrong", 0) + 1
        data = check_achievements(data)
        save_data(data)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔄 다시 도전", use_container_width=True):
                st.session_state.quiz_active = False; st.rerun()
        with c2:
            if st.button("📝 오답노트 보기", use_container_width=True):
                st.session_state.quiz_active = False
                st.session_state.go_to = "📝  오답노트"; st.rerun()
        return

    # 문제 화면
    word    = quiz_ws[idx]
    q_type  = st.session_state.get("quiz_type", "🇫🇷 프랑스어 → 한국어")
    answered= st.session_state.get("quiz_answered", False)

    # 진행률
    st.markdown(f"""
<div style='display:flex; justify-content:space-between; color:#475569; font-size:.8rem; margin-bottom:8px;'>
  <span>문제 {idx+1} / {total}</span>
  <span>점수 {st.session_state.quiz_score}점 &nbsp;|&nbsp; +{st.session_state.quiz_score * 5} XP</span>
</div>""", unsafe_allow_html=True)
    st.progress((idx + 1) / total)
    st.markdown("<br>", unsafe_allow_html=True)

    # 문제 카드
    question = word["french"] if "프랑스어 →" in q_type else word["korean"]
    st.markdown(f"""
<div class='quiz-q-card'>
  <div class='q-label'>다음 단어의 뜻은 무엇일까요?</div>
  <div class='q-word'>{question}</div>
</div>""", unsafe_allow_html=True)

    # 보기
    opt_key = f"opts_{idx}"
    cor_key = f"corr_{idx}"
    if opt_key not in st.session_state:
        correct    = word["korean"] if "프랑스어 →" in q_type else word["french"]
        wrong_pool = [w for w in st.session_state.quiz_all_words if w["id"] != word["id"]]
        wrongs     = random.sample(wrong_pool, min(3, len(wrong_pool)))
        if "프랑스어 →" in q_type:
            opts = [correct] + [w["korean"] for w in wrongs]
        else:
            opts = [correct] + [w["french"] for w in wrongs]
        random.shuffle(opts)
        st.session_state[opt_key] = opts
        st.session_state[cor_key] = correct

    opts    = st.session_state[opt_key]
    correct = st.session_state[cor_key]
    labels  = ["①", "②", "③", "④"]

    if answered:
        for li, opt in zip(labels, opts):
            if opt == correct:
                bg, bc, fc = "rgba(16,185,129,.15)", "#10b981", "#6ee7b7"
                icon = "✓"
            elif opt == st.session_state.get("quiz_selected"):
                bg, bc, fc = "rgba(248,113,113,.15)", "#f87171", "#fca5a5"
                icon = "✗"
            else:
                bg, bc, fc = "rgba(255,255,255,.03)", "rgba(255,255,255,.08)", "#64748b"
                icon = li
            st.markdown(f"""
<div style='background:{bg}; border:1.5px solid {bc}; border-radius:12px;
            padding:14px 20px; margin-bottom:8px; display:flex; align-items:center; gap:12px;'>
  <span style='color:{fc}; font-weight:700; width:22px;'>{icon}</span>
  <span style='color:{fc}; font-size:.95rem;'>{opt}</span>
</div>""", unsafe_allow_html=True)

        sel = st.session_state.get("quiz_selected")
        if sel == correct:
            st.markdown("<div style='color:#10b981; font-weight:700; font-size:1.05rem; margin:12px 0;'>🎉 정답입니다! +5 XP</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='color:#f87171; font-weight:700; font-size:1.05rem; margin:12px 0;'>❌ 오답! 정답: <span style='color:#6ee7b7;'>{correct}</span></div>", unsafe_allow_html=True)
        if st.button("다음 문제 ➡️", use_container_width=True):
            st.session_state.quiz_index   += 1
            st.session_state.quiz_answered = False
            st.session_state.quiz_selected = None
            st.rerun()
    else:
        for li, opt in zip(labels, opts):
            if st.button(f"{li}  {opt}", key=f"qopt_{idx}_{opt}", use_container_width=True):
                st.session_state.quiz_answered = True
                st.session_state.quiz_selected = opt
                if opt == correct:
                    st.session_state.quiz_score += 1
                    for w in data["words"]:
                        if w["id"] == word["id"]:
                            w["quiz_correct"] = w.get("quiz_correct", 0) + 1
                else:
                    if not any(ww["id"] == word["id"] for ww in st.session_state.get("quiz_wrong_words", [])):
                        st.session_state.setdefault("quiz_wrong_words", []).append(word)
                    for w in data["words"]:
                        if w["id"] == word["id"]:
                            w["quiz_wrong"] = w.get("quiz_wrong", 0) + 1
                save_data(data)
                st.rerun()

# ─────────────────────────────────────────
# 오답노트
# ─────────────────────────────────────────
def page_wrong_notes(data: dict):
    section_header("📝 오답노트", "자주 틀리는 단어를 집중적으로 학습하세요")
    words = data["words"]
    wrong = sorted([w for w in words if w.get("quiz_wrong", 0) > 0],
                   key=lambda x: x.get("quiz_wrong", 0), reverse=True)

    if not wrong:
        st.markdown("""
<div style='text-align:center; padding:80px 0; color:#334155;'>
  <div style='font-size:3rem; margin-bottom:16px;'>📝</div>
  <div style='font-size:1.1rem; color:#475569;'>아직 오답 기록이 없습니다.</div>
  <div style='font-size:.85rem; margin-top:8px; color:#334155;'>퀴즈를 풀면 틀린 단어가 여기에 저장됩니다.</div>
</div>""", unsafe_allow_html=True)
        return

    st.markdown(f"<div style='color:#475569; font-size:.8rem; margin-bottom:16px;'>오답 단어 {len(wrong)}개</div>", unsafe_allow_html=True)

    for w in wrong:
        wc = w.get("quiz_wrong", 0)
        cc = w.get("quiz_correct", 0)
        tot = wc + cc
        acc = round(cc / tot * 100) if tot else 0
        bar_color = "#10b981" if acc >= 70 else "#f87171"
        bar_w = acc

        st.markdown(f"""
<div class='glass' style='margin-bottom:10px; padding:18px 22px;'>
  <div style='display:flex; justify-content:space-between; align-items:flex-start; gap:16px;'>
    <div style='flex:1;'>
      <div style='display:flex; align-items:center; gap:10px; margin-bottom:4px;'>
        <span style='font-size:1.05rem; font-weight:700; color:#f1f5f9;'>{w['french']}</span>
        {badge(w.get('category',''), w.get('category',''))}
      </div>
      <div style='color:#94a3b8; font-size:.88rem; margin-bottom:6px;'>{w['korean']}</div>
      <div style='color:#475569; font-size:.78rem; font-style:italic;'>{w.get('example','')}</div>
    </div>
    <div style='text-align:right; flex-shrink:0;'>
      <div style='color:#f87171; font-weight:700; font-size:.9rem;'>❌ {wc}번 틀림</div>
      <div style='color:#10b981; font-size:.78rem; margin-top:2px;'>✅ {cc}번 정답</div>
      <div style='color:{bar_color}; font-size:.78rem; margin-top:2px;'>정답률 {acc}%</div>
      <div style='width:80px; background:rgba(255,255,255,.07); border-radius:99px; height:4px; margin-top:6px; margin-left:auto;'>
        <div style='width:{bar_w}%; height:4px; background:{bar_color}; border-radius:99px;'></div>
      </div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if len(wrong) >= 4:
        if st.button("🔄 오답만 다시 풀기", use_container_width=True):
            st.session_state.update({
                "quiz_active": True, "quiz_words": wrong[:20],
                "quiz_index": 0, "quiz_score": 0,
                "quiz_answered": False, "quiz_selected": None,
                "quiz_type": "🇫🇷 프랑스어 → 한국어",
                "quiz_all_words": words, "quiz_wrong_words": [],
            })
            st.session_state.go_to = "🎯  퀴즈 게임"
            st.rerun()
    else:
        st.info("오답만 다시 풀기는 4개 이상의 오답 단어가 필요합니다.")

# ─────────────────────────────────────────
# 학습 통계
# ─────────────────────────────────────────
def page_stats(data: dict):
    section_header("📊 학습 통계", "나의 학습 현황을 한눈에 확인하세요")
    stats = data["stats"]
    words = data["words"]

    total_q  = stats.get("total_correct", 0) + stats.get("total_wrong", 0)
    accuracy = round(stats.get("total_correct", 0) / total_q * 100) if total_q > 0 else 0
    memorized= sum(1 for w in words if w.get("memorized"))
    xp       = stats.get("xp", 0)
    sessions = stats.get("total_quiz_sessions", 0)

    c1,c2,c3,c4,c5 = st.columns(5)
    for col, ico, val, lbl in [
        (c1,"📚",str(len(words)),"등록 단어"),
        (c2,"✅",str(memorized),"암기 완료"),
        (c3,"🎯",f"{accuracy}%","퀴즈 정답률"),
        (c4,"⚡",str(xp),"총 XP"),
        (c5,"🎮",str(sessions),"퀴즈 세션"),
    ]:
        with col:
            st.markdown(f"""
<div class='scard'>
  <div style='font-size:1.4rem; margin-bottom:6px;'>{ico}</div>
  <div class='scard-num'>{val}</div>
  <div class='scard-label'>{lbl}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    cl, cr = st.columns(2)

    # 카테고리 도넛 차트
    with cl:
        if words:
            cat_c = {}
            for w in words:
                c = w.get("category","기타")
                cat_c[c] = cat_c.get(c, 0) + 1
            colors = ["#0055A4","#EF4135","#ffffff","#3b82f6","#8b5cf6","#f59e0b","#10b981"]
            fig = go.Figure(go.Pie(
                labels=list(cat_c.keys()), values=list(cat_c.values()),
                hole=.5, marker=dict(colors=colors[:len(cat_c)]),
                textfont=dict(color="white"),
            ))
            fig.update_layout(
                title=dict(text="카테고리별 단어 분포", font=dict(color="#94a3b8", size=13)),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"), legend=dict(font=dict(color="#94a3b8")),
                margin=dict(t=50,b=10,l=10,r=10), height=280,
            )
            st.plotly_chart(fig, use_container_width=True)

    # 정답/오답 게이지
    with cr:
        if total_q > 0:
            fig2 = go.Figure(go.Bar(
                x=["정답", "오답"],
                y=[stats.get("total_correct",0), stats.get("total_wrong",0)],
                marker_color=["#10b981","#f87171"],
                text=[stats.get("total_correct",0), stats.get("total_wrong",0)],
                textposition="auto", textfont=dict(color="white"),
            ))
            fig2.update_layout(
                title=dict(text="퀴즈 정답 vs 오답", font=dict(color="#94a3b8", size=13)),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
                xaxis=dict(gridcolor="rgba(255,255,255,.05)"),
                yaxis=dict(gridcolor="rgba(255,255,255,.05)"),
                showlegend=False, margin=dict(t=50,b=10,l=10,r=10), height=280,
            )
            st.plotly_chart(fig2, use_container_width=True)

    divider()

    # 암기 진행률 카테고리별
    st.markdown("<div style='color:#94a3b8; font-size:.85rem; margin-bottom:14px;'>📈 카테고리별 암기 진행률</div>", unsafe_allow_html=True)
    cats = [c for c in CATEGORIES[1:] if any(w.get("category")==c for w in words)]
    if cats:
        for cat in cats:
            cat_ws = [w for w in words if w.get("category")==cat]
            mem_c  = sum(1 for w in cat_ws if w.get("memorized"))
            pct    = round(mem_c/len(cat_ws)*100) if cat_ws else 0
            color  = CAT_COLORS.get(cat, "#3b82f6")
            st.markdown(f"""
<div style='margin-bottom:10px;'>
  <div style='display:flex; justify-content:space-between; font-size:.82rem; margin-bottom:5px;'>
    <span>{badge(cat, cat)} &nbsp;<span style='color:#64748b;'>{mem_c}/{len(cat_ws)}</span></span>
    <span style='color:{color}; font-weight:600;'>{pct}%</span>
  </div>
  <div style='background:rgba(255,255,255,.06); border-radius:99px; height:6px;'>
    <div style='width:{pct}%; height:6px; background:{color}; border-radius:99px; transition:width .6s;'></div>
  </div>
</div>""", unsafe_allow_html=True)

    divider()

    # 자주 틀리는 TOP 5
    st.markdown("<div style='color:#94a3b8; font-size:.85rem; margin-bottom:14px;'>📉 자주 틀리는 단어 TOP 5</div>", unsafe_allow_html=True)
    hard = sorted([w for w in words if w.get("quiz_wrong",0)>0],
                  key=lambda x: x.get("quiz_wrong",0), reverse=True)[:5]
    if hard:
        for i,w in enumerate(hard):
            st.markdown(f"""
<div style='display:flex; align-items:center; gap:12px; background:rgba(248,113,113,.05);
            border:1px solid rgba(248,113,113,.12); border-radius:10px; padding:10px 16px; margin-bottom:6px;'>
  <span style='color:#f87171; font-weight:800; font-size:1rem; width:22px;'>#{i+1}</span>
  <div style='flex:1;'>
    <span style='color:#f1f5f9; font-weight:600;'>{w['french']}</span>
    <span style='color:#64748b; font-size:.85rem; margin-left:8px;'>{w['korean']}</span>
  </div>
  <span style='color:#f87171; font-weight:700; font-size:.85rem;'>❌ {w.get('quiz_wrong',0)}번</span>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div style='color:#334155; font-size:.85rem;'>오답 데이터가 없습니다. 퀴즈를 먼저 풀어보세요!</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────
# 즐겨찾기
# ─────────────────────────────────────────
def page_favorites(data: dict):
    section_header("⭐ 즐겨찾기", "중요한 단어를 모아 빠르게 복습하세요")
    words = data["words"]
    favs  = [w for w in words if w.get("favorited")]

    if not favs:
        st.markdown("""
<div style='text-align:center; padding:80px 0; color:#334155;'>
  <div style='font-size:3rem; margin-bottom:16px;'>⭐</div>
  <div style='font-size:1.1rem; color:#475569;'>즐겨찾기한 단어가 없습니다.</div>
  <div style='font-size:.85rem; margin-top:8px; color:#334155;'>단어장에서 ☆ 버튼을 눌러 추가하세요.</div>
</div>""", unsafe_allow_html=True)
        return

    st.markdown(f"<div style='color:#475569; font-size:.8rem; margin-bottom:16px;'>즐겨찾기 {len(favs)}개</div>", unsafe_allow_html=True)

    for w in favs:
        c1, c2 = st.columns([6, 1])
        with c1:
            st.markdown(f"""
<div class='glass' style='padding:18px 20px;'>
  <div style='display:flex; align-items:flex-start; gap:14px;'>
    <span style='font-size:1.4rem; margin-top:2px;'>⭐</span>
    <div style='flex:1;'>
      <div style='display:flex; align-items:center; gap:8px; margin-bottom:4px;'>
        <span style='font-weight:700; color:#f1f5f9; font-size:1rem;'>{w['french']}</span>
        {badge(w.get('category',''), w.get('category',''))}
      </div>
      <div style='color:#94a3b8; font-size:.88rem; margin-bottom:5px;'>{w['korean']}</div>
      <div style='color:#475569; font-size:.78rem; font-style:italic;'>" {w.get('example','')} "</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)
        with c2:
            if st.button("제거", key=f"unfav_{w['id']}"):
                for x in data["words"]:
                    if x["id"] == w["id"]:
                        x["favorited"] = False
                save_data(data); st.rerun()

# ─────────────────────────────────────────
# 업적
# ─────────────────────────────────────────
def page_achievements(data: dict):
    section_header("🏆 업적", "학습 목표를 달성하고 XP를 획득하세요")
    achieved = data["stats"].get("achievements", [])
    total    = len(ACHIEVEMENTS)
    done     = len(achieved)

    # 진행 배너
    pct = round(done/total*100)
    st.markdown(f"""
<div style='background:linear-gradient(135deg,rgba(251,191,36,.08),rgba(251,191,36,.02));
            border:1px solid rgba(251,191,36,.15); border-radius:20px;
            padding:28px 32px; margin-bottom:24px;'>
  <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;'>
    <div>
      <div style='font-size:1.5rem; font-weight:800; color:#fde68a;'>{done} / {total} 업적</div>
      <div style='color:#92400e; font-size:.82rem; margin-top:2px;'>총 XP: {sum(ACHIEVEMENTS[k]["xp"] for k in achieved)} / {sum(a["xp"] for a in ACHIEVEMENTS.values())}</div>
    </div>
    <div style='font-size:2.5rem;'>🏆</div>
  </div>
  <div style='background:rgba(255,255,255,.07); border-radius:99px; height:8px;'>
    <div style='width:{pct}%; height:8px; background:linear-gradient(90deg,#fbbf24,#f59e0b); border-radius:99px;'></div>
  </div>
  <div style='color:#92400e; font-size:.72rem; margin-top:6px; text-align:right;'>{pct}% 달성</div>
</div>""", unsafe_allow_html=True)

    # 업적 목록
    for key, ach in ACHIEVEMENTS.items():
        unlocked = key in achieved
        cls      = "unlocked" if unlocked else "locked"
        xp_badge = f"<span style='color:#fbbf24; font-weight:700;'>+{ach['xp']} XP</span>"
        status   = "<span style='color:#10b981; font-size:.82rem;'>✅ 달성</span>" if unlocked else "<span style='color:#334155; font-size:.82rem;'>🔒 미달성</span>"

        st.markdown(f"""
<div class='ach-card {cls}'>
  <span style='font-size:2rem;'>{ach['icon']}</span>
  <div style='flex:1;'>
    <div style='color:#{"fde68a" if unlocked else "475569"}; font-weight:700; font-size:.95rem;'>{ach['name']}</div>
    <div style='color:#{"94a3b8" if unlocked else "334155"}; font-size:.78rem; margin-top:2px;'>{ach['desc']}</div>
  </div>
  <div style='text-align:right;'>
    {xp_badge}
    <div style='margin-top:4px;'>{status}</div>
  </div>
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# 메인
# ─────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="Mots Clés — 프랑스어 학습",
        page_icon="🇫🇷",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_css()

    data = load_data()
    menu = render_sidebar(data)

    # 페이지 이동 오버라이드
    if "go_to" in st.session_state:
        menu = st.session_state.pop("go_to")

    if   "홈"       in menu: page_home(data)
    elif "단어장"   in menu: page_vocabulary(data)
    elif "플래시카드" in menu: page_flashcard(data)
    elif "퀴즈"     in menu: page_quiz(data)
    elif "오답노트" in menu: page_wrong_notes(data)
    elif "통계"     in menu: page_stats(data)
    elif "즐겨찾기" in menu: page_favorites(data)
    elif "업적"     in menu: page_achievements(data)

if __name__ == "__main__":
    main()
