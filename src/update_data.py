import os, io, re, zipfile, requests, pandas as pd, xml.etree.ElementTree as ET
from pathlib import Path
from datetime import date

API='https://opendart.fss.or.kr/api'
KEY=os.environ.get('DART_API_KEY','').strip()
ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/'data/raw'; OUT=ROOT/'data/processed'
REPORTS={'annual':'11011','half-year':'11012','quarterly-q1':'11013','quarterly-q3':'11014'}
METRICS={
 'assets':['ifrs-full_Assets','자산총계'],'cash':['ifrs-full_CashAndCashEquivalents','현금및현금성자산'],
 'receivables':['ifrs-full_TradeAndOtherCurrentReceivables','매출채권'], 'inventory':['ifrs-full_Inventories','재고자산'],
 'ppe':['ifrs-full_PropertyPlantAndEquipment','유형자산'], 'liabilities':['ifrs-full_Liabilities','부채총계'],
 'equity':['ifrs-full_Equity','자본총계'], 'revenue':['ifrs-full_Revenue','매출액','수익(매출액)'],
 'gross_profit':['ifrs-full_GrossProfit','매출총이익'], 'operating_income':['dart_OperatingIncomeLoss','영업이익'],
 'pretax_income':['ifrs-full_ProfitLossBeforeTax','법인세비용차감전순이익'], 'net_income':['ifrs-full_ProfitLoss','당기순이익'],
 'cfo':['ifrs-full_CashFlowsFromUsedInOperatingActivities','영업활동현금흐름'],
 'cfi':['ifrs-full_CashFlowsFromUsedInInvestingActivities','투자활동현금흐름'],
 'cff':['ifrs-full_CashFlowsFromUsedInFinancingActivities','재무활동현금흐름'],
}

def get(path, **params):
    r=requests.get(f'{API}/{path}', params={'crtfc_key':KEY,**params}, timeout=60); r.raise_for_status(); return r

def corp_code():
    z=zipfile.ZipFile(io.BytesIO(get('corpCode.xml').content)); root=ET.fromstring(z.read(z.namelist()[0]))
    hits=[]
    for x in root.findall('list'):
        name=(x.findtext('corp_name') or '').strip(); stock=(x.findtext('stock_code') or '').strip()
        if name=='이마트' or stock=='139480': hits.append(x.findtext('corp_code'))
    if not hits: raise RuntimeError('이마트 corp_code를 찾지 못했습니다.')
    return hits[0]

def filings(corp):
    # DART list API supports historical filing search; split by year for reliability.
    rows=[]
    for y in range(2010,date.today().year+1):
        j=get('list.json',corp_code=corp,bgn_de=f'{y}0101',end_de=f'{y}1231',pblntf_ty='A',page_count=100).json()
        if j.get('status') not in ('000','013'): raise RuntimeError(j)
        for x in j.get('list',[]):
            if any(k in x['report_nm'] for k in ('사업보고서','반기보고서','분기보고서')): rows.append(x)
    pd.DataFrame(rows).to_csv(RAW/'filings.csv',index=False,encoding='utf-8-sig')
    return rows

def financials(corp):
    # Structured full financial statements are officially provided from 2015 onward.
    rows=[]
    for y in range(2015,date.today().year+1):
      for kind,code in REPORTS.items():
       for fs in ('CFS','OFS'):
        j=get('fnlttSinglAcntAll.json',corp_code=corp,bsns_year=y,reprt_code=code,fs_div=fs).json()
        if j.get('status')=='000':
            for x in j['list']: x.update(period_kind=kind,fs_div=fs); rows.append(x)
            break
        if j.get('status') not in ('013','000'): print('WARN',y,kind,fs,j.get('message'))
    df=pd.DataFrame(rows); df.to_csv(RAW/'financial_statements.csv',index=False,encoding='utf-8-sig'); return df

def num(x):
    if pd.isna(x): return None
    s=re.sub(r'[^0-9.-]','',str(x));
    try:return float(s) if s else None
    except:return None

def extract(df):
    if df.empty: return pd.DataFrame()
    out=[]
    for (y,k,fs),g in df.groupby(['bsns_year','period_kind','fs_div']):
      row={'year':int(y),'period':k,'fs_div':fs}
      for key,aliases in METRICS.items():
        z=g[g['account_id'].isin(aliases)]
        if z.empty: z=g[g['account_nm'].astype(str).isin(aliases)]
        row[key]=num(z.iloc[0]['thstrm_add_amount'] if (not z.empty and k!='annual' and pd.notna(z.iloc[0].get('thstrm_add_amount'))) else (z.iloc[0]['thstrm_amount'] if not z.empty else None))
      out.append(row)
    x=pd.DataFrame(out).sort_values(['period','year'])
    for c in ['gross_profit','operating_income','net_income']:
        x[c.replace('_income','')+'_margin' if c!='gross_profit' else 'gross_margin']=x[c]/x['revenue']
    x['debt_ratio']=x['liabilities']/x['equity']; x['equity_ratio']=x['equity']/x['assets']
    x['asset_turnover']=x['revenue']/x.groupby('period')['assets'].transform(lambda s:(s+s.shift())/2)
    x['roe']=x['net_income']/x.groupby('period')['equity'].transform(lambda s:(s+s.shift())/2)
    x['roa']=x['net_income']/x.groupby('period')['assets'].transform(lambda s:(s+s.shift())/2)
    x['cfo_net_income']=x['cfo']/x['net_income']
    OUT.mkdir(parents=True,exist_ok=True); x.to_csv(OUT/'metrics.csv',index=False,encoding='utf-8-sig'); return x

if __name__=='__main__':
    if not KEY: raise SystemExit('DART_API_KEY GitHub Secret을 설정하세요.')
    RAW.mkdir(parents=True,exist_ok=True); corp=corp_code(); print('corp_code',corp)
    filings(corp); extract(financials(corp))
