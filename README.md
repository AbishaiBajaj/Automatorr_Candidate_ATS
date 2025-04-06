# AUTOMATORR - Project Phase 4

An Automated Resume System for managing job applications with a candidate application form and an admin dashboard.

## Features

### Candidate Application Form
- Validation for required fields with error messages
- Shaking animations for empty required fields
- Error messages fade out after 3 seconds
- Mandatory fields indicated with a red asterisk (*)
- Fields include: Full Name, Email, Phone Number, Date of Birth, Country, State/Province, City, Experience, Resume, and optional message

### Admin Dashboard
- Drag-and-drop functionality for moving candidates between statuses
- Selection mode with blue ticks for selecting candidates
- Bulk actions: Move to Applied, Shortlist, Hire, and Delete
- Copy email button with tooltip notification
- Contact button with email template
- View resume functionality
- Real-time column count updates
- Confirmation modal for delete actions
- Advanced search functionality with text highlighting

## File Structure

```
AUTOMATORR/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── resumes/               # Directory for uploaded resumes
└── templates/
    ├── admin_dashboard.html  # Admin interface
    ├── admin_login.html      # Admin login page
    ├── index.html            # Candidate application form
    └── success.html          # Success page after form submission
```

## Main File Paths

- Candidate Application Form: http://localhost:5000/
- Admin Dashboard: http://localhost:5000/admin

## Sharing the Project

To share this project with someone, they would need:

1. All the files in the project directory:
   - app.py
   - requirements.txt
   - templates/ directory with all HTML files
   - resumes/ directory (can be empty, will be created automatically)

2. Python installed on their computer (version 3.6 or higher)

3. The required Python packages:
   - They can install these by running: `pip install -r requirements.txt`

4. Instructions to run the application:
   - Navigate to the project directory in a terminal/command prompt
   - Run the command: `python app.py`
   - Open a web browser and go to http://localhost:5000/
   - For the admin dashboard, go to http://localhost:5000/admin
   - Default login credentials: username: admin, password: password123

## Notes

- The application uses in-memory storage, so data will be lost when the server is restarted
- Uploaded resumes are stored in the 'resumes' directory
- The application runs on port 5000 by default
