from flask import render_template,request,redirect,url_for,jsonify,flash
from flask_login import login_user,logout_user,current_user,login_required
from models import Users,Medications,Pathologies,Pharmacies,Appointments,Medication_Reminders
from datetime import datetime
from functions import Load_Medicine_Data,MedicineAutocomplete
from difflib import get_close_matches
import re

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
    @login_required
    def add_medication():
        if request.method == 'GET':
            return render_template('add_medication.html')
        elif request.method == 'POST':
            # Extract form data for Medications
            name = request.form.get('medicineName')
            dosage = f"{request.form.get('dosage')} {request.form.get('unit')}"
            frequency = request.form.get('frequency')
            start_date = request.form.get('startDate')
            end_date = request.form.get('endDate')

            # Validate form data
            if not name or not dosage or not frequency or not start_date:
                flash('All fields are required!', 'danger')
                return redirect(url_for('add_medication'))

            # Convert dates
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                if end_date:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
                return redirect(url_for('add_medication'))

            # Create a new Medication instance
            new_medication = Medications(
                patient_id=current_user.user_id,
                name=name,
                dosage=dosage,
                frequency=frequency,
                start_date=start_date,
                end_date=end_date
            )

            # Add medication to the database
            try:
                db.session.add(new_medication)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while adding the medication. Please try again.', 'danger')
                return redirect(url_for('add_medication'))

            # Extract reminder times
            reminder_times = []                    
            for i in range(1, int(frequency) + 1):
                time_str = request.form.get(f'reminderTime_{i}')
                if time_str:
                    reminder_times.append(time_str)

            # Add reminders to the database
            try:
                for time_str in reminder_times:
                    time_obj = datetime.strptime(time_str, '%H:%M').time()
                    new_reminder = Medication_Reminders(
                        medication_id=new_medication.medication_id,
                        patient_id=current_user.user_id,
                        reminder_time=time_obj
                    )
                    db.session.add(new_reminder)
                db.session.commit()
                flash('Medication and reminders added successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while adding the reminders. Please try again.', 'danger')

            return redirect(url_for('medications'))
            
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
            # Split dosage into amount and unit
            dosage_parts = med.dosage.split() if med.dosage else []
            dosage = dosage_parts[0] if len(dosage_parts) >= 1 else ''
            unit = dosage_parts[1] if len(dosage_parts) >= 2 else ''
            return render_template('edit_medication.html', med=med, dosage=dosage,unit=unit)

        elif request.method == 'POST':
            # Extract form data
            name = request.form.get('medicineName')
            dosage = f"{request.form.get('dosage')} {request.form.get('unit')}" 
            frequency = request.form.get('frequency')
            start_date = request.form.get('startDate')
            end_date = request.form.get('endDate')  # This is optional

            # Validate form data
            if not name or not dosage or not frequency or not start_date:
                flash('All fields are required!', 'danger')
                print('All fields are required!', 'danger')
                return render_template('edit_medication.html', med=med)

            # Convert start_date and end_date to datetime.date objects
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                if end_date:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
                print('Invalid date format. Please use YYYY-MM-DD.', 'danger')
                return render_template('edit_medication.html', med=med)

            # Update the medication instance
            med.name = name
            med.dosage = dosage
            med.frequency = frequency
            med.start_date = start_date
            med.end_date = end_date

            # Update reminders
            # First, delete existing reminders for this medication
            Medication_Reminders.query.filter_by(medication_id=med.medication_id).delete()

            # Add new reminders
            for i in range(int(frequency)):
                reminder_time_str = request.form.get(f'reminderTime_{i + 1}')
                if reminder_time_str:
                    reminder_time = datetime.strptime(reminder_time_str, '%H:%M').time()
                    new_reminder = Medication_Reminders(
                        medication_id=med.medication_id,
                        patient_id=current_user.user_id,
                        reminder_time=reminder_time
                    )
                    db.session.add(new_reminder)

            # Commit the changes to the database
            try:
                db.session.commit()
                flash('Medication updated successfully!', 'success')
                return redirect(url_for('medications'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while updating the medication. Please try again.', 'danger')
                app.logger.error(f'Error updating medication: {e}')

            
        
    @app.route('/pathologies')
    def pathologies():
        pathologies = Pathologies.query.filter_by(patient_id=current_user.user_id).all()
        return render_template('pathologies.html', pathologies=pathologies)
    
    @app.route('/add_pathology', methods=['GET', 'POST'])
    @login_required
    def add_pathology():
        if request.method == 'GET':
            return render_template('add_pathology.html')
        elif request.method == 'POST':
            # Extract form data
            condition_name = request.form.get('conditionName')
            diagnosis_date = request.form.get('diagnosisDate')
            notes = request.form.get('notes')

            # Validate form data
            if not condition_name or not diagnosis_date:
                flash('Condition name and diagnosis date are required!', 'danger')
                return redirect(url_for('add_pathology'))

            # Convert diagnosis_date to datetime.date object
            try:
                diagnosis_date = datetime.strptime(diagnosis_date, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
                return redirect(url_for('add_pathology'))

            # Create a new Pathology instance
            new_pathology = Pathologies(
                patient_id=current_user.user_id,
                condition_name=condition_name,
                diagnosis_date=diagnosis_date,
                notes=notes
            )

            # Add to the database
            try:
                db.session.add(new_pathology)
                db.session.commit()
                flash('Pathology added successfully!', 'success')
                return redirect(url_for('pathologies'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while adding the pathology. Please try again.', 'danger')
                return redirect(url_for('add_pathology'))
            
    @app.route('/delete_pathology/<int:path_id>')
    @login_required
    def delete_pathology(path_id):
        path = Pathologies.query.filter_by(pathology_id=path_id, patient_id=current_user.user_id).first()
        if path:
            db.session.delete(path)
            db.session.commit()
            flash('Pathology deleted successfully.', 'success')
        else:
            flash('Pathology not found or unauthorized.', 'error')
        return redirect(url_for('pathologies'))
    
    @app.route('/edit_pathology/<int:path_id>', methods=['GET', 'POST'])
    @login_required
    def edit_pathology(path_id):
        path = Pathologies.query.filter_by(pathology_id=path_id, patient_id=current_user.user_id).first()
        
        if not path:
            flash('Pathology not found or unauthorized.', 'danger')
            return redirect(url_for('pathologies'))

        if request.method == 'GET':
            # Render the form with the current pathology data
            return render_template('edit_pathology.html', path=path)

        elif request.method == 'POST':
            # Extract form data
            condition_name = request.form.get('conditionName')
            diagnosis_date = request.form.get('diagnosisDate')
            notes = request.form.get('notes')

            # Validate form data
            if not condition_name or not diagnosis_date:
                flash('Condition Name and Diagnosis Date are required!', 'danger')
                return render_template('edit_pathology.html', path=path)

            # Convert diagnosis_date to datetime.date object
            try:
                diagnosis_date = datetime.strptime(diagnosis_date, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
                return render_template('edit_pathology.html', path=path)

            # Update the pathology instance
            path.condition_name = condition_name
            path.diagnosis_date = diagnosis_date
            path.notes = notes

            # Commit the changes to the database
            try:
                db.session.commit()
                flash('Pathology updated successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while updating the pathology. Please try again.', 'danger')
                app.logger.error(f'Error updating pathology: {e}')

            return redirect(url_for('pathologies'))

    @app.route('/pharmacies')
    @login_required
    def pharmacies():
        pharmacies = Pharmacies.query.filter_by(patient_id=current_user.user_id).all()
        return render_template('pharmacies.html', pharmacies=pharmacies)
    
    @app.route('/add_pharmacy', methods=['GET', 'POST'])
    @login_required
    def add_pharmacy():
        if request.method == 'GET':
            return render_template('add_pharmacy.html')
        elif request.method == 'POST':
            # Extract form data
            name = request.form.get('name')
            address = request.form.get('address')
            phone_number = request.form.get('phone_number')
            email = request.form.get('email')

            # Validate form data
            if not name:
                flash('Pharmacy name is required!', 'danger')
                return redirect(url_for('add_pharmacy'))

            # Create a new Pharmacy instance
            new_pharmacy = Pharmacies(
                patient_id=current_user.user_id,
                name=name,
                address=address,
                phone_number=phone_number,
                email=email
            )

            # Add to the database
            try:
                db.session.add(new_pharmacy)
                db.session.commit()
                flash('Pharmacy added successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while adding the pharmacy. Please try again.', 'danger')
                app.logger.error(f'Error adding pharmacy: {e}')

            return redirect(url_for('pharmacies'))
    
    @app.route('/edit_pharmacy/<int:pharmacy_id>', methods=['GET', 'POST'])
    @login_required
    def edit_pharmacy(pharmacy_id):
        pharmacy = Pharmacies.query.filter_by(pharmacy_id=pharmacy_id, patient_id=current_user.user_id).first()
        
        if not pharmacy:
            flash('Pharmacy not found or unauthorized.', 'danger')
            return redirect(url_for('pharmacies'))

        if request.method == 'GET':
            return render_template('edit_pharmacy.html', pharmacy=pharmacy)
        
        elif request.method == 'POST':
            name = request.form.get('name')
            address = request.form.get('address')
            phone_number = request.form.get('phone_number')
            email = request.form.get('email')

            if not name:
                flash('Pharmacy name is required!', 'danger')
                return render_template('edit_pharmacy.html', pharmacy=pharmacy)

            pharmacy.name = name
            pharmacy.address = address
            pharmacy.phone_number = phone_number
            pharmacy.email = email

            try:
                db.session.commit()
                flash('Pharmacy updated successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while updating the pharmacy. Please try again.', 'danger')
                app.logger.error(f'Error updating pharmacy: {e}')

            return redirect(url_for('pharmacies'))

    @app.route('/delete_pharmacy/<int:pharmacy_id>')
    @login_required
    def delete_pharmacy(pharmacy_id):
        pharmacy = Pharmacies.query.filter_by(pharmacy_id=pharmacy_id, patient_id=current_user.user_id).first()
        if pharmacy:
            db.session.delete(pharmacy)
            db.session.commit()
            flash('Pharmacy deleted successfully.', 'success')
        else:
            flash('Pharmacy not found or unauthorized.', 'error')
        return redirect(url_for('pharmacies'))
    
    @app.route('/appointments')
    @login_required
    def appointments():
        appointments = Appointments.query.filter_by(patient_id=current_user.user_id).all()
        return render_template('appointments.html', appointments=appointments)

    @app.route('/add_appointment', methods=['GET', 'POST'])
    @login_required
    def add_appointment():
        if request.method == 'GET':
            return render_template('add_appointment.html')
        elif request.method == 'POST':
            doctor_name = request.form.get('doctor_name')
            appointment_date_str = request.form.get('appointment_date')
            appointment_time_str = request.form.get('appointment_time')
            location = request.form.get('location')
            notes = request.form.get('notes')

            if not doctor_name or not appointment_date_str or not appointment_time_str:
                flash('Doctor name, date, and time are required!', 'danger')
                return redirect(url_for('add_appointment'))

            try:
                appointment_date = datetime.strptime(f"{appointment_date_str} {appointment_time_str}", '%Y-%m-%d %H:%M')
            except ValueError:
                flash('Invalid date/time format.', 'danger')
                return redirect(url_for('add_appointment'))

            new_appointment = Appointments(
                patient_id=current_user.user_id,
                doctor_name=doctor_name,
                appointment_date=appointment_date,
                location=location,
                notes=notes
            )

            try:
                db.session.add(new_appointment)
                db.session.commit()
                flash('Appointment added successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while adding the appointment. Please try again.', 'danger')

            return redirect(url_for('appointments'))

    @app.route('/edit_appointment/<int:appointment_id>', methods=['GET', 'POST'])
    @login_required
    def edit_appointment(appointment_id):
        appointment = Appointments.query.filter_by(appointment_id=appointment_id, patient_id=current_user.user_id).first()

        if not appointment:
            flash('Appointment not found or unauthorized.', 'danger')
            return redirect(url_for('appointments'))

        if request.method == 'GET':
            return render_template('edit_appointment.html', appointment=appointment)
        
        elif request.method == 'POST':
            doctor_name = request.form.get('doctor_name')
            appointment_date_str = request.form.get('appointment_date')
            appointment_time_str = request.form.get('appointment_time')
            location = request.form.get('location')
            notes = request.form.get('notes')

            if not doctor_name or not appointment_date_str or not appointment_time_str:
                flash('Doctor name, date, and time are required!', 'danger')
                return render_template('edit_appointment.html', appointment=appointment)

            try:
                appointment_date = datetime.strptime(f"{appointment_date_str} {appointment_time_str}", '%Y-%m-%d %H:%M')
            except ValueError:
                flash('Invalid date/time format.', 'danger')
                return render_template('edit_appointment.html', appointment=appointment)

            appointment.doctor_name = doctor_name
            appointment.appointment_date = appointment_date
            appointment.location = location
            appointment.notes = notes

            try:
                db.session.commit()
                flash('Appointment updated successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while updating the appointment. Please try again.', 'danger')

            return redirect(url_for('appointments'))

    @app.route('/delete_appointment/<int:appointment_id>')
    @login_required
    def delete_appointment(appointment_id):
        appointment = Appointments.query.filter_by(appointment_id=appointment_id, patient_id=current_user.user_id).first()
        if appointment:
            db.session.delete(appointment)
            db.session.commit()
            flash('Appointment deleted successfully.', 'success')
        else:
            flash('Appointment not found or unauthorized.', 'error')
        return redirect(url_for('appointments'))
    
    @app.route('/signout')
    @login_required
    def signout():
        logout_user()
        flash('You have been logged out successfully.', 'success')
        return redirect(url_for('index'))
    
    # Load medicines when the application starts
    medicines = Load_Medicine_Data.load_medicines()
    autocomplete_helper = MedicineAutocomplete.MedicineAutocomplete(medicines)

    @app.route('/autocomplete')
    def autocomplete():
        query = request.args.get('query', '').strip()
        results = autocomplete_helper.autocomplete(query)
        return jsonify(results)
