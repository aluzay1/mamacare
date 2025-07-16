# MamaCare - Comprehensive Healthcare Management Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![FHIR](https://img.shields.io/badge/FHIR-R4-orange.svg)](https://www.hl7.org/fhir/)

**MamaCare** is a comprehensive healthcare management platform designed to provide secure, FHIR-compliant patient record management with a focus on maternal care, hospital management, and healthcare provider coordination.

## 🌟 Key Features

### **🏥 Patient Management**
- **FHIR-Compliant Registration**: Full compliance with FHIR R4 standards
- **Secure PIN Access**: 6-digit PIN-based authentication system
- **Comprehensive Profiles**: Detailed patient information with pregnancy tracking
- **Medical Records**: Complete medical history management with FHIR Observation resources
- **Responsive Interface**: Mobile-first design for all devices

### **🏨 Healthcare Provider Management**
- **Hospital Directory**: Comprehensive hospital database with services and contact information
- **Pharmacy Network**: Extensive pharmacy listings with 24/7 availability tracking
- **Healthcare Professionals**: Doctor and medical personnel directory with specializations
- **Provider Verification**: Secure verification system for healthcare providers

### **🤱 Maternal Care Focus**
- **Pregnancy Tracking**: Gestational age calculation and due date management
- **Risk Assessment**: Comprehensive risk factor evaluation
- **Birth Planning**: Customizable birth plans and emergency contacts
- **Prenatal Care**: Medication tracking and prenatal vitamin management

### **📱 User Experience**
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Active Navigation**: Visual indicators for current page location
- **Image Management**: Cache-busting for reliable image loading
- **Search & Filter**: Advanced search capabilities across all data types

## 🏗️ System Architecture

### **Backend Stack**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Flask App     │    │   PostgreSQL    │    │   FHIR Server   │
│   (Python)      │◄──►│   Database      │◄──►│   (HAPI FHIR)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Email Service │    │   SMS Service   │    │   File Storage  │
│   (Gmail SMTP)  │    │   (Twilio)      │    │   (Local/Cloud) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **Frontend Stack**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   HTML5         │    │   CSS3          │    │   JavaScript    │
│   (Semantic)    │    │   (Responsive)  │    │   (ES6+)        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Font Awesome  │    │   Google Fonts  │    │   jsPDF         │
│   (Icons)       │    │   (Typography)  │    │   (PDF Export)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

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
Frontend: http://localhost:5000
Backend API: http://localhost:5000/api
```

## 📱 Pages & Features

### **🏠 Home Page (`index.html`)**
- **Hero Section**: Welcome message with call-to-action buttons
- **Features Overview**: Key system capabilities
- **Services Section**: Healthcare services offered
- **Emergency Care**: 24/7 emergency information
- **Community Support**: Health education and outreach

### **🏥 Hospitals (`hospitals.html`)**
- **Search & Filter**: By location, services, and name
- **Hospital Cards**: Detailed information with images
- **Contact Information**: Phone, email, website, address
- **Services Offered**: Comprehensive service listings
- **Interactive Features**: Call, directions, and verification badges

### **💊 Pharmacy (`pharmacy.html`)**
- **Pharmacy Directory**: Complete pharmacy listings
- **24/7 Availability**: Filter by availability
- **Type Classification**: Community, hospital, chain, independent
- **Contact Details**: Phone, email, website
- **Location Services**: Google Maps integration

### **👨‍⚕️ Healthcare Professionals (`medical_personnel.html`)**
- **Professional Directory**: Doctors, nurses, specialists
- **Specialization Filter**: By medical specialty
- **Location Search**: Find professionals by city
- **Contact Options**: WhatsApp and phone integration
- **Professional Details**: Experience, qualifications, affiliations

### **📋 Medical Records (`medical_records.html`)**
- **PIN Authentication**: Secure 6-digit PIN access
- **Patient Registration**: FHIR-compliant registration form
- **Medical Records Table**: Comprehensive record management
- **Search & Filter**: Advanced search capabilities
- **Export Features**: PDF download and bulk operations
- **Responsive Design**: Mobile-optimized table layout

### **🔐 Provider Access (`provider_access.html`)**
- **Secure Login**: Healthcare provider authentication
- **Patient Records Access**: Authorized access to patient data
- **Referral Management**: Send and track referrals
- **SMS Notifications**: Automated feedback system

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

### **Database Schema**
The system uses PostgreSQL with the following main tables:
- `patients`: Patient information and FHIR IDs
- `medical_records`: Patient medical records
- `hospitals`: Hospital information and services
- `pharmacies`: Pharmacy details and availability
- `doctors`: Healthcare professional information
- `admins`: Administrator accounts
- `referral_feedback`: Referral management system

## 📚 API Documentation

### **Patient Management**
```http
POST /api/patient/register
Content-Type: application/json

