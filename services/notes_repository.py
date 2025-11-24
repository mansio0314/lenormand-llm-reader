# services/notes_repository.py
import re
from pathlib import Path
from typing import Dict, Optional


class NotesRepository:
    """
    lenormand_notes.txt에서 <rider>...</rider> 같은 블록을
    name_en 기반으로 찾아오는 유틸리티.
    """

    def __init__(self, notes_path: Path) -> None:
        self.raw = ""
        if notes_path.exists():
            self.raw = notes_path.read_text(encoding="utf-8")
        self.cache: Dict[str, str] = {}

    def get_block(self, name_en: Optional[str]) -> Optional[str]:
        """카드 영어 이름으로 해당 태그 블록 반환."""
        if not self.raw or not name_en:
            return None

        key = name_en.lower().strip()
        if key in self.cache:
            return self.cache[key]

        pattern = rf"<{re.escape(key)}>(.*?)</{re.escape(key)}>"
        m = re.search(pattern, self.raw, re.DOTALL | re.IGNORECASE)
        if not m:
            return None

        content = m.group(1).strip()
        self.cache[key] = content
        return content
