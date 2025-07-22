import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import matplotlib.pyplot as plt
import platform
import altair as alt
from db.connector import DBconnector
from settings import DB_SETTINGS

# 한글 폰트 설정 함수
def setup_korean_font():
    """
    운영체제별 한글 폰트 설정을 적용하는 함수
    - macOS: AppleGothic
    - Windows: Malgun Gothic
    - Linux: DejaVu Sans
    - 마이너스 기호 깨짐 방지
    """
    font_mapping = {
        'Darwin': 'AppleGothic',
        'Windows': 'Malgun Gothic',
        'Linux': 'DejaVu Sans'
    }
    try:
        os_name = platform.system()
        plt.rcParams['font.family'] = font_mapping.get(os_name, 'DejaVu Sans')
        plt.rcParams['axes.unicode_minus'] = False
    except Exception as e:
        st.warning(f"한글 폰트 설정 실패: {e}")

# 데이터 전처리 함수
def preprocess_data(df):
    """
    데이터프레임 전처리: Null 처리 및 성별 표현 변환
    - Null 값을 'Unknown'으로 대체
    - 성별 M/F를 '남자'/'여자'로 변환
    """
    df = df.copy()  # 원본 데이터 보호
    for col in ['sex', 'blood', 'city', 'age_category']:
        df[col] = df[col].fillna('Unknown').astype(str)
    df['sex'] = df['sex'].replace({'M': '남자', 'F': '여자'})
    return df

# 그룹핑 데이터 생성 함수
def create_grouped_data(df):
    """
    성별, 혈액형, 도시, 나이대별 그룹핑 데이터 생성
    """
    return {
        'sex': df.groupby('sex').size().reset_index(name='count'),
        'blood': df.groupby('blood').size().reset_index(name='count'),
        'city': df.groupby('city').size().reset_index(name='count'),
        'age': df.groupby('age_category').size().reset_index(name='count'),
        'sex_blood': df.groupby(['sex', 'blood']).size().reset_index(name='count'),
        'sex_age': df.groupby(['sex', 'age_category']).size().reset_index(name='count'),
        'city_age': df.groupby(['city', 'age_category']).size().reset_index(name='count')
    }

# 통계 계산 함수
def calculate_stats(df, group_by_col, count_col, agg_cols):
    """
    그룹별 통계 계산
    - group_by_col: 그룹핑 기준 컬럼
    - count_col: 카운트 대상 컬럼
    - agg_cols: 집계 대상 컬럼 리스트
    """
    agg_dict = {count_col: 'count'}
    for col in agg_cols:
        agg_dict[col] = lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'N/A'
    stats = df.groupby(group_by_col).agg(agg_dict).rename(columns={
        count_col: '사용자 수',
        'blood': '최다 혈액형',
        'city': '최다 도시'
    })
    return stats