{
  "email": "patient@example.com",
  "first_name": "Jane",
  "middle_name": "Marie",
  "last_name": "Doe",
  "date_of_birth": "1990-05-15",
  "gender": "female",
  "phone": "+232123456789",
  "address_line": "123 Main Street",
  "city": "Freetown",
  "state": "Western Area",
  "country": "Sierra Leone"
}
```

### **Medical Records**
```http
GET /api/patient/medical-records?pin=123456
POST /api/patient/medical-records
DELETE /api/patient/medical-records/<record_id>
```

### **Healthcare Providers**
```http
GET /api/hospitals
GET /api/pharmacies
GET /api/doctors
POST /api/referral/feedback
```

## 🎨 Frontend Features

### **Responsive Design**
- **Mobile-First**: Optimized for mobile devices
- **Breakpoints**: 480px, 768px, 992px, 1200px
- **Flexible Layouts**: CSS Grid and Flexbox
- **Touch-Friendly**: Optimized for touch interactions

### **Navigation System**
- **Active State Highlighting**: Visual indicators for current page
- **Mobile Menu**: Hamburger menu for mobile devices
- **Smooth Transitions**: CSS animations and transitions
- **Accessibility**: ARIA labels and keyboard navigation

### **Image Management**
- **Cache Busting**: Automatic cache refresh for images
- **Fallback Images**: Default images for missing content
- **Optimized Loading**: Lazy loading and error handling
- **Responsive Images**: Different sizes for different devices

### **Interactive Features**
- **Search & Filter**: Real-time search with multiple filters
- **Form Validation**: Client-side and server-side validation
- **PDF Export**: Medical records export functionality
- **SMS Integration**: WhatsApp and phone integration

## 🔒 Security Features

### **Authentication & Authorization**
- **PIN-Based Access**: Secure 6-digit PIN system
- **Email Verification**: PIN delivery via email
- **Session Management**: Secure session handling
- **Input Validation**: Comprehensive validation on all inputs

### **Data Protection**
- **FHIR Compliance**: Standard healthcare data formats
- **Encryption**: Secure data transmission and storage
- **Access Control**: Role-based access control
- **Audit Logging**: Comprehensive activity logging

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
The system is configured for deployment on:
- **Render**: Automatic deployment from GitHub
- **Heroku**: Cloud platform deployment
- **Docker**: Containerized deployment

### **Environment Setup**
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=production
export DATABASE_URL=your-production-database-url

# Run migrations
python -m flask db upgrade

# Start the application
gunicorn app:app
```

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

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

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

## 🔄 Changelog

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

## 🌟 Acknowledgments

- **FHIR Community**: For healthcare interoperability standards
- **Flask Community**: For the excellent web framework
- **Open Source Contributors**: For various libraries and tools
- **Healthcare Professionals**: For domain expertise and feedback

---

**MamaCare** - Empowering healthcare through technology and innovation. 

*Built with ❤️ for better healthcare outcomes.* 