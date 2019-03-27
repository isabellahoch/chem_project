from flask import Flask, render_template, request, redirect, url_for, make_response, abort
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, Form, SelectField, SubmitField, BooleanField
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms.validators import Email, Length, InputRequired, EqualTo, Regexp, URL
from wtforms.widgets import TextArea
from werkzeug.security import generate_password_hash, check_password_hash
from db_connect import MONGODB_URI, db
from math import ceil
from forms import ContactForm, LoginForm, ContactForm
from credentials import mlab_host, mlab_api_key, google_api_key, google_client_id, google_client_secret, gmail_password, google_app_password, sendgrid_password, cloudinary_api_key, cloudinary_api_secret
from webclasses import WebStartup, WebInvestor, pushStartup, updateStartup, pushInvestor, updateInvestor, parse_multi_form, WebUser
# from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_mail import Mail, Message
# from flask_oauth import OAuth
# from oauth_flask import OAuth

import urllib
import time

try:
	from urllib import urlopen
except:
	from urllib.request import urlopen

# heroku push fails with first one; internal development server only works with first one and doesn't work with #2.

import pymongo
import functools
from pymongo import MongoClient
import io; io.StringIO()
import random
import string
import os
import csv
import re
import json
import datetime as dt
from datetime import datetime, timedelta

app = Flask(__name__)

# app.config['MONGODB_SETTINGS'] = {
#     'db': 'incub8sf',
#     'host': db_uri,
#     'username': 'incub8sf',
#     'password': 'willw0ntwin'
# }

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USERNAME'] = 'incub8sf@gmail.com'
app.config['MAIL_PASSWORD'] = gmail_password
pw_option = google_app_password
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False


def reset_email_settings():
	app.config['MAIL_SERVER'] = 'smtp.gmail.com'
	app.config['MAIL_USERNAME'] = 'incub8sf@gmail.com'
	app.config['MAIL_PASSWORD'] = gmail_password
	app.config['MAIL_PORT'] = '465'
	app.config['MAIL_USE_SSL'] = True
	app.config['MAIL_USE_TLS'] = False	

mail = Mail(app)
# # administrator list
ADMINS = ['incub8sf@gmail.com']
default_sender = "INCUB8 <incub8sf@gmail.com>"

