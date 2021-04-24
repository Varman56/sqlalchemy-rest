from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class DepartmnetForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    chief = IntegerField('Chief id', validators=[DataRequired()])
    members = StringField('Members')
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')
