from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class SendMessageForm(FlaskForm):
    text = StringField(validators=[DataRequired()])

    submit = SubmitField('Send')
