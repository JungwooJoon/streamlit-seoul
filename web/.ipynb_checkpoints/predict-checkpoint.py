import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from prophet import Prophet
import numpy as np
import matplotlib.font_manager as fm

def home_predict(total_df):
    path = 'C:\Windows\Fonts\H2MJRE.TTF'
    fontprop = fm.FontProperties(fname=path, size=12)
    
    total_df['DEAL_YMD'] = pd.to_datetime(total_df['DEAL_YMD'], format='%Y-%m-%d')
    types = list(total_df['HOUSE_TYPE'].unique())
    periods = 28
    
    fig, ax = plt.subplots(figsize=(10, 6), sharex=True, ncols=2, nrows=2)
    for i in range(0, len(types)):
        model = Prophet()
    
        total_df2 = total_df.loc[total_df['HOUSE_TYPE'] == types[i], ['DEAL_YMD', 'OBJ_AMT']]
        
        summary_df = total_df2.groupby('DEAL_YMD')['OBJ_AMT'].agg('mean').reset_index()
        summary_df = summary_df.rename(columns = {'DEAL_YMD' : 'ds', 'OBJ_AMT' : 'y'})
    
        model.fit(summary_df)
    
        future1 = model.make_future_dataframe(periods=periods)
    
        forcast1 = model.predict(future1)
        x = i // 2
        y = i % 2
    
        fig = model.plot(forcast1, uncertainty=True, ax=ax[x, y])
        ax[x, y].set_title(f'서울시 {types[i]} 평균 가격 예측 시나리어 {periods}일간', fontproperties=fontprop)
        ax[x, y].set_xlabel(f'날짜', fontproperties=fontprop)
        ax[x, y].set_ylabel(f'평균가격(만원)', fontproperties=fontprop)
        
        for tick in ax[x, y].get_xticklabels():
            tick.set_rotation(30)
    st.pyplot(fig)
    
def area_predict(total_df):
    path = 'C:\Windows\Fonts\H2MJRE.TTF'
    fontprop = fm.FontProperties(fname=path, size=12)
    
    total_df['DEAL_YMD'] = pd.to_datetime(total_df['DEAL_YMD'], format='%Y-%m-%d')
    
    total_df = total_df[total_df['HOUSE_TYPE'] == '아파트']
    
    sgg_nms = list(total_df['SGG_NM'].unique())
    print(sgg_nms)
    
    sgg_nms = [x for x in sgg_nms if x is not np.nan]
    print(sgg_nms)
    
    periods = 28
    
    fig, ax = plt.subplots(figsize=(20, 10), sharex=True, ncols=5, nrows=5)
    
    loop = 0
    for sgg_nm in sgg_nms:
        model = Prophet()
    
        total_df2 = total_df.loc[total_df['SGG_NM'] == sgg_nm, ['DEAL_YMD', 'OBJ_AMT']]
        
        summary_df = total_df2.groupby('DEAL_YMD')['OBJ_AMT'].agg('mean').reset_index()
        summary_df = summary_df.rename(columns = {'DEAL_YMD' : 'ds', 'OBJ_AMT' : 'y'})
    
        print(sgg_nm)
        
        model.fit(summary_df)
    
        future = model.make_future_dataframe(periods=periods)
    
        forcast = model.predict(future)
        x = loop // 5
        y = loop % 5
        loop = loop + 1
    
        fig = model.plot(forcast, uncertainty=True, ax=ax[x, y])
        ax[x, y].set_title(f'서울시 {sgg_nm} 평균 가격 예측 시나리어 {periods}일간', fontproperties=fontprop)
        ax[x, y].set_xlabel(f'날짜', fontproperties=fontprop)
        ax[x, y].set_ylabel(f'평균가격(만원)', fontproperties=fontprop)
        for tick in ax[x, y].get_xticklabels():
            tick.set_rotation(30)
            
    st.pyplot(fig)