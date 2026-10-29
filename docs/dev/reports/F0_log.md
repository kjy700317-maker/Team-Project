# F0 실행 로그

실행 python = `C:/Users/money/anaconda3/envs/python311/python.exe` 직접 호출(사용자 결정 10-28 — `conda run -n python311`은 base 3.14.6을 잡음, L1). 아래 `<python311>`은 이 경로.

## L1 시작 전 점검 (1절) — 1차 실행 + 원인 확인

```
$ git status --porcelain
 M .vscode/settings.json
 M README.md
 M docs/decisions.md
 M utils/README.md
?? .obsidian/
?? docs/dev/
?? "\354\247\204\355\226\211 \355\230\204\355\231\251 \353\260\217 \352\263\204\355\232\215 \354\240\225\353\246\254/"

$ git branch --show-current
develop

$ git fetch origin
From https://github.com/kjy700317-maker/Team-Project
 * [new branch]      docs/readme-db-files -> origin/docs/readme-db-files

$ git log --oneline -3 origin/develop
064c655 Merge pull request #13 from kjy700317-maker/docs/readme-db-files
8b5724f docs: README 폴더 구조에 DB 빌드 파일 설명추가
a05b019 doc: 들여쓰기 수정

$ git rev-list --left-right --count develop...origin/develop
0	29

$ conda env list
Error while loading conda entry point: conda-anaconda-telemetry (cannot import name 'CondaRequestHeader' from 'conda.plugins' (C:\Users\money\anaconda3\Lib\site-packages\conda\plugins\__init__.py))
Error while loading conda entry point: conda-anaconda-tos (cannot import name 'CondaPreCommand' from 'conda.plugins' (C:\Users\money\anaconda3\Lib\site-packages\conda\plugins\__init__.py))
Error while loading conda entry point: repo (cannot import name 'CondaSubcommand' from 'conda.plugins' (C:\Users\money\anaconda3\Lib\site-packages\conda\plugins\__init__.py))
Error while loading conda entry point: conda-anaconda-telemetry (cannot import name 'CondaRequestHeader' from 'conda.plugins' (C:\Users\money\anaconda3\Lib\site-packages\conda\plugins\__init__.py))
Error while loading conda entry point: conda-anaconda-tos (cannot import name 'CondaPreCommand' from 'conda.plugins' (C:\Users\money\anaconda3\Lib\site-packages\conda\plugins\__init__.py))
Error while loading conda entry point: repo (cannot import name 'CondaSubcommand' from 'conda.plugins' (C:\Users\money\anaconda3\Lib\site-packages\conda\plugins\__init__.py))

# conda environments:
#
# * -> active
# + -> frozen
base                     C:\Users\money\anaconda3
python311                C:\Users\money\anaconda3\envs\python311


$ conda run -n python311 python --version
WARNING conda.plugins.manager:load_entrypoints(378): Error while loading conda entry point: conda-anaconda-telemetry (cannot import name 'CondaRequestHeader' from 'conda.plugins' (C:\Users\money\anaconda3\Lib\site-packages\conda\plugins\__init__.py))
WARNING conda.plugins.manager:load_entrypoints(378): Error while loading conda entry point: conda-anaconda-tos (cannot import name 'CondaPreCommand' from 'conda.plugins' (C:\Users\money\anaconda3\Lib\site-packages\conda\plugins\__init__.py))
WARNING conda.plugins.manager:load_entrypoints(378): Error while loading conda entry point: repo (cannot import name 'CondaSubcommand' from 'conda.plugins' (C:\Users\money\anaconda3\Lib\site-packages\conda\plugins\__init__.py))
WARNING conda.plugins.manager:load_entrypoints(378): Error while loading conda entry point: conda-anaconda-telemetry (cannot import name 'CondaRequestHeader' from 'conda.plugins' (C:\Users\money\anaconda3\Lib\site-packages\conda\plugins\__init__.py))
WARNING conda.plugins.manager:load_entrypoints(378): Error while loading conda entry point: conda-anaconda-tos (cannot import name 'CondaPreCommand' from 'conda.plugins' (C:\Users\money\anaconda3\Lib\site-packages\conda\plugins\__init__.py))
WARNING conda.plugins.manager:load_entrypoints(378): Error while loading conda entry point: repo (cannot import name 'CondaSubcommand' from 'conda.plugins' (C:\Users\money\anaconda3\Lib\site-packages\conda\plugins\__init__.py))
Python 3.14.6

$ conda run -n python311 python -c "import numpy, pandas, pytest, openpyxl; print(numpy.__version__, pandas.__version__, pytest.__version__, openpyxl.__version__)"
WARNING conda.plugins.manager:load_entrypoints(378): Error while loading conda entry point: conda-anaconda-telemetry (cannot import name 'CondaRequestHeader' from 'conda.plugins' (C:\Users\money\anaconda3\Lib\site-packages\conda\plugins\__init__.py))
WARNING conda.plugins.manager:load_entrypoints(378): Error while loading conda entry point: conda-anaconda-tos (cannot import name 'CondaPreCommand' from 'conda.plugins' (C:\Users\money\anaconda3\Lib\site-packages\conda\plugins\__init__.py))
WARNING conda.plugins.manager:load_entrypoints(378): Error while loading conda entry point: repo (cannot import name 'CondaSubcommand' from 'conda.plugins' (C:\Users\money\anaconda3\Lib\site-packages\conda\plugins\__init__.py))
WARNING conda.plugins.manager:load_entrypoints(378): Error while loading conda entry point: conda-anaconda-telemetry (cannot import name 'CondaRequestHeader' from 'conda.plugins' (C:\Users\money\anaconda3\Lib\site-packages\conda\plugins\__init__.py))
WARNING conda.plugins.manager:load_entrypoints(378): Error while loading conda entry point: conda-anaconda-tos (cannot import name 'CondaPreCommand' from 'conda.plugins' (C:\Users\money\anaconda3\Lib\site-packages\conda\plugins\__init__.py))
WARNING conda.plugins.manager:load_entrypoints(378): Error while loading conda entry point: repo (cannot import name 'CondaSubcommand' from 'conda.plugins' (C:\Users\money\anaconda3\Lib\site-packages\conda\plugins\__init__.py))
2.4.6 3.0.3 9.0.3 3.1.5

$ ls envs/python311/python.exe & version
-rwxr-xr-x 2 money 197613 105288 Oct  2 05:23 /c/Users/money/anaconda3/envs/python311/python.exe
Python 3.11.17
$ conda run -n python311 python -c "import sys; print(sys.executable)"
C:\Users\money\anaconda3\python.exe
$ which -a python
/c/Users/money/anaconda3/python
/c/Users/money/unwash-preprocess/.venv/Scripts/python
/c/Users/money/AppData/Local/Microsoft/WindowsApps/python
/c/Users/money/AppData/Local/Programs/Python/Python39/python
/c/Users/money/AppData/Local/Programs/Python/Python311/python
$ git diff --stat a05b019 origin/develop
 README.md | 8 ++++----
 1 file changed, 4 insertions(+), 4 deletions(-)
$ git diff --name-only develop origin/develop
.gitignore
.vscode/settings.default.json
.vscode/settings.json
README.md
SOURCES.md
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
requirements.txt
utils/build_db.py
utils/build_erd.py
"\355\231\210.py"
$ <envs/python311/python.exe> -c "import numpy, pandas, pytest, openpyxl; ..."
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'pytest'
$ conda --version
conda 26.9.1
$ git log --oneline a05b019..origin/develop
064c655 Merge pull request #13 from kjy700317-maker/docs/readme-db-files
8b5724f docs: README 폴더 구조에 DB 빌드 파일 설명추가
$ <envs/python311/python.exe> 개별 import
numpy 2.4.6
pandas 3.0.6
ModuleNotFoundError: No module named 'pytest'
ModuleNotFoundError: No module named 'openpyxl'
```

