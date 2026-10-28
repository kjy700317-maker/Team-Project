# F0-pre 보고서 — 원격 develop 점검
- 날짜: 2026-10-28 · 실행 위치(브랜치): `develop` (db782f8, 실행 시점 origin/develop보다 27 커밋 뒤) · 고친 파일: 없음(이 보고서만)
- 실행 환경: Windows 11, Claude Code Bash 도구(Git Bash/MSYS). 명령은 작업 파일 1절 그대로 실행. 실패한 명령은 출력을 그대로 두고, 아래 "보충"에 따로 표시해 덧붙임.

## 1-1 현재 상태
```text
$ git status --porcelain
 M .vscode/settings.json
 M README.md
 M docs/decisions.md
 M utils/README.md
?? .obsidian/
?? docs/dev/
?? "\354\247\204\355\226\211 \355\230\204\355\231\251 \353\260\217 \352\263\204\355\232\215 \354\240\225\353\246\254/"

$ git branch -vv
* develop db782f8 [origin/develop: behind 27] Update README.md

$ python --version
Python 3.14.6

$ python -c "import numpy, pandas; print(numpy.__version__, pandas.__version__)"
2.4.6 3.0.3

$ python -c "import pytest; print(pytest.__version__)" || echo "pytest 없음"
9.0.3

$ python -c "import openpyxl; print(openpyxl.__version__)" || echo "openpyxl 없음"
3.1.5

$ python -c "import streamlit; print(streamlit.__version__)" || echo "streamlit 없음"
1.58.0

$ gh --version || echo "gh 없음"
gh version 2.97.0 (2026-07-31)
https://github.com/cli/cli/releases/tag/v2.97.0

$ gh auth status || echo "gh 로그인 안 됨"
github.com
  ✓ Logged in to github.com account money2082 (keyring)
  - Active account: true
  - Git operations protocol: https
  - Token: gho_************************************
  - Token scopes: 'gist', 'read:org', 'repo', 'workflow'

```

## 1-2 원격 기록
```text
$ git fetch origin
From https://github.com/kjy700317-maker/Team-Project
 * [new branch]      feature/a-data-update   -> origin/feature/a-data-update
 * [new branch]      feature/erd-integration -> origin/feature/erd-integration
 * [new branch]      feature/erd-v4-tables   -> origin/feature/erd-v4-tables
 * [new branch]      feature/exclude-growth-rate -> origin/feature/exclude-growth-rate
 * [new branch]      feature/tension-dashboard -> origin/feature/tension-dashboard

$ git log --oneline -15 origin/develop
a05b019 doc: 들여쓰기 수정
95c46c4 Merge pull request #11 from kjy700317-maker/feature/a-data-update
ad495db README 최신화 및 SOURCES.md 출처표기 파일 생성
6574ea6 1028 1차 최신화
ef9002c data: A4, A6 2021~2026 행 추가, A7 주체국 보완
180228c fix: .gitignore - .vscode 설정 수정
3ecfad0 fix: .vscode 폴더 인식 문제해결
7cc4bbe docs: README 폴더구조 최신화 , requirements 패키지 추가
1cd5495 Merge pull request #10 from kjy700317-maker/feature/exclude-growth-rate
946b1c4 refactor: 증감률 지표 지표값 적재 제외(원 지표에서 계산)
535b5da Merge pull request #8 from kjy700317-maker/feature/erd-v4-tables
d18fd46 docs: ERD V4 테이블 분리 기준 및 EF 사건 지표 중복처리 결정기록
0501eba feat: ERD V4기준 대기능1 테이블 분리(기준-데이터-보조-상세 13개)
8b8066d Merge pull request #6 from kjy700317-maker/feature/erd-integration
bb05498 전처리 데이터 저장

$ git rev-list --left-right --count develop...origin/develop
0	27

$ git ls-remote --symref origin HEAD
ref: refs/heads/develop	HEAD
a05b01983f81e3510a5fef2dff826b14b72cb238	HEAD

```

