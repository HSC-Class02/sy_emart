# 이마트 DART Financial Agent

[![🔗 대시보드 바로가기](https://img.shields.io/badge/%F0%9F%94%97_%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C-%EB%B0%94%EB%A1%9C%EA%B0%80%EA%B8%B0-1f6feb?style=for-the-badge)](https://hsc-class02.github.io/sy_emart/)

OpenDART 정기보고서에서 이마트 재무제표를 수집하고 재무비율을 계산하여 GitHub Pages 대시보드로 배포합니다.

## 중요: 2010~2014
OpenDART `fnlttSinglAcntAll` 구조화 재무제표 API는 2015년 이후 데이터를 제공합니다. 따라서 이 프로젝트는 **2010년부터 공시 목록을 저장**하고, **구조화 재무수치/비율은 2015년부터 자동 추출**합니다. 2010~2014 수치까지 자동화하려면 원문 공시(XBRL/문서) 파서를 별도로 확장해야 합니다.

## 설치/실행
1. OpenDART에서 API 키 발급
2. GitHub 저장소 → Settings → Secrets and variables → Actions → New repository secret
3. 이름 `DART_API_KEY`, 값에 API 키 입력
4. Actions → `Monthly DART update` → Run workflow를 1회 수동 실행
5. Settings → Pages → Source를 **GitHub Actions**로 설정

워크플로우는 매월 1일 09:17 KST에 실행됩니다. 새 공시가 있으면 CSV와 `docs/index.html`을 다시 만들고 커밋합니다.

## 주요 지표
총자산, 현금및현금성자산, 매출채권, 재고자산, 유형자산, 총부채, 자본총계, 매출액, 매출총이익, 영업이익, 세전이익, 당기순이익, CFO/CFI/CFF 및 매출총이익률·영업이익률·순이익률·ROA·ROE·부채비율·자기자본비율·총자산회전율·CFO/순이익을 기본 계산합니다. EBITDA, CAPEX, FCF, 순차입금, ROIC, CCC, PER/PBR/EV-EBITDA는 기업별 XBRL 태그/시장가격/주석 보강이 필요한 항목이라 2단계 확장 대상으로 둡니다.

## 국내 Peer Firms
| 기업 | 종목코드 | 비교 관점 |
|---|---:|---|
| 롯데쇼핑 | 023530 | 백화점·마트·e커머스 등 종합 유통 |
| GS리테일 | 007070 | 편의점·슈퍼 등 오프라인 유통 |
| BGF리테일 | 282330 | 편의점 중심 소매 유통 |

Peer는 사업구조가 완전히 동일하지 않으므로 채널 믹스와 사업부 구성을 함께 보세요.

## About 링크
저장소 오른쪽 **About → 톱니바퀴 → Website**에 `https://hsc-class02.github.io/sy_emart/`를 입력하세요. 이 항목은 저장소 관리자 UI 설정이라 ZIP만으로 자동 변경되지 않습니다.
