from flask import Flask
from flask import url_for, render_template, request
from flask import redirect, jsonify
from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
db = MongoEngine(app)
app.secret_key = 'j+cTGqe32uAkc9oHxlu0fgx2SRAy9kVsJ1/MkBho3Po='
app.config['MONGODB_SETTINGS'] = {
	'db': 'flaskapp'
}
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

#User Model
class User(db.Document):
	username = db.StringField(max_length=50, required=True, unique=True)
	email = db.StringField(max_length=100, required=True)
	password = db.StringField(max_length=50, required=True)

	def __repr__(self):
		return '<User %r>' % self.username
	def is_authenticated(self):
		return True
	def is_active(self):
		return True
	def is_anonymous(self):
		return False
	def get_id(self):
		return str(self.username)

@login_manager.user_loader
def load_user(user_id):
	return User.objects.get(username=user_id)

@app.route('/')
@login_required
def index():
	return 'Welcome to FlaskApp'

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
	if request.method=='GET': #Send the signup form
		return render_template('signup.html')

	elif request.method=='POST': #Signup the user
		#Get the post data
		username = request.form.get('username')
		email    = request.form.get('email')
		password = request.form.get('password')
		confirm_password = request.form.get('confirm_password')

		#Checks
		errors = []
		if username is None or username=='':
			errors.append('Username is required')
		if email is None or email=='':
			errors.append('Email is required')
		if password is None or password=='':
			errors.append('Password is required')
		if confirm_password is None or confirm_password=='':
			errors.append('Confirm Password is required')
		if password!=confirm_password:
			errors.append('Passwords do not match')

		#Create New User and Save to Database
		pw_hash = bcrypt.generate_password_hash(password).decode(‘utf-8’)
		newuser = User(username=username, email=email, password=pw_hash)
		newuser.save()

		#Return Success Message
		return "Signup Successful"
		
		#Error Message
		if len(errors)>0:
			return render_template('error.html', errors=errors)
		
@app.route('/login/', methods=['GET', 'POST'])
def login():
	if request.method=='GET': #Send the login form
		return render_template('login.html')

	elif request.method=='POST': #Login the user
		#Get the post data
		username = request.form.get('username')
		password = request.form.get('password')

		#Checks
		errors = []
		if username is None or username=='':
			errors.append('Username is required')
		if password is None or password=='':
			errors.append('Password is required')
		#Query for user from database and check password
		user = User.objects.get_or_404(username=username)
		if bcrypt.check_password_hash(user.password, password) :
			login_user(user)
			return "Login Successful"
		else:
			errors.append("Password is incorrect")

		#Error Message
		if len(errors)>0:
			return render_template('error.html', errors=errors)

@app.route("/logout/")
@login_required
def logout():
	logout_user()
	return "Logged out"

@app.route("/change_password/", methods=['GET', 'POST'])
@login_required
def change_password():
	if request.method=='GET': #Send the change password form
		return render_template('change_password.html')

	elif request.method=='POST': 
		#Get the post data
		username = request.form.get('username')
		current_password = request.form.get('current_password')
		new_password = request.form.get('password')
		confirm_new_password = request.form.get('confirm_password')

		#Checks
		errors = []
		if username is None or username=='':
			errors.append('Username is required')
		if current_password is None or current_password=='':
			errors.append('Current Password is required')
		if new_password is None or new_password=='':
			errors.append('New Password is required')
		if confirm_new_password is None or confirm_new_password=='':
			errors.append('Confirm New Password is required')
		if new_password!=confirm_new_password:
			errors.append('New Passwords do not match')
		user = User.objects.get_or_404(username=username)
		if not bcrypt.check_password_hash(user.password, password) :
			errors.append("Password is incorrect")
		#Query for user from database and check password
		if len(errors)==0:
			pw_hash = bcrypt.generate_password_hash(new_password).decode(‘utf-8’)
			user.password = pw_hash
			user.save()
			return "Password Changed"
		#Error Message
		elif len(errors)>0:
			return render_template('error.html', errors=errors)



################################
###HIDDEN VIEWS FOR DEBUGGING###
################################
@app.route('/users/')
def users():
	return jsonify(User.objects)

@app.route('/del_user/<username>/')
def del_user(username):
	try:
		User.objects.get_or_404(username=username).delete()
		return "Deleted"
	except Exception as e:
		return str(e)

@app.route('/del_all_users/')
def del_all_users():
	for i in User.objects:
		i.delete()
	return "Deleted All Users"

@app.route('/me/')
@login_required
def me():
	return "You are logged in as : %s" % current_user.username