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
            
        pin = secrets.randbelow(1000000)
        pin_str = str(pin).zfill(6)
        
        logger.info(f"Creating new user with email: {data['email']}")
        
        # Create new user with all FHIR-compliant fields
        new_user = User(
            email=data['email'],
            pin=pin_str,
            name=data['name'],
            given_name=data['given_name'],
            family_name=data['family_name'],
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date(),
            gender=data['gender'],
            phone=data['phone'],
            address_line=data['address_line'],
            city=data['city'],
            state=data['state'],
            postal_code=data['postal_code'],
            country=data['country'],
            marital_status=data.get('marital_status'),
            language=data.get('language', 'en'),
            nationality=data.get('nationality'),
            blood_type=data.get('blood_type'),
            allergies=data.get('allergies'),
            medications=data.get('medications'),
            emergency_contact_name=data.get('emergency_contact_name'),
            emergency_contact_phone=data.get('emergency_contact_phone'),
            emergency_contact_relationship=data.get('emergency_contact_relationship')
        )
        
        logger.info("Attempting to add user to database session")
        db.session.add(new_user)
        
        logger.info("Attempting to commit user to database")
        db.session.commit()
        logger.info(f"Successfully committed user with ID: {new_user.id}")
        
        # Create FHIR Patient resource
        logger.info("Creating FHIR Patient resource")
        fhir_patient = create_fhir_patient(data)
        fhir_patient.id = str(new_user.id)
        new_user.fhir_id = fhir_patient.id
        
        logger.info("Attempting to commit FHIR ID to database")
        db.session.commit()
        logger.info(f"Successfully committed FHIR ID: {fhir_patient.id}")
        
        # Send email with PIN
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
        
        return jsonify({
            'message': 'Patient registered successfully',
            'pin': pin_str,
            'patient_id': new_user.id,
            'fhir_id': new_user.fhir_id
        }), 201
            
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error details: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 