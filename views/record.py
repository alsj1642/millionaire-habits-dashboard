"""분석 — 기록 한 걸음 (DESIGN.md 4장 분석 순서 + 수업 조건: Plotly 차트 1개)"""
import math

import plotly.graph_objects as go
import streamlit as st

import common as c

c.setup()
N = c.load_numbers()
R = N["record"]
c.header("record")

c.html("""
<style>
.gs.q{display:flex;flex-direction:column;gap:28px;padding-top:72px}
.gs.q .kick{font-size:20px;font-weight:500;color:var(--muted)}
.gs.q h1{font-size:clamp(44px,6vw,72px);line-height:1.1;font-weight:900;letter-spacing:-.045em;max-width:13em}
.gs.q .lead{font-size:18px;line-height:1.7;max-width:32em}
.gs.cmp{grid-template-columns:repeat(auto-fit,minmax(min(100%,460px),1fr));gap:48px 64px;align-items:center}
.gs .bubbles{display:flex;justify-content:center;align-items:flex-end;gap:16px;flex-wrap:wrap}
.gs .bub{display:flex;flex-direction:column;align-items:center;gap:16px}
.gs .circle{border-radius:50%;display:flex;align-items:center;justify-content:center;max-width:42vw;max-height:42vw}
.gs .circle b{font-size:clamp(36px,4.5vw,64px);font-weight:700;letter-spacing:-.04em;line-height:1;font-variant-numeric:tabular-nums}
.gs .bub .nm{font-size:16px;font-weight:700;text-align:center;line-height:1.5}
.gs .bub .nm span{display:block;font-size:13px;font-weight:400;color:var(--muted)}
.gs .table{border-top:2px solid var(--ink)}
.gs .table h2{padding:18px 0;font-size:24px;font-weight:900;letter-spacing:-.03em}
.gs .tr{display:flex;justify-content:space-between;align-items:baseline;gap:16px;padding:18px 0;border-top:1px solid var(--line)}
.gs .tr .k{font-size:15px;line-height:1.5}
.gs .tr .k span{display:block;font-size:13px;color:var(--muted)}
.gs .tr .v{font-size:40px;font-weight:700;letter-spacing:-.04em;line-height:1;white-space:nowrap;font-variant-numeric:tabular-nums}
.gs.chart-intro{display:flex;flex-direction:column;gap:14px}
.gs.chart-intro .kick{font-size:15px;font-weight:900}
.gs.chart-intro p{font-size:15px;line-height:1.7;max-width:46em}
.gs .legend{display:flex;flex-wrap:wrap;gap:22px;font-size:14px;font-weight:500}
.gs .legend>span{display:inline-flex;align-items:center;gap:8px}
.gs .mk{width:14px;height:14px;flex-shrink:0;display:inline-block}
.gs.three{grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:20px}
.gs .card{display:flex;flex-direction:column;gap:14px;padding:32px 0;border-top:2px solid var(--ink)}
.gs .card h2{font-size:15px;font-weight:900}
.gs .card p{font-size:22px;line-height:1.5;font-weight:500;letter-spacing:-.02em}
.gs .card.todo{padding:32px;background:var(--ink);color:var(--white);border:0;border-radius:24px}
.gs .card.todo h2{display:flex;align-items:center;gap:10px}
.gs .card.todo h2 i{width:12px;height:12px;border-radius:50%;background:var(--accent)}
.gs .card.todo p{font-size:24px;line-height:1.45;font-weight:900;letter-spacing:-.03em}
</style>
""")

# ---------------------------------------------------------------
# 1. 질문 (열리자마자 한 줄씩 떠오름)
# ---------------------------------------------------------------
c.html(f"""
<section class="gs q" aria-labelledby="q2">
  <p class="kick rise-now">이 데이터에서는 부자 습관이 따로 보이지 않았죠. 그럼 첫 걸음은 뭐부터?</p>
  <h1 id="q2" class="rise-now" style="--d:.12s">돈을 적는 사람과<br>안 적는 사람,<br>뭐가 다를까요?</h1>
  <p class="lead rise-now" style="--d:.24s">가장 쉬운 한 걸음인 ‘기록’만 따로 봤어요. {N['total'] // 10000}만 명을 지출을 주 1회 이상 기록하는 사람({c.fmt(R['yes']['n'])}명)과 그렇지 않은 사람({c.fmt(R['no']['n'])}명)으로 나눠, 각각 백만장자가 몇 %인지 비교했어요.</p>
</section>
""")
c.gap(112)