def send_email(subject, sender, recipients, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    mail.send(msg)

def welcome_email(email, role):
	role = role.lower()
	if role == "startup":
		user = WebStartup(email).get_info()
		try:
			send_email("Thanks for joining INCUB8!",
               default_sender, [email],
               render_template("welcome_email.html", 
                               user=user))
		except:
			try:
				app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
				app.config['MAIL_USERNAME'] = 'apikey'
				app.config['MAIL_PASSWORD'] = sendgrid_password
				app.config['MAIL_PORT'] = '587'
				app.config['MAIL_USE_SSL'] = False
				app.config['MAIL_USE_TLS'] = True
				send_email("Thanks for joining INCUB8!",
               default_sender, [email],
               render_template("welcome_email.html", 
                               user=user))
				reset_email_settings()
			except:
				print('noooo')
			return(redirect(url_for('dashboard')))
	elif role == "investor":
		user = WebInvestor(email).get_info()
		try:
			send_email("Thanks for joining INCUB8!",
               default_sender, [email],
               render_template("investor_welcome_email.html", 
                               user=user))
		except:
			try:
				app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
				app.config['MAIL_USERNAME'] = 'apikey'
				app.config['MAIL_PASSWORD'] = sendgrid_password
				app.config['MAIL_PORT'] = '587'
				app.config['MAIL_USE_SSL'] = False
				app.config['MAIL_USE_TLS'] = True
				send_email("Thanks for joining INCUB8!",
               default_sender, [email],
               render_template("welcome_email.html", 
                               user=user))
				reset_email_settings()
			except:
				print('noooo')
			return redirect(url_for('dashboard'))

contact_sender = default_sender
contact_receiver = ["INCUB8 <incub8sf@gmail.com>"]
contact_sender = "INCUB8 <incub8sf@gmail.com>"

def contact_us(subject, name, email, message):
	info = {}
	info["subject"] = subject
	info["name"] = name
	info["email"] = email
	info["message"] = message
	info['timestamp'] = datetime.now()
	if get_user_role(email) == 'startup':
		user = WebStartup(email).get_info()
		user["profile"] = url_for('get_startup', startup_id = user["id"])
	elif get_user_role(email) == 'investor':
		user = WebStartup(email).get_info()
		user["profile"] = url_for('get_investor', investor_id = user["id"])
	else:
		user = {"name":name, "email":email}
	try:
		send_email("Contact Form Submission",
           contact_sender, contact_receiver,
           render_template("contact_email.html", info=info, 
                           user=user))
	except:
		try:
			app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
			app.config['MAIL_USERNAME'] = 'apikey'
			app.config['MAIL_PASSWORD'] = sendgrid_password
			app.config['MAIL_PORT'] = '587'
			app.config['MAIL_USE_SSL'] = False
			app.config['MAIL_USE_TLS'] = True
			send_email("Contact Form Submission",
           contact_sender, contact_receiver,
           render_template("contact_email.html", info=info, 
                           user=user))
			reset_email_settings()
		except:
			print('noooo')
			# send_email("Contact Form Submission",
   #         contact_sender, contact_receiver,
   #         render_template("contact_email.html", info=info, 
   #                         user=user))
			return False

def test_mail():
	welcome_email("incub8sf@gmail.com", "startup")

app.config['MONGODB_SETTINGS'] = {
	'db': 'incub8sf',
	'host': mlab_host
}

app.config['SECRET_KEY'] = "\xe2!\xfb\xbb+h\xbe\xf1\x97\x1b:\x92\x19I\x13\x19\x1fzz\xbc\x18_:"
secret_key_encoded = "8280d1960d36d9ea65a14f5fb864fe0b3e829ba940e64c84"
# secondary_key = "e221fbbb2b68bef1971b3a92194913191f7a7abc185f3a"

dbapp = MongoEngine(app)

# app.config['SECRET_KEY'] = 'SECRET_KEY'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, dbapp.Document):
    meta = {'collection': 'Users'}
    email = dbapp.StringField()
    password = dbapp.StringField()
    name = dbapp.StringField()
    role = dbapp.StringField()

@login_manager.user_loader
def load_user(user_id):
	return User.objects(pk=user_id).first()

def admin_required(view):
    @functools.wraps(view)
    def inner(*args, **kwargs):
        if db.Users.find({'email':current_user.email, 'role':'admin'}).count() > 0:
            return view(*args, **kwargs)
        else:
            abort(401)
    return inner

def startup_required(view):
    @functools.wraps(view)
    def inner(*args, **kwargs):
        if db.Users.find({'email':current_user.email, 'role':'startup'}).count() > 0:
            return view(*args, **kwargs)
        else:
            abort(401)
    return inner

def investor_required(view):
    @functools.wraps(view)
    def inner(*args, **kwargs):
        if db.Users.find({'email':current_user.email, 'role':'investor'}).count() > 0:
            return view(*args, **kwargs)
        else:
            abort(401)
    return inner

def get_user_role(email):
	if db.Users.find({'email':email, 'role':'startup'}).count() > 0:
		role = "startup"
	elif db.Users.find({'email':email, 'role':'investor'}).count() > 0:
		role = "investor"
	elif db.Users.find({'email':email, 'role':'admin'}).count() > 0:
		role = "admin"
	else:
		role = None
	return role

@app.errorhandler(404)
def page_not_found(e):
    title = 'Not Found'
    code = '404'
    message = "We can't seem to find the page you're looking for."
    if (current_user.is_authenticated):
        return render_template('error.html', title = title, code = code, message = message, name=current_user.email, logged_in=current_user.is_authenticated), 404
    else:
        return render_template('error.html', title = title, code = code, message = message, logged_in=current_user.is_authenticated), 404

@app.errorhandler(403)
def page_forbidden(e):
    title = 'Forbidden'
    code = '403'
    message = "You do not have access to this page."
    if (current_user.is_authenticated):
        return render_template('error.html', title = title, code = code, message = message, name=current_user.email, logged_in=current_user.is_authenticated), 403
    else:
        return render_template('error.html', title = title, code = code, message = message, logged_in=current_user.is_authenticated), 403

@app.errorhandler(500)
def internal_server_error(e):
    title = 'Internal Server Error'
    code = '500'
    message = "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application."
    if (current_user.is_authenticated):
        return render_template('error.html', title = title, code = code, message = message, name=current_user.email, logged_in=current_user.is_authenticated), 500
    else:
        return render_template('error.html', title = title, code = code, message = message, logged_in=current_user.is_authenticated), 500

@app.route('/')
def index():
	# current_features = ["sophiamartika", "incub8", "eaglerivercustomtshirts"]
	# features = list(db.Startups.find({"id": {"$in": current_features}}))
	features = list(db.Startups.find({"feature": True}))
	feature_indexes = []
	for feature in features:
		feature["index"] = features.index(feature)
		if "location" in feature:
			if "latitude" in feature["location"]:
				feature["coordinates"] = [feature["location"]["latitude"], feature["location"]["longitude"]]
				feature["location"] = feature["location"]["address"]
		feature_indexes.append(features.index(feature))
	feature_indexes.pop(0)
	return render_template('index.html', feature_no = feature_indexes, features = features, logged_in=current_user.is_authenticated)

@app.route('/sorry')
def sorry():
    return render_template('under_construction.html', logged_in = current_user.is_authenticated)

@app.route('/simulation')
def simulation():
    return render_template('simulation.html', logged_in = current_user.is_authenticated)

@app.route('/embedded-simulation')
def embedded_simulation():
    return render_template('actual_simulation.html', logged_in = current_user.is_authenticated)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
    	if form.validate():
        	contact_us(form.subject.data, form.name.data, form.email.data, form.message.data)
        	if current_user.is_authenticated:
        		return redirect(url_for('dashboard', if_message = True, message="Your message was sent."))
        	else:
        		return render_template('contact.html', post = 'yup', form = form, logged_in=current_user.is_authenticated)
    form.name.data = ""
    form.email.data = ""
    form.subject.data = ""
    form.message.data = ""
    return render_template('contact.html', form = form, logged_in=current_user.is_authenticated)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('dashboard', name=current_user.email))
    if request.method == 'POST':
        if form.validate():
            check_user = User.objects(email=form.email.data).first()
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return redirect(url_for('dashboard'))
        else:
            print(form.errors)
    return render_template('login.html', form=form)

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard', methods = ['GET','POST'])
@login_required
def dashboard():
	return render_template('dashboard.html', info = {"name":"N/A"}, logged_in=current_user.is_authenticated)

@app.route('/routes', methods=['GET'])
@admin_required
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)
    
    for line in sorted(output):
        print(line)
    return redirect(url_for('index'))

@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Generate sitemap.xml """
    pages = []
    # All pages registed with flask apps
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            pages.append(rule.rule)

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    # return response
    return render_template('sitemap_template.xml', pages=pages)








if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)