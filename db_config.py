
from .app_metadata import *

#1 - create Tables
@app.route("/createdb")
def createdb_view():
	cursor = mysql.connection.cursor()
	
	#1 - create 'admins' Table
	admins_sql = """CREATE TABLE admins(
	admin_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, 
	fname VARCHAR(15) NOT NULL, 
	lname VARCHAR(15) NOT NULL, 
	username VARCHAR(15) UNIQUE NOT NULL, 
	password VARCHAR(100) NOT NULL
	)"""
	
    #2 - create 'categories' Table
	categories_sql = """CREATE TABLE categories(
	category_id INT AUTO_INCREMENT PRIMARY KEY,
	category_name VARCHAR(50) UNIQUE NOT NULL
	)"""

	#3 - create 'posts' Table
	posts_sql = """CREATE TABLE posts(
	post_id INT AUTO_INCREMENT PRIMARY KEY, 
	title VARCHAR(100) UNIQUE NOT NULL,
	content TEXT NOT NULL, 
	publish_date DATE NOT NULL, 
	read_duration INT NOT NULL,
	author_id INT,
	category_id INT,
	img_url TEXT NOT NULL,
	FOREIGN KEY (author_id) REFERENCES admins(admin_id),
	FOREIGN KEY (category_id) REFERENCES categories(category_id)
	ON DELETE CASCADE
	ON UPDATE CASCADE
	)"""
	
	#4 - create 'clients' Table (to store info of clients whose projects have been completed)
	clients_sql = """CREATE TABLE clients(
    client_id INT AUTO_INCREMENT PRIMARY KEY,
    organization VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL
    )
    """

    #5 - create 'projects' Table
	projects_sql = """CREATE TABLE projects(
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    leader_image VARCHAR(100) NOT NULL,
    client_id INT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    project_url VARCHAR(150) NOT NULL,
    project_category VARCHAR(50) NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(client_id)
    )"""

    #6 - create 'project_images' Table
	projects_imgages_sql = """CREATE TABLE project_images(
    project_image_id INT AUTO_INCREMENT PRIMARY KEY,
    project_image_url VARCHAR(50) NOT NULL,
    project_id INT,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
    )"""

    #7 - create 'project_tools' Table
	project_tools_sql = """CREATE TABLE project_tools(
    tool_id INT AUTO_INCREMENT PRIMARY KEY,
    tool_name VARCHAR(50) NOT NULL,
    tool_description TEXT NOT NULL,
    project_id INT,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
    )"""

    #8 - create 'services' Table
	services_sql = """CREATE TABLE services(
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    leader_image VARCHAR(50) NOT NULL,
    icon VARCHAR(20) NOT NULL,
    title VARCHAR(20) NOT NULL,
    description TEXT NOT NULL
    )"""

    #9 - create 'strategies' Table (all services have common strategies)
	strategies_sql = """CREATE TABLE strategies(
    strategy_id INT AUTO_INCREMENT PRIMARY KEY,
	strategy_name VARCHAR(50) NOT NULL,
	description TEXT NOT NULL
    )"""

	#10 - create 'training_contact' Table
	training_contact_sql = """CREATE TABLE training_contact(
	training_id INT AUTO_INCREMENT PRIMARY KEY,
	fname VARCHAR(30) NOT NULL,
	lname VARCHAR(30) NOT NULL,
	email VARCHAR(100) NOT NULL,
	phone VARCHAR(30) NOT NULL,
	dob DATE NOT NULL,
	stack VARCHAR(100) NOT NULL,
	level VARCHAR(100) NOT NULL,
	cycle VARCHAR(20) NOT NULL
	)"""

	#11 - create 'mentorship_contact' Table
	mentorship_contact_sql = """CREATE TABLE mentorship_contact(
	mentorship_id INT AUTO_INCREMENT PRIMARY KEY,
	fname VARCHAR(30) NOT NULL,
	lname VARCHAR(30) NOT NULL,
	email VARCHAR(100) NOT NULL,
	phone VARCHAR(30) NOT NULL,
	dob DATE NOT NULL,
	stack VARCHAR(100) NOT NULL,
	level VARCHAR(100) NOT NULL,
	slot VARCHAR(20) NOT NULL
	)"""

	#12 - create 'project_contact' Table
	project_contact_sql = """CREATE TABLE project_contact(
	pc_id INT AUTO_INCREMENT PRIMARY KEY,
	fname VARCHAR(30) NOT NULL,
	lname VARCHAR(30) NOT NULL,
	company VARCHAR(100) NOT NULL,
	email VARCHAR(100) NOT NULL,
	phone VARCHAR(30) NOT NULL,
	type VARCHAR(30) NOT NULL,
	description TEXT NOT NULL,
	budget VARCHAR(30) NOT NULL,
	start_date DATE NOT NULL,
	end_date DATE NOT NULL
	)"""
	
	sql_queries = [
		admins_sql,
		categories_sql,
		posts_sql,
		clients_sql,
		projects_sql,
		projects_imgages_sql,
		project_tools_sql,
		services_sql,
		strategies_sql,
		training_contact_sql,
		mentorship_contact_sql,
		project_contact_sql
		]
	
	for query in sql_queries:
		cursor.execute(query)
	cursor.close()
	return f"""
	12 Tables created: [
		'admins', 
		'catgegories', 
		'posts',
		'clients',
		'projects',
		'projects_imgages',
		'project_tools',
		'services',
		'strategies',
		'training_contact',
		'mentorship_contact',
		'project_contact'
	]
	"""

#-------------------------------------------------------------------------------------------------------------------------

#2 - Create admin users
@app.route("/enter_admin")
def enter_admin_view():
	try:
		cursor = mysql.connection.cursor()
		password = "admin101pass101"
		#password = "admin102pass102"
		password = flask_bcrypt.generate_password_hash(password,10).decode("utf-8")
		user = ["Stanley", "Edeh", "admin101", password]
		#user = ["John", "Doe", "admin102", password]
		db_insert = "INSERT INTO admins(fname, lname, username, password) VALUES (%s, %s, %s, %s)"
		cursor.execute(db_insert, (user[0], user[1], user[2], user[3]))
		mysql.connection.commit()
		cursor.close()
		return "Admin user created!"
	except:
		return "Error in creating user!"

#-------------------------------------------------------------------------------------------------------------------------


#3 - insert blog categories into database
@app.route("/insert_categories")
def insert_categories_view():
	try:
		cursor = mysql.connection.cursor()
		sql = "INSERT INTO categories() VALUES (%s, %s)"
		val = [
			(1, "AI/ML"),
			(2, "Backend"),
			(3, "Blockchain"),
			(4, "Database"),
			(5, "Frontend"),
			(6, "Fullstack"),
			(7, "UI/UX"),
			(8, "IoT")
		]
		cursor.executemany(sql, val)
		count = cursor.rowcount
		mysql.connection.commit()
		cursor.close()
		return f"{count} records created!"
	except:
		return "Error in creating records!"
