# 이마트 DART Financial Agent & Dashboard

[![🔗 대시보드 바로가기](https://img.shields.io/badge/%F0%9F%94%97_%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C-%EB%B0%94%EB%A1%9C%EA%B0%80%EA%B8%B0-1f6feb?style=for-the-badge)](https://hsc-class02.github.io/sy_emart/)

OpenDART API를 이용하여 **이마트(139480)**의 사업보고서·반기보고서·분기보고서를 수집하고, 주요 재무수치와 재무비율을 계산하여 GitHub Pages Dashboard로 제공합니다.

## 프로젝트 범위
- 대상 기업: 이마트 / 139480
- 공시자료: 사업보고서 / 반기보고서 / 분기보고서
- 공시목록 수집 시작: **2010년**
- 자동 업데이트: **매월 1일 09:15 KST**
- Dashboard: GitHub Pages
- 자동화: GitHub Actions
- API 인증키: GitHub Repository Secret `DART_API_KEY`

> 중요: 2010년부터 정기보고서 **공시목록과 DART 원문 링크**를 저장하고, 구조화된 XBRL 재무수치는 OpenDART 구조화 재무제표 API가 반환하는 기간부터 자동 추출합니다. 2010~2014년 비-XBRL 원문 계정까지 동일 계정체계로 완전 소급하려면 별도의 원문 XML 계정 매핑을 추가해야 합니다.

## Dashboard
**https://hsc-class02.github.io/sy_emart/**

상단: KPI 카드 / 매출·이익 / 현금흐름 / 수익성 / ROE·ROA 그래프  
하단: **Annual / Half-year / Quarterly(Q1·Q3)** 테이블 및 국내 Peer Firms 테이블

## 주요 재무수치
- 재무상태표: 총자산, 현금및현금성자산, 매출채권, 재고자산, 유형자산, 총부채, 자본총계
- 손익계산서: 매출액, 매출총이익, 영업이익, 세전이익, 당기순이익
- 현금흐름표: CFO, CFI, CFF
- 비율: 매출총이익률, 영업이익률, 순이익률, ROA, ROE, 부채비율, 자기자본비율, 총자산회전율, CFO/순이익

## OpenDART API Key 입력
1. OpenDART에서 API 인증키를 발급합니다.
2. GitHub Repository → **Settings**
3. **Secrets and variables → Actions**
4. **New repository secret**
5. Name: `DART_API_KEY`
6. Secret: 발급받은 OpenDART 인증키
7. 저장합니다.

API 키는 소스코드, README, `.env` 등에 넣지 않습니다.

## 최초 실행
API Secret 저장 후 **Actions → Monthly DART update → Run workflow**를 1회 실행합니다.

자동 생성/갱신 파일:
```
data/raw/filings.csv
data/raw/report_sources.csv
data/raw/financial_statements.csv
data/processed/metrics.csv
data/processed/update_status.csv
docs/index.html
```

이후 매월 1일 자동으로 동일 작업을 수행합니다.

## GitHub Pages
Repository → **Settings → Pages → Source: GitHub Actions**

Pages workflow가 `docs/`를 배포합니다.

## About → Website
Repository 오른쪽 **About → 톱니바퀴 → Website**에 아래 주소를 입력하세요.

`https://hsc-class02.github.io/sy_emart/`

이 항목은 GitHub 관리 UI에서 한 번 수동으로 입력해야 합니다.

## 국내 Peer Firms
| 기업 | 종목코드 | 비교 관점 |
|---|---:|---|
| 롯데쇼핑 | 023530 | 백화점·마트·e커머스 등 종합 유통 |
| 신세계 | 004170 | 백화점·이커머스·유통 |
| GS리테일 | 007070 | 편의점·슈퍼·홈쇼핑 등 유통 |
| BGF리테일 | 282330 | 편의점 중심 소매 유통 |
| 현대백화점 | 069960 | 백화점·면세·유통 |

Peer는 국내 상장 유통기업 가운데 사업 채널이 겹치는 기업을 중심으로 구성했습니다. 사업구조가 완전히 동일하지 않으므로 채널 믹스와 사업부 구성을 함께 확인합니다.

## Agent 구조
```
OpenDART API
  ↓ corpCode.xml
이마트 corp_code 탐색
  ↓ list.json
2010~현재 정기보고서 목록 + DART 원문 링크
  ↓ fnlttSinglAcntAll.json
주요 재무계정 추출 → 재무비율 계산 → metrics.csv
  ↓
Dashboard HTML → GitHub Pages
```

## ZIP
업로드용 ZIP은 **hidden file / hidden directory를 포함하지 않도록** 별도로 생성합니다. `.github` workflow는 Repository에 별도로 배치됩니다.

## Data source
- OpenDART: https://opendart.fss.or.kr/
- DART: https://dart.fss.or.kr/
