#!/usr/bin/env python3
"""
Demo script to show the new SMS format with date and time
"""

from datetime import datetime

def format_datetime_with_ordinal(datetime_obj):
    """Format datetime as '30th June, 2025 at 2:30 PM'"""
    if not datetime_obj:
        return "Unknown"
    
    day = datetime_obj.day
    month = datetime_obj.strftime('%B')  # Full month name
    year = datetime_obj.year
    time = datetime_obj.strftime('%I:%M %p')  # 12-hour format with AM/PM
    
    # Add ordinal suffix to day
    if 10 <= day % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    
    return f"{day}{suffix} {month}, {year} at {time}"

def demo_sms_format():
    """Demonstrate the new SMS format"""
    print("=" * 60)
    print("NEW SMS FORMAT WITH DATE AND TIME")
    print("=" * 60)
    
    # Sample data
    patient_id = "12345"
    patient_name = "Sylvia Bobson Hardings"
    patient_contact = "+23212345678"
    doctor_name = "Dr. Ahmed"
    doctor_phone = "+23278656832"
    doctor_affiliation = "Life Care"
    feedback_notes = "Patient is responding well to treatment. Follow-up scheduled for next week."
    current_datetime = format_datetime_with_ordinal(datetime.now())
    
    # Create SMS message (same format as in the backend)
    sms_message = f"""REFERRAL FEEDBACK - MamaCare
        
Patient ID: {patient_id}
Patient: {patient_name}
Patient Contact: {patient_contact}
Doctor: {doctor_name}
Doctor Phone: {doctor_phone}
Hospital/Affiliation: {doctor_affiliation}
Feedback: {feedback_notes[:150]}{'...' if len(feedback_notes) > 150 else ''}
        
Submitted: {current_datetime}
        """
    
    print("SMS MESSAGE:")
    print(sms_message)
    
    print("\n" + "=" * 60)
    print("CHANGES MADE:")
    print("✅ Removed 'Source: MamaCare' line")
    print("✅ Changed date format to '30th June, 2025 at 2:30 PM'")
    print("✅ Added ordinal suffixes (1st, 2nd, 3rd, 4th, etc.)")
    print("✅ Added time in 12-hour format with AM/PM")
    print("=" * 60)
    
    # Show some example date formats
    print("\nEXAMPLE DATE FORMATS:")
    test_dates = [
        datetime(2025, 6, 30, 14, 30),  # 30th June, 2025 at 2:30 PM
        datetime(2025, 1, 1, 9, 15),    # 1st January, 2025 at 9:15 AM
        datetime(2025, 2, 2, 23, 45),   # 2nd February, 2025 at 11:45 PM
        datetime(2025, 12, 25, 12, 0),  # 25th December, 2025 at 12:00 PM
    ]
    
    for date in test_dates:
        formatted = format_datetime_with_ordinal(date)
        print(f"{date.strftime('%Y-%m-%d %H:%M')} -> {formatted}")

if __name__ == "__main__":
    demo_sms_format() 