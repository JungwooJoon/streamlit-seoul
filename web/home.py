import pandas as pd
import streamlit as st
from millify import prettify

def run_home(total_df) :
    st.markdown("## 대시보드 개요 \n"
    "본 프로젝트는 서울시 부동산 실거래가를 알려주는 대시보드 입니다."
    "여기에 추가하고 싶은 내용을 추가하면 됩니다")
    total_df['DEAL_YMD'] = pd.to_datetime(total_df['DEAL_YMD'], format="%Y-%m-%d")
    
    total_df['month'] = total_df['DEAL_YMD'].dt.month
    total_df['year'] = total_df['DEAL_YMD'].dt.year
    total_df = total_df.loc[total_df['HOUSE_TYPE'] == '아파트', :]


    sgg_nm = st.sidebar.selectbox("자치구", sorted(total_df['SGG_NM'].unique()))
    acc_year = st.sidebar.selectbox("년도", [2023, 2024])
    
    month_dic = {'1월' : 1, '2월' : 2, '3월' : 3, '4월' : 4, '5월' : 5, '6월' : 6, '7월' : 7, '8월' : 8, '9월' : 9, '10월' : 10, '11월' : 11, '12월' : 12}
    
    selected_month = st.sidebar.radio("확인하고 싶은 월을 선택하시오 ", list(month_dic.keys()))
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader(f'{sgg_nm} {acc_year}년 {selected_month} 아파트 가격 개요')
    st.markdown('자치구와 월을 클릭하면 자동으로 각 지역구에서 거래된 **최소가격**, **최대가격**을 확인할 수 있습니다')
    
    col1, col2 = st.columns(2)
    
    filtered_month = total_df[total_df['month'] == month_dic[selected_month]]
    filtered_month = filtered_month[filtered_month['year'] == acc_year]
    filtered_month = filtered_month[filtered_month['SGG_NM'] == sgg_nm]
    march_min_price = filtered_month['OBJ_AMT'].min()
    march_max_price = filtered_month['OBJ_AMT'].max()

    new_df = filtered_month[['SGG_NM', 'BJDONG_NM', 'BLDG_NM', 'BLDG_AREA', 'OBJ_AMT']]

    st.markdown('### 아파트 가격 상위 3위')
    st.dataframe(new_df.sort_values(by='OBJ_AMT',ascending=False).head(3))

    st.markdown('### 아파트 가격 하위 3위')
    st.dataframe(new_df.sort_values(by='OBJ_AMT',ascending=True).head(3))

    
    with col1:
        st.metric(label = f'{sgg_nm} 최소가격(만원)', value = prettify(march_min_price))
    with col2:
        st.metric(label = f'{sgg_nm} 최대가격(만원)', value = prettify(march_max_price))