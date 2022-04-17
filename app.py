#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os

import json
from sportevents import SportEvents

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'loggedIn' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


session = {
    "profile": {
        "name": "Denis"
    },
    "loggedIn": "True",
    "events": SportEvents,
    "eventsJSON": json.dumps(SportEvents, default=vars)
}


@app.route('/')
def home():
    return redirect(url_for('calendar'))

@app.route('/calendar')
def calendar():
    return render_template('pages/home.html', session=session)

@app.route('/profile')
def profile():
    return render_template('pages/profile.html', session=session)

@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
'''
if __name__ == '__main__':
    app.run()
'''

# Or specify port manually:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5023))
    app.run(host='0.0.0.0', port=port)
