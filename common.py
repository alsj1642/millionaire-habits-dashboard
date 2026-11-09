"""부자 습관 팩트체크 대시보드 공통 부분 — 색 · 글꼴 · 헤더 · 푸터 · 숫자 계산 (DESIGN.md 시안 A2)"""
import math
from pathlib import Path

import pandas as pd
import streamlit as st

BASE = Path(__file__).resolve().parent
CLEAN = BASE / "data" / "clean.csv"

# ---------------------------------------------------------------
# 1. 색 (DESIGN.md 1장) — 새 색을 직접 쓰지 말고 여기 이름만 쓴다
# ---------------------------------------------------------------
BG = "#E4E1D8"        # 바탕 그레이지
INK = "#000000"       # 글자 · 아닌 사람 그룹 · 블랙 영역
MUTED = "#5E5B54"     # 보조 글자
LINE = "#CBC7BB"      # 구분선 · 트랙선 · 자리 표시 점
ACCENT = "#D45200"    # 백만장자 · 나 · 핵심 한 개
UNIT = "#7D7A72"      # 큰 숫자 뒤 단위 (24px 이상에서만)
WHITE = "#FFFFFF"     # 블랙 배경 위 글자

TARGET = "millionaire_status"
THRESHOLD_PP = 10  # 결정 한 줄의 기준 (%p)
RECORD_COL = "do_expense_tracking_frequency"  # '기록한다' = 지출을 주 1회 이상 기록

# (칸 이름, 화면에 쓸 짧은 이름, 묶음)
HABITS = [
    ("expense_tracking_frequency", "지출 기록", "money"),
    ("budgeting_frequency", "예산 짜기", "money"),
    ("financial_goal_setting", "돈 목표", "money"),
    ("automatic_savings", "자동이체 저축", "money"),
    ("dollar_cost_averaging", "적립식 투자", "money"),
    ("credit_card_payment_behavior", "카드값 완납", "money"),
    ("habit_tracking", "습관 기록", "life"),
    ("daily_planning", "하루 계획", "life"),
    ("exercise_days_per_week", "주 3일 운동", "life"),
    ("books_read_per_year", "월 1권 독서", "life"),
    ("social_media_hours_per_day", "SNS 2시간 이하", "life"),
    ("wake_up_time", "6시 전 기상", "life"),
]


# ---------------------------------------------------------------
# 2. 숫자 계산 (data/clean.csv 한 곳에서만 나온다)
# ---------------------------------------------------------------
@st.cache_data
def load_numbers() -> dict:
    df = pd.read_csv(CLEAN)
    n = len(df)
    n_mil = int(df[TARGET].sum())

    habits = []
    for col, label, group in HABITS:
        s = df[["do_" + col, TARGET]].dropna()  # 독서만 빈 값이 빠짐
        row = {"col": col, "label": label, "group": group}
        for g, key in ((1, "mil"), (0, "non")):
            x = s.loc[s[TARGET] == g, "do_" + col]
            row[key] = {"pct": x.mean() * 100, "yes": int(x.sum()), "n": int(len(x))}
        row["diff"] = row["mil"]["pct"] - row["non"]["pct"]
        habits.append(row)

    rec = df[[RECORD_COL, TARGET]]
    record = {}
    for flag, key in ((1, "yes"), (0, "no")):
        g = rec.loc[rec[RECORD_COL] == flag, TARGET]
        record[key] = {"pct": g.mean() * 100, "mil": int(g.sum()), "n": int(len(g))}
    record["diff"] = record["yes"]["pct"] - record["no"]["pct"]

    # 우연 범위: 습관과 백만장자 여부가 무관해도 95% 확률로 생길 수 있는 차이의 최대치
    # (비율 50%일 때가 가장 넓음) = 1.96 × √(0.25 × (1/백만장자 수 + 1/아닌 사람 수))
    chance_pp = 1.96 * math.sqrt(0.25 * (1 / n_mil + 1 / (n - n_mil))) * 100

    return {
        "chance_pp": chance_pp,
        "total": n,
        "millionaires": n_mil,
        "non": n - n_mil,
        "millionaire_pct": n_mil / n * 100,
        "habits": habits,
        "over": [h for h in habits if abs(h["diff"]) >= THRESHOLD_PP],
        "biggest": max(habits, key=lambda h: abs(h["diff"])),
        "record": record,
    }


def fmt(n: int) -> str:
    return f"{n:,}"


def p1(x: float) -> str:
    return f"{x:.1f}"