# ---------------------------------------------------------------
# 2. 핵심 숫자 + 원 차트 (넓이 ∝ 비율, 가장 큰 원 지름 260px)
#    원은 튀어나오고, 숫자는 굴러 올라가고, 표 줄은 차례로 떠오름
# ---------------------------------------------------------------
top = max(R["yes"]["pct"], R["no"]["pct"])
dia = {k: round(260 * math.sqrt(R[k]["pct"] / top)) for k in ("yes", "no")}
y, n = R["yes"], R["no"]
c.html(f"""
<section class="gs grid cmp" data-reveal aria-labelledby="chart2">
  <div class="bubbles" role="img" aria-label="기록하는 사람 중 백만장자 {c.p1(y['pct'])}%, 기록 안 하는 사람 중 {c.p1(n['pct'])}%를 원 넓이로 비교한 그림">
    <div class="bub">
      <div class="circle pp" style="width:{dia['yes']}px;height:{dia['yes']}px;background:var(--accent);--d:0s"><b>{c.odometer(c.p1(y['pct']))}%</b></div>
      <p class="nm rise" style="--d:.3s">기록한다<span>{c.fmt(y['n'])}명</span></p>
    </div>
    <div class="bub">
      <div class="circle pp" style="width:{dia['no']}px;height:{dia['no']}px;border:3px solid var(--ink);--d:.15s"><b>{c.odometer(c.p1(n['pct']))}%</b></div>
      <p class="nm rise" style="--d:.45s">기록 안 한다<span>{c.fmt(n['n'])}명</span></p>
    </div>
  </div>
  <div class="table">
    <h2 id="chart2">그룹별 백만장자 비율</h2>
    <div class="tr rise" style="--d:.1s"><p class="k">기록하는 사람 중 백만장자<span>{c.fmt(y['mil'])} / {c.fmt(y['n'])}명</span></p><p class="v">{c.odometer(c.p1(y['pct']))}<span class="u">%</span></p></div>
    <div class="tr rise" style="--d:.2s"><p class="k">기록 안 하는 사람 중 백만장자<span>{c.fmt(n['mil'])} / {c.fmt(n['n'])}명</span></p><p class="v">{c.odometer(c.p1(n['pct']))}<span class="u">%</span></p></div>
    <div class="tr rise" style="--d:.3s"><p class="k" style="font-weight:700">두 그룹 차이</p><p class="v">{c.odometer(c.p1(abs(R['diff'])))}<span class="u">%p</span></p></div>
    <p class="cap rise" style="margin-top:8px;--d:.4s">원의 넓이를 백만장자 비율에 맞췄어요. 두 원의 크기가 같으면 차이가 없다는 뜻이에요.</p>
  </div>
</section>
""")
c.gap(112)

# ---------------------------------------------------------------
# 3. Plotly 차트 — 습관 12개의 두 그룹 차이(%p), 0이 가운데 기준선
# ---------------------------------------------------------------
chance = N["chance_pp"]
habits = N["habits"]
# 가로축은 결정 기준(±10%p)까지 넓게 고정한다.
# 축을 좁게 잡으면 0.4%p 같은 작은 차이도 크게 보이는 '함정 차트'가 되기 때문.
TH = c.THRESHOLD_PP
max_abs = max(abs(h["diff"]) for h in habits)
inside = all(abs(h["diff"]) < chance for h in habits)
title = (f"<b>습관 12개 모두, 두 그룹 차이가<br>우연 범위(±{c.p1(chance)}%p) 안이었어요</b>" if inside
         else f"<b>습관 12개 중 가장 큰 차이는<br>{c.p1(max_abs)}%p였어요</b>")

