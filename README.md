# 국방 대시보드 (Defense Dashboard)

## 1. 프로젝트 소개
- **개발 배경 및 목적** :
- **주요기능**
 - 대한민국 안보·위험도 예측
 - 대한민국과 타국과의 관계도

---

## 2.팀원 역할 분담 (Contributors)
| 이름 | 담당 역할 | 주요 기여 내용 |
| :---: | :---: | :--- |
| **박성인** | TA | :--- |
| **이원희** | AA | :--- |
| **고현진** | AA | :--- |
| **남석현** | DA | :--- |

---

## 3. 기술 스텍 (Tech Stack)
### 개발 기반
 - **Python 3.11** ()
 - **Git & GitHub** ()
 - **Streamlit Community Cloud** ()
### 화면·배포
 - **Streamlit** ()
 - **Ploty** ()
### 계산 및 데이터 처리
 - **Pandas** ()
 - **NetworkX** ()
 - **Country Converter** ()
### 데이터 저장소
 - **SQLite** ()
### 데이터 수집
 - **Requests** ()
 - **Google Cloud BigQuery** ()
 - **수동 수집** ()

---

## 4. 프로젝트 폴더 구조 (Directory Structure)
```text
Team-Project/
├── .github/                   # 이슈 및 PR 템플릿
├── .streamlit/                # 스트림릿 디자인 및 설정 파일 (.toml)
├── .vscode/                   # VS Code 에디터 설정 (settings.json)
├── data/                      # 원본 및 샘플 데이터 파일 (.csv, SQLite 등)
├── docs/                      # 프로젝트 문서화 폴더
│   └── decisions.md           # 주요 설정값 및 기술 의사결정 기록
├── pages/                     # 멀티페이지 대시보드 화면 파일들
├── utils/                     # 공통 함수 및 전처리 모듈
│   └── helpers.py             # 데이터 로드, 전처리, 공통 UI 함수 모음
├── .gitignore                 # 깃 제외 파일 목록 (보안 키, 대용량 파일 차단)
├── app.py                     # 메인 실행 파일
├── config.py                  # 프로젝트 전역 설정값 모음 (반감기, 기준 기간 등)
├── README.md                  # 프로젝트 소개 및 가이드 문서
└── requirements.txt           # 패키지 의존성 목록 (버전 고정)
```
---

## 5. 협업 규칙 및 템플릿 사용법 (Workflow & Templates)

우리 팀은 원활한 협업과 코드 품질 관리를 위해 다음과 같은 규칙과 템플릿을 사용합니다.

### 1. 이슈(Issue) 활용법 (`.github/ISSUE_TEMPLATE/feature.md`)
- 새로운 기능을 개발하거나 작업을 시작하기 전, 반드시 깃허브 **[Issues]** 탭에서 이슈를 먼저 생성합니다.
- 템플릿 양식(**배경, 범위, 완료 조건**)에 맞춰 작성하여 팀원들과 작업 내용을 공유합니다.

### 2. 풀 리퀘스트(Pull Request) 템플릿 (`.github/pull_request_template.md`)
- 코드 작성이 끝나고 `main` 브랜치로 병합(Merge)을 요청할 때 자동으로 적용되는 양식입니다.
- **체크리스트 확인 사항:**
  - `[ ]` `.env` 또는 보안 키 파일이 실수로 커밋되지 않았는지 확인[cite: 9]
  - `[ ]` 응답/데이터 스키마 변경 시 관련 문서 반영 확인[cite: 9]
  - `[ ]` 주요 기능 테스트 완료

---

## 6. 개발 가이드 및 보안 원칙

다음 폴더와 파일들은 보안 및 용량 문제로 인해 **깃허브에 커밋되지 않도록(`.gitignore`) 설정**되어 있습니다.
- **데이터 폴더 (`data/`)**: 대용량 SQLite(`.db`) 파일은 깃 제외 대상이며, 로컬 테스트용 또는 샘플 중심으로 관리합니다.
- **인증키 및 환경변수 (`.env`, `secrets/`)**: BigQuery 서비스 계정 JSON 키 및 API 비밀키는 절대 업로드하지 않으며, 배포 시 Streamlit `st.secrets`를 활용합니다. - 필요시 생성 예정 -

