from . import auth_bp
from flask import render_template

@auth_bp.route('/login',methods=['GET'])
def login():
    return render_template('login.html')

@auth_bp.route('/register')
def register():
    return render_template('register.html')