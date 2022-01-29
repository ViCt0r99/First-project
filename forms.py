from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    DateField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField
)
from wtforms.validators import URL, DataRequired, Email, EqualTo, Length
import email_validator
from datetime import datetime


class BookAddingForm(FlaskForm):
    Title = StringField('Title', [DataRequired()])

    Author = StringField('Author', [DataRequired()])

    PublishedDate = DateField('Published Date', format='%Y-%m-%d')

    ISBN = StringField('ISBN', [DataRequired(), Length(min=13, message=('You must enter 13 digits.'))])

    Page_count = StringField('Page Count', [DataRequired()])

    #url_thumbnail

    Language = StringField('Language (enter two letter symbol of language)', [DataRequired(), Length(max=2, message=('You must enter 2 letters'))])



    submit = SubmitField('Add')