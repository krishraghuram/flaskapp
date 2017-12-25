from flask import Flask, url_for, render_template, request, jsonify
from flask_pymongo import PyMongo
from flask_login import LoginManager

app = Flask(__name__)
mongo = PyMongo(app)
login_manager = LoginManager()
login_manager.init_app(app)

# 127.0.0.1:5000/users
@app.route("/users/")
def users():
	users = []
	for i in mongo.db.user.find():
		temp = i
		del temp['_id']
		users.append(temp)
	return jsonify({'users' : users})

# 127.0.0.1:5000/add_user?usernam=raghu&password=ram
@app.route("/add_user/")
def index():
	# print(type(request.args))
	# print(request.args.get('raghu'))
	username = request.args.get('username')
	email = request.args.get('email')
	password = request.args.get('password')
	try :
		assert username is not None or password is not None
	except:
		return "Hello World!\nSend GET request with username, email and password to signup."
	mongo.db.user.insert({
		"username" : username,
		"email" : email,
		"password" : password
	})
	# return "Hello World!\nSend GET request with username, email and password to signup."
	return "Signed UP"

# 127.0.0.1:5000/del_user/raghu
@app.route("/del_user/<username>/")
def del_user(username):
	mongo.db.user.delete_one({"username" : username})
	return "Deleted	"

# 127.0.0.1:5000/del_all_users
@app.route("/del_all_users/")
def del_all_users():
	mongo.db.user.delete_many({})
	return "Deleted	All Users"