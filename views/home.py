"""홈 — 부자 습관 이야기 (DESIGN.md 4장 홈 순서 그대로)"""
import common as c

c.setup()
N = c.load_numbers()
c.header("home")

PAGE_CSS = """
<style>
.gs.hero{grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));align-items:center;padding-top:72px}
.gs.hero h1{font-size:clamp(48px,6vw,76px);line-height:1.08;font-weight:900;letter-spacing:-.045em}
.gs.hero .lead{font-size:20px;line-height:1.65;max-width:24em}
.gs.hero .first{display:flex;align-items:center;gap:12px;font-size:16px;font-weight:700}
.gs.hero .first i{width:10px;height:10px;border-radius:50%;background:var(--accent);flex-shrink:0}
.gs .stage{position:relative;width:516px;max-width:100%;aspect-ratio:1;margin-left:auto;overflow:hidden}
.gs .stage-in{position:absolute;top:0;left:0;width:516px;height:516px;transform-origin:0 0}
/* 첫 화면 원 애니메이션도 화면에 다 들어온 뒤(in)에 시작 — 그 전에는 첫 장면에서 멈춰 있음 */
.gs.hero:not(.in) .strip,.gs.hero:not(.in) .pop{animation-play-state:paused}
.gs .strip,.gs .pop{position:absolute;top:0;left:0;width:160px;height:160px;border-radius:50%}
/* 흐름 0~1.0s → 정렬 1.0~2.0s → 위아래 원 튀어나옴 ~2.0s → 가운데 주황 2.0~2.8s */
.gs .strip{background:var(--ink);transform:translate(var(--ex),178px);animation:gsStrip 2s both}
.gs .strip.me{background:var(--accent);animation:gsStrip 2s both,gsOrange 2.8s ease-out both}
.gs .pop{background:var(--ink);transform:translate(var(--gx),var(--gy));animation:gsPopIn 2s both}
@keyframes gsStrip{0%{transform:translate(var(--sx),98px);width:320px;height:320px;animation-timing-function:linear}50%{transform:translate(calc(var(--sx) - 140px),98px);width:320px;height:320px;animation-timing-function:cubic-bezier(.65,0,.15,1)}100%{transform:translate(var(--ex),178px);width:160px;height:160px}}
@keyframes gsPopIn{0%,72%{transform:translate(var(--gx),var(--gy)) scale(0);animation-timing-function:cubic-bezier(.2,.8,.2,1)}100%{transform:translate(var(--gx),var(--gy)) scale(1)}}
@keyframes gsOrange{0%,71%{background:var(--ink)}100%{background:var(--accent)}}

.gs .stats{grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr))}
.gs .stat{display:flex;flex-direction:column;gap:18px}
.gs .big{font-size:clamp(72px,8vw,96px);line-height:1;font-weight:700;letter-spacing:-.05em;font-variant-numeric:tabular-nums}
.gs .lbl{font-size:16px;font-weight:700}
.gs .d100{display:grid;grid-template-columns:repeat(10,12px);gap:6px}
.gs .d100 span{width:12px;height:12px;border-radius:50%;background:var(--line)}
.gs .d12{display:grid;grid-template-columns:repeat(6,34px);gap:10px}
.gs .d12 span{width:34px;height:34px;border-radius:50%;border:2px solid var(--ink)}
.gs .on{background:var(--accent)!important;border-color:var(--accent)!important}
.gs .pair{display:flex;align-items:flex-end;gap:6px;height:78px}
.gs .pair span{width:78px;height:78px;border-radius:50%}

.gs .chart-head{grid-template-columns:repeat(auto-fit,minmax(min(100%,360px),1fr));gap:24px 48px}
.gs .legend{display:flex;flex-wrap:wrap;gap:22px;font-size:14px;font-weight:500}
.gs .legend>span{display:inline-flex;align-items:center;gap:8px}
.gs .mk{width:14px;height:14px;border-radius:50%;flex-shrink:0;display:inline-block}
.gs .groups{grid-template-columns:repeat(auto-fit,minmax(min(100%,480px),1fr));gap:40px 64px}
.gs .grp h3{font-size:15px;font-weight:900;margin-bottom:10px}
.gs .row{display:grid;grid-template-columns:96px minmax(0,1fr) 96px;gap:14px;align-items:center;min-height:44px;border-bottom:1px solid var(--line)}
.gs .row .nm{font-size:14px}
.gs .row .plot{position:relative;height:22px}
.gs .row .track{position:absolute;left:0;right:0;top:10px;height:2px;background:var(--line)}
.gs .row .dd{position:absolute;top:0;width:22px;height:22px;margin-left:-11px;border-radius:50%}
.gs .row .val{font-size:14px;text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
.gs .row .val span{color:var(--muted)}
/* 비율 아래 인원 (분모). 트랙~값 칸 아래에 오른쪽 정렬, 좁은 화면에선 두 덩어리가 줄바꿈 */
.gs .row{row-gap:0;padding-top:8px}
.gs .row .cnt{grid-column:2/4;text-align:right;font-size:12px;line-height:1.5;color:var(--muted);padding:2px 0 8px;font-variant-numeric:tabular-nums}
.gs .row .cnt span{white-space:nowrap}

.gs.reveal{grid-template-columns:repeat(auto-fit,minmax(min(100%,440px),1fr));gap:40px 64px;align-items:end}
.gs.reveal .kick{font-size:20px;font-weight:500;color:var(--muted)}
.gs.reveal h2{font-size:clamp(44px,5vw,64px);line-height:1.12;font-weight:900;letter-spacing:-.045em;margin-top:20px}
.gs .lines{border-top:2px solid var(--ink)}
.gs .lines p{padding:18px 0;font-size:17px;line-height:1.6;border-bottom:1px solid var(--line)}
.gs .lines p:last-child{border-bottom:0;font-weight:700}

.gs.step{background:var(--ink);color:var(--white);border-radius:28px;padding:64px 56px;grid-template-columns:repeat(auto-fit,minmax(min(100%,380px),1fr));gap:40px;align-items:center;overflow:hidden}
@media (max-width:640px){.gs.step{padding:40px 24px}}
.gs.step h2{font-size:clamp(40px,4.5vw,56px);line-height:1.15;font-weight:900;letter-spacing:-.04em}
.gs.step p{font-size:18px;line-height:1.65;color:var(--bg);max-width:24em;margin-top:22px}
.gs.step .cta{display:inline-flex;align-items:center;min-height:52px;padding:0 26px;margin-top:22px;border-radius:999px;background:var(--accent);color:var(--ink);text-decoration:none;font-size:16px;font-weight:700}
.gs.step .cta:hover{color:var(--ink);filter:brightness(1.08)}
.gs .circles{display:flex;justify-content:flex-end;align-items:flex-end;gap:14px;height:220px}
.gs .circles span{border-radius:50%;border:2px solid var(--white);flex-shrink:0}
.gs .circles .c4{border:0;background:var(--accent)}
</style>
"""
c.html(PAGE_CSS)

