# MamaCare - Comprehensive Healthcare Management Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![FHIR](https://img.shields.io/badge/FHIR-R4-orange.svg)](https://www.hl7.org/fhir/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)](https://www.postgresql.org/)

**MamaCare** is a comprehensive healthcare management platform designed specifically for Sierra Leone's healthcare infrastructure. The system provides a centralized platform for managing hospitals, pharmacies, healthcare professionals, and patient records, with a strong emphasis on maternal and child healthcare services.

## 🌟 Mission & Vision

**Mission**: To improve healthcare accessibility and quality in Sierra Leone by providing a comprehensive digital platform that connects patients with healthcare providers, streamlines medical record management, and enhances healthcare service delivery.

**Vision**: To become the leading healthcare management platform in Sierra Leone, ensuring every citizen has access to quality healthcare services through innovative technology solutions.

---

## 🏗️ System Architecture

### **Technology Stack**

#### **Frontend**
- **HTML5**: Semantic markup and structure
- **CSS3**: Modern styling with gradients, animations, and responsive design
- **JavaScript (ES6+)**: Interactive functionality and dynamic content
- **Bootstrap 5.3.0**: Responsive framework for mobile-first design
- **Bootstrap Icons 1.7.2**: Comprehensive icon library
- **Chart.js & ApexCharts**: Data visualization and analytics
- **Moment.js**: Date and time handling
- **jsPDF**: PDF generation for medical records

#### **Backend**
- **Python 3.x**: Core programming language
- **Flask**: Lightweight web framework
- **SQLAlchemy**: Object-relational mapping and database abstraction
- **JWT (JSON Web Tokens)**: Secure authentication system
- **Flask-Migrate**: Database migration management
- **FHIR Client**: Healthcare interoperability standards
- **Email Integration**: SMTP for automated notifications
- **Twilio Integration**: SMS functionality for notifications

#### **Database**
- **PostgreSQL**: Primary relational database
- **SQLAlchemy ORM**: Database abstraction layer
- **Flask-Migrate**: Database schema management
- **Connection Pooling**: Optimized database connections

#### **DevOps & Infrastructure**
- **Docker**: Containerization for consistent deployment
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Web server and reverse proxy
- **Git**: Version control system
- **GitHub**: Code repository and collaboration platform

---

## 🚀 Key Features

### **🏥 Patient Management System**

#### **FHIR-Compliant Registration**
- **Complete Patient Profiles**: Comprehensive patient information with FHIR R4 standards
- **Secure PIN Authentication**: 6-digit PIN-based access system with email verification
- **Multi-language Support**: Support for multiple languages and nationalities
- **Emergency Contacts**: Comprehensive emergency contact management
- **Medical History**: Complete medical background tracking

#### **Pregnancy & Maternal Care**
- **Pregnancy Status Tracking**: Real-time pregnancy status monitoring
- **Gestational Age Calculation**: Automatic calculation based on LMP date
- **Due Date Management**: Estimated due date calculation and tracking
- **Risk Assessment**: Comprehensive risk factor evaluation and categorization
- **Prenatal Care**: Medication tracking and prenatal vitamin management
- **Birth Planning**: Customizable birth plans and emergency hospital designation
- **Multiple Pregnancy Support**: Twins, triplets, and multiple pregnancy tracking
- **Pregnancy Complications**: Detailed complication tracking and management

#### **Medical Records Management**
- **Comprehensive Records**: Complete medical history with diagnosis, treatment, and medications
- **Search & Filter**: Advanced search capabilities across all medical data
- **Data Export**: PDF generation and CSV export functionality
- **Responsive Design**: Mobile-optimized table layouts and touch-friendly interface
- **Real-time Updates**: Instant data synchronization and updates

### **🏨 Healthcare Provider Management**

#### **Hospital Directory System**
- **Comprehensive Listings**: Detailed hospital information with services and contact details
- **Service Categorization**: Filter hospitals by specialty and available services
- **Real-time Status**: Availability indicators and operational hours
- **Interactive Maps**: Location services with directions and contact integration
- **Verification System**: Admin-verified hospital profiles for reliability
- **Image Management**: Hospital photos with cache-busting for reliable loading

#### **Pharmacy Management System**
- **24/7 Locator**: Find pharmacies with round-the-clock availability
- **Inventory Tracking**: Medication availability and prescription processing
- **Service Status**: Real-time operational status indicators
- **Contact Management**: Direct phone and email integration
- **Geographic Filtering**: Location-based pharmacy search
- **Type Classification**: Community, hospital, chain, and independent pharmacies

