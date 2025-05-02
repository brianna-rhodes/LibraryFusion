# LibraryFusion

A comprehensive library management system built with Django, featuring user authentication, book management, borrowing system, and more.

## Features

- User Authentication (Students, Librarians, Managers)
- Book Management
- Borrowing System
- Book Reviews and Ratings
- Fine Management
- Search and Filtering
- Responsive Design
- Role-based Access Control

## Technologies Used

- Backend: Django 5.0
- Frontend: HTML, CSS, JavaScript, Bootstrap 5
- Database: SQLite (Development), PostgreSQL (Production)
- Authentication: Django's built-in authentication system
- Form Handling: django-crispy-forms
- Static Files: WhiteNoise
- Deployment: Heroku/PythonAnywhere (Optional)

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd library
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
library/
├── account/          # User authentication and profiles
├── books/           # Book management
├── librarians/      # Librarian-specific features
├── managers/        # Manager-specific features
├── reviews/         # Book reviews and ratings
├── static/          # Static files (CSS, JS, images)
├── templates/       # HTML templates
└── media/           # User-uploaded files
```

## User Roles

1. **Students**
   - Browse and search books
   - Borrow books
   - Write reviews
   - View borrowing history
   - Pay fines

2. **Librarians**
   - Manage books
   - Handle book issues and returns
   - Manage fines
   - View reports

3. **Managers**
   - All librarian privileges
   - Manage users
   - Generate reports
   - System configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
