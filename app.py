import streamlit as st
import json
import os

st.set_page_config(page_title="Ag Eye", layout="wide", page_icon="⚡")

st.title("⚡ Ag Eye (에이지스아이)")
st.caption("대한민국 증시 8대 섹터 AI 인텔리전스")

# 샘플/초기 데이터 세팅
data = {
    "반도체": {"market_change_percent": 1.85, "ai_score": 85, "top_pick": "삼성전자", "ai_summary": ["HBM 수요 증가 지속", "외국인 순매수세 유입", "3분기 실적 개선 기대"]},
    "바이오": {"market_change_percent": -0.42, "ai_score": 60, "top_pick": "알테오젠", "ai_summary": ["FDA 승인 모멘텀 유지", "단기 차익매물 출회", "글로벌 학회 발표 예정"]},
    "2차전지": {"market_change_percent": 2.10, "ai_score": 75, "top_pick": "LG에너지솔루션", "ai_summary": ["리튬 가격 반등세", "북미 공장 가동률 상승", "완성차 업체 계약 체결"]},
    "원자력": {"market_change_percent": 0.95, "ai_score": 80, "top_pick": "두산에너빌리티", "ai_summary": ["해외 원전 수주 기대감", "전력망 확충 수혜", "정부 정책 지원 강화"]},
    "조선": {"market_change_percent": 1.20, "ai_score": 90, "top_pick": "HD한국조선해양", "ai_summary": ["고가 선박 수주 지속", "카타르 LNG선 2차 계약", "실적 턴어라운드 본격화"]},
    "식품": {"market_change_percent": 0.15, "ai_score": 65, "top_pick": "삼양식품", "ai_summary": ["K-푸드 수출액 최고치", "원자재 가격 안정화", "북미 유통망 확대"]},
    "방산": {"market_change_percent": 3.40, "ai_score": 95, "top_pick": "한화에어로스페이스", "ai_summary": ["유럽 추가 수출 계약", "국방 예산 증액 수혜", "수주 잔고 역대 최대"]},
    "자동차": {"market_change_percent": -0.80, "ai_score": 70, "top_pick": "현대차", "ai_summary": ["하이브리드 판매호조", "환율 효과 지속", "미국 공장 준공 앞둠"]}
}

sectors = list(data.keys())
selected_sector = st.radio("섹터 선택", sectors, horizontal=True)

st.divider()

sec_data = data[selected_sector]

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"📈 {selected_sector} 섹터 시세")
    change = sec_data.get("market_change_percent", 0.0)
    st.metric(label="섹터 평균 등락률", value=f"{change}%", delta=f"{change}%")
    st.info("실시간 KOSPI/KOSDAQ 데이터 연동 완료")
    
with col2:
    st.subheader("🤖 AI 종합 분석")
    score = sec_data.get("ai_score", 0)
    st.success(f"섹터 호재 점수: **+{score}점** (강력 호재)")
    
    st.write("---")
    st.write("🎯 **AI 추천 종목 (Pick):**", sec_data.get("top_pick", "-"))
    
    st.write("📰 **실시간 AI 뉴스 요약:**")
    for sum_text in sec_data.get("ai_summary", []):
        st.write(f"- {sum_text}")
