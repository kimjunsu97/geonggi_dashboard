import streamlit as st
import pandas as pd
import plotly.express as px
from make_graph import *
selected_date='202406'
selected_option='인구'
st.set_page_config(
    page_title="경기도 대시보드",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")# First row

# # 차트 함수들 임포트하기
# from map_preprocessing import make_geomap
# # 예시
# data = pd.DataFrame({
#   '날짜':[202306, 202307, 202308, 202309, 202310, 202311, 202312, 202401, 202402, 202403, 202404, 202405, 202406],
#   '전국': [3,4,5,6,7,8,9,10,11,12,13,14,15],
#   '서울': [4,5,6,7,8,9,10,11,12,13,14,15,16],
#   '경기': [5,6,7,8,9,10,11,12,13,14,15,16,17] 
# })
# fig = px.bar(data, y=['전국','서울','경기'])

# Define the layout
st.title("경기도 통계표")
option = '인구'
col1, col2, col3, col4 = st.columns([1, 1, 3, 2])
with col1:
    with st.container(height=200):
        st.markdown("#### 전국")
        make_country_population_graph(selected_date, selected_option)
    
    with st.container(height=200):
        st.markdown("#### 서울")
        make_seoul_population_graph(selected_date, selected_option)


with col2:
    with st.container(height=200):
        st.markdown("#### 경기")
        make_geonggi_population_graph(selected_date, selected_option)


    with st.container(height=200):
        #st.markdown("#### 서울, 경기 비중")
        make_population_rate_graph(selected_date, selected_option)



with col3:
    with st.container(height=415):

        st.markdown("#### 지도 시각화")
        make_sigun_geo_graph(selected_date, selected_option)

with col4:
    with st.container(height=415):
        st.markdown(f"#### 시군별 경기도 {option}수")
        make_sigun_graph(selected_date, selected_option)


# Second row
col5, col6, = st.columns([2, 5])
with col5:
    with st.container(height=400):
        st.write("옵션 :\n년도, 월")
        year_list = [2024,2023,2022,2021,2020]
        option_list = ['인구']
        selected_year = st.selectbox('Select a year', year_list)
        selected_option = st.selectbox('Select a option', option_list)

with col6:
    with st.container(height=400):
        st.markdown(f"### 전국, 서울, 경기 {option} 추세")
        #st.plotly_chart(fig, theme="streamlit",use_container_width=True)
        make_trend_graph(selected_date, selected_option)


