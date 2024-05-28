import pandas as pd

def load_data():
    data = pd.read_csv('web/seoul_estate.csv')
    return data
