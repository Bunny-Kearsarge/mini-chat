from wtforms import IntegerField, StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    login = StringField(validators=[DataRequired()])
    password = StringField(validators=[DataRequired()])
    username = StringField(validators=[DataRequired()])

    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    login = StringField(validators=[DataRequired()])
    password = StringField(validators=[DataRequired()])

    submit = SubmitField('Login')
