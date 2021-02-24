"""
runs Wine Predictor website
"""

# IMPORTS
# import packages to create and load environment variables
# from dotenv import load_dotenv
import os

# to manage the website
from flask import (Flask,
                   url_for,
                   redirect,
                   render_template,
                   request
                   #, g, session
                   )

# form classes
from form_classes import (WineScoreForm)


# flask bootstrap
from flask_bootstrap import Bootstrap

# to manage current date
from time_functions import current_date_str, current_datetime_str, current_time_str

# to read from api
from api import read_api, read_api_fx

# import markdown rendering
from flaskext.markdown import Markdown

import joblib
import pandas as pd
FEATURE = joblib.load('model/feature_eng.joblib')
MODEL = joblib.load('model/model.joblib')
# APP CONFIG
# https://flask.palletsprojects.com/en/1.1.x/config/
app = Flask(__name__)

# load_dotenv() # any code after this will be able to use environment variables


# Debug - if in this mode, change lines below + end of code
app.config['DEBUG'] = True
app.config['FLASK_ENV'] = 'development'

app.config['SECRET_KEY'] = 'shoppingdemos'

# regarding forms csrf tokens
# enable/disable CSRF token
app.config['WTF_CSRF_ENABLED'] = True
# update CSFR secret key; default is SECRET_KEY
app.config['WTF_CSRF_SECRET_KEY'] = 'this_is_SPARTAAAAA'
# change csrf time limit in sec (1 hour/3600sec by default)
app.config['WTF_CSRF_TIME_LIMIT'] = 3600

"""
about SECRET_KEY:
what's inside the cookie is still public. but without the SECRET_KEY,
others won't be able to modify the cookie and send it back to the server
"""

# Markdown
Markdown(app)

# Bootstrap
bootstrap = Bootstrap(app)



# METHODS
def home_init():
    """
    initializes all the variable assignment required for the home page
    this is called later to avoid having the code pasted in all page functions
    """

    # FORMS
    ws_form = WineScoreForm()
    ws_form.year.choices = list(range(1970, 2021 +1, 1))
    ws_form.country.choices = ['london', 'Argentina', 'Armenia', 'Australia',
                               'Austria', 'Bosnia and Herzegovina', 'Brazil',
                               'Bulgaria', 'Canada', 'Chile', 'China',
                               'Croatia', 'Cyprus', 'Czech Republic', 'Egypt',
                               'England', 'France', 'Georgia', 'Germany',
                               'Greece', 'Hungary', 'India', 'Israel', 'Italy',
                               'Lebanon', 'Luxembourg', 'Macedonia', 'Mexico',
                               'Moldova', 'Morocco', 'New Zealand', 'Peru',
                               'Portugal', 'Romania', 'Serbia', 'Slovakia',
                               'Slovenia', 'South Africa', 'Spain',
                               'Switzerland', 'Turkey', 'Ukraine', 'Uruguay',
                               'US']
    ws_form.price_currency.choices = read_api_fx()[1]
    fx_rates_values_dict = read_api_fx()[0]
    fx_rates_list = read_api_fx()[1]


    # import ipdb; ipdb.set_trace()
    return (ws_form,
            ws_form.year.choices,
            ws_form.country.choices,
            ws_form.price_currency.choices,
            fx_rates_values_dict,
            fx_rates_list)


# ROUTES
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    redirects to the home page
    """
    return redirect(url_for('home')) # , name=name, location=location


@app.route('/home', methods=['GET', 'POST'])
def home():

    """
    returns home template with initialized variables
    """
    (ws_form,
            ws_form.year.choices,
            ws_form.country.choices,
            ws_form.price_currency.choices,
            fx_rates_values_dict,
            fx_rates_list) = home_init()

    return render_template('home.html',
                            **locals() # returns all local variables
                           )

@app.route('/submitwine', methods=['POST', 'GET'])
def submitwine():
    """
    returns home template with initialized variables after submitwine
    """
    (ws_form,
            ws_form.year.choices,
            ws_form.country.choices,
            ws_form.price_currency.choices,
            fx_rates_values_dict,
            fx_rates_list) = home_init()

    # VARIABLES
    # si_date_str = current_date_str()
    input_variety = str(ws_form.variety.data)
    input_winery = str(ws_form.winery.data)
    input_country = str(ws_form.country.data)
    input_province = str(ws_form.province.data)
    input_year = str(ws_form.year.data)
    input_price = round(float(ws_form.price.data),2)
    input_price_currency = str(ws_form.price_currency.data)
    currency_fx = float(fx_rates_values_dict[input_price_currency])
    price_usd = round(input_price/currency_fx, 2)
    input_description = str(ws_form.description.data)
    region = "Other"
    title = f"{input_winery} {input_year} {input_variety} ({input_province})"
    df = pd.DataFrame(
            dict(country=[input_country],
                description=[input_description],
                price=[price_usd],
                province=[input_province],
                region_1=[region],
                title=[title],
                variety=[input_variety],
                winery=[input_winery]
                ))
    feat_eng_x = FEATURE.transform(df)
    prediction = MODEL.predict(feat_eng_x)[0]
    if ws_form.validate_on_submit():
        # validation of fields

        # get score 
        # api_results = read_api(place=input_country)
        api_results_2 = prediction
        api_stars = '⭐' * api_results_2

        # display score
        display_added_record = True # shows success message

        return render_template('home.html', **locals())
        # works but resends POST request/form at page refresh:
        # render_template('home.html', **locals())
        # works but doesn't display success message:
        # redirect(url_for('home'))


    return render_template('home.html', **locals())
    # **locals returns all local variables

# @app.route('/howto', methods=['GET'])
# def projects():
#     projects_content = ""
#     with open("markdown/how-to-use.md", "r") as f:
#         howto_content = f.read()

#     return render_template('markdown.html',
#                            mkd_text=howto_content,
#                            n_cols=1,
#                            page_title="How to Use This Website")


if __name__ == '__main__':
    """
    runs only if the app is ran on the terminal
    initializes the website
    """
    # app.run()
    app.run(debug=True)

    """
    about debug=True:
    - restarts the app every time you make changes to the file
    - it might not work in latest versions, but use it if it does
    - if there's a code error, it will crash and you'll need to restart it
    - it also shows you the debug/error pages when there are errors
    - turn it off once app goes live
    """
