import os
import sys
#import app_metadata
from .app_metadata import *
#import login manager
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

#getting the parent directory name where the current directory is present
parent_path = os.path.dirname(os.path.realpath(__file__))

#adding the parent directory to the sys.path
sys.path.append(parent_path)

#import admin blueprint
from admin.routes import * #admin_bp, admin_dashboard, admin_logout, admin_create_post, admin_create_service
#import home page blueprint
from pages.routes import * #home_bp, blog_bp, contact_entry_bp, training_form_bp, mentorship_form_bp, project_form_bp, service_bp

# Create database table - delete or comment out immediately after deploying to production
from .db_config import * #import database functions/endpoints

#register home page blueprint
app.register_blueprint(home_bp)

#register admin blueprint
app.register_blueprint(admin_bp)

#register admin dashboard blueprint
app.register_blueprint(admin_dashboard)

#register admin create post blueprint
app.register_blueprint(admin_create_post)

#register admin create service blueprint
app.register_blueprint(admin_create_service)

#register admin create strategy blueprint
app.register_blueprint(admin_create_strategy)

#register admin create client blueprint
app.register_blueprint(admin_create_client)

#register admin create project blueprint
app.register_blueprint(admin_create_project)

#register admin create project tool blueprint
app.register_blueprint(admin_create_project_tool)

#register admin logout blueprint
app.register_blueprint(admin_logout)

#register blog page blueprint
app.register_blueprint(blog_bp)

#register blog page blueprint
app.register_blueprint(service_bp)

# register contact_entry route blueprint
app.register_blueprint(contact_entry_bp)

# register training_form route blueprint
app.register_blueprint(training_form_bp)

# register mentorship_form route blueprint
app.register_blueprint(mentorship_form_bp)

# register project_form route blueprint
app.register_blueprint(project_form_bp)

# register single_project route blueprint
app.register_blueprint(single_project_bp)

# register single_project_contact route blueprint
app.register_blueprint(single_project_contact_bp)

# register single_mentorship_contact route blueprint
app.register_blueprint(single_mentorship_contact_bp)

# register single_training_contact_bp route blueprint
app.register_blueprint(single_training_contact_bp)

if __name__=="__main__":
	app.run(debug=True)