# ---------------------------------------------------------------
# 1. 질문 (첫 화면) — 왼쪽 글, 오른쪽 원 그래픽
# ---------------------------------------------------------------
sx, ex = [-240, 98, 436, 774, 1112], [-700, -520, 0, 178, 356]
strips = "".join(
    f'<span class="strip{" me" if i == 3 else ""}" style="--sx:{x}px;--ex:{e}px"></span>'
    for i, (x, e) in enumerate(zip(sx, ex))
)
pops = "".join(
    f'<span class="pop" style="--gx:{x}px;--gy:{y}px;animation-delay:{i * 0.04:.2f}s"></span>'
    for i, (x, y) in enumerate([(0, 0), (178, 0), (356, 0), (0, 356), (178, 356), (356, 356)])
)
c.html(f"""
<section class="gs grid hero" data-reveal aria-labelledby="q">
  <div style="display:flex;flex-direction:column;gap:28px">
    <h1 id="q">백만장자가<br>되고 싶나요?</h1>
    <p class="lead">부자들은 뭔가 특별한 습관이 있을 것 같죠. 그래서 {N['total'] // 10000}만 명의 습관 12개를 직접 비교해 봤어요.</p>
    <p class="cap" style="margin-top:-16px">※ Kaggle에 공개된 가상(합성) 데이터예요</p>
    <p class="first"><i aria-hidden="true"></i>이번 주 결정: 가계부 + 습관 기록부터. 이 데이터에서는 백만장자만의 습관이 보이지 않았거든요.</p>
  </div>
  <div class="stage" id="stage" role="img" aria-label="3줄 3칸으로 놓인 검은 원 가운데 하나가 주황색인 그림. 주황 원은 나를 뜻해요.">
    <div class="stage-in">{strips}{pops}</div>
  </div>
</section>
<script>
(function () {{
  var s = document.getElementById('stage'); if (!s) return;
  function fit() {{ s.firstElementChild.style.transform = 'scale(' + (s.clientWidth / 516) + ')'; }}
  fit(); window.addEventListener('resize', fit);
}})();
</script>
""", js=True)
c.gap(120)

