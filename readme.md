# django_website_blog

This Django project is a web application for managing blog posts and user profiles.

## Overview

The project consists of two main apps:

1. **Blog App:**
   - Manages blog posts.
   - Allows users to create, edit, and delete blog posts.
   - Supports categorization and tagging of blog posts.

2. **Users App:**
   - Handles user registration and authentication.
   - Allows users to update their profiles, including profile images.

## Installation

```bash
git clone https://github.com/your-username/bms-django-website.git
cd bms-django-website

python -m venv venv
source venv/bin/activate   # On Linux/macOS, on Windows use .\venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your web browser to access the application.

## Usage

**Blog App:**
- Create, edit, and delete blog posts.
- Explore categorized and tagged blog posts.

**Users App:**
- Register and log in.
- Update user profiles, including profile images.

## Tests

```bash
python manage.py test
```
