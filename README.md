# MamaCare - FHIR-Compliant Maternal Healthcare Platform

MamaCare is a comprehensive maternal healthcare platform built with Flask and PostgreSQL, designed to provide secure, FHIR-compliant patient record management with a focus on maternal care and pregnancy tracking.

## 🚀 Recent Updates - FHIR Compliance Enhancement

### ✅ FHIR-Compliant Patient Registration

The patient registration system has been completely updated to ensure full compliance with the FHIR (Fast Healthcare Interoperability Resources) standard:

#### **Enhanced Form Features:**
- **Full Gender Support**: Now supports male, female, other, and unknown (FHIR-compliant)
- **Optional Postal Code**: Made optional for regions where it's not applicable
- **Structured Inputs**: Replaced free-text fields with structured dropdowns for:
  - Allergies (multi-select with common options)
  - Medications (multi-select with common medications)
  - Pregnancy complications (multi-select with medical conditions)
- **Real-time Validation**: Client-side validation for:
  - Phone numbers (Sierra Leone format: +232XXXXXXXX)
  - Email addresses
  - Blood pressure format (systolic/diastolic)
- **Conditional Display**: JavaScript logic to show/hide pregnancy fields based on gender and pregnancy status

#### **FHIR Resource Creation:**
The system now creates multiple FHIR resources for each patient:

1. **Patient Resource** with custom extensions:
   - Blood type, nationality, pregnancy status
   - LMP date, due date, gestational age
   - Multiple pregnancy, risk level, previous pregnancies
   - Prenatal vitamins, emergency hospital

2. **Observation Resources** for clinical measurements:
   - Blood pressure (LOINC 55284-4)
   - Hemoglobin (LOINC 718-7)
   - Blood sugar (LOINC 2339-0)
   - Weight (LOINC 29463-7)

3. **AllergyIntolerance Resources** for patient allergies

4. **MedicationStatement Resources** for current medications

5. **Condition Resources** for pregnancy complications and risk factors

6. **CarePlan Resources** for birth plans

#### **Backend Enhancements:**
- **Enhanced Validation**: Server-side validation for all FHIR-compliant fields
- **FHIR Extensions**: Custom extensions for pregnancy-specific data
- **Resource Mapping**: Proper mapping of form fields to FHIR resources
- **Error Handling**: Comprehensive error handling and validation feedback

## 📋 System Overview

MamaCare provides a comprehensive healthcare management system with the following key features:

### **Patient Management**
- FHIR-compliant patient registration
- Secure PIN-based access to medical records
- Comprehensive patient profiles with pregnancy tracking
- Medical record management with FHIR Observation resources

### **Healthcare Provider Access**
- Hospital and pharmacy registration
- Healthcare professional management
- Referral feedback system with SMS notifications
- Provider verification system

### **Maternal Care Focus**
- Pregnancy status tracking
- Gestational age calculation
- Risk factor assessment
- Birth plan management
- Emergency contact management

### **Data Interoperability**
- Full FHIR R4 compliance
- Standard coding systems (LOINC, SNOMED CT, RxNorm)
- Custom extensions for maternal care data
- Export/import capabilities

## 🏗️ Architecture

### **Backend (Flask)**
- **Framework**: Flask with SQLAlchemy ORM
- **Database**: PostgreSQL with Alembic migrations
- **FHIR Integration**: fhirclient library for FHIR R4 resources
- **Authentication**: PIN-based system with email verification
- **API**: RESTful endpoints with JSON responses

### **Frontend (HTML/CSS/JavaScript)**
- **Responsive Design**: Mobile-first approach
- **Form Validation**: Real-time client-side validation
- **Conditional Logic**: Dynamic form field display
- **User Experience**: Intuitive interface for healthcare providers

### **FHIR Resources**
- **Patient**: Core patient information with custom extensions
- **Observation**: Clinical measurements and vital signs
- **AllergyIntolerance**: Patient allergies and intolerances
- **MedicationStatement**: Current medications
- **Condition**: Medical conditions and complications
- **CarePlan**: Treatment plans and birth plans

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8+
- PostgreSQL 12+
- Docker (optional)

### **Installation**

