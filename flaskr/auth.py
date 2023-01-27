
from flask import (
    Blueprint, render_template,flash, request, redirect, render_template, request, url_for,jsonify
)
# from werkzeug.exceptions import FileNotFoundError
from flaskr.calculate_payout_new import payout

bp = Blueprint('auth', __name__)
import numpy as np
import os

flag = False




@bp.route('/')
def index():
    return redirect(url_for('auth.register'))


@bp.route('/register', methods=(['POST','GET']))
def register():
    
        if request.method == 'GET':
            return render_template('auth/register.html')
        
        global flag
        if request.method == "POST":
            if flag:
                return "API call is in progress. Please wait."
            else:
                #API handling!
                flag = True
                # API call code here
                error = None
                power_price_strike = request.form['power_price_strike']
                mw_notional = request.form['mw_notional']

                if not power_price_strike:
                    error = 'power_price_strike is required.'
                elif not mw_notional:
                    error = 'mw_notional is required.'
                elif not os.path.isfile('flaskr/FinalData.csv'):
                    
                    error= 'flaskr/FinalData.csv not present'
                else:
                    error=None
                    
                if error is None:
                    try:
                        calculator = payout(int(power_price_strike),int (mw_notional), ['2022-10-01', '2022-12-31'])
                        raw_payouts, contingent_payouts = calculator.cal_raw_payout(), calculator.cal_cond_payout()
                        labels1=np.array(raw_payouts.keys().tolist())
                        values1=np.array(raw_payouts.values.tolist())       
                        labels2=np.array(contingent_payouts.keys().tolist())
                        values2=np.array(contingent_payouts.values.tolist())      
                        flag = False 
                        return render_template('auth/bargraph.html',labels=labels1, values=values1,labels2=labels2, values2=values2,rows1=len(labels1),rows2=len(labels2))                      
                        
                    except Exception as e:
                        print("Hello with error")
                        error = "Please insert the FinalData.csv in flakr directory"              
                        flag = False 
                        return render_template('auth/error.html', message= e), 404
                return render_template('auth/error.html', message= error), 404    

            
            
