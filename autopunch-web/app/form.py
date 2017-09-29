from flask_wtf import Form
from wtforms import TextField, BooleanField,PasswordField
from wtforms.validators import Required
 
class LoginForm(Form):
    account = TextField('account', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)
