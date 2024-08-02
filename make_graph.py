from make_data import *
import streamlit as st
import plotly.express as px
#1 전국 평균 인구수
def make_country_population_graph(date, option):
    country_population_data = make_country_population_data(date)
    value = str(int(country_population_data/10000))+"만 "+str(int((country_population_data%10000)/1000+0.5))+"천명"
    st.metric(label=f'평균 {option}수', value=value, delta=0)
    
#2 서울 평균 인구수
def make_seoul_population_graph(date, option):
    seoul_population_data = make_seoul_population_data(date)
    value = str(int(seoul_population_data/10000))+"만 "+str(int((seoul_population_data%10000)/1000+0.5))+"천명"

    st.metric(label=f'평균 {option}수', value=value, delta=0)

#3 경기 평균 인구수
def make_geonggi_population_graph(date, option):
    geonggi_population_data = make_geonggi_population_data(date)
    value = str(int(geonggi_population_data/10000))+"만 "+str(int((geonggi_population_data%10000)/1000+0.5))+"천명"
    st.metric(label=f'평균 {option}수', value=value, delta=0)

#4 전국, 서울, 경기 비중 
def make_population_rate_graph(date, option):
    population_rate_data = make_population_rate_data(date)
    fig = px.pie(population_rate_data, values='data', names='area', width=200, height=180, hole=.4)
    fig.update_traces(textposition='inside')
    fig.update_layout(legend=dict(
    orientation='h',
    yanchor="bottom",
    y=-0.3,
    xanchor="left",
    x=0.01),
    margin=dict(t=0,b=0,l=0,r=0),
)

    st.plotly_chart(fig, use_container_width=True, theme="streamlit")

#5 시군별 경기도 인구수(지도시각화)
def make_sigun_geo_graph(date, option):
    sigun_geo_data = make_sigun_geo_data(date)
    geonggi_geo_data = make_geonggi_geo_data()
    fig = px.choropleth(data_frame=sigun_geo_data, featureidkey="properties.SIG_KOR_NM",locations='지역', geojson=geonggi_geo_data, color='인구', color_continuous_scale=["white","blue"])
    
    fig.update_geos(
        visible=False, 
        fitbounds="locations",
        showcountries=False,
        showsubunits=False
    )
    fig.update_layout(
        autosize=False,
        margin = dict(
                l=0, r=0, b=0, t=0, pad=4, autoexpand=True
            ),
        width=150, height=300
    )
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))

    st.plotly_chart(fig, theme="streamlit",use_container_width=True)
    
#6 시군별 경기도 인구수(Top Rank)
def make_sigun_graph(date, option):
    sigun_data = make_sigun_data(date)
    st.dataframe(sigun_data,
                 column_order=("지역", "인구"),
                 hide_index=True,
                 width=None,
                 height=300,
                 column_config={
                    "지역": st.column_config.TextColumn(
                        "지역",
                    ),
                    '인구': st.column_config.ProgressColumn(
                        '인구',
                        format="%f",
                        min_value=0,
                        max_value=max(df['인구']),
                        width=360
                     )}
                 )
#7 전국, 서울, 경기 인구수
def make_trend_graph(date, option):
    trend_data = make_Trend_data(date)
    fig = px.bar(trend_data, x='날짜', y='인구', color='지역',barmode='group')
    fig.update_layout(
        width=600, height=300,
        legend=dict(orientation='h',
                    yanchor="bottom", y=-0.7,
                    xanchor="left", x = 0.3
    ))
    

    st.plotly_chart(fig, theme="streamlit",use_container_width=True)