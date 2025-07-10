# 🏥 MamaCare Healthcare Management System

[![GitHub stars](https://img.shields.io/github/stars/aluzay1/mamacare)](https://github.com/aluzay1/mamacare/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/aluzay1/mamacare)](https://github.com/aluzay1/mamacare/network)
[![GitHub issues](https://img.shields.io/github/issues/aluzay1/mamacare)](https://github.com/aluzay1/mamacare/issues)
[![GitHub license](https://img.shields.io/github/license/aluzay1/mamacare)](https://github.com/aluzay1/mamacare/blob/main/LICENSE)
 

## For Quick Testing of the front-end, use this link https://verdant-gumdrop-61281b.netlify.app/


> **A comprehensive healthcare management system designed to connect patients with healthcare providers, with a specific focus on maternal and child healthcare services in Sierra Leone.**

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Team Members](#team-members)
- [Recent Updates](#recent-updates)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Installation Guide](#installation-guide)
- [System Architecture](#system-architecture)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Security Features](#security-features)
- [Deployment Guide](#deployment-guide)
- [Development Guide](#development-guide)
- [Contributing](#contributing)
- [Support](#support)
- [License](#license)

## 🎯 Project Overview

MamaCare is a revolutionary healthcare management system specifically designed for Sierra Leone's healthcare infrastructure. The system provides a centralized platform for managing hospitals, pharmacies, healthcare professionals, and patient records, with a strong emphasis on maternal and child healthcare services.

### 🌟 Mission
To improve healthcare accessibility and quality in Sierra Leone by providing a comprehensive digital platform that connects patients with healthcare providers, streamlines medical record management, and enhances healthcare service delivery.

### 🎯 Vision
To become the leading healthcare management platform in Sierra Leone, ensuring every citizen has access to quality healthcare services through innovative technology solutions.

## 👥 Team Members
1. Alusine Kuyateh
2. Ishaka Kargbo
3. Sylvia Harding
4. Sonia Goba
5. Abdul Salim Gani
## 🚀 Recent Updates


### **Previous Updates**
- **v2.0.0**: FHIR integration, PIN-based authentication, comprehensive admin dashboard
- **v1.5.0**: Hospital and pharmacy management systems
- **v1.0.0**: Initial release with basic patient management

## ✨ Key Features

### 🏥 **Hospital Management**
- Comprehensive hospital listings with detailed information
- Service categorization and filtering
- Real-time availability status
- Interactive maps and directions
- Hospital verification system

### 💊 **Pharmacy Management**
- 24/7 pharmacy locator
- Medication inventory tracking
- Prescription processing
- Service status indicators
- Contact information management

### 👨‍⚕️ **Healthcare Professional Management**
- Professional profiles with specializations
- Hospital affiliations
- Qualification verification
- Professional type categorization

### 📋 **Medical Records System**
- FHIR-compliant patient records
- Secure PIN-based access
- Comprehensive medical history
- Pregnancy tracking and calculations
- Prescription management

### 🔐 **Security & Authentication**
- PIN-based patient authentication
- JWT token authentication for healthcare providers
- Role-based access control
- Secure data encryption
- FHIR-compliant data security

### 📊 **Admin Dashboard**
- Comprehensive system management
- Real-time statistics and analytics
- User management interface
- Content verification system
- System monitoring tools

## 🛠 Technology Stack

### **Frontend**
- **HTML5** - Semantic markup and structure
- **CSS3** - Modern styling with gradients and animations
- **JavaScript (ES6+)** - Interactive functionality
- **Bootstrap 5.3.0** - Responsive framework
- **Bootstrap Icons 1.7.2** - Icon library
- **Chart.js** - Data visualization
- **ApexCharts** - Advanced charting
- **Moment.js** - Date handling

### **Backend**
- **Python 3.x** - Core programming language
- **Flask** - Web framework
- **SQLAlchemy** - Object-relational mapping
- **JWT** - Authentication tokens
- **Flask-Migrate** - Database migrations
- **FHIR Client** - Healthcare interoperability
- **Email Integration** - SMTP for notifications

### **Database**
- **PostgreSQL** - Primary database
- **PostgreSQL** - Primary database

### **DevOps & Infrastructure**
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Web server and reverse proxy
- **Git** - Version control
- **GitHub** - Code repository and collaboration

## 📦 Installation Guide

### **Prerequisites**
- Python 3.8+
- pip (Python package manager)
- Docker and Docker Compose
- Git
- PostgreSQL (for production)

### **Local Development Setup**

1. **Clone the repository:**
```bash
git clone https://github.com/aluzay1/mamacare.git
cd mamacare
```

2. **Set up Python virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install backend dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
# Create .env file with the following variables
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:postgres@db:5432/mamacare
SECRET_KEY=your-secret-key
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-email-password
```

5. **Initialize the database:**
```bash
flask db upgrade
python init_db.py
```

6. **Run the development server:**
```bash
flask run
```

### **Docker Setup**

1. **Build and run with Docker Compose:**
```bash
docker-compose up --build
```

2. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Admin Dashboard: http://localhost:3000/admin_dashboard.html

## 🚀 Running and Testing the Application

### **Starting the Application**

#### **Option 1: Local Development (Recommended for Development)**
```bash
# 1. Navigate to the project directory
cd mamacare

# 2. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Navigate to backend directory
cd backend

# 4. Set environment variables (create .env file)
echo "FLASK_APP=app.py" > .env
echo "FLASK_ENV=development" >> .env
echo "DATABASE_URL=sqlite:///mamacare.db" >> .env
echo "SECRET_KEY=your-secret-key-here" >> .env

# 5. Install dependencies
pip install -r requirements.txt

# 6. Initialize database
flask db upgrade
python init_db.py

# 7. Run the Flask application
flask run --host=0.0.0.0 --port=5000
```

#### **Option 2: Docker (Recommended for Production)**
```bash
# 1. Navigate to the project directory
cd mamacare

# 2. Build and start containers
docker-compose up --build -d

# 3. Check container status
docker-compose ps

# 4. View logs
docker-compose logs -f
```

### **Accessing the Application**

Once the application is running, you can access:

- **Main Application**: http://localhost:5000 or http://localhost:3000
- **Backend API**: http://localhost:5000/api/
- **Admin Dashboard**: http://localhost:5000/admin_dashboard.html
- **Medical Records**: http://localhost:5000/medical_records.html
- **Hospital Listings**: http://localhost:5000/hospitals.html
- **Pharmacy Listings**: http://localhost:5000/pharmacy.html
- **Healthcare Professionals**: http://localhost:5000/doctors.html

### **Testing the Application**

#### **1. Backend API Testing**

**Test the API endpoints using curl or Postman:**

```bash
# Test server health
curl http://localhost:5000/api/health

# Test hospitals endpoint
curl http://localhost:5000/api/hospitals

# Test pharmacies endpoint
curl http://localhost:5000/api/pharmacies

# Test healthcare professionals endpoint
curl http://localhost:5000/api/healthcare-providers
```

**Using the provided test script:**
```bash
cd backend
python test_api.py
```

#### **2. Frontend Testing**

**Manual Testing Checklist:**

1. **Homepage (index.html)**
   - [ ] Emergency button functionality
   - [ ] Navigation menu
   - [ ] Responsive design on different screen sizes

2. **Hospital Management (hospitals.html)**
   - [ ] Hospital cards display correctly
   - [ ] Search functionality works
   - [ ] Filter options work
   - [ ] Call and directions buttons work
   - [ ] Responsive layout (4 cards per row on large screens)

3. **Pharmacy Management (pharmacy.html)**
   - [ ] Pharmacy cards display correctly
   - [ ] 24/7 status indicators
   - [ ] Contact information
   - [ ] Call and directions functionality

4. **Healthcare Professionals (doctors.html)**
   - [ ] Professional cards display
   - [ ] Professional type categorization
   - [ ] Contact information
   - [ ] Image display

5. **Medical Records (medical_records.html)**
   - [ ] Patient registration
   - [ ] PIN generation and email
   - [ ] Profile editing
   - [ ] Pregnancy section (for female patients)
   - [ ] Medical measurements
   - [ ] Tabbed interface

6. **Admin Dashboard (admin_dashboard.html)**
   - [ ] Admin login
   - [ ] Hospital management (add, edit, verify)
   - [ ] Pharmacy management (add, edit, verify)
   - [ ] Healthcare professional management
   - [ ] Statistics display

#### **3. Database Testing**

**Test database operations:**
```bash
cd backend

# Test database connection
python -c "
from app import db
print('Database connection successful')
"

# Test data insertion
python add_test_data.py
```

#### **4. Authentication Testing**

**Test PIN-based authentication:**
```bash
# Register a new patient
curl -X POST http://localhost:5000/api/patient/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test Patient",
    "gender": "female",
    "date_of_birth": "1990-01-01"
  }'

# Login with PIN (use the PIN from the response above)
curl -X POST http://localhost:5000/api/patient/profile \
  -H "Content-Type: application/json" \
  -d '{"pin": "123456"}'
```

#### **5. File Upload Testing**

**Test image uploads:**
```bash
# Test hospital image upload (via admin dashboard)
# Navigate to admin dashboard and try uploading hospital images

# Test healthcare professional image upload
# Navigate to admin dashboard and try uploading professional images
```

### **Troubleshooting Common Issues**

#### **1. Database Connection Issues**
```bash
# Check if database is running
docker-compose ps

# Restart database container
docker-compose restart db

# Reset database
docker-compose down -v
docker-compose up --build
```

#### **2. Port Conflicts**
```bash
# Check if ports are in use
netstat -tulpn | grep :5000
netstat -tulpn | grep :3000

# Kill processes using the ports
sudo kill -9 <PID>
```

#### **3. Permission Issues**
```bash
# Fix file permissions
chmod -R 755 backend/uploads/
chmod -R 755 backend/static/uploads/
```

#### **4. Email Configuration Issues**
```bash
# Test email configuration
python -c "
import smtplib
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.starttls()
smtp.login('your-email@gmail.com', 'your-app-password')
print('Email configuration successful')
"
```

### **Performance Testing**

#### **Load Testing with Apache Bench**
```bash
# Test homepage performance
ab -n 100 -c 10 http://localhost:5000/

# Test API performance
ab -n 100 -c 10 http://localhost:5000/api/hospitals
```

#### **Database Performance**
```bash
# Test database query performance
python -c "
import time
from app import db
from models import Hospital

start_time = time.time()
hospitals = Hospital.query.all()
end_time = time.time()
print(f'Query took {end_time - start_time:.4f} seconds')
"
```

### **Security Testing**

#### **1. Authentication Security**
- Test PIN validation
- Test JWT token expiration
- Test role-based access control

#### **2. Input Validation**
- Test SQL injection prevention
- Test XSS prevention
- Test file upload security

#### **3. CORS Testing**
```bash
# Test CORS headers
curl -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -X OPTIONS http://localhost:5000/api/patient/register
```

### **Browser Testing**

**Test in different browsers:**
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile browsers (iOS Safari, Chrome Mobile)

**Test responsive design:**
- [ ] Desktop (1920x1080)
- [ ] Laptop (1366x768)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667)

### **Continuous Integration Testing**

**Run automated tests:**
```bash
# Run all tests
python -m pytest backend/tests/

# Run specific test categories
python -m pytest backend/tests/test_api.py
python -m pytest backend/tests/test_models.py
python -m pytest backend/tests/test_auth.py
```

### **Monitoring and Logs**

**Check application logs:**
```bash
# View Flask application logs
tail -f backend/app.log

# View Docker container logs
docker-compose logs -f app

# View database logs
docker-compose logs -f db
```

**Monitor system resources:**
```bash
# Check container resource usage
docker stats

# Check disk usage
df -h

# Check memory usage
free -h
```

### **Cleanup and Reset**

**Reset the entire system:**
```bash
# Stop all containers
docker-compose down

# Remove all data
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Rebuild from scratch
docker-compose up --build
```

This comprehensive testing guide ensures that all aspects of the MamaCare system are thoroughly tested and functioning correctly before deployment.

## 🏗 System Architecture

```
mamacare/
├── backend/                 # Backend Flask application
│   ├── app.py              # Main application file
│   ├── requirements.txt    # Python dependencies
│   ├── migrations/         # Database migrations
│   ├── static/            # Static files and uploads
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
│   ├── doctors.html       # Healthcare professional listings
│   ├── hospitals.html     # Hospital listings
│   ├── pharmacy.html      # Pharmacy listings
│   ├── styles.css         # Global styles
│   └── scripts.js         # JavaScript functions
├── migrations/            # Database migrations
├── Images/               # Image assets
├── docker-compose.yml    # Docker configuration
├── nginx.conf           # Nginx configuration
└── README.md           # Project documentation
```

## 📚 API Documentation

### **Authentication Endpoints**
```http
POST /api/admin/login
POST /api/healthcare-provider/login
POST /api/patient/login
```

### **Patient Management**
```http
POST /api/patient/register
POST /api/patient/profile
PUT /api/patient/profile
GET /api/patient/medical-records
POST /api/patient/medical-records
```

### **Healthcare Provider Management**
```http
POST /api/healthcare-provider/register
GET /api/healthcare-providers
POST /api/healthcare-providers
PUT /api/healthcare-providers/<id>
DELETE /api/healthcare-providers/<id>
```

### **Hospital Management**
```http
GET /api/hospitals
GET /api/admin/hospitals
POST /api/admin/hospitals
PUT /api/admin/hospitals/<id>
DELETE /api/admin/hospitals/<id>
```

### **Pharmacy Management**
```http
GET /api/pharmacies
GET /api/admin/pharmacies
POST /api/admin/pharmacies
PUT /api/admin/pharmacies/<id>
DELETE /api/admin/pharmacies/<id>
```

## 🗄️ Database Schema

### **Overview**
The MamaCare system uses PostgreSQL as its primary database with SQLAlchemy ORM for database operations. The schema is designed to support comprehensive healthcare management with FHIR compliance for interoperability.

### **Core Tables**

#### **1. Users Table (`user`)**
The central user management table supporting multiple user types with role-based access control. **Note: Admin users are stored in this same table with `role='admin'` - there is no separate admins table.**

```sql
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,  -- 'hospital', 'individual', 'admin'
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    pin VARCHAR(6) UNIQUE,  -- 6-digit PIN for patient access
    auth_token VARCHAR(255) UNIQUE,  -- Token for API authentication
    token_expiry TIMESTAMP,  -- Token expiration time
    
    -- Common fields
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address VARCHAR(200),
    
    -- FHIR-compliant fields
    given_name VARCHAR(100),
    family_name VARCHAR(100),
    gender VARCHAR(10),
    date_of_birth DATE,
    address_line VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    marital_status VARCHAR(50),
    language VARCHAR(10),
    nationality VARCHAR(100),
    blood_type VARCHAR(5),
    allergies TEXT,
    medications TEXT,
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(20),
    emergency_contact_relationship VARCHAR(50),
    fhir_id VARCHAR(100),
    
    -- Hospital-specific fields
    hospital_name VARCHAR(200),
    license_number VARCHAR(50),
    registration_document VARCHAR(255),
    
    -- Individual-specific fields
    medical_condition TEXT,
    medical_documents TEXT,  -- JSON string of document URLs
    
    -- Pregnancy-related fields
    pregnancy_status VARCHAR(20),  -- 'not_pregnant', 'pregnant', 'postpartum'
    previous_pregnancies INTEGER,
    lmp_date DATE,  -- Last Menstrual Period date
    due_date DATE,
    gestational_age INTEGER,
    multiple_pregnancy VARCHAR(20),  -- 'no', 'twins', 'triplets'
    risk_factors TEXT,  -- Store as JSON string
    blood_pressure VARCHAR(20),
    hemoglobin FLOAT,
    blood_sugar FLOAT,
    weight FLOAT,
    prenatal_vitamins TEXT,
    pregnancy_complications TEXT,
    emergency_hospital VARCHAR(200),
    birth_plan TEXT
);
```

#### **2. Medical Records Table (`medical_record`)**
Stores patient medical records with FHIR compliance.

```sql
CREATE TABLE medical_record (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id),
    date DATE NOT NULL,
    diagnosis VARCHAR(200) NOT NULL,
    treatment TEXT NOT NULL,
    medication TEXT,
    doctor VARCHAR(100) NOT NULL,
    hospital VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **3. Hospitals Table (`hospital`)**
Comprehensive hospital information management.

```sql
CREATE TABLE hospital (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    address VARCHAR(200) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    website VARCHAR(200),
    services TEXT,  -- Store services as a JSON string
    image_url VARCHAR(500),  -- Hospital image URL
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **4. Pharmacies Table (`pharmacy`)**
Pharmacy information and service management.

```sql
CREATE TABLE pharmacy (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    address VARCHAR(200) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    website VARCHAR(200),
    is_24_hours BOOLEAN DEFAULT FALSE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **5. Doctors Table (`doctor`)**
Healthcare professional profiles and specializations.

```sql
CREATE TABLE doctor (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    professional_type VARCHAR(50) NOT NULL DEFAULT 'Medical Doctor',
    specialization VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    hospital_affiliation VARCHAR(200) NOT NULL,
    address VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    website VARCHAR(200),
    image_url VARCHAR(255),
    is_verified BOOLEAN DEFAULT FALSE,
    qualifications TEXT,
    experience VARCHAR(100),
    pin VARCHAR(6) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **6. Healthcare Professionals Table (`healthcare_professional`)**
Extended healthcare professional management.

```sql
CREATE TABLE healthcare_professional (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    professional_type VARCHAR(50) NOT NULL,  -- e.g., Medical Doctor, Nurse, Midwife, etc.
    specialization VARCHAR(100) NOT NULL,
    hospital_affiliation VARCHAR(200) NOT NULL,
    address VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    website VARCHAR(200),
    image_url VARCHAR(255),
    is_verified BOOLEAN DEFAULT FALSE,
    qualifications TEXT,
    experience VARCHAR(100),
    pin VARCHAR(6) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **7. Referral Feedback Table (`referral_feedback`)**
Patient referral feedback and tracking system.

```sql
CREATE TABLE referral_feedback (
    id SERIAL PRIMARY KEY,
    patient_name VARCHAR(200) NOT NULL,
    referral_source VARCHAR(100) NOT NULL DEFAULT 'PresTrack',
    feedback_notes TEXT NOT NULL,
    doctor_id INTEGER REFERENCES "user"(id),  -- Can be null if doctor not logged in
    patient_id INTEGER REFERENCES "user"(id),  -- Reference to patient
    doctor_name VARCHAR(200),
    doctor_phone VARCHAR(20),
    doctor_affiliation VARCHAR(200),
    sms_sent BOOLEAN DEFAULT FALSE,
    sms_sent_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **User Roles and Access Control**

The system uses a role-based access control system where all users (including admins) are stored in the single `user` table. The `role` field determines user permissions and access levels:

#### **User Roles:**
- **`'admin'`** - System administrators with full access to all features
- **`'hospital'`** - Hospital users who can manage hospital data
- **`'individual'`** - Individual patients with access to medical records

#### **Role-Based Permissions:**
- **Admins**: Full system access, user verification, system management
- **Hospitals**: Hospital data management, patient care coordination
- **Individuals**: Medical record access, profile management, PIN-based authentication

### **Database Relationships**

#### **One-to-Many Relationships:**
- **User → Medical Records**: A patient can have multiple medical records

#### **Foreign Key Constraints:**
- `medical_record.user_id` → `user.id`
- `referral_feedback.doctor_id` → `user.id`
- `referral_feedback.patient_id` → `user.id`

### **Indexes and Performance**

#### **Primary Indexes:**
- All tables have primary key indexes on `id` columns
- Unique indexes on email fields across all user-related tables
- Unique indexes on license numbers for hospitals, pharmacies, and doctors
- Unique indexes on PIN fields for secure access

#### **Performance Optimizations:**
- Foreign key indexes for efficient joins
- Composite indexes on frequently queried fields
- Text search indexes for medical records and feedback
- Timestamp indexes for temporal queries

### **Data Integrity and Constraints**

#### **Check Constraints:**
- Email format validation
- Phone number format validation
- Amount validation (positive values)
- Date range validation for pregnancy-related fields
- Status field validation (enum-like constraints)

#### **Not Null Constraints:**
- Essential identification fields (name, email, phone)
- Required relationship fields (foreign keys)
- Critical business fields (amounts, dates, status)

### **FHIR Compliance**

The database schema is designed to support FHIR (Fast Healthcare Interoperability Resources) compliance:

#### **FHIR Mappings:**
- **Patient Resource**: Mapped to `user` table with FHIR-compliant fields
- **Observation Resource**: Mapped to `medical_record` table
- **MedicationRequest Resource**: Supported through medication fields
- **Organization Resource**: Mapped to `hospital` and `pharmacy` tables
- **Practitioner Resource**: Mapped to `doctor` and `healthcare_professional` tables

#### **FHIR Identifiers:**
- `fhir_id` field in user table for external FHIR system integration
- Standardized field naming conventions
- Extensible JSON fields for FHIR extensions

### **Security Features**

#### **Data Protection:**
- Password hashing using Werkzeug security
- JWT token authentication
- PIN-based access for patients
- Role-based access control
- Encrypted sensitive data fields

#### **Audit Trail:**
- `created_at` and `updated_at` timestamps on all tables
- User activity tracking through foreign key relationships
- Medical record access logging

### **Migration Management**

The database uses Flask-Migrate for schema versioning:

#### **Migration Files:**
- `add_doctor_fields_to_referral_feedback.py`: Added doctor-specific fields
- `add_services_to_hospital.py`: Added services JSON field to hospitals
- `add_image_url_to_hospital.py`: Added image URL support for hospitals

#### **Migration Commands:**
```bash
# Initialize migrations
flask db init

# Create new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade
```

### **Backup and Recovery**

#### **Backup Strategy:**
- Automated daily backups using PostgreSQL pg_dump
- Point-in-time recovery capabilities
- Encrypted backup storage
- Cross-region backup replication

#### **Recovery Procedures:**
- Full database restore procedures
- Incremental backup restoration
- Data consistency verification
- Rollback procedures for failed migrations

## 🔒 Security Features

- **PIN-based Authentication** - Secure patient access
- **JWT Token Authentication** - Provider and admin access
- **Role-based Access Control** - Different permission levels
- **FHIR Compliance** - Healthcare data standards
- **Data Encryption** - Secure data transmission
- **Input Validation** - XSS and SQL injection prevention
- **CORS Protection** - Cross-origin request security

## 🚀 Deployment Guide

### **Production Deployment**
1. Set up production environment variables
2. Configure PostgreSQL database
3. Set up SSL certificates
4. Configure Nginx reverse proxy
5. Deploy using Docker Compose
6. Run database migrations
7. Initialize the system with admin user

### **Environment Variables**
```bash
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-production-secret-key
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-email-password
```

## 👨‍💻 Development Guide

### **Code Standards**
- Follow PEP 8 style guide for Python
- Use semantic HTML5 markup
- Implement responsive CSS design
- Write clean, documented JavaScript
- Follow Git commit conventions

### **Testing**
- Unit tests for API endpoints
- Integration tests for FHIR resources
- Security testing and validation
- Performance testing
- User acceptance testing


### **Development Setup**
See the [Installation Guide](#installation-guide) for detailed setup instructions.



## 🙏 Acknowledgments

- **Sierra Leone Ministry of Health** - For healthcare domain expertise
- **FHIR Community** - For healthcare interoperability standards
- **Open Source Community** - For the amazing tools and libraries
- **Healthcare Providers** - For valuable feedback and requirements

---

**Made with ❤️ for Sierra Leone's Healthcare System**

*Last updated: December 2024* 