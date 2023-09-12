import os
import sys
import random
#from flask import Flask, render_template, Blueprint, url_for, request
from flask_login import LoginManager, login_user, login_required, logout_user
from datetime import datetime

#getting the parent directory name where the current directory is present
parent_path = os.path.dirname(os.path.realpath(__file__))

#adding the parent directory to the sys.path
sys.path.append(parent_path)

#import app_metadata
from app_metadata import *

#import query_functions
from query_functions import *

#create LoginManager
login_manager = LoginManager()
login_manager.init_app(app)



# import modules
from forms import AdminLoginForm #define form --> admin/forms.py
from models import User, users #define user model --> admin/models.py

#load users by their ID
@login_manager.user_loader
def load_user(user_id):
	# Load User from database or any other storage based on user_id
	user_id = "stan"
	return User(user_id)

# Defining Blueprints
admin_bp = Blueprint('admin_bp', __name__, template_folder='templates', static_folder='static/pages')
admin_dashboard = Blueprint('admin_dashboard', __name__, template_folder='templates', static_folder='static/admin')
admin_logout = Blueprint('admin_logout', __name__)

# Admin Control Panel Blueprints - 'admin_create_post'
admin_create_post = Blueprint('admin_create_post', __name__, template_folder='templates', static_folder='static/admin')

# Admin Control Panel Blueprints - 'admin_create_service'
admin_create_service = Blueprint('admin_create_service', __name__, template_folder='templates', static_folder='static/admin')

# Admin Control Panel Blueprints - 'admin_create_strategy'
admin_create_strategy = Blueprint('admin_create_strategy', __name__, template_folder='templates', static_folder='static/admin')

# Admin Control Panel Blueprints - 'admin_create_client'
admin_create_client = Blueprint('admin_create_client', __name__, template_folder='templates', static_folder='static/admin')

# Admin Control Panel Blueprints - 'admin_create_project'
admin_create_project = Blueprint('admin_create_project', __name__, template_folder='templates', static_folder='static/admin')

# Admin Control Panel Blueprints - 'admin_create_project_tool'
admin_create_project_tool = Blueprint('admin_create_project_tool', __name__, template_folder='templates', static_folder='static/admin')

# Admin Control Panel Blueprints - 'single_project_contact_bp'
single_project_contact_bp = Blueprint('single_project_contact_bp', __name__, template_folder='templates', static_folder='static/admin')

# Admin Control Panel Blueprints - 'single_training_contact_bp'
single_training_contact_bp = Blueprint('single_training_contact_bp', __name__, template_folder='templates', static_folder='static/admin')

# Admin Control Panel Blueprints - 'single_mentorship_contact_bp'
single_mentorship_contact_bp = Blueprint('single_mentorship_contact_bp', __name__, template_folder='templates', static_folder='static/admin')


# Defining routes with Blueprint
@admin_bp.route('/admin', methods=["GET", "POST"])
def admin_home():
	form = AdminLoginForm(request.form)
	session["msg"] = ""
	if (request.method == 'POST'):
		username = form.username.data
		password = form.password.data
		# query user data from the database
		cursor = mysql.connection.cursor()
		cursor.execute("SELECT * FROM admins WHERE username=%s", (username,))
		record = cursor.fetchone()
		cursor.close()
		if record:
			if flask_bcrypt.check_password_hash(record[4], password):
				session['loggedin'] = True
				session['username'] = record[3]
				session['id'] = record[0]
				return redirect(url_for("admin_dashboard.admin_panel"))
			else:
				session["msg"] = 'Incorrect username or password. Please, try again!'
	return render_template("pages/admin/index.html", form=form)

# Defining admin dashboard Blueprint routes
@admin_dashboard.route('/admin/adminDashboard', methods=["GET", "POST"])
def admin_panel():
	if "loggedin" in session:
		#Get statistics
		project_count = db_stats()[0]
		project_requests_count = db_stats()[1]
		training_count = db_stats()[2]
		mentorship_count = db_stats()[3]

		#Get Contact Recocords
		training_contact = training_contact_select_db()
		mentorship_contact = mentorship_contact_select_db()
		project_contact = project_contact_select_db()

		return render_template(
			"control_panel/index.html", 
			username=session["username"], 
			project_count=project_count,
			project_requests_count=project_requests_count,
			training_count=training_count,
			mentorship_count=mentorship_count,
			training_contact=training_contact,
			mentorship_contact=mentorship_contact,
			project_contact=project_contact
			)
	else:
		return redirect(url_for("admin_bp.admin_home"))

