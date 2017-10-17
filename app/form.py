#@
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired
#@
class EventSearch(FlaskForm):
	event_name = StringField('event_name', validators=[DataRequired()])
	curr_location = StringField('curr_location', validators=[DataRequired()])
	city = SelectField('city', choices=[('ha-noi', 'Hà Nội'),('hai-phong', 'Hải Phòng')])