## L1b 환경 보완 (사용자 결정 후)

```
# 사용자 결정 10-28: env python 직접 호출, pytest·openpyxl 설치 허락
$ <python311> -m pip install pytest==9.0.3 openpyxl==3.1.5
Successfully installed colorama-0.4.6 et-xmlfile-2.0.0 iniconfig-2.3.1 openpyxl-3.1.5 pluggy-1.7.0 pygments-2.21.0 pytest-9.0.3
$ <python311> --version
Python 3.11.17
$ <python311> -c "import numpy, pandas, pytest, openpyxl; print(...)"
2.4.6 3.0.6 9.0.3 3.1.5
```

## L2 develop 최신화 · 브랜치 · 이슈 (2절) — pull 출력은 끝 40줄만

```
$ git status --porcelain (재확인)
 M .vscode/settings.json
 M README.md
 M docs/decisions.md
 M utils/README.md
?? .obsidian/
?? docs/dev/
?? "\354\247\204\355\226\211 \355\230\204\355\231\251 \353\260\217 \352\263\204\355\232\215 \354\240\225\353\246\254/"
$ ls -R docs/dev
docs/dev:
reports
tasks
식_함수_대응표.md
진행기록.md

docs/dev/reports:
F0-pre_report.md
F0_log.md
F0_report.md

docs/dev/tasks:
F0-pre_원격점검.md
F0_scaffold.md
# 2-1 B=/c/Users/money/bongsu_F0_backup_20261028
warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'utils/README.md', LF will be replaced by CRLF the next time Git touches it
$ wc -l "$B"/*
  238 /c/Users/money/bongsu_F0_backup_20261028/README.md
  224 /c/Users/money/bongsu_F0_backup_20261028/decisions.md
    0 /c/Users/money/bongsu_F0_backup_20261028/readme_local.diff
    8 /c/Users/money/bongsu_F0_backup_20261028/settings.json
   21 /c/Users/money/bongsu_F0_backup_20261028/utils_README.md
  491 total
$ git diff --stat HEAD -- README.md utils/README.md docs/decisions.md .vscode/settings.json
warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'docs/decisions.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'utils/README.md', LF will be replaced by CRLF the next time Git touches it
 .vscode/settings.json |   7 +-
 docs/decisions.md     | 223 +++++++++++++++++++++++++++++++++++++++++++++++++-
 2 files changed, 228 insertions(+), 2 deletions(-)
$ git config core.autocrlf
true
$ file (backup vs HEAD)
/c/Users/money/bongsu_F0_backup_20261028/README.md: Unicode text, UTF-8 text
/dev/stdin: Unicode text, UTF-8 text
# 2-2
$ git status --porcelain
?? .obsidian/
?? docs/dev/
?? "\354\247\204\355\226\211 \355\230\204\355\231\251 \353\260\217 \352\263\204\355\232\215 \354\240\225\353\246\254/"
 create mode 100644 "data/processed/D/D3_\354\243\274\354\232\224\352\265\255\353\263\204\352\265\220\354\227\255\353\271\204\354\244\221.csv"
 create mode 100644 "data/processed/E/E1_UN\355\221\234\352\262\260_\353\214\200\354\235\221\355\221\234.csv"
 create mode 100644 "data/processed/E/E1_UN\355\221\234\352\262\260_\354\202\254\352\261\264.csv"
 create mode 100644 "data/processed/E/E1_UN\355\221\234\352\262\260_\355\210\254\355\221\234.csv"
 create mode 100644 "data/processed/E/E3_\352\265\255\352\260\200\352\260\204\353\217\231\353\247\271\354\240\234\353\217\204\355\231\224.csv"
 create mode 100644 "data/processed/E/E3_\353\217\231\353\247\271\352\264\200\352\263\204.csv"
 create mode 100644 "data/processed/E/E3_\353\217\231\353\247\271\352\264\200\352\263\204_\354\227\260\352\262\260.csv"
 create mode 100644 "data/processed/E/E3_\353\217\231\353\247\271\354\234\240\354\202\254\353\217\204_\354\243\274\354\232\224\352\265\255.csv"
 create mode 100644 "data/processed/E/E5_\353\202\250\353\266\201\352\264\200\352\263\204\354\227\260\355\221\234_\354\240\225\354\240\234.csv"
 create mode 100644 "data/processed/F/F1_1\354\235\270\353\213\271\352\265\255\353\257\274\354\264\235\354\206\214\353\223\235_\354\240\225\354\240\234.csv"
 create mode 100644 "data/processed/F/F1_\352\265\255\353\257\274\354\264\235\354\206\214\353\223\235_\354\240\225\354\240\234.csv"
 create mode 100644 "data/processed/F/F1_\353\202\250\353\266\201\355\225\234\352\265\220\354\227\255\354\225\241_\354\240\225\354\240\234.csv"
 create mode 100644 "data/processed/F/F1_\353\213\250\353\260\261\354\247\210_\354\240\225\354\240\234.csv"
 create mode 100644 "data/processed/F/F1_\353\254\264\354\227\255\354\264\235\354\225\241_\354\240\225\354\240\234.csv"
 create mode 100644 "data/processed/F/F1_\353\254\264\354\227\255\354\264\235\354\225\241\354\246\235\352\260\220\353\245\240_\354\240\225\354\240\234.csv"
 create mode 100644 "data/processed/F/F1_\354\213\235\353\237\211\354\236\221\353\254\274\354\203\235\354\202\260\353\237\211_\354\240\225\354\240\234.csv"
 create mode 100644 "data/processed/F/F1_\354\213\235\353\237\211\354\236\221\353\254\274\354\203\235\354\202\260\353\237\211\354\246\235\352\260\220\353\245\240_\354\240\225\354\240\234.csv"
 create mode 100644 "data/processed/F/F1_\354\227\220\353\204\210\354\247\200_\354\240\225\354\240\234.csv"
 create mode 100644 "data/processed/F/F1_\354\235\270\352\265\254_\354\240\225\354\240\234.csv"
 create mode 100644 "data/processed/F/F1_\354\247\200\353\260\251\354\247\210_\354\240\225\354\240\234.csv"
 create mode 100644 "data/processed/F/F2_\354\227\260\353\217\204\353\263\204\355\232\214\353\213\264_\354\240\225\354\240\234.csv"
 create mode 100644 "data/processed/F/F4_\355\206\265\354\235\274\354\235\230\354\213\235\354\241\260\354\202\254_\354\234\204\355\230\221\353\254\270\355\225\255\354\247\221\352\263\204.csv"
 create mode 100644 "data/processed/F/F4_\355\206\265\354\235\274\354\235\230\354\213\235\354\241\260\354\202\254_\354\235\221\353\213\265\354\236\220_\354\240\225\354\240\234.csv"
 create mode 100644 data/processed/README.md
 create mode 100644 "data/processed/\352\263\265\355\206\265_\352\265\255\352\260\200\354\275\224\353\223\234.csv"
 create mode 100644 "data/processed/\352\263\265\355\206\265_\353\213\250\354\234\204.csv"
 create mode 100644 "data/processed/\352\263\265\355\206\265_\354\260\270\354\227\254\352\265\255.csv"
 create mode 100644 db/schema.sql
 create mode 100644 utils/build_db.py
 create mode 100644 utils/build_erd.py
 rename app.py => "\355\231\210.py" (100%)
$ git log --oneline -1
064c655 Merge pull request #13 from kjy700317-maker/docs/readme-db-files
# 2-4
$ git check-ignore -v .vscode/settings.json
.gitignore:253:.vscode/*	.vscode/settings.json
$ git status --porcelain
?? .obsidian/
?? docs/dev/
?? "\354\247\204\355\226\211 \355\230\204\355\231\251 \353\260\217 \352\263\204\355\232\215 \354\240\225\353\246\254/"
# 2-5 $ git switch -c feature/tension-scaffold
Switched to a new branch 'feature/tension-scaffold'
feature/tension-scaffold
# 2-6 $ gh issue create --title "[CHORE] 긴장도 코드화 뼈대(F0)" --label chore --body-file "$B/issue_F0.md"
https://github.com/kjy700317-maker/Team-Project/issues/14
```

