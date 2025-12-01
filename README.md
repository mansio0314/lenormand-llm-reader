
# 🎴 Lenormand LLM Reader (FastAPI + Next.js)

*A bilingual Lenormand reading service prototype powered by an LLM.*


<p align="center">
  <em>⚠️ The preview image above is a temporary placeholder. It may use artwork with unclear copyright status and is NOT intended for redistribution. Will be replaced with original assets later.</em>
</p>

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/Next.js-Frontend-000000?style=for-the-badge&logo=next.js" />
  <img src="https://img.shields.io/badge/TypeScript-4.x-3178C6?style=for-the-badge&logo=typescript" />
  <img src="https://img.shields.io/badge/LLM-OpenAI_mock-412991?style=for-the-badge&logo=openai" />
</p>

---

## ✨ Overview

**Lenormand LLM Reader** is a prototype stack for a **bilingual Lenormand reading service**:

- **FastAPI** backend  
  - Handles spread logic, shuffling, basic request/response models  
  - Provides stubs for LLM + translation services  
- **Next.js** frontend  
  - Minimal UI to send a question, choose a spread, and render results  

The goal is to model the **end-to-end flow** of:

> “Korean question → spread selection → card sampling → LLM reading (EN) → translated reading (KO)”

…while keeping all LLM / translation bits swappable.

---

## 📂 Project Structure

현재 리포 폴더 기준으로 실제 구조를 반영한 프로젝트 개요:

