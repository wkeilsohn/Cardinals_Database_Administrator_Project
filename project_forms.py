# William Keilsohn
# March 14, 2026

# Import Packages
from flask_wtf import FlaskForm, Form
from wtforms.fields import form, StringField, SubmitField, TextAreaField # Not sure which ones I will need...
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired

# Define Form Classes

class raw_query_form(FlaskForm):
	query = TextAreaField('Write Your Query Here', validators=[DataRequired()])
	submit = SubmitField('Submit')