## L4 결정 문서 사본 크기 대조 (4절) — | 원본 | 사본 | 원본 bytes | 사본 bytes | cmp |

```
| 긴장도_산출식_정리_v1_2026-10-27.md | 산출식_정리.md | 47540 | 47540 | 같음 |
| 인수인계_v0.1.3_통합세션_2026-10-27.md | 인수인계_v0.1.4.md | 16266 | 16266 | 같음 |
| 채점_v0_결과_2026-10-28.md | 채점_v0_결과.md | 15435 | 15435 | 같음 |
| 단계5_값확정_결정자료_2026-10-28.md | 단계5_값확정_결정자료.md | 48244 | 48244 | 같음 |
| 인계_단계5_to_통합세션_2026-10-28.md | 인계_단계5.md | 26204 | 26204 | 같음 |
| S1_하한_완화_결정자료_2026-10-27.md | S1_하한_완화_결정자료.md | 36456 | 36456 | 같음 |
| S2_사건점수_묶음_결정자료_2026-10-27.md | S2_사건점수_묶음_결정자료.md | 70108 | 70108 | 같음 |
| S3_척도_단계_표시_결정자료_2026-10-27.md | S3_척도_단계_표시_결정자료.md | 43959 | 43959 | 같음 |
| 감쇠_표시_단계유예_조사_2026-10-27.md | 감쇠_표시_단계유예_조사.md | 40301 | 40301 | 같음 |
```

