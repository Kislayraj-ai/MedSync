# Medsync

[![Django](https://img.shields.io/badge/Django-4.x-green.svg)](https://www.djangoproject.com/)  
[![DRF](https://img.shields.io/badge/DRF-3.x-red.svg)](https://www.django-rest-framework.org/)  
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Medsync is a **Django + Django REST Framework (DRF)** application designed for **appointment scheduling and patient management**.  
It uses **PostgreSQL** for persistence and integrates **Calendar.js** for an interactive scheduling UI.  

---

## 🚀 Features

### 🔐 Authentication & User Management
- Secure authentication & role-based access  
- JWT-ready API authentication  

### 📅 Appointment Scheduling
- Interactive calendar powered by **Calendar.js**  
- Create, update, and cancel appointments  
- Real-time availability visualization  

### 📡 API Layer (DRF)
- RESTful APIs under `/api/`  
- Pagination, filtering, validation via serializers  
- Optimized querysets  

### 🗄 Database
- **PostgreSQL** with migrations & indexing  
- Scalable relational structure for clinics, patients, and appointments  

### 🏗 Project Structure
- Modular apps inside `apps/`  
- Dedicated `api/` layer for DRF  
- Configurable `config/` for settings, urls, asgi/wsgi  
- Organized static/media handling  

### 🚀 Deployment Ready
- Configured with **Whitenoise** for static files  
- **Procfile + Gunicorn** for production (Railway/Heroku/Render)  

---

## 📂 Project Structure

Medsync’s codebase follows a clean, modular architecture to ensure maintainability, scalability, and clear separation of concerns:

```bash
medsync/
├── apps/                  # Core Django apps
│   ├── authentication/    # User login, registration & role management
│   ├── patients/          # Patient record management
│   ├── clinics/           # Clinic-specific logic
│   ├── dashboards/        # Role-based dashboards (Admin, Doctor, etc.)
│   ├── tables/            # Table utilities & helpers
│   ├── ui/                # UI helper modules
│   └── ...
│
├── api/                   # Django REST Framework (DRF) API layer
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── config/                # Core Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── src/                   # Frontend assets (JS, CSS, Calendar.js)
├── templates/             # Django HTML templates
├── staticfiles/           # Collected static files (for production)
├── media/                 # Uploaded media files
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── Procfile               # Deployment process file (e.g., for Railway/Heroku)
└── runtime.txt            # Python runtime version
```

---

### 🛠 Tech Stack

- **Backend:** Django, Django REST Framework (DRF)  
- **Database:** PostgreSQL  
- **Frontend:** Calendar.js, HTML templates, CSS, JS , JQuery , Bootstrap
- **Static Handling:** Whitenoise  

---

### ⚙️ Setup & Installation

#### Clone the Repository
```bash
git clone https://github.com/your-username/medsync.git
cd medsync
```

#### Create Virtual Environment
#### Windows
python -m venv venv
venv\Scripts\activate

#### Mac/Linux
python -m venv venv
source venv/bin/activate

#### Install Requirements
```bash
pip install -r requirements.txt
```

#### Configure Environment Variables

##### Create a .env file in the project root:
```bash
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/medsync
```

#### Apply Migrations
```bash
python manage.py migrate
```

#### Run Development Server
```bash
python manage.py runserver
```

### 📡 API Endpoints

All endpoints are included in the Postman collection:  

** Export the file name in your postman **

```bash
medsync.postman_collection.json
```



#### 🖥 Frontend (Calendar.js)

Integrated Calendar.js for appointment booking
Supports date, time slot, and event selection
Fully synced with backend APIs for real-time availability


#### 🚀 Deployment

Collect static files:

python manage.py collectstatic --noinput
Run with Gunicorn:
gunicorn config.wsgi:application



#### 📌 Future Enhancements

Real-time appointment updates with Django Channels + Redis
Email/SMS notifications for reminders
Docker + CI/CD pipeline integration
Multi-clinic support with advanced analytics dashboard


#### 🤝 Contributing
Contributions are welcome!
Please open an issue or submit a pull request .



### 🔗 Connect with Me

💡 Crafted by Kislay Raj ✍️

🌐 Connect with me on:

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/kislay-raj-ai/) 

[![Instagram](https://img.shields.io/badge/Instagram-Follow-pink?style=for-the-badge&logo=instagram)](https://www.instagram.com/__kislayraj/#)