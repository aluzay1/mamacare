from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_cors import CORS
from flask_migrate import Migrate
from fhirclient import client
from fhirclient.models.patient import Patient
from fhirclient.models.observation import Observation
from fhirclient.models.medicationrequest import MedicationRequest
from fhirclient.models.humanname import HumanName
from fhirclient.models.contactpoint import ContactPoint
from fhirclient.models.address import Address
from fhirclient.models.identifier import Identifier
import os
import secrets
from datetime import datetime, timedelta
import logging
import time
import sys
import psycopg2
import smtplib
import random
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import json
import csv
from io import StringIO
from sqlalchemy import text

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure CORS to allow requests from your Flutter app
CORS(app, resources={
    r"/*": {  # Allow all routes
        "origins": ["http://localhost", "http://localhost:5000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "expose_headers": ["Content-Type", "Authorization"]
    }
})

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/mamacare'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'pool_size': 5,
    'max_overflow': 10,
    'pool_timeout': 30,
    'pool_reset_on_return': 'rollback'
}
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')

# Email configuration
if os.getenv('EMAIL_USER') and os.getenv('EMAIL_PASSWORD') and os.getenv('EMAIL_USER') != 'your-actual-email@gmail.com':
    # Use Gmail if credentials are properly configured
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')
else:
    # Use a test configuration that logs emails instead of sending them
    app.config['MAIL_SERVER'] = 'localhost'
    app.config['MAIL_PORT'] = 1025
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USERNAME'] = None
    app.config['MAIL_PASSWORD'] = None
    app.config['MAIL_DEFAULT_SENDER'] = 'noreply@mamacare.com'
    logger.warning("Email credentials not configured. Emails will be logged instead of sent.")

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize FHIR client
settings = {
    'app_id': 'mamacare',
    'api_base': 'http://hapi.fhir.org/baseR4',
    'verify': False
}
fhir_client = client.FHIRClient(settings=settings)

# Database connection check
@app.before_request
def check_db_connection():
    try:
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        db.session.rollback()
        try:
            db.session.close()
            db.session.remove()
            db.engine.dispose()
        except:
            pass
        return jsonify({'error': 'Database connection error'}), 500

# Health check endpoint
@app.route('/health')
def health_check():
    try:
        # Check database connection
        db.session.execute(text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'database': 'connected'
        }), 200
    except Exception as e:
        logger.error(f'Health check failed: {str(e)}')
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 500

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'hospital', 'individual', 'donor', 'admin'
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    pin = db.Column(db.String(6), unique=True)  # 6-digit PIN for patient access
    auth_token = db.Column(db.String(255), unique=True)  # Token for API authentication
    token_expiry = db.Column(db.DateTime)  # Token expiration time
    
    # Common fields
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200))
    
    # FHIR-compliant fields
    given_name = db.Column(db.String(100))
    family_name = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    date_of_birth = db.Column(db.Date)
    address_line = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    marital_status = db.Column(db.String(50))
    language = db.Column(db.String(10))
    nationality = db.Column(db.String(100))
    blood_type = db.Column(db.String(5))
    allergies = db.Column(db.Text)
    medications = db.Column(db.Text)
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(20))
    emergency_contact_relationship = db.Column(db.String(50))
    fhir_id = db.Column(db.String(100))
    
    # Hospital-specific fields
    hospital_name = db.Column(db.String(200))
    license_number = db.Column(db.String(50))
    registration_document = db.Column(db.String(255))
    
    # Individual-specific fields
    medical_condition = db.Column(db.Text)
    medical_documents = db.Column(db.Text)  # JSON string of document URLs
    
    # Pregnancy-related fields
    pregnancy_status = db.Column(db.String(20))  # 'not_pregnant', 'pregnant', 'postpartum'
    previous_pregnancies = db.Column(db.Integer)
    lmp_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    gestational_age = db.Column(db.Integer)
    multiple_pregnancy = db.Column(db.String(20))  # 'no', 'twins', 'triplets'
    risk_level = db.Column(db.String(20))  # 'low', 'medium', 'high'
    risk_factors = db.Column(db.Text)  # Store as JSON string
    blood_pressure = db.Column(db.String(20))
    hemoglobin = db.Column(db.Float)
    blood_sugar = db.Column(db.Float)
    weight = db.Column(db.Float)
    prenatal_vitamins = db.Column(db.Text)
    pregnancy_complications = db.Column(db.Text)
    emergency_hospital = db.Column(db.String(200))
    birth_plan = db.Column(db.Text)
    
    # Relationships
    campaigns = db.relationship('Campaign', backref='creator', lazy=True)
    donations = db.relationship('Donation', backref='donor', lazy=True)
    withdrawal_requests = db.relationship('WithdrawalRequest', backref='hospital', lazy=True)

    def get_id(self):
        return str(self.id)

class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    diagnosis = db.Column(db.String(200), nullable=False)
    treatment = db.Column(db.Text, nullable=False)
    medication = db.Column(db.Text)
    doctor = db.Column(db.String(100), nullable=False)
    hospital = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='active')  # active, completed, suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Foreign keys
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    donations = db.relationship('Donation', backref='campaign', lazy=True)
    withdrawal_requests = db.relationship('WithdrawalRequest', backref='campaign', lazy=True)

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)  # orange_money, afrimoney, qmoney
    transaction_id = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    donor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)

class WithdrawalRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    
    # Foreign keys
    hospital_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    website = db.Column(db.String(200))
    services = db.Column(db.Text)  # Store services as a JSON string
    image_url = db.Column(db.String(500))  # Add image_url field
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Pharmacy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    website = db.Column(db.String(200))
    is_24_hours = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    professional_type = db.Column(db.String(50), nullable=False, default='Medical Doctor')  # Add this line
    specialization = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    hospital_affiliation = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    website = db.Column(db.String(200))
    image_url = db.Column(db.String(255))
    is_verified = db.Column(db.Boolean, default=False)
    qualifications = db.Column(db.Text)
    experience = db.Column(db.String(100))
    pin = db.Column(db.String(6), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class HealthcareProfessional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    professional_type = db.Column(db.String(50), nullable=False)  # e.g., Medical Doctor, Nurse, Midwife, etc.
    specialization = db.Column(db.String(100), nullable=False)
    hospital_affiliation = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=True)  # Made nullable
    city = db.Column(db.String(100), nullable=True)  # Made nullable
    state = db.Column(db.String(100), nullable=True)  # Made nullable
    postal_code = db.Column(db.String(20), nullable=True)  # Made nullable
    country = db.Column(db.String(100), nullable=True)  # Made nullable
    website = db.Column(db.String(200), nullable=True)  # Made nullable
    image_url = db.Column(db.String(255), nullable=True)  # Made nullable
    is_verified = db.Column(db.Boolean, default=False)
    qualifications = db.Column(db.Text, nullable=True)  # Made nullable
    experience = db.Column(db.String(100), nullable=True)  # Made nullable
    pin = db.Column(db.String(6), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Authentication decorators
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization token required'}), 401
            
        token = auth_header.split(' ')[1]
        user = User.query.filter_by(auth_token=token, role='admin').first()
        
        if not user:
            return jsonify({'error': 'Invalid token'}), 401
            
        if user.token_expiry and user.token_expiry < datetime.utcnow():
            return jsonify({'error': 'Token expired'}), 401
            
        return f(*args, **kwargs)
    return decorated_function

def hospital_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'hospital':
            return jsonify({'error': 'Hospital access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def individual_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'individual':
            return jsonify({'error': 'Individual access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def donor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'donor':
            return jsonify({'error': 'Donor access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# Add these helper functions after the imports and before the app initialization
def calculate_gestational_age(lmp_date):
    """Calculate gestational age in weeks based on LMP date"""
    if not lmp_date:
        return None
    today = datetime.now().date()
    days = (today - lmp_date).days
    weeks = days // 7
    return weeks

def calculate_due_date(lmp_date):
    """Calculate due date based on LMP date (40 weeks from LMP)"""
    if not lmp_date:
        return None
    return lmp_date + timedelta(days=280)  # 40 weeks * 7 days

# Registration endpoints
@app.route('/api/register/hospital', methods=['POST'])
def register_hospital():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'name', 'phone', 'hospital_name', 'license_number']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
            
        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 409
            
        # Create new hospital user
        hospital = User(
            email=data['email'],
            password=generate_password_hash(data['password']),
            role='hospital',
            name=data['name'],
            phone=data['phone'],
            hospital_name=data['hospital_name'],
            license_number=data['license_number']
        )
        
        db.session.add(hospital)
        db.session.commit()
        
        return jsonify({
            'message': 'Hospital registered successfully. Please wait for admin verification.',
            'hospital_id': hospital.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/register/individual', methods=['POST'])
def register_individual():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'name', 'phone', 'date_of_birth', 'medical_condition']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
            
        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 409
            
        # Create new individual user
        individual = User(
            email=data['email'],
            password=generate_password_hash(data['password']),
            role='individual',
            name=data['name'],
            phone=data['phone'],
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date(),
            medical_condition=data['medical_condition']
        )
        
        db.session.add(individual)
        db.session.commit()
        
        return jsonify({
            'message': 'Individual registered successfully. Please wait for admin verification.',
            'individual_id': individual.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/register/donor', methods=['POST'])
def register_donor():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'name', 'phone']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
            
        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 409
            
        # Create new donor user
        donor = User(
            email=data['email'],
            password=generate_password_hash(data['password']),
            role='donor',
            name=data['name'],
            phone=data['phone']
        )
        
        db.session.add(donor)
        db.session.commit()
        
        return jsonify({
            'message': 'Donor registered successfully',
            'donor_id': donor.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/register/healthcare-provider', methods=['POST'])
def register_healthcare_provider():
    try:
        # Log the raw request data
        logger.debug(f"Raw request data: {request.get_data()}")
        
        # Get and validate JSON data
        if not request.is_json:
            logger.error("Request is not JSON")
            return jsonify({'error': 'Request must be JSON'}), 400
            
        data = request.get_json()
        logger.debug(f"Received healthcare provider registration data: {data}")
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'license_number', 'professional_type', 'specialization', 'hospital_affiliation']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            logger.error(f"Missing required fields: {missing_fields}")
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
            
        # Check if email already exists
        existing_provider = HealthcareProfessional.query.filter_by(email=data['email']).first()
        if existing_provider:
            logger.info(f"Registration attempt with existing email: {data['email']}")
            return jsonify({
                'error': 'This email is already registered. Please use your existing PIN to access your records.',
                'status': 'already_registered'
            }), 409
            
        # Generate PIN
        pin = secrets.randbelow(1000000)
        pin_str = str(pin).zfill(6)
        logger.info(f"Generated PIN for new healthcare provider: {pin_str}")
        
        try:
            # Create new healthcare provider with only required fields
            new_provider = HealthcareProfessional(
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                license_number=data['license_number'],
                professional_type=data['professional_type'],
                specialization=data['specialization'],
                hospital_affiliation=data['hospital_affiliation'],
                is_verified=True,  # Auto-verify healthcare providers
                pin=pin_str  # Store the PIN
            )
            
            # Add optional fields if provided
            optional_fields = ['address', 'city', 'state', 'postal_code', 'country', 
                             'website', 'qualifications', 'experience']
            for field in optional_fields:
                if field in data and data[field]:
                    setattr(new_provider, field, data[field])
            
            logger.info("Attempting to add healthcare provider to database session")
            db.session.add(new_provider)
            
            logger.info("Attempting to commit healthcare provider to database")
            db.session.commit()
            logger.info(f"Successfully committed healthcare provider with ID: {new_provider.id}, PIN: {pin_str}")
            
            # Send email with PIN
            try:
                logger.info(f"Attempting to send email to {data['email']}")
                msg = Message('Your MamaCare Healthcare Provider PIN',
                             sender=app.config['MAIL_USERNAME'],
                             recipients=[data['email']])
                msg.body = f'''Welcome to MamaCare Healthcare Provider Portal!

Your PIN is: {pin_str}

This is your permanent PIN for accessing patient medical records. Please keep it safe as you will need it to access records at any time. This PIN will remain valid indefinitely.

Best regards,
MamaCare Team'''
                
                mail.send(msg)
                logger.info(f"Email sent successfully to {data['email']}")
                
            except Exception as e:
                logger.error(f"Failed to send email: {str(e)}")
                # Don't return error if email fails, just log it
            
            return jsonify({
                'message': 'Healthcare provider registered successfully',
                'pin': pin_str,
                'provider_id': new_provider.id
            }), 201
            
        except Exception as db_error:
            logger.error(f"Database error: {str(db_error)}")
            db.session.rollback()
            return jsonify({'error': f'Database error: {str(db_error)}'}), 500
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/healthcare-provider/pin/<pin>', methods=['GET'])
def get_healthcare_provider_by_pin(pin):
    try:
        provider = HealthcareProfessional.query.filter_by(pin=pin).first()
        if not provider:
            return jsonify({'error': 'Invalid PIN'}), 401
            
        return jsonify({
            'id': provider.id,
            'name': provider.name,
            'email': provider.email,
            'phone': provider.phone,
            'professional_type': provider.professional_type,
            'specialization': provider.specialization,
            'hospital_affiliation': provider.hospital_affiliation,
            'is_verified': provider.is_verified
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting healthcare provider by PIN: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Campaign endpoints
@app.route('/api/campaigns', methods=['POST'])
@hospital_required
def create_campaign():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'target_amount', 'deadline']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
            
        # Create new campaign
        campaign = Campaign(
            title=data['title'],
            description=data['description'],
            target_amount=float(data['target_amount']),
            deadline=datetime.strptime(data['deadline'], '%Y-%m-%d'),
            creator_id=current_user.id
        )
        
        db.session.add(campaign)
        db.session.commit()
        
        return jsonify({
            'message': 'Campaign created successfully',
            'campaign_id': campaign.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/campaigns', methods=['GET'])
def get_campaigns():
    try:
        # Get query parameters
        status = request.args.get('status', 'active')
        role = request.args.get('role')
        
        # Build query
        query = Campaign.query
        
        if status:
            query = query.filter_by(status=status)
            
        if role and current_user.is_authenticated:
            if role == 'my_campaigns':
                query = query.filter_by(creator_id=current_user.id)
            elif role == 'my_donations':
                query = query.join(Donation).filter_by(donor_id=current_user.id)
        
        campaigns = query.all()
        
        return jsonify([{
            'id': campaign.id,
            'title': campaign.title,
            'description': campaign.description,
            'target_amount': campaign.target_amount,
            'current_amount': campaign.current_amount,
            'status': campaign.status,
            'deadline': campaign.deadline.strftime('%Y-%m-%d'),
            'creator': {
                'id': campaign.creator.id,
                'name': campaign.creator.name,
                'role': campaign.creator.role
            }
        } for campaign in campaigns])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Donation endpoints
@app.route('/api/donations', methods=['POST'])
@donor_required
def create_donation():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['amount', 'payment_method', 'campaign_id']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
            
        # Validate campaign exists and is active
        campaign = Campaign.query.get_or_404(data['campaign_id'])
        if campaign.status != 'active':
            return jsonify({'error': 'Campaign is not active'}), 400
            
        # Generate transaction ID
        transaction_id = f"TRX{int(time.time())}{random.randint(1000, 9999)}"
        
        # Create new donation
        donation = Donation(
            amount=float(data['amount']),
            payment_method=data['payment_method'],
            transaction_id=transaction_id,
            donor_id=current_user.id,
            campaign_id=campaign.id
        )
        
        db.session.add(donation)
        
        # Update campaign current amount
        campaign.current_amount += float(data['amount'])
        
        # Check if campaign is completed
        if campaign.current_amount >= campaign.target_amount:
            campaign.status = 'completed'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Donation initiated successfully',
            'transaction_id': transaction_id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Withdrawal endpoints
@app.route('/api/withdrawals', methods=['POST'])
@hospital_required
def request_withdrawal():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['amount', 'campaign_id']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
            
        # Validate campaign exists and belongs to hospital
        campaign = Campaign.query.get_or_404(data['campaign_id'])
        if campaign.creator_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
            
        # Validate withdrawal amount
        if float(data['amount']) > campaign.current_amount:
            return jsonify({'error': 'Insufficient funds'}), 400
            
        # Create withdrawal request
        withdrawal = WithdrawalRequest(
            amount=float(data['amount']),
            hospital_id=current_user.id,
            campaign_id=campaign.id
        )
        
        db.session.add(withdrawal)
        db.session.commit()
        
        return jsonify({
            'message': 'Withdrawal request submitted successfully',
            'withdrawal_id': withdrawal.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Admin endpoints
@app.route('/api/admin/verify/<int:user_id>', methods=['POST'])
@admin_required
def verify_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        
        if user.is_verified:
            return jsonify({'error': 'User already verified'}), 400
            
        user.is_verified = True
        db.session.commit()
        
        return jsonify({
            'message': 'User verified successfully',
            'user_id': user.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/withdrawals/<int:withdrawal_id>', methods=['POST'])
@admin_required
def process_withdrawal(withdrawal_id):
    try:
        withdrawal = WithdrawalRequest.query.get_or_404(withdrawal_id)
        
        if withdrawal.status != 'pending':
            return jsonify({'error': 'Withdrawal already processed'}), 400
            
        data = request.get_json()
        action = data.get('action')
        
        if action not in ['approve', 'reject']:
            return jsonify({'error': 'Invalid action'}), 400
            
        withdrawal.status = 'approved' if action == 'approve' else 'rejected'
        withdrawal.processed_at = datetime.utcnow()
        
        if action == 'reject':
            # Return funds to campaign
            campaign = withdrawal.campaign
            campaign.current_amount += withdrawal.amount
            
        db.session.commit()
        
        return jsonify({
            'message': f'Withdrawal {action}ed successfully',
            'withdrawal_id': withdrawal.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/campaigns/<int:campaign_id>', methods=['POST'])
@admin_required
def review_campaign(campaign_id):
    try:
        campaign = Campaign.query.get_or_404(campaign_id)
        
        data = request.get_json()
        action = data.get('action')
        
        if action not in ['verify', 'suspend']:
            return jsonify({'error': 'Invalid action'}), 400
            
        if action == 'verify':
            campaign.is_verified = True
        else:
            campaign.status = 'suspended'
            
        db.session.commit()
        
        return jsonify({
            'message': f'Campaign {action}ed successfully',
            'campaign_id': campaign.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/hospitals', methods=['POST'])
@admin_required
def add_hospital():
    try:
        data = request.form.to_dict()
        image = request.files.get('image')
        
        # Validate required fields
        required_fields = ['name', 'license_number', 'email', 'phone', 'address', 'city', 'state', 'postal_code', 'country']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        # Check if hospital with same license number or email already exists
        existing_hospital = Hospital.query.filter(
            (Hospital.license_number == data['license_number']) |
            (Hospital.email == data['email'])
        ).first()
        
        if existing_hospital:
            return jsonify({'error': 'Hospital with this license number or email already exists'}), 400

        # Handle image upload
        image_url = None
        if image:
            # Create uploads directory if it doesn't exist
            upload_dir = os.path.join('static', 'uploads', 'hospitals')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Generate unique filename
            filename = secure_filename(f"{data['license_number']}_{image.filename}")
            image_path = os.path.join(upload_dir, filename)
            
            # Save the image
            image.save(image_path)
            image_url = f"/static/uploads/hospitals/{filename}"

        # Parse services
        services = data.get('services', '')
        if services:
            try:
                services = json.loads(services)
            except json.JSONDecodeError:
                services = [s.strip() for s in services.split('\n') if s.strip()]

        new_hospital = Hospital(
            name=data['name'],
            license_number=data['license_number'],
            email=data['email'],
            phone=data['phone'],
            address=data['address'],
            city=data['city'],
            state=data['state'],
            postal_code=data['postal_code'],
            country=data['country'],
            website=data.get('website'),
            services=json.dumps(services) if services else None,
            image_url=image_url,
            is_verified=data.get('is_verified') == 'on'
        )

        db.session.add(new_hospital)
        db.session.commit()

        return jsonify({'message': 'Hospital added successfully', 'hospital': {
            'id': new_hospital.id,
            'name': new_hospital.name,
            'license_number': new_hospital.license_number,
            'email': new_hospital.email,
            'phone': new_hospital.phone,
            'address': new_hospital.address,
            'city': new_hospital.city,
            'state': new_hospital.state,
            'postal_code': new_hospital.postal_code,
            'country': new_hospital.country,
            'website': new_hospital.website,
            'services': new_hospital.services,
            'image_url': new_hospital.image_url,
            'is_verified': new_hospital.is_verified
        }}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/hospitals', methods=['GET'])
@admin_required
def get_hospitals():
    try:
        hospitals = Hospital.query.all()
        return jsonify([{
            'id': hospital.id,
            'name': hospital.name,
            'license_number': hospital.license_number,
            'address': hospital.address,
            'city': hospital.city,
            'state': hospital.state,
            'postal_code': hospital.postal_code,
            'country': hospital.country,
            'phone': hospital.phone,
            'email': hospital.email,
            'website': hospital.website,
            'services': json.loads(hospital.services) if hospital.services else [],
            'image_url': hospital.image_url,
            'is_verified': hospital.is_verified,
            'created_at': hospital.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': hospital.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        } for hospital in hospitals])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/pharmacies', methods=['POST'])
@admin_required
def add_pharmacy():
    try:
        data = request.form.to_dict()
        
        # Validate required fields
        required_fields = ['name', 'license_number', 'address', 'city', 'state', 
                         'postal_code', 'country', 'phone', 'email']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
            
        # Check if pharmacy already exists
        if Pharmacy.query.filter_by(license_number=data['license_number']).first():
            return jsonify({'error': 'Pharmacy with this license number already exists'}), 409
            
        if Pharmacy.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Pharmacy with this email already exists'}), 409
            
        # Create new pharmacy
        pharmacy = Pharmacy(
            name=data['name'],
            license_number=data['license_number'],
            address=data['address'],
            city=data['city'],
            state=data['state'],
            postal_code=data['postal_code'],
            country=data['country'],
            phone=data['phone'],
            email=data['email'],
            website=data.get('website'),
            is_24_hours=data.get('is_24_hours') == 'on',
            is_verified=data.get('is_verified') == 'on'
        )
        
        db.session.add(pharmacy)
        db.session.commit()
        
        return jsonify({
            'message': 'Pharmacy added successfully',
            'pharmacy': {
                'id': pharmacy.id,
                'name': pharmacy.name,
                'license_number': pharmacy.license_number,
                'email': pharmacy.email,
                'phone': pharmacy.phone,
                'address': pharmacy.address,
                'city': pharmacy.city,
                'state': pharmacy.state,
                'postal_code': pharmacy.postal_code,
                'country': pharmacy.country,
                'website': pharmacy.website,
                'is_24_hours': pharmacy.is_24_hours,
                'is_verified': pharmacy.is_verified
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error adding pharmacy: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/pharmacies', methods=['GET'])
@admin_required
def get_pharmacies():
    try:
        pharmacies = Pharmacy.query.all()
        return jsonify([{
            'id': pharmacy.id,
            'name': pharmacy.name,
            'license_number': pharmacy.license_number,
            'address': pharmacy.address,
            'city': pharmacy.city,
            'state': pharmacy.state,
            'postal_code': pharmacy.postal_code,
            'country': pharmacy.country,
            'phone': pharmacy.phone,
            'email': pharmacy.email,
            'website': pharmacy.website,
            'is_24_hours': pharmacy.is_24_hours,
            'is_verified': pharmacy.is_verified,
            'created_at': pharmacy.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': pharmacy.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        } for pharmacy in pharmacies])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/hospitals/<int:hospital_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def update_hospital(hospital_id):
    hospital = Hospital.query.get_or_404(hospital_id)
    
    if request.method == 'GET':
        return jsonify({
            'id': hospital.id,
            'name': hospital.name,
            'license_number': hospital.license_number,
            'address': hospital.address,
            'city': hospital.city,
            'state': hospital.state,
            'postal_code': hospital.postal_code,
            'country': hospital.country,
            'phone': hospital.phone,
            'email': hospital.email,
            'website': hospital.website,
            'services': json.loads(hospital.services) if hospital.services else [],
            'image_url': hospital.image_url,
            'is_verified': hospital.is_verified,
            'created_at': hospital.created_at.isoformat(),
            'updated_at': hospital.updated_at.isoformat()
        })
    
    elif request.method == 'PUT':
        try:
            # Handle both form data and JSON data
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()
                
            image = request.files.get('image')

            # Handle image upload
            if image:
                # Create uploads directory if it doesn't exist
                upload_dir = os.path.join('static', 'uploads', 'hospitals')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Generate unique filename
                filename = secure_filename(f"{hospital.license_number}_{image.filename}")
                image_path = os.path.join(upload_dir, filename)
                
                # Save the image
                image.save(image_path)
                hospital.image_url = f"/static/uploads/hospitals/{filename}"

            # Update fields
            hospital.name = data.get('name', hospital.name)
            hospital.license_number = data.get('license_number', hospital.license_number)
            hospital.email = data.get('email', hospital.email)
            hospital.phone = data.get('phone', hospital.phone)
            hospital.address = data.get('address', hospital.address)
            hospital.city = data.get('city', hospital.city)
            hospital.state = data.get('state', hospital.state)
            hospital.postal_code = data.get('postal_code', hospital.postal_code)
            hospital.country = data.get('country', hospital.country)
            hospital.website = data.get('website', hospital.website)
            
            # Handle is_verified field properly for both form and JSON data
            if 'is_verified' in data:
                if isinstance(data['is_verified'], bool):
                    hospital.is_verified = data['is_verified']
                else:
                    hospital.is_verified = data['is_verified'] == 'on'

            # Update services if provided
            if 'services' in data:
                if isinstance(data['services'], list):
                    # If services is already a list, convert it to JSON string
                    hospital.services = json.dumps(data['services'])
                else:
                    try:
                        services = json.loads(data['services'])
                    except json.JSONDecodeError:
                        services = [s.strip() for s in data['services'].split('\n') if s.strip()]
                    hospital.services = json.dumps(services)

            db.session.commit()
            return jsonify({'message': 'Hospital updated successfully'}), 200

        except Exception as e:
            db.session.rollback()
            logger.error(f'Error updating hospital: {str(e)}')
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(hospital)
            db.session.commit()
            return jsonify({'message': 'Hospital deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

@app.route('/api/admin/pharmacies/<int:pharmacy_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def update_pharmacy(pharmacy_id):
    pharmacy = Pharmacy.query.get_or_404(pharmacy_id)
    
    if request.method == 'GET':
        return jsonify({
            'id': pharmacy.id,
            'name': pharmacy.name,
            'license_number': pharmacy.license_number,
            'address': pharmacy.address,
            'city': pharmacy.city,
            'state': pharmacy.state,
            'postal_code': pharmacy.postal_code,
            'country': pharmacy.country,
            'phone': pharmacy.phone,
            'email': pharmacy.email,
            'website': pharmacy.website,
            'is_24_hours': pharmacy.is_24_hours,
            'is_verified': pharmacy.is_verified,
            'created_at': pharmacy.created_at.isoformat(),
            'updated_at': pharmacy.updated_at.isoformat()
        })
    
    elif request.method == 'PUT':
        try:
            # Handle both form data and JSON data
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()
            
            # Update fields
            pharmacy.name = data.get('name', pharmacy.name)
            pharmacy.license_number = data.get('license_number', pharmacy.license_number)
            pharmacy.email = data.get('email', pharmacy.email)
            pharmacy.phone = data.get('phone', pharmacy.phone)
            pharmacy.address = data.get('address', pharmacy.address)
            pharmacy.city = data.get('city', pharmacy.city)
            pharmacy.state = data.get('state', pharmacy.state)
            pharmacy.postal_code = data.get('postal_code', pharmacy.postal_code)
            pharmacy.country = data.get('country', pharmacy.country)
            pharmacy.website = data.get('website', pharmacy.website)
            
            # Handle is_24_hours field properly for both form and JSON data
            if 'is_24_hours' in data:
                if isinstance(data['is_24_hours'], bool):
                    pharmacy.is_24_hours = data['is_24_hours']
                else:
                    pharmacy.is_24_hours = data['is_24_hours'] == 'on'
            
            # Handle is_verified field properly for both form and JSON data
            if 'is_verified' in data:
                if isinstance(data['is_verified'], bool):
                    pharmacy.is_verified = data['is_verified']
                else:
                    pharmacy.is_verified = data['is_verified'] == 'on'
            
            db.session.commit()
            return jsonify({'message': 'Pharmacy updated successfully'}), 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error updating pharmacy: {str(e)}')
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(pharmacy)
            db.session.commit()
            return jsonify({'message': 'Pharmacy deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

@app.route('/api/admin/hospitals/<int:hospital_id>', methods=['DELETE'])
@admin_required
def delete_hospital(hospital_id):
    try:
        hospital = Hospital.query.get_or_404(hospital_id)
        db.session.delete(hospital)
        db.session.commit()
        return jsonify({'message': 'Hospital deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/pharmacies/<int:pharmacy_id>', methods=['DELETE'])
@admin_required
def delete_pharmacy(pharmacy_id):
    try:
        pharmacy = Pharmacy.query.get_or_404(pharmacy_id)
        db.session.delete(pharmacy)
        db.session.commit()
        return jsonify({'message': 'Pharmacy deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def create_fhir_patient(user_data):
    """Create a FHIR Patient resource from user data"""
    patient = Patient()
    
    # Set name
    name = HumanName()
    name.family = user_data.get('family_name', '')
    name.given = [user_data.get('given_name', '')]
    patient.name = [name]
    
    # Set gender
    gender_map = {
        'male': 'male',
        'female': 'female',
        'other': 'other',
        'unknown': 'unknown'
    }
    patient.gender = gender_map.get(user_data.get('gender', '').lower(), 'unknown')
    
    # Set birth date
    if user_data.get('date_of_birth'):
        patient.birthDate = user_data['date_of_birth']
    
    # Set contact information
    if user_data.get('phone'):
        phone = ContactPoint()
        phone.system = 'phone'
        phone.value = user_data['phone']
        patient.telecom = [phone]
    
    # Set address
    if user_data.get('address_line'):
        address = Address()
        address.line = [user_data['address_line']]
        address.city = user_data.get('city', '')
        address.state = user_data.get('state', '')
        address.postalCode = user_data.get('postal_code', '')
        address.country = user_data.get('country', '')
        patient.address = [address]
    
    # Set identifier
    identifier = Identifier()
    identifier.system = 'urn:mamacare:patients'
    identifier.value = str(user_data.get('id', ''))
    patient.identifier = [identifier]
    
    return patient

@app.route('/api/patient/register', methods=['POST'])
def register_patient():
    try:
        data = request.json
        logger.debug(f"Received registration data: {data}")
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            logger.info(f"Registration attempt with existing email: {data['email']}")
            return jsonify({
                'error': 'This email is already registered. Please use your existing PIN to access your records.',
                'status': 'already_registered'
            }), 409
        
        required_fields = ['email', 'name', 'given_name', 'family_name', 'gender', 
                         'date_of_birth', 'phone', 'address_line', 'city', 'state', 
                         'postal_code', 'country']
        
        if not all(key in data for key in required_fields):
            missing_fields = [field for field in required_fields if field not in data]
            logger.error(f"Missing required fields: {missing_fields}")
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
            
        # Generate PIN
        pin = secrets.randbelow(1000000)
        pin_str = str(pin).zfill(6)
        logger.info(f"Generated PIN for new user: {pin_str}")
        
        logger.info(f"Creating new user with email: {data['email']}")
    
        # Create new user with all FHIR-compliant fields
        user_data = {
            'email': data['email'],
            'password': generate_password_hash(pin_str),  # Use PIN as initial password
            'role': 'individual',  # Set role as individual
            'is_verified': True,  # Auto-verify patient registrations
            'pin': pin_str,
            'name': data['name'],
            'given_name': data['given_name'],
            'family_name': data['family_name'],
            'date_of_birth': datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date(),
            'gender': data['gender'],
            'phone': data['phone'],
            'address_line': data['address_line'],
            'city': data['city'],
            'state': data['state'],
            'postal_code': data['postal_code'],
            'country': data['country'],
            'marital_status': data.get('marital_status'),
            'language': data.get('language', 'en'),
            'nationality': data.get('nationality'),
            'blood_type': data.get('blood_type'),
            'allergies': data.get('allergies'),
            'medications': data.get('medications'),
            'emergency_contact_name': data['emergency_contact_name'],
            'emergency_contact_phone': data['emergency_contact_phone'],
            'emergency_contact_relationship': data['emergency_contact_relationship']
        }

        # Only add pregnancy-related fields if the patient is female
        if data['gender'].lower() == 'female':
            lmp_date = None
            if data.get('lmp_date'):
                try:
                    lmp_date = datetime.strptime(data['lmp_date'], '%Y-%m-%d').date()
                    gestational_age = calculate_gestational_age(lmp_date)
                    due_date = calculate_due_date(lmp_date)
                except ValueError:
                    logger.error(f"Invalid LMP date format: {data['lmp_date']}")
                    return jsonify({'error': 'Invalid LMP date format. Please use YYYY-MM-DD format.'}), 400
            else:
                gestational_age = None
                due_date = None

            user_data.update({
                'pregnancy_status': data.get('pregnancy_status', 'not_pregnant'),
                'previous_pregnancies': int(data.get('previous_pregnancies', 0)) if data.get('previous_pregnancies') else None,
                'lmp_date': lmp_date,
                'due_date': due_date,  # This is now calculated, not input
                'gestational_age': gestational_age,  # This is now calculated, not input
                'multiple_pregnancy': data.get('multiple_pregnancy'),
                'risk_level': data.get('risk_level'),
                'risk_factors': json.dumps(data.get('risk_factors', [])),
                'blood_pressure': data.get('blood_pressure'),
                'hemoglobin': float(data.get('hemoglobin', 0)) if data.get('hemoglobin') else None,
                'blood_sugar': float(data.get('blood_sugar', 0)) if data.get('blood_sugar') else None,
                'weight': float(data.get('weight', 0)) if data.get('weight') else None,
                'prenatal_vitamins': data.get('prenatal_vitamins'),
                'pregnancy_complications': data.get('pregnancy_complications'),
                'emergency_hospital': data.get('emergency_hospital'),
                'birth_plan': data.get('birth_plan')
            })
        
        new_user = User(**user_data)
        
        logger.info("Attempting to add user to database session")
        db.session.add(new_user)
        
        logger.info("Attempting to commit user to database")
        db.session.commit()
        logger.info(f"Successfully committed user with ID: {new_user.id}, PIN: {new_user.pin}")
        
        # Create FHIR Patient resource
        logger.info("Creating FHIR Patient resource")
        fhir_patient = create_fhir_patient(data)
        fhir_patient.id = str(new_user.id)
        new_user.fhir_id = fhir_patient.id
        
        logger.info("Attempting to commit FHIR ID to database")
        db.session.commit()
        logger.info(f"Successfully committed FHIR ID: {fhir_patient.id}")
    
        # Send email with PIN
        email_sent = True
        email_error = None
        try:
            logger.info(f"Attempting to send email to {data['email']}")
            msg = Message('Your MamaCare PIN',
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[data['email']])
            msg.body = f'''Welcome to MamaCare!

Your PIN is: {pin_str}

This is your permanent PIN for accessing your medical records. Please keep it safe as you will need it to access your medical records at any time. This PIN will remain valid indefinitely.

Best regards,
MamaCare Team'''
            mail.send(msg)
            logger.info(f"Email sent successfully to {data['email']}")
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            print(f"EMAIL ERROR: {str(e)}")
            email_sent = False
            email_error = str(e)
        
        response = {
            'message': 'Patient registered successfully',
            'pin': pin_str,
            'patient_id': new_user.id,
            'fhir_id': new_user.fhir_id,
            'due_date': new_user.due_date.strftime('%Y-%m-%d') if new_user.due_date else None,
            'gestational_age': new_user.gestational_age,
            'email_sent': email_sent
        }
        if not email_sent:
            response['email_error'] = email_error
            response['note'] = f'Email could not be sent, but your PIN is: {pin_str}. Please save this PIN for future access.'
        return jsonify(response), 201
            
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error details: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/patient/profile', methods=['GET', 'POST', 'PUT'])
def get_patient_profile():
    try:
        # Get PIN from either query parameters (GET) or request body (POST/PUT)
        if request.method == 'GET':
            pin = request.args.get('pin')
        else:
            data = request.get_json()
            pin = data.get('pin')

        if not pin:
            return jsonify({'error': 'PIN is required'}), 400

        # Find user by PIN
        user = User.query.filter_by(pin=pin).first()
        if not user:
            return jsonify({'error': 'Invalid PIN'}), 401

        # Handle profile update for PUT requests
        if request.method == 'PUT':
            data = request.get_json()
            logger.info(f"Received profile update data: {data}")
            
            # Update user fields - only update fields that are provided
            updateable_fields = [
                'name', 'email', 'phone', 'gender', 'date_of_birth', 'address_line',
                'city', 'state', 'postal_code', 'country', 'blood_type', 'allergies',
                'medications', 'emergency_contact_name', 'emergency_contact_phone',
                'emergency_contact_relationship', 'marital_status', 'language',
                'nationality'
            ]
            
            for field in updateable_fields:
                if field in data and data[field] is not None:
                    try:
                        setattr(user, field, data[field])
                        logger.debug(f"Updated field {field} to {data[field]}")
                    except Exception as e:
                        logger.error(f"Error updating field {field}: {str(e)}")
                        return jsonify({'error': f'Error updating field {field}: {str(e)}'}), 500

            # Handle date fields
            if 'date_of_birth' in data and data['date_of_birth']:
                try:
                    user.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
                    logger.debug(f"Updated date_of_birth to {user.date_of_birth}")
                except ValueError:
                    logger.error(f"Invalid date format for date_of_birth: {data['date_of_birth']}")
                    return jsonify({'error': 'Invalid date format for date_of_birth. Use YYYY-MM-DD format.'}), 400
            
            # Handle pregnancy-related fields if gender is female
            if user.gender and user.gender.lower() == 'female':
                pregnancy_fields = [
                    'pregnancy_status', 'previous_pregnancies', 'lmp_date', 'due_date',
                    'gestational_age', 'multiple_pregnancy', 'risk_level', 'risk_factors',
                    'blood_pressure', 'hemoglobin', 'blood_sugar', 'weight',
                    'prenatal_vitamins', 'pregnancy_complications', 'emergency_hospital',
                    'birth_plan'
                ]
                
                for field in pregnancy_fields:
                    if field in data:
                        if field == 'lmp_date' and data[field]:
                            user.lmp_date = datetime.strptime(data[field], '%Y-%m-%d').date()
                        elif field == 'due_date' and data[field]:
                            user.due_date = datetime.strptime(data[field], '%Y-%m-%d').date()
                        elif field == 'risk_factors':
                            user.risk_factors = json.dumps(data[field])
                        elif field in ['hemoglobin', 'blood_sugar', 'weight']:
                            # Only update numeric fields if a valid value is provided
                            if data[field] and str(data[field]).strip():
                                try:
                                    setattr(user, field, float(data[field]))
                                except (ValueError, TypeError):
                                    # If conversion fails, keep the existing value
                                    pass
                        else:
                            setattr(user, field, data[field])

            try:
                logger.info("Attempting to commit profile changes to database")
                db.session.commit()
                logger.info("Successfully committed profile changes to database")
            except Exception as e:
                logger.error(f"Database error during profile update: {str(e)}")
                db.session.rollback()
                return jsonify({'error': f'Database error: {str(e)}'}), 500

        # Return user profile data
        response_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'gender': user.gender,
            'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d') if user.date_of_birth else None,
            'address_line': user.address_line,
            'city': user.city,
            'state': user.state,
            'postal_code': user.postal_code,
            'country': user.country,
            'blood_type': user.blood_type,
            'allergies': user.allergies,
            'medications': user.medications,
            'emergency_contact_name': user.emergency_contact_name,
            'emergency_contact_phone': user.emergency_contact_phone,
            'emergency_contact_relationship': user.emergency_contact_relationship,
            'marital_status': user.marital_status,
            'language': user.language,
            'nationality': user.nationality,
            'fhir_id': user.fhir_id
        }

        # Add pregnancy-related fields if the user is female
        if user.gender and user.gender.lower() == 'female':
            response_data.update({
                'pregnancy_status': user.pregnancy_status,
                'previous_pregnancies': user.previous_pregnancies,
                'lmp_date': user.lmp_date.strftime('%Y-%m-%d') if user.lmp_date else None,
                'due_date': user.due_date.strftime('%Y-%m-%d') if user.due_date else None,
                'gestational_age': user.gestational_age,
                'multiple_pregnancy': user.multiple_pregnancy,
                'risk_level': user.risk_level,
                'risk_factors': json.loads(user.risk_factors) if user.risk_factors else [],
                'blood_pressure': user.blood_pressure,
                'hemoglobin': user.hemoglobin,
                'blood_sugar': user.blood_sugar,
                'weight': user.weight,
                'prenatal_vitamins': user.prenatal_vitamins,
                'pregnancy_complications': user.pregnancy_complications,
                'emergency_hospital': user.emergency_hospital,
                'birth_plan': user.birth_plan
            })

        return jsonify(response_data), 200

    except Exception as e:
        logger.error(f"Error in patient profile endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/patient/medical-records', methods=['POST'])
def add_medical_record():
    try:
        data = request.json
        logger.debug(f"Received medical record data: {data}")
        
        if not data or 'pin' not in data:
            return jsonify({'error': 'PIN is required'}), 400
            
        # Find user by PIN
        user = User.query.filter_by(pin=data['pin']).first()
        if not user:
            return jsonify({'error': 'Invalid PIN'}), 401
        
        # Create new medical record
        record = MedicalRecord(
            user_id=user.id,
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            diagnosis=data['diagnosis'],
            treatment=data['treatment'],
            medication=data.get('medication'),
            doctor=data['doctor'],
            hospital=data['hospital']
        )
        
        db.session.add(record)
        db.session.commit()
        
        # Create FHIR Observation for the medical record
        if user.fhir_id:
            try:
                observation = Observation()
                observation.status = 'final'
                observation.code = {
                    'coding': [{
                        'system': 'http://loinc.org',
                        'code': '11526-1',
                        'display': 'Progress note'
                    }]
                }
                observation.subject = {'reference': f'Patient/{user.fhir_id}'}
                observation.valueString = f"Diagnosis: {data['diagnosis']}\nTreatment: {data['treatment']}\nMedication: {data.get('medication', 'N/A')}\nDoctor: {data['doctor']}\nHospital: {data['hospital']}"
                observation.effectiveDateTime = data['date']
                
                observation.save(fhir_client.server)
                logger.info(f"Created FHIR Observation for medical record {record.id}")
            except Exception as e:
                logger.error(f"Error creating FHIR Observation: {str(e)}")
    
        return jsonify({
            'id': record.id,
            'date': record.date.strftime('%Y-%m-%d'),
            'diagnosis': record.diagnosis,
            'treatment': record.treatment,
            'medication': record.medication,
            'doctor': record.doctor,
            'hospital': record.hospital
        })
    except Exception as e:
        logger.error(f"Error in add_medical_record: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/patient/medical-records/<int:record_id>', methods=['DELETE'])
def delete_medical_record(record_id):
    try:
        record = MedicalRecord.query.get_or_404(record_id)
        user = User.query.get(record.user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        # Store record details before deletion for email
        record_details = {
            'date': record.date.strftime('%Y-%m-%d'),
            'diagnosis': record.diagnosis,
            'treatment': record.treatment,
            'medication': record.medication,
            'doctor': record.doctor,
            'hospital': record.hospital
        }
        
        # Delete the record
        db.session.delete(record)
        db.session.commit()
        
        # Send email notification
        try:
            msg = Message('Medical Record Deletion Notification',
                         sender=app.config['MAIL_USERNAME'],
                         recipients=[user.email])
            msg.body = f'''Dear {user.name},

A medical record has been deleted from your profile. Here are the details of the deleted record:

Date: {record_details['date']}
Diagnosis: {record_details['diagnosis']}
Treatment: {record_details['treatment']}
Medication: {record_details['medication'] or 'N/A'}
Doctor: {record_details['doctor']}
Hospital: {record_details['hospital']}

If you did not authorize this deletion, please contact us immediately.

Best regards,
MamaCare Team'''
            
            mail.send(msg)
            logger.info(f"Deletion notification email sent to {user.email}")
            
        except Exception as e:
            logger.error(f"Failed to send deletion notification email: {str(e)}")
            # Continue with the deletion even if email fails
        
        return jsonify({'message': 'Record deleted successfully'})
    except Exception as e:
        logger.error(f"Error in delete_medical_record: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

# Add this new endpoint for debugging
@app.route('/api/debug/pins', methods=['GET'])
def debug_pins():
    try:
        users = User.query.all()
        pins = [{'id': user.id, 'email': user.email, 'pin': user.pin} for user in users]
        return jsonify({'pins': pins})
    except Exception as e:
        logger.error(f"Error in debug_pins: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/patient/medical-records', methods=['GET'])
def get_medical_records():
    try:
        pin = request.args.get('pin')
        if not pin:
            return jsonify({'error': 'PIN is required'}), 400

        pin = pin.strip()
        
        # Validate PIN format
        if not pin.isdigit() or len(pin) != 6:
            return jsonify({'error': 'Invalid PIN format. PIN must be exactly 6 digits.'}), 400

        # Find user by PIN
        user = User.query.filter_by(pin=pin).first()
        if not user:
            return jsonify({'error': 'Invalid PIN'}), 401

        # Get user's medical records
        records = MedicalRecord.query.filter_by(user_id=user.id).all()
        
        return jsonify([{
            'id': record.id,
            'date': record.date.strftime('%Y-%m-%d'),
            'diagnosis': record.diagnosis,
            'treatment': record.treatment,
            'medication': record.medication,
            'doctor': record.doctor,
            'hospital': record.hospital
        } for record in records])

    except Exception as e:
        logger.error(f"Error in get_medical_records: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# New endpoint for mobile app authentication
@app.route('/api/mobile/auth', methods=['POST'])
def mobile_auth():
    try:
        data = request.get_json()
        if not data or 'pin' not in data:
            return jsonify({'error': 'PIN is required'}), 400

        user = User.query.filter_by(pin=data['pin']).first()
        if not user:
            return jsonify({'error': 'Invalid PIN'}), 401

        # Generate a temporary token (you might want to use JWT in production)
        token = secrets.token_urlsafe(32)
        user.auth_token = token
        user.token_expiry = datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
        db.session.commit()

        return jsonify({
            'token': token,
            'user_id': user.id,
            'name': user.name,
            'email': user.email
        })

    except Exception as e:
        app.logger.error(f"Mobile auth error: {str(e)}")
        return jsonify({'error': 'Authentication failed'}), 500

# New endpoint for mobile app profile data
@app.route('/api/mobile/profile', methods=['GET'])
def mobile_profile():
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Authorization token required'}), 401

        user = User.query.filter_by(auth_token=token).first()
        if not user or user.token_expiry < datetime.utcnow():
            return jsonify({'error': 'Invalid or expired token'}), 401

        # Return profile data in a mobile-friendly format
        return jsonify({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'gender': user.gender,
            'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d') if user.date_of_birth else None,
            'blood_type': user.blood_type,
            'allergies': user.allergies,
            'medications': user.medications,
            'marital_status': user.marital_status,
            'language': user.language,
            'nationality': user.nationality,
            'emergency_contact': {
                'name': user.emergency_contact_name,
                'phone': user.emergency_contact_phone,
                'relationship': user.emergency_contact_relationship
            },
            'pregnancy_info': {
                'status': user.pregnancy_status,
                'previous_pregnancies': user.previous_pregnancies,
                'lmp_date': user.lmp_date.strftime('%Y-%m-%d') if user.lmp_date else None,
                'due_date': user.due_date.strftime('%Y-%m-%d') if user.due_date else None,
                'gestational_age': user.gestational_age,
                'multiple_pregnancy': user.multiple_pregnancy,
                'risk_level': user.risk_level,
                'risk_factors': json.loads(user.risk_factors) if user.risk_factors else [],
                'blood_pressure': user.blood_pressure,
                'hemoglobin': user.hemoglobin,
                'blood_sugar': user.blood_sugar,
                'weight': user.weight,
                'prenatal_vitamins': user.prenatal_vitamins,
                'complications': user.pregnancy_complications,
                'emergency_hospital': user.emergency_hospital,
                'birth_plan': user.birth_plan
            } if user.gender == 'female' else None
        })

    except Exception as e:
        app.logger.error(f"Mobile profile error: {str(e)}")
        return jsonify({'error': 'Failed to fetch profile'}), 500

# New endpoint for mobile app medical records
@app.route('/api/mobile/medical-records', methods=['GET'])
def mobile_medical_records():
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Authorization token required'}), 401

        user = User.query.filter_by(auth_token=token).first()
        if not user or user.token_expiry < datetime.utcnow():
            return jsonify({'error': 'Invalid or expired token'}), 401

        records = MedicalRecord.query.filter_by(user_id=user.id).order_by(MedicalRecord.date.desc()).all()
        
        return jsonify([{
            'id': record.id,
            'date': record.date.strftime('%Y-%m-%d'),
            'diagnosis': record.diagnosis,
            'treatment': record.treatment,
            'medication': record.medication,
            'doctor': record.doctor,
            'hospital': record.hospital
        } for record in records])

    except Exception as e:
        app.logger.error(f"Mobile medical records error: {str(e)}")
        return jsonify({'error': 'Failed to fetch medical records'}), 500

# CSV Export endpoint
@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    try:
        # Get all patients
        patients = User.query.filter_by(role='individual').all()
        
        # Create CSV data
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'ID', 'Name', 'Email', 'Phone', 'Gender', 'Date of Birth',
            'Blood Type', 'Marital Status', 'Language', 'Nationality',
            'Allergies', 'Medications', 'Emergency Contact Name',
            'Emergency Contact Phone', 'Emergency Contact Relationship',
            'Pregnancy Status', 'Previous Pregnancies', 'LMP Date',
            'Due Date', 'Gestational Age', 'Multiple Pregnancy',
            'Risk Level', 'Risk Factors', 'Blood Pressure',
            'Hemoglobin', 'Blood Sugar', 'Weight', 'Prenatal Vitamins',
            'Pregnancy Complications', 'Emergency Hospital', 'Birth Plan'
        ])
        
        # Write data rows
        for patient in patients:
            writer.writerow([
                patient.id,
                patient.name,
                patient.email,
                patient.phone,
                patient.gender,
                patient.date_of_birth.strftime('%Y-%m-%d') if patient.date_of_birth else '',
                patient.blood_type,
                patient.marital_status,
                patient.language,
                patient.nationality,
                patient.allergies,
                patient.medications,
                patient.emergency_contact_name,
                patient.emergency_contact_phone,
                patient.emergency_contact_relationship,
                patient.pregnancy_status,
                patient.previous_pregnancies,
                patient.lmp_date.strftime('%Y-%m-%d') if patient.lmp_date else '',
                patient.due_date.strftime('%Y-%m-%d') if patient.due_date else '',
                patient.gestational_age,
                patient.multiple_pregnancy,
                patient.risk_level,
                patient.risk_factors,
                patient.blood_pressure,
                patient.hemoglobin,
                patient.blood_sugar,
                patient.weight,
                patient.prenatal_vitamins,
                patient.pregnancy_complications,
                patient.emergency_hospital,
                patient.birth_plan
            ])
        
        # Prepare response
        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename=patients_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            }
        )
        
    except Exception as e:
        app.logger.error(f"CSV export error: {str(e)}")
        return jsonify({'error': 'Failed to export CSV'}), 500

# CSV Import endpoint
@app.route('/api/import/csv', methods=['POST'])
def import_csv():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'File must be a CSV'}), 400
            
        # Read CSV file
        stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream)
        
        # Process each row
        for row in csv_reader:
            try:
                # Check if patient exists
                patient = User.query.filter_by(email=row['Email']).first()
                
                if patient:
                    # Update existing patient
                    patient.name = row['Name']
                    patient.phone = row['Phone']
                    patient.gender = row['Gender']
                    patient.date_of_birth = datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date() if row['Date of Birth'] else None
                    patient.blood_type = row['Blood Type']
                    patient.marital_status = row['Marital Status']
                    patient.language = row['Language']
                    patient.nationality = row['Nationality']
                    patient.allergies = row['Allergies']
                    patient.medications = row['Medications']
                    patient.emergency_contact_name = row['Emergency Contact Name']
                    patient.emergency_contact_phone = row['Emergency Contact Phone']
                    patient.emergency_contact_relationship = row['Emergency Contact Relationship']
                    
                    # Update pregnancy information if gender is female
                    if row['Gender'].lower() == 'female':
                        patient.pregnancy_status = row['Pregnancy Status']
                        patient.previous_pregnancies = int(row['Previous Pregnancies']) if row['Previous Pregnancies'] else None
                        patient.lmp_date = datetime.strptime(row['LMP Date'], '%Y-%m-%d').date() if row['LMP Date'] else None
                        patient.due_date = datetime.strptime(row['Due Date'], '%Y-%m-%d').date() if row['Due Date'] else None
                        patient.gestational_age = int(row['Gestational Age']) if row['Gestational Age'] else None
                        patient.multiple_pregnancy = row['Multiple Pregnancy']
                        patient.risk_level = row['Risk Level']
                        patient.risk_factors = row['Risk Factors']
                        patient.blood_pressure = row['Blood Pressure']
                        patient.hemoglobin = float(row['Hemoglobin']) if row['Hemoglobin'] else None
                        patient.blood_sugar = float(row['Blood Sugar']) if row['Blood Sugar'] else None
                        patient.weight = float(row['Weight']) if row['Weight'] else None
                        patient.prenatal_vitamins = row['Prenatal Vitamins']
                        patient.pregnancy_complications = row['Pregnancy Complications']
                        patient.emergency_hospital = row['Emergency Hospital']
                        patient.birth_plan = row['Birth Plan']
                else:
                    # Create new patient
                    new_patient = User(
                        email=row['Email'],
                        name=row['Name'],
                        phone=row['Phone'],
                        gender=row['Gender'],
                        date_of_birth=datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date() if row['Date of Birth'] else None,
                        blood_type=row['Blood Type'],
                        marital_status=row['Marital Status'],
                        language=row['Language'],
                        nationality=row['Nationality'],
                        allergies=row['Allergies'],
                        medications=row['Medications'],
                        emergency_contact_name=row['Emergency Contact Name'],
                        emergency_contact_phone=row['Emergency Contact Phone'],
                        emergency_contact_relationship=row['Emergency Contact Relationship'],
                        role='individual',
                        is_verified=True
                    )
                    
                    # Set pregnancy information if gender is female
                    if row['Gender'].lower() == 'female':
                        new_patient.pregnancy_status = row['Pregnancy Status']
                        new_patient.previous_pregnancies = int(row['Previous Pregnancies']) if row['Previous Pregnancies'] else None
                        new_patient.lmp_date = datetime.strptime(row['LMP Date'], '%Y-%m-%d').date() if row['LMP Date'] else None
                        new_patient.due_date = datetime.strptime(row['Due Date'], '%Y-%m-%d').date() if row['Due Date'] else None
                        new_patient.gestational_age = int(row['Gestational Age']) if row['Gestational Age'] else None
                        new_patient.multiple_pregnancy = row['Multiple Pregnancy']
                        new_patient.risk_level = row['Risk Level']
                        new_patient.risk_factors = row['Risk Factors']
                        new_patient.blood_pressure = row['Blood Pressure']
                        new_patient.hemoglobin = float(row['Hemoglobin']) if row['Hemoglobin'] else None
                        new_patient.blood_sugar = float(row['Blood Sugar']) if row['Blood Sugar'] else None
                        new_patient.weight = float(row['Weight']) if row['Weight'] else None
                        new_patient.prenatal_vitamins = row['Prenatal Vitamins']
                        new_patient.pregnancy_complications = row['Pregnancy Complications']
                        new_patient.emergency_hospital = row['Emergency Hospital']
                        new_patient.birth_plan = row['Birth Plan']
                    
                    db.session.add(new_patient)
                
                db.session.commit()
                
            except Exception as e:
                app.logger.error(f"Error processing row: {str(e)}")
                db.session.rollback()
                continue
        
        return jsonify({'message': 'CSV import completed successfully'})
        
    except Exception as e:
        app.logger.error(f"CSV import error: {str(e)}")
        return jsonify({'error': 'Failed to import CSV'}), 500

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find admin user
        admin = User.query.filter_by(email=email, role='admin').first()
        
        if not admin or not check_password_hash(admin.password, password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not admin.is_verified:
            return jsonify({'error': 'Account not verified. Please contact administrator.'}), 401
        
        # Generate token
        token = secrets.token_urlsafe(32)
        admin.auth_token = token
        admin.token_expiry = datetime.utcnow() + timedelta(hours=24)
        db.session.commit()
        
        return jsonify({
            'token': token,
            'user': {
                'id': admin.id,
                'name': admin.name,
                'email': admin.email,
                'role': admin.role
            }
        }), 200
        
    except Exception as e:
        logger.error(f'Admin login error: {str(e)}')
        return jsonify({'error': 'Login failed'}), 500

@app.route('/api/admin/signup', methods=['POST'])
def admin_signup():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 409
        
        # Validate phone number format (Sierra Leone format)
        phone = data['phone']
        if not phone.startswith('+232') or len(phone) != 12:
            return jsonify({'error': 'Phone number must be in Sierra Leone format (+232XXXXXXXX)'}), 400
        
        # Hash password
        hashed_password = generate_password_hash(data['password'])
        
        # Create new admin user
        new_admin = User(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            password=hashed_password,
            role='admin',
            is_verified=False,  # New admins need verification
            created_at=datetime.utcnow()
        )
        
        db.session.add(new_admin)
        db.session.commit()
        
        # Send notification email to existing admins (optional)
        try:
            existing_admins = User.query.filter_by(role='admin', is_verified=True).all()
            for admin in existing_admins:
                send_admin_notification_email(admin.email, data['name'], data['email'])
        except Exception as e:
            logger.error(f'Failed to send admin notification email: {str(e)}')
        
        return jsonify({
            'message': 'Admin account created successfully. Please wait for verification.',
            'admin_id': new_admin.id
        }), 201
        
    except Exception as e:
        logger.error(f'Admin signup error: {str(e)}')
        db.session.rollback()
        return jsonify({'error': 'Failed to create admin account'}), 500

def send_admin_notification_email(admin_email, new_admin_name, new_admin_email):
    """Send notification email to existing admins about new admin signup"""
    try:
        msg = Message(
            'New Admin Registration',
            recipients=[admin_email]
        )
        msg.body = f"""
        A new admin has registered for MamaCare:
        
        Name: {new_admin_name}
        Email: {new_admin_email}
        
        Please review and verify this account in the admin dashboard.
        """
        mail.send(msg)
    except Exception as e:
        logger.error(f'Failed to send admin notification email: {str(e)}')

@app.route('/api/admin/doctors', methods=['POST'])
@admin_required
def add_doctor():
    try:
        data = request.form.to_dict()
        image = request.files.get('image')
        
        # Validate required fields
        required_fields = ['name', 'license_number', 'email', 'phone', 'professional_type', 'specialization', 'hospital_affiliation']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        # Check if doctor with same license number or email already exists
        existing_doctor = Doctor.query.filter(
            (Doctor.license_number == data['license_number']) |
            (Doctor.email == data['email'])
        ).first()
        
        if existing_doctor:
            return jsonify({'error': 'Doctor with this license number or email already exists'}), 400

        # Handle image upload
        image_url = None
        if image:
            # Create uploads directory if it doesn't exist
            upload_dir = os.path.join('static', 'uploads', 'doctors')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Generate unique filename
            filename = secure_filename(f"{data['license_number']}_{image.filename}")
            image_path = os.path.join(upload_dir, filename)
            
            # Save the image
            image.save(image_path)
            image_url = f"/static/uploads/doctors/{filename}"

        new_doctor = Doctor(
            name=data['name'],
            license_number=data['license_number'],
            email=data['email'],
            phone=data['phone'],
            professional_type=data['professional_type'],
            specialization=data['specialization'],
            hospital_affiliation=data['hospital_affiliation'],
            address=data.get('address'),
            city=data.get('city'),
            state=data.get('state'),
            postal_code=data.get('postal_code'),
            country=data.get('country'),
            website=data.get('website'),
            image_url=image_url,
            qualifications=data.get('qualifications'),
            experience=data.get('experience'),
            is_verified=data.get('is_verified') == 'on'
        )

        db.session.add(new_doctor)
        db.session.commit()

        return jsonify({'message': 'Doctor added successfully', 'doctor': {
            'id': new_doctor.id,
            'name': new_doctor.name,
            'license_number': new_doctor.license_number,
            'email': new_doctor.email,
            'phone': new_doctor.phone,
            'professional_type': new_doctor.professional_type,
            'specialization': new_doctor.specialization,
            'hospital_affiliation': new_doctor.hospital_affiliation,
            'image_url': new_doctor.image_url,
            'is_verified': new_doctor.is_verified
        }}), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding doctor: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/doctors', methods=['GET'])
@admin_required
def get_doctors():
    try:
        doctors = Doctor.query.all()
        return jsonify([{
            'id': doctor.id,
            'name': doctor.name,
            'license_number': doctor.license_number,
            'email': doctor.email,
            'phone': doctor.phone,
            'professional_type': doctor.professional_type,  # Add this line
            'specialization': doctor.specialization,
            'hospital_affiliation': doctor.hospital_affiliation,
            'image_url': doctor.image_url,
            'is_verified': doctor.is_verified,
            'qualifications': doctor.qualifications,
            'experience': doctor.experience,
            'address': doctor.address,
            'city': doctor.city,
            'state': doctor.state,
            'country': doctor.country,
            'website': doctor.website
        } for doctor in doctors]), 200
    except Exception as e:
        logger.error(f'Error getting public doctors: {str(e)}')
        return jsonify({'error': 'Failed to get doctors'}), 500

@app.route('/api/admin/doctors/<int:doctor_id>', methods=['PUT'])
@admin_required
def update_doctor(doctor_id):
    try:
        doctor = Doctor.query.get_or_404(doctor_id)
        data = request.form.to_dict()
        image = request.files.get('image')

        # Handle image upload
        if image:
            # Create uploads directory if it doesn't exist
            upload_dir = os.path.join('static', 'uploads', 'doctors')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Generate unique filename
            filename = secure_filename(f"{doctor.license_number}_{image.filename}")
            image_path = os.path.join(upload_dir, filename)
            
            # Save the image
            image.save(image_path)
            doctor.image_url = f"/static/uploads/doctors/{filename}"

        # Update other fields
        doctor.name = data.get('name', doctor.name)
        doctor.license_number = data.get('license_number', doctor.license_number)
        doctor.email = data.get('email', doctor.email)
        doctor.phone = data.get('phone', doctor.phone)
        doctor.specialization = data.get('specialization', doctor.specialization)
        doctor.hospital_affiliation = data.get('hospital_affiliation', doctor.hospital_affiliation)
        doctor.address = data.get('address', doctor.address)
        doctor.city = data.get('city', doctor.city)
        doctor.state = data.get('state', doctor.state)
        doctor.postal_code = data.get('postal_code', doctor.postal_code)
        doctor.country = data.get('country', doctor.country)
        doctor.website = data.get('website', doctor.website)
        doctor.qualifications = data.get('qualifications', doctor.qualifications)
        doctor.experience = data.get('experience', doctor.experience)
        doctor.is_verified = data.get('is_verified') == 'on'

        db.session.commit()
        return jsonify({'message': 'Doctor updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating doctor: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/doctors/<int:doctor_id>', methods=['DELETE'])
@admin_required
def delete_doctor(doctor_id):
    try:
        doctor = Doctor.query.get_or_404(doctor_id)
        db.session.delete(doctor)
        db.session.commit()
        return jsonify({'message': 'Doctor deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error deleting doctor: {str(e)}')
        return jsonify({'error': 'Failed to delete doctor'}), 500

@app.route('/api/admin/doctors/<int:doctor_id>', methods=['GET'])
@admin_required
def get_doctor(doctor_id):
    try:
        doctor = Doctor.query.get_or_404(doctor_id)
        return jsonify({
            'id': doctor.id,
            'name': doctor.name,
            'license_number': doctor.license_number,
            'specialization': doctor.specialization,
            'email': doctor.email,
            'phone': doctor.phone,
            'hospital_affiliation': doctor.hospital_affiliation,
            'address': doctor.address,
            'city': doctor.city,
            'state': doctor.state,
            'postal_code': doctor.postal_code,
            'country': doctor.country,
            'website': doctor.website,
            'image_url': doctor.image_url,
            'is_verified': doctor.is_verified,
            'qualifications': doctor.qualifications,
            'experience': doctor.experience
        }), 200
    except Exception as e:
        logger.error(f'Error getting doctor: {str(e)}')
        return jsonify({'error': 'Failed to get doctor'}), 500

@app.route('/api/admin/patients/count', methods=['GET'])
@admin_required
def get_patient_count():
    try:
        count = User.query.filter_by(role='individual').count()
        return jsonify({'count': count}), 200
    except Exception as e:
        logger.error(f'Error getting patient count: {str(e)}')
        return jsonify({'error': 'Failed to get patient count'}), 500

def init_db():
    try:
        with app.app_context():
            db.create_all()
            logger.info("Database tables created successfully")
            
            # Check if admin user exists
            admin = User.query.filter_by(email='admin@mamacare.com').first()
            if not admin:
                # Create admin user
                admin = User(
                    email='admin@mamacare.com',
                    password=generate_password_hash('admin123'),
                    role='admin',
                    is_verified=True,
                    name='Admin User',
                    phone='+23212345678'
                )
                db.session.add(admin)
                db.session.commit()
                logger.info("Admin user created successfully")
            else:
                logger.info("Admin user already exists")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

# Call init_db when the application starts
init_db()

@app.route('/api/doctors', methods=['GET'])
def get_public_doctors():
    try:
        doctors = Doctor.query.filter_by(is_verified=True).all()
        return jsonify([{
            'id': doctor.id,
            'name': doctor.name,
            'specialization': doctor.specialization,
            'email': doctor.email,
            'phone': doctor.phone,
            'professional_type': doctor.professional_type,  # Add this line
            'hospital_affiliation': doctor.hospital_affiliation,
            'address': doctor.address,
            'city': doctor.city,
            'state': doctor.state,
            'country': doctor.country,
            'image_url': doctor.image_url,
            'website': doctor.website,
            'qualifications': doctor.qualifications,
            'experience': doctor.experience
        } for doctor in doctors]), 200
    except Exception as e:
        logger.error(f'Error getting public doctors: {str(e)}')
        return jsonify({'error': 'Failed to get doctors'}), 500

@app.route('/api/hospitals', methods=['GET'])
def get_public_hospitals():
    try:
        hospitals = Hospital.query.filter_by(is_verified=True).all()
        return jsonify([{
            'id': hospital.id,
            'name': hospital.name,
            'address': hospital.address,
            'city': hospital.city,
            'state': hospital.state,
            'country': hospital.country,
            'phone': hospital.phone,
            'email': hospital.email,
            'website': hospital.website,
            'services': json.loads(hospital.services) if hospital.services else [],
            'image_url': hospital.image_url
        } for hospital in hospitals]), 200
    except Exception as e:
        logger.error(f'Error getting public hospitals: {str(e)}')
        return jsonify({'error': 'Failed to get hospitals'}), 500

@app.route('/api/pharmacies', methods=['GET'])
def get_public_pharmacies():
    try:
        pharmacies = Pharmacy.query.filter_by(is_verified=True).all()
        return jsonify([{
            'id': pharmacy.id,
            'name': pharmacy.name,
            'address': pharmacy.address,
            'city': pharmacy.city,
            'state': pharmacy.state,
            'country': pharmacy.country,
            'phone': pharmacy.phone,
            'email': pharmacy.email,
            'website': pharmacy.website,
            'is_24_hours': pharmacy.is_24_hours
        } for pharmacy in pharmacies]), 200
    except Exception as e:
        logger.error(f'Error getting public pharmacies: {str(e)}')
        return jsonify({'error': 'Failed to get pharmacies'}), 500

# Remove the before_first_request decorator and replace with a function
def init_app():
    with app.app_context():
        db.create_all()
        logger.info("Database tables created successfully")

# Update the main block
if __name__ == '__main__':
    try:
        logger.info("Starting Flask application...")
        logger.info(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        init_app()  # Initialize the database
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logger.error(f"Application startup error: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error stack: {str(e.__traceback__)}")
        sys.exit(1)

@app.route('/api/admin/hospitals/<int:hospital_id>', methods=['GET', 'PUT', 'DELETE', 'OPTIONS'])
@admin_required
def hospital_detail(hospital_id):
    if request.method == 'OPTIONS':
        return '', 204
        
    hospital = Hospital.query.get_or_404(hospital_id)
    
    if request.method == 'GET':
        return jsonify({
            'id': hospital.id,
            'name': hospital.name,
            'license_number': hospital.license_number,
            'address': hospital.address,
            'city': hospital.city,
            'state': hospital.state,
            'postal_code': hospital.postal_code,
            'country': hospital.country,
            'phone': hospital.phone,
            'email': hospital.email,
            'website': hospital.website,
            'services': json.loads(hospital.services) if hospital.services else [],
            'image_url': hospital.image_url,
            'is_verified': hospital.is_verified,
            'created_at': hospital.created_at.isoformat(),
            'updated_at': hospital.updated_at.isoformat()
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        # Update hospital fields
        for field in ['name', 'license_number', 'address', 'city', 'state', 
                     'postal_code', 'country', 'phone', 'email', 'website', 
                     'services', 'image_url', 'is_verified']:
            if field in data:
                if field == 'services':
                    hospital.services = json.dumps(data[field])
                else:
                    setattr(hospital, field, data[field])
        
        try:
            db.session.commit()
            return jsonify({'message': 'Hospital updated successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(hospital)
            db.session.commit()
            return jsonify({'message': 'Hospital deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

@app.route('/api/admin/pharmacies/<int:pharmacy_id>', methods=['GET', 'PUT', 'DELETE', 'OPTIONS'])
@admin_required
def pharmacy_detail(pharmacy_id):
    if request.method == 'OPTIONS':
        return '', 204
        
    pharmacy = Pharmacy.query.get_or_404(pharmacy_id)
    
    if request.method == 'GET':
        return jsonify({
            'id': pharmacy.id,
            'name': pharmacy.name,
            'license_number': pharmacy.license_number,
            'address': pharmacy.address,
            'city': pharmacy.city,
            'state': pharmacy.state,
            'postal_code': pharmacy.postal_code,
            'country': pharmacy.country,
            'phone': pharmacy.phone,
            'email': pharmacy.email,
            'website': pharmacy.website,
            'is_24_hours': pharmacy.is_24_hours,
            'is_verified': pharmacy.is_verified,
            'created_at': pharmacy.created_at.isoformat(),
            'updated_at': pharmacy.updated_at.isoformat()
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        # Update pharmacy fields
        for field in ['name', 'license_number', 'address', 'city', 'state', 
                     'postal_code', 'country', 'phone', 'email', 'website', 
                     'is_24_hours', 'is_verified']:
            if field in data:
                setattr(pharmacy, field, data[field])
        
        try:
            db.session.commit()
            return jsonify({'message': 'Pharmacy updated successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(pharmacy)
            db.session.commit()
            return jsonify({'message': 'Pharmacy deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

@app.route('/api/admin/doctors/<int:doctor_id>', methods=['GET', 'PUT', 'DELETE', 'OPTIONS'])
@admin_required
def doctor_detail(doctor_id):
    if request.method == 'OPTIONS':
        return '', 204
        
    doctor = Doctor.query.get_or_404(doctor_id)
    
    if request.method == 'GET':
        return jsonify({
            'id': doctor.id,
            'name': doctor.name,
            'license_number': doctor.license_number,
            'professional_type': doctor.professional_type,
            'specialization': doctor.specialization,
            'email': doctor.email,
            'phone': doctor.phone,
            'hospital_affiliation': doctor.hospital_affiliation,
            'address': doctor.address,
            'city': doctor.city,
            'state': doctor.state,
            'postal_code': doctor.postal_code,
            'country': doctor.country,
            'website': doctor.website,
            'image_url': doctor.image_url,
            'is_verified': doctor.is_verified,
            'qualifications': doctor.qualifications,
            'experience': doctor.experience,
            'pin': doctor.pin,
            'created_at': doctor.created_at.isoformat(),
            'updated_at': doctor.updated_at.isoformat()
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        # Update doctor fields
        for field in ['name', 'license_number', 'professional_type', 'specialization',
                     'email', 'phone', 'hospital_affiliation', 'address', 'city',
                     'state', 'postal_code', 'country', 'website', 'image_url',
                     'is_verified', 'qualifications', 'experience', 'pin']:
            if field in data:
                setattr(doctor, field, data[field])
        
        try:
            db.session.commit()
            return jsonify({'message': 'Doctor updated successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(doctor)
            db.session.commit()
            return jsonify({'message': 'Doctor deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

@app.route('/api/admin/admins', methods=['GET'])
@admin_required
def get_admins():
    try:
        admins = User.query.filter_by(role='admin').all()
        return jsonify([{
            'id': admin.id,
            'name': admin.name,
            'email': admin.email,
            'role': admin.role,
            'status': 'active' if admin.is_verified else 'inactive',
            'created_at': admin.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for admin in admins])
    except Exception as e:
        logger.error(f'Error getting admins: {str(e)}')
        return jsonify({'error': 'Failed to get admins'}), 500

@app.route('/api/admin/admins', methods=['POST'])
@admin_required
def create_admin():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['name', 'email', 'password', 'role']):
            return jsonify({'error': 'Missing required fields'}), 400

        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400

        # Create new admin user
        admin = User(
            name=data['name'],
            email=data['email'],
            password=generate_password_hash(data['password']),
            role='admin',
            is_verified=data.get('status') == 'active',
            phone=data.get('phone', '')
        )
        db.session.add(admin)
        db.session.commit()

        # Send credentials email if requested
        if data.get('send_credentials'):
            try:
                send_admin_credentials_email(admin.email, data['password'])
            except Exception as e:
                logger.error(f'Error sending credentials email: {str(e)}')

        return jsonify({
            'message': 'Administrator created successfully',
            'admin_id': admin.id
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f'Error creating admin: {str(e)}')
        return jsonify({'error': 'Failed to create administrator'}), 500

@app.route('/api/admin/admins/<int:admin_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def admin_detail(admin_id):
    try:
        admin = User.query.filter_by(id=admin_id, role='admin').first_or_404()

        if request.method == 'GET':
            return jsonify({
                'id': admin.id,
                'name': admin.name,
                'email': admin.email,
                'role': admin.role,
                'status': 'active' if admin.is_verified else 'inactive',
                'created_at': admin.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        elif request.method == 'PUT':
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400

            if 'name' in data:
                admin.name = data['name']
            if 'email' in data:
                # Check if new email is already taken
                existing = User.query.filter_by(email=data['email']).first()
                if existing and existing.id != admin.id:
                    return jsonify({'error': 'Email already registered'}), 400
                admin.email = data['email']
            if 'password' in data:
                admin.password = generate_password_hash(data['password'])
            if 'status' in data:
                admin.is_verified = data['status'] == 'active'

            db.session.commit()
            return jsonify({'message': 'Administrator updated successfully'})

        elif request.method == 'DELETE':
            # Prevent deleting the last admin
            admin_count = User.query.filter_by(role='admin').count()
            if admin_count <= 1:
                return jsonify({'error': 'Cannot delete the last administrator'}), 400

            db.session.delete(admin)
            db.session.commit()
            return jsonify({'message': 'Administrator deleted successfully'})

    except Exception as e:
        db.session.rollback()
        logger.error(f'Error in admin_detail: {str(e)}')
        return jsonify({'error': str(e)}), 500

def send_admin_credentials_email(email, password):
    """Send email with admin credentials"""
    try:
        msg = Message(
            'Your MamaCare Admin Account Credentials',
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[email]
        )
        msg.body = f'''Welcome to MamaCare Admin Portal!

Your account has been created. Here are your login credentials:

Email: {email}
Password: {password}

Please login at: http://localhost:5000/admin
And change your password immediately after first login.

Best regards,
MamaCare Team
'''
        mail.send(msg)
    except Exception as e:
        logger.error(f'Error sending admin credentials email: {str(e)}')
        raise

# Sample doctors data
DOCTORS = [
    {
        "id": 1,
        "name": "Dr. Sarah Johnson",
        "specialty": "Obstetrician",
        "experience": "15 years",
        "rating": 4.8,
        "image": "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80",
        "location": "Central Hospital",
        "availability": "Mon-Fri, 9AM-5PM"
    },
    {
        "id": 2,
        "name": "Dr. Michael Chen",
        "specialty": "Gynecologist",
        "experience": "12 years",
        "rating": 4.9,
        "image": "https://images.unsplash.com/photo-1622253692010-333f2da6031d?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80",
        "location": "Women's Health Center",
        "availability": "Mon-Sat, 8AM-6PM"
    },
    {
        "id": 3,
        "name": "Dr. Emily Rodriguez",
        "specialty": "Pediatrician",
        "experience": "10 years",
        "rating": 4.7,
        "image": "https://images.unsplash.com/photo-1594824476967-48c8b964273f?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80",
        "location": "Children's Hospital",
        "availability": "Mon-Fri, 10AM-7PM"
    }
]

@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    return jsonify(DOCTORS)

# Sample hospitals data
HOSPITALS = [
    {
        "id": 1,
        "name": "Central Hospital",
        "address": "123 Medical Center Drive",
        "phone": "(555) 123-4567",
        "rating": 4.7,
        "image": "https://images.unsplash.com/photo-1587351021759-3e566b6af7cc?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80",
        "specialties": ["Obstetrics", "Gynecology", "Pediatrics"],
        "availability": "24/7"
    },
    {
        "id": 2,
        "name": "Women's Health Center",
        "address": "456 Health Avenue",
        "phone": "(555) 234-5678",
        "rating": 4.8,
        "image": "https://images.unsplash.com/photo-1587351021759-3e566b6af7cc?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80",
        "specialties": ["Maternity", "Women's Health", "Fertility"],
        "availability": "Mon-Sat, 8AM-8PM"
    },
    {
        "id": 3,
        "name": "Children's Hospital",
        "address": "789 Care Street",
        "phone": "(555) 345-6789",
        "rating": 4.9,
        "image": "https://images.unsplash.com/photo-1587351021759-3e566b6af7cc?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80",
        "specialties": ["Pediatrics", "Neonatal Care", "Child Development"],
        "availability": "24/7"
    }
]

@app.route('/api/hospitals', methods=['GET'])
def get_hospitals():
    return jsonify(HOSPITALS)

# Sample pharmacies data
PHARMACIES = [
    {
        "id": 1,
        "name": "MedPlus Pharmacy",
        "address": "123 Health Street",
        "phone": "(555) 123-4567",
        "rating": 4.6,
        "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80",
        "services": ["Prescription", "OTC", "Delivery"],
        "hours": "Mon-Sun, 8AM-10PM"
    },
    {
        "id": 2,
        "name": "HealthFirst Pharmacy",
        "address": "456 Care Avenue",
        "phone": "(555) 234-5678",
        "rating": 4.8,
        "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80",
        "services": ["Prescription", "OTC", "Consultation"],
        "hours": "Mon-Sat, 9AM-9PM"
    },
    {
        "id": 3,
        "name": "QuickCare Pharmacy",
        "address": "789 Medical Drive",
        "phone": "(555) 345-6789",
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80",
        "services": ["Prescription", "OTC", "24/7 Service"],
        "hours": "24/7"
    }
]

@app.route('/api/pharmacies', methods=['GET'])
def get_pharmacies():
    return jsonify(PHARMACIES)

@app.route('/api/doctors/pin/<pin>', methods=['GET'])
def get_doctor_by_pin(pin):
    try:
        # Find doctor by PIN
        doctor = Doctor.query.filter_by(pin=pin).first()
        if not doctor:
            return jsonify({'error': 'Invalid PIN'}), 401

        return jsonify({
            'id': doctor.id,
            'name': doctor.name,
            'email': doctor.email,
            'phone': doctor.phone,
            'specialization': doctor.specialization,
            'hospital_affiliation': doctor.hospital_affiliation,
            'is_verified': doctor.is_verified
        }), 200

    except Exception as e:
        logger.error(f"Error getting doctor by PIN: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500