## L5 .gitignore 확인 (5절)

```
$ git check-ignore -v "진행 현황 및 계획 정리/긴장도_산출식_정리_v1_2026-10-27.md"
.gitignore:258:진행 현황 및 계획 정리/	"\354\247\204\355\226\211 \355\230\204\355\231\251 \353\260\217 \352\263\204\355\232\215 \354\240\225\353\246\254/\352\270\264\354\236\245\353\217\204_\354\202\260\354\266\234\354\213\235_\354\240\225\353\246\254_v1_2026-10-27.md"
$ git check-ignore -v data/tension/events_기본.csv
.gitignore:260:data/tension/events_*.csv	"data/tension/events_\352\270\260\353\263\270.csv"
$ git check-ignore -v data/raw/processed || true
.gitignore:236:data/raw/*	data/raw/processed
$ git check-ignore data/tension/일별_기본.csv && echo ... || echo ...
정상: 결과 CSV는 추적 대상
```

## L6 requirements (6절)

```
$ file requirements.txt (변경 전)
requirements.txt: ASCII text, with CRLF line terminators
$ git diff requirements.txt
warning: in the working copy of 'requirements.txt', LF will be replaced by CRLF the next time Git touches it
diff --git a/requirements.txt b/requirements.txt
index 9c56e66..d5af16b 100644
--- a/requirements.txt
+++ b/requirements.txt
@@ -27,9 +27,11 @@ uvicorn==0.52.4
 watchdog==6.0.0
 websockets==16.1.1
 streamlit>=1.40.0
-pandas>=2.0.0
+pandas==3.0.6
 plotly>=5.0.0
 networkx>=3.1
 country-converter>=1.2.0
 google-cloud-bigquery>=3.10.0
-python-docx>=1.1.0
\ No newline at end of file
+python-docx>=1.1.0
+pytest==9.0.3
+openpyxl==3.1.5
$ file requirements.txt
requirements.txt: ASCII text
$ <python311> -m pip install -r requirements.txt --dry-run | tail -5
Requirement already satisfied: cffi>=2.0.0 in C:\Users\money\anaconda3\envs\python311\Lib\site-packages (from cryptography>=38.0.3->google-auth<3.0.0,>=2.14.1->google-auth[pyopenssl]<3.0.0,>=2.14.1->google-cloud-bigquery>=3.10.0->-r requirements.txt (line 34)) (2.1.1)
Requirement already satisfied: pycparser in C:\Users\money\anaconda3\envs\python311\Lib\site-packages (from cffi>=2.0.0->cryptography>=38.0.3->google-auth<3.0.0,>=2.14.1->google-auth[pyopenssl]<3.0.0,>=2.14.1->google-cloud-bigquery>=3.10.0->-r requirements.txt (line 34)) (3.0)
Requirement already satisfied: jsonschema-specifications>=2023.03.6 in C:\Users\money\anaconda3\envs\python311\Lib\site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<7,>=5.0.0->streamlit>=1.40.0->-r requirements.txt (line 29)) (2025.9.1)
Requirement already satisfied: pyasn1<0.7.0,>=0.6.1 in C:\Users\money\anaconda3\envs\python311\Lib\site-packages (from pyasn1-modules>=0.2.1->google-auth<3.0.0,>=2.14.1->google-auth[pyopenssl]<3.0.0,>=2.14.1->google-cloud-bigquery>=3.10.0->-r requirements.txt (line 34)) (0.6.4)
Would install lxml-6.1.3 python-docx-1.2.0
exit=0
```

