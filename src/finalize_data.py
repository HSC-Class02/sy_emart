from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/"data/raw"
OUT=ROOT/"data/processed"

filings_path=RAW/"filings.csv"
metrics_path=OUT/"metrics.csv"
if filings_path.exists():
    f=pd.read_csv(filings_path)
    if "rcept_no" in f.columns:
        f["dart_url"]="https://dart.fss.or.kr/dsaf001/main.do?rcpNo="+f["rcept_no"].astype(str)
        f[["rcept_no","rcept_dt","report_nm","dart_url"]].to_csv(
            RAW/"report_sources.csv",index=False,encoding="utf-8-sig"
        )
else:
    f=pd.DataFrame()

m=pd.read_csv(metrics_path) if metrics_path.exists() else pd.DataFrame()
OUT.mkdir(parents=True,exist_ok=True)
latest=f["rcept_dt"].max() if not f.empty and "rcept_dt" in f.columns else ""
status=pd.DataFrame([{
    "updated_at_utc":pd.Timestamp.utcnow().isoformat(),
    "filings_from":2010,
    "filing_count":len(f),
    "structured_metric_rows":len(m),
    "latest_filing_date":latest
}])
status.to_csv(OUT/"update_status.csv",index=False,encoding="utf-8-sig")
print(f"Finalized: {len(f)} filings, {len(m)} metric rows")
