from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import NumberRange


class UserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    age = IntegerField('Age',
        validators=[NumberRange(min=0, max=200,
            message='Must a valid age in years (up to 200)')
        ]
    )
    submit = SubmitField('Enter')
