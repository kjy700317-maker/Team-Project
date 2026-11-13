# 출처 (Sources)

봉수 안보 긴장도 대시보드에 쓴 데이터와 참고 자료의 출처·이용 조건입니다.

- **이용 목적**: 비상업 교육용 팀 프로젝트(포트폴리오 포함). 상업적으로 쓰지 않습니다.
- **가공 표시**: 대시보드의 사건 선별·제외·분류·점수와 긴장도 지수는 팀이 원자료를 바탕으로 직접 정하고 계산한 것입니다. 각 기관의 공식 자료, 공식 수정본, 공식 평가나 입장이 아닙니다.
- **원문 복제 안 함**: 기사·보고서의 문장, 사진, 표, 그래프는 옮기지 않고 날짜·건수 같은 사실과 팀이 쓴 요약만 씁니다. 언론 기사는 링크만 남깁니다.
- 구분: **1장 = 대시보드 화면·지수 계산에 실제로 쓴 자료**, **2장 = 수집했지만 화면·지수에 쓰지 않은 자료**, 3장 = 방법 참고 문헌, 4장 = 도구·디자인.

---

## 1. 실사용 자료 (대시보드 화면·지수 계산)

긴장도 지수(산출식 v0.1.4)는 A1-A7, B1, B4, C1-C3, E5, F2를 씁니다. C5는 확장 계산에만 씁니다. B3·C4는 지수에는 넣지 않고 2페이지 사건 기록 목록에만 보여 줍니다(지수 밖 표시).

### A 군사행동

