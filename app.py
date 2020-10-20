from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

#sets the app and database configs
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'you-will-never-guess'
db = SQLAlchemy(app)


#an initial greeting
@app.route('/')
@app.route('/index')
def greeting():
    return render_template('greeting.html')

 
@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html") 

import routes