import os
from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail, Message

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')

# Initialize mail
mail = Mail(app)

def test_email():
    try:
        print(f"Email configuration:")
        print(f"MAIL_USERNAME: {app.config['MAIL_USERNAME']}")
        print(f"MAIL_PASSWORD: {'*' * len(app.config['MAIL_PASSWORD']) if app.config['MAIL_PASSWORD'] else 'NOT SET'}")
        print(f"MAIL_SERVER: {app.config['MAIL_SERVER']}")
        print(f"MAIL_PORT: {app.config['MAIL_PORT']}")
        
        if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
            print("ERROR: Email credentials not set in .env file")
            return False
            
        with app.app_context():
            msg = Message('Test Email from MamaCare',
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[app.config['MAIL_USERNAME']])  # Send to yourself
            msg.body = '''This is a test email from MamaCare.

If you receive this email, the email configuration is working correctly.

Best regards,
MamaCare Team'''
            
            mail.send(msg)
            print("SUCCESS: Test email sent successfully!")
            return True
            
    except Exception as e:
        print(f"ERROR: Failed to send test email: {str(e)}")
        return False

if __name__ == '__main__':
    test_email() 