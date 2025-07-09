#!/usr/bin/env python3
"""Force re-sync all emails to get attachment content."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.models.email import EmailAccount, EmailMessage

# Database setup
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def clear_all_email_data():
    """Clear all email data to force complete re-sync."""
    session = SessionLocal()
    try:
        print("🗑️  Clearing all email data...")
        
        # Clear in correct order due to foreign keys
        session.execute(text("DELETE FROM email_attachments"))
        session.execute(text("DELETE FROM email_messages"))
        
        # Don't delete email accounts
        print("   ✅ Cleared attachments and messages")
        print("   📧 Keeping email accounts")
        
        session.commit()
        
    except Exception as e:
        print(f"❌ Failed to clear data: {e}")
        session.rollback()
    finally:
        session.close()


def run_fresh_sync():
    """Run a fresh email sync."""
    from src.workers.tasks.email_tasks import sync_email_account
    
    session = SessionLocal()
    try:
        # Get email account
        account = session.query(EmailAccount).first()
        if not account:
            print("❌ No email account found")
            return False
        
        print(f"\n📥 Starting fresh sync for: {account.username}")
        
        # Sync emails (limiting to recent messages)
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


def check_results():
    """Check sync results."""
    session = SessionLocal()
    try:
        print("\n📊 Checking Results")
        print("=" * 50)
        
        # Count messages
        message_count = session.query(EmailMessage).count()
        print(f"📧 Total messages: {message_count}")
        
        # Check attachments
        attachment_query = text("""
            SELECT 
                filename,
                size,
                CASE WHEN content IS NOT NULL THEN LENGTH(content) ELSE 0 END as content_length
            FROM email_attachments
            WHERE filename LIKE '%.csv'
            ORDER BY created_at DESC
            LIMIT 5
        """)
        
        result = session.execute(attachment_query)
        attachments = result.fetchall()
        
        print(f"\n📎 Sample CSV attachments:")
        for att in attachments:
            print(f"   - {att[0]}")
            print(f"     Size: {att[1]} bytes, Content stored: {att[2]} bytes")
        
        # Check if content is actually stored
        content_check = text("""
            SELECT 
                COUNT(*) as total,
                COUNT(content) as with_content,
                SUM(CASE WHEN content IS NOT NULL THEN LENGTH(content) ELSE 0 END) as total_size
            FROM email_attachments
            WHERE filename LIKE '%.csv'
        """)
        
        result = session.execute(content_check)
        stats = result.fetchone()
        
        print(f"\n📈 Attachment Storage Stats:")
        print(f"   Total CSV attachments: {stats[0]}")
        print(f"   With content stored: {stats[1]}")
        print(f"   Total content size: {stats[2] or 0:,} bytes")
        
        if stats[1] > 0:
            print("\n✅ Attachment content is being stored successfully!")
        else:
            print("\n⚠️  No attachment content found - checking why...")
            
            # Debug check
            debug_query = text("""
                SELECT 
                    a.filename,
                    a.content_type,
                    m.subject
                FROM email_attachments a
                JOIN email_messages m ON a.message_id = m.id
                WHERE a.filename LIKE '%.csv'
                LIMIT 3
            """)
            
            result = session.execute(debug_query)
            debug_info = result.fetchall()
            
            print("\n🔍 Debug info:")
            for info in debug_info:
                print(f"   File: {info[0]} ({info[1]})")
                print(f"   From email: {info[2]}")
        
    except Exception as e:
        print(f"❌ Failed to check results: {e}")
    finally:
        session.close()


def main():
    """Main function."""
    print("🚀 Force Re-sync All Emails with Attachment Content")
    print("=" * 60)
    
    # Step 1: Clear existing data
    clear_all_email_data()
    
    # Step 2: Run fresh sync
    success = run_fresh_sync()
    
    if not success:
        print("❌ Sync failed")
        return False
    
    # Step 3: Check results
    check_results()
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)