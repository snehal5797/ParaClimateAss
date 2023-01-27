import pandas as pd
from numpy import maximum

import os
from flask import (
    Blueprint, render_template,flash, request, redirect, render_template, request, url_for,jsonify
)

class payout:
    
    def __init__(self,power_price_strike, mw_notional, dates):
        self.MW_Notional=mw_notional
        self.Power_Price_Strike=power_price_strike
        self.Temperature=41
        
    
        self.merged_df= pd.read_csv('flaskr/FinalData.csv')
       
        
    #     try:
    #     data = request.get_json()
    #     filename = data['filename']
    #     if not os.path.isfile(filename):
    #         return jsonify(error=f"File Not Found: {filename}"),404
    #     else:
    #         # Perform file operation
    #         with open(filename, "w") as f:
    #             f.write(data["content"])
    #         return jsonify(success=True)
    # except Exception as e:
    #     return jsonify(error=str(e)), 500
        
        
            
        

    # def init_parse(self):
    #     SA_Price_df = pd.read_csv('SA_Price.csv')
    #     Para_TMAX_df = pd.read_excel('Parafield_TMAX.xlsx')
    #     SA_Price_df['date'] = pd.to_datetime(SA_Price_df['Dates']).dt.date
    #     Para_TMAX_df['date'] = pd.to_datetime(Para_TMAX_df['Date']).dt.date
    #     merged_df = pd.merge(SA_Price_df, Para_TMAX_df, on='date', how='outer')
    #     return merged_df
        
        
    def read_csv():
        try:              
            merged_df= pd.read_csv('flaskr/FinalData.csv')
            return merged_df
        except FileNotFoundError as e:
            return json.dumps({"error": f"File Not Found: {e}"}),404
        except pd.errors.ParserError as e:
            return json.dumps({"error": f"Invalid data format: {e}"}),400
        except Exception as e:
            return json.dumps({"error": str(e)}), 500

        
    
    def cal_raw_payout(self):
        self.merged_df["Final_price"] = self.MW_Notional * 1/12 * maximum(0, self.merged_df["Price"]-self.Power_Price_Strike)
        self.merged_df['Dates'] = pd.to_datetime(self.merged_df['Dates'], errors='coerce')
        raw_payout = self.merged_df[self.merged_df["Dates"].dt.quarter == 1]
        raw_payout["year"] = raw_payout["Dates"].dt.year
        # # Group the data by year and sum the payouts for each year
        raw_payout = raw_payout.groupby("year").sum()["Final_price"]
    
        return raw_payout
        
        
    def cal_cond_payout(self):
        cond_payount = self.merged_df[self.merged_df["Tmax"] > self.Temperature]
        # Add year column to the dataframe  
        cond_payount["year"] = cond_payount["Dates"].dt.year
        # Group the data by year and sum the price for each year
        yearly_sum = cond_payount.groupby("year").sum()["Final_price"]
        return yearly_sum


    '''
    Function to validate the parameters received: Source, destination, place, percent, min/max type
    '''
    def validate_params(source, destination, percent ,route_type):
        if len(source)!=2:
            return (True, "Source not correct.")

        if len(destination)!=2:
            return (True, "Destination not correct.")

        if percent<100 or percent>200:
            return (True, "Percent increase not between 100 and 200")
        
        if route_type not in ('min','max'):
            return (True, "Route type not between min or max")

        return (False, "No Error")
    
    