#function to validate image file extensions
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Admin Control Panel | Views - createPost
@admin_create_post.route("/admin/createPost", methods=["POST", "GET"])
def admin_post():
	if "loggedin" in session:
		if (request.method == 'POST'):
			title = request.form.get("title")
			category = request.form.get("category")
			img_url = request.form.get("img_url")
			#get image file data
			img_file = request.files['img_file']

			content = request.form.get("content")
			pub_date = datetime.now()
			read_duration = request.form.get("duration")

			cursor = mysql.connection.cursor()
			# retrieve from db the  category_id entered by the admin
			cat_sql = "SELECT * FROM categories WHERE category_name=%s"
			cursor.execute(cat_sql, (category,))
			record = cursor.fetchone()

			#process image storage
			if img_file.filename == '':
				flash('No selected file!')
				return redirect(url_for('admin_create_post.admin_post'))
			if img_file and allowed_file(img_file.filename):
				filename = secure_filename(img_file.filename)
				suffices = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
				random_suffix = random.choices(suffices,k=4)
				random_suffix = ''.join(random_suffix)
				filename = filename.rsplit('.', 1)[0] + "_" + random_suffix + "." + filename.rsplit('.', 1)[1]
				img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			if record:
				post_sql = "INSERT INTO posts(title, content, publish_date, read_duration, author_id, category_id, img_url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
				cursor.execute(post_sql, (title, content, pub_date, read_duration, session['id'], record[0], filename))
				mysql.connection.commit()
				cursor.close()
			
			return f"""Blog post created successfully!"""
		return render_template("control_panel/create-post.html", username=session["username"])
	else:
		return redirect(url_for("admin_bp.admin_home"))

# Admin Control Panel | Views - createService
@admin_create_service.route("/admin/createService", methods=["POST", "GET"])
def admin_service():
	if "loggedin" in session:
		if (request.method == 'POST'):
			title = request.form.get("title")
			icon = request.form.get("icon")
			#get image file data
			img_file = request.files['img_file']

			description = request.form.get("service_desc")

			cursor = mysql.connection.cursor()

			#process image storage
			if img_file.filename == '':
				flash('No selected file!')
				return redirect(url_for('admin_create_service.admin_service'))
			if img_file and allowed_file(img_file.filename):
				filename = secure_filename(img_file.filename)
				suffices = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
				random_suffix = random.choices(suffices,k=4)
				random_suffix = ''.join(random_suffix)
				filename = filename.rsplit('.', 1)[0] + "_" + random_suffix + "." + filename.rsplit('.', 1)[1]
				img_file.save(os.path.join(app.config['SERVICE_UPLOAD_FOLDER'], filename))

			service_sql = "INSERT INTO services(leader_image, icon, title, description) VALUES (%s, %s, %s, %s)"
			cursor.execute(service_sql, (filename, icon, title, description))
			mysql.connection.commit()
			cursor.close()
			
			return f"""Service created successfully!"""
		return render_template("control_panel/create-service.html", username=session["username"])
	else:
		return redirect(url_for("admin_bp.admin_home"))


# Admin Control Panel | Views - createStrategy
@admin_create_strategy.route("/admin/createStrategy", methods=["POST", "GET"])
def admin_strategy():
	if "loggedin" in session:
		if (request.method == 'POST'):
			title = request.form.get("title")

			description = request.form.get("strategy_desc")

			cursor = mysql.connection.cursor()
			strategy_sql = "INSERT INTO strategies(strategy_name, description) VALUES (%s, %s)"
			cursor.execute(strategy_sql, (title, description))
			mysql.connection.commit()
			cursor.close()
			
			return f"""Strategy created successfully!"""
		return render_template("control_panel/create-strategy.html", username=session["username"])
	else:
		return redirect(url_for("admin_bp.admin_home"))

#Admin Control Panel | Views - 'client_insert_db' function
def client_insert_db(organization, location):
	cursor = mysql.connection.cursor()
	strategy_sql = "INSERT INTO clients(organization, location) VALUES (%s, %s)"
	cursor.execute(strategy_sql, (organization, location))
	mysql.connection.commit()
	cursor.close()

# Admin Control Panel | Views - createClient
@admin_create_client.route("/admin/createClient", methods=["POST", "GET"])
def admin_client():
	if "loggedin" in session:
		if (request.method == 'POST'):
			organization = request.form.get("organization")
			location = request.form.get("location")
			# call 'client_insert_db()' function
			client_insert_db(organization, location)
			return f"""Client created successfully!"""
		return render_template("control_panel/create-client.html", username=session["username"])
	else:
		return redirect(url_for("admin_bp.admin_home"))

# Function to fetch data from 'clients' database
def clients_db():
	# process database - strategies
	cursor = mysql.connection.cursor()
	clients_sql = "SELECT * FROM clients"
	cursor.execute(clients_sql)
	clients_record = cursor.fetchall()
	cursor.close()
	return clients_record


# Admin Control Panel | Views - createProject
@admin_create_project.route("/admin/createProject", methods=["POST", "GET"])
def admin_project():
	if "loggedin" in session:
		if (request.method == 'POST'):
			title = request.form.get("title")
			project_desc = request.form.get("project_desc")
			#img_url = request.form.get("img_url")
			#get image file data
			img_file = request.files['img_file']
			client_id = int(request.form.get('client_id'))
			start_date = request.form.get("start_date")
			end_date = request.form.get("end_date")
			project_url = request.form.get("project_url")
			project_category = request.form.get("project_category")

			cursor = mysql.connection.cursor()

			#process image storage
			if img_file.filename == '':
				flash('No selected file!')
				return redirect(url_for('admin_create_post.admin_post'))
			if img_file and allowed_file(img_file.filename):
				filename = secure_filename(img_file.filename)
				suffices = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
				random_suffix = random.choices(suffices,k=4)
				random_suffix = ''.join(random_suffix)
				filename = filename.rsplit('.', 1)[0] + "_" + random_suffix + "." + filename.rsplit('.', 1)[1]
				img_file.save(os.path.join(app.config['PROJECT_LEADER_IMG_UPLOAD_FOLDER'], filename))

			project_sql = "INSERT INTO projects(title, description, leader_image, client_id, start_date, end_date, project_url, project_category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
			cursor.execute(project_sql, (title, project_desc, filename, client_id, start_date, end_date, project_url, project_category))
			mysql.connection.commit()
			cursor.close()
			
			return f"""Project created successfully!"""
		clients_record = clients_db()
		return render_template("control_panel/create-project.html", username=session["username"], clients_record=clients_record)
	else:
		return redirect(url_for("admin_bp.admin_home"))

# Admin Control Panel | Views - createProjectTool
@admin_create_project_tool.route("/admin/createProjectTool", methods=["POST", "GET"])
def admin_project_tool():
	if "loggedin" in session:
		projects_record = projects_db()
		if (request.method == 'POST'):
			tool_name = request.form.get("tool_name")
			tool_description = request.form.get("tool_description")
			project_id = request.form.get("project_id")

			cursor = mysql.connection.cursor()

			project_sql = "INSERT INTO project_tools(tool_name, tool_description, project_id) VALUES (%s, %s, %s)"
			cursor.execute(project_sql, (tool_name, tool_description, project_id))
			mysql.connection.commit()
			cursor.close()
			
			#return f"""Project tool created successfully!"""
			return render_template("control_panel/create-project-tool.html", username=session["username"], projects_record=projects_record)
		#projects_record = projects_db()
		return render_template("control_panel/create-project-tool.html", username=session["username"], projects_record=projects_record)
	else:
		return redirect(url_for("admin_bp.admin_home"))

#Single Project Contact route
@single_project_contact_bp.route('/admin/project/<int:id>', methods=['GET', 'POST'])
def single_project_contact(id):
	project_record = single_project_contact_select_db(id) # returns a single record
	return render_template(
		"control_panel/project-report.html",
		project_record=project_record
		)

#Single Training Contact route
@single_training_contact_bp.route('/admin/training/<int:id>', methods=['GET', 'POST'])
def single_training_contact(id):
	training_record = single_training_contact_select_db(id) # returns a single record
	return render_template(
		"control_panel/training-report.html",
		training_record=training_record
		)

#Single Mentorship Contact route
@single_mentorship_contact_bp.route('/admin/mentorship/<int:id>', methods=['GET', 'POST'])
def single_mentorship_contact(id):
	mentorship_record = single_mentorship_contact_select_db(id) # returns a single record
	return render_template(
		"control_panel/mentorship-report.html",
		mentorship_record=mentorship_record
		)

# Logout view
@admin_logout.route("/adminLogout", methods=['GET', 'POST'])
def adlogout():
	session.pop("loggedin", None)
	session.pop("username", None)
	return redirect(url_for("admin_bp.admin_home"))