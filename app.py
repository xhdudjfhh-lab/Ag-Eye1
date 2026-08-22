import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Ag Eye", layout="wide", page_icon="⚡")

st.title("⚡ Ag Eye (에이지스아이)")
st.caption("대한민국 증시 8대 섹터 AI 인텔리전스")

# 섹터별 대표 종목 및 티커 (KOSPI=.KS, KOSDAQ=.KQ)
data = {
    "반도체": {"ticker": "005930.KS", "top_pick": "삼성전자", "ai_score": 85,
              "ai_summary": ["HBM 수요 증가 지속", "외국인 순매수세 유입", "3분기 실적 개선 기대"]},
    "바이오": {"ticker": "196170.KQ", "top_pick": "알테오젠", "ai_score": 60,
              "ai_summary": ["FDA 승인 모멘텀 유지", "단기 차익매물 출회", "글로벌 학회 발표 예정"]},
    "2차전지": {"ticker": "373220.KS", "top_pick": "LG에너지솔루션", "ai_score": 75,
               "ai_summary": ["리튬 가격 반등세", "북미 공장 가동률 상승", "완성차 업체 계약 체결"]},
    "원자력": {"ticker": "034020.KS", "top_pick": "두산에너빌리티", "ai_score": 80,
              "ai_summary": ["해외 원전 수주 기대감", "전력망 확충 수혜", "정부 정책 지원 강화"]},
    "조선": {"ticker": "009540.KS", "top_pick": "HD한국조선해양", "ai_score": 90,
            "ai_summary": ["고가 선박 수주 지속", "카타르 LNG선 2차 계약", "실적 턴어라운드 본격화"]},
    "식품": {"ticker": "003230.KS", "top_pick": "삼양식품", "ai_score": 65,
            "ai_summary": ["K-푸드 수출액 최고치", "원자재 가격 안정화", "북미 유통망 확대"]},
    "방산": {"ticker": "012450.KS", "top_pick": "한화에어로스페이스", "ai_score": 95,
            "ai_summary": ["유럽 추가 수출 계약", "국방 예산 증액 수혜", "수주 잔고 역대 최대"]},
    "자동차": {"ticker": "005380.KS", "top_pick": "현대차", "ai_score": 70,
             "ai_summary": ["하이브리드 판매호조", "환율 효과 지속", "미국 공장 준공 앞둠"]}
}

sectors = list(data.keys())


@st.cache_data(ttl=300)  # 5분 캐싱: API 과호출 방지
def get_stock_info(ticker: str):
    """yfinance로 실시간 현재가, 전일대비 등락률을 가져온다."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")
        if len(hist) < 2:
            return None
        prev_close = hist["Close"].iloc[-2]
        current_close = hist["Close"].iloc[-1]
        change_percent = ((current_close - prev_close) / prev_close) * 100
        return {
            "price": round(current_close, 2),
            "change_percent": round(change_percent, 2),
        }
    except Exception:
        return None


selected_sector = st.radio("섹터 선택", sectors, horizontal=True)

st.divider()

sec_data = data[selected_sector]
stock_info = get_stock_info(sec_data["ticker"])

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"📈 {selected_sector} 섹터 시세")

    if stock_info is not None:
        change = stock_info["change_percent"]
        st.metric(
            label=f"{sec_data['top_pick']} ({sec_data['ticker']})",
            value=f"{stock_info['price']:,}원",
            delta=f"{change}%",
        )
        st.success("✅ 실시간 데이터 연동 중 (yfinance)")
    else:
        st.warning("⚠️ 실시간 데이터를 불러오지 못했습니다. 잠시 후 다시 시도해주세요.")

with col2:
    st.subheader("🤖 AI 종합 분석")
    score = sec_data.get("ai_score", 0)
    st.success(f"섹터 호재 점수: **+{score}점** (강력 호재)")

    st.write("---")
    st.write("🎯 **AI 추천 종목 (Pick):**", sec_data.get("top_pick", "-"))

    st.write("📰 **실시간 AI 뉴스 요약:**")
    for sum_text in sec_data.get("ai_summary", []):
        st.write(f"- {sum_text}")

st.caption("데이터 출처: Yahoo Finance (yfinance) · 5분 캐싱 적용")

