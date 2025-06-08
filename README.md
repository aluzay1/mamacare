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
MamaCare is a comprehensive healthcare management system designed to connect patients with healthcare providers, with a specific focus on maternal and child healthcare services. The system provides a centralized platform for managing hospitals, pharmacies, doctors, and patient records, with FHIR integration for healthcare interoperability.

### Key Features
- Hospital Management
- Pharmacy Management
- Doctor Management
- Patient Records with FHIR Integration
- Live Monitoring
- Chat System
- FHIR-compliant Medical Records
- Secure PIN-based Patient Access

## Project Structure
```
mamacare/
├── backend/                 # Backend Flask application
│   ├── app.py              # Main application file
│   ├── requirements.txt    # Python dependencies
│   ├── migrations/         # Database migrations
│   ├── static/            # Static files
│   ├── uploads/           # File uploads directory
│   ├── instance/          # Instance-specific files
│   ├── test_api.py        # API tests
│   ├── init_db.py         # Database initialization
│   └── Dockerfile         # Docker configuration
├── frontend/              # Frontend files
│   ├── index.html         # Main landing page
│   ├── admin_dashboard.html  # Admin interface
│   ├── medical_records.html  # Patient records
│   ├── medical_records_view.html  # Patient records view
│   ├── doctors.html       # Doctor listings
│   ├── hospitals.html     # Hospital listings
│   ├── pharmacy.html      # Pharmacy listings
│   ├── styles.css         # Global styles
│   └── scripts.js         # JavaScript functions
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
- FHIR Client (Healthcare Interoperability)

### Database
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
- PostgreSQL

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

4. Set up environment variables:
```bash
# Create .env file with the following variables
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:postgres@db:5432/mamacare
SECRET_KEY=your-secret-key
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-email-password
```

5. Initialize the database:
```bash
flask db upgrade
python init_db.py
```

6. Run the development server:
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
- Patient profiles with FHIR integration
- Medical history
- Prescription management
- FHIR-compliant data storage
- Secure PIN-based access

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

### 6. FHIR Integration
- FHIR Patient Resources
- FHIR Observation Resources
- FHIR MedicationRequest Resources
- Healthcare Interoperability
- Standardized Data Exchange

## API Documentation

### Authentication
```
POST /api/admin/login
- Purpose: Admin login
- Request Body: { email, password }
- Response: { token }
```

### Patient Management
```
POST /api/patient/register
- Purpose: Register new patient
- Request Body: { email, name, given_name, family_name, gender, date_of_birth, ... }
- Response: { pin, patient_id, fhir_id }

POST /api/patient/profile
- Purpose: Get patient profile
- Request Body: { pin }
- Response: { id, fhir_id, name, gender, ... }
```

### Medical Records
```
POST /api/patient/medical-records
- Purpose: Add medical record
- Request Body: { pin, date, diagnosis, treatment, ... }
- Response: { id, date, diagnosis, ... }

GET /api/patient/medical-records
- Purpose: Get medical records
- Query Params: { pin }
- Response: [{ id, date, diagnosis, ... }]
```

### Hospital Management
```
GET /api/admin/hospitals
POST /api/admin/hospitals
PUT /api/admin/hospitals/<id>
DELETE /api/admin/hospitals/<id>
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

### User
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    name VARCHAR(100) NOT NULL,
    given_name VARCHAR(100),
    family_name VARCHAR(100),
    gender VARCHAR(20),
    date_of_birth DATE,
    phone VARCHAR(20),
    address_line VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    blood_type VARCHAR(10),
    allergies TEXT,
    medications TEXT,
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(20),
    emergency_contact_relationship VARCHAR(50),
    marital_status VARCHAR(20),
    language VARCHAR(50),
    nationality VARCHAR(100),
    fhir_id VARCHAR(100) UNIQUE,
    pin VARCHAR(6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

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

### Medical Record
```sql
CREATE TABLE medical_record (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    date DATE NOT NULL,
    diagnosis TEXT NOT NULL,
    treatment TEXT,
    medications TEXT,
    notes TEXT,
    doctor_id INTEGER,
    hospital_id INTEGER,
    fhir_resource_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES user(id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(id),
    FOREIGN KEY (hospital_id) REFERENCES hospital(id)
);
```

### Admin
```sql
CREATE TABLE admin (
    id INTEGER PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Security Features
- PIN-based patient authentication
- JWT token authentication for admin
- FHIR-compliant data security
- Secure password hashing
- CORS protection
- Input validation
- SQL injection prevention
- XSS protection

## Deployment Guide
1. Set up production environment variables
2. Configure PostgreSQL database
3. Set up SSL certificates
4. Configure Nginx
5. Deploy using Docker Compose
6. Run database migrations
7. Initialize the system

## Development Guide
1. Follow PEP 8 style guide
2. Write unit tests for new features
3. Document API changes
4. Update database migrations
5. Test FHIR integration
6. Verify security measures

## Testing
- Unit tests for API endpoints
- Integration tests for FHIR resources
- Security testing
- Performance testing
- User acceptance testing

## Maintenance
- Regular database backups
- Log monitoring
- Security updates
- Performance optimization
- FHIR compliance checks

## Support
For support and issues:
- Email: support@mamacare.com
- GitHub Issues: [Create an issue](https://github.com/yourusername/mamacare/issues)

## License
This project is licensed under the MIT License - see the LICENSE file for details. 