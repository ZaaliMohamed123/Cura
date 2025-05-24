from flask import render_template,request,redirect,url_for,jsonify,flash
from flask_login import login_user,logout_user,current_user,login_required
from models import Users,Medications
from datetime import datetime


def register_routes(app,db,bcrypt):
    
    @app.route('/')
    def index():
        return render_template("Login_Signup.html")
    
    @app.route('/dashboard')
    def dashboard():
        return render_template("dashboard.html")
    
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
            
    @app.route('/medications')
    def medications():
        medications = Medications.query.filter_by(patient_id=current_user.user_id).all()
        return render_template('medications.html', medications=medications)

    @app.route('/add_medication', methods=['GET', 'POST'])
    @login_required  # Ensure only logged-in users can access this route
    def add_medication():
        if request.method == 'GET':
            return render_template('add_medication.html')
        elif request.method == 'POST':
            # Extract form data
            name = request.form.get('medicineName')
            dosage = request.form.get('dosage')
            frequency = request.form.get('frequency')
            start_date = request.form.get('startDate')
            end_date = request.form.get('endDate')  # This is optional
            print(name)

            # Validate form data
            if not name or not dosage or not frequency or not start_date:
                flash('All fields are required!', 'danger')
                return redirect(url_for('add_medication'))

            # Convert start_date and end_date to datetime.date objects
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                if end_date:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
                return redirect(url_for('add_medication'))

            # Create a new Medication instance
            new_medication = Medications(
                patient_id=current_user.user_id,  # Use the current_user's user_id
                name=name,
                dosage=dosage,
                frequency=frequency,
                start_date=start_date,
                end_date=end_date
            )
            print(new_medication)

            # Add to the database
            try:
                db.session.add(new_medication)
                db.session.commit()
                flash('Medication added successfully!', 'success')
                return redirect(url_for('medications'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while adding the medication. Please try again.', 'danger')
                return redirect(url_for('add_medication'))
            
    @app.route('/delete_medication/<int:med_id>')
    @login_required
    def delete_medication(med_id):
        med = Medications.query.filter_by(medication_id=med_id, patient_id=current_user.user_id).first()
        if med:
            db.session.delete(med)
            db.session.commit()
            flash('Medication deleted successfully.', 'success')
        else:
            flash('Medication not found or unauthorized.', 'error')
        return redirect(url_for('medications'))
    
    @app.route('/edit_medication/<int:med_id>', methods=['GET','POST'])
    def edit_medication(med_id):
        med = Medications.query.filter_by(medication_id=med_id, patient_id=current_user.user_id).first()
        if request.method == 'GET':
        # Render the form with the current medication data
            return render_template('edit_medication.html', med=med)

        elif request.method == 'POST':
            # Extract form data
            name = request.form.get('medicineName')
            dosage = request.form.get('dosage')
            frequency = request.form.get('frequency')
            start_date = request.form.get('startDate')
            end_date = request.form.get('endDate')  # This is optional

            # Validate form data
            if not name or not dosage or not frequency or not start_date:
                flash('All fields are required!', 'danger')
                return render_template('edit_medication.html', med=med)

            # Convert start_date and end_date to datetime.date objects
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                if end_date:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
                return render_template('edit_medication.html', med=med)

            # Update the medication instance
            med.name = name
            med.dosage = dosage
            med.frequency = frequency
            med.start_date = start_date
            med.end_date = end_date

            # Commit the changes to the database
            try:
                db.session.commit()
                flash('Medication updated successfully!', 'success')
                return redirect(url_for('medications'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while updating the medication. Please try again.', 'danger')
                app.logger.error(f'Error updating medication: {e}')
                return redirect(url_for('add_medication'))

            
