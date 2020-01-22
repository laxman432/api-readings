from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    company_name = StringField('Company name', validators=[DataRequired()])
    email = StringField('Contact email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class AddingClients(FlaskForm):
    name = StringField('Contact person', validators=[DataRequired()])
    company = StringField('Company name', validators=[DataRequired()])
    email = StringField('Contact email', validators=[DataRequired(), Email()])
    invoice = StringField('Amount to be issued', validators=[DataRequired()])
    service_desc = StringField('What is the bill for(service description):', validators=[DataRequired()])
    submit = SubmitField('ADD')
