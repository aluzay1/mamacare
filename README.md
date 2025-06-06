# MamaCare Healthcare Management System

## Table of Contents
1. [System Overview](#system-overview)
2. [Project Structure](#project-structure)
3. [Technology Stack](#technology-stack)
4. [Installation Guide](#installation-guide)
5. [System Components](#system-components)
6. [API Documentation](#api-documentation)
7. [Database Schema](#database-schema)
8. [Security Features](#security-features)
9. [Deployment Guide](#deployment-guide)
10. [Development Guide](#development-guide)
11. [Testing](#testing)
12. [Maintenance](#maintenance)

## System Overview
MamaCare is a comprehensive healthcare management system designed to connect patients with healthcare providers, with a specific focus on maternal and child healthcare services. The system provides a centralized platform for managing hospitals, pharmacies, doctors, and patient records.

### Key Features
- Hospital Management
- Pharmacy Management
- Doctor Management
- Patient Records
- Pregnancy Tracking
- Live Monitoring
- Chat System
- Campaign Management

## Project Structure
```
mamacare/
├── backend/                 # Backend Flask application
│   ├── app.py              # Main application file
│   ├── app_new.py          # New application features
│   ├── requirements.txt    # Python dependencies
│   ├── migrations/         # Database migrations
│   ├── static/            # Static files
│   ├── uploads/           # File uploads directory
│   ├── instance/          # Instance-specific files
│   ├── test_api.py        # API tests
│   ├── init_db.py         # Database initialization
│   ├── update_db.py       # Database updates
│   ├── add_test_data.py   # Test data generation
│   └── Dockerfile         # Docker configuration
├── frontend/              # Frontend files
│   ├── index.html         # Main landing page
│   ├── admin_dashboard.html  # Admin interface
│   ├── medical_records.html  # Patient records
│   ├── doctors.html       # Doctor listings
│   ├── hospitals.html     # Hospital listings
│   ├── pharmacy.html      # Pharmacy listings
│   ├── hospital_details.html # Hospital details page
│   ├── pregnancy_tracker.html # Pregnancy tracking
│   ├── live_monitor.html  # Live monitoring
│   ├── chat.html          # Chat system
│   ├── campaign_management.html # Campaign management
│   ├── styles.css         # Global styles
│   ├── scripts.js         # JavaScript functions
│   └── chart.js           # Data visualization
├── migrations/            # Database migrations
├── Images/               # Image assets
├── docker-compose.yml    # Docker configuration
└── nginx.conf           # Nginx configuration
```

## Technology Stack

### Frontend
- HTML5
- CSS3
- JavaScript (ES6+)
- Bootstrap 5.3.0
- Bootstrap Icons 1.7.2
- Chart.js for data visualization

### Backend
- Python 3.x
- Flask (Web Framework)
- SQLAlchemy (ORM)
- JWT Authentication
- Flask-Migrate (Database Migrations)

### Database
- SQLite (Development)
- PostgreSQL (Production)

### DevOps
- Docker
- Nginx
- Git

## Installation Guide

### Prerequisites
- Python 3.x
- pip (Python package manager)
- Docker and Docker Compose (for containerization)
- Git

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mamacare.git
cd mamacare
```

2. Set up Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python init_db.py
python add_test_data.py  # Optional: Add test data
```

5. Run the development server:
```bash
flask run
```

### Docker Setup

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

## System Components

### 1. Admin Dashboard
- Hospital management
- Pharmacy management
- Doctor management
- User management
- System statistics

### 2. Medical Records
- Patient profiles
- Medical history
- Pregnancy tracking
- Prescription management

### 3. Hospital Management
- Hospital listings
- Service details
- Doctor affiliations
- Patient records
- Detailed hospital information

### 4. Pharmacy Management
- Pharmacy listings
- Medication inventory
- Prescription processing
- 24/7 service status

### 5. Doctor Management
- Doctor profiles
- Specializations
- Hospital affiliations
- Patient assignments

### 6. Pregnancy Tracker
- Due date calculator
- Appointment scheduling
- Health monitoring
- Progress tracking

### 7. Live Monitor
- Real-time health monitoring
- Emergency alerts
- Vital signs tracking
- Medical history access

### 8. Chat System
- Patient-doctor communication
- Appointment scheduling
- Medical advice
- Emergency support

### 9. Campaign Management
- Health awareness campaigns
- Event scheduling
- Participant management
- Resource allocation

## API Documentation

### Authentication
```
POST /api/admin/login
- Purpose: Admin login
- Request Body: { email, password }
- Response: { token }
```

### Hospital Management
```
GET /api/admin/hospitals
POST /api/admin/hospitals
PUT /api/admin/hospitals/<id>
DELETE /api/admin/hospitals/<id>
GET /api/hospitals/<id>  # Get detailed hospital information
```

### Pharmacy Management
```
GET /api/admin/pharmacies
POST /api/admin/pharmacies
PUT /api/admin/pharmacies/<id>
DELETE /api/admin/pharmacies/<id>
```

### Doctor Management
```
GET /api/admin/doctors
POST /api/admin/doctors
PUT /api/admin/doctors/<id>
DELETE /api/admin/doctors/<id>
```

## Database Schema

### Hospital
```sql
CREATE TABLE hospital (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address VARCHAR(200) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    website VARCHAR(200),
    directions TEXT,
    services TEXT,
    image VARCHAR(200),
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Pharmacy
```sql
CREATE TABLE pharmacy (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address VARCHAR(200) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    website VARCHAR(200),
    directions TEXT,
    is_24_hours BOOLEAN DEFAULT FALSE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Doctor
```sql
CREATE TABLE doctor (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    hospital_affiliation VARCHAR(100) NOT NULL,
    qualifications TEXT,
    experience VARCHAR(50),
    image VARCHAR(200),
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Security Features

### Authentication
- JWT-based authentication
- Secure token storage
- Password hashing
- Session management

### Data Protection
- Input validation
- SQL injection prevention
- XSS protection
- CSRF protection

### File Security
- Secure file uploads
- File type validation
- Size restrictions
- Secure storage

## Deployment Guide

### Production Requirements
- Python 3.x
- PostgreSQL
- Nginx
- SSL certificate
- Domain name

### Deployment Steps
1. Set up production server
2. Configure Nginx
3. Set up SSL
4. Configure environment variables
5. Initialize database
6. Deploy application
7. Set up monitoring

### Environment Variables
```
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost/mamacare
UPLOAD_FOLDER=/path/to/uploads
```

## Development Guide

### Code Style
- Follow PEP 8 for Python
- Use ESLint for JavaScript
- Follow Bootstrap guidelines for CSS

### Git Workflow
1. Create feature branch
2. Make changes
3. Write tests
4. Create pull request
5. Code review
6. Merge to main

### Testing
- Unit tests (test_api.py)
- Integration tests
- API tests
- Frontend tests

## Maintenance

### Regular Tasks
- Database backups
- Log rotation
- Security updates
- Performance monitoring

### Monitoring
- Error logging (app.log)
- User activity
- System health
- Resource usage

### Backup Procedures
- Daily database backups
- Weekly file backups
- Monthly full backups

## Support
For support and issues:
- Email: support@mamacare.com
- GitHub Issues: [Create an issue](https://github.com/yourusername/mamacare/issues)

## License
This project is licensed under the MIT License - see the LICENSE file for details. 