import pandas as pd
import streamlit as st

# 1. 데이터 로드 함수 예시
def load_sample_data():
    """
    프로젝트에서 공통으로 사용할 데이터를 불러오는 함수입니다.
    data/ 폴더에 CSV 파일이 있다면 경로를 맞춰서 사용하세요.
    """
    try:
        # 임시 데이터프레임 생성 (테스트용)
        data = {
            "이름": ["김철수", "이영희", "박민수"],
            "점수": [85, 92, 78],
            "합격여부": ["합격", "합격", "불합격"]
        }
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"데이터를 불러오는 중 에러가 발생했습니다: {e}")
        return None

# 2. 데이터 전처리 함수 예시
def preprocess_data(df):
    """
    불러온 데이터에 전처리(결측치 처리, 컬럼 가공 등)를 수행하는 함수입니다.
    """
    if df is not None:
        # 예시: 점수가 80점 이상인 사람만 필터링하는 전처리
        filtered_df = df[df["점수"] >= 80]
        return filtered_df
    return None

# 3. 공통 메시지 출력 함수 예시
def show_footer():
    """
    앱 하단에 공통으로 들어갈 푸터(꼬리말)를 출력하는 함수입니다.
    """
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: gray;'>© 2026 Team-Project. All rights reserved.</p>", unsafe_allow_html=True)