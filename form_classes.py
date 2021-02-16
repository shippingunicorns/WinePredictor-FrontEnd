# flask forms
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField #, PasswordField
from wtforms.validators import InputRequired #, Length, AnyOf
# from wtforms.fields.html5 import DateField

class WineScoreForm(FlaskForm):
    wine_type = SelectField(
        label='Wine Type',
        choices=[],
        validators=[InputRequired()] #,
                    # AnyOf(values=subst_avail_ids,
                    #      message='Must be a valid substance ID')
                    # ]
                        )
    year = IntegerField(
        label='Year',
        validators=[InputRequired()]
        )
    # record_date = DateField('Date (optional)',
    #     format='%Y-%m-%d',
    #     validators=[Optional()])
