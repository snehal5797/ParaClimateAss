from flask import (
    Blueprint, redirect, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    return redirect(url_for('auth.register'))


