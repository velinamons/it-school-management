# IT School Management Platform

## Description
The IT School Management Platform is a Django-based web application designed to manage the enrollment and education process within an offline robotics school. It allows for efficient handling of users (students, teachers, and managers), courses, groups, and notifications, providing a structured environment for managing educational activities.

## Roles
- **Students**: Enroll in courses and participate in groups.
- **Teachers**: Facilitate education in designated groups.
- **Managers**: Oversee groups, manage users (adding/removing students and teachers), and control the education process (starting and finishing courses).

## Models
- **CustomUser**: Base user model for handling authentication.
- **Student**: Inherits from CustomUser, associated with multiple groups.
- **Teacher**: Inherits from CustomUser, associated with multiple groups.
- **Manager**: Inherits from CustomUser, with specific roles to manage groups and courses.
- **Filia**: Represents branches or locations of the school.
- **Course**: Represents educational courses offered.
- **Group**: Represents a cohort of students participating in a course.
- **StudentGroupMembership**: Handles the relationship between students and groups, including payment status.
- **Notification**: Tracks notifications related to user actions and updates.

## Features
- User authentication with custom user roles (students, teachers, managers).
- Course and group management (add, update, delete).
- Enrollment management (add/remove students and teachers from groups).
- Status management for education processes (start/finish education).
- Notification system for user actions.

## How to Start
* Note: If you have both Python 2 and 3 installed, use python3 instead of python.

1. Clone the repository:
   ```bash
   git clone https://github.com/velinamons/it-school-management.git

2. Navigate to the project directory:
   ```bash
   cd it-school-management
   
3. Activate venv:
* Windows:
  ```bash
   python -m venv venv
   source venv/Scripts/activate
   
* Unix-based (macOS, Linux):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   
5. Make migrations for the database:
   ```bash
   python manage.py makemigrations

6. Apply the migrations:
   ```bash
   python manage.py migrate
   
7. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   
8. Run the development server:
   ```bash
   python manage.py runserver

9. Create managers and teachers in the Django admin panel.
   * Note: Managers and teachers cannot register themselves; they can only log in after being created in the admin panel.
   