# 차트 생성 함수
def create_pie_chart(data, column, title, colors=None):
    """
    파이 차트 생성
    - data: 데이터프레임
    - column: 레이블로 사용할 컬럼
    - title: 차트 제목
    - colors: 색상 리스트 (선택)
    """
    fig, ax = plt.subplots()
    ax.pie(data['count'], labels=data[column].tolist(), colors=colors,
           autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.markdown(f"### {title}")
    st.pyplot(fig)

# 사이드바 설정 함수
def setup_sidebar(df, grouped_data):
    """
    사이드바에 필터 및 통계 정보 표시
    """
    st.sidebar.title("📊 대시보드 옵션")
    st.sidebar.metric("총 사용자 수", len(df))
    st.sidebar.markdown("#### 📈 주요 통계 요약")

    # 통계 표시
    metrics = [
        ('성별 종류', grouped_data['sex']['sex'].nunique()),
        ('최다 성별', f"{grouped_data['sex'].loc[grouped_data['sex']['count'].idxmax(), 'sex']} ({grouped_data['sex']['count'].max()})"),
        ('혈액형 종류', grouped_data['blood']['blood'].nunique()),
        ('최다 혈액형', f"{grouped_data['blood'].loc[grouped_data['blood']['count'].idxmax(), 'blood']} ({grouped_data['blood']['count'].max()})"),
        ('도시 수', grouped_data['city']['city'].nunique()),
        ('최다 도시', f"{grouped_data['city'].loc[grouped_data['city']['count'].idxmax(), 'city']} ({grouped_data['city']['count'].max()})"),
        ('나이대 수', grouped_data['age']['age_category'].nunique()),
        ('최다 나이대', f"{grouped_data['age'].loc[grouped_data['age']['count'].idxmax(), 'age_category']} ({grouped_data['age']['count'].max()})")
    ]
    for label, value in metrics:
        st.sidebar.metric(label, value)

    # 필터 옵션
    st.sidebar.markdown("#### 🔍 필터 옵션")
    selected_city = st.sidebar.multiselect("도시 선택", options=df['city'].unique(), default=df['city'].unique())
    selected_age = st.sidebar.multiselect("나이대 선택", options=df['age_category'].unique(), default=df['age_category'].unique())
    return selected_city, selected_age

# 메인 대시보드 함수
def main():
    """대시보드 메인 함수"""
    # 한글 폰트 설정
    setup_korean_font()

    # 실시간 리프레시
    st_autorefresh(interval=3000, key="dataframerefresh")

    # 데이터 로딩
    postgres_conn = DBconnector(**DB_SETTINGS['postgres_params']).sql_conn
    df = pd.read_sql_table(table_name='user_data_summary', con=postgres_conn)

    # 데이터 전처리
    df = preprocess_data(df)

    # 그룹핑 데이터 생성
    grouped_data = create_grouped_data(df)

    # 사이드바 설정
    selected_city, selected_age = setup_sidebar(df, grouped_data)

    # 필터링된 데이터
    filtered_df = df[df['city'].isin(selected_city) & df['age_category'].isin(selected_age)]

    # 타이틀 및 데이터 미리보기
    st.title("👤 사용자 요약 대시보드")
    st.markdown("데이터는 3초마다 자동 갱신됩니다.")
    if len(filtered_df) != len(df):
        st.info(f"🔍 필터링된 데이터: {len(filtered_df)}개 (전체: {len(df)}개)")
    st.subheader("📌 원본 데이터 미리보기")
    st.dataframe(filtered_df.head(50), use_container_width=True)
    
    # 1행: 성별 & 혈액형 분포
    col1, col2 = st.columns(2)
    with col1:
        colors = ['#1f77b4' if sex == '남자' else '#d62728' for sex in grouped_data['sex']['sex']]
        create_pie_chart(grouped_data['sex'], 'sex', "👨‍🦰 성별 분포", colors)
    with col2:
        create_pie_chart(grouped_data['blood'], 'blood', "🩸 혈액형 분포")

    # 2행: 도시 & 나이대 분포
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### 🏙️ 도시 분포")
        city_df = grouped_data['city'].sort_values(by='count', ascending=False)
        chart = alt.Chart(city_df).mark_bar().encode(
            x=alt.X('city:N', sort=list(city_df['city'])),
            y=alt.Y('count:Q'),
            color=alt.Color('city:N', legend=None)
        ).properties(width=350, height=300)
        st.altair_chart(chart, use_container_width=True)
    with col4:
        st.markdown("### 🎂 나이대 분포")
        # 나이대별 분포도 내림차순 정렬하여 시각화
        age_df = grouped_data['age'].sort_values(by='count', ascending=False)
        chart = alt.Chart(age_df).mark_bar().encode(
            x=alt.X('age_category:N', sort=list(age_df['age_category'])),
            y=alt.Y('count:Q'),
            color=alt.Color('age_category:N', legend=None)
        ).properties(width=350, height=300)
        st.altair_chart(chart, use_container_width=True)

    # 3행: 상세 통계 테이블
    st.markdown("### 📋 상세 통계 테이블")
    col5, col6 = st.columns(2)
    with col5:
        st.markdown("#### 성별 통계")
        sex_stats = calculate_stats(df, 'sex', 'age_category', ['blood', 'city'])
        st.dataframe(sex_stats, use_container_width=True)
    with col6:
        st.markdown("#### 나이대별 통계")
        age_stats = calculate_stats(df, 'age_category', 'sex', ['blood', 'city'])
        st.dataframe(age_stats, use_container_width=True)

if __name__ == "__main__":
    main()