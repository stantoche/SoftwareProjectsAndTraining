import os
from flask import Flask, flash, render_template, Blueprint, url_for, redirect, request, session
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL #import sql connector
from flask_ckeditor import CKEditor

app = Flask(__name__)
app.secret_key = '!^Mun57opPaBul'
flask_bcrypt = Bcrypt(app)
app.config['CKEDITOR_PKG_TYPE'] = 'full'
ckeditor = CKEditor(app)

#Image handling
UPLOAD_FOLDER = 'static/pages/images/blog'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Service mage handling
SERVICE_UPLOAD_FOLDER = 'static/pages/images/services'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['SERVICE_UPLOAD_FOLDER'] = SERVICE_UPLOAD_FOLDER

#Project Leader Image handling
PROJECT_LEADER_IMG_UPLOAD_FOLDER = 'static/pages/images/project_leaders'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['PROJECT_LEADER_IMG_UPLOAD_FOLDER'] = PROJECT_LEADER_IMG_UPLOAD_FOLDER

# configure database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'stantoche'
mysql = MySQL(app)