import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
#from flaskr.calculate_payout import payout
from flaskr.calculate_payout_new import payout

from flaskr.parse_data import init_parse
bp = Blueprint('auth', __name__, url_prefix='/auth')
import numpy as np


# @bp.route('/register', methods=('GET', 'POST'))
# def register():
#     print("register function")
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         db = get_db()
#         error = None

#         if not username:
#             error = 'Username is required.'
#         elif not password:
#             error = 'Password is required.'

#         if error is None:
#             try:
#                 db.execute(
#                     "INSERT INTO user (username, password) VALUES (?, ?)",
#                     (username, generate_password_hash(password)),
#                 )
#                 db.commit()
#             except db.IntegrityError:
#                 error = f"User {username} is already registered."
#             else:
#                 return redirect(url_for("auth.login"))

#         flash(error)

#     return render_template('auth/register.html')


@bp.route('/register', methods=(['POST','GET']))
def register():
    
        if request.method == 'GET':
            return render_template('auth/register.html')
            

        power_price_strike = request.form['power_price_strike']
        mw_notional = request.form['mw_notional']
        print(power_price_strike)
        print(mw_notional)
        calculator = payout(int(power_price_strike),int (mw_notional), ['2022-10-01', '2022-12-31'])
        raw_payouts, contingent_payouts = calculator.cal_raw_payout(), calculator.cal_cond_payout()

        print(raw_payouts)
        print(contingent_payouts)
        labels=np.array(raw_payouts.keys().tolist())
        values=np.array(raw_payouts.values.tolist())
        
        # labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
        # values = [10, 20, 30, 40, 50]

        # return render_template('auth/bargraph.html',labels=labels, values=values)
        # labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
        # values = [10, 20, 30, 40, 50]
        data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        # return render_template('auth/bargraph.html', data=data)

        return render_template('auth/bargraph.html',labels=labels, values=values,data=data)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
