from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('home', __name__, url_prefix='/home')

@bp.route('/')
@login_required
def home():
    return render_template('Home/homePage.html')