## 1-3 파일 목록·바뀐 것
(파일 이름의 `\355\231\210.py` 같은 표기는 git의 8진 이스케이프. `\355\231\210.py` = `홈.py`)
```text
$ git ls-tree -r --name-only origin/develop
.github/ISSUE_TEMPLATE/feature.md
.github/pull_request_template.md
.gitignore
.streamlit/.gitkeep
.vscode/settings.default.json
README.md
SOURCES.md
config.py
data/.gitkeep
data/processed/.gitkeep
"data/processed/A/A1_\355\225\265\354\213\244\355\227\230_CSV.csv"
"data/processed/A/A1_\355\225\265\354\213\244\355\227\230_\354\235\274\353\213\250\354\234\204_CSV.csv"
"data/processed/A/A2_\353\257\270\354\202\254\354\235\274_\353\260\234\354\202\254_CSV.csv"
"data/processed/A/A3_\354\240\200\352\260\225\353\217\204_\353\254\274\353\246\254_\353\217\204\353\260\234_CSV.csv"
"data/processed/A/A4_\352\265\260\354\202\254\355\233\210\353\240\250_CSV.csv"
"data/processed/A/A5_\353\257\270_\354\240\204\353\240\245\354\236\220\354\202\260_\354\240\204\352\260\234_CSV.csv"
"data/processed/A/A5_\353\257\270_\354\240\204\353\240\245\354\236\220\354\202\260_\354\240\204\352\260\234_\354\235\274\353\213\250\354\234\204_CSV.csv"
"data/processed/A/A6_\354\227\264\353\263\221\354\213\235_CSV.csv"
"data/processed/A/A7_\355\217\254\352\262\251_\354\264\235\352\262\251_\353\254\274\353\246\254_\354\266\251\353\217\214_CSV.csv"
"data/processed/B/B1_\354\213\240\355\230\225\353\254\264\352\270\260\352\260\234\353\260\234\354\213\234\355\227\230_\354\240\204\354\262\230\353\246\254.csv"
"data/processed/B/B2_SIPRI_\353\254\264\352\270\260\354\235\264\354\240\204_\354\240\204\354\262\230\353\246\254.csv"
"data/processed/B/B3_\352\265\260\353\271\204\354\235\264\353\262\244\355\212\270_\354\240\204\354\262\230\353\246\254.csv"
"data/processed/B/B4_\355\225\265\355\203\234\354\204\270\355\231\225\354\236\245\354\226\265\354\240\234_\354\202\254\352\261\264.csv"
"data/processed/B/B4_\355\231\225\354\236\245\354\226\265\354\240\234_\352\263\265\354\225\275\353\254\270\352\265\254.csv"
"data/processed/C/C1_\354\234\204\355\230\221\354\204\261\353\252\205\353\213\264\355\231\224_\354\240\204\354\262\230\353\246\254.csv"
"data/processed/C/C2_\352\265\220\353\246\254\353\262\225\354\240\234_\354\240\204\354\262\230\353\246\254.csv"
"data/processed/C/C3_\353\217\231\353\247\271\355\230\221\354\235\230_\354\202\254\352\261\264.csv"
"data/processed/C/C3_\354\266\234\354\262\230.csv"
"data/processed/C/C4_\353\214\200\355\231\224\355\230\221\354\203\201\355\225\251\354\235\230_\354\240\204\354\262\230\353\246\254.csv"
"data/processed/C/C5_\354\240\234\354\236\254_\352\262\260\354\235\230_\354\210\230\354\266\234\355\206\265\354\240\234.csv"
"data/processed/D/D1_\352\262\275\354\240\234\354\204\261\354\236\245\353\245\240.csv"
"data/processed/D/D1_\352\265\255\353\257\274\354\264\235\354\206\214\353\223\235.csv"
"data/processed/D/D1_\354\202\260\354\227\205\353\263\204\354\204\261\354\236\245\353\245\240.csv"
"data/processed/D/D1_\354\210\230\354\266\234\354\236\205\354\225\241.csv"
"data/processed/D/D1_\354\213\235\353\237\211\354\236\221\353\254\274\354\203\235\354\202\260\353\237\211.csv"
"data/processed/D/D1_\354\226\264\354\227\205\353\260\217\354\226\221\354\213\235\354\203\235\354\202\260\353\237\211.csv"
"data/processed/D/D3_\354\210\230\354\266\234\354\210\230\354\236\205.csv"
"data/processed/D/D3_\354\243\274\354\232\224\352\265\255\353\263\204\352\265\220\354\227\255\353\271\204\354\244\221.csv"
"data/processed/E/E1_UN\355\221\234\352\262\260_\353\214\200\354\235\221\355\221\234.csv"
"data/processed/E/E1_UN\355\221\234\352\262\260_\354\202\254\352\261\264.csv"
"data/processed/E/E1_UN\355\221\234\352\262\260_\355\210\254\355\221\234.csv"
"data/processed/E/E3_\352\265\255\352\260\200\352\260\204\353\217\231\353\247\271\354\240\234\353\217\204\355\231\224.csv"
"data/processed/E/E3_\353\217\231\353\247\271\352\264\200\352\263\204.csv"
"data/processed/E/E3_\353\217\231\353\247\271\352\264\200\352\263\204_\354\227\260\352\262\260.csv"
"data/processed/E/E3_\353\217\231\353\247\271\354\234\240\354\202\254\353\217\204_\354\243\274\354\232\224\352\265\255.csv"
"data/processed/E/E5_\353\202\250\353\266\201\352\264\200\352\263\204\354\227\260\355\221\234_\354\240\225\354\240\234.csv"
"data/processed/F/F1_1\354\235\270\353\213\271\352\265\255\353\257\274\354\264\235\354\206\214\353\223\235_\354\240\225\354\240\234.csv"
"data/processed/F/F1_\352\265\255\353\257\274\354\264\235\354\206\214\353\223\235_\354\240\225\354\240\234.csv"
"data/processed/F/F1_\353\202\250\353\266\201\355\225\234\352\265\220\354\227\255\354\225\241_\354\240\225\354\240\234.csv"
"data/processed/F/F1_\353\213\250\353\260\261\354\247\210_\354\240\225\354\240\234.csv"
"data/processed/F/F1_\353\254\264\354\227\255\354\264\235\354\225\241_\354\240\225\354\240\234.csv"
"data/processed/F/F1_\353\254\264\354\227\255\354\264\235\354\225\241\354\246\235\352\260\220\353\245\240_\354\240\225\354\240\234.csv"
"data/processed/F/F1_\354\213\235\353\237\211\354\236\221\353\254\274\354\203\235\354\202\260\353\237\211_\354\240\225\354\240\234.csv"
"data/processed/F/F1_\354\213\235\353\237\211\354\236\221\353\254\274\354\203\235\354\202\260\353\237\211\354\246\235\352\260\220\353\245\240_\354\240\225\354\240\234.csv"
"data/processed/F/F1_\354\227\220\353\204\210\354\247\200_\354\240\225\354\240\234.csv"
"data/processed/F/F1_\354\235\270\352\265\254_\354\240\225\354\240\234.csv"
"data/processed/F/F1_\354\247\200\353\260\251\354\247\210_\354\240\225\354\240\234.csv"
"data/processed/F/F2_\354\227\260\353\217\204\353\263\204\355\232\214\353\213\264_\354\240\225\354\240\234.csv"
"data/processed/F/F4_\355\206\265\354\235\274\354\235\230\354\213\235\354\241\260\354\202\254_\354\234\204\355\230\221\353\254\270\355\225\255\354\247\221\352\263\204.csv"
"data/processed/F/F4_\355\206\265\354\235\274\354\235\230\354\213\235\354\241\260\354\202\254_\354\235\221\353\213\265\354\236\220_\354\240\225\354\240\234.csv"
data/processed/README.md
"data/processed/\352\263\265\355\206\265_\352\265\255\352\260\200\354\275\224\353\223\234.csv"
"data/processed/\352\263\265\355\206\265_\353\213\250\354\234\204.csv"
"data/processed/\352\263\265\355\206\265_\354\260\270\354\227\254\352\265\255.csv"
db/schema.sql
docs/decisions.md
pages/.gitkeep
requirements.txt
utils/README.md
utils/build_db.py
utils/build_erd.py
utils/helpers.py
"\355\231\210.py"

$ git ls-tree origin/develop | grep 160000 || echo "gitlink 없음"
gitlink 없음

$ git diff --stat develop origin/develop
 .gitignore                                         |     25 +-
 .vscode/settings.default.json                      |      6 +
 .vscode/settings.json                              |      4 -
 README.md                                          |    101 +-
 SOURCES.md                                         |      1 +
 data/processed/.gitkeep                            |      0
 ...1_\355\225\265\354\213\244\355\227\230_CSV.csv" |    641 +
 ...0_\354\235\274\353\213\250\354\234\204_CSV.csv" |   2059 +
 ...4\354\235\274_\353\260\234\354\202\254_CSV.csv" |    318 +
 ...4\353\246\254_\353\217\204\353\260\234_CSV.csv" |     66 +
 ...60\354\202\254\355\233\210\353\240\250_CSV.csv" |     52 +
 ...0\354\202\260_\354\240\204\352\260\234_CSV.csv" |     19 +
 ...4_\354\235\274\353\213\250\354\234\204_CSV.csv" |    119 +
 ...6_\354\227\264\353\263\221\354\213\235_CSV.csv" |     18 +
 ...4\353\246\254_\354\266\251\353\217\214_CSV.csv" |    126 +
 ...7\230_\354\240\204\354\262\230\353\246\254.csv" |     33 +
 ...0\204_\354\240\204\354\262\230\353\246\254.csv" |   6081 +
 ...2\270_\354\240\204\354\262\230\353\246\254.csv" |     37 +
 ...6\265\354\240\234_\354\202\254\352\261\264.csv" |     42 +
 ...63\265\354\225\275\353\254\270\352\265\254.csv" |     28 +
 ...1\224_\354\240\204\354\262\230\353\246\254.csv" |     69 +
 ...0\234_\354\240\204\354\262\230\353\246\254.csv" |     63 +
 ...0\221\354\235\230_\354\202\254\352\261\264.csv" |     68 +
 "data/processed/C/C3_\354\266\234\354\262\230.csv" |    117 +
 ...5\230_\354\240\204\354\262\230\353\246\254.csv" |     86 +
 ...10\230\354\266\234\355\206\265\354\240\234.csv" |    283 +
 ...40\234\354\204\261\354\236\245\353\245\240.csv" |     41 +
 ...57\274\354\264\235\354\206\214\353\223\235.csv" |     81 +
 ...63\204\354\204\261\354\236\245\353\245\240.csv" |    481 +
 ...10\230\354\266\234\354\236\205\354\225\241.csv" |    281 +
 ...54\274\354\203\235\354\202\260\353\237\211.csv" |     81 +
 ...13\235\354\203\235\354\202\260\353\237\211.csv" |     81 +
 ...10\230\354\266\234\354\210\230\354\236\205.csv" |   4455 +
 ...65\220\354\227\255\353\271\204\354\244\221.csv" |   9793 +
 ...2\260_\353\214\200\354\235\221\355\221\234.csv" |  10057 +
 ...1\234\352\262\260_\354\202\254\352\261\264.csv" |  10057 +
 ...1\234\352\262\260_\355\210\254\355\221\234.csv" | 978740 ++++++++++++++++++
 ...47\271\354\240\234\353\217\204\355\231\224.csv" |    790 +
 ...17\231\353\247\271\352\264\200\352\263\204.csv" | 266525 +++++
 ...4\200\352\263\204_\354\227\260\352\262\260.csv" | 400925 +++++++
 ...7\204_\354\243\274\354\232\224\352\265\255.csv" | 180323 ++++
 ...7\260\355\221\234_\354\240\225\354\240\234.csv" |  11516 +
 ...6\214\353\223\235_\354\240\225\354\240\234.csv" |    145 +
 ...6\214\353\223\235_\354\240\225\354\240\234.csv" |    145 +
 ...7\255\354\225\241_\354\240\225\354\240\234.csv" |     37 +
 ...0\261\354\247\210_\354\240\225\354\240\234.csv" |    193 +
 ...4\235\354\225\241_\354\240\225\354\240\234.csv" |     73 +
 ...0\220\353\245\240_\354\240\225\354\240\234.csv" |     73 +
 ...2\260\353\237\211_\354\240\225\354\240\234.csv" |     83 +
 ...0\220\353\245\240_\354\240\225\354\240\234.csv" |     83 +
 ...4\210\354\247\200_\354\240\225\354\240\234.csv" |    193 +
 ...5\270\352\265\254_\354\240\225\354\240\234.csv" |    127 +
 ...0\251\354\247\210_\354\240\225\354\240\234.csv" |    193 +
 ...2\214\353\213\264_\354\240\225\354\240\234.csv" |    668 +
 ...54\270\355\225\255\354\247\221\352\263\204.csv" |     23 +
 ...3\265\354\236\220_\354\240\225\354\240\234.csv" |   1201 +
 data/processed/README.md                           |    262 +
 ...65\255\352\260\200\354\275\224\353\223\234.csv" |    257 +
 ...3\265\355\206\265_\353\213\250\354\234\204.csv" |     76 +
 ...6\265_\354\260\270\354\227\254\352\265\255.csv" |    431 +
 db/schema.sql                                      |     99 +
 docs/decisions.md                                  |     22 +-
 requirements.txt                                   |    Bin 1266 -> 618 bytes
 utils/build_db.py                                  |    267 +
 utils/build_erd.py                                 |    237 +
 app.py => "\355\231\210.py"                        |      0
 66 files changed, 1889525 insertions(+), 52 deletions(-)

```

