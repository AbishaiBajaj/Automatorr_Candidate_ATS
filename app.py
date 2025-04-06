from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, send_from_directory
import os
import uuid
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'automatorr_secret_key'

# In-memory storage for applicants
applicants = []

# Admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'automatorr123'

# Ensure upload folder exists
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'resumes')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get form data
            full_name = request.form['full_name']
            email = request.form['email']
            phone = request.form['phone']
            dob = request.form['dob']
            country = request.form['country']
            state = request.form['state']
            city = request.form['city']
            experience = request.form['experience']
            message = request.form.get('message', '')
            
            # Handle resume upload
            resume = request.files['resume']
            resume_filename = f"{uuid.uuid4()}_{resume.filename}"
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
            resume.save(resume_path)
            
            # Create applicant record
            applicant = {
                'id': str(uuid.uuid4()),
                'full_name': full_name,
                'email': email,
                'phone': phone,
                'dob': dob,
                'country': country,
                'state': state,
                'city': city,
                'experience': experience,
                'message': message,
                'resume_path': resume_filename,
                'status': 'Applied',
                'applied_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Add to in-memory storage
            applicants.append(applicant)
            
            return redirect(url_for('success'))
        except Exception as e:
            # Log the error and show a user-friendly message
            print(f"Error processing form: {str(e)}")
            return render_template('index.html', error=f"An error occurred: {str(e)}")
    
    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Invalid credentials. Please try again.'
    
    return render_template('admin_login.html', error=error)

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    
    return render_template('admin_dashboard.html', applicants=applicants)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/resumes/<filename>')
def get_resume(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.json
    applicant_id = data.get('id')
    new_status = data.get('status')
    
    for applicant in applicants:
        if applicant['id'] == applicant_id:
            applicant['status'] = new_status
            return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': 'Applicant not found'})

@app.route('/admin/bulk-action', methods=['POST'])
def bulk_action():
    if 'logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    data = request.json
    action = data.get('action')
    ids = data.get('ids', [])
    
    if not ids:
        return jsonify({'success': False, 'message': 'No candidates selected'})
    
    for applicant in applicants:
        if str(applicant['id']) in ids:
            if action == 'Delete':
                applicants.remove(applicant)
            elif action in ['Applied', 'Shortlisted', 'Hired']:
                applicant['status'] = action
    
    return jsonify({'success': True})

if __name__ == '__main__':
    # Add some sample applicants for testing
    if not applicants:
        # Create sample resume files for testing
        sample_files = ['sample_resume.pdf', 'sample_resume2.pdf', 'sample_resume3.pdf']
        for sample in sample_files:
            with open(os.path.join(app.config['UPLOAD_FOLDER'], sample), 'w') as f:
                f.write('This is a sample resume file for testing purposes.')
        
        applicants.append({
            'id': str(uuid.uuid4()),
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+1 123-456-7890',
            'dob': '1990-01-01',
            'country': 'United States',
            'state': 'California',
            'city': 'San Francisco',
            'experience': '5 years of experience in software development',
            'message': 'I am excited to join your team!',
            'resume_path': 'sample_resume.pdf',
            'status': 'Applied',
            'applied_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        applicants.append({
            'id': str(uuid.uuid4()),
            'full_name': 'Jane Smith',
            'email': 'jane@example.com',
            'phone': '+1 987-654-3210',
            'dob': '1992-05-15',
            'country': 'United Kingdom',
            'state': 'England',
            'city': 'London',
            'experience': '3 years of experience in UI/UX design',
            'message': 'Looking forward to contributing to your projects!',
            'resume_path': 'sample_resume2.pdf',
            'status': 'Shortlisted',
            'applied_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        applicants.append({
            'id': str(uuid.uuid4()),
            'full_name': 'Michael Johnson',
            'email': 'michael@example.com',
            'phone': '+1 555-123-4567',
            'dob': '1988-11-30',
            'country': 'Australia',
            'state': 'New South Wales',
            'city': 'Sydney',
            'experience': '7 years of experience in project management',
            'message': 'I believe I would be a great fit for your team!',
            'resume_path': 'sample_resume3.pdf',
            'status': 'Hired',
            'applied_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    app.run(debug=True, host='0.0.0.0')
