### Key requirements
1) REST API
2) Python3, Flask, MongoDB
3) Basic Authentication
4) Sign in, Sign up, Forgot Password

### Detailed Requirements
1) User - username, email, password
2) Authentication - password needs to be hashed
3) Sign Up, Login, Logout, Change Password, Forgot Password

### Choices 
1) The ORM
	* Pymongo, Mongokit, MongoEngine and MongoAlchemy
	* All have flask extensions
	* MongoAlchemy is no longer maintained
	* Among the other three, do not know which one is better
	* So, based on our choice of Authentication Framework, we are going with MongoEngine.

2) The Authentication Framework
	* There are two extensions  Flask-Login and Flask-User
	* Flask-Login is a no-frills extension that provides simple features. 
		* It handles session management, restricting views to logged in users and a few other minor things. 
		* It does not provide a User model. 
		* It does not provide User Registration or User Recovery. 
	* Flask-User is actually built on top of Flask-Login. 
		* Besides doing what Flask-Login does, it also does the following. 
			* Added Security and Reliability
			* User Registrations and Email Confirmations
			* Change Usernames/Passwords and handle Forgotten Passwords
		* However, unlike flask-login, it is not ORM and DB agnostic. 
			* It comes with a adapter for SQLAlchemy as stated (here)[http://flask-user.readthedocs.io/en/v0.6/limitations.html#supported-databases]
			* But that is not a big problem. (This)[https://github.com/lingthio/Flask-User/issues/37] and (this)[https://flask-user.readthedocs.io/en/latest/mongodb_app.html] provide a solution for using MongoDB, using MongoEngine.