## 1-4 F0이 손댈 파일의 원격 내용
작업 파일 명령 그대로 실행한 출력:
```text
$ git show origin/develop:config.py
# ==========================================
# 🛡️ 국방 대시보드 프로젝트 전역 설정 파일 (config.py)
# ==========================================

# 1. 분석 관련 설정
HALF_LIFE_DAYS = 14          # 위험도 계산 시 적용할 반감기 (일 단위)
DEFAULT_PERIOD_MONTHS = 6    # 기본 조회 기간 (월 단위)

# 2. 데이터베이스 및 경로 설정
DB_PATH = "data/database.db" # SQLite 데이터베이스 파일 경로

# 3. API 및 기타 설정
# 필요한 공통 상수가 있다면 이곳에 추가하세요.
$ git show origin/develop:.gitignore
fatal: ambiguous argument 'origin\develop;.gitignore': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'

$ git show origin/develop:requirements.txt | file -
/dev/stdin: ASCII text

$ git show origin/develop:requirements.txt | iconv -f UTF-16 -t UTF-8 2>/dev/null || git show origin/develop:requirements.txt
慴瑲猽㴲㘮ㄮ《捥牴楦椽㴲〲㘮㜮㈲੣桡牳整⵮潲浡汩穥爽㴳⸵⸱੣汩捫㴽㠮㔮《栱ㄽ㴰⸱㘮《桴瑰瑯潬猽㴰⸸⸰੩摮愽㴳⸱㤊楴獤慮来牯畳㴽㈮㈮《䵡牫異卡晥㴽㌮〮㌊湡牷桡汳㴽㈮㈶⸰੮畭灹㴽㈮㐮㘊灡捫慧楮朽㴲㘮㌊灩汬潷㴽ㄲ⸳⸰ੰ牯瑯扵昽㴷⸳㘮ㄊ灹慲牯眽㴲㔮〮ㄊ灹瑨潮ⵤ慴敵瑩氽㴲⸹⸰⹰潳琰ੰ祴桯渭浵汴楰慲琽㴰⸰⸳㈊牥晥牥湣楮朽㴰⸳㜮《牥煵敳瑳㴽㈮㌴⸲ੲ灤猭灹㴽㈰㈶⸶⸳ੳ楸㴽ㄮㄷ⸰ੴ潭氽㴰⸱〮㈊瑹灩湧彥硴敮獩潮猽㴴⸱㘮《瑺摡瑡㴽㈰㈶⸴ੵ牬汩戳㴽㈮㜮《當楣潲渽㴰⸵㈮㐊睡瑣桤潧㴽㘮〮《睥扳潣步瑳㴽ㄶ⸱⸱ੳ瑲敡浬楴㸽ㄮ㐰⸰ੰ慮摡猾㴲⸰⸰ੰ汯瑬社㴵⸰⸰੮整睯牫砾㴳⸱੣潵湴特ⵣ潮癥牴敲㸽ㄮ㈮《杯潧汥ⵣ汯畤ⵢ楧煵敲社㴳⸱〮《灹瑨潮ⵤ潣砾㴱⸱⸰
$ git show origin/develop:.github/pull_request_template.md
fatal: ambiguous argument 'origin\develop;.github\pull_request_template.md': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'

$ git show origin/develop:utils/README.md || echo "없음"
## 유틸리티 모듈 (`utils/helpers.py`)
프로젝트 전반에서 공통으로 사용하는 함수들을 `utils/helpers.py`에 모아두었습니다.

* **`load_sample_data()`**: 샘플 데이터프레임을 불러옵니다. (추후 `data/` 폴더의 CSV 파일 연동 가능)
* **`preprocess_data(df)`**: 데이터 전처리(예: 특정 조건 필터링)를 수행합니다.
* **`show_footer()`**: 앱 하단에 공통 푸터를 출력합니다.

### 코드 사용 방법 (Usage Example)
메인 파일(`app.py`)에서 모듈을 불러와 사용하는 방식입니다:

```python
import streamlit as st
from utils.helpers import load_sample_data, preprocess_data, show_footer

