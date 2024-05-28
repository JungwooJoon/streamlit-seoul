import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

from predict import home_predict, area_predict

def home():
    st.marker("### Visualization \n"
              "- 가구당 평균 가격 추이 \n"
              "- 가구당 거래 건수 추세 \n"
              "- 지역별 평균 가격 막대 그래프 \n")

def run_estate_home(total_data):
    st.markdown("## 탐색적 자료 분석 개요 \n"
    "탐색적 자료 분석 페이지입니다."
    "여기에 추가하고 싶은 내용을 추가하면 됩니다")
    
    selected = option_menu(None, ['Home', 'Map'],
                          icons=['house', 'map'],
                          menu_icon='cast', default_index=0, orientation='horizontal',
                          styles={
                              'container' : {
                                  'padding' : '0',
                                  'backgroung-color' : '#808080'
                              },
                              'icon' : {
                                  'color' : 'orange',
                                  'font-size' : '25px'
                              },
                              'nav-link':{
                                  'font-size' : '15px',
                                  'text-align' : 'left',
                                  'margin' : '0px',
                                  '--hover-color' : '#eee'
                              },
                              'nav-link-selected' : {
                                  'background-color' : 'skyblue',
                                  'color' : 'white'
                              }
                          })
    if selected == 'Home' :
        home_predict(total_data)
    elif selected == 'Map' :
        area_predict(total_data)
    else:
        st.warning('오류')