"""갓생 데이터 — 백만장자 습관, 진짜일까?

실행:  streamlit run app.py
"""
import streamlit as st

st.set_page_config(page_title="부자 습관 팩트체크",layout="wide",
                   initial_sidebar_state="collapsed")

# 메뉴는 Streamlit 기본 메뉴를 숨기고, common.header()가 그리는 상단 헤더에 둔다 (DESIGN.md 4장)
page = st.navigation(
    [
        st.Page("views/home.py", title="부자 습관 이야기", url_path="home", default=True),
        st.Page("views/record.py", title="기록 한 걸음", url_path="record"),
    ],
    position="hidden",
)
page.run()