# ---------------------------------------------------------------
# 3. 화면 공통 CSS — Streamlit 기본 장식 숨기기 + 시안 A2 스타일
# ---------------------------------------------------------------
CSS = f"""
<style>
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css");
:root{{--bg:{BG};--ink:{INK};--muted:{MUTED};--line:{LINE};--accent:{ACCENT};--unit:{UNIT};--white:{WHITE}}}

/* Streamlit 기본 헤더 · 사이드바 · 푸터 숨기기 */
header[data-testid="stHeader"],[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"],
[data-testid="stToolbar"],[data-testid="stDecoration"],footer:not(.gs){{display:none!important}}
.stApp{{background:var(--bg)}}
.block-container,[data-testid="stMainBlockContainer"]{{max-width:1240px!important;padding:0 48px 40px!important}}
[data-testid="stVerticalBlock"]{{gap:0!important}}
@media (max-width:640px){{.block-container,[data-testid="stMainBlockContainer"]{{padding:0 16px 32px!important}}}}

.gs,.gs *{{box-sizing:border-box}}
.gs{{font-family:"Pretendard Variable","Pretendard",system-ui,sans-serif;color:var(--ink);word-break:keep-all;line-height:1.5}}
.gs p,.gs h1,.gs h2,.gs h3{{margin:0;padding:0;font-family:inherit;color:inherit;line-height:inherit}}
.gs a{{color:var(--ink)}} .gs a:hover{{color:var(--muted)}}
.gs a:focus-visible{{outline:3px solid var(--accent);outline-offset:4px}}
.gs .sr{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}
.gs.grid,.gs .grid{{display:grid;gap:48px}}
.gs .sec-head{{border-top:2px solid var(--ink);padding-top:18px}}
.gs .h2{{font-size:28px;font-weight:900;letter-spacing:-.03em;line-height:1.3}}
.gs .cap{{font-size:13px;line-height:1.7;color:var(--muted)}}
.gs .u{{color:var(--unit)}}

/* 헤더 */
.gs.top{{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:16px;padding:22px 0}}
.gs .logo{{display:flex;align-items:center;gap:10px;text-decoration:none;font-size:16px;font-weight:900;letter-spacing:-.02em}}
.gs .logo i{{width:18px;height:18px;border-radius:50%;background:var(--accent)}}
.gs .nav{{display:flex;flex-wrap:wrap;gap:8px}}
.gs .nav a{{display:inline-flex;align-items:center;min-height:44px;padding:0 18px;border-radius:999px;text-decoration:none;font-size:14px;font-weight:500}}
.gs .nav a[aria-current="page"]{{background:var(--ink);color:var(--white);font-weight:700}}

/* 푸터 */
.gs.foot{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:16px 48px;font-size:13px;line-height:1.7;color:var(--muted);padding-top:18px;border-top:1px solid var(--line)}}
.gs.foot strong{{color:var(--ink)}}

/* 모션: 섹션이 화면에 들어올 때 한 번 (JS가 armed를 붙였을 때만) */
.gs .reel{{display:flex;flex-direction:column;transform:translateY(var(--to))}}
.gs .reel>span{{display:block;height:1em;line-height:1em}}
.gs .wheel{{display:inline-block;height:1em;overflow:hidden;vertical-align:top}}
.armed .reel{{transform:translateY(0)}}
.armed.in .reel{{animation:gsRoll .8s cubic-bezier(.16,1,.3,1) both;animation-delay:var(--d,0s)}}
@keyframes gsRoll{{from{{transform:translateY(0)}}to{{transform:translateY(var(--to))}}}}
.armed .pp{{transform:scale(0)}}
.armed.in .pp{{animation:gsPop .7s cubic-bezier(.34,1.56,.64,1) both;animation-delay:var(--d,0s)}}
@keyframes gsPop{{from{{transform:scale(0)}}to{{transform:scale(1)}}}}
.armed .slideL{{transform:translateX(42px)}} .armed .slideR{{transform:translateX(-42px)}}
.armed.in .slideL,.armed.in .slideR{{animation:gsBack 1.1s cubic-bezier(.34,1.56,.64,1) .5s both}}
@keyframes gsBack{{to{{transform:none}}}}
.armed .track{{transform:scaleX(0);transform-origin:left center}}
.armed.in .track{{animation:gsGrow 1s cubic-bezier(.22,1,.36,1) both;animation-delay:var(--d,0s)}}
@keyframes gsGrow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
.armed .dd{{visibility:hidden}}
.armed.in .dd{{visibility:visible;animation:gsDot 1.1s cubic-bezier(.34,1.56,.64,1) both;animation-delay:var(--d,0s)}}
@keyframes gsDot{{from{{transform:translateX(-80px) scale(.4)}}}}
/* 아래에서 떠오르며 나타나기 */
.armed .rise{{opacity:0;transform:translateY(28px)}}
.armed.in .rise{{animation:gsRise 1s cubic-bezier(.16,1,.3,1) both;animation-delay:var(--d,0s)}}
@keyframes gsRise{{from{{opacity:0;transform:translateY(28px)}}to{{opacity:1;transform:none}}}}
/* 첫 화면 글은 열리자마자 떠오르기 */
.gs .rise-now{{animation:gsRise .8s cubic-bezier(.16,1,.3,1) both;animation-delay:var(--d,0s)}}
/* Plotly 차트도 다 보일 때 떠오르기.
   Streamlit이 차트 요소의 class를 다시 그리며 지우므로, 차트 바로 아래 캡션(.chart-cap)의 상태로 차트를 움직인다 */
[data-testid="stElementContainer"]:has(+ [data-testid="stElementContainer"] .chart-cap.armed:not(.in)) [data-testid="stPlotlyChart"]{{opacity:0;transform:translateY(28px)}}
[data-testid="stElementContainer"]:has(+ [data-testid="stElementContainer"] .chart-cap.in) [data-testid="stPlotlyChart"]{{animation:gsRise 1s cubic-bezier(.16,1,.3,1) both}}
@media (prefers-reduced-motion: reduce){{.gs *,[data-testid="stPlotlyChart"]{{animation:none!important;opacity:1!important;transform:none!important}}}}
</style>
"""

