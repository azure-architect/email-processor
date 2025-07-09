#!/usr/bin/env python3
"""Test script to verify email processing functionality."""

import sys
from pathlib import Path
from uuid import uuid4

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.models.email import EmailAccount, EmailMessage, EmailAttachment

# Database setup
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_test_email_account():
    """Create a test email account using the IMAP configuration."""
    session = SessionLocal()
    try:
        # Check if test account already exists
        existing_account = session.query(EmailAccount).filter(
            EmailAccount.username == settings.IMAP_USERNAME
        ).first()
        
        if existing_account:
            print(f"✅ Test account already exists: {existing_account.id}")
            return existing_account.id
        
        # Create new account
        account = EmailAccount(
            name="Test Account",
            imap_server=settings.IMAP_SERVER,
            imap_port=settings.IMAP_PORT,
            username=settings.IMAP_USERNAME,
            password=settings.IMAP_PASSWORD,
            use_ssl=settings.IMAP_USE_SSL,
            is_active=True
        )
        
        session.add(account)
        session.commit()
        
        print(f"✅ Created test email account: {account.id}")
        return account.id
        
    except Exception as e:
        print(f"❌ Failed to create test account: {e}")
        session.rollback()
        return None
    finally:
        session.close()


def test_sync_email_account(account_id):
    """Test syncing emails for a specific account."""
    from src.workers.tasks.email_tasks import sync_email_account
    
    try:
        print(f"🔄 Testing email sync for account: {account_id}")
        
        # Call the sync function directly (not as a Celery task)
        result = sync_email_account(str(account_id))
        
        print(f"✅ Sync completed successfully!")
        print(f"   Messages processed: {result['messages_processed']}")
        print(f"   Messages failed: {result['messages_failed']}")
        print(f"   Duration: {result['duration_seconds']:.2f}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Sync failed: {e}")
        return False


def check_database_content():
    """Check what's in the database after sync."""
    session = SessionLocal()
    try:
        # Count records
        account_count = session.query(EmailAccount).count()
        message_count = session.query(EmailMessage).count()
        attachment_count = session.query(EmailAttachment).count()
        
        print(f"\n📊 Database Content:")
        print(f"   Email Accounts: {account_count}")
        print(f"   Email Messages: {message_count}")
        print(f"   Email Attachments: {attachment_count}")
        
        # Show recent messages
        if message_count > 0:
            recent_messages = session.query(EmailMessage).order_by(
                EmailMessage.created_at.desc()
            ).limit(5).all()
            
            print(f"\n📧 Recent Messages:")
            for msg in recent_messages:
                print(f"   - {msg.subject[:50]}... ({msg.from_address})")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to check database: {e}")
        return False
    finally:
        session.close()


def main():
    """Main test function."""
    print("🧪 Testing Email Processing System")
    print("=" * 50)
    
    # Step 1: Create test account
    print("\n1. Creating test email account...")
    account_id = create_test_email_account()
    if not account_id:
        print("❌ Failed to create test account")
        return False
    
    # Step 2: Test email sync
    print("\n2. Testing email sync...")
    success = test_sync_email_account(account_id)
    if not success:
        print("❌ Email sync test failed")
        return False
    
    # Step 3: Check database content
    print("\n3. Checking database content...")
    success = check_database_content()
    if not success:
        print("❌ Database check failed")
        return False
    
    print("\n✅ All tests passed!")
    print("The email processing system is working correctly.")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)