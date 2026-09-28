from pathlib import Path
import pandas as pd, plotly.express as px, plotly.io as pio
ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'data/processed/metrics.csv'; DOCS=ROOT/'docs'; DOCS.mkdir(exist_ok=True)
PEERS=[('롯데쇼핑','023530','백화점·마트·e커머스 등 종합 유통'),('GS리테일','007070','편의점·슈퍼 등 오프라인 유통'),('BGF리테일','282330','편의점 중심 소매 유통')]
if D.exists(): df=pd.read_csv(D)
else: df=pd.DataFrame(columns=['year','period','revenue','operating_income','net_income','cfo','assets','liabilities','equity','gross_margin','operating_margin','net_margin','roe','roa','debt_ratio','equity_ratio','asset_turnover','cfo_net_income'])
ann=df[df.period=='annual'].copy() if len(df) else df
charts=[]
for cols,title in [(['revenue','operating_income','net_income'],'매출·이익 추이'),(['cfo'],'영업현금흐름'),(['operating_margin','roe','roa'],'수익성 지표')]:
    if not ann.empty:
      long=ann.melt(id_vars='year',value_vars=[c for c in cols if c in ann],var_name='metric',value_name='value')
      charts.append(pio.to_html(px.line(long,x='year',y='value',color='metric',markers=True,title=title),full_html=False,include_plotlyjs='cdn'))

def table(period,title):
    z=df[df.period==period].sort_values('year',ascending=False) if len(df) else df
    keep=[c for c in ['year','fs_div','revenue','gross_profit','operating_income','net_income','cfo','assets','liabilities','equity','gross_margin','operating_margin','net_margin','roe','roa','debt_ratio','equity_ratio','asset_turnover','cfo_net_income'] if c in z]
    return f'<h2>{title}</h2>'+z[keep].to_html(index=False,classes='data',border=0,float_format=lambda x:f'{x:,.2f}')
peer=''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a,b,c in PEERS)
html=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>이마트 DART Financial Dashboard</title><style>body{{font-family:system-ui,sans-serif;margin:0;background:#f5f7fb;color:#172033}}main{{max-width:1400px;margin:auto;padding:28px}}.hero{{background:white;padding:24px;border-radius:18px;box-shadow:0 6px 24px #0001}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:18px;margin:18px 0}}.chart,section{{background:white;border-radius:18px;padding:14px;overflow:auto;box-shadow:0 6px 24px #0001}}table.data,table.peer{{border-collapse:collapse;width:100%;font-size:13px}}th{{position:sticky;top:0;background:#162f52;color:white}}th,td{{padding:9px 11px;border-bottom:1px solid #e6eaf0;text-align:right;white-space:nowrap}}td:first-child,th:first-child{{text-align:left}}h1,h2{{margin:8px 0 16px}}</style></head><body><main><div class="hero"><h1>이마트 DART Financial Dashboard</h1><p>사업·반기·분기보고서 기반 재무 추세 및 비율 분석. GitHub Actions에서 매월 자동 갱신됩니다.</p></div><div class="grid">{''.join('<div class="chart">'+c+'</div>' for c in charts)}</div><section>{table('annual','Annual')}</section><section>{table('half-year','Half-year')}</section><section>{table('quarterly-q1','Quarterly · Q1')}{table('quarterly-q3','Quarterly · Q3')}</section><section><h2>국내 Peer Firms</h2><table class="peer"><tr><th>기업</th><th>종목코드</th><th>비교 관점</th></tr>{peer}</table><p>사업구조가 완전히 동일하지 않으므로 비교 시 채널 믹스·사업부 구성을 함께 확인하세요.</p></section></main></body></html>'''
(DOCS/'index.html').write_text(html,encoding='utf-8')