# 데이터 로드 및 전처리 예시
df = load_sample_data()
if df is not None:
    processed_df = preprocess_data(df)
    st.dataframe(processed_df)

show_footer()
```
$ git show origin/develop:README.md | grep -n -E "^(<<<<<<<|=======|>>>>>>>)" || echo "충돌 표시 없음"
충돌 표시 없음

```

**보충 (작업 파일에 없는 추가 실행, 파일은 건드리지 않음):** 위에서 `.gitignore`·`pull_request_template.md` 두 줄은 Git Bash(MSYS)가 `origin/develop:경로` 인자를 Windows 경로로 바꿔서(`origin\develop;.gitignore`) 실패함. `MSYS_NO_PATHCONV=1`로 같은 명령을 다시 실행한 출력. 또 원격 `requirements.txt`는 `file`이 ASCII로 판정했는데 1-4의 iconv 줄이 UTF-16으로 강제 변환해 글자가 깨졌으므로(iconv가 성공해 `||` 뒤가 실행되지 않음) 원본을 그대로 다시 출력함.
```text
$ MSYS_NO_PATHCONV=1 git show origin/develop:.gitignore
# --- 파이썬 바이트 컴파일 / 최적화 / DLL 파일 ---
__pycache__/
*.py[codz]
*$py.class

# C 확장 파일
*.so

# 배포 및 패키징 관련 파일
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller 관련 (실행파일 빌드 시 생성되는 파일)
# 보통 이 파일들은 PyInstaller가 실행 파일(.exe)을 빌드하기 전에
# 날짜나 기타 정보를 주입하기 위해 템플릿을 기반으로 파이썬 스크립트가 작성하는 파일들입니다.
*.manifest
*.spec

# 패키지 설치 로그
pip-log.txt
pip-delete-this-directory.txt

# 유닛 테스트 및 커버리지 리포트
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py.cover
.hypothesis/
.pytest_cache/
cover/

# 번역 파일
*.mo
*.pot

# 장고(Django) 관련
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# 플라스크(Flask) 관련
instance/
.webassets-cache

# 스크라피(Scrapy) 관련
.scrapy

# 스핑크스(Sphinx) 문서 빌드 결과물
docs/_build/

# 파이빌더(PyBuilder) 관련
.pybuilder/
target/

# 주피터 노트북 체크포인트
.ipynb_checkpoints

# 아이파이썬(IPython) 관련
profile_default/
ipython_config.py

## 피브엔프(pyenv) 버전 지정 파일 (필요시 주석 해제)
#   라이브러리나 패키지의 경우 여러 환경에서 실행을 테스트해야 하므로
#   이 파일을 무시(gitignore)하는 것이 좋습니다.
#   그렇지 않은 일반 프로젝트라면 Git에 포함(커밋)하세요:
# .python-version

# 핍env (Pipenv) 관련 잠금 파일
#   pypa/pipenv 이슈 #598에 따르면, 버전 관리(Git)에 Pipfile.lock을 포함하는 것이 권장됩니다.
#   하지만 협업 시 플랫폼(OS)에 종속적인 패키지가 있거나 크로스 플랫폼을 지원하지 않는 패키지가 있다면,
#   pipenv가 작동하지 않는 의존성을 설치하거나 필요한 의존성 전체를 설치하지 못할 수 있습니다.
# Pipfile.lock

# UV 패키지 매니저 잠금 파일
#   Pipfile.lock과 마찬가지로, 일반적으로 버전 관리(Git)에 uv.lock을 포함하는 것이 권장됩니다.
#   특히 실행 가능한(바이너리) 패키지의 경우 재현성을 보장하기 위해 포함하는 것이 좋으며,
#   라이브러리의 경우 보통 무시(gitignore)하는 편입니다.
# uv.lock

# 포이트리 (Poetry) 관련 잠금 파일
#   Pipfile.lock과 마찬가지로, 일반적으로 버전 관리(Git)에 poetry.lock을 포함하는 것이 권장됩니다.
#   특히 실행 가능한(바이너리) 패키지의 경우 재현성을 보장하기 위해 포함하는 것이 좋으며,
#   라이브러리의 경우 보통 무시(gitignore)하는 편입니다.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
# poetry.lock
# poetry.toml

# PDM 패키지 매니저 관련
#   Pipfile.lock과 마찬가지로, 일반적으로 버전 관리(Git)에 pdm.lock을 포함하는 것이 권장됩니다.
#   pdm은 프로젝트 전체 설정인 pdm.toml은 포함하고, .pdm-python은 제외할 것을 권장합니다.
#   https://pdm-project.org/en/latest/usage/project/#working-with-version-control
# pdm.lock
# pdm.toml
.pdm-python
.pdm-build/

# 픽시 (Pixi) 가상환경 및 잠금 파일
#   Pipfile.lock과 마찬가지로, 일반적으로 버전 관리(Git)에 pixi.lock을 포함하는 것이 권장됩니다.
# pixi.lock
#   Pixi는 venv 모듈이 .venv 디렉토리를 만드는 것과 마찬가지로, .pixi 디렉토리 안에 가상 환경을 생성합니다.
#   이 디렉토리는 버전 관리에 포함하지 않는 것(Git 무시)을 권장합니다.
.pixi

# PEP 582 패키지 디렉토리
# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# 샐러리(Celery) 관련
celerybeat-schedule
celerybeat.pid

# 레디스(Redis) 관련
*.rdb
*.aof
*.pid

# 래빗MQ 관련
mnesia/
rabbitmq/
rabbitmq-data/

# 액티브MQ 관련
activemq-data/

# 세이지매스(SageMath) 파싱 파일
*.sage.py

# 가상환경 폴더들 (절대 커밋 금지)
.env
.envrc
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# 스파이더(Spyder) 프로젝트 설정
.spyderproject
.spyproject

# 로프(Rope) 프로젝트 설정
.ropeproject

# mkdocs 문서 빌드 폴더
/site

# 마이피(mypy) 타입 체커 캐시
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre 타입 체커
.pyre/

# pytype 정적 분석기 pytype static type analyzer
.pytype/

# 사이톤(Cython) 디버그 심볼
cython_debug/

# 파이참(PyCharm) 등 JetBrains IDE 설정
#   JetBrains 전용 템플릿은 별도의 JetBrains.gitignore로 관리되며,
#   https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore 에서 확인할 수 있습니다.
#   이 템플릿은 글로벌 gitignore에 추가하거나 이 파일에 병합할 수 있습니다.
#   더 강력한(전부 차단하는) 방법으로는(권장하지 않음), 다음 주석을 해제하여 전체 .idea 폴더를 무시할 수 있습니다.
# .idea/

# Abstra 자동화 프레임워크 설정
#   Abstra는 AI 기반 프로세스 자동화 프레임워크입니다.
#   사용자 인증 정보, 로컬 상태 및 설정이 포함된 디렉토리를 무시합니다.
#   자세한 내용은 https://abstra.io/docs 에서 확인하세요.
.abstra/

# 비주얼 스튜디오 코드(VS Code) 설정 (필요시 주석 해제)
#   Visual Studio Code 전용 템플릿은 별도의 VisualStudioCode.gitignore로 관리되며,
#   https://github.com/github/gitignore/blob/main/Global/VisualStudioCode.gitignore 에서 확인할 수 있습니다.
#   이 템플릿은 글로벌 gitignore에 추가하거나 이 파일에 병합할 수 있습니다.
#   하지만 원하신다면, 다음 주석을 해제하여 전체 .vscode 폴더를 무시할 수도 있습니다.
# .vscode/

# 부분 코드 실행을 위한 임시 파일
tempCodeRunnerFile.py

# Ruff 린터 캐시
.ruff_cache/

# PyPI 설정 파일
.pypirc

# Marimo 관련
marimo/_static/
marimo/_lsp/
__marimo__/

# Streamlit 비밀키 설정 파일 (배포 시 보안 필수)
.streamlit/secrets.toml

# --- 국방 대시보드 팀 프로젝트 추가 보안 및 데이터 관리 ---

# 로컬 SQLite 데이터베이스 파일 (100MB 용량 제한 대응)
data/*.db
data/*.sqlite

# 빅쿼리(BigQuery) 등 서비스 계정 인증 JSON 키 및 비밀키 폴더
*.json
secrets/

# SSH 키 파일 차단
*.pem

# 원본 데이터 폴더 차단 (내부 README만 예외 허용)
data/raw/*
!data/raw/README.md

# 가공된 데이터 및 벡터DB 등 대용량 파일 차단
data/processed/*.db
data/processed/chroma/
data/processed/_*
data/processed/fund_chunks/

!data/processed/*.csv

# 운영체제 생성 파일 및 로그
.DS_Store
*.log

# .vscode /* 환경 고정 커밋 금지
# 3 : 1 환경 기준
.vscode/*
!.vscode/settings.default.json

$ MSYS_NO_PATHCONV=1 git show origin/develop:.github/pull_request_template.md
## 요약
- 이번 PR에서 처리한 핵심 작업 내용을 간략히 요약해주세요.

## 관련 이슈
- closes # (연결할 이슈 번호를 적어주세요. 예: closes #1)

## 변경 사항
- 주요 코드 변경 사항이나 추가된 기능을 적어주세요.
- 

## 테스트
- 어떤 방식으로 테스트를 거쳤는지 확인 내용을 적어주세요.
- 

## 체크리스트
- [ ] `.env` 등 민감 파일 커밋 안 함
- [ ] 응답/데이터 스키마 변경 시 관련 문서 반영
- [ ] (해당 시) 도메인 함정 확인

$ git show origin/develop:requirements.txt   (변환 없이 원본)
attrs==26.1.0
certifi==2026.7.22
charset-normalizer==3.5.1
click==8.5.0
h11==0.16.0
httptools==0.8.0
idna==3.19
itsdangerous==2.2.0
MarkupSafe==3.0.3
narwhals==2.26.0
numpy==2.4.6
packaging==26.3
pillow==12.3.0
protobuf==7.36.1
pyarrow==25.0.1
python-dateutil==2.9.0.post0
python-multipart==0.0.32
referencing==0.37.0
requests==2.34.2
rpds-py==2026.6.3
six==1.17.0
toml==0.10.2
typing_extensions==4.16.0
tzdata==2026.4
urllib3==2.7.0
uvicorn==0.52.4
watchdog==6.0.0
websockets==16.1.1
streamlit>=1.40.0
pandas>=2.0.0
plotly>=5.0.0
networkx>=3.1
country-converter>=1.2.0
google-cloud-bigquery>=3.10.0
python-docx>=1.1.0

$ git show develop:requirements.txt | file -   (비교용: 로컬 develop)
/dev/stdin: Unicode text, UTF-16, little-endian text, with CRLF line terminators
```

