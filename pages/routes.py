import os
import sys

from flask import render_template, Blueprint

#getting the parent directory name where the current directory is present
parent_path = os.path.dirname(os.path.realpath(__file__))

#adding the parent directory to the sys.path
sys.path.append(parent_path)

#import app_metadata
from app_metadata import *

#import query_functions
from query_functions import *

# Home page Blueprint
home_bp = Blueprint('home_bp', __name__, template_folder='templates/pages', static_folder='static/pages')
# Blog page Blueprint
blog_bp = Blueprint('blog_bp', __name__, template_folder='templates/pages', static_folder='static/pages')
# Service page Blueprint
service_bp = Blueprint('service_bp', __name__, template_folder='templates/pages', static_folder='static/pages')
# Contact Entry Blueprint
contact_entry_bp = Blueprint('contact_entry_bp', __name__, template_folder='templates/pages', static_folder='static/pages')
# Training Contact Form Blueprint
training_form_bp = Blueprint('training_form_bp', __name__, template_folder='templates/pages', static_folder='static/pages')
# Mentorship Contact Form Blueprint
mentorship_form_bp = Blueprint('mentorship_form_bp', __name__, template_folder='templates/pages', static_folder='static/pages')
# Project Contact Form Blueprint
project_form_bp = Blueprint('project_form_bp', __name__, template_folder='templates/pages', static_folder='static/pages')
# Single Project Blueprint
single_project_bp = Blueprint('single_project_bp', __name__, template_folder='templates/pages', static_folder='static/pages')

@home_bp.route('/')
def home():
	cursor = mysql.connection.cursor()
	# retrieve from db the  category_id entered by the admin
	posts_sql = "SELECT * FROM posts"
	cursor.execute(posts_sql)
	records = cursor.fetchall()
	cursor.close()

	# process database - services
	cursor = mysql.connection.cursor()
	# retrieve from db the  category_id entered by the admin
	services_sql = "SELECT * FROM services"
	cursor.execute(services_sql)
	services_records = cursor.fetchall()
	cursor.close()

	#project database query
	projects_record = projects_db()
	return render_template("pages/index.html", records=records, services_records=services_records, projects_record = projects_record)

#Blog route
@blog_bp.route('/blog/<int:id>', methods=['GET', 'POST'])
def blog(id):
	cursor = mysql.connection.cursor()
	#blog_sql = "SELECT * FROM posts WHERE post_id=%s"
	blog_sql = """
	SELECT posts.post_id, posts.title, posts.content, posts.publish_date, posts.read_duration,
	admins.fname, admins.lname, categories.category_name, posts.img_url
	FROM posts 
	JOIN admins ON posts.author_id=admins.admin_id
	JOIN categories ON posts.category_id=categories.category_id
	WHERE post_id=%s
	"""
	cursor.execute(blog_sql, (id,))
	record = cursor.fetchone()
	cursor.close()
	#return f"Title: {records[1]}"
	return render_template("pages/blog-single.html", record=record)

# query 'strategies' function
def strategies_db():
	# process database - strategies
	cursor = mysql.connection.cursor()
	# retrieve from db the  category_id entered by the admin
	strategies_sql = "SELECT * FROM strategies"
	cursor.execute(strategies_sql)
	strategies_record = cursor.fetchall()
	cursor.close()
	return strategies_record

#Service route
@service_bp.route('/service/<int:id>', methods=['GET', 'POST'])
def service(id):
	# process database - services
	cursor = mysql.connection.cursor()
	# retrieve from db the  category_id entered by the admin
	services_sql = "SELECT * FROM services WHERE service_id=%s"
	cursor.execute(services_sql, (id,))
	service_record = cursor.fetchone()
	cursor.close()

	# process database - strategies -> call 'strategies_db' function
	strategies_record = strategies_db()
	return render_template("pages/service-single.html", service_record=service_record, strategies_record=strategies_record)

#Contact entry route
@contact_entry_bp.route('/contact', methods=['GET', 'POST'])
def contact_entry():
	if (request.method == 'POST'):
		#cursor = mysql.connection.cursor()
		service = request.form.get('services')
		if (service == 'Progamming (Training)'):
			return redirect(url_for('training_form_bp.training_form'))
		elif (service == 'Progamming (Mentorship)'):
			return redirect(url_for('mentorship_form_bp.mentorship_form'))
		elif (service == 'Software Project Management'):
			return redirect(url_for('project_form_bp.project_form'))
	return redirect(url_for('home_bp.home'))

#Training Form route
@training_form_bp.route('/contact_training', methods=['GET', 'POST'])
def training_form():
	
	if (request.method == 'POST'):
		firstname = request.form.get('firstname')
		lastname = request.form.get('lastname')
		email = request.form.get('email')
		phone = request.form.get('phone')
		dob = request.form.get('dob')
		experience_level = request.form.get('experience_level')
		training_stack = request.form.get('training_stack')
		training_cycle = request.form.get('training_cycle')
		# call appropriate insert function
		training_contact_insert_db(firstname, lastname, email, phone, dob, training_stack, experience_level, training_cycle)
		return redirect(url_for('home_bp.home'))
	return render_template("pages/training-form.html")

#Mentorship Form route
@mentorship_form_bp.route('/contact_mentorship', methods=['GET', 'POST'])
def mentorship_form():
	if (request.method == 'POST'):
		firstname = request.form.get('firstname')
		lastname = request.form.get('lastname')
		email = request.form.get('email')
		phone = request.form.get('phone')
		dob = request.form.get('dob')
		experience_level = request.form.get('experience_level')
		mentorship_stack = request.form.get('mentorship_stack')
		mentorship_slot = request.form.get('mentorship_slot')
		# call appropriate insert function
		mentorship_contact_insert_db(firstname, lastname, email, phone, dob, mentorship_stack, experience_level, mentorship_slot)
		return redirect(url_for('home_bp.home'))
	return render_template("pages/mentorship-form.html")

#Project Form route
@project_form_bp.route('/contact_project', methods=['GET', 'POST'])
def project_form():
	if (request.method == 'POST'):
		firstname = request.form.get('firstname')
		lastname = request.form.get('lastname')
		company = request.form.get('company')
		email = request.form.get('email')
		phone = request.form.get('phone')
		project_type = request.form.get('project_type')
		project_desc = request.form.get('project_desc')
		project_budget = request.form.get('project_budget')
		start_date = request.form.get('start_date')
		end_date = request.form.get('end_date')
		# call appropriate insert function
		project_contact_insert_db(firstname, lastname,  company, email, phone, project_type, project_desc, project_budget, start_date, end_date)
		return redirect(url_for('home_bp.home'))
	return render_template("pages/project-form.html")

#Single Project route
@single_project_bp.route('/project/<int:id>', methods=['GET', 'POST'])
def single_project(id):
	project_record = single_projects_db(id) # returns a single record
	project_tools_record = project_tools_db(project_record[0]) #returns record for a specified project
	client_record = client_db(project_record[4])
	return render_template(
		"pages/portfolio-single.html", 
		project_record=project_record, 
		project_tools_record=project_tools_record,
		client_record=client_record
		)