c.html(f"""
<section class="gs chart-intro sec-head" data-reveal>
  <p class="kick rise">기록 말고 다른 습관은요?</p>
  <p class="rise" style="--d:.1s">습관 12개마다 ‘백만장자 그룹의 실천 비율 − 아닌 사람 그룹의 실천 비율’을 막대로 그렸어요. 가운데 검은 선이 차이 0이에요. 오른쪽으로 길면 백만장자 그룹에, 왼쪽으로 길면 아닌 사람 그룹에 그 습관이 더 많다는 뜻이에요. 회색 띠는 습관과 백만장자 여부가 아무 상관이 없어도 우연히 생길 수 있는 차이(±{c.p1(chance)}%p)예요. 양쪽 점선은 습관을 고르기로 미리 정한 결정 기준(±{TH}%p)이에요. 작은 차이가 부풀려 보이지 않도록 가로축을 이 기준까지 넓게 잡았어요.</p>
  <div class="legend rise" style="--d:.2s">
    <span><i class="mk" style="background:var(--accent);border-radius:2px" aria-hidden="true"></i>백만장자 그룹에 더 많음</span>
    <span><i class="mk" style="background:var(--ink);border-radius:2px" aria-hidden="true"></i>아닌 사람 그룹에 더 많음</span>
    <span><i class="mk" style="background:var(--line)" aria-hidden="true"></i>우연 범위</span>
    <span><i class="mk" style="width:18px;height:0;border-top:2px dashed var(--ink)" aria-hidden="true"></i>결정 기준 ±{TH}%p</span>
  </div>
</section>
""")

order = list(reversed(habits))  # 위에서부터 돈 습관 6개 → 생활 습관 6개
labels = [h["label"] for h in order]
diffs = [h["diff"] for h in order]
hover = [
    f"<b>{h['label']}</b><br>"
    f"백만장자 {c.p1(h['mil']['pct'])}% ({c.fmt(h['mil']['yes'])} / {c.fmt(h['mil']['n'])}명)<br>"
    f"아닌 사람 {c.p1(h['non']['pct'])}% ({c.fmt(h['non']['yes'])} / {c.fmt(h['non']['n'])}명)<br>"
    f"차이 {h['diff']:+.2f}%p"
    for h in order
]
lim = TH + 0.6  # ±10 점선이 가장자리에 붙지 않게 약간 여유
FONT = '"Pretendard Variable", Pretendard, system-ui, sans-serif'

fig = go.Figure(go.Bar(
    x=diffs, y=labels, orientation="h",
    marker=dict(color=[c.ACCENT if d >= 0 else c.INK for d in diffs], cornerradius=3),
    width=0.56,
    text=[f"{d:+.2f}%p" for d in diffs], textposition="outside", cliponaxis=False,
    textfont=dict(size=13, color=c.INK),
    hovertext=hover, hoverinfo="text",
))
fig.add_vrect(x0=-chance, x1=chance, fillcolor=c.LINE, opacity=0.45, line_width=0, layer="below")
fig.add_vline(x=0, line=dict(color=c.INK, width=2))
fig.add_hline(y=5.5, line=dict(color=c.LINE, width=1))  # 돈 습관 | 생활 습관 사이 구분선
# 결정 기준 ±10%p 점선 + 이름표 (차트 위쪽 바깥)
for x, text, anchor in ((-TH, f"−{TH}%p 결정 기준", "left"), (TH, f"결정 기준 +{TH}%p", "right")):
    fig.add_vline(x=x, line=dict(color=c.INK, width=1.5, dash="dash"))
    fig.add_annotation(text=f"<b>{text}</b>", x=x, y=1, yref="paper", yanchor="bottom", xanchor=anchor,
                       showarrow=False, font=dict(size=13, color=c.INK))