보충 2 — 원격 README가 가리키는 파일과 원격 트리 비교용:
```text
$ git show origin/develop:README.md | grep -n -E "real.py|loader.py|build_db|schema.sql|pages/|settings.default|홈.py|app.py"
47:│   └── settings.default.json       # 팀 공유용 기본 설정 템플릿
56:│   └── schema.sql                  # ERD v4 기준 SQLite 테이블 
59:├── pages/                       # 멀티페이지 화면 (파일명 앞 숫자 = 메뉴 순서)
65:│   └── build_db.py                 # CSV를 읽어 SQLite DB를 만드는 스크립트
69:│   └── loader.py                   # 데이터 통로: USE_DUMMY에 따라 dummy 또는 real을 불러옴 (캐시 적용)
71:│   └── real.py                     # 실제 사건 CSV → 원점수·평소대비·단계 계산 (결과_일별·월별·연별)
74:├── 홈.py                        # 메인 실행 파일
148:- BigQuery 및 외부 API 호출은 별도 수집 스크립트에서만 수행하고, Streamlit(`app.py`)은 오직 SQLite 데이터만 읽어 성능을 보장합니다.
161:streamlit run 홈.py

$ git diff --stat develop origin/develop -- utils/README.md README.md
 README.md | 101 +++++++++++++++++++++++++++++++++++++++-----------------------
 1 file changed, 63 insertions(+), 38 deletions(-)
```

