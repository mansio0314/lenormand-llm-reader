import json
import random
from pathlib import Path

# 경로는 네 프로젝트 구조에 맞게 수정하기
BASE_DIR = Path(__file__).resolve().parent
cards_path = BASE_DIR / "data" / "cards.json"
spreads_path = BASE_DIR / "data" / "spreads.json"

# 1) JSON 잘 읽히는지
with cards_path.open(encoding="utf-8") as f:
    cards = json.load(f)

with spreads_path.open(encoding="utf-8") as f:
    spreads = json.load(f)["spreads"]

print(f"카드 개수: {len(cards)}")          # 36 나와야 정상
print(f"스프레드 종류: {list(spreads.keys())}")

# 2) 임의 스프레드 하나 꺼내서 카드 뽑아보기
spread = spreads["past_present_future"]   # 다른 스프레드 이름으로 바꿔도 됨
card_count = spread["card_count"]

selected_ids = random.sample(list(cards.keys()), card_count)

print("\n=== 테스트 리딩 ===")
print("스프레드:", spread["name_ko"])
for pos, cid in zip(spread["positions"], selected_ids):
    c = cards[cid]
    print(
        f"- 위치 {pos['label_ko']} ({pos['slot']}): "
        f"{c['name_ko']} / {c['name_en']} "
        f"-> 키워드: {', '.join(c['keywords_ko'][:3])}"
    )