## L8 decisions.md 합치기 (8절)

```
$ <python311> "$B/merge_decisions.py"
224 23 246
exit=0
$ git diff --stat docs/decisions.md
warning: in the working copy of 'docs/decisions.md', LF will be replaced by CRLF the next time Git touches it
 docs/decisions.md | 225 +++++++++++++++++++++++++++++++++++++++++++++++++++++-
 1 file changed, 224 insertions(+), 1 deletion(-)
```

## L9 커밋 (9절)

```
## commit 1
$ git diff --cached --stat
 .gitignore                                         |  10 +-
 CLAUDE.md                                          |  82 +++
 data/tension/.gitkeep                              |   0
 docs/dev/reports/.gitkeep                          |   0
 docs/dev/reports/F0-pre_report.md                  | 695 +++++++++++++++++++++
 ...233\220\352\262\251\354\240\220\352\262\200.md" |  68 ++
 docs/dev/tasks/F0_scaffold.md                      | 392 ++++++++++++
 ...10\230_\353\214\200\354\235\221\355\221\234.md" |  60 ++
 ...247\204\355\226\211\352\270\260\353\241\235.md" |  63 ++
 pytest.ini                                         |   4 +
 scripts/README.md                                  |   1 +
 tests/__init__.py                                  |   0
 tests/fixtures/.gitkeep                            |   0
 tests/test_smoke.py                                |  27 +
 utils/tension/__init__.py                          |  12 +
 15 files changed, 1413 insertions(+), 1 deletion(-)
71c5b36 chore: 긴장도 코드화 뼈대와 Claude Code 규칙 추가
## commit 2
$ git diff --cached --stat
 requirements.txt | 6 ++++--
 1 file changed, 4 insertions(+), 2 deletions(-)
2040539 chore: requirements 버전 고정·pytest·openpyxl 추가
## commit 3
$ git diff --cached --stat
 config.py | 50 ++++++++++++++++++++++++++++++++++++++++++++++++--
 1 file changed, 48 insertions(+), 2 deletions(-)
a442c1a chore: config.py에 긴장도 파라미터 추가
## commit 4
$ git diff --cached --stat
 ...262\260\354\240\225\354\236\220\353\243\214.md" | 393 +++++++++++++
 ...262\260\354\240\225\354\236\220\353\243\214.md" | 641 +++++++++++++++++++++
 ...262\260\354\240\225\354\236\220\353\243\214.md" | 391 +++++++++++++
 ...34\240\354\230\210_\354\241\260\354\202\254.md" | 457 +++++++++++++++
 ...262\260\354\240\225\354\236\220\353\243\214.md" | 429 ++++++++++++++
 ...66\234\354\213\235_\354\240\225\353\246\254.md" | 411 +++++++++++++
 ...5\270\352\263\204_\353\213\250\352\263\2045.md" | 210 +++++++
 ...\354\210\230\354\235\270\352\263\204_v0.1.4.md" | 161 ++++++
 ...204\354\240\220_v0_\352\262\260\352\263\274.md" | 153 +++++
 9 files changed, 3246 insertions(+)
6f32c3e docs: 긴장도 결정 문서 사본을 docs/tension에 추가
## commit 5
$ git diff --cached --stat
 docs/decisions.md | 225 +++++++++++++++++++++++++++++++++++++++++++++++++++++-
 1 file changed, 224 insertions(+), 1 deletion(-)
e4965be docs: ADR 갱신 반영(v0.1.4까지)
$ git -c core.quotepath=off diff --name-only develop..HEAD | grep -E "data/raw|진행 현황|\.env|\.json$" (금지 경로 재확인)
없음 — 금지 경로 0건
$ git -c core.quotepath=off diff --name-only develop..HEAD
.gitignore
CLAUDE.md
config.py
data/tension/.gitkeep
docs/decisions.md
docs/dev/reports/.gitkeep
docs/dev/reports/F0-pre_report.md
docs/dev/tasks/F0-pre_원격점검.md
docs/dev/tasks/F0_scaffold.md
docs/dev/식_함수_대응표.md
docs/dev/진행기록.md
docs/tension/S1_하한_완화_결정자료.md
docs/tension/S2_사건점수_묶음_결정자료.md
docs/tension/S3_척도_단계_표시_결정자료.md
docs/tension/감쇠_표시_단계유예_조사.md
docs/tension/단계5_값확정_결정자료.md
docs/tension/산출식_정리.md
docs/tension/인계_단계5.md
docs/tension/인수인계_v0.1.4.md
docs/tension/채점_v0_결과.md
pytest.ini
requirements.txt
scripts/README.md
tests/__init__.py
tests/fixtures/.gitkeep
tests/test_smoke.py
utils/tension/__init__.py
```

