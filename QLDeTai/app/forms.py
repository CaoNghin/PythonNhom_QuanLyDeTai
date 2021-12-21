from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


from app import db

from app.models import user
from app.models import lop_hoc
from app.models import chitiet

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')
class RegisterForm(FlaskForm):
    r_username = StringField('Username',validators=[DataRequired()])
    r_password = PasswordField('Password',validators=[DataRequired()])
    r_passwordrepeat = PasswordField('Passwordrepeat',validators=[DataRequired()])
    r_email = StringField('Email',validators=[DataRequired()])
    submit = SubmitField('Register')

class ThemMoiForm(FlaskForm):
    TenLop = StringField('dientenlophoc', validators=[DataRequired()])
  
    ds = user.query.all()
        # Kiem tra password

    # for sv in ds:
    #     print(sv.id)
    #     ten =BooleanField(sv.id, validators=[DataRequired()])
    submit = SubmitField('thêm mới')