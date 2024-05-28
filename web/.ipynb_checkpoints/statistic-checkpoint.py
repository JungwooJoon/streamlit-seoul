import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
from pingouin import ttest
import matplotlib.pyplot as plt
import seaborn as sns

def twoMeans(total_df, sgg_nm):

    st.markdown('### 서울시 2월, 3월 아파트 평균 가격 차이 검증')
    
    total_df['month'] = total_df['DEAL_YMD'].dt.month
    apt_df = total_df[(total_df['HOUSE_TYPE'] == '아파트') & (total_df['month'].isin([2, 3]))]
    
    dec_df = apt_df[apt_df['month'] == 2]
    nov_df = apt_df[apt_df['month'] == 3]
    
    st.markdown(f"2월 아파트 평균 가격(만원) : {round(dec_df['OBJ_AMT'].mean(),3)} , 3월 아파트 평균 가격(만원) : {round(nov_df['OBJ_AMT'].mean(),3)} ")
    result = ttest(dec_df['OBJ_AMT'], nov_df['OBJ_AMT'], paired=False)

    st.dataframe(result,use_container_width=True)

    if result['p-val'].values[0] > 0.05:
        st.markdown('p-val 값이 0.05보다 크므로 평균 가격 차이는 없다.')
    else:
        st.markdown('p-val 값이 0.05보다 작으므로 평균 가격 차이는 있다.')


    st.markdown(f'### 서울시 {sgg_nm} 2월, 3월 아파트 평균 가격 검증')

    total_df['month'] = total_df['DEAL_YMD'].dt.month
    apt_df = total_df[(total_df['HOUSE_TYPE'] == '아파트') & (total_df['month'].isin([2, 3]))]

    sgg_df = apt_df[apt_df['SGG_NM'] == sgg_nm ]
    sgg_dec_df = sgg_df[sgg_df['month'] == 2]
    sgg_nov_df = sgg_df[sgg_df['month'] == 3]
    
    st.markdown(f"{sgg_nm} 2월 아파트 평균 가격(만원) : {sgg_dec_df['OBJ_AMT'].mean()}, {sgg_nm} 3월 아파트 평균 가격(만원) : {sgg_nov_df['OBJ_AMT'].mean()}")
    
    sgg_result = ttest(sgg_dec_df['OBJ_AMT'], sgg_nov_df['OBJ_AMT'], paired=False)

    st.dataframe(sgg_result,use_container_width=True)

    if sgg_result['p-val'].values[0] > 0.05:
        st.markdown('p-val 값이 0.05보다 크므로 평균 가격 차이는 없다.')
    else:
        st.markdown('p-val 값이 0.05보다 작으므로 평균 가격 차이는 있다.')

    st.markdown(f'### 서울시 {sgg_nm} 2월, 3월 아파트 거래 건수 검증')
    mean_df = sgg_df.groupby('DEAL_YMD')['OBJ_AMT'].agg(['mean', 'size'])
    
    mean_df = mean_df.reset_index()
    mean_df['month'] = mean_df['DEAL_YMD'].dt.month
    
    mean_dec_df = mean_df[mean_df['month'] == 2]
    mean_nov_df = mean_df[mean_df['month'] == 3]
    
    st.markdown(f"{sgg_nm} 2월 아파트 거래 건수(건) : {mean_dec_df['size'].mean()}, {sgg_nm} 3월 아파트 거래 건수(건) : {mean_nov_df['size'].mean()}")
    
    sgg_result = ttest(mean_dec_df['size'], mean_nov_df['size'], paired=False)
    
    st.dataframe(sgg_result,use_container_width=True)

    if sgg_result['p-val'].values[0] > 0.05:
        st.markdown('p-val 값이 0.05보다 크므로 평균 가격 차이는 없다.')
    else:
        st.markdown('p-val 값이 0.05보다 작으므로 평균 가격 차이는 있다.')

def corrRealtion(total_df, sgg_nm) :
    st.markdown(f'### 서울시 {sgg_nm} 2월, 3월 아파트 평균 가격 검증')

    total_df['month'] = total_df['DEAL_YMD'].dt.month
    apt_df = total_df[(total_df['HOUSE_TYPE'] == '아파트') & (total_df['month'].isin([2, 3]))]

    sgg_df = apt_df[apt_df['SGG_NM'] == sgg_nm ]
    sgg_dec_df = sgg_df[sgg_df['month'] == 2]
    sgg_nov_df = sgg_df[sgg_df['month'] == 3]
    
    st.markdown(f"{sgg_nm} 2월 아파트 평균 가격(만원) : {sgg_dec_df['OBJ_AMT'].mean()}, {sgg_nm} 3월 아파트 평균 가격(만원) : {sgg_nov_df['OBJ_AMT'].mean()}")
    
    sgg_result = ttest(sgg_dec_df['OBJ_AMT'], sgg_nov_df['OBJ_AMT'], paired=False)

        
    st.dataframe(sgg_result,use_container_width=True)

    if sgg_result['p-val'].values[0] > 0.05:
        st.markdown('p-val 값이 0.05보다 크므로 평균 가격 차이는 없다.')
    else:
        st.markdown('p-val 값이 0.05보다 작으므로 평균 가격 차이는 있다.')

    corr_df = sgg_df[['DEAL_YMD', 'OBJ_AMT', 'BLDG_AREA', 'SGG_NM', 'month']].reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='BLDG_AREA', y='OBJ_AMT', data=corr_df, ax=ax)
    st.pyplot(fig)




def showStat(total_df) :
    total_df['DEAL_YMD'] = pd.to_datetime(total_df['DEAL_YMD'], format='%Y-%m-%d')
    
    analisys_nm = st.sidebar.selectbox('분석매뉴', ['두 집단간 차이 검정', '상관분석'])
    sgg_nm = st.sidebar.selectbox('자치구명', total_df['SGG_NM'].unique())
    
    if analisys_nm == '두 집단간 차이 검정' :
        twoMeans(total_df, sgg_nm)
    elif analisys_nm == '상관분석' :
        corrRealtion(total_df, sgg_nm)
    else :
        st.warning("Error")