## 1-5 pull --ff-only 막힘 여부
**판단: 막힘** — 로컬에서 커밋 안 된 채 수정된 `README.md`·`docs/decisions.md`·`.vscode/settings.json`을 원격도 바꿨으므로(`.vscode/settings.json`은 원격에서 삭제) `git pull --ff-only`는 "local changes would be overwritten"으로 멈춘다. (`utils/README.md`는 로컬만 수정, 원격 변경 없음)
```text
$ git diff --stat develop origin/develop -- docs/decisions.md .vscode/settings.json docs/dev config.py requirements.txt .gitignore
 .gitignore            |  25 ++++++++++++++++---------
 .vscode/settings.json |   4 ----
 docs/decisions.md     |  22 +++++++++++++++++++++-
 requirements.txt      | Bin 1266 -> 618 bytes
 4 files changed, 37 insertions(+), 14 deletions(-)

$ git ls-tree origin/develop -- .vscode/settings.json || true

$ git check-ignore -v .vscode/settings.json || echo "현재 로컬 .gitignore로는 무시 안 됨"
현재 로컬 .gitignore로는 무시 안 됨

```

## 1-6 이슈·PR·라벨
```text
$ gh label list || true
feat	새로운 기능 추가	#0e8a16
fix	버그 및 오류 수정	#d93f0b
docs	문서 작성 및 README 수정	#0075ca
refactor	코드 구조 개선	#7057ff
chore	환경 설정 및 잡다한 작업	#fef2c0
critical	대시보드가 아예 실행되지 않거나, 데이터가 유출되는 등 즉시 해결해야 하는 치명적인 버그	#b60205
ui-bug	로직은 맞지만 Streamlit 대시보드의 레이아웃이 깨지거나 스타일이 어긋나는 시각적 오류	#fbca04
bug	프로그램이 정상 작동하지 않거나 에러가 발생하는 일반적인 버그	#b0178f
data-error	데이터베이스 연동 실패나 잘못된 데이터 파싱으로 인해 값이 비거나 다르게 나오는 오류	#d93f0b
enhancement	완전히 새로운 기능을 만드는 것(feat)은 아니지만, 기존 기능을 더 편리하게 다듬거나 성능을 개선하는 작업	#0052cc
help wanted	혼자 해결하기 어렵거나 팀원들의 아이디어나 도움이 필요한 이슈에 붙이는 라벨	#006b75
wip	아직 완성되지 않았지만 현재 열심히 개발 중인 이슈나 PR임을 알리는 라벨	#8e5688

$ gh issue list --state all --limit 10 || true
9	CLOSED	[REFACTOR] 증감률 지표 지표값 적재 제외	refactor	2026-10-23T06:15:46Z
7	CLOSED	[FEAT] ERD v4 기준 대기능1 테이블 분리(기준-데이터-보조)	enhancement	2026-10-22T06:05:00Z

$ gh pr list --state all --limit 10 || true
11	data: A4, A6 2021~2026 행 추가, A7 주체국 보완	feature/a-data-update	MERGED	2026-10-28T06:58:25Z
10	refactor: 증감률 지표 지표값 적재 제외(원 지표에서 계산)	feature/exclude-growth-rate	MERGED	2026-10-22T08:11:20Z
8	[FEAT]ERD v4 기준 대기능1 테이블 분리 (기준-데이터-보조-상세 13개)	feature/erd-v4-tables	MERGED	2026-10-22T05:40:11Z
6	feat: 전처리 CSV를 SQLite 통합 DB로 적재하는 빌드 스크립트 추가	feature/erd-integration	MERGED	2026-10-22T01:17:10Z
5	dsssadas	develop	MERGED	2026-09-29T08:17:13Z
2	Main	main	MERGED	2026-09-18T04:27:25Z
1	txt files	develop	MERGED	2026-09-16T00:20:36Z

```

