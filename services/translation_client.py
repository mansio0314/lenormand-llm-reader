from typing import Any, Dict, List, Union


class TranslationClient:
    """
    Placeholder translation client. Swap with actual provider (e.g., DeepL, Google Cloud)
    by replacing translate and translate_reading implementations.
    """

    def translate(self, text: str, target_lang: str) -> str:
        if not text:
            return ""
        # Simple stub to mark that translation would happen here.
        return f"{text} [{target_lang} draft]"

    def _translate_value(self, value: Union[str, List[str]], target_lang: str) -> Union[str, List[str]]:
        if isinstance(value, list):
            return [self.translate(v, target_lang) for v in value]
        if isinstance(value, str):
            return self.translate(value, target_lang)
        return value

    def translate_reading(self, reading: Dict[str, Any]) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for key, value in reading.items():
            if key.endswith("_en"):
                target_key = key.replace("_en", "_ko")
            else:
                target_key = f"{key}_ko"
            result[target_key] = self._translate_value(value, target_lang="ko")
        return result
