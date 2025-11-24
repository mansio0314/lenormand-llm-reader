# Lenormand LLM Reader (FastAPI + Next.js)

Prototype stack for a bilingual Lenormand reading service. FastAPI handles spread logic, shuffling, and LLM/translation stubs; Next.js provides a minimal UI to request readings.

## Project Structure
- `main.py` - FastAPI app bootstrap and router include  
- `api/reading.py` - `/api/reading` endpoint, request/response models  
- `services/` - pluggable service stubs  
  - `llm_client.py` - prompt builder + mock LLM response  
  - `translation_client.py` - mock translator  
  - `spread_engine.py` - loads spreads/cards, shuffles, assigns positions  
- `data/` - JSON templates  
  - `cards.json` - keys 1..36, content to be filled  
  - `spreads.json` - 3-card spreads, 3x3 box, Grand Tableau layout  
- `pages/` - Next.js pages (`index.tsx`, `reading.tsx`)  
- `components/` - UI building blocks (`SpreadSelector`, `CardView`, `ResultView`)

## Backend (FastAPI)
```bash
python -m venv .venv
.venv\Scripts\activate
pip install fastapi uvicorn
uvicorn main:app --reload
```

Health check: `GET http://localhost:8000/health`  
Reading: `POST http://localhost:8000/api/reading`

### Request
```json
{
  "question_ko": "올해 커리어 방향은?",
  "category": "career",
  "spread_type": "past_present_future"
}
```

### Response (shape)
```json
{
  "reading_en": { "summary_en": "...", "overall_story_en": "...", "action_items_en": [] },
  "reading_ko": { "summary_ko": "...", "overall_story_ko": "...", "action_items_ko": [] },
  "cards": [ { "card_id": 1, "position_label_en": "Past", "row": 1, "column": 1 } ],
  "spread_type": "past_present_future"
}
```

> Replace `LLMClient` and `TranslationClient` implementations with real providers and enrich `data/cards.json` with actual card metadata.

## Frontend (Next.js)
```bash
npm install
npm run dev
```
Set `NEXT_PUBLIC_API_BASE_URL` (default `http://localhost:8000`) to point to the FastAPI server. The `/reading` page posts to the backend and renders cards and results.

## Data Templates
- `data/cards.json`: keys 1..36 prepared for Lenormand deck metadata (names, keywords, meanings).  
- `data/spreads.json`: definitions for Past-Present-Future, Situation-Obstacle-Advice, 3x3 Box, and Grand Tableau (8x4+4).

## Extending
- Add real translation in `services/translation_client.py`.
- Integrate an LLM provider in `services/llm_client.py`.
- Fill `cards.json` with English/Korean names, keywords per domain, and interpretations per schema.
- Add authentication, rate limiting, and persistence as needed.