## 막힌 것 · 이상한 것
1. 로컬 `develop`이 `origin/develop`보다 27 커밋 뒤(앞선 커밋 0). 원격 HEAD는 `develop`(a05b019).
2. 로컬 미커밋 수정 4개 중 3개(`README.md`, `docs/decisions.md`, `.vscode/settings.json`)를 원격도 바꿈 → 1-5의 `pull --ff-only` 막힘.
3. `.vscode/settings.json`: 원격에서 삭제되고 `.vscode/settings.default.json`이 추가됨. 원격 `.gitignore`는 `.vscode/*` 무시 + `!.vscode/settings.default.json` 예외. 현재 로컬 `.gitignore`로는 `.vscode/settings.json`이 무시되지 않음.
4. 원격 `.gitignore`에 `*.json` 전체 무시 규칙이 있음(`.vscode/settings.default.json`은 `!` 예외로 따로 허용).
5. `requirements.txt` 인코딩: 로컬 develop 버전은 UTF-16 LE·CRLF, 원격 버전은 ASCII(UTF-8 호환)로 바뀜(1266 → 618 bytes). 원격 버전에서 `streamlit`·`pandas` 등은 `>=` 하한만, 나머지는 `==` 고정. `pytest`·`openpyxl`은 원격 requirements에 없음(로컬 Python엔 둘 다 설치됨).
6. 원격 README가 설명하는 `utils/loader.py`, `utils/real.py`, `pages/` 아래 1~4 페이지 파일은 원격 트리에 없음(`pages/`엔 `.gitkeep`만). `홈.py`, `utils/build_db.py`, `db/schema.sql`, `.vscode/settings.default.json`은 있음. 원격 README 148행엔 아직 `app.py`가 언급됨(파일은 `app.py` → `홈.py`로 이름 바뀜).
7. 원격 `utils/README.md`는 여전히 `helpers.py`·`app.py` 기준 설명(로컬 develop과 차이 없음). 원격 트리엔 `utils/build_erd.py`도 새로 있음(README 언급 여부는 확인 안 함).
8. 원격 `config.py`는 `HALF_LIFE_DAYS`, `DEFAULT_PERIOD_MONTHS`, `DB_PATH = "data/database.db"`만 있음.
9. 원격 README에 충돌 표시(`<<<<<<<` 등) 없음. gitlink(서브모듈) 없음.
10. 이 셸(Git Bash)에서 `git show origin/develop:<경로>` 중 경로가 `.`으로 시작하는 두 줄이 MSYS 경로 변환으로 실패함(1-4 보충 참고). `config.py`·`requirements.txt`·`utils/README.md`·`README.md`는 정상.
11. 1-4의 `iconv -f UTF-16` 줄은 원격 파일이 ASCII라서 깨진 글자를 출력함(실패로 판정되지 않아 대체 명령이 안 돌았음).
12. `git fetch`로 원격 브랜치 5개를 새로 받음: `feature/a-data-update`, `feature/erd-integration`, `feature/erd-v4-tables`, `feature/exclude-growth-rate`, `feature/tension-dashboard`. 이 중 `feature/tension-dashboard`는 1-6 PR 목록(최근 10개)에 없음.
13. 이슈는 닫힌 2개(#7, #9)만 보임. PR #5 제목이 `dsssadas`. 라벨 `fix`·`data-error`가 같은 색(#d93f0b).
14. 환경: Python 3.14.6, numpy 2.4.6, pandas 3.0.3, pytest 9.0.3, openpyxl 3.1.5, streamlit 1.58.0, gh 2.97.0(money2082 로그인, scope repo 포함).
