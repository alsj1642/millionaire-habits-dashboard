"""data/raw.csv → data/clean.csv 정제 스크립트 (기준은 회의록.md '정제 규칙')

사용법:
    python clean.py          # 결과만 보여 줌 (저장 안 함)
    python clean.py --save   # 결과를 보여 주고 data/clean.csv 로 저장
"""
import sys
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
RAW = BASE / "data" / "raw.csv"
CLEAN = BASE / "data" / "clean.csv"

TARGET = "millionaire_status"

# 습관 칸 → '한다(1)' 기준. 새 칸 이름은 do_<원래 칸 이름>
RULES = {
    # 돈 습관
    "expense_tracking_frequency": lambda s: s.isin(["Daily", "Weekly"]),
    "budgeting_frequency": lambda s: s.isin(["Daily", "Weekly", "Monthly"]),
    "financial_goal_setting": lambda s: s == 1,
    "automatic_savings": lambda s: s == 1,
    "dollar_cost_averaging": lambda s: s == 1,
    "credit_card_payment_behavior": lambda s: s == "Always Full",
    # 생활 습관
    "habit_tracking": lambda s: s == 1,
    "daily_planning": lambda s: s == 1,
    "exercise_days_per_week": lambda s: s >= 3,
    "books_read_per_year": lambda s: s >= 12,
    "social_media_hours_per_day": lambda s: s <= 2,
    "wake_up_time": lambda s: s <= 6.0,
}
HABITS = list(RULES)


def make_clean(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw[HABITS + [TARGET]].copy()
    for col, rule in RULES.items():
        flag = rule(df[col]).astype("Int8")
        # 빈 값은 '안 한다'로 바꾸지 않고 빈 값 그대로 둠 (독서 비교에서만 제외)
        flag[df[col].isna()] = pd.NA
        df[f"do_{col}"] = flag
    return df


def main() -> None:
    save = "--save" in sys.argv

    raw = pd.read_csv(RAW)
    clean = make_clean(raw)

    print("=== 정제 전후 크기 ===")
    print(f"정제 전 (raw.csv)  : {len(raw):>7,}행 × {raw.shape[1]:>3}칸")
    print(f"정제 후 (clean.csv): {len(clean):>7,}행 × {clean.shape[1]:>3}칸"
          f"  (원래 칸 {len(HABITS) + 1}개 + 새 0/1 칸 {len(HABITS)}개)")

    print("\n=== 칸별 빈 값 개수 (정제 전 → 정제 후) ===")
    rows = []
    for col in HABITS + [TARGET]:
        new = f"do_{col}" if col in RULES else None
        rows.append({
            "칸": col,
            "정제 전 빈 값": int(raw[col].isna().sum()),
            "정제 후 빈 값(원래 칸)": int(clean[col].isna().sum()),
            "새 칸": new or "-",
            "새 칸 빈 값": int(clean[new].isna().sum()) if new else "-",
            "'한다' 비율(%)": round(clean[new].mean() * 100, 1) if new else "-",
        })
    print(pd.DataFrame(rows).to_string(index=False))

    if save:
        clean.to_csv(CLEAN, index=False, encoding="utf-8-sig")
        print(f"\n저장함: {CLEAN}")
    else:
        print("\n(저장하지 않음 — 저장하려면 python clean.py --save)")


if __name__ == "__main__":
    main()