```text
lenormand-llm-reader/
│
├── main.py               # FastAPI app bootstrap & router include
│
├── api/
│   └── reading.py        # /api/reading endpoint, Pydantic models, wiring
│
├── services/             # Pluggable service layer
│   ├── llm_client.py         # Prompt builder + mock LLM response
│   ├── translation_client.py # Mock translator (ko <-> en)
│   └── spread_engine.py      # Loads spreads/cards, shuffles, assigns positions
│
├── data/                 # JSON templates (deck & spreads)
│   ├── cards.json            # Keys 1..36 prepared for Lenormand metadata
│   └── spreads.json          # Past–Present–Future, SOA, 3x3 box, Grand Tableau
│   # (ignored) lenormand_notes.txt - personal notes, excluded via .gitignore
│
├── pages/                # Next.js pages
│   ├── index.tsx             # Landing / entry page
│   └── reading.tsx           # Reading request + result rendering
│
├── components/           # Frontend building blocks
│   ├── SpreadSelector.tsx    # Choose spread type
│   ├── CardView.tsx          # Individual card view
│   └── ResultView.tsx        # LLM reading display
│
├── static/               # Static assets (preview images, etc.)
│   └── cards/                # Card artwork (ignored by git)
│
├── templates/            # (Optional) HTML templates for manual testing
│
├── test_spread.py        # Quick Python-side sanity tests for spread_engine
│
├── .gitignore            # venv/.env, static/cards, data/lenormand_notes, tools/…
└── README.md
````

> 🔒 **Privacy / Safety Note (.gitignore)**
>
> * `static/cards/*` → card images that might have copyright issues
> * `data/lenormand_notes.txt` → personal reading notes
> * `tools/` → local helpers, experiments
> * `.env`, `.env*`, `venv/` → secrets & local environment
>
> 이 리포는 실제 배포용이 아니라, **구조/흐름을 보여주는 프로토타입**입니다.

---

## 🧠 Backend: FastAPI

### 1. Create a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 2. Install backend dependencies

(최소 예시. 실제로는 `requirements.txt`로 관리하는 것을 권장)

```bash
pip install fastapi uvicorn
# plus: pydantic, httpx, etc. depending on your implementation
```

### 3. Run the server

```bash
uvicorn main:app --reload
```

* Health check: `GET http://localhost:8000/health`
* Reading API: `POST http://localhost:8000/api/reading`

### Example Request

```json
{
  "question_ko": "올해 커리어 방향은?",
  "category": "career",
  "spread_type": "past_present_future"
}
```

### Example Response Shape

```json
{
  "reading_en": {
    "summary_en": "...",
    "overall_story_en": "...",
    "action_items_en": []
  },
  "reading_ko": {
    "summary_ko": "...",
    "overall_story_ko": "...",
    "action_items_ko": []
  },
  "cards": [
    {
      "card_id": 1,
      "position_label_en": "Past",
      "row": 1,
      "column": 1
    }
  ],
  "spread_type": "past_present_future"
}
```

> 👉 In this prototype, `LLMClient` and `TranslationClient` return mocked responses.
> For a real deployment, plug in actual providers (OpenAI, NLLB, etc.) and secrets via `.env`.

---

## 🖼 Frontend: Next.js

```bash
npm install
npm run dev
```

By default, the frontend expects the API at:

```text
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

* `/reading` page posts to `POST /api/reading`
* Renders:

  * Selected spread
  * Card positions
  * `reading_en` / `reading_ko` blocks

---

## 📦 Data Templates

* `data/cards.json`

  * keys `1..36`
  * structure ready for:

    * names (EN/KR)
    * domain-specific keywords
    * interpretive text

* `data/spreads.json`

  * definitions for:

    * Past–Present–Future
    * Situation–Obstacle–Advice
    * 3×3 Box
    * Grand Tableau (8×4+4)

이 JSON 설계는 나중에 **LLM 프롬프트용 RAG 컨텍스트**로 확장하기 쉽게 구성되어 있습니다.

---

## 🧪 Manual Test (Backend-only)

1. Start backend:

```bash
uvicorn main:app --reload
```

2. POST to:

```text
http://localhost:8000/api/reading
```

with:

```json
{
  "question_ko": "지금 취업 준비 방향이 맞는지 알고 싶어요",
  "category": "career",
  "spread_type": "past_present_future"
}
```

3. Expect:

* HTTP 200
* `reading_en.summary_en` populated in English (mock)
* `reading_ko.summary_ko` populated in Korean (mock)
* `cards` + `spread_type` echoed back according to `spread_engine` logic

---

## 🖼 Image Assets & Copyright

> ⚠️ **Important notice**

* Some images under `static/` (especially card-like artwork) are **temporary placeholders**.
* 원본 출처의 저작권 상태가 명확하지 않을 수 있으며,
  **상업적/공개 배포용으로 사용하면 안 됩니다.**
* 실제 배포 시에는:

  * 직접 제작한 일러스트
  * 상업적 사용이 허용된 에셋
  * 또는 완전히 텍스트 기반 UI
    중 하나로 교체해야 합니다.

---

## 🔮 Roadmap / Ideas

* Integrate real LLM + translation APIs
* Fill `cards.json` with full Lenormand metadata (EN/KR)
* Add persistent reading history
* Add user profiles & rate limiting
* Replace placeholder art with original, copyright-safe illustrations

---

## 👤 About

Built as a personal exploration into:

* LLM-backed **symbolic systems** (Lenormand)
* **Backend–Frontend** separation with FastAPI & Next.js
* Designing JSON schemas for card-based RAG-style prompts

Author: **따옴표**
LLM collaborator: **Rico**

---

## 🃏 Additional Reading Mode: Single-Card (YES/NO/MAYBE)

레노먼드의 강점 중 하나는 **단일 카드로도 간단한 YES/NO/MAYBE 판정을 할 수 있다는 점**입니다.  
본 프로젝트에서는 이 장점을 활용하기 위해 **Single-Card Draw** 모드를 지원합니다.

### 🔍 Why Single-Card Mode?
- 즉각적인 직관적 답변 제공  
- 사용자의 짧은 질문에도 빠르게 대응 가능  
- 상담/리딩 상황에서 “빠른 1차 가이드”로 활용 가능  
- 장문의 스프레드 이전에 *초기 방향성* 제시 가능  

### ✔️ YES/NO/MAYBE 예시 (Realistic Lenormand Style)

아래 예시는 실제 레노먼드 해석 흐름에 맞춘 간단한 판정 스타일입니다.  
(LLM 해석과 사람 리더의 직관을 결합해 사용할 수 있는 구조로 기획되었습니다.)

| Card | Interpretation | Verdict |
|------|----------------|---------|
| **Sun** ☀️ | 성공, 명확성, 긍정, 활력 | **YES** |
| **Clover** 🍀 | 예상외의 기회, 가벼운 행운 | **YES (light)** |
| **Rider** 🏇 | 변화의 시작, 방문, 메시지 | **Maybe → 상황 더 필요** |
| **Clouds** ☁️ | 혼란, 불확실성, 흐림 | **MAYBE/NO** |
| **Mountain** ⛰ | 지연, 장애물, 단단한 벽 | **NO** |
| **Coffin** ⚰️ | 종료, 마무리, 침체 | **NO** |

### ✔ Example Output  
**Question:**  
“제가 준비한 포트폴리오가 이번 주에 좋은 결과를 가져올까요?”

**Card Drawn:** *Sun*

**Quick Interpretation:**  
긍정적 결과가 기대되며 흐름이 당신에게 유리하게 작용할 가능성이 큽니다.

**Verdict:** **YES**

---

## 💬 Hybrid Reading Concept (Human + LLM)

본 프로젝트는 단순 LLM 자동화 리딩이 아니라,  
**“사람 리더의 해석 + LLM의 텍스트 생성 능력”을 결합하는 모델**을 목표로 기획되었습니다.

### 🔎 기획 의도
- 상담자가 기존에 하는 리딩 방식과 LLM의 장문 표현력을 결합  
- 단일 카드/소형 스프레드에서는 리더의 판단을 우선  
- 장문 스토리텔링이 필요한 상황에서는 LLM을 보조로 활용  
- 상담자마다 해석 스타일이 다르므로, *노트 파일*을 별도로 두어  
  → **리더 개인의 해석을 LLM 컨텍스트에 자연스럽게 녹이도록 설계**

### 🧠 The Pipeline Supports Hybrid Reading Naturally  
1) 사람이 스프레드를 보고 **핵심 메시지/테마를 먼저 잡음**  
2) `lenormand_notes.txt` 에 자신의 해석 철학을 적재  
3) LLM prompt에 카드 의미 + 개인 노트 + 질문이 함께 들어감  
4) LLM은 **리더의 세계관에 맞춘 리딩 텍스트**를 자동 생성  
5) 상담자는  
   - 빠른 직관(YES/NO)  
   - 자기만의 해석  
   - LLM이 생성한 장문 설명  
   을 조합해서 **최종 리딩을 상담자에게 제공**

→ 즉, 본 프로젝트는 ‘AI가 사람을 대체’하는 구조가 아니라,  
**사람 리더의 해석을 강화하는 지원형 설계(Decision-Augmentation)** 를 중심에 두고 있음.


## 🎯 Why This Matters (As an AI Service Planner / PM)

이 구조는 실제 상담/리딩 서비스에서도 매우 경쟁력 있는 UX입니다.

- 단일 카드 YES/NO → ‘즉각 응답’ 경험 제공  
- Multi-card spread → 심층 리딩 제공  
- Hybrid Reading → 상담자의 전문성 + AI의 언어 능력 결합  
- 개인 노트 기반 RAG → **리더마다 다른 해석 스타일을 반영 가능**  
- 확장성: 상담 기록, 사용자 맞춤 리딩, LLM 페르소나 조정 등으로 확장 용이  

본 설계는 “AI가 기존 해석자/리더의 역량을 강화한다”는 목표를 기반으로 진행되었습니다.
