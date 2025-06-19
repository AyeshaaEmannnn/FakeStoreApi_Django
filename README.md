# FakeStoreAPI Clone (Django)

This is a Django-based clone of the FakeStoreAPI. It provides REST APIs for managing products, users, carts, and orders.

## Features

- Product listing and detail APIs
- Cart creation and updates
- User registration and login
- Order creation


## Installation

1. Clone the repository  
2. Create a virtual environment  
3. Install dependencies  
4. Run migrations  
5. Start the server

```bash
git clone https://github.com/AyeshaaEmannnn/FakeStoreApi_Django.git
cd FakeStoreApi_Django
python -m venv env
env\Scripts\activate  # For Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver