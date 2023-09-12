from app_metadata import *

# Function to fetch data from 'projects' table
def projects_db():
	cursor = mysql.connection.cursor()
	projects_sql = "SELECT * FROM projects"
	cursor.execute(projects_sql)
	projects_record = cursor.fetchall()
	cursor.close()
	return projects_record

# Single Project Function to fetch data from 'projects' table
def single_projects_db(id):
	cursor = mysql.connection.cursor()
	single_project_sql = "SELECT * FROM projects WHERE project_id=%s"
	cursor.execute(single_project_sql, (id,))
	single_project_record = cursor.fetchone()
	cursor.close()
	return single_project_record

# Project Tools Function to fetch data from 'project_tools' table for a specific project
def project_tools_db(id):
	cursor = mysql.connection.cursor()
	project_tools_sql = "SELECT * FROM project_tools WHERE project_id=%s"
	cursor.execute(project_tools_sql, (id,))
	project_tools_record = cursor.fetchall()
	cursor.close()
	return project_tools_record

# Client Function to fetch data from 'clients' table for a specific project
def client_db(id):
	cursor = mysql.connection.cursor()
	client_sql = "SELECT * FROM clients WHERE client_id=%s"
	cursor.execute(client_sql, (id,))
	client_record = cursor.fetchone()
	cursor.close()
	return client_record

#INSERT Query -> training_contact_insert_db()
def training_contact_insert_db(fname, lname, email, phone, dob, stack, level, cycle):
	cursor = mysql.connection.cursor()
	training_contact_sql = "INSERT INTO training_contact(fname, lname, email, phone, dob, stack, level, cycle) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
	cursor.execute(training_contact_sql, (fname, lname, email, phone, dob, stack, level, cycle))
	mysql.connection.commit()
	cursor.close()

#INSERT Query -> mentorship_contact_insert_db()
def mentorship_contact_insert_db(fname, lname, email, phone, dob, stack, level, slot):
	cursor = mysql.connection.cursor()
	mentorship_contact_sql = "INSERT INTO mentorship_contact(fname, lname, email, phone, dob, stack, level, slot) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
	cursor.execute(mentorship_contact_sql, (fname, lname, email, phone, dob, stack, level, slot))
	mysql.connection.commit()
	cursor.close()

#INSERT Query -> project_contact_insert_db()
def project_contact_insert_db(fname, lname,  company, email, phone, type, description, budget, start_date, end_date):
	cursor = mysql.connection.cursor()
	project_contact_sql = "INSERT INTO project_contact(fname, lname, company, email, phone, type, description, budget, start_date, end_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	cursor.execute(project_contact_sql, (fname, lname, company, email, phone, type, description, budget, start_date, end_date))
	mysql.connection.commit()
	cursor.close()

#SELECT Query -> training_contact_select_db()
def training_contact_select_db():
	cursor = mysql.connection.cursor()
	training_contact_sql = "SELECT * FROM training_contact"
	cursor.execute(training_contact_sql)
	training_contact_record = cursor.fetchall()
	cursor.close()
	return training_contact_record

#SELECT Query -> mentorship_contact_select_db()
def mentorship_contact_select_db():
	cursor = mysql.connection.cursor()
	mentorship_contact_sql = "SELECT * FROM mentorship_contact"
	cursor.execute(mentorship_contact_sql)
	mentorship_contact_record = cursor.fetchall()
	cursor.close()
	return mentorship_contact_record

#SELECT Query -> project_contact_select_db()
def project_contact_select_db():
	cursor = mysql.connection.cursor()
	project_contact_sql = "SELECT * FROM project_contact"
	cursor.execute(project_contact_sql)
	project_contact_record = cursor.fetchall()
	cursor.close()
	return project_contact_record

#SELECT Query -> single_training_contact_select_db()
def single_training_contact_select_db(id):
	cursor = mysql.connection.cursor()
	training_contact_sql = "SELECT * FROM training_contact WHERE training_id=%s"
	cursor.execute(training_contact_sql, (id,))
	training_contact_record = cursor.fetchone()
	cursor.close()
	return training_contact_record

#SELECT Query -> single_mentorship_contact_select_db()
def single_mentorship_contact_select_db(id):
	cursor = mysql.connection.cursor()
	mentorship_contact_sql = "SELECT * FROM mentorship_contact WHERE mentorship_id=%s"
	cursor.execute(mentorship_contact_sql, (id,))
	mentorship_contact_record = cursor.fetchone()
	cursor.close()
	return mentorship_contact_record

#SELECT Query -> single_project_contact_select_db()
def single_project_contact_select_db(id):
	cursor = mysql.connection.cursor()
	project_contact_sql = "SELECT * FROM project_contact WHERE pc_id=%s"
	cursor.execute(project_contact_sql, (id,))
	project_contact_record = cursor.fetchone()
	cursor.close()
	return project_contact_record

# Get Statistics
# Function to fetch data from 'projects' table
def db_stats():
	cursor = mysql.connection.cursor()
	projects_sql = "SELECT * FROM projects"
	number_of_projects = cursor.execute(projects_sql)
	cursor.close()

	cursor = mysql.connection.cursor()
	project_contact_sql = "SELECT * FROM project_contact"
	number_of_project_requests = cursor.execute(project_contact_sql)
	cursor.close()

	cursor = mysql.connection.cursor()
	training_contact_sql = "SELECT * FROM training_contact"
	number_of_training_requests = cursor.execute(training_contact_sql)
	cursor.close()

	cursor = mysql.connection.cursor()
	mentorship_contact_sql = "SELECT * FROM mentorship_contact"
	number_of_mentorship_requests = cursor.execute(mentorship_contact_sql)
	cursor.close()

	return (
		number_of_projects,
		number_of_project_requests,
		number_of_training_requests,
		number_of_mentorship_requests
		)