from flask import Flask
from flask import url_for, render_template, request
from flask import redirect, jsonify
from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form

app = Flask(__name__)
db = MongoEngine(app)
app.config['MONGODB_SETTINGS'] = {
	'db': 'flaskapp'
}

#User Model
class User(db.Document):
	username = db.StringField(max_length=50, required=True, unique=True)
	email = db.StringField(max_length=100, required=True)
	password = db.StringField(max_length=50, required=True)

@app.route('/')
def index():
	return "To be implemented"

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
		newuser = User(username=username, email=email, password=password)
		newuser.save()

		#Return Success Message
		return "Signup Successful"
		
		#Error Message
		if len(errors)>0:
			return render_template('error.html', errors=errors)
		
@app.route('/login/')
def login():
	return "To be implemented"












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
