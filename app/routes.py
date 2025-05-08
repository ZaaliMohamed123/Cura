from flask import render_template,request,redirect,url_for,jsonify
from flask_login import login_user,logout_user,current_user,login_required
from models import Users
from datetime import datetime


def register_routes(app,db,bcrypt):
    
    @app.route('/')
    def index():
        return render_template("Login_Signup.html")
    
    @app.route('/test')
    def test():
        return render_template("core.html")
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            # Get form data
            data = request.get_json()
            print(data)
            email = data.get('email')
            password = data.get('password')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            phone_number = data.get('phone_number')
            
            role = 'Patient'  
            
            date_of_birth_str = data.get('date_of_birth')  # Get the date string
        
            # Parse the date string into a Python date object
            date_of_birth = None
            if date_of_birth_str:
                try:
                    date_of_birth = datetime.strptime(date_of_birth_str, "%Y-%m-%d").date()
                except ValueError:
                    return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
            

            # Check if email already exists
            existing_user = Users.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({'error': 'error'}), 409

            # Hash password
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            # Create new user
            new_user = Users(
                email=email,
                password_hash=hashed_password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                date_of_birth=date_of_birth,
                role=role  
            )

            # Save to database
            db.session.add(new_user)
            db.session.commit()

            return jsonify({'message': 'success'}), 200
        
        
    @app.route('/login',methods=['POST'])
    def login():
        if request.method == 'POST':
            data = request.get_json()
            print(data)
            email = data.get('email')
            password = data.get('password')
            
            user = Users.query.filter_by(email=email).first()
            
            if not user:
                return jsonify({"error": "noUser"}), 409
            
            if bcrypt.check_password_hash(user.password_hash, password):
                login_user(user)
                return jsonify({"message": "Login successful!"}), 200
            else:
                return jsonify({"error": "passProb"}), 409
