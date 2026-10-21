import streamlit as st
st.title("한반도 군사 긴장 지수")
st.write("이곳에 긴장도 지수 대시보드가 들어갈 예정입니다")

import config # 맨 위 폴더의 config.py를 불러온다. streamlit은  app.py가 있는 폴더를 기준으로 파일을 찾아서, pages 안에서도 이렇게 불러 올 수 있다.
st.write("더미 데이터 사용중:", config.USE_DUMMY) # config.USE_DUMMY : config 파일 안의 USE_DUMMY 값을 꺼내 온다 "파일이름.변수이름"형태 / st.write에 쉽표로 여러개를 넣으면 이어서 보여준다.

from utils.dummy import make_daily # utils 폴더 → dummy.py 파일 → make_daily 함수를 꺼내옴 , 맨아레
st.dataframe(make_daily()) # 표를 화면에 보여줌