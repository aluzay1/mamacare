# MamaCare Healthcare Management System - Complete System Documentation

## Executive Summary

MamaCare is a comprehensive healthcare management system specifically designed for Sierra Leone's healthcare infrastructure. The system provides a centralized platform for managing hospitals, pharmacies, healthcare professionals, and patient records, with a strong emphasis on maternal and child healthcare services.

**Mission**: To improve healthcare accessibility and quality in Sierra Leone by providing a comprehensive digital platform that connects patients with healthcare providers, streamlines medical record management, and enhances healthcare service delivery.

**Vision**: To become the leading healthcare management platform in Sierra Leone, ensuring every citizen has access to quality healthcare services through innovative technology solutions.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Team Information](#team-information)
3. [Key Features](#key-features)
4. [Technology Architecture](#technology-architecture)
5. [System Components](#system-components)
6. [Database Design](#database-design)
7. [API Documentation](#api-documentation)
8. [Security Features](#security-features)
9. [User Interfaces](#user-interfaces)
10. [Deployment Information](#deployment-information)
11. [Testing and Quality Assurance](#testing-and-quality-assurance)
12. [Maintenance and Support](#maintenance-and-support)

---

## System Overview

### Purpose and Scope
MamaCare addresses the critical need for digital healthcare management in Sierra Leone by providing:
- **Patient Management**: Secure, FHIR-compliant patient records with PIN-based authentication
- **Provider Management**: Comprehensive hospital, pharmacy, and healthcare professional directories
- **Administrative Tools**: Full-featured admin dashboard for system management
- **Mobile Accessibility**: Responsive design for mobile and tablet access
- **Data Interoperability**: FHIR integration for healthcare data standards compliance

### Target Users
- **Patients**: Access medical records, find healthcare providers
- **Healthcare Providers**: Manage patient data, access medical records
- **Administrators**: System management, user verification, content moderation
- **Hospitals & Pharmacies**: Profile management, service listings

---

## Team Information

### Development Team
1. **Alusine Kuyateh** - Lead Developer & Project Manager
2. **Ishaka Kargbo** - Backend Development & Database Design
3. **Sylvia Harding** - Frontend Development & UI/UX Design
4. **Sonia Goba** - System Architecture & Security
5. **Abdul Salim Gani** - Testing & Quality Assurance

### Project Timeline
- **v1.0.0**: Initial release with basic patient management
- **v1.5.0**: Hospital and pharmacy management systems
- **v2.0.0**: FHIR integration, PIN-based authentication, comprehensive admin dashboard
- **Current**: Enhanced responsive design, mobile optimization, advanced features

---

## Key Features

### 🏥 Hospital Management System
- **Comprehensive Listings**: Detailed hospital information with services, contact details, and locations
- **Service Categorization**: Filter hospitals by specialty and available services
- **Real-time Status**: Availability indicators and operational hours
- **Interactive Maps**: Location services with directions and contact integration
- **Verification System**: Admin-verified hospital profiles for reliability

### 💊 Pharmacy Management System
- **24/7 Locator**: Find pharmacies with round-the-clock availability
- **Inventory Tracking**: Medication availability and prescription processing
- **Service Status**: Real-time operational status indicators
- **Contact Management**: Direct phone and email integration
- **Geographic Filtering**: Location-based pharmacy search

### 👨‍⚕️ Healthcare Professional Management
- **Professional Profiles**: Comprehensive profiles with specializations and qualifications
- **Hospital Affiliations**: Professional relationships with healthcare facilities
- **Verification System**: Admin-verified professional credentials
- **Categorization**: Professional type classification (Doctors, Nurses, Midwives, etc.)
- **Contact Integration**: Direct communication channels

### 📋 Medical Records System
- **FHIR Compliance**: International healthcare data standards
- **PIN-based Security**: 6-digit PIN authentication for patient access
- **Comprehensive History**: Complete medical record management
- **Pregnancy Tracking**: Specialized maternal health features
- **Prescription Management**: Medication tracking and management
- **Data Export**: PDF generation and CSV export capabilities

### 🔐 Security & Authentication
- **Multi-level Authentication**: PIN-based for patients, JWT for providers
- **Role-based Access Control**: Different access levels for different user types
- **Data Encryption**: Secure data transmission and storage
- **Session Management**: Secure session handling and timeout
- **Audit Logging**: Comprehensive activity tracking

### 📊 Administrative Dashboard
- **System Management**: Complete administrative control panel
- **Real-time Analytics**: System statistics and usage metrics
- **User Management**: Admin, provider, and patient account management
- **Content Verification**: Hospital, pharmacy, and professional verification
- **System Monitoring**: Performance and health monitoring tools

---

## Technology Architecture

### Frontend Technology Stack
- **HTML5**: Semantic markup and structure
- **CSS3**: Modern styling with gradients, animations, and responsive design
- **JavaScript (ES6+)**: Interactive functionality and dynamic content
- **Bootstrap 5.3.0**: Responsive framework for mobile-first design
- **Bootstrap Icons 1.7.2**: Comprehensive icon library
- **Chart.js**: Data visualization and analytics
- **ApexCharts**: Advanced charting capabilities
- **Moment.js**: Date and time handling
- **jsPDF**: PDF generation for medical records

### Backend Technology Stack
- **Python 3.x**: Core programming language
- **Flask**: Lightweight web framework
- **SQLAlchemy**: Object-relational mapping and database abstraction
- **JWT (JSON Web Tokens)**: Secure authentication system
- **Flask-Migrate**: Database migration management
- **FHIR Client**: Healthcare interoperability standards
- **Email Integration**: SMTP for automated notifications
- **Twilio Integration**: SMS functionality for notifications

### Database Technology
- **PostgreSQL**: Primary relational database
- **SQLAlchemy ORM**: Database abstraction layer
- **Flask-Migrate**: Database schema management
- **Connection Pooling**: Optimized database connections

### DevOps & Infrastructure
- **Docker**: Containerization for consistent deployment
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Web server and reverse proxy
- **Git**: Version control system
- **GitHub**: Code repository and collaboration platform

---

## System Components

### Core Modules

#### 1. Authentication Module
- **Patient Authentication**: 6-digit PIN system with email verification
- **Provider Authentication**: JWT-based authentication for healthcare providers
- **Admin Authentication**: Secure admin login with role-based access
- **Session Management**: Secure session handling with timeout controls

#### 2. User Management Module
- **Patient Registration**: Comprehensive patient profile creation
- **Provider Registration**: Hospital, pharmacy, and professional registration
- **Admin Management**: Administrative user creation and management
- **Profile Management**: User profile editing and updates

#### 3. Medical Records Module
- **Record Creation**: Add new medical records with comprehensive details
- **Record Management**: Edit, delete, and organize medical records
- **Data Export**: PDF and CSV export functionality
- **Search and Filter**: Advanced search capabilities across records

#### 4. Provider Directory Module
- **Hospital Directory**: Comprehensive hospital listings with services
- **Pharmacy Directory**: Pharmacy listings with availability information
- **Professional Directory**: Healthcare professional profiles
- **Search and Filter**: Advanced filtering by location, specialty, and services

#### 5. Administrative Module
- **System Dashboard**: Comprehensive administrative interface
- **User Verification**: Verify hospitals, pharmacies, and professionals
- **Content Management**: Manage system content and configurations
- **Analytics**: System usage statistics and reporting

### Integration Points

#### FHIR Integration
- **Patient Data**: FHIR-compliant patient information management
- **Medical Records**: Standardized medical record format
- **Data Interoperability**: Healthcare data standards compliance
- **External Systems**: Integration with external healthcare systems

#### Communication Integration
- **Email System**: Automated email notifications for PINs and updates
- **SMS Integration**: Twilio-based SMS notifications
- **Contact Management**: Direct phone and email integration

---

## Database Design

### Core Database Models

#### User Management
```sql
-- Admin Users
CREATE TABLE admin (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address VARCHAR(200),
    is_verified BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- General Users
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL, -- 'hospital', 'individual', 'admin'
    is_verified BOOLEAN DEFAULT FALSE,
    pin VARCHAR(6) UNIQUE,
    auth_token VARCHAR(255) UNIQUE,
    token_expiry TIMESTAMP,
    -- FHIR-compliant fields
    given_name VARCHAR(100),
    family_name VARCHAR(100),
    gender VARCHAR(10),
    date_of_birth DATE,
    -- Contact information
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address_line VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    -- Medical information
    blood_type VARCHAR(5),
    allergies TEXT,
    medications TEXT,
    -- Emergency contact
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(20),
    emergency_contact_relationship VARCHAR(50),
    fhir_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Healthcare Providers
```sql
-- Hospitals
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
    services TEXT, -- JSON string
    image_url VARCHAR(500),
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pharmacies
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

-- Healthcare Professionals
CREATE TABLE healthcare_professional (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    professional_type VARCHAR(50) NOT NULL,
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

#### Medical Records
```sql
-- Medical Records
CREATE TABLE medical_record (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user(id),
    date DATE NOT NULL,
    diagnosis VARCHAR(200) NOT NULL,
    treatment TEXT NOT NULL,
    medication TEXT,
    doctor VARCHAR(100) NOT NULL,
    hospital VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Referral Feedback
CREATE TABLE referral_feedback (
    id SERIAL PRIMARY KEY,
    patient_name VARCHAR(200) NOT NULL,
    referral_source VARCHAR(100) NOT NULL DEFAULT 'PresTrack',
    feedback_notes TEXT NOT NULL,
    doctor_id INTEGER REFERENCES user(id),
    patient_id INTEGER REFERENCES user(id),
    doctor_name VARCHAR(200),
    doctor_phone VARCHAR(20),
    doctor_affiliation VARCHAR(200),
    sms_sent BOOLEAN DEFAULT FALSE,
    sms_sent_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Database Relationships
- **One-to-Many**: User to Medical Records
- **One-to-Many**: User to Referral Feedback (as doctor)
- **One-to-Many**: User to Referral Feedback (as patient)
- **Independent**: Hospitals, Pharmacies, Healthcare Professionals

---

## API Documentation

### Authentication Endpoints

#### Patient Authentication
```http
POST /api/patient/register
Content-Type: application/json

{
    "email": "patient@example.com",
    "name": "John Doe",
    "gender": "male",
    "date_of_birth": "1990-01-01",
    "phone": "+23212345678",
    "address_line": "123 Main Street",
    "city": "Freetown",
    "state": "Western Area",
    "country": "Sierra Leone"
}

Response:
{
    "message": "Registration successful",
    "pin": "123456",
    "fhir_id": "patient-12345"
}
```

```http
GET /api/patient/profile?pin=123456

Response:
{
    "id": 1,
    "name": "John Doe",
    "email": "patient@example.com",
    "gender": "male",
    "date_of_birth": "1990-01-01",
    "blood_type": "O+",
    "allergies": "None",
    "medications": "None",
    "fhir_id": "patient-12345"
}
```

#### Provider Authentication
```http
POST /api/register/hospital
Content-Type: application/json

{
    "name": "General Hospital",
    "license_number": "HOSP-001",
    "email": "admin@generalhospital.com",
    "phone": "+23212345678",
    "address": "123 Hospital Road",
    "city": "Freetown",
    "state": "Western Area",
    "country": "Sierra Leone",
    "services": ["Emergency Care", "Maternity", "Surgery"]
}

Response:
{
    "message": "Hospital registered successfully",
    "auth_token": "jwt-token-here"
}
```

### Data Management Endpoints

#### Medical Records
```http
POST /api/patient/medical-records
Content-Type: application/json

{
    "pin": "123456",
    "date": "2024-01-15",
    "diagnosis": "Hypertension",
    "treatment": "Prescribed medication and lifestyle changes",
    "medication": "Amlodipine 5mg daily",
    "doctor": "Dr. Smith",
    "hospital": "General Hospital"
}

Response:
{
    "message": "Medical record added successfully",
    "record_id": 1
}
```

```http
GET /api/patient/medical-records?pin=123456

Response:
[
    {
        "id": 1,
        "date": "2024-01-15",
        "diagnosis": "Hypertension",
        "treatment": "Prescribed medication and lifestyle changes",
        "medication": "Amlodipine 5mg daily",
        "doctor": "Dr. Smith",
        "hospital": "General Hospital"
    }
]
```

#### Provider Directory
```http
GET /api/hospitals

Response:
[
    {
        "id": 1,
        "name": "General Hospital",
        "address": "123 Hospital Road",
        "city": "Freetown",
        "phone": "+23212345678",
        "email": "info@generalhospital.com",
        "services": ["Emergency Care", "Maternity", "Surgery"],
        "is_verified": true
    }
]
```

```http
GET /api/pharmacies

Response:
[
    {
        "id": 1,
        "name": "City Pharmacy",
        "address": "456 Pharmacy Street",
        "city": "Freetown",
        "phone": "+23212345678",
        "is_24_hours": true,
        "is_verified": true
    }
]
```

### Administrative Endpoints

#### Admin Authentication
```http
POST /api/admin/login
Content-Type: application/json

{
    "email": "admin@mamacare.com",
    "password": "adminpassword"
}

Response:
{
    "message": "Login successful",
    "auth_token": "jwt-token-here",
    "admin_id": 1
}
```

#### Content Management
```http
POST /api/admin/hospitals
Authorization: Bearer jwt-token-here
Content-Type: application/json

{
    "name": "New Hospital",
    "license_number": "HOSP-002",
    "address": "789 New Road",
    "city": "Bo",
    "phone": "+23212345678",
    "email": "info@newhospital.com",
    "services": ["General Medicine", "Pediatrics"]
}

Response:
{
    "message": "Hospital added successfully",
    "hospital_id": 2
}
```

### Data Export Endpoints

#### CSV Export
```http
GET /api/export/csv?type=patients&admin_token=jwt-token-here

Response:
Content-Type: text/csv
Content-Disposition: attachment; filename="patients_export.csv"

ID,Name,Email,Gender,Date of Birth,Phone,City
1,John Doe,john@example.com,male,1990-01-01,+23212345678,Freetown
2,Jane Smith,jane@example.com,female,1985-05-15,+23212345679,Bo
```

---

## Security Features

### Authentication & Authorization
- **Multi-factor Authentication**: PIN-based for patients, JWT for providers
- **Role-based Access Control**: Different permissions for different user types
- **Session Management**: Secure session handling with automatic timeout
- **Token-based Authentication**: JWT tokens for API access

### Data Security
- **Data Encryption**: All sensitive data encrypted in transit and at rest
- **Password Hashing**: Secure password storage using bcrypt
- **Input Validation**: Comprehensive input sanitization and validation
- **SQL Injection Prevention**: Parameterized queries and ORM usage

### Privacy & Compliance
- **FHIR Compliance**: Healthcare data standards compliance
- **Data Anonymization**: Patient data protection measures
- **Audit Logging**: Comprehensive activity tracking
- **Access Controls**: Granular access control mechanisms

### Communication Security
- **HTTPS Enforcement**: All communications encrypted
- **Email Security**: Secure email transmission for notifications
- **SMS Security**: Secure SMS delivery for critical notifications
- **API Security**: Rate limiting and request validation

---

## User Interfaces

### Patient Interface
- **Responsive Design**: Mobile-first approach for accessibility
- **PIN Authentication**: Simple 6-digit PIN login system
- **Medical Records View**: Comprehensive medical history display
- **Profile Management**: Easy profile editing and updates
- **Data Export**: PDF and CSV export capabilities

### Provider Interface
- **Professional Dashboard**: Comprehensive provider management
- **Patient Records Access**: Secure access to patient information
- **Profile Management**: Professional profile editing
- **Service Management**: Service offerings and availability updates

### Administrative Interface
- **System Dashboard**: Comprehensive administrative control panel
- **User Management**: Admin, provider, and patient account management
- **Content Verification**: Hospital, pharmacy, and professional verification
- **Analytics Dashboard**: System usage statistics and reporting
- **Bulk Operations**: CSV import/export for data management

### Public Interface
- **Hospital Directory**: Public hospital listings with search and filter
- **Pharmacy Directory**: Public pharmacy listings with availability
- **Professional Directory**: Public healthcare professional listings
- **Emergency Access**: Quick access to emergency services

---

## Deployment Information

### Production Environment
- **Frontend**: Netlify deployment (https://verdant-gumdrop-61281b.netlify.app/)
- **Backend**: Docker containerized deployment
- **Database**: PostgreSQL with connection pooling
- **Web Server**: Nginx reverse proxy
- **SSL**: HTTPS enforcement for all communications

### Development Environment
- **Local Development**: Docker Compose for local development
- **Database**: PostgreSQL with Docker
- **Hot Reloading**: Development server with automatic reloading
- **Debug Mode**: Comprehensive logging and debugging tools

### Deployment Process
1. **Code Repository**: GitHub-based version control
2. **Automated Testing**: Comprehensive test suite execution
3. **Docker Build**: Containerized application packaging
4. **Database Migration**: Automated schema updates
5. **Health Checks**: System health verification
6. **Rollback Capability**: Quick rollback to previous versions

---

## Testing and Quality Assurance

### Testing Strategy
- **Unit Testing**: Individual component testing
- **Integration Testing**: API endpoint testing
- **End-to-End Testing**: Complete user workflow testing
- **Security Testing**: Authentication and authorization testing
- **Performance Testing**: Load and stress testing

### Quality Assurance Process
- **Code Review**: Peer review for all code changes
- **Automated Testing**: CI/CD pipeline integration
- **Manual Testing**: User acceptance testing
- **Security Audits**: Regular security assessments
- **Performance Monitoring**: Continuous performance monitoring

### Testing Tools
- **Backend Testing**: Python unittest framework
- **API Testing**: Postman and curl for API validation
- **Frontend Testing**: Manual testing with browser developer tools
- **Database Testing**: Direct database query testing
- **Load Testing**: Apache Bench and custom load testing scripts

---

## Maintenance and Support

### System Maintenance
- **Regular Updates**: Monthly security and feature updates
- **Database Maintenance**: Regular database optimization and backup
- **Performance Monitoring**: Continuous system performance tracking
- **Security Updates**: Regular security patches and updates
- **Backup Procedures**: Automated backup and recovery procedures

### Support Procedures
- **User Support**: Email and phone support for users
- **Technical Support**: Developer support for technical issues
- **Documentation**: Comprehensive user and technical documentation
- **Training**: User training and onboarding procedures
- **Troubleshooting**: Systematic troubleshooting procedures

### Monitoring and Alerts
- **System Health**: Continuous system health monitoring
- **Performance Metrics**: Real-time performance tracking
- **Error Logging**: Comprehensive error logging and alerting
- **User Activity**: User activity monitoring and analytics
- **Security Monitoring**: Security event monitoring and alerting

---

## Future Enhancements

### Planned Features
- **Mobile Application**: Native mobile apps for iOS and Android
- **Telemedicine Integration**: Video consultation capabilities
- **AI-powered Diagnostics**: Machine learning for preliminary diagnostics
- **Blockchain Integration**: Secure medical record blockchain
- **Advanced Analytics**: Predictive analytics for healthcare trends

### Scalability Plans
- **Microservices Architecture**: Transition to microservices for scalability
- **Cloud Migration**: Cloud-based deployment for global access
- **Multi-region Support**: Support for multiple regions and countries
- **API Gateway**: Centralized API management and monitoring
- **Load Balancing**: Advanced load balancing for high availability

---

## Conclusion

MamaCare represents a significant advancement in healthcare management technology for Sierra Leone. The system provides a comprehensive, secure, and user-friendly platform that addresses the critical needs of healthcare providers and patients alike.

With its FHIR-compliant architecture, robust security features, and comprehensive functionality, MamaCare is positioned to become the leading healthcare management platform in Sierra Leone, contributing to improved healthcare accessibility and quality across the country.

The system's modular design, comprehensive testing procedures, and scalable architecture ensure long-term sustainability and growth potential, making it a valuable asset for the healthcare sector in Sierra Leone and beyond.

---

**Document Version**: 2.0  
**Last Updated**: January 2025  
**Prepared By**: MamaCare Development Team  
**Contact**: For technical support and inquiries, please contact the development team through the project repository. 