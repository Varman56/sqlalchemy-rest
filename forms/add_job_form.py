from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class AddJob(FlaskForm):
    team_leader = IntegerField('Team leader id', validators=[DataRequired()])
    job = StringField('Title', validators=[DataRequired()])
    work_size = IntegerField('Work size (hours)')
    collaborators = StringField('Collaborators')
    is_finished = BooleanField('Is job finished?', default=False)
    submit = SubmitField('Submit')
