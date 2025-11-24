# services/spread_engine.py

from pathlib import Path
from typing import Dict, Any
import json
import random


class SpreadEngine:
    def __init__(self, cards_path: Path, spreads_path: Path) -> None:
        # cards.json / spreads.json 로딩
        with cards_path.open(encoding="utf-8") as f:
            self.cards: Dict[str, Any] = json.load(f)

        with spreads_path.open(encoding="utf-8") as f:
            data = json.load(f)
            # 네 spreads.json 구조가 {"spreads": {...}} 이니까
            self.spreads: Dict[str, Any] = data["spreads"]

    def get_spread(self, spread_id: str) -> Dict[str, Any] | None:
        return self.spreads.get(spread_id)

    def shuffle_and_draw(self, spread_id: str) -> Dict[str, Any]:
        """
        spread_id에 해당하는 스프레드를 가져와서,
        cards.json에서 랜덤으로 카드를 뽑고,
        API에서 그대로 쓸 수 있는 카드 리스트를 만들어 반환.
        """
        spread = self.get_spread(spread_id)
        if not spread:
            raise ValueError(f"Unknown spread_id: {spread_id}")

        card_count = spread["card_count"]

        # cards.json 키는 "1","2","3"... 이런 문자열이니까 그대로 샘플링
        all_ids_str = list(self.cards.keys())
        selected_ids_str = random.sample(all_ids_str, card_count)

        positions = spread["positions"]

        cards_out: list[Dict[str, Any]] = []

        for pos, cid_str in zip(positions, selected_ids_str):
            card_data = self.cards[cid_str]

            cards_out.append(
                {
                    # 응답에서는 숫자로 쓰기 편하게 int 변환
                    "card_id": int(cid_str),
                    "position_key": pos.get("slot"),
                    "position_label_en": pos.get("label_en"),
                    "position_label_ko": pos.get("label_ko"),
                    "row": pos.get("row"),
                    "column": pos.get("column"),
                    "name_en": card_data.get("name_en"),
                    "name_ko": card_data.get("name_ko"),
                    # 👉 여기서 meaning_en/ko를 interpretation_*으로 넘겨줌
                    "interpretation_en": card_data.get("meaning_en"),
                    "interpretation_ko": card_data.get("meaning_ko"),
                }
            )

        return {
            "spread_type": spread_id,
            "cards": cards_out,
        }
