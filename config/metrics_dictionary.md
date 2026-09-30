# Metrics dictionary

| Field | Meaning | Formula / source |
|---|---|---|
| assets | 총자산 | OpenDART XBRL |
| cash | 현금및현금성자산 | OpenDART XBRL |
| receivables | 매출채권 | OpenDART XBRL |
| inventory | 재고자산 | OpenDART XBRL |
| ppe | 유형자산 | OpenDART XBRL |
| liabilities | 총부채 | OpenDART XBRL |
| equity | 자본총계 | OpenDART XBRL |
| revenue | 매출액 | OpenDART XBRL |
| gross_profit | 매출총이익 | OpenDART XBRL |
| operating_income | 영업이익 | OpenDART XBRL |
| pretax_income | 세전이익 | OpenDART XBRL |
| net_income | 당기순이익 | OpenDART XBRL |
| cfo/cfi/cff | 영업/투자/재무활동 현금흐름 | OpenDART XBRL |
| gross_margin | 매출총이익률 | gross_profit / revenue |
| operating_margin | 영업이익률 | operating_income / revenue |
| net_margin | 순이익률 | net_income / revenue |
| roa | ROA | net_income / average assets |
| roe | ROE | net_income / average equity |
| debt_ratio | 부채비율 | liabilities / equity |
| equity_ratio | 자기자본비율 | equity / assets |
| asset_turnover | 총자산회전율 | revenue / average assets |
| cfo_net_income | CFO/순이익 | cfo / net_income |

Interim reports prefer thstrm_add_amount when available; annual reports prefer thstrm_amount. Consolidated statements are preferred when both consolidated and separate statements are returned.
