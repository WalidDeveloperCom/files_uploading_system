# Files Uploading System with aamarPay Integration

A Django-based system where users can:
- Register & log in
- Pay ৳100 via aamarPay (sandbox)
- Upload `.txt` or `.docx` files **only after payment**
- Have files processed asynchronously via Celery to count words
- View payment history & activity logs
- Access a Bootstrap-based dashboard

## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/files_uploading_system.git
cd files_uploading_system
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Start Redis (for Celery)
```bash
redis-server
```

### 7. Start Celery Worker
```bash
celery -A files_uploading_system worker -l info
```

### 8. Run Django Server
```bash
python manage.py runserver
```

## Usage
- Register: http://localhost:8000/accounts/register/
- Login: http://localhost:8000/accounts/login/
- Dashboard: http://localhost:8000/dashboard/

## API Endpoints
- POST /api/initiate-payment/  (auth required)
- GET /api/payment/success/   (gateway callback)
- GET /api/transactions/      (auth required)
- POST /api/upload/           (auth required)
- GET /api/files/             (auth required)
- GET /api/activity/          (auth required)

## Testing aamarPay Sandbox
- Store ID: aamarpaytest
- Signature Key: dbb74894e82415a2f7ff0ec3a97e4183
- Endpoint: https://sandbox.aamarpay.com/jsonpost.php

## License
MIT License