| 요소 | 출처 | 이용 조건·표기 |
|---|---|---|
| A1 핵실험 | 북한 6건: Wikipedia, "List of nuclear weapons tests of North Korea." · 연도별 건수(원본 A1 연 단위 집계): Source: Arms Control Association, The Nuclear Testing Tally (https://www.armscontrol.org/factsheets/nuclear-testing-tally), via Our World in Data. | 사실 정보(날짜·장소·위력·건수)만 사용. 레포의 A1 일단위 파일에는 북한 6건만 둠. ACA 연 단위 표는 Arms Control Association 허가(2026-11-10, Arms Control Today 편집장 Carol Giacomo)를 받아 레포 포함·차트 사용 가능. 위키 CC BY-SA 4.0 |
| A2 미사일 발사 | 원자료: James Martin Center for Nonproliferation Studies (CNS), *The CNS North Korea Missile Test Database*, Nuclear Threat Initiative (NTI). https://www.nti.org/analysis/articles/cns-north-korea-missile-test-database/ | 원본 303건 중 294건 사용. 사건 선별·제외·분류·보완은 팀 작업이며 CNS·NTI의 공식 수정본이 아님. 보조 검증: CSIS Missile Threat, 38 North |
| A3 저강도 물리 도발 | Center for Strategic and International Studies (CSIS), *Beyond Parallel*, "Database: North Korean Provocations." https://beyondparallel.csis.org/database-north-korean-provocations/ | 65건 선별(사용 62). 영문 설명문은 옮기지 않음. CSIS 재게시 정책 https://www.csis.org/about/media/reprint-permissions |
| A4 군사훈련 | CSIS, *Beyond Parallel*, "North Korean Provocations and US-ROK Military Exercises." https://beyondparallel.csis.org/north-korean-provocations-us-rok-military-exercises/ · 2021~2026 보완 11건: 사건별 언론·주한미군 보도(부록 A) | 원본에서 40건 선별(사용 39) + 보완 11건 |
| A5 미 전략자산 전개 | National Committee on American Foreign Policy (NCAFP), *Shaping the Future of Security on the Korean Peninsula*. https://ncafp.org/resources/edited-volume-2024-next-generation-korean-peninsula-specialists/ · 일 단위 118행: 사건별 언론·군 발표(부록 B) | 보고서 표·도표 복제 안 함, 사건별 링크 유지 |
| A6 열병식 | 홍민. 2020. *Analysis on the Military Parade Marking the 75th Anniversary of the WPK Foundation* (CO20-26(e)). 통일연구원. https://repo.kinu.or.kr/bitstream/2015.oak/11901/1/CO20-26%28e%29.pdf · 보완 8건: CSIS Missile Threat, TWZ, Defense News, Al Jazeera, Business Insider, AP, NK News, 프레시안·문화일보·경향신문 | KINU 보고서: 공공누리 제2유형(출처표시·상업적 이용금지). 보완 8건은 각 출처 조건 |
| A7 포격·총격·물리 충돌 | CSIS, *Beyond Parallel*, "Database: North Korean Provocations." | 125건 사용. 영문 설명문 옮기지 않음 |

### B 군비·능력

| 요소 | 출처 | 이용 조건·표기 |
|---|---|---|
| B1 신형 무기 개발·시험 | CSIS, *Beyond Parallel*, "Database: North Korean Provocations." | 32건 선별(사용 31) |
| B3 국방비 결정 (사건 기록 화면만) | 국방부·방위사업청 보도자료(정책브리핑 https://www.korea.kr) · e-나라지표 「국방예산 추이」(국방부) https://www.index.go.kr/unity/potal/main/EachDtlPageDetail.do?idx_cd=1699 · 국회예산정책처, 「NABO Focus」 제81호 https://www.nabo.go.kr · 북한 국방비 비중: 최고인민회의 예산 보고(조선중앙통신)를 인용한 언론 보도 | 보도자료·NABO 공공누리 제1유형. 본예산 기준(추경 제외). 북한 비중은 공식 발표치 |
| B4 핵태세·확장억제 | 국방부·외교부 보도자료(정책브리핑, SCM·EDSCG·NCG·전략사령부) · U.S. Department of Defense (War), https://media.defense.gov · The White House (archived), https://bidenwhitehouse.archives.gov · 북한 핵교리: 조선중앙통신 보도를 인용한 통일부·38 North·KEI·NCNK | 보도자료 공공누리 제1유형, 미국 정부 문서는 17 U.S.C. §105 |

### C 선언·교리·외교 행위

| 요소 | 출처 | 이용 조건·표기 |
|---|---|---|
| C1 위협 성명·담화 | 팀 작성(행별 근거 링크) · 국내외 언론 보도 · UMD Digital Archive (구 Wilson Center) https://digitalarchive.umd.edu/ · UN Digital Library · 통일연구원 · Wikipedia · 한국민족문화대백과사전 | 북한 발언은 조선중앙통신 직접 접속이 막혀 모두 인용 보도 기준. 위키 CC BY-SA 4.0. AI 활용 금지 표시 매체 본문은 분석에 안 씀 |
| C2 교리·법제 변경 | 정책브리핑 보도자료·전문자료(정전협정, 국방백서) · 국가법령정보센터 https://www.law.go.kr · 헌법재판소 https://www.ccourt.go.kr · 백악관 아카이브 · 통일연구원 · 한국민족문화대백과사전 · 언론 보도(링크만) | 정책브리핑 공공누리 제1유형(텍스트), 법령·판결은 저작권 보호 대상 아님. B4와 겹치는 5건은 제외 |
| C3 동맹 협의·정상회담 | 외교부 https://www.mofa.go.kr · 중국 외교부 https://www.mfa.gov.cn · 위키문헌 · 국가기록원 · 한국민족문화대백과사전 · VOA · RFA · Wikipedia · 참여연대 · Ukrainska Pravda · 통일연구원 · 국내 언론(사실 확인용) | 외교부: "출처: 외교부 「문서명」, 공공누리 제1유형". RFA: Copyright © 1998-2023, RFA. Used with the permission of Radio Free Asia. 중국 외교부 발표문 전문 번역·게시 안 함 |
| C4 대화·협상·합의 (사건 기록 화면만) | 통일부 남북회담본부 「남북합의서」·「회담별 자료」 https://dialogue.unikorea.go.kr · 국가기록원 「기록으로 보는 남북회담」 · 정책브리핑 · 미국 정부 원문(FRUS·국무부·백악관 아카이브·govinfo·포드 도서관) · 위키문헌·Wikipedia · 통일연구원 · PA-X Peace Agreements Database (CC BY-NC-SA 4.0) · 언론·대통령기록관(링크만) | 국가기록원 스캔 이미지 게시 안 함. 근거: 각 언론 보도(링크 참조) |
| C5 제재·결의·수출통제 (확장 계산만) | UN Security Council 결의·의장성명·1718위원회 https://documents.un.org , https://main.un.org/securitycouncil/en/sanctions/1718 · U.S. Treasury OFAC https://ofac.treasury.gov/recent-actions · Federal Register · Congress.gov · 외교부 「대북 독자제재」 · (1950~2005 보강) govinfo·CRS·재무부·백악관 아카이브·FRUS·국가법령정보센터·정책브리핑 | Source: United Nations Security Council, S/RES/xxxx · Source: U.S. Treasury OFAC(미국 정부 보증처럼 쓰지 않음) · 출처: 외교부, 공공누리 제1유형. UN PDF는 올리지 않음 |

### E 관계 구조 · F 국내 정치

| 요소 | 출처 | 이용 조건·표기 |
|---|---|---|
| E5 북러 밀착 | 통일부 북한정보포털, 「남북관계 연표」. 북한정보포털(https://nkinfo.unikorea.go.kr) > 남북관계 연표 (2026-10-05 다운로드, 8,977건 중 북러 관계 선별). 연표에 없는 2024-05·06, 2025-09의 11행은 언론 기사(뉴시스·경향신문·서울신문·이데일리 등, 행별 출처 열)로 보완 | 북한정보포털 저작권 정책(https://nkinfo.unikorea.go.kr/nkp/pge/view.do): 모든 자료는 저작권법상 보호 저작물이며, 비영리 목적은 자유 이용, 상업 이용은 통일부 사전 협의, 이용 시 출처 명시, 단순 오류 정정 외 내용 변경 금지. 레포에는 북러 관계로 선별한 127행만 두고 원본 연표 전체는 올리지 않음. 사건명 원문은 그대로 두고, 선별·주체국·점수는 팀이 붙인 가공 정보. 보완 행은 각 언론사 저작권, 기사 문장은 옮기지 않음 |
| F2 남북회담 | 통일부 남북회담본부(Office of the Inter-Korean Dialogue), 「연도별 회담정보」. https://dialogue.unikorea.go.kr/ukd/a/ae/usryear/List.do (2026-10-05 다운로드, 667건) | 공공누리 마크(유형 표기 없음) → 제4유형 기준. 점수표는 팀이 따로 계산한 가공물 |

### 비교 지표 (3페이지)

| 자료 | 출처 |
|---|---|
| GPR 한국(GPRC_KOR) | Caldara, Dario, and Matteo Iacoviello. 2022. "Measuring Geopolitical Risk." *American Economic Review* 112 (4): 1194–1225. 데이터 https://www.matteoiacoviello.com/gpr.htm (비교 지수로만 사용) |

---

## 2. 미사용 자료 (수집했지만 화면·지수에 쓰지 않음)

전처리 과정에서 수집·검토했지만 현재 대시보드 화면과 지수 계산에는 들어가지 않은 자료입니다. 이용 조건을 지키기 위해 출처를 함께 남깁니다.

> **KOSIS 북한통계 (D 북한 경제·교역, F 북한 내부 지표)**
>
> **라이선스**
> 1. KOSIS 통계정보 이용지침: 북한통계는 예외 조항이 적용되어 비상업적 목적으로만 쓸 수 있고, 재배포가 금지됨
> 2. 국가데이터처 콜센터(02-2012-9114) 전화 문의(2026-11-03, KOSIS > 북한통계 > 주제별 > 영양 > 1인 1일당 영양공급량 경로를 따라가며 문의): "KOSIS 게시 정보는 출처와 관리기관만 명시하면 사용 가능"이라고 답변받음. 서면 확인은 받지 않음
>
> - **용도**: 수집·검토 자료. 현재 대시보드 화면과 산출식에는 넣지 않음
> - **이용 조건**: 비상업적 연구·교육 목적에 한함. 위 2번 답변에 따라 출처와 관리기관을 명시하고 정제 CSV를 레포에 포함함
> - **필수 준수 사항**:
>   1. 출처와 관리기관 명시: 표별 작성기관 문구 + “KOSIS 국가통계포털(자료관리: 국제협력담당관실)” + 통계표명 + 참조일자(2026.10.05) + URL
>   2. 통계 수치를 임의로 바꾸거나 왜곡하지 않음
>   3. 개인·사업체·특정 조직을 식별할 목적으로 다른 정보와 연결하지 않음
>   4. 영양공급량은 2010년부터 FBS 새 방법론 자료이고, 인구 2026년 이후는 추계값임을 표시함
>
> 레포의 파일은 KOSIS 원자료를 팀이 정제·가공한 것이며, 국가데이터처나 작성기관의 공식 자료가 아닙니다.

> **통일의식조사 (F4 위협 인식 여론)**
>
> **출처**: 김범수. 통일의식조사, 2025 [데이터 세트]. 서울대학교 통일평화연구원 [연구수행기관]. 서울대학교 통일평화연구원 데이터 아카이브 [자료제공기관], 2026-02-03, https://ipus.snu.ac.kr/blog/archives/research/11790. (2026-10-05 다운로드)
>
> **라이선스**: 명시적 라이선스 없음. 저작권은 통일평화연구원에 있음("all rights reserved"). 원자료는 누구나 받을 수 있게 공개되어 있고, 출처 명기를 요청함
>
> - **데이터**: 1-2025-통일의식조사_로데이터.zip (2025년, 1,200명, 조사 2025-08-08~09-01) → F4_통일의식조사_응답자_정제.csv, F4_통일의식조사_위협문항집계.csv
> - **용도**: 위협 문항 5개의 응답 비율을 긴장도의 검증 마커(대조용)로만 쓰고, 점수는 매기지 않음
> - **이용 조건**: 비상업적 학술·교육 목적(KDT 프로젝트·포트폴리오)에 한함. 원자료 zip은 레포에 두지 않고, 정제 파일만 포함함. 원자료가 필요한 사람에게는 IPUS 링크를 안내함
> - **필수 준수 사항**:
>   1. 출처는 위 인용 서식(KOSSDA 데이터 인용 서식 준용)으로 표기
>   2. 논문·보고서 등으로 발간하면 tongil@snu.ac.kr로 발간 사실을 알림(기관 요청 사항)
>   3. 기초보고서의 문장·표·그래프는 복제하지 않음
>   4. 응답자 단위 자료를 다른 정보와 연결하지 않음

| 자료 (요소) | 출처 | 이용 조건 |
|---|---|---|
| 국방비 지출 (keep) | Stockholm International Peace Research Institute (SIPRI), *SIPRI Military Expenditure Database*. https://www.sipri.org/databases/milex | 비상업 무료. 화면에 쓸 경우 "Data source: SIPRI Military Expenditure Database" 표기. 데이터셋 10% 이상 그대로 재배포 금지 |
| 북한 미사일·핵실험 (keep) | CSIS Missile Defense Project, *Missile Threat*. https://missilethreat.csis.org | 비상업 연구·교육. 전체 재배포 금지. A2·A6 보조 검증에만 참고 |
| 무력 충돌·사건 (keep) | Uppsala Conflict Data Program (UCDP), UCDP/PRIO Armed Conflict Dataset v26.1, UCDP Georeferenced Event Dataset v26.1. https://ucdp.uu.se | CC BY 4.0 |
| 무기 이전 (B2) | Information from the Stockholm International Peace Research Institute (SIPRI), https://www.sipri.org/databases/armstransfers | 비상업 무료. 상업 이용·10% 넘는 재게시는 허가 필요(전처리 CSV 약 1,843건은 전체 DB의 9% 미만). 원본 CSV 올리지 않음. 연 단위라 일 단위 지수에 안 넣음 |
| 북한 경제·사회 통계 | 국가데이터처 국가통계포털(KOSIS) 북한통계 12개 표(국민총소득·식량작물·무역·영양공급량·인구·성장률·교역비중 등). https://kosis.kr/bukhan · 표별 작성기관·관리부서는 [KOSIS 표별 출처](#kosis-표별-출처) | 비상업 교육용. 출처·관리부서 명시(2026-11-03 콜센터 확인). 통계 수치 임의 변경 금지. 인구 2026년 이후는 추계값 |
| UN 총회 표결 (E1) | United Nations Voting Data (Up to 2025), UN_Voting_Records_1946-2025_v3. 원출처 UN Digital Library https://digitallibrary.un.org | CC0. 안보리 거부권은 기록 투표가 없어 포함 안 됨 |
| 동맹 (E1·E3) | Leeds, Brett Ashley, Jeffrey M. Ritter, Sara McLaughlin Mitchell, and Andrew G. Long. 2002. "Alliance Treaty Obligations and Provisions, 1815-1944." *International Interactions* 28: 237-260. 데이터 ATOP v5.1(atop5_1ddyr, atopinst5_1, atop-sscore). http://www.atopdata.org | 학술·비영리 무료. 결과물에 공식 인용 문구 필수 |
| 위협 인식 여론 (F4) | 김범수. 통일의식조사, 2025 [데이터 세트]. 서울대학교 통일평화연구원 [연구수행기관]. 서울대학교 통일평화연구원 데이터 아카이브 [자료제공기관], 2026-02-03, https://ipus.snu.ac.kr/blog/archives/research/11790. (2026-10-05 다운로드, 1,200명, 조사 2025-08-08~09-01) | 저작권은 통일평화연구원(all rights reserved), 출처는 KOSSDA 데이터 인용 서식 준용. 비상업 학술·교육용. 응답자 단위 정제 파일과 위협 문항 집계 파일을 레포에 포함(원자료 zip은 미포함). 발간 시 tongil@snu.ac.kr에 알림 |
| 북↔남 위협 이벤트 (C1 선택) | The GDELT Project. https://www.gdeltproject.org | 제한 없이 이용, 출처 표기 필수. 미수집 |


### KOSIS 표별 출처

구분: D = 북한 경제·교역, F = 북한 내부 지표, D·F = 둘 다 같은 표를 씀. 형식(라이선스 노트 F1 기준): 작성기관, KOSIS 국가통계포털(자료관리: 관리부서), 「통계표명」, 참조일자, URL

| 구분 | 통계표 | 출처 |
|---|---|---|
| D·F | 남북한 국민총소득 | (남북)한국은행「국민계정」, KOSIS 국가통계포털(자료관리: 국제협력담당관실), 「남북한 국민총소득」, 2026.10.05, https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1ZGA37 |
| D·F | 남북한 식량작물 생산량 | (북)농촌진흥청, (남)국가데이터처「농작물생산조사」, KOSIS 국가통계포털(자료관리: 국제협력담당관실), 「남북한 식량작물 생산량」, 2026.10.05, https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1ZGA55 |
| F | 남북한 무역총액·교역액 | (북)KOTRA「북한의 대외무역동향」, (남)한국무역협회「한국무역통계」, (남북교역)통일부「남북교역통계」, KOSIS 국가통계포털(자료관리: 국제협력담당관실), 「남북한 무역총액·교역액」, 2026.10.05, https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1ZGA91 |
| F | 남북한 1인 1일당 영양공급량 | (북)FAO, (남)한국농촌경제연구원, KOSIS 국가통계포털(자료관리: 국제협력담당관실), 「남북한 1인 1일당 영양공급량」, 2026.10.05, https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1ZGAB4 ※ 2010년부터 FBS 새 방법론 자료 |
| F | 남북한 인구 | 국가데이터처, KOSIS 국가통계포털(자료관리: 국제협력담당관실), 「남북한 인구」, 2026.10.05, https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1ZGA21 ※ 2026년 이후는 추계값 |
| D | 어업 및 양식 생산량 | (북)관계기관, (남)국가데이터처「어업생산동향조사」, KOSIS 국가통계포털(자료관리: 국제협력담당관실), 「어업 및 양식 생산량」, 2026.10.02, https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1ZGA58 |
| D | 경제성장률 | (남북)한국은행「국민계정」, KOSIS 국가통계포털(자료관리: 국제협력담당관실), 「경제성장률」, 2026.10.02, https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1ZGA31 |
| D | 산업별 성장률 | (남북)한국은행「국민계정」, KOSIS 국가통계포털(자료관리: 국제협력담당관실), 「산업별 성장률」, 2026.10.02, https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1ZGA32 |
| D | 수출입액 | (북)KOTRA「북한의 대외무역동향」, (남)한국무역협회「한국무역통계」, KOSIS 국가통계포털(자료관리: 국제협력담당관실), 「수출입액」, 2026.10.02, https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1ZGA92 |
| D | 주요국별 교역비중 변화 추이 | (북)KOTRA「북한의 대외무역동향」, (남)한국무역협회「한국무역통계」, (남북교역)통일부「남북교류협력동향」, KOSIS 국가통계포털(자료관리: 국제협력담당관실), 「주요국별 교역비중 변화 추이」, 2026.10.04, https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1ZGA97 |
| D | 수출·수입 | 관세청, IMF, KOSIS 국가통계포털(자료관리: 통계서비스기획과), 「수출·수입」, 2026.10.04, https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1ZGA96 |
| D (레포에 파일 없음) | 농업생산지수 | (북)FAO, (남)농림축산식품부「농림업생산지수」, KOSIS 국가통계포털(자료관리: 국제협력담당관실), 「농업생산지수」, 2026.10.02, https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1ZGAE22 |

---

## 3. 방법 참고 문헌

- Goldstein, Joshua S. 1992. "A Conflict-Cooperation Scale for WEIS Events Data." *Journal of Conflict Resolution* 36 (2): 369–85.
- Jeon, Hee-Jae, and Moon-Gul Lee. 2022. "Real-Time Military Security Index Calculation Model Using Big Data Analytics: The Case of South Korea." *Social Sciences* 11 (12): 572.
- 최성근. 2010. 「HRI 한반도 평화지수」. 『통일경제』 겨울호. 현대경제연구원.
- 김병로·김병연·박명규·정은미. 2007. 『남북통합지수 개발을 위한 기초연구』. 서울대학교 통일평화연구원.
- 김재철. 2015. 「남북한의 군사적 긴장완화 방안: 근본요인과 촉발요인을 중심으로」. 『한국동북아논총』 20 (4): 121–40.
- Sample, Susan G. 1997. "Arms Races and Dispute Escalation: Resolving the Debate." *Journal of Peace Research* 34 (1): 7–22.
- Armed Conflict Location & Event Data (ACLED). https://acleddata.com (30일 창 가중 방식 검토)

## 4. 도구·디자인

- Python 3.11, Streamlit, Plotly, pandas, SQLite, python-docx
- 선 아이콘: Lucide (https://lucide.dev, ISC License)
- 홈 배너 봉수대 그림: 팀 직접 제작

## 이용하지 않은 자료

- KCNA Watch(NK Pro): 약관상 사용 불가
- POLECAT·ICEWS·FocusData: 약관 미확인으로 보류

---

## 부록 A. A4 군사훈련 보완 11건 사건별 출처

CSIS 원본과 별개로 2021~2026년 공백을 채운 사건입니다. 기사 원문은 옮기지 않고 링크만 남깁니다.

- A4-0041  Combined Command Post Training | https://www.ytn.co.kr/_ln/0101_202108062011435356 ; https://stripes.com/theaters/asia_pacific/2021-08-27/north-korea-joint-training-exercise-us-military-2684114.html
- A4-0042  Combined Command Post Training | https://m.dailian.co.kr/news/view/1104177 ; https://m.dailian.co.kr/news/view/1103958 ; https://www.newstomato.com/RealTime/RealTimeDetail.aspx?no=1117711
- A4-0043  Ulchi Freedom Shield Exercises | https://www.newdaily.co.kr/site/data/html/2022/08/16/2022081600088.amp.html ; https://www.rfa.org/korean/in_focus/nk_nuclear_talks/ufsdrills-09012022083500.html
- A4-0044  Freedom Shield Exercises | https://www.seoul.co.kr/news/newsView.php?id=20230303500080 ; https://www.khan.co.kr/article/202303031028001
- A4-0045  Ulchi Freedom Shield Exercises | https://www.usfk.mil/Media/Press-Products/Press-Releases/Article/3491557/the-republic-of-korea-and-united-states-announce-exercise-ulchi-freedom-shield/ ; https://www.munhwa.com/article/11379199
- A4-0046  Freedom Shield Exercises | https://www.newdaily.co.kr/site/data/html/2024/03/04/2024030400290.html
- A4-0047  Ulchi Freedom Shield Exercises | https://www.usfk.mil/Media/Press-Products/Press-Releases/Article/3889608/ufs-24-successfully-concludes/ ; https://www.newdaily.co.kr/site/data/html/2024/08/29/2024082900132.html ; https://www.fnnews.com/news/202408191445562224
- A4-0048  Freedom Shield Exercises | https://m.seoul.co.kr/news/2025/03/20/20250320500212 ; https://www.dailian.co.kr/news/view/1469244/
- A4-0049  Ulchi Freedom Shield Exercises | https://www.usfk.mil/Media/Press-Products/Press-Releases/Article/4288364/ufs-25-concludes-reinforcing-readiness-and-deterrence/ ; https://v.daum.net/v/20250807122258004 ; https://www.asiae.co.kr/en/article/2025082810341734087
- A4-0050  Freedom Shield Exercises | https://www.etoday.co.kr/news/view/2567280 ; https://www.ytn.co.kr/_ln/0101_202602251853158903
- A4-0051  Ulchi Freedom Shield Exercises | https://www.koreaherald.com/article/10848435 ; https://www.ytn.co.kr/_ln/0101_202608211321593325 ; https://www.rfa.org/korean/in-focus/2026/08/10/ufs-military-exercise-unc-summertime/

## 부록 B. A5 미 전략자산 전개 일 단위 사건별 출처

<details><summary>118행 펼치기</summary>

- A5-0001  2007년 미 항공모함 전개(로널드 레이건) | https://www.globalsecurity.org/military/library/news/2007/03/mil-070322-nns03.htm
- A5-0002  2008년 미 항공모함 전개(니미츠) | https://www.globalsecurity.org/military/ops/key-resolve-foal-eagle-2008.htm
- A5-0003  2008년 미 항공모함 전개(조지 워싱턴) | https://www.globalsecurity.org/military/library/news/2008/10/mil-081017-nns06.htm
- A5-0004  2009년 미 항공모함 전개(존 C. 스테니스) | https://www.strategypage.com/military_photos/military_photos_20090311215949.aspx
- A5-0005  2010년 미 항공모함 전개(조지 워싱턴) | https://nocutnews.co.kr/news/4530459
- A5-0006  2010년 미 항공모함 전개(조지 워싱턴) | https://www.globalsecurity.org/military/library/news/2010/07/mil-100721-nns01.htm
- A5-0007  2010년 미 항공모함 전개(조지 워싱턴) | https://nocutnews.co.kr/news/4530459
- A5-0008  2010년 미 잠수함 전개(투산) | https://nocutnews.co.kr/news/4530459
- A5-0009  2010년 미 스텔스전투기 전개(F-22) | https://nocutnews.co.kr/news/4530459 ; https://www.hankookilbo.com/news/article/201602171756711993
- A5-0010  2010년 미 항공모함 전개(조지 워싱턴) | https://nocutnews.co.kr/news/4530459
- A5-0011  2011년 미 항공모함 전개(조지 워싱턴) | https://www.globalsecurity.org/military/library/news/2011/10/mil-111001-nns03.htm
- A5-0012  2012년 미 전략폭격기 전개(B-52 2대) | https://theaviationist.com/2012/05/29/target-north-korea-b-52/
- A5-0013  2012년 미 항공모함 전개(조지 워싱턴) | https://nocutnews.co.kr/news/4530459
- A5-0014  2012년 미 항공모함 전개(조지 워싱턴) | https://www.globalsecurity.org/military/library/news/2012/06/mil-120628-nns01.htm
- A5-0015  2013년 미 잠수함 전개(샌프란시스코) | https://www.koreajoongangdaily.com/korea/us-sends-submarine-to-east-sea/10920849 ; https://nocutnews.co.kr/news/4530459
- A5-0016  2013년 미 전략폭격기 전개(B-52) | https://www.dailynk.com/english/b52-sends-clear-message-to-pyongya/
- A5-0017  2013년 미 잠수함 전개(샤이엔) | https://edaily.co.kr/News/Read?mediaCodeNo=257&newsId=02217286602745288 ; https://nocutnews.co.kr/news/4530459
- A5-0018  2013년 미 전략폭격기 전개(B-52) | https://nocutnews.co.kr/news/4530459
- A5-0019  2013년 미 전략폭격기 전개(B-52) | https://nocutnews.co.kr/news/4530459
- A5-0020  2013년 미 전략폭격기 전개(B-2 2대) | https://nocutnews.co.kr/news/4530459
- A5-0021  2013년 미 스텔스전투기 전개(F-22) | https://www.seoul.co.kr/news/politics/diplomacy/2013/04/02/20130402005006
- A5-0022  2013년 미 항공모함 전개(니미츠) | https://nocutnews.co.kr/news/4530459
- A5-0023  2013년 미 잠수함 전개(브레머턴) | https://nocutnews.co.kr/news/4530459
- A5-0024  2013년 미 항공모함 전개(니미츠) | https://nocutnews.co.kr/news/4530459
- A5-0025  2013년 미 항공모함 전개(조지 워싱턴) | https://www.seoul.co.kr/news/society/2013/10/05/20131005800003 ; https://nocutnews.co.kr/news/4530459
- A5-0026  2014년 미 전략폭격기 전개(B-52) | https://thepeninsulaqatar.com/article/07/02/2014/bomber-run-imperils-reunions-plan-n-korea-1
- A5-0027  2014년 미 잠수함 전개(콜럼버스) | https://nocutnews.co.kr/news/4530459
- A5-0028  2014년 미 항공모함 전개(조지 워싱턴) | https://nocutnews.co.kr/news/4530459
- A5-0029  2015년 미 항공모함 전개(로널드 레이건) | https://nocutnews.co.kr/news/4530459
- A5-0030  2016년 미 전략폭격기 전개(B-52) | https://nocutnews.co.kr/news/4530459 ; https://www.af.mil/News/Article-Display/Article/642180/
- A5-0031  2016년 미 잠수함 전개(노스캐롤라이나) | https://www.khan.co.kr/article/201603130949201
- A5-0032  2016년 미 스텔스전투기 전개(F-22 4대) | https://www.khan.co.kr/article/201603130949201
- A5-0033  2016년 미 항공모함 전개(존 C. 스테니스) | https://www.khan.co.kr/article/201603130949201
- A5-0034  2016년 미 잠수함 전개(미시시피) | https://m.go.seoul.co.kr/news/2016/06/14/20160614016014
- A5-0035  2016년 미 잠수함 전개(오하이오) | https://www.stripes.com/news/2016-07-13/nuclear-powered-sub-stops-in-korea-during-heightened-tensions-1548555.html1
- A5-0036  2016년 미 전략폭격기 전개(B-1B 2대) | https://theaviationist.com/2016/09/13/u-s-b-1-bombers-fly-over-south-korea-in-response-to-the-recent-nuclear-test-by-north-korea
- A5-0037  2016년 미 전략폭격기 전개(B-1B 2대) | https://www.seoul.co.kr/news/politics/2016/09/26/20160926800049
- A5-0038  2016년 미 항공모함 전개(로널드 레이건) | https://m.seoul.co.kr/news/2016/10/10/20161010800084
- A5-0039  2017년 미 미사일방어 전개(사드) | https://kyeonggi.com/article/201703070909849
- A5-0040  2017년 미 항공모함 전개(칼 빈슨) | https://www.sidae.com/article/2017040919518017013
- A5-0041  2017년 미 전략폭격기 전개(B-1B 2대) | https://www.seoul.co.kr/news/politics/north/2017/03/31/20170331008009
- A5-0042  2017년 미 잠수함 전개(콜럼버스) | https://edaily.co.kr/News/Read?mediaCodeNo=257&newsId=04756006615865616
- A5-0043  2017년 미 전략폭격기 전개(B-1B) | https://www.seoul.co.kr/news/politics/2017/03/22/20170322800071
- A5-0044  2017년 미 전략폭격기 전개(B-1B) | https://www.seoul.co.kr/news/politics/north/2017/03/31/20170331008009
- A5-0045  2017년 미 잠수함 전개(미시간) | https://www.globalsecurity.org/military/library/news/2017/04/mil-170425-nns03.htm
- A5-0046  2017년 미 미사일방어 전개(사드) | https://m.seoul.co.kr/news/2017/04/27/20170427800091
- A5-0047  2017년 미 항공모함 전개(칼 빈슨) | https://www.pressreader.com/sri-lanka/sunday-times-sri-lanka/20170430/282600262776216 ; https://www.newdaily.co.kr/site/data/html/2017/06/01/2017060100058.html
- A5-0048  2017년 미 전략폭격기 전개(B-1B 2대) | https://m.seoul.co.kr/news/2017/05/30/20170530500005
- A5-0049  2017년 미 전략폭격기 전개(B-1B 2대) | https://m.seoul.co.kr/news/2017/05/30/20170530500005
- A5-0050  2017년 미 항공모함 전개(로널드 레이건) | https://www.newdaily.co.kr/site/data/html/2017/06/01/2017060100058.html
- A5-0051  2017년 미 잠수함 전개(샤이엔) | https://nknews.org/?p=812278
- A5-0052  2017년 미 전략폭격기 전개(B-1B) | https://www.munhwa.com/article/11041590
- A5-0053  2017년 미 전략폭격기 전개(B-1B 2대) | https://www.munhwa.com/article/11041590
- A5-0054  2017년 미 전략폭격기 전개(B-1B 2대) | https://nationalinterest.org/blog/buzz/2017-americas-b-1b-lancer-bombers-returned-south-korea-yet-again-77186
- A5-0055  2017년 미 전략폭격기 전개(B-1B) | https://www.newsis.com/view/NISX20170925_0000105006
- A5-0056  2017년 미 전략폭격기 전개(B-1B 2대 + F-35B 4대) | https://sports.khan.co.kr/article/201709010107003 ; https://www.newsis.com/view/NISX20170925_0000105006
- A5-0057  2017년 미 미사일방어 전개(사드) | https://kbmaeil.com/article/201709080202075
- A5-0058  2017년 미 전략폭격기 전개(B-1B 2대 + F-35B 4대) | https://www.newsis.com/view/NISX20170925_0000105006
- A5-0059  2017년 미 전략폭격기 전개(B-1B 2대) | https://www.newsis.com/view/NISX20170925_0000105006
- A5-0060  2017년 미 잠수함 전개(투산) | https://edaily.co.kr/News/Read?mediaCodeNo=257&newsId=03896646616091936
- A5-0061  2017년 미 전략폭격기 전개(B-1B 2대) | https://edaily.co.kr/News/Read?mediaCodeNo=257&newsId=03896646616091936 ; https://www.seoul.co.kr/news/politics/2017/10/11/20171011800005
- A5-0062  2017년 미 잠수함 전개(미시간) | https://www.seoul.co.kr/news/politics/diplomacy/2017/10/15/20171015800014
- A5-0063  2017년 미 항공모함 전개(로널드 레이건) | https://www.seoul.co.kr/news/politics/diplomacy/2017/10/15/20171015800014
- A5-0064  2017년 미 항공모함 전개(로널드 레이건) | https://kyeonggi.com/article/201710210949692
- A5-0065  2017년 미 전략폭격기 전개(B-1B 2대) | https://m.dailian.co.kr/news/view/671532
- A5-0066  2017년 미 항공모함 전개(레이건·니미츠·시어도어 루스벨트) | https://m.dailian.co.kr/news/view/673430
- A5-0067  2017년 미 스텔스전투기 전개(F-22 6대, F-35A, F-35B) | https://www.hankookilbo.com/news/article/201712060891515101
- A5-0068  2017년 미 전략폭격기 전개(B-1B) | https://www.hankookilbo.com/news/article/201712060891515101
- A5-0069  2017년 미 전략폭격기 전개(B-1B) | https://www.seoul.co.kr/news/politics/2017/12/07/20171207800083
- A5-0070  2022년 미 항공모함 전개(에이브러햄 링컨) | https://www.etoday.co.kr/news/view/2122971
- A5-0071  2022년 미 스텔스전투기 전개(F-35A 6대) | https://www.newspim.com/news/view/20230509000251
- A5-0072  2022년 미 항공모함 전개(로널드 레이건) | https://www.newspim.com/news/view/20230509000251 ; https://www.mindlenews.com/news/articleView.html?idxno=2231
- A5-0073  2022년 미 잠수함 전개(아나폴리스) | https://www.newspim.com/news/view/20230509000251
- A5-0074  2022년 미 항공모함 전개(로널드 레이건) | https://v.daum.net/v/20221005204445304 ; https://www.newspim.com/news/view/20230509000251
- A5-0075  2022년 미 잠수함 전개(키웨스트) | https://www.newspim.com/news/view/20230509000251 ; https://www.mindlenews.com/news/articleView.html?idxno=2231
- A5-0076  2022년 미 스텔스전투기 전개(F-35B 4대) | https://www.newspim.com/news/view/20230509000251
- A5-0077  2022년 미 전략폭격기 전개(B-1B 2대) | https://m.seoul.co.kr/news/2022/11/20/20221120500129 ; https://www.newspim.com/news/view/20230509000251
- A5-0078  2022년 미 전략폭격기 전개(B-1B) | https://m.seoul.co.kr/news/2022/11/20/20221120500129
- A5-0079  2022년 미 스텔스전투기 전개(F-22) | https://www.newspim.com/news/view/20230509000251
- A5-0080  2022년 미 전략폭격기 전개(B-52H) | https://www.mindlenews.com/news/articleView.html?idxno=2231
- A5-0081  2023년 미 전략폭격기 전개(B-1B 2대 + F-22·F-35B) | https://www.newspim.com/news/view/20230509000251 ; https://www.mindlenews.com/news/articleView.html?idxno=2231
- A5-0082  2023년 미 전략폭격기 전개(B-1B) | https://www.newspim.com/news/view/20230509000251 ; https://www.dt.co.kr/article/11555168
- A5-0083  2023년 미 잠수함 전개(스프링필드) | https://www.newspim.com/news/view/20230509000251 ; https://www.mindlenews.com/news/articleView.html?idxno=2231
- A5-0084  2023년 미 전략폭격기 전개(B-1B + MQ-9) | https://www.newspim.com/news/view/20230509000251
- A5-0085  2023년 미 전략폭격기 전개(B-52H) | https://www.newspim.com/news/view/20230509000251 ; https://v.daum.net/v/20231107122358090
- A5-0086  2023년 미 전략폭격기 전개(B-1B) | https://www.newspim.com/news/view/20230509000251
- A5-0087  2023년 미 항공모함 전개(니미츠) | https://www.newspim.com/news/view/20230509000251 ; https://www.spnews.co.kr/news/articleView.html?idxno=63944
- A5-0088  2023년 미 전략폭격기 전개(B-52H) | https://www.newspim.com/news/view/20230509000251 ; https://v.daum.net/v/20231107122358090
- A5-0089  2023년 미 전략폭격기 전개(B-52H) | https://www.newspim.com/news/view/20230509000251
- A5-0090  2023년 미 잠수함 전개(미시간) | https://www.rfa.org/korean/in_focus/nk_nuclear_talks/ssgn-06162023062101.html
- A5-0091  2023년 미 전략폭격기 전개(B-52H) | https://v.daum.net/v/20231107122358090 ; https://www.newspim.com/news/view/20230630000887
- A5-0092  2023년 미 전략폭격기 전개(B-52H) | https://v.daum.net/v/20231107122358090
- A5-0093  2023년 미 잠수함 전개(켄터키) | https://v.daum.net/v/20231107122358090 ; https://www.ajunews.com/view/20230718173307326
- A5-0094  2023년 미 잠수함 전개(아나폴리스) | https://hawaiitribune-herald.com/2023/07/24/nation-world-news/us-sends-another-submarine-to-south-korea-adding-to-show-of-force-against-north-korea/amp/
- A5-0095  2023년 미 전략폭격기 전개(B-1B) | https://www.usfk.mil/Media/Newsroom/News/Article/3509900/us-and-republic-of-korea-enhance-combat-readiness-with-combined-air-training/
- A5-0096  2023년 미 항공모함 전개(로널드 레이건) | https://www.navysite.de/cvn/cvn76.html
- A5-0097  2023년 미 전략폭격기 전개(B-52H) | https://v.daum.net/v/20231107122358090 ; https://www.newsis.com/view/NISX20231019_0002489515
- A5-0098  2023년 미 전략폭격기 전개(B-52H) | https://v.daum.net/v/20231107122358090 ; https://www.newsis.com/view/NISX20231019_0002489515
- A5-0099  2023년 미 항공모함 전개(칼 빈슨) | https://m.seoul.co.kr/news/2023/11/21/20231121800002
- A5-0100  2023년 미 잠수함 전개(미주리) | https://www.imaeil.com/page/view/2023121712100418292
- A5-0101  2023년 미 전략폭격기 전개(B-1B) | https://www.dt.co.kr/article/11555168
- A5-0102  2024년 미 항공모함 전개(칼 빈슨) | https://m.seoul.co.kr/news/2024/01/18/20240118001005 ; https://www.minplusnews.com/news/articleView.html?idxno=15906
- A5-0103  2024년 미 전략폭격기 전개(B-52H) | https://www.newdaily.co.kr/site/data/html/2024/04/02/2024040200279.amp.html
- A5-0104  2024년 미 스텔스전투기 전개(F-22) | https://www.newdaily.co.kr/site/data/html/2024/05/16/2024051600133.html
- A5-0105  2024년 미 전략폭격기 전개(B-1B) | https://www.segye.com/view/20240605514289 ; https://www.ajunews.com/view/20240605161913200
- A5-0106  2024년 미 항공모함 전개(시어도어 루스벨트) | https://www.metroseoul.co.kr/article/20240622500021 ; https://www.newdaily.co.kr/site/data/html/2024/06/27/2024062700229.html
- A5-0107  2024년 미 스텔스전투기 전개(F-22) | https://www.newdaily.co.kr/site/data/html/2024/06/26/2024062600310.amp.html
- A5-0108  2024년 미 잠수함 전개(버몬트) | https://v.daum.net/v/20240923180437231
- A5-0109  2024년 미 전략폭격기 전개(B-1B) | https://www.arabnews.com/node/2577870/amp
- A5-0110  2024년 미 항공모함 전개(조지 워싱턴) | https://www.seoul.co.kr/news/politics/diplomacy/2024/11/13/20241113500193
- A5-0111  2025년 미 전략폭격기 전개(B-1B) | https://rfa.org/korean/in_focus/k022025my1-02202025031449.html
- A5-0112  2025년 미 잠수함 전개(알렉산드리아) | https://rfa.org/korean/in_focus/k022025my1-02202025031449.html
- A5-0113  2025년 미 전략폭격기 전개(B-1B) | https://www.fnnews.com/news/202502201350049839
- A5-0114  2025년 미 항공모함 전개(칼 빈슨) | https://www.khan.co.kr/article/202503021629001 ; https://www.sidae.com/article/2025030217050736498
- A5-0115  2025년 미 전략폭격기 전개(B-1B) | https://news.sbs.co.kr/news/endPage.do?news_id=N1008063619
- A5-0116  2025년 미 전략폭격기 전개(B-52H) | https://www.kukinews.com/article/view/kuk202507110119
- A5-0117  2025년 미 항공모함 전개(조지 워싱턴) | https://m.seoul.co.kr/news/2025/11/05/20251105800003
- A5-0118  2025년 미 잠수함 전개(그린빌) | https://www.khan.co.kr/article/202512231057001

</details>