# 섹션 내용이 화면에 '다 들어왔을 때' 'in'을 붙여 모션을 한 번만 재생한다.
#  - 화면보다 작은 섹션: 85% 이상 보일 때
#  - 화면보다 큰 섹션: 화면의 80%를 채울 때
#  - 빠르게 스크롤해서 그 순간을 건너뛰고 섹션 윗부분이 화면 위로 지나가 버린 경우에도 시작
REVEAL_JS = """
<script>
(function () {
  var targets = document.querySelectorAll('[data-reveal]:not(.armed)');
  var watchers = document.querySelectorAll('[data-watch-prev]:not(.armed)');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!window.IntersectionObserver || reduce) {
    targets.forEach(function (s) { s.classList.add('in'); });
    watchers.forEach(function (s) { s.classList.add('in'); });
    return;
  }
  // data-watch-prev: 바로 앞 Streamlit 요소(예: Plotly 차트)가 정해진 비율만큼 보이면 이 요소에 'in'을 붙인다
  watchers.forEach(function (w) {
    var box = w.closest('[data-testid="stElementContainer"]');
    var prev = box && box.previousElementSibling;
    if (!prev) { w.classList.add('in'); return; }
    var ratio = parseFloat(w.getAttribute('data-watch-prev')) || 0.35;
    w.classList.add('armed');
    var wo = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.intersectionRatio >= ratio || (e.isIntersecting && e.boundingClientRect.top < 0)) { w.classList.add('in'); wo.disconnect(); }
      });
    }, { threshold: [0, 0.1, 0.2, 0.3, 0.35, 0.4, 0.5, 0.6, 0.8, 1] });
    wo.observe(prev);
  });
  var steps = [];
  for (var i = 0; i <= 20; i++) steps.push(i / 20);
  function need(el) {
    var h = el.getBoundingClientRect().height || 1;
    return Math.min(0.85, (window.innerHeight * 0.8) / h);
  }
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      var passed = e.isIntersecting && e.boundingClientRect.top < 0;
      if (passed || e.intersectionRatio >= need(e.target) - 0.001) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: steps });
  targets.forEach(function (s) { s.classList.add('armed'); io.observe(s); });
})();
</script>
"""


def setup() -> None:
    """페이지마다 맨 처음 한 번 부른다."""
    st.html(CSS)


def html(body: str, js: bool = False) -> None:
    st.html(body, unsafe_allow_javascript=js)


def header(active: str) -> None:
    pages = [("./", "home", "부자 습관 이야기"), ("./record", "record", "기록 한 걸음")]
    cur = ' aria-current="page"'
    links = "".join(
        f'<a href="{href}" target="_self"{cur if key == active else ""}>{label}</a>'
        for href, key, label in pages
    )
    html(
        f'<header class="gs top"><a class="logo" href="./" target="_self"><i aria-hidden="true"></i>부자 습관 팩트체크</a>'
        f'<nav class="nav" aria-label="페이지">{links}</nav></header>'
    )


def gap(px: int) -> None:
    html(f'<div aria-hidden="true" style="height:{px}px"></div>')


def odometer(text: str) -> str:
    """큰 숫자를 자리마다 굴러 올라가는 바퀴로 만든다 (숫자가 아닌 글자는 그대로)."""
    out, k = [], 0
    for ch in text:
        if not ch.isdigit():
            out.append(ch)
            continue
        digits = "".join(f"<span>{i % 10}</span>" for i in range(20))
        out.append(
            f'<span class="wheel"><span class="reel" style="--to:-{10 + int(ch)}em;--d:{k * 0.06:.2f}s">{digits}</span></span>'
        )
        k += 1
    return f'<span aria-hidden="true">{"".join(out)}</span><span class="sr">{text}</span>'


def reveal_script() -> None:
    """페이지 맨 끝에서 부른다."""
    html(REVEAL_JS, js=True)
