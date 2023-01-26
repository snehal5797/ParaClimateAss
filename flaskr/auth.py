
from flask import (
    Blueprint, render_template, request,redirect, url_for
)

from flaskr.calculate_payout_new import payout

bp = Blueprint('auth', __name__, url_prefix='/auth')
import numpy as np


@bp.route('/register', methods=(['POST','GET']))
def register():
    
        if request.method == 'GET':
            return render_template('auth/register.html')
            

        power_price_strike = request.form['power_price_strike']
        mw_notional = request.form['mw_notional']
        
        calculator = payout(int(power_price_strike),int (mw_notional), ['2022-10-01', '2022-12-31'])
        raw_payouts, contingent_payouts = calculator.cal_raw_payout(), calculator.cal_cond_payout()
        labels1=np.array(raw_payouts.keys().tolist())
        values1=np.array(raw_payouts.values.tolist())       
        labels2=np.array(contingent_payouts.keys().tolist())
        values2=np.array(contingent_payouts.values.tolist())
        data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        return render_template('auth/bargraph.html',labels=labels1, values=values1,labels2=labels2, values2=values2,data=data)


# @bp.route('/')
# def index():
#     return redirect(url_for('auth.register'))