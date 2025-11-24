from typing import Any, Dict, List, Optional


class LLMClient:
    """
    Placeholder LLM client.
    Replace generate_reading with a real provider call (OpenAI, Anthropic, etc.).
    """

    def __init__(self, model_name: str = "gpt-4o-mini") -> None:
        self.model_name = model_name

    def build_prompt(
        self,
        question_en: str,
        category: Optional[str],
        spread_type: str,
        cards: List[Dict[str, Any]],
    ) -> str:
        """
        Lenormand 프롬프트 생성.
        - single_card_yes_no  : 예/아니오 스타일
        - 그 외 스프레드      : 일반 스토리형 리딩
        """

        # 카드 정보를 레노먼드스럽게 표현
        position_lines = []
        for card in cards:
            pos_label = card.get("position_label_en") or card.get("position_key")
            name_en = card.get("name_en", "Unknown")
            meaning_en = card.get("interpretation_en", "")

            # 첫 문장만 잘라서 짧게 사용
            if meaning_en:
                first_sentence = meaning_en.split(".")[0].strip()
            else:
                first_sentence = ""

            line = f"{pos_label}: {name_en}"
            if first_sentence:
                line += f" – {first_sentence}"
            position_lines.append(line)

        positions_block = "\n".join(position_lines)
        category_text = category or "general"

        # 🔹 스프레드 타입에 따라 프롬프트 문구 분기
        if spread_type == "single_card_yes_no":
            mode_instruction = (
                "This is a *single-card YES/NO style* Lenormand reading.\n"
                "Decide whether the answer leans mostly YES, mostly NO, or UNCLEAR.\n"
                "\n"
                "Write your answer in this structure:\n"
                "Short answer: YES/NO/UNCLEAR\n"
                "Explanation: 2–3 sentences explaining why, mentioning the card.\n"
                "Actions: 3 bullet points of practical advice.\n"
                "Avoid being fatalistic or scary; focus on realistic, empowering guidance.\n"
            )
        else:
            mode_instruction = (
                "Create a narrative-style Lenormand reading using all cards.\n"
                "Give a concise summary, an overall story, and 3 short, practical action items.\n"
                "Avoid being fatalistic or scary; focus on empowerment and realistic guidance.\n"
            )

        # 최종 프롬프트
        return (
            f"[MODEL:{self.model_name}] You are an experienced Lenormand reader.\n"
            f"Create the reading in natural English.\n\n"
            f"Question: {question_en}\n"
            f"Category: {category_text}\n"
            f"Spread type: {spread_type}\n\n"
            f"Cards and positions:\n{positions_block}\n\n"
            f"{mode_instruction}"
        )


    def generate_reading(self, prompt: str, spread_type: str) -> Dict[str, Any]:
        # Stubbed response; replace with actual LLM call and parsing.
        base_summary = f"Draft reading for spread '{spread_type}'."
        return {
            "summary_en": base_summary,
            "overall_story_en": "This is a placeholder overall story based on the shuffled cards.",
            "action_items_en": [
                "Reflect on the main theme highlighted in the cards.",
                "Identify one practical step to move forward.",
                "Revisit the reading after a few days to notice shifts.",
            ],
            "prompt_used": prompt,
        }
