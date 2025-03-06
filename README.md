# Student-Teacher Booking Appointment System

## Project Overview
The **Student-Teacher Booking Appointment System** is a web-based platform that facilitates seamless scheduling between students and teachers. The system allows students to book appointments with teachers, send messages, and get updates on their bookings. Teachers can approve or decline requests, view scheduled meetings, and communicate with students. This project is built using **Flask** for the backend and **PostgreSQL** for local database storage.

## Technologies Used
- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** PostgreSQL

## Features
### Student Features
- Register and log in securely.
- Search for teachers based on subjects/departments.
- Book an appointment with an available teacher.
- View appointment status (pending, approved, canceled).
- Send messages to teachers.
- Receive notifications on appointment updates.

### Teacher Features
- Log in securely.
- View upcoming appointment requests.
- Approve or decline student appointments.
- Receive messages from students.
- Manage availability and schedule.

### Admin Features
- Add, update, or remove teacher profiles.
- Approve student registrations.
- View system logs for tracking activities.

## Installation Guide
### Prerequisites
- Python 3.x
- PostgreSQL
- Flask & required libraries
- Git (for version control)

### Steps to Run the Project
1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/student-teacher-booking.git
   cd student-teacher-booking
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate  # For Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Database**
   - Install PostgreSQL and create a database.
   - Update `config.py` with your database credentials.
   - Run migrations:
     ```bash
     flask db init
     flask db migrate
     flask db upgrade
     ```

5. **Run the Flask Application**
   ```bash
   flask run
   ```
   The app will be available at `http://127.0.0.1:5000/`

## Usage
- **Students**: Register, log in, search for teachers, and book appointments.
- **Teachers**: Approve or decline appointments and manage availability.
- **Admin**: Manage teachers and students, and monitor the system.

## Future Enhancements
- Email & SMS reminders for appointments.
- Google Calendar integration.
- Video call feature for remote appointments.

## Contributing
1. Fork the repository.
2. Create a feature branch.
3. Make your changes and commit them.
4. Open a pull request for review.

