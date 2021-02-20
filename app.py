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
from api import read_api

# import markdown rendering
from flaskext.markdown import Markdown

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
    ws_form.variety.choices = ["Type A", "Type B"]
    ws_form.year.choices = list(range(1970, 2021 +1, 1))
    ws_form.country.choices = ["london", "US"]

    # import ipdb; ipdb.set_trace()
    return (ws_form,
            ws_form.variety.choices,
            ws_form.year.choices,
            ws_form.country.choices)


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
            ws_form.variety.choices,
            ws_form.year.choices,
            ws_form.country.choices) = home_init()

    return render_template('home.html',
                            **locals() # returns all local variables
                           )

@app.route('/submitwine', methods=['POST', 'GET'])
def submitwine():
    """
    returns home template with initialized variables after submitwine
    """
    (ws_form,
            ws_form.variety.choices,
            ws_form.year.choices,
            ws_form.country.choices) = home_init()

    # VARIABLES
    # si_date_str = current_date_str()
    input_variety = str(ws_form.variety.data)
    input_winery = str(ws_form.winery.data)
    input_country = str(ws_form.country.data)
    input_province = str(ws_form.province.data)
    input_year = str(ws_form.year.data)
    input_price = str(ws_form.price.data)
    input_description = str(ws_form.description.data)

    if ws_form.validate_on_submit():
        # validation of fields

        # get score
        api_results = read_api(place=input_country)

        # display score
        display_added_record = True # shows success message

        return render_template('home.html', **locals())
        # works but resends POST request/form at page refresh:
        # render_template('home.html', **locals())
        # works but doesn't display success message:
        # redirect(url_for('home'))


    return render_template('home.html', **locals())
    # **locals returns all local variables

@app.route('/howto', methods=['GET'])
def projects():
    projects_content = ""
    with open("markdown/how-to-use.md", "r") as f:
        howto_content = f.read()

    return render_template('markdown.html',
                           mkd_text=howto_content,
                           n_cols=1,
                           page_title="How to Use This Website")


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