### 1. 수집과 화면 코드 분리
- BigQuery 및 외부 API 호출은 별도 수집 스크립트에서만 수행하고, Streamlit(`app.py`)은 오직 SQLite 데이터만 읽어 성능을 보장합니다.

### 2. 보안 및 인증키 관리
- BigQuery 서비스 계정 JSON 키 및 API 비밀키는 절대 깃허브에 업로드하지 않습니다 (`.gitignore` 필수 등록 및 Streamlit Cloud 배포 시 `st.secrets` 활용).

### 3. 용량 관리
- GitHub 파일 제한(100MB) 대응을 위해 대용량 SQLite(`.db`) 파일은 깃 제외 처리하고 샘플 데이터 위주로 공유합니다.

### 4. 설정값 및 의사결정 문서화
- 반감기(14일) 등의 주요 파라미터는 `config.py`에 집중 관리하며, 채택 근거는 `docs/decisions.md`에 기록합니다.

---

## 커밋

우리 팀은 커밋 메시지만 보고도 어떤 작업인지 파악할 수 있도록 아래의 말머리 규칙을 따릅니다.

###  말머리 종류
* **`feat`**: 새로운 기능 추가 (예: `feat: 대시보드 사이드바 필터 기능 구현`)
* **`fix`**: 버그 수정 (예: `fix: 데이터 로드 시 NoneType 에러 수정`)
* **`docs`**: 문서 수정 (예: `docs: README에 Git 가이드 및 템플릿 사용법 추가`)
* **`refactor`**: 코드 리팩토링 (기능 변화 없이 구조 개선)
* **`style`**: 코드 형식 변경, 세미콜론 누락, 스타일 수정 (로직 변경 없음)
* **`test`**: 테스트 코드 추가 및 수정
* **`chore`**: 빌드 업무 수정, 패키지 매니저 설정 등 잡다한 작업 (예: `chore: requirements.txt 라이브러리 버전 업데이트`)

###  작성 요약 형식
```text
말머리(영소문자): 간결한 작업 내용 요약 (50자 이내)

[본문 내용 선택사항 - 상세 설명이 필요한 경우 작성]
## 7. Git & GitHub 실무 명령어 가이드

프로젝트 협업 시 자주 사용하는 Git 명령어 정리입니다.
```

### 기본 저장 및 기록
```bash
# Git 저장소 초기화
git init

# 변경 사항을 깃허브에 업로드하는 표준 순서
git add .
git commit -m "메모 작성"
git push origin develop

# 스테이징 (Staging Area로 이동)
git add 파일명                  # 특정 파일만 추가
git add 파일명1 파일명2         # 여러 파일 동시 추가
git add .                     # 변경된 모든 파일 추가

# 커밋 (Repository에 기록)
git commit -m "커밋 메시지 메모"

# 현재 작업 상태 확인
git status

# 전체 커밋 내역 간결하게 조회
git log --all --oneline

# 변경점 비교 (Diff)
git difftool                  # 수정된 파일 차이점 비교
git difftool 커밋아이디         # 특정 커밋 간 차이점 비교

# 브랜치 생성 및 이동
git branch 브랜치명             # 브랜치 생성
git switch 브랜치명             # 해당 브랜치로 이동

# 브랜치 삭제
git branch -d 브랜치명          # 이미 머지(Merge)된 브랜치 삭제
git branch -D 브랜치명          # 머지되지 않은 브랜치 강제 삭제

# 1. 기준 브랜치로 이동 후 합치기 (※ 같은 줄 수정 시 충돌 주의)
git merge 합칠브랜치명

# 2. 서브 브랜치의 여러 커밋을 하나로 압축하여 main에 커밋
git merge --squash 새브랜치

# 파일 수정 사항 취소 (최근 커밋 상태로 복구)
git restore 파일명

# 특정 커밋 시점으로 파일 상태 돌리기
git restore --source 커밋아이디 파일명

# 특정 커밋의 작업 내역을 취소하는 새로운 커밋 생성 (가장 안전한 방법)
git revert 커밋아이디
