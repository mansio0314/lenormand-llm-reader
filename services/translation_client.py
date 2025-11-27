import os
from typing import Any, Dict, List, Union

from openai import OpenAI


class TranslationClient:
    """
    Translation client for Korean <-> English.
    """

    def __init__(self, model_name: str = "gpt-5.1") -> None:
        self.model_name = model_name
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("[TranslationClient] Warning: OPENAI_API_KEY not set. Calls will fail.")
        self.client = OpenAI(api_key=api_key)

    def translate(self, text: str, target_lang: str) -> str:
        if not text:
            return ""
        print(f"[TranslationClient] Translating to {target_lang}, text_length={len(text)}")
        if target_lang not in {"en", "ko"}:
            return text

        if target_lang == "en":
            instruction = (
                "Translate the following Korean text into clear, natural English. "
                "Preserve meaning and tone. Return ONLY the translated text, "
                "with no explanations or extra formatting."
            )
        else:
            instruction = (
                "Translate the following English text into natural, smooth Korean appropriate for a Lenormand card reading. "
                "Preserve line breaks and basic formatting. Return ONLY the translated text, "
                "with no explanations or extra formatting."
            )

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": instruction},
                    {"role": "user", "content": text},
                ],
            )
            content = response.choices[0].message.content or ""
            return content.strip()
        except Exception as exc:  # noqa: BLE001
            print("[TranslationClient] Error during translation:", exc)
            return text

    def _translate_value(self, value: Union[str, List[str]], target_lang: str) -> Union[str, List[str]]:
        if isinstance(value, list):
            return [self.translate(v, target_lang) for v in value]
        if isinstance(value, str):
            return self.translate(value, target_lang)
        return value

    def translate_reading(self, reading: Dict[str, Any]) -> Dict[str, Any]:
        print("[TranslationClient] Translating full reading dict en->ko.")
        summary_en = reading.get("summary_en", "")
        overall_story_en = reading.get("overall_story_en", "")
        actions_en = reading.get("action_items_en", [])
        prompt_used = reading.get("prompt_used", "")

        summary_ko = self.translate(summary_en, target_lang="ko")
        overall_story_ko = self.translate(overall_story_en, target_lang="ko")

        if isinstance(actions_en, list):
            actions_ko = [self.translate(item, target_lang="ko") for item in actions_en]
        else:
            actions_ko = []

        prompt_used_ko = self.translate(prompt_used, target_lang="ko")

        return {
            "summary_ko": summary_ko,
            "overall_story_ko": overall_story_ko,
            "action_items_ko": actions_ko,
            "prompt_used_ko": prompt_used_ko,
        }
