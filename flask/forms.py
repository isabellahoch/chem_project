from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, Form, SelectField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import Email, Length, InputRequired, EqualTo, Regexp, URL
from wtforms.widgets import TextArea

class RegForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=50)], render_kw={'class': 'form-control'})
    email = StringField('Email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)], render_kw={'class': 'form-control'})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=25)], render_kw={'class': 'form-control'})
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=4, max=25), EqualTo('password', message='Passwords must match.')], render_kw={'class': 'form-control'})
    submit = SubmitField('Submit', render_kw={'class': 'form-control btn btn-incub8','style':'width:100%'})
    role = 'investor'

class LoginForm(FlaskForm):
    email = StringField('Email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)], render_kw={'class': 'form-control'})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=25)], render_kw={'class': 'form-control'})
    submit = SubmitField('Submit', render_kw={'class': 'form-control btn btn-incub8','style':'width:100%'})


class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=50)], render_kw={'class': 'form-control'})      
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)], render_kw={'class': 'form-control'})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=25), EqualTo('confirmpassword', message='Passwords must match')], render_kw={'class': 'form-control'})
    submit = SubmitField('Submit', render_kw={'class': 'form-control btn btn-incub8','style':'width:100%'})

class ContactForm(FlaskForm):
  name = StringField("name", render_kw={'class': 'form-control'})
  email = StringField("_replyto", render_kw={'class': 'form-control'})
  subject = StringField("Subject", render_kw={'class': 'form-control'})
  message = TextAreaField("Message", render_kw={'class': 'form-control'})
  submit = SubmitField("Send", render_kw={'class': 'btn btn-incub8','style':'width:100%'})