# 묶음 이름 (각 묶음 위 경계선 바로 위). 막대 옆 숫자와 겹치지 않게 '돈'은 −10 점선 안쪽, '생활'은 +10 점선 안쪽
for text, yy, x, anchor in (("돈 습관 ↓", 11.5, -TH + 0.3, "left"), ("생활 습관 ↓", 5.5, TH - 0.3, "right")):
    fig.add_annotation(text=f"<b>{text}</b>", x=x, y=yy, yanchor="bottom", xanchor=anchor,
                       showarrow=False, font=dict(size=13, color=c.MUTED))
fig.update_layout(
    title=dict(text=title, x=0, xanchor="left", font=dict(size=22, color=c.INK, family=FONT)),
    font=dict(family=FONT, size=14, color=c.INK),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    height=660, margin=dict(l=8, r=16, t=124, b=56), showlegend=False, bargap=0.3,
    hoverlabel=dict(bgcolor=c.WHITE, bordercolor=c.LINE, font=dict(family=FONT, size=13, color=c.INK)),
)
fig.update_xaxes(range=[-lim, lim], showgrid=False, zeroline=False,
                 tickvals=[-TH, -TH / 2, 0, TH / 2, TH],
                 ticktext=[f"−{TH}%p", f"−{TH / 2:g}%p", "0", f"+{TH / 2:g}%p", f"+{TH}%p"],
                 tickfont=dict(color=c.MUTED, size=12),
                 title=dict(text="두 그룹 차이 (백만장자 − 아닌 사람, %p)", font=dict(color=c.MUTED, size=13)),
                 fixedrange=True)
fig.update_yaxes(showgrid=False, tickfont=dict(size=14, color=c.INK), automargin=True, fixedrange=True)
st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

books = next(h for h in habits if h["col"] == "books_read_per_year")
# 위 차트가 35% 보이면 이 캡션에 'in'이 붙고, 그 상태로 차트가 떠오른다 (common.py CSS · JS 참고)
c.html(f'<div class="gs chart-cap" data-watch-prev="0.35"><p class="cap">막대에 마우스를 올리면 그룹별 인원이 나와요. 독서는 빈 값을 뺀 {c.fmt(books["mil"]["n"])}명 · {c.fmt(books["non"]["n"])}명으로 계산했어요.</p></div>')
c.gap(112)

# ---------------------------------------------------------------
# 4. 사실 · 해석 · 행동 (데이터에서 나온 말만)
# ---------------------------------------------------------------
c.html(f"""
<section class="gs grid three" data-reveal aria-label="사실, 해석, 행동">
  <div class="card rise">
    <h2>사실</h2>
    <p>지출을 주 1회 이상 기록하는 사람은 {c.fmt(y['n'])}명 중 {c.fmt(y['mil'])}명({c.p1(y['pct'])}%), 기록하지 않는 사람은 {c.fmt(n['n'])}명 중 {c.fmt(n['mil'])}명({c.p1(n['pct'])}%)이 백만장자였어요.</p>
  </div>
  <div class="card rise" style="--d:.12s">
    <h2>해석</h2>
    <p>기록 여부와 백만장자 여부 사이에 관련이 보이지 않았어요. 가상 데이터라 실제 사람들도 그런지는 알 수 없어요.</p>
  </div>
  <div class="card todo rise" style="--d:.24s">
    <h2><i aria-hidden="true"></i>행동</h2>
    <p>이 데이터로는 고를 습관이 없었어요. 그래서 미리 정한 규칙대로, 기록하기부터 시작해요.</p>
  </div>
</section>
""")
c.gap(112)

# ---------------------------------------------------------------
# 5. 한계 · 출처
# ---------------------------------------------------------------
c.html(f"""
<footer class="gs foot">
  <p><strong>한계</strong><br>가상 인물 데이터라 실제와 다를 수 있어요. 기록과 백만장자 여부가 함께 나타나는지만 볼 수 있고, 원인과 결과는 말할 수 없어요. ‘기록한다’는 지출을 주 1회 이상(Daily · Weekly) 기록하는 사람이에요.</p>
  <p><strong>출처</strong><br>Kaggle Millionaire Habits Dataset, 가상 인물 {N['total'] // 10000}만 명</p>
</footer>
""")
c.reveal_script()
