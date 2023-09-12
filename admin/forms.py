#import wtform class
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField
from wtforms.validators import InputRequired, Length

#define form
class AdminLoginForm(Form):
	username = StringField(
		label='Admin Username', 
		validators=[InputRequired(),
		Length(min=4, max=20)]
		)
	password = PasswordField(
		label='Password', 
		validators=[InputRequired()]
		)
	submit = SubmitField("Login")