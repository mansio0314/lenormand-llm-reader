from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.llm_client import LLMClient
from services.spread_engine import SpreadEngine
from services.translation_client import TranslationClient
from services.notes_repository import NotesRepository


BASE_DIR = Path(__file__).resolve().parent.parent

cards_path = BASE_DIR / "data" / "cards.json"
spreads_path = BASE_DIR / "data" / "spreads.json"
notes_path = BASE_DIR / "data" / "lenormand_notes.txt"

spread_engine = SpreadEngine(cards_path=cards_path, spreads_path=spreads_path)
llm_client = LLMClient()
translation_client = TranslationClient()
notes_repo = NotesRepository(notes_path=notes_path)


router = APIRouter(prefix="/api", tags=["reading"])


class ReadingRequest(BaseModel):
    question_ko: str = Field(..., description="사용자 질문 (한국어)")
    category: Optional[str] = Field(None, description="love/career/finance/self 등 카테고리")
    spread_type: str = Field(..., description="스프레드 종류 id")


class CardPosition(BaseModel):
    card_id: int
    position_key: Optional[str]
    position_label_en: Optional[str]
    position_label_ko: Optional[str]
    row: Optional[int]
    column: Optional[int]
    name_en: Optional[str]
    name_ko: Optional[str]
    interpretation_en: Optional[str] = None
    interpretation_ko: Optional[str] = None
    reader_note: Optional[str] = None


class ReadingResponse(BaseModel):
    reading_en: Dict[str, Any]
    reading_ko: Dict[str, Any]
    cards: List[CardPosition]
    spread_type: str


@router.post("/reading", response_model=ReadingResponse)
async def create_reading(payload: ReadingRequest) -> ReadingResponse:
    spread = spread_engine.get_spread(payload.spread_type)
    if not spread:
        raise HTTPException(status_code=404, detail="Unknown spread_type")

    spread_result = spread_engine.shuffle_and_draw(payload.spread_type)
    for card in spread_result["cards"]:
        name_en = card.get("name_en")
        note = notes_repo.get_block(name_en)
        if note:
            card["reader_note"] = note
        
    question_en = translation_client.translate(payload.question_ko, target_lang="en")

    prompt = llm_client.build_prompt(
        question_en=question_en,
        category=payload.category,
        spread_type=payload.spread_type,
        cards=spread_result["cards"],
    )

    reading_en = llm_client.generate_reading(prompt=prompt, spread_type=payload.spread_type)
    reading_ko = translation_client.translate_reading(reading_en)

    return ReadingResponse(
        reading_en=reading_en,
        reading_ko=reading_ko,
        cards=spread_result["cards"],
        spread_type=payload.spread_type,
    )
