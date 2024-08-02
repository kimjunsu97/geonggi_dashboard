# 행정구역(읍면동)별/5세별 주민등록인구(2011년~)
import warnings
warnings.filterwarnings('ignore')
import json
from urllib.request import urlopen
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('api_key')
area_list = ['수원시','성남시','용인시','안양시','안산시','과천시','광명시','광주시','군포시','부천시','시흥시','김포시','안성시','오산시','의왕시','이천시','평택시','하남시','화성시','여주시','양평군'
             ,'고양시','구리시','남양주시','동두천시','양주시','의정부시','파주시','포천시','연천군','가평군']
#행정구역(읍면동)별/5세별 주민등록인구(2011년~)

#timId=T2+T3+T4 : 성별 전부
#objL2=ALL : 나이 전부
api_url = f'https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList\
\&apiKey={api_key}\
&itmId=T2+\
&objL1=00+11+41+41110+41130+41150+41170+41190+41210+41220+41250+41270+41280+41290+41310+41360+41370+41390+41410+41430+41450+41460+41480+41500+41550+41570+41590+41610+41630+41650+41670+41730+41800+41820+41830+\
&objL2=0\
&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=\
&format=json\
&jsonVD=Y\
&prdSe=M\
&newEstPrdCnt=12\
&orgId=101\
&tblId=DT_1B04005N'
with urlopen(api_url) as url:

    json_file = url.read()
    py_json = json.loads(json_file.decode('utf-8'))
    df = pd.DataFrame(py_json)
# PRD_DE : 날짜, ITM_NM : 성별, C1_NM : 지역, c2_NM :  연령, DT : 수
df = df[['PRD_DE','C1_NM','DT']]
df = df.rename(columns={'PRD_DE':'날짜',
                       'C1_NM':'지역',
                       'DT':'인구'})
#print(df)
#1 전국 평균 인구수
def make_country_population_data(date):
    condition1 = df['날짜']==date
    condition2 = df['지역'] =='전국' 
    data = df.loc[condition1&condition2,'인구'].values.astype(int)
    return data
#print(make_country_population_data('202406'))
#2 서울 평균 인구수
def make_seoul_population_data(date):
    condition1 = df['날짜']==date
    condition2 = df['지역'] =='서울특별시' 
    data = df.loc[condition1&condition2,'인구'].values.astype(int)
    return data
#print(make_seoul_population_data('202406'))
#3 경기 평균 인구수
def make_geonggi_population_data(date):
    condition1 = df['날짜']==date
    condition2 = df['지역'] =='경기도' 
    data = df.loc[condition1&condition2,'인구'].values.astype(int)
    return data
#print(make_geonggi_population_data('202406'))
#4 전국, 서울, 경기 비중 
def make_population_rate_data(date):
    seoul_data = make_seoul_population_data(date)
    geonggi_data = make_geonggi_population_data(date)
    etc_data = make_country_population_data(date) - seoul_data - geonggi_data
    
    tmp_df = pd.DataFrame({'서울' : seoul_data,
              '경기' : geonggi_data,
              'etc' : etc_data})
    
    rate_df = pd.melt(tmp_df, var_name='area',value_name='data')
    return rate_df
#print(make_population_rate_data('202406'))
#5 시군별 경기도 인구수(지도시각화)
def make_sigun_geo_data(date):
    condition1 = df['날짜']==date
    condition2 = df['지역'].isin(area_list) 
    tmp_df = df.loc[condition1&condition2,['지역','인구']].reset_index(drop=True)
 
    districts = {
        '수원시': ['수원시 장안구', '수원시 권선구', '수원시 팔달구', '수원시 영통구'],
        '성남시': ['성남시 수정구', '성남시 중원구', '성남시 분당구'],
        '안양시': ['안양시 만안구', '안양시 동안구'],
        '안산시': ['안산시 상록구', '안산시 단원구'],
        '고양시': ['고양시 덕양구', '고양시 일산동구', '고양시 일산서구'],
        '용인시': ['용인시 처인구', '용인시 기흥구', '용인시 수지구']
    }
    
    geo_data = {
        '지역': [],
        '인구': []
    }
    for index, row in tmp_df.iterrows():
        city = row['지역']
        dt = row['인구']
        
        if city in districts:
            district_list = districts[city]
            for district in district_list:
                geo_data['지역'].append(district)
                geo_data['인구'].append(dt)
        else:
            geo_data['지역'].append(city)
            geo_data['인구'].append(dt)

    geo_df = pd.DataFrame(geo_data)
    geo_df['인구'] = geo_df['인구'].astype(int)
    return geo_df
#print(make_sigun_geo_data('202406'))
def make_geonggi_geo_data():
    geo_path = './data/geojson_data.json'
    geo = json.load(open(geo_path, encoding='utf-8'))

    area_list = ['수원시','성남시','용인시','안양시','안산시','과천시','광명시','광주시','군포시','부천시','시흥시','김포시','안성시','오산시','의왕시','이천시','평택시','하남시','화성시','여주시','양평군'
                ,'고양시','구리시','남양주시','동두천시','양주시','의정부시','파주시','포천시','연천군','가평군']

    sigun_name = []
    geonggi_geo_df = dict()
    geonggi_geo_df['type'] = geo['type']
    geonggi_geo_df['bbox'] = geo['bbox']
    geonggi_geo_df['features'] = []
    for idx, sigun_dict in enumerate(geo['features']):
        #print(sigun_dict)
        #sigun_geo = sigun_dict['geometry']['coordinates'] #도형정보
        sigun_id = sigun_dict['properties']['SIG_KOR_NM'] #시군이름
        for area in area_list:
            if area in sigun_id:
                sigun_name.append(sigun_id)
                geonggi_geo_df['features'].append(sigun_dict)
    return geonggi_geo_df
#print(make_geonggi_geo_data())

#6 시군별 경기도 인구수(Top Rank)
def make_sigun_data(date):
    condition1 = df['날짜']==date
    condition2 = df['지역'].isin(area_list) 
    sigun_df = df.loc[condition1&condition2,['지역','인구']].reset_index(drop=True)
    return sigun_df
#print(make_sigun_data('202406'))
#7 전국, 서울, 경기 인구수
def make_Trend_data(date):
    #df['PRD_DE'] = pd.to_datetime(df['PRD_DE'])
    area = ['전국','서울특별시','경기도']
    condition1 = df['지역'].isin(area) 
    sigun_df = df.loc[condition1].reset_index(drop=True)
    #sigun_df = sigun_df.pivot_table(index='PRD_DE',columns='C1_NM',values='DT',aggfunc='first')
    sigun_df['날짜'] = pd.to_datetime(df['날짜'], format='%Y%m').dt.to_period('M').astype(str)

    return sigun_df
print(make_Trend_data('202406'))