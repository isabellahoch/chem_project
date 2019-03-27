from flask import Flask, render_template, request, redirect, url_for, make_response, abort
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, Form, SelectField, SubmitField, BooleanField
from wtforms.validators import Email, Length, InputRequired, EqualTo, Regexp, URL
from wtforms.widgets import TextArea
from db_connect import MONGODB_URI, db
from math import ceil
from forms import ContactForm, LoginForm, ContactForm
from credentials import mlab_host, mlab_api_key, google_api_key, google_client_id, google_client_secret, gmail_password, google_app_password, sendgrid_password, cloudinary_api_key, cloudinary_api_secret
from flask_mail import Mail, Message

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

app.config['SECRET_KEY'] = "\xe2!\xfb\xbb+h\xbe\xf1\x97\x1b:\x92\x19I\x13\x19\x1fzz\xbc\x18_:"
secret_key_encoded = "8280d1960d36d9ea65a14f5fb864fe0b3e829ba940e64c84"
# secondary_key = "e221fbbb2b68bef1971b3a92194913191f7a7abc185f3a"

dbapp = MongoEngine(app)

@app.errorhandler(404)
def page_not_found(e):
    title = 'Not Found'
    code = '404'
    message = "We can't seem to find the page you're looking for."
    return render_template('error.html', title = title, code = code, message = message), 404

@app.errorhandler(403)
def page_forbidden(e):
    title = 'Forbidden'
    code = '403'
    message = "You do not have access to this page."
    return render_template('error.html', title = title, code = code, message = message), 403

@app.errorhandler(500)
def internal_server_error(e):
    title = 'Internal Server Error'
    code = '500'
    message = "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application."
    return render_template('error.html', title = title, code = code, message = message), 500

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/sorry')
def sorry():
    return render_template('under_construction.html')

@app.route('/simulation')
def simulation():
    return render_template('simulation.html')

@app.route('/embedded-simulation')
def embedded_simulation():
    return render_template('actual_simulation.html')

@app.route('/bibliography')
def bibliography():
    return render_template('bibliography.html')

# @app.route('/routes', methods=['GET'])
# def list_routes():
#     import urllib
#     output = []
#     for rule in app.url_map.iter_rules():

#         options = {}
#         for arg in rule.arguments:
#             options[arg] = "[{0}]".format(arg)

#         methods = ','.join(rule.methods)
#         url = url_for(rule.endpoint, **options)
#         line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
#         output.append(line)
    
#     for line in sorted(output):
#         print(line)
#     return redirect(url_for('index'))

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