import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


class LLMClient:
    """
    LLM client for Lenormand readings.
    """

    def __init__(self, model_name: str = "gpt-5.1") -> None:
        self.model_name = model_name
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("[LLMClient] Warning: OPENAI_API_KEY not set. Calls will fail.")
        self.client = OpenAI(api_key=api_key)

    def build_prompt(
        self,
        question_en: str,
        category: Optional[str],
        spread_type: str,
        cards: List[Dict[str, Any]],
    ) -> str:
        """
        Build a Lenormand reading prompt in English.
        """

        position_lines = []
        for card in cards:
            pos_label = card.get("position_label_en") or card.get("position_key")
            name_en = card.get("name_en", "Unknown")
            meaning_en = card.get("interpretation_en", "")

            if meaning_en:
                first_sentence = meaning_en.split(".")[0].strip()
            else:
                first_sentence = ""

            line = f"{pos_label}: {name_en}"
            if first_sentence:
                line += f" - {first_sentence}"
            position_lines.append(line)

        positions_block = "\n".join(position_lines)
        category_text = category or "general"

        if spread_type == "single_card_yes_no":
            mode_instruction = (
                "This is a *single-card YES/NO style* Lenormand reading.\n"
                "Decide whether the answer leans mostly YES, mostly NO, or UNCLEAR.\n"
                "\n"
                "Write your answer in this structure:\n"
                "Short answer: YES/NO/UNCLEAR\n"
                "Explanation: 2-3 sentences explaining why, mentioning the card.\n"
                "Actions: 3 bullet points of practical advice.\n"
                "Avoid being fatalistic or scary; focus on realistic, empowering guidance.\n"
            )
        else:
            mode_instruction = (
                "Create a narrative-style Lenormand reading using all cards.\n"
                "Give a concise summary, an overall story, and 3 short, practical action items.\n"
                "Avoid being fatalistic or scary; focus on empowerment and realistic guidance.\n"
            )

        prompt = (
            f"[MODEL:{self.model_name}] You are an experienced Lenormand reader. Answer in English.\n"
            f"Question: {question_en}\n"
            f"Category: {category_text}\n"
            f"Spread type: {spread_type}\n"
            f"Cards and positions:\n{positions_block}\n\n"
            f"{mode_instruction}\n"
            "Apply these Lenormand techniques in the reading (do not just list card keywords):\n"
            "- Center card: treat the middle card in odd-number spreads as the core of the situation.\n"
            "- Mirroring: for odd-number line spreads, read outer pairs as mirrors (3-card: 1↔3 around center 2; 5-card: 1↔5 and 2↔4 around center 3; 7-card: 1↔7, 2↔6, 3↔5 around center 4). Use mirrors to reveal hidden dynamics, conflicting motivations, or alternate ways the situation could unfold.\n"
            "- Chaining: read overlapping adjacent pairs as combined phrases (e.g., 3-card: 1+2 and 2+3; 5-card: 1+2, 2+3, 3+4, 4+5; 7-card: chain neighbors similarly). Use these chained phrases to create a flowing, sentence-like story.\n"
            "Explicitly show how the center defines the core, mirrors expand/complicate it, and chained pairs create a narrative flow.\n"
            "Return ONLY valid JSON, with no explanation or commentary, using this exact schema and types:\n"
            "{\n"
            '  "summary_en": "string, 2-4 sentence high-level summary of the reading.",\n'
            '  "overall_story_en": "string, short narrative explanation of how the cards connect as a story.",\n'
            '  "action_items_en": [\n'
            '    "string - one concrete suggestion or advice per item.",\n'
            '    "string - 2-5 items total."\n'
            "  ],\n"
            '  "prompt_used": "string, optional – will be ignored and overwritten."\n'
            "}\n"
            'The field "action_items_en" MUST be a JSON array of strings, NOT a single string.\n'
        )
        return prompt

    def _strip_code_fences(self, text: str) -> str:
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.lstrip("`")
            if "\n" in cleaned:
                cleaned = cleaned.split("\n", 1)[1]
            if "```" in cleaned:
                cleaned = cleaned.split("```", 1)[0]
        return cleaned.strip()

    def generate_reading(self, prompt: str, spread_type: str) -> Dict[str, Any]:
        print(f"[LLMClient] Calling model={self.model_name}, prompt_length={len(prompt)}")
        fallback = {
            "summary_en": "The model could not generate a reading at this time.",
            "overall_story_en": "There was an error while contacting the language model or parsing its response.",
            "action_items_en": [
                "Try again in a few moments.",
                "If the problem persists, check the server logs or API key configuration.",
            ],
            "prompt_used": prompt,
        }

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
            )
            content = response.choices[0].message.content
            if not content:
                print("[LLMClient] Empty response content from model.")
                return fallback

            cleaned = self._strip_code_fences(content)
            data = json.loads(cleaned)

            summary = str(data.get("summary_en", "")).strip()
            overall_story = str(data.get("overall_story_en", "")).strip()
            actions = data.get("action_items_en", [])

            if isinstance(actions, str):
                actions = [actions]
            elif not isinstance(actions, list):
                actions = []

            actions = [str(a).strip() for a in actions if str(a).strip()]

            result = {
                "summary_en": summary,
                "overall_story_en": overall_story,
                "action_items_en": actions,
                "prompt_used": prompt,
            }
            print("[LLMClient] Successfully generated reading.")
            return result
        except Exception as exc:  # noqa: BLE001
            print("[LLMClient] Error during LLM call or parsing:", exc)
            return fallback