## L10 검산 (10절)

```
## 1
���� ���嵵 ��� ��Ű�� (v0.1.4 �̽�).
## 2
...                                                                      [100%]
## 3
(2010, 2019) (0.7, 0.9, 0.95, 0.98) ('A7-0098', 'A7-0100')
## 5
requirements.txt: ASCII text
## 8
e4965be docs: ADR 갱신 반영(v0.1.4까지)
6f32c3e docs: 긴장도 결정 문서 사본을 docs/tension에 추가
a442c1a chore: config.py에 긴장도 파라미터 추가
2040539 chore: requirements 버전 고정·pytest·openpyxl 추가
71c5b36 chore: 긴장도 코드화 뼈대와 Claude Code 규칙 추가
## 9
?? .obsidian/
?? docs/dev/reports/F0_log.md
?? docs/dev/reports/F0_report.md
## 10
# CLAUDE.md — 봉수(烽燧) Team-Project · Claude Code 작업 규칙
1
## 11
data/tension/.gitkeep
docs/dev/reports/.gitkeep
pytest.ini
scripts/README.md
tests/__init__.py
tests/fixtures/.gitkeep
## 13
.gitignore:253:.vscode/*	.vscode/settings.json
## extra: CLAUDE.md·부록 대조
CLAUDE.md = 부록 그대로
utils/tension/__init__.py = 부록 그대로
tests/test_smoke.py = 부록 그대로
pytest.ini = 부록 그대로
## 1 (PYTHONIOENCODING=utf-8 재출력)
봉수 긴장도 계산 패키지 (v0.1.4 이식).
## 2 (-rA 요약)
=================================== PASSES ====================================
=========================== short test summary info ===========================
PASSED tests/test_smoke.py::test_import_package
PASSED tests/test_smoke.py::test_config_values_match_adr
PASSED tests/test_smoke.py::test_half_life_definition
## extra: config.py 부록 E 대조
config.py 끝 45줄 = 부록 E 그대로
$ git diff develop..HEAD -- config.py | grep "^-"
--- a/config.py
-HALF_LIFE_DAYS = 14          # 위험도 계산 시 적용할 반감기 (일 단위)
-# 필요한 공통 상수가 있다면 이곳에 추가하세요.
```

## L11 동기화 · 푸시 · PR (11절)

```
$ git fetch origin
$ git merge origin/develop
Already up to date.
$ <python311> -m pytest -q
...                                                                      [100%]
$ git push -u origin feature/tension-scaffold
remote: 
remote: Create a pull request for 'feature/tension-scaffold' on GitHub by visiting:        
remote:      https://github.com/kjy700317-maker/Team-Project/pull/new/feature/tension-scaffold        
remote: 
To https://github.com/kjy700317-maker/Team-Project.git
 * [new branch]      feature/tension-scaffold -> feature/tension-scaffold
branch 'feature/tension-scaffold' set up to track 'origin/feature/tension-scaffold'.
$ gh pr create --draft --base develop --label chore --title "[CHORE] 긴장도 코드화 뼈대(F0)" --body-file "$B/pr_F0.md"
Warning: 3 uncommitted changes
https://github.com/kjy700317-maker/Team-Project/pull/15
```
