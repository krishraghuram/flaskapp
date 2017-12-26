### Key requirements
1) REST API
2) Python3, Flask, MongoDB
3) Basic Authentication
4) Sign in, Sign up, Forgot Password
5) OAuth

### Detailed Requirements
1) User - username, email, password
2) Authentication - password needs to be hashed
3) Sign Up, Login, Logout, Change Password
4) Forgot Password - Sending a reset link to the registered email
5) OAuth - Registering as a client to the Google OAuth Provider.


## What has been done?

### TL;DR
1) User Model using MongoEngine with username, email and password fields
2) Session based Authentication using Flask-Login
3) Endpoints for signup, login, logout and change password. 
4) To be done : 
	* Forgot Password reset link using gmail api/postfix etc.
	* OAuth using google's oauth providers 

### Detailed
1) The ORM/ODM/Database Framework
	* PyMongo, Mongokit, MongoEngine and MongoAlchemy
	* All have flask extensions
	* MongoAlchemy is no longer maintained
	* PyMongo is a no-frills, bare bones python api for mongodb. It allows executing mongodb statements/queries from python. It does not contain any higher level abstractions, in terms of Fields, Models or Validation. 
	* Between MongoKit and MongoEngine, MongoEngine seemed more popular and stable. Thus, I used MongoEngine. 

2) The Authentication Framework
	* There are several flask extensions that abstract authentication - Flask-User, Flask-Login, Flask-Security. 
	* Flask-Login is a no-frills extension that provides simple features. 
		* It handles Session Management, Restricting views to logged in users and a few other minor things. 
		* It does not provide a User model. 
		* It does not provide User Registration, User Recovery. 
		* [This](https://medium.com/@perwagnernielsen/getting-started-with-flask-login-can-be-a-bit-daunting-in-this-tutorial-i-will-use-d68791e9b5b5) is a good place to start with flask-login, as the documentation does not give clear examples. 
	* Flask-User is actually built on top of Flask-Login. 
		* Besides doing what Flask-Login does, it also does the following. 
			* Added Security and Reliability
			* User Registrations and Email Confirmations
			* Change Usernames/Passwords and handle Forgotten Passwords
		* However, unlike flask-login, it is not ORM and DB agnostic. The current stable version, v0.6 does not support MongoDB. 
		* Version v0.9 supports MongoDB, but it is in alpha now. Thus, we are going with Flask-Login.
	* Flask-Security is similar to Flask-User and is compatible with Flask-MongoEngine. There is no good reason as to why I didn't use it instead of Flask-Login. This is the first thing that I would change in this project. 
	* To implement some form of security on Flask-Login, I checked out the following, 
		* [Flask-Bcrypt](https://github.com/maxcountryman/flask-bcrypt/)
		* [From Explore Flask](http://exploreflask.com/en/latest/users.html#storing-passwords), we have the same. 
		* [This](https://pythonprogramming.net/password-hashing-flask-tutorial/) suggests a different method, using SHA256 for generating salted passwords.
		* I do not know about the comparative security of the above methods or more. **But right now, bcrypt seems like a fine solution.**
		* On a unrelated note, this is a good post on [securing flask](https://damyanon.net/post/flask-series-security/)

3) OAuth
	* [Prior knowledge](https://www.youtube.com/playlist?list=PL1wWPceZhcVlD0Mt0YI7a-ky3boOGNTUM)
	* Soooo many projects - Flask-OAuthlib, Flask-Social, Flask-Dance and Flask-OAuth and more. 
	* [Flask-OAuthlib](https://github.com/lepture/flask-oauthlib), [authlib](https://github.com/lepture/authlib) and [oauthlib](https://github.com/idan/oauthlib) are packages which allow creation of Providers - which we dont need, and will never need. 
	* [Flask-Dance](https://github.com/singingwolfboy/flask-dance) looks good, and is actually listed on [Flask Extensions](http://flask.pocoo.org/extensions/) page
	* [Flask-OAuth](https://github.com/mitsuhiko/flask-oauth) also seems good and is also listed on Flask Extensions page. 
 	* [Flask-Social](https://github.com/mattupstate/flask-social) is built by the same developer as Flask-Security. That makes it easy to interface them both. 