#### **Healthcare Professional Directory**
- **Professional Profiles**: Comprehensive profiles with specializations and qualifications
- **Hospital Affiliations**: Professional relationships with healthcare facilities
- **Verification System**: Admin-verified professional credentials
- **Categorization**: Professional type classification (Doctors, Nurses, Midwives, etc.)
- **Contact Integration**: Direct communication channels including WhatsApp
- **Experience Tracking**: Professional experience and qualification management

### **🔐 Security & Authentication**

#### **Multi-level Authentication**
- **Patient Authentication**: 6-digit PIN system with email verification
- **Provider Authentication**: JWT-based authentication for healthcare providers
- **Admin Authentication**: Secure admin login with role-based access control
- **Session Management**: Secure session handling with timeout controls

#### **Data Protection**
- **FHIR Compliance**: International healthcare data standards compliance
- **Data Encryption**: Secure data transmission and storage
- **Access Control**: Role-based access control for different user types
- **Audit Logging**: Comprehensive activity tracking and logging
- **Input Validation**: Comprehensive validation on all user inputs

### **📊 Administrative Dashboard**

#### **System Management**
- **Complete Administrative Control**: Full system management capabilities
- **Real-time Analytics**: System statistics and usage metrics
- **User Management**: Admin, provider, and patient account management
- **Content Verification**: Hospital, pharmacy, and professional verification
- **System Monitoring**: Performance and health monitoring tools

#### **Data Management**
- **CSV Import/Export**: Bulk data import and export functionality
- **User Verification**: Manual verification of healthcare providers
- **Content Moderation**: System content management and moderation
- **Backup & Recovery**: Data backup and recovery capabilities

### **📱 User Experience Features**

#### **Responsive Design**
- **Mobile-First Approach**: Optimized for mobile devices
- **Breakpoint System**: 480px, 768px, 992px, 1200px responsive breakpoints
- **Flexible Layouts**: CSS Grid and Flexbox for adaptive layouts
- **Touch-Friendly Interface**: Optimized for touch interactions
- **Progressive Enhancement**: Enhanced experience on capable devices

#### **Navigation System**
- **Active State Highlighting**: Visual indicators for current page location
- **Mobile Menu**: Hamburger menu for mobile devices
- **Smooth Transitions**: CSS animations and transitions
- **Accessibility**: ARIA labels and keyboard navigation support

#### **Interactive Features**
- **Advanced Search**: Real-time search with multiple filters and debouncing
- **Form Validation**: Client-side and server-side validation
- **PDF Export**: Medical records export functionality
- **SMS Integration**: WhatsApp and phone integration
- **Image Management**: Cache-busting for reliable image loading

### **🤱 Maternal Care Specialization**

#### **Pregnancy Tracking**
- **Gestational Age Calculation**: Automatic calculation from LMP date
- **Due Date Management**: Estimated due date tracking
- **Risk Level Assessment**: Low, medium, high risk categorization
- **Multiple Pregnancy Support**: Twins, triplets tracking
- **Pregnancy Complications**: Detailed complication management

#### **Prenatal Care**
- **Blood Pressure Monitoring**: Blood pressure tracking
- **Hemoglobin Levels**: Anemia monitoring and management
- **Blood Sugar Monitoring**: Gestational diabetes tracking
- **Weight Management**: Pregnancy weight tracking
- **Prenatal Vitamins**: Vitamin and supplement tracking

#### **Birth Planning**
- **Emergency Hospital Designation**: Emergency facility selection
- **Birth Plan Management**: Customizable birth plans
- **Risk Factor Documentation**: Comprehensive risk factor tracking
- **Emergency Contact Management**: Emergency contact information

---

## 📋 Pages & Features

### **🏠 Home Page (`index.html`)**
- **Hero Section**: Welcome message with call-to-action buttons
- **Features Overview**: Key system capabilities and benefits
- **Services Section**: Healthcare services offered
- **Emergency Care**: 24/7 emergency information and contacts
- **Community Support**: Health education and outreach programs

### **🏥 Hospitals (`hospitals.html`)**
- **Advanced Search & Filter**: By location, services, and hospital name
- **Hospital Cards**: Detailed information with images and services
- **Contact Information**: Phone, email, website, and address
- **Services Offered**: Comprehensive service listings
- **Interactive Features**: Call, directions, and verification badges
- **Real-time Status**: Operational status and availability

