from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField
)
from wtforms.validators import DataRequired, Length


class BookAddingForm(FlaskForm):
    Title = StringField('Title', validators=[DataRequired("Please enter title name")])

    Author = StringField('Author', validators=[DataRequired("Please enter author name")])

    PublishedDate = IntegerField('Published date', validators=[DataRequired("Please enter published date")])

    ISBN = StringField('ISBN', validators=[DataRequired("Please enter industry identifiers")])

    PageCount = StringField('Page Count', validators=[DataRequired("Please enter page count")])

    Url_thumbnail = StringField('Link to thumbnail of book', validators=[DataRequired("Please enter page count")])

    Language = StringField('Language (enter two letter symbol of language)', validators=[DataRequired("Please enter language of the book"), Length(max=2, min=2, message=('You must enter 2 letters'))])