1. **Clone the repository**
```bash
   git clone <repository-url>
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
   # Edit .env with your database and email settings
   ```

4. **Initialize the database**
```bash
python init_db.py
```

5. **Run the application**
```bash
   python app.py
   ```

### **Testing the FHIR Registration**

Use the provided test script to verify FHIR compliance:

```bash
python test_fhir_registration.py
```

Or use curl:

```bash
curl -X POST http://localhost:5000/api/patient/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane.doe@example.com",
    "name": "Jane Marie Doe",
    "given_name": "Jane",
    "middle_name": "Marie",
    "family_name": "Doe",
    "gender": "female",
    "date_of_birth": "1990-05-15",
    "phone": "+232123456789",
    "address_line": "123 Main Street",
    "city": "Freetown",
    "state": "Western Area",
    "country": "Sierra Leone",
    "blood_type": "O+",
    "allergies": ["penicillin"],
    "medications": ["folic_acid"],
    "pregnancy_status": "pregnant",
    "lmp_date": "2024-01-15"
  }'
```

## 📚 API Documentation

### **Patient Registration**
- **Endpoint**: `POST /api/patient/register`
- **Content-Type**: `application/json`
- **Response**: Patient ID, FHIR ID, PIN, and created FHIR resources

### **Patient Profile Access**
- **Endpoint**: `GET /api/patient/profile?pin=<PIN>`
- **Response**: Complete patient profile with FHIR-compliant data

### **Medical Records**
- **Add Record**: `POST /api/patient/medical-records`
- **Get Records**: `GET /api/patient/medical-records?pin=<PIN>`

## 🔧 Configuration

### **Environment Variables**
```bash
# Database
SQLALCHEMY_DATABASE_URI=postgresql://user:password@localhost/mamacare

# Email (for PIN delivery)
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# FHIR Server
FHIR_SERVER_URL=http://hapi.fhir.org/baseR4

# SMS (optional)
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=your-twilio-number
```

## 📖 FHIR Extensions Documentation

Custom FHIR extensions are documented in `docs/fhir_extensions.md`:

- **Blood Type Extension**: `http://mamacare.com/fhir/StructureDefinition/patient-bloodType`
- **Pregnancy Status Extension**: `http://mamacare.com/fhir/StructureDefinition/patient-pregnancyStatus`
- **LMP Date Extension**: `http://mamacare.com/fhir/StructureDefinition/patient-lmpDate`
- **And more...**

## 🧪 Testing

### **Unit Tests**
```bash
cd backend
python -m pytest tests/
```

### **Integration Tests**
```bash
python test_fhir_registration.py
```

### **Manual Testing**
1. Open `medical_records.html` in a browser
2. Test the registration form with various inputs
3. Verify FHIR resource creation in the response

## 🔒 Security Features

- **PIN-based Authentication**: Secure 6-digit PIN system
- **Email Verification**: PIN delivery via email
- **Input Validation**: Comprehensive client and server-side validation
- **FHIR Compliance**: Standard healthcare data formats
- **Data Encryption**: Secure storage and transmission

## 🌟 Key Features

### **For Patients**
- Easy registration with structured forms
- Secure access to medical records
- Pregnancy tracking and management
- Emergency contact management

### **For Healthcare Providers**
- FHIR-compliant data exchange
- Comprehensive patient profiles
- Referral management system
- SMS notifications for feedback

### **For Administrators**
- User management and verification
- Hospital and pharmacy registration
- System monitoring and maintenance
- Data export and reporting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the documentation in `docs/`
- Review the API documentation
- Open an issue on GitHub

## 🔄 Changelog

### **v2.0.0 - FHIR Compliance Update**
- ✅ Full FHIR R4 compliance
- ✅ Enhanced patient registration form
- ✅ Multiple FHIR resource creation
- ✅ Structured data inputs
- ✅ Real-time validation
- ✅ Custom FHIR extensions
- ✅ Comprehensive documentation

### **v1.0.0 - Initial Release**
- Basic patient management
- Medical records system
- Healthcare provider access
- SMS integration

---

**MamaCare** - Empowering maternal healthcare through FHIR-compliant technology. 