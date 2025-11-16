# celery_worker.py
from celery import Celery
import time
from datetime import datetime

# Create Celery app
celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

# This is the background task
@celery_app.task
def send_welcome_email(email, full_name):
    """Send welcome email in background (MOCK - just prints)"""
    
    print("\n" + "="*60)
    print("📧 SENDING WELCOME EMAIL (MOCK)")
    print("="*60)
    
    # Simulate sending email (wait 3 seconds)
    time.sleep(3)
    
    # Print mock email
    print(f"""
    To: {email}
    Subject: Welcome to FastAPI!
    
    Hi {full_name},
    
    Thank you for registering!
    Your account is now active.
    
    Best regards,
    FastAPI Team
    
    Sent at: {datetime.now()}
    """)
    
    print("="*60)
    print("✅ EMAIL SENT SUCCESSFULLY!")
    print("="*60 + "\n")
    
    return f"Email sent to {email}"