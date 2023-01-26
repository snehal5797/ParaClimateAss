import pandas as pd
from numpy import maximum

        

def init_parse():
    SA_Price_df = pd.read_csv('flaskr/SA_Price.csv')
    Para_TMAX_df = pd.read_excel('flaskr/Parafield_TMAX.xlsx')
    SA_Price_df['date'] = pd.to_datetime(SA_Price_df['Dates']).dt.date
    Para_TMAX_df['date'] = pd.to_datetime(Para_TMAX_df['Date']).dt.date
    merged_df = pd.merge(SA_Price_df, Para_TMAX_df, on='date', how='outer')
    merged_df['Dates'] = pd.to_datetime(merged_df['Dates'], errors='coerce')
    with open('FinalData.csv', 'w') as file:
        merged_df.to_csv(file, index=False)
    print("completeeee!!!")
    
    return merged_df
        
        
   