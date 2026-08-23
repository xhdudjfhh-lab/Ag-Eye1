import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Ag Eye", layout="wide", page_icon=None)

# ---------------------------------------------------------
# 스타일
# ---------------------------------------------------------
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}

    .block-container {
        padding-top: 2rem;
        max-width: 1100px;
    }

    .app-title {
        font-size: 2.1rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        color: #1a1a1a;
        margin-bottom: 0.1rem;
    }

    .app-caption {
        color: #8a8a8a;
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }

    /* 눈 아이콘 (컴패니언 큐브 스타일) */
    .eye-icon {
        width: 64px;
        height: 64px;
        margin: 0 auto 10px auto;
        border: 3px solid #c9c9c9;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #fafafa;
    }
    .eye-icon .ring {
        width: 26px;
        height: 26px;
        border-radius: 50%;
        border: 5px solid var(--ring-color);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .eye-icon .pupil {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--ring-color);
    }
    .eye-icon.active {
        border-color: var(--ring-color);
        background: #ffffff;
    }
    .eye-icon.disabled {
        opacity: 0.45;
    }

    .eye-label {
        text-align: center;
        font-weight: 600;
        font-size: 0.95rem;
        color: #333;
    }
    .eye-label.disabled {
        color: #aaaaaa;
    }
    .eye-sub {
        text-align: center;
        font-size: 0.75rem;
        color: #b0b0b0;
        margin-bottom: 1.5rem;
    }

    .section-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #999;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.4rem;
    }

    div[data-testid="stMetric"] {
        background: #fafafa;
        border: 1px solid #ececec;
        border-radius: 10px;
        padding: 1rem 1.2rem;
    }
</style>
""", unsafe_allow_html=True)


def render_eye(name: str, color: str, active: bool = False):
    state_class = "active" if active else "disabled"
    label_class = "" if active else "disabled"
    sub = "" if active else "Coming soon"
    st.markdown(f"""
        <div class="eye-icon {state_class}" style="--ring-color:{color};">
            <div class="ring"><div class="pupil"></div></div>
        </div>
        <div class="eye-label {label_class}">{name}</div>
        <div class="eye-sub">{sub}</div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# 제목
# ---------------------------------------------------------
st.markdown('<div class="app-title">Ag Eye</div>', unsafe_allow_html=True)
st.markdown('<div class="app-caption">대한민국 증시 8대 섹터 AI 인텔리전스</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 마켓 네비게이션 (Fe - Ag - Au)
# ---------------------------------------------------------
nav_left, nav_center, nav_right = st.columns([1, 1, 1])

with nav_left:
    render_eye("Fe Eye", "#5a5a5a", active=False)

with nav_center:
    render_eye("Ag Eye", "#8a8a8a", active=True)

with nav_right:
    render_eye("Au Eye", "#c9a13b", active=False)

st.divider()

# ---------------------------------------------------------
# 섹터 데이터
# ---------------------------------------------------------
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


@st.cache_data(ttl=300)
def get_stock_info(ticker: str):
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


selected_sector = st.radio("섹터 선택", sectors, horizontal=True, label_visibility="collapsed")

st.write("")

sec_data = data[selected_sector]
stock_info = get_stock_info(sec_data["ticker"])

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f'<div class="section-label">{selected_sector} 섹터 시세</div>', unsafe_allow_html=True)

    if stock_info is not None:
        change = stock_info["change_percent"]
        st.metric(
            label=f"{sec_data['top_pick']} ({sec_data['ticker']})",
            value=f"{stock_info['price']:,}원",
            delta=f"{change}%",
        )
    else:
        st.warning("실시간 데이터를 불러오지 못했습니다. 잠시 후 다시 시도해주세요.")

with col2:
    st.markdown('<div class="section-label">AI 종합 분석</div>', unsafe_allow_html=True)
    score = sec_data.get("ai_score", 0)
    st.success(f"섹터 호재 점수 **+{score}점**")

    st.write("")
    st.markdown(f"**AI 추천 종목**  \n{sec_data.get('top_pick', '-')}")

    st.write("")
    st.markdown("**AI 뉴스 요약**")
    for sum_text in sec_data.get("ai_summary", []):
        st.write(f"- {sum_text}")

st.caption("데이터 출처: Yahoo Finance (yfinance) · 5분 캐싱 적용")
