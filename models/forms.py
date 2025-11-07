from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Email



#Class for the login form
class LoginForm(FlaskForm):
    email= StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Login')




#class for the signup form
class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=6, max=50)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('confrim password', validators=[DataRequired(), EqualTo(password)])
    submit = SubmitField('Register')


#class to create and store users in the database





