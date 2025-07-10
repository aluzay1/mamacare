#  MamaCare Healthcare Management System
## Complete System Documentation

**Version:** 2.0.0  
**Last Updated:** December 2024  
**Document Status:** Current  

---

##  Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Database Design](#database-design)
4. [API Documentation](#api-documentation)
5. [Security Framework](#security-framework)
6. [User Management](#user-management)
7. [Data Flow](#data-flow)
8. [Deployment Guide](#deployment-guide)
9. [Maintenance Procedures](#maintenance-procedures)
10. [Troubleshooting](#troubleshooting)
11. [Compliance & Standards](#compliance--standards)

---

##  System Overview

### **Purpose**
MamaCare is a comprehensive healthcare management system designed specifically for Sierra Leone's healthcare infrastructure. The system provides a centralized platform for managing hospitals, pharmacies, healthcare professionals, and patient records, with a strong emphasis on maternal and child healthcare services.

### **Key Objectives**
- Improve healthcare accessibility in Sierra Leone
- Streamline medical record management
- Enhance healthcare service delivery
- Provide FHIR-compliant data interoperability
- Support maternal and child healthcare initiatives

### **Target Users**
- **Patients**: Individual users accessing medical records
- **Healthcare Providers**: Doctors, nurses, and medical professionals
- **Hospitals**: Healthcare facilities managing services
- **Pharmacies**: Pharmaceutical service providers
- **Administrators**: System administrators managing the platform

---

##  Architecture

### **System Architecture Overview**

The MamaCare system follows a three-tier architecture:

1. **Presentation Layer**: HTML/CSS/JavaScript frontend
2. **Application Layer**: Flask Python backend API
3. **Data Layer**: PostgreSQL database

### **Technology Stack**

#### **Frontend**
- **HTML5**: Semantic markup and structure
- **CSS3**: Modern styling with gradients and animations
- **JavaScript (ES6+)**: Interactive functionality
- **Bootstrap 5.3.0**: Responsive framework
- **Chart.js & ApexCharts**: Data visualization
- **Moment.js**: Date handling

#### **Backend**
- **Python 3.x**: Core programming language
- **Flask**: Web framework
- **SQLAlchemy**: Object-relational mapping
- **JWT**: Authentication tokens
- **Flask-Migrate**: Database migrations
- **FHIR Client**: Healthcare interoperability

#### **Database**
- **PostgreSQL**: Primary database
- **SQLAlchemy ORM**: Database abstraction layer

#### **Infrastructure**
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Web server and reverse proxy
- **Git**: Version control

---

##  Database Design

### **Database Schema Overview**

The system uses a relational database with the following core tables:

#### **1. Admin Table (dmin)**
Separate table for system administrators with enhanced security.

#### **2. User Table (user)**
Central user management table supporting multiple user types with role-based access control.

#### **3. Medical Records Table (medical_record)**
Stores patient medical records with FHIR compliance.

#### **4. Hospitals Table (hospital)**
Comprehensive hospital information management.

# Removed crowdfunding tables - no longer needed

### **Database Relationships**

#### **One-to-Many Relationships**
- **User  Medical Records**: A patient can have multiple medical records

---

##  API Documentation

### **Authentication Endpoints**

#### **Admin Authentication**
- **POST /api/admin/login**: Admin login with email/password
- **POST /api/admin/signup**: Create new admin account

#### **Patient Authentication**
- **POST /api/patient/profile**: Patient login with PIN

### **User Management Endpoints**

#### **Registration Endpoints**
- **POST /api/register/hospital**: Register hospital account
- **POST /api/register/individual**: Register patient account

### **Medical Records Endpoints**

#### **Medical Record Management**
- **POST /api/patient/medical-records**: Add medical record
- **GET /api/patient/medical-records**: Get patient records

### **Hospital Management Endpoints**

#### **Hospital Operations**
- **GET /api/hospitals**: Get public hospital listings
- **POST /api/admin/hospitals**: Add hospital (admin only)

# Removed Campaign Management Endpoints - no longer needed

---

##  Security Framework

### **Authentication & Authorization**

#### **Multi-Level Authentication**
1. **PIN-based Authentication**: For patients accessing medical records
2. **JWT Token Authentication**: For healthcare providers and admins
3. **Role-based Access Control**: Different permissions for different user types

#### **Password Security**
- **Hashing**: Passwords are hashed using Werkzeug's security functions
- **Salt**: Automatic salt generation for additional security
- **Verification**: Secure password verification

#### **Token Management**
- **JWT Tokens**: Stateless authentication for API access
- **Token Expiry**: Configurable token expiration times
- **Secure Storage**: Tokens stored securely in database

### **Data Protection**

#### **Input Validation**
- **SQL Injection Prevention**: Parameterized queries via SQLAlchemy
- **XSS Prevention**: Input sanitization and output encoding
- **File Upload Security**: Secure file handling with validation

#### **Data Encryption**
- **HTTPS**: All communications encrypted in transit
- **Database Encryption**: Sensitive data encrypted at rest
- **API Security**: CORS protection and request validation

---

##  User Management

### **User Types & Roles**

#### **1. Administrators**
- **Storage**: Separate dmin table
- **Permissions**: Full system access
- **Authentication**: Email/password with JWT tokens
- **Management**: Can create, edit, and delete other admins

#### **2. Hospitals**
- **Storage**: user table with 
ole='hospital'
- **Permissions**: Campaign creation, withdrawal requests
- **Authentication**: Email/password with JWT tokens
- **Features**: Hospital profile management, service listings

#### **3. Individuals (Patients)**
- **Storage**: user table with 
ole='individual'
- **Permissions**: Medical record access, profile management
- **Authentication**: PIN-based access
- **Features**: Medical history, pregnancy tracking

# Removed Donor role - no longer needed

---

##  Data Flow

### **Patient Data Flow**

`
Patient Registration  Profile Creation  Medical Records  FHIR Integration
                                                             
   PIN Generation  Email Notification  Record Storage  External Systems
`

### **Hospital Data Flow**

`
Hospital Registration  Admin Verification  Service Listing  Campaign Creation
                                                                 
   Profile Setup  Approval Process  Public Display  Fundraising
`

# Removed Campaign & Donation Flow - no longer needed

---

##  Deployment Guide

### **Production Deployment**

#### **Prerequisites**
- Docker and Docker Compose installed
- PostgreSQL database (local or cloud)
- Domain name and SSL certificate
- Email service configuration

#### **Docker Deployment**
`ash
# Build and start containers
docker-compose up --build -d

# Run database migrations
docker-compose exec backend flask db upgrade

# Initialize database
docker-compose exec backend python init_db.py
`

### **Development Setup**

#### **Local Development**
`ash
# Clone repository
git clone https://github.com/aluzay1/mamacare.git
cd mamacare

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Set up environment
export FLASK_APP=app.py
export FLASK_ENV=development

# Run migrations
flask db upgrade

# Start development server
flask run --host=0.0.0.0 --port=5000
`

---

##  Maintenance Procedures

### **Database Maintenance**

#### **Regular Backups**
- Automated daily backups using PostgreSQL pg_dump
- Point-in-time recovery capabilities
- Encrypted backup storage
- Cross-region backup replication

#### **Database Optimization**
- Regular table statistics analysis
- Database vacuum operations
- Index optimization
- Query performance monitoring

### **Application Maintenance**

#### **Log Management**
- Log rotation and archiving
- Error monitoring and alerting
- Performance log analysis
- Security event logging

#### **Security Maintenance**
- Regular dependency updates
- Security vulnerability scanning
- Access control reviews
- Security audit procedures

---

##  Troubleshooting

### **Common Issues**

#### **Database Connection Issues**
- Check database container status
- Verify connection credentials
- Review database logs
- Test network connectivity

#### **Application Startup Issues**
- Check application logs
- Verify environment variables
- Test dependency installation
- Review configuration files

#### **Email Configuration Issues**
- Test SMTP connection
- Verify email credentials
- Check firewall settings
- Review email service logs

### **Performance Issues**

#### **Slow Database Queries**
- Enable query logging
- Analyze slow query patterns
- Optimize database indexes
- Review query execution plans

#### **Memory Issues**
- Monitor memory usage
- Check for memory leaks
- Optimize application code
- Review resource allocation

---

##  Compliance & Standards

### **Healthcare Standards**

#### **FHIR Compliance**
- **Patient Resources**: FHIR-compliant patient data structure
- **Observation Resources**: Medical records stored as FHIR observations
- **MedicationRequest**: Medication information in FHIR format
- **Organization**: Hospitals and pharmacies as FHIR organizations

#### **Data Interoperability**
- **HL7 FHIR R4**: Latest FHIR standard implementation
- **RESTful APIs**: Standard healthcare API patterns
- **JSON Format**: Standard data exchange format
- **Terminology Standards**: SNOMED CT and LOINC code support

### **Security Standards**

#### **Data Protection**
- **Encryption**: Data encrypted in transit and at rest
- **Access Control**: Role-based access control (RBAC)
- **Audit Logging**: Comprehensive audit trails
- **Data Minimization**: Only necessary data collected

#### **Privacy Compliance**
- **GDPR Compliance**: European data protection standards
- **HIPAA Considerations**: Healthcare privacy standards
- **Local Regulations**: Sierra Leone healthcare regulations
- **Consent Management**: User consent tracking and management

---

##  Support & Contact

### **Technical Support**
- **Email**: support@mamacare.com
- **Documentation**: https://docs.mamacare.com
- **GitHub Issues**: https://github.com/aluzay1/mamacare/issues

### **Emergency Contacts**
- **System Administrator**: admin@mamacare.com
- **Database Administrator**: dba@mamacare.com
- **Security Team**: security@mamacare.com

### **Maintenance Schedule**
- **Regular Maintenance**: Every Sunday 2:00 AM - 4:00 AM
- **Security Updates**: As needed
- **Database Backups**: Daily at 2:00 AM
- **Performance Monitoring**: 24/7

---

**Document Version:** 2.0.0  
**Last Updated:** December 2024  
**Next Review:** March 2025  
**Document Owner:** MamaCare Development Team
