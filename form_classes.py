# flask forms
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField #, PasswordField
from wtforms.validators import InputRequired #, Length, AnyOf
# from wtforms.fields.html5 import DateField

# https://wtforms.readthedocs.io/en/2.3.x/fields/#field-definitions

class WineScoreForm(FlaskForm):
    variety = SelectField(
        label='Variety',
        choices=[],
        validators=[]#InputRequired()] #,
                    # AnyOf(values=subst_avail_ids,
                    #      message='Must be a valid substance ID')
                    # ]
        )

    winery = StringField(
        label='Winery',
        validators=[] #InputRequired()]
        )

    country = SelectField(
        label='Country',
        validators=[ ] #InputRequired()]
        )

    province = StringField(
        label='Province',
        validators=[] # optional field
        )

    year = SelectField( # IntegerField(
        label='Year',
        choices=[],
        validators=[] #InputRequired()]
        )

    price = IntegerField(
        label='Price',
        validators=[] #InputRequired()]
        )

    description = StringField(
        label='Description',
        validators=[] # optional field
        )
