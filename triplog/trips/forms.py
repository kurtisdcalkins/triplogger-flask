from wtforms import StringField, DateField, TextAreaField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class TripForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    trip_date = DateField('Date', validators=[DataRequired()])
    difficulty = StringField('Difficulty', validators=[DataRequired()])
    fun_rating = StringField('Fun Rating', validators=[DataRequired()])
    trip_group = TextAreaField('Group', validators=[DataRequired()])
    highlights = TextAreaField('Highights', validators=[DataRequired()])
    submit = SubmitField('Add Trip')
