from flask import render_template,request,redirect,url_for
from flask_login import login_user,logout_user,current_user,login_required


def register_routes(app,db,bcrypt):
    
    @app.route('/')
    def index():
        return f"<h1>Hello world</h1>"