#  Clothify — Online Clothing Shopping Platform

Clothify is a full-stack **Django-based e-commerce web application** for online clothing shopping.  
It allows users to browse products, manage carts, apply coupons, place orders, and authenticate using Google OAuth.

🔗 **Live Demo**: https://clothify-v8gz.onrender.com/
But Currently the live demo is under maintanence due to oauth issues it gonna resolved with in a short period of time

---

## Features

### User Features
- User authentication (Email & Google OAuth)
- Browse clothing products by **category & brand**
- Product search and filtering
- Add / remove products from cart
- Apply discount coupons
- View order history
- Responsive and modern UI

---

### Cart & Orders
- Cart quantity management
- Coupon-based discounts (percentage & flat)
- Order creation and tracking
- Order status management

---

### Admin Features
- Admin dashboard (Django Admin)
- Manage products, categories, and brands
- Manage coupons and coupon usage
- View customer orders
- User and role management

---

### Authentication
- Email-based login & signup
- Google OAuth using `django-allauth`
- Password reset via email
- Secure session handling

---

## Tech Stack

### Backend
- Python 3
- Django 5
- Django ORM
- django-allauth
- Gunicorn

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Database
- SQLite (used for demo)
- PostgreSQL ready (for production)

### Deployment
- GitHub

---

## Project Structure

del/
│
├── accounts/ # Authentication & custom user model
├── products/ # Products, categories, brands
├── orders/ # Cart and order management
├── coupons/ # Coupon and discount logic
├── templates/ # HTML templates
├── static/ # CSS, JS, images
│
├── delivery/
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│
├── manage.py
├── requirements.txt
 Local Setup

### 1️ Clone the repository
bash
git clone https://github.com/your-username/clothify.git
cd del
## 2 Create virtual environment
python -m venv env
#windows source env\Scripts\activate
#macos source env/bin/activate 
## 3 Install dependencies
pip install -r requirements.txt
## 4️ Run migrations
python manage.py migrate
## 5️ Create superuser
python manage.py createsuperuser
## 6️ Run the server
python manage.py runserver
Open:
http://127.0.0.1:8000/

Google OAuth Setup
1.Create OAuth credentials in Google Cloud Console
2.Add redirect URLs:
http://127.0.0.1:8000/accounts/google/login/callback/
3.Add credentials in Django Admin → Social Applications

Author
Hemanth Naidu Marpuri
Backend Developer | Django | Python

🔗 GitHub: https://github.com/your-username