### **💊 Pharmacy (`pharmacy.html`)**
- **Pharmacy Directory**: Complete pharmacy listings with details
- **24/7 Availability**: Filter by 24/7 availability
- **Type Classification**: Community, hospital, chain, independent
- **Contact Details**: Phone, email, website integration
- **Location Services**: Google Maps integration
- **Service Status**: Real-time operational status

### **👨‍⚕️ Healthcare Professionals (`medical_personnel.html`)**
- **Professional Directory**: Doctors, nurses, specialists, midwives
- **Specialization Filter**: By medical specialty and type
- **Location Search**: Find professionals by city and region
- **Contact Options**: WhatsApp and phone integration
- **Professional Details**: Experience, qualifications, affiliations
- **Verification Status**: Admin-verified professional credentials

### **📋 Medical Records (`medical_records.html`)**
- **PIN Authentication**: Secure 6-digit PIN access system
- **Patient Registration**: FHIR-compliant registration form
- **Medical Records Table**: Comprehensive record management
- **Advanced Search & Filter**: Search capabilities across all data
- **Export Features**: PDF download and bulk operations
- **Responsive Design**: Mobile-optimized table layout
- **Pregnancy Data**: Specialized pregnancy information display
- **Confirmation Dialogs**: Edit confirmation for sensitive data

### **🔐 Provider Access (`provider_access.html`)**
- **Secure Login**: Healthcare provider authentication
- **Patient Records Access**: Authorized access to patient data
- **Referral Management**: Send and track referrals
- **SMS Notifications**: Automated feedback system
- **Professional Verification**: Admin verification system

### **📊 Admin Dashboard (`admin_dashboard.html`)**
- **System Overview**: Comprehensive system statistics
- **User Management**: Admin, provider, and patient management
- **Content Verification**: Hospital, pharmacy, and professional verification
- **Data Import/Export**: CSV import and export functionality
- **System Monitoring**: Performance and health monitoring
- **Analytics Dashboard**: Usage statistics and reporting

### **📚 Education (`education.html`)**
- **Health Education**: Educational content and resources
- **Maternal Care Information**: Pregnancy and childbirth education
- **Community Outreach**: Health awareness programs
- **Resource Library**: Educational materials and guides

---

## 🗄️ Database Schema

### **Core Database Models**

#### **User Management**
```sql
-- Admin Users (Separate table for enhanced security)
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

-- General Users (Patients, Healthcare Providers)
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL, -- 'hospital', 'individual', 'admin'
    is_verified BOOLEAN DEFAULT FALSE,
    pin VARCHAR(6) UNIQUE, -- 6-digit PIN for patient access
    auth_token VARCHAR(255) UNIQUE, -- Token for API authentication
    token_expiry TIMESTAMP,
    
    -- FHIR-compliant fields
    given_name VARCHAR(100),
    middle_name VARCHAR(100),
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
    
    -- Pregnancy-related fields
    pregnancy_status VARCHAR(20), -- 'not_pregnant', 'pregnant', 'postpartum'
    previous_pregnancies INTEGER,
    lmp_date DATE,
    due_date DATE,
    gestational_age INTEGER,
    multiple_pregnancy VARCHAR(20), -- 'no', 'twins', 'triplets'
    risk_level VARCHAR(20), -- 'low', 'medium', 'high'
    risk_factors TEXT, -- Store as JSON string
    blood_pressure VARCHAR(20),
    hemoglobin FLOAT,
    blood_sugar FLOAT,
    weight FLOAT,
    prenatal_vitamins TEXT,
    pregnancy_complications TEXT,
    emergency_hospital VARCHAR(200),
    birth_plan TEXT,
    
    fhir_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **Healthcare Providers**
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

#### **Medical Records**
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

### **Database Relationships**
- **One-to-Many**: User to Medical Records
- **One-to-Many**: User to Referral Feedback (as doctor)
- **One-to-Many**: User to Referral Feedback (as patient)
- **Independent**: Hospitals, Pharmacies, Healthcare Professionals

---

## 🔧 Configuration

### **Environment Variables**
```bash
# Database Configuration
SQLALCHEMY_DATABASE_URI=postgresql://user:password@localhost/mamacare
DATABASE_URL=postgresql://user:password@localhost/mamacare

# Email Configuration (for PIN delivery)
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_SERVER=smtp.gmail.com
EMAIL_PORT=587

