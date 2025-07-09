#!/usr/bin/env python3
"""Re-sync emails to store attachment content."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.models.email import EmailAccount
from src.workers.tasks.email_tasks import sync_email_account

# Database setup
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def clear_existing_attachments():
    """Clear existing attachments to re-sync with content."""
    session = SessionLocal()
    try:
        print("🗑️  Clearing existing attachments...")
        
        # Delete all attachments
        from sqlalchemy import text
        session.execute(text("DELETE FROM email_attachments"))
        session.commit()
        
        print("✅ Cleared all existing attachments")
        
    except Exception as e:
        print(f"❌ Failed to clear attachments: {e}")
        session.rollback()
    finally:
        session.close()


def resync_emails():
    """Re-sync emails to get attachment content."""
    session = SessionLocal()
    try:
        # Get email account
        account = session.query(EmailAccount).first()
        if not account:
            print("❌ No email account found")
            return False
        
        print(f"📧 Re-syncing emails for account: {account.username}")
        
        # Sync emails (this will now store attachment content)
        result = sync_email_account(str(account.id))
        
        print(f"✅ Sync completed!")
        print(f"   Messages processed: {result['messages_processed']}")
        print(f"   Messages failed: {result['messages_failed']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Sync failed: {e}")
        return False
    finally:
        session.close()


def check_attachment_content():
    """Check if attachments now have content."""
    session = SessionLocal()
    try:
        print("\n🔍 Checking attachment content...")
        
        from sqlalchemy import text
        
        # Query for CSV attachments with content
        query = text("""
            SELECT 
                filename,
                content_type,
                size,
                CASE WHEN content IS NOT NULL THEN 'YES' ELSE 'NO' END as has_content,
                LENGTH(content) as content_length
            FROM email_attachments
            WHERE filename LIKE '%.csv'
            ORDER BY created_at DESC
            LIMIT 10
        """)
        
        result = session.execute(query)
        attachments = result.fetchall()
        
        print(f"\nFound {len(attachments)} CSV attachments:")
        for att in attachments:
            print(f"   - {att[0]}")
            print(f"     Type: {att[1]}, Size: {att[2]} bytes")
            print(f"     Has Content: {att[3]} (Length: {att[4] or 0})")
        
        # Count attachments with content
        count_query = text("""
            SELECT 
                COUNT(*) as total,
                COUNT(content) as with_content
            FROM email_attachments
            WHERE filename LIKE '%.csv'
        """)
        
        result = session.execute(count_query)
        counts = result.fetchone()
        
        print(f"\n📊 Summary:")
        print(f"   Total CSV attachments: {counts[0]}")
        print(f"   With content: {counts[1]}")
        print(f"   Missing content: {counts[0] - counts[1]}")
        
    except Exception as e:
        print(f"❌ Failed to check content: {e}")
    finally:
        session.close()


def main():
    """Main function."""
    print("🔄 Email Re-sync with Attachment Content")
    print("=" * 50)
    
    # Step 1: Clear existing attachments
    clear_existing_attachments()
    
    # Step 2: Re-sync emails
    print("\n📥 Re-syncing emails with content storage...")
    success = resync_emails()
    
    if not success:
        print("❌ Re-sync failed")
        return False
    
    # Step 3: Check results
    check_attachment_content()
    
    print("\n✅ Re-sync completed!")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)