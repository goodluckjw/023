import streamlit as st
from processing.law_processor import process_laws

st.title("📘 부칙 개정 도우미 (전자동002)")

search_word = st.text_input("🔍 찾을 단어", placeholder="예: 지방법원")

if st.button("🚀 시작하기"):
    if not search_word:
        st.warning("찾을 단어를 입력해주세요.")
    else:
        with st.spinner("법령 검색 중..."):
            result_text = process_laws(search_word)
            st.success("📄 결과가 생성되었습니다.")
            st.download_button("📥 결과 텍스트 다운로드", result_text, file_name="개정안_결과.txt")
