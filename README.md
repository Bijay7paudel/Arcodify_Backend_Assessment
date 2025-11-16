# FastAPI JWT Authentication Project

A FastAPI application with JWT authentication, user management, and post creation features.

## 🚀 **Features**

- ✅ **JWT Authentication** - Access and refresh tokens
- ✅ **User Management** - Registration, login, profile management
- ✅ **Role-Based Access Control** - Admin and regular user roles
- ✅ **Post Management** - Create and manage posts
- ✅ **Admin Dashboard** - User management for administrators
- ✅ **Database Migrations** - Alembic for database version control
- ✅ **Async Operations** - Full async/await support with SQLAlchemy
- ✅ **Input Validation** - Pydantic schemas for data validation
- ✅ **API Documentation** - Auto-generated with Swagger UI
- ✅ **Background Tasks** - Celery used for sending welcome emails and other async tasks


## 📋 Prerequisites

- Python 3.8+
- pip 
- SQLite (default) or PostgreSQL/MySQL

## 🛠️ Installation

### 1. Clone the repository

```bash
cd fastapi-jwt-project
git clone https://github.com/Bijay7paudel/Arcodify_Backend_Assessment.git
```

### 2. Create virtual environment

```bash
python -m venv myvenv

# On Windows
myvenv\Scripts\activate

# On macOS/Linux
source myvenv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=sqlite+aiosqlite:///./tes.db

# Security (Generate a secure key: openssl rand -hex 32)
SECRET_KEY=your-secret-key-change-in-production-use-openssl-rand-hex-32
ALGORITHM=HS256

### 5. Initialize database

```bash
# Create tables
python scripts/init_db.py

# Create admin user
python scripts/create_admin.py
```

### 6. Run the application

```bash
# Development mode (with auto-reload)
uvicorn app.main:app --reload --port 8000

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs

## 📁 Project Structure

fastapi-jwt-project/
├── alembic/
│   ├── versions/
│   │      
│   ├── env.py
│   ├── README
│   └── script.py.mako
│
├── routers/
│   ├── __init__.py
│   ├── admin.py          # Admin endpoints (list users, deactivate)
│   ├── auth.py           # Authentication (register, login)
│   ├── posts.py          # Post endpoints (create, list, get)
│   └── profile.py        # User profile endpoint
│
├── .env                  # Environment variables
├── alembic.ini           # Alembic configuration
├── celery_worker.py      # Background tasks (Celery)
├── create_admin.py       # Script to create admin user
├── create_tables.py      # Script to create database table
├── crud.py               # User CRUD operations
├── database.py           # Database connection and session
├── dependencies.py       # Auth dependencies (get_current_user, get_current_admin)
├── main.py               # FastAPI application entry point
├── models.py             # SQLAlchemy models (User, Post)
├── requirements.txt      # Python dependencies
├── schemas.py            # Pydantic schemas (User, Token)
├── schemas_post.py       # Pydantic schemas for posts
├── security.py           # JWT and password hashing
└── services_post.py      # Post service functions (fetch, search, paginate)

web framework
- **Uvicorn** - ASGI server
- **SQLAlchemy** - SQL toolkit and ORM
- **Alembic** - Database migrations
- **python-jose** - JWT encoding/decoding
- **passlib** - Password hashing
- **pydantic** - Data validation
- **aiosqlite** - Async SQLite driver

**END**
