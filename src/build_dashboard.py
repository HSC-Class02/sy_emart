from pathlib import Path
import html
import pandas as pd
import plotly.express as px
import plotly.io as pio

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "metrics.csv"
STATUS = ROOT / "data" / "processed" / "update_status.csv"
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)

PEERS = [
    ("롯데쇼핑", "023530", "백화점·마트·e커머스 등 종합 유통"),
    ("신세계", "004170", "백화점·이커머스·유통"),
    ("GS리테일", "007070", "편의점·슈퍼·홈쇼핑 등 유통"),
    ("BGF리테일", "282330", "편의점 중심 소매 유통"),
    ("현대백화점", "069960", "백화점·면세·유통"),
]

METRIC_LABELS = {
    "revenue": "매출액", "gross_profit": "매출총이익",
    "operating_income": "영업이익", "net_income": "당기순이익",
    "assets": "총자산", "cash": "현금및현금성자산",
    "receivables": "매출채권", "inventory": "재고자산",
    "ppe": "유형자산", "liabilities": "총부채", "equity": "자본총계",
    "cfo": "영업활동현금흐름", "cfi": "투자활동현금흐름", "cff": "재무활동현금흐름",
    "gross_margin": "매출총이익률", "operating_margin": "영업이익률",
    "net_margin": "순이익률", "roe": "ROE", "roa": "ROA",
    "debt_ratio": "부채비율", "equity_ratio": "자기자본비율",
    "asset_turnover": "총자산회전율", "cfo_net_income": "CFO/순이익",
}

TABLE_COLS = [
    "year", "revenue", "gross_profit", "operating_income", "net_income",
    "assets", "liabilities", "equity", "cfo", "gross_margin",
    "operating_margin", "net_margin", "roe", "roa", "debt_ratio",
    "equity_ratio", "asset_turnover", "cfo_net_income",
]

if DATA.exists():
    df = pd.read_csv(DATA)
    if "period_kind" in df.columns and "period" not in df.columns:
        df = df.rename(columns={"period_kind": "period"})
else:
    df = pd.DataFrame(columns=["year", "period"] + list(METRIC_LABELS))

if STATUS.exists():
    _status_df = pd.read_csv(STATUS)
    status = _status_df.iloc[0].to_dict() if not _status_df.empty else {}
else:
    status = {}

def ratio_cols(cols):
    return [c for c in cols if c in ("gross_margin", "operating_margin", "net_margin", "roe", "roa", "debt_ratio", "equity_ratio", "cfo_net_income")]

def fmt_table(z, cols):
    if z.empty:
        return '<div class="empty">아직 데이터가 없습니다. GitHub Actions에서 <b>Monthly DART update</b>를 실행하세요.</div>'
    cols = [c for c in cols if c in z.columns]
    out = z[cols].copy()
    out = out.rename(columns={c: METRIC_LABELS.get(c, c) for c in cols})
    for c in out.columns:
        if c == "year":
            continue
        if c in [METRIC_LABELS.get(x) for x in ratio_cols(cols)]:
            out[c] = out[c].map(lambda x: "" if pd.isna(x) else f"{x*100:,.2f}%")
        else:
            out[c] = out[c].map(lambda x: "" if pd.isna(x) else f"{x:,.0f}")
    return out.to_html(index=False, classes="data", border=0, escape=False)

def chart(data, ycols, title, percent=False):
    if data.empty:
        return '<div class="empty">데이터가 아직 수집되지 않았습니다.</div>'
    present = [c for c in ycols if c in data.columns]
    if not present:
        return '<div class="empty">해당 지표 데이터가 없습니다.</div>'
    long = data.melt(id_vars=["year"], value_vars=present, var_name="metric", value_name="value")
    long["metric"] = long["metric"].map(METRIC_LABELS).fillna(long["metric"])
    fig = px.line(long, x="year", y="value", color="metric", markers=True, title=title)
    fig.update_layout(template="plotly_white", margin=dict(l=45, r=20, t=55, b=35),
                      legend_title_text="", hovermode="x unified", height=360)
    if percent:
        fig.update_yaxes(tickformat=".1%")
    return pio.to_html(fig, full_html=False, include_plotlyjs="cdn")

annual = df[df.get("period", pd.Series(dtype=str)) == "annual"].copy()
half = df[df.get("period", pd.Series(dtype=str)) == "half-year"].copy()
q1 = df[df.get("period", pd.Series(dtype=str)) == "quarterly-q1"].copy()
q3 = df[df.get("period", pd.Series(dtype=str)) == "quarterly-q3"].copy()

latest = annual.sort_values("year").tail(1)
if latest.empty:
    kpi_html = "".join(f'<div class="kpi"><span>{label}</span><strong>—</strong></div>'
                       for label in ["매출액", "영업이익", "당기순이익", "영업현금흐름"])
else:
    r = latest.iloc[0]
    kpi_html = "".join(
        f'<div class="kpi"><span>{METRIC_LABELS[c]}</span><strong>{("" if pd.isna(r.get(c)) else r.get(c)):,.0f}</strong></div>'
        for c in ["revenue", "operating_income", "net_income", "cfo"]
    )

peer_rows = "".join(
    f"<tr><td>{html.escape(n)}</td><td>{code}</td><td>{html.escape(desc)}</td></tr>"
    for n, code, desc in PEERS
)

updated = html.escape(str(status.get("updated_at_utc", "아직 실행되지 않음")))
filing_count = int(status.get("filing_count", 0) or 0)

html_doc = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>이마트 DART Financial Dashboard</title>
<style>
:root{{--bg:#f4f7fb;--card:#fff;--ink:#182230;--muted:#667085;--line:#e5e7eb}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
main{{max-width:1500px;margin:auto;padding:28px 24px 70px}}
.hero{{background:linear-gradient(135deg,#122b49,#274c77);color:#fff;padding:30px;border-radius:22px;box-shadow:0 12px 35px #122b4928}}
.hero h1{{margin:0 0 8px;font-size:30px}} .hero p{{margin:0;color:#dce8f6}}
.meta{{margin-top:18px;font-size:13px;color:#c7d6e7}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:18px 0}}
.kpi{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;box-shadow:0 5px 20px #1018280b}}
.kpi span{{display:block;color:var(--muted);font-size:13px;margin-bottom:8px}} .kpi strong{{font-size:23px}}
.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin:18px 0}}
section,.chart{{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:16px;box-shadow:0 5px 20px #1018280b;overflow:auto}}
h2{{font-size:19px;margin:6px 0 15px}}
.data,.peer{{border-collapse:separate;border-spacing:0;width:100%;font-size:13px;min-width:950px}}
.data th,.peer th{{position:sticky;top:0;background:#17365d;color:#fff;font-weight:600}}
.data th,.data td,.peer th,.peer td{{padding:10px 12px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}}
.data th:first-child,.data td:first-child,.peer th:first-child,.peer td:first-child{{text-align:left}}
.data tr:hover td,.peer tr:hover td{{background:#f8fafc}}
.empty{{padding:35px;text-align:center;color:var(--muted);background:#f8fafc;border-radius:12px}}
.note{{color:var(--muted);font-size:12px;line-height:1.6}}
.badge{{display:inline-block;background:#eef4fb;color:#17365d;border:1px solid #d9e5f2;border-radius:999px;padding:5px 9px;font-size:12px}}
@media(max-width:900px){{.kpis{{grid-template-columns:repeat(2,1fr)}}.grid{{grid-template-columns:1fr}}}}
@media(max-width:560px){{main{{padding:16px 12px}}.kpis{{grid-template-columns:1fr}}}}
</style>
</head>
<body><main>
<div class="hero"><h1>이마트 DART Financial Dashboard</h1>
<p>사업보고서 · 반기보고서 · 분기보고서 기반 재무제표 및 재무비율 분석</p>
<div class="meta">OpenDART 자동수집 · 2010년 이후 공시목록 · 구조화 XBRL 재무수치 · 월 1회 자동 갱신</div></div>
<div class="kpis">{kpi_html}</div>
<div class="grid">
<div class="chart">{chart(annual, ["revenue","operating_income","net_income"], "Annual: 매출·이익 추이")}</div>
<div class="chart">{chart(annual, ["cfo","cfi","cff"], "Annual: 현금흐름")}</div>
<div class="chart">{chart(annual, ["gross_margin","operating_margin","net_margin"], "Annual: 이익률", True)}</div>
<div class="chart">{chart(annual, ["roe","roa"], "Annual: ROE · ROA", True)}</div>
</div>
<section><h2>Annual</h2>{fmt_table(annual.sort_values("year", ascending=False), TABLE_COLS)}</section>
<section><h2>Half-year</h2>{fmt_table(half.sort_values("year", ascending=False), TABLE_COLS)}</section>
<section><h2>Quarterly</h2><h3>Q1</h3>{fmt_table(q1.sort_values("year", ascending=False), TABLE_COLS)}<h3>Q3</h3>{fmt_table(q3.sort_values("year", ascending=False), TABLE_COLS)}</section>
<section><h2>국내 Peer Firms</h2>
<table class="peer"><tr><th>기업</th><th>종목코드</th><th>비교 관점</th></tr>{peer_rows}</table>
<p class="note">Peer는 국내 상장 유통기업 가운데 사업 채널이 겹치는 기업을 중심으로 구성했습니다. 이마트와 사업구조가 완전히 동일하지 않으므로 채널 믹스와 사업부 구성을 함께 확인하세요.</p>
</section>
<section><h2>데이터·자동화 상태</h2>
<p><span class="badge">수집된 정기보고서 {filing_count:,}건</span> <span class="badge">마지막 실행 {updated}</span></p>
<p class="note">2010년 이후 사업·반기·분기보고서의 공시 메타데이터와 DART 원문 링크를 저장합니다. 구조화 XBRL 재무수치는 OpenDART의 구조화 재무제표 API가 반환하는 기간부터 자동 추출합니다. 과거 비-XBRL 원문 수치까지 동일 계정으로 소급하려면 별도의 원문 XML 계정 매핑이 필요합니다.</p>
</section>
</main></body></html>"""
(DOCS / "index.html").write_text(html_doc, encoding="utf-8")
