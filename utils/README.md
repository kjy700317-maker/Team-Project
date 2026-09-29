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