# FHIR Server Configuration
FHIR_SERVER_URL=http://hapi.fhir.org/baseR4

# SMS Configuration (Twilio)
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=your-twilio-number

# Application Configuration
SECRET_KEY=your-secret-key
DEBUG=True
FLASK_ENV=development
```

---

## 📚 API Documentation

### **Authentication Endpoints**

#### **Patient Authentication**
```http
POST /api/patient/register
Content-Type: application/json

{
    "email": "patient@example.com",
    "name": "John Doe",
    "given_name": "John",
    "middle_name": "Michael",
    "family_name": "Doe",
    "gender": "male",
    "date_of_birth": "1990-01-01",
    "phone": "+23212345678",
    "address_line": "123 Main Street",
    "city": "Freetown",
    "state": "Western Area",
    "country": "Sierra Leone",
    "blood_type": "O+",
    "allergies": "None",
    "medications": "None",
    "emergency_contact_name": "Jane Doe",
    "emergency_contact_phone": "+23212345679",
    "emergency_contact_relationship": "Spouse"
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

#### **Provider Authentication**
```http
POST /api/register/hospital
Content-Type: application/json

{
    "name": "General Hospital",
    "license_number": "HOSP001",
    "email": "hospital@example.com",
    "phone": "+23212345678",
    "address": "123 Hospital Street",
    "city": "Freetown",
    "state": "Western Area",
    "country": "Sierra Leone",
    "services": ["Emergency Care", "Maternity", "Surgery"]
}
```

### **Medical Records Endpoints**
```http
GET /api/patient/medical-records?pin=123456
POST /api/patient/medical-records
DELETE /api/patient/medical-records/<record_id>
```

### **Healthcare Provider Endpoints**
```http
GET /api/hospitals
GET /api/pharmacies
GET /api/doctors
POST /api/referral/feedback
```

---

## 🚀 Quick Start

### **Prerequisites**
- **Python**: 3.8 or higher
- **PostgreSQL**: 12 or higher
- **Node.js**: 14 or higher (for development)
- **Git**: Latest version

### **Installation**

1. **Clone the repository**
```bash
git clone https://github.com/aluzay1/mamacare.git
cd mamacare
```

2. **Set up the backend**
```bash
cd backend
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Initialize the database**
```bash
python init_db.py
python create_default_admin.py
```

5. **Run the application**
```bash
python app.py
```

6. **Access the application**
```
Local Development:
Frontend: http://localhost:5000
Backend API: http://localhost:5000/api

Production:
Frontend: https://mamacare.netlify.app
Backend API: https://mamacare-backend.onrender.com
```

---

## 🧪 Testing

### **Backend Testing**
```bash
cd backend
python -m pytest tests/
python test_fhir_registration.py
```

### **Frontend Testing**
- **Manual Testing**: Test all pages and features
- **Responsive Testing**: Test on different screen sizes
- **Browser Testing**: Test on Chrome, Firefox, Safari, Edge

### **API Testing**
```bash
# Test patient registration
curl -X POST http://localhost:5000/api/patient/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "first_name": "Test", ...}'

# Test medical records access
curl "http://localhost:5000/api/patient/medical-records?pin=123456"
```

---

## 🚀 Deployment

### **Local Development**
```bash
# Backend
cd backend
python app.py

# Frontend (if using a local server)
python -m http.server 8000
```

### **Production Deployment**

#### **Frontend Deployment (Netlify)**
The frontend is deployed on **Netlify** for optimal performance and reliability:

- **Automatic Deployment**: Connected to GitHub repository for automatic updates
- **Global CDN**: Fast loading times worldwide
- **SSL Certificate**: Automatic HTTPS encryption
- **Custom Domain**: Support for custom domain configuration
- **Build Optimization**: Automatic build optimization and caching

**Deployment URL**: [https://mamacare.netlify.app](https://mamacare.netlify.app)

#### **Backend Deployment (Render)**
The backend API is hosted on **Render** for scalable cloud hosting:

- **Automatic Deployment**: Connected to GitHub repository for automatic updates
- **Auto-scaling**: Automatic scaling based on traffic
- **Database Integration**: PostgreSQL database hosting
- **Environment Variables**: Secure environment variable management
- **Health Monitoring**: Built-in health checks and monitoring

**API Base URL**: [https://mamacare-backend.onrender.com](https://mamacare-backend.onrender.com)

#### **Deployment Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Database      │
│   (Netlify)     │◄──►│   (Render)      │◄──►│   (PostgreSQL)  │
│   Static Hosting│    │   Cloud Hosting │    │   Managed DB    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **Production Deployment**
The system is configured for deployment on:
- **Frontend (Netlify)**: Static site hosting with automatic deployment from GitHub
- **Backend (Render)**: Cloud platform hosting with automatic deployment from GitHub
- **Docker**: Containerized deployment option

### **Environment Setup**

#### **Local Development**
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=development
export DATABASE_URL=postgresql://user:password@localhost/mamacare

# Run migrations
python -m flask db upgrade

# Start the application
python app.py
```

#### **Production Deployment (Render)**
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables (configured in Render dashboard)
export FLASK_ENV=production
export DATABASE_URL=your-production-database-url

# Run migrations
python -m flask db upgrade

# Start the application
gunicorn app:app
```

#### **Frontend Deployment (Netlify)**
The frontend is automatically deployed from the GitHub repository:
- **Build Command**: Not required (static files)
- **Publish Directory**: `/` (root directory)
- **Environment Variables**: Configured in Netlify dashboard

---

## 📊 Performance Optimization

### **Frontend Optimization**
- **CSS Minification**: Compressed stylesheets
- **JavaScript Optimization**: Minified and bundled scripts
- **Image Optimization**: Compressed and responsive images
- **Caching**: Browser and CDN caching strategies

### **Backend Optimization**
- **Database Indexing**: Optimized database queries
- **Connection Pooling**: Efficient database connections
- **Caching**: Redis caching for frequently accessed data
- **Load Balancing**: Horizontal scaling capabilities

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**: Follow the coding standards
4. **Add tests**: Ensure all new features are tested
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**: Provide detailed description

### **Coding Standards**
- **Python**: PEP 8 style guide
- **JavaScript**: ESLint configuration
- **CSS**: BEM methodology
- **HTML**: Semantic markup

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

### **Documentation**
- **API Docs**: Complete API documentation
- **FHIR Extensions**: Custom FHIR extensions documentation
- **Deployment Guide**: Step-by-step deployment instructions
- **User Manual**: End-user documentation

### **Getting Help**
- **GitHub Issues**: Report bugs and request features
- **Email Support**: Contact the development team
- **Community Forum**: Join our community discussions

---

## 🔄 Changelog

### **v2.4.0 - Birth Records Integration**
- ✅ Birth records table schema design
- ✅ Birth records tab integration planning
- ✅ CRUD operations for birth records
- ✅ Search and filter functionality
- ✅ Responsive design for birth records

### **v2.5.0 - Production Deployment**
- ✅ Frontend deployment on Netlify
- ✅ Backend deployment on Render
- ✅ Automatic deployment from GitHub
- ✅ SSL certificates and HTTPS
- ✅ Global CDN for frontend
- ✅ Auto-scaling for backend

### **v2.3.0 - Navigation & Image Improvements**
- ✅ Active navigation highlighting on all pages
- ✅ Cache-busting for reliable image loading
- ✅ Improved responsive table design
- ✅ Enhanced mobile user experience
- ✅ Better error handling for images

### **v2.2.0 - Responsive Design Enhancement**
- ✅ Mobile-optimized table layouts
- ✅ Touch-friendly interface elements
- ✅ Progressive column width adjustments
- ✅ Horizontal scroll indicators
- ✅ Improved button visibility on small screens

### **v2.1.0 - Search & Filter Improvements**
- ✅ Advanced search functionality
- ✅ Real-time search with debouncing
- ✅ Multiple filter options
- ✅ Clear search functionality
- ✅ Search result highlighting

### **v2.0.0 - FHIR Compliance Update**
- ✅ Full FHIR R4 compliance
- ✅ Enhanced patient registration form
- ✅ Multiple FHIR resource creation
- ✅ Structured data inputs
- ✅ Real-time validation
- ✅ Custom FHIR extensions

### **v1.0.0 - Initial Release**
- ✅ Basic patient management
- ✅ Medical records system
- ✅ Healthcare provider access
- ✅ SMS integration

---

## 🌟 Acknowledgments

- **FHIR Community**: For healthcare interoperability standards
- **Flask Community**: For the excellent web framework
- **Open Source Contributors**: For various libraries and tools
- **Healthcare Professionals**: For domain expertise and feedback

---

**MamaCare** - Empowering healthcare through technology and innovation. 

*Built with ❤️ for better healthcare outcomes in Sierra Leone.* 