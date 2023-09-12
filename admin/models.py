from flask_login import UserMixin

class User(UserMixin):
	def __init__(self, user_id, username, password):
		self.user_id = user_id
		self.username = username
		self.password = password

	def get_id(self):
		return str(self.user_id)

	# Predefined list of users
users = [
	User(1, 'user1', 'password1'),
	User(2, 'user2', 'password2'),
	User(3, 'user3', 'password3')	
] 
	
"""class User(UserMixin):
	def __init__(self, id):
		self.id = id

	def get_id(self):
		return str(self.id)"""