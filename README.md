This repository contains a Django backend application for managing restaurant orders. It includes APIs for handling orders, products, and user authentication.

Prerequisites
Before running the application, ensure you have the following installed:

Python 3.x
PostgreSQL
pip (Python package installer)
Installation
Clone the repository:
git clone https://github.com/your-username/your-repository.git
cd your-repository
Setup Virtual Environment:
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
Install Dependencies:
pip install -r requirements.txt
Database Setup:

Create a PostgreSQL database.

Configure database settings in settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
Run Migrations:
python manage.py migrate
Create Superuser (Optional):
python manage.py createsuperuser
Run Development Server:
python manage.py runserver
The server will start at http://localhost:8000/.
APIs
Orders API: /api/orders/
Products API: /api/products/
Cart API: /api/cart/
Orders API: /api/orders/
Authentication API: /api/auth/
Configuration
Settings: Customize settings in settings.py such as ALLOWED_HOSTS, DEBUG, and other application-specific settings.
Deployment
For production deployment, it's recommended to use a proper web server like Nginx or Apache with Gunicorn or uWSGI. Ensure to set DEBUG = False and secure your application with appropriate security measures.