# ---------------------------------------------------------------
# 2. 숫자 3개
# ---------------------------------------------------------------
mil_pct = N["millionaire_pct"]
on100 = int(N["millionaires"] * 100 // N["total"])  # 100명으로 줄였을 때 (42,492명 → 42명)
dots100 = "".join(
    f'<span class="pp{" on" if i < on100 else ""}" style="--d:{(i // 10 + i % 10) * 0.025:.3f}s"></span>'
    for i in range(100)
)
n_over = len(N["over"])
dots12 = "".join(
    f'<span class="pp{" on" if i < n_over else ""}" style="--d:{i * 0.06:.2f}s"></span>' for i in range(12)
)
big = N["biggest"]
who = "백만장자가" if big["diff"] >= 0 else "아닌 사람이"
chance_note = (f" (우연 범위 ±{c.p1(N['chance_pp'])}%p 안의 차이)"
               if abs(big["diff"]) < N["chance_pp"] else "")
cap12 = (f"차이가 큰 습관만 주황으로 채워져요. 12개 모두 {c.THRESHOLD_PP}%p에 못 미쳐 비어 있어요"
         if n_over == 0 else "차이가 큰 습관만 주황으로 채워져요")
c.html(f"""
<section class="gs" data-reveal aria-labelledby="num" style="display:flex;flex-direction:column;gap:40px">
  <div class="sec-head"><h2 id="num" class="h2">먼저, 숫자 세 개만 볼게요</h2></div>
  <div class="grid stats">
    <div class="stat">
      <p class="big">{c.odometer(c.p1(mil_pct))}<span class="u">%</span></p>
      <p class="lbl">{N['total'] // 10000}만 명 중 백만장자</p>
      <div class="d100" role="img" aria-label="100명 중 {on100}명이 백만장자">{dots100}</div>
      <p class="cap">100명 중 주황 점 {on100}개가 백만장자예요</p>
    </div>
    <div class="stat">
      <p class="big">{c.odometer(str(n_over))}<span class="u">/12</span></p>
      <p class="lbl">두 그룹 차이가 {c.THRESHOLD_PP}%p 넘는 습관</p>
      <div class="d12" role="img" aria-label="습관 12개 중 {n_over}개">{dots12}</div>
      <p class="cap">{cap12}</p>
    </div>
    <div class="stat">
      <p class="big">{c.odometer(f"{abs(big['diff']):.2f}")}<span class="u">%p</span></p>
      <p class="lbl">가장 크게 벌어진 차이</p>
      <div class="pair" aria-hidden="true">
        <span class="slideL" style="background:var(--accent)"></span>
        <span class="slideR" style="border:2px dashed var(--unit)"></span>
      </div>
      <p class="cap">{big['label']} · {who} {abs(big['diff']):.2f}%p 더 많았어요{chance_note}</p>
    </div>
  </div>
</section>
""")
c.gap(120)

# ---------------------------------------------------------------
# 3. 대표 차트 — 점 2개 비교 차트 (DESIGN.md 5장)
# ---------------------------------------------------------------
def rows(group: str) -> str:
    out = []
    for i, h in enumerate([h for h in N["habits"] if h["group"] == group]):
        d = i * 0.12
        m, o = h["mil"], h["non"]
        tip = (f"{h['label']} — 백만장자 {c.p1(m['pct'])}% ({c.fmt(m['yes'])}/{c.fmt(m['n'])}명), "
               f"아닌 사람 {c.p1(o['pct'])}% ({c.fmt(o['yes'])}/{c.fmt(o['n'])}명)")
        out.append(f"""
<div class="row" role="img" aria-label="{tip}" title="{tip}">
  <span class="nm">{h['label']}</span>
  <div class="plot">
    <div class="track" style="--d:{d:.2f}s"></div>
    <span class="dd" style="left:{o['pct']:.2f}%;border:2px solid var(--ink);--d:{d + 0.35:.2f}s"></span>
    <span class="dd" style="left:{m['pct']:.2f}%;background:var(--accent);--d:{d + 0.25:.2f}s"></span>
  </div>
  <span class="val">{c.p1(m['pct'])}% · <span>{c.p1(o['pct'])}%</span></span>
  <span class="cnt"><span>{c.fmt(m['yes'])} / {c.fmt(m['n'])}명</span> · <span>{c.fmt(o['yes'])} / {c.fmt(o['n'])}명</span></span>
</div>""")
    return "".join(out)


books = next(h for h in N["habits"] if h["col"] == "books_read_per_year")
c.html(f"""
<section class="gs" data-reveal aria-labelledby="chart" style="display:flex;flex-direction:column;gap:36px">
  <div class="grid chart-head sec-head">
    <h2 id="chart" class="h2">습관 12개 모두,<br>두 그룹의 점이 거의 겹쳤어요</h2>
    <div style="display:flex;flex-direction:column;gap:14px">
      <p style="font-size:15px;line-height:1.7">한 줄이 습관 하나예요. 선의 왼쪽 끝이 0%, 오른쪽 끝이 100%이고, 각 그룹에서 그 습관을 하는 사람의 비율에 점을 찍었어요. 두 점이 멀수록 차이가 크고, 붙어 있으면 차이가 거의 없다는 뜻이에요.</p>
      <div class="legend">
        <span><i class="mk" style="background:var(--accent)" aria-hidden="true"></i>백만장자 {c.fmt(N['millionaires'])}명</span>
        <span><i class="mk" style="border:2px solid var(--ink)" aria-hidden="true"></i>아닌 사람 {c.fmt(N['non'])}명</span>
      </div>
    </div>
  </div>
  <div class="grid groups">
    <div class="grp"><h3>돈 습관</h3>{rows("money")}</div>
    <div class="grp"><h3>생활 습관</h3>{rows("life")}</div>
  </div>
  <p class="cap">오른쪽 숫자는 ‘백만장자 · 아닌 사람’ 순서예요. 독서는 빈 값을 뺀 {c.fmt(books['mil']['n'])}명 · {c.fmt(books['non']['n'])}명으로 계산했어요.</p>
</section>
""")
c.gap(120)

# ---------------------------------------------------------------
# 4. 결론 3줄
# ---------------------------------------------------------------
max_abs = max(abs(h["diff"]) for h in N["habits"])
ceil_pp = (int(max_abs * 10) + 1) / 10  # 0.43 → 0.5
c.html(f"""
<section class="gs grid reveal" aria-labelledby="reveal">
  <div>
    <p class="kick">알고 보니,</p>
    <h2 id="reveal">이 데이터에서는<br>부자 습관이 따로<br>보이지 않았어요.</h2>
  </div>
  <div class="lines">
    <p>습관 12개 모두, 백만장자와 아닌 사람의 차이가 {ceil_pp:.1f}%p도 되지 않았어요. 가장 큰 차이도 {big['label']}의 {abs(big['diff']):.2f}%p였어요.</p>
    <p>이 인원이면 우연으로도 ±{c.p1(N['chance_pp'])}%p쯤 차이가 생겨요. 이 데이터에서는 ‘백만장자만의 습관’이 보이지 않았어요.</p>
    <p>그래서 이번 주는 가계부와 습관 기록부터 매일 해 봐요.</p>
  </div>
</section>
""")
c.gap(120)

# ---------------------------------------------------------------
# 5. 마무리
# ---------------------------------------------------------------
c.html("""
<section class="gs grid step" data-reveal aria-labelledby="step">
  <div>
    <h2 id="step">천 리 길도<br>한 걸음부터.</h2>
    <p>데이터로 고를 습관이 없어서, 나는 가장 쉬운 기록부터 해 보기로 했어요. 기록하는 사람과 안 하는 사람은 얼마나 다를까요?</p>
    <a class="cta" href="./record" target="_self">기록 한 걸음 보러 가기</a>
  </div>
  <div class="circles" aria-hidden="true">
    <span class="pp" style="width:40px;height:40px"></span>
    <span class="pp" style="width:72px;height:72px;--d:.15s"></span>
    <span class="pp" style="width:120px;height:120px;--d:.3s"></span>
    <span class="pp c4" style="width:200px;height:200px;--d:.5s"></span>
  </div>
</section>
""")
c.gap(120)

# ---------------------------------------------------------------
# 6. 출처 · 한계
# ---------------------------------------------------------------
c.html(f"""
<footer class="gs foot">
  <p><strong>출처</strong><br>Kaggle Millionaire Habits Dataset, 가상 인물 {N['total'] // 10000}만 명. 백만장자 = 순자산 100만 달러 이상.</p>
  <p><strong>한계</strong><br>가상 데이터라 백만장자 비율({c.p1(mil_pct)}%)도 실제보다 훨씬 높아요. 습관과 백만장자 여부가 함께 나타날 뿐, 원인과 결과는 아니에요.</p>
</footer>
""")
c.reveal_script()
