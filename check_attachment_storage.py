#!/usr/bin/env python3
"""Check how email attachments are stored and if we can access their content."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.models.email import EmailAttachment, EmailMessage

# Database setup
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def check_attachment_storage():
    """Check how attachments are stored in the database."""
    session = SessionLocal()
    try:
        print("🔍 Checking Attachment Storage")
        print("=" * 60)
        
        # Get a CSV attachment
        attachment = session.query(EmailAttachment).filter(
            EmailAttachment.filename.like('%.csv')
        ).first()
        
        if not attachment:
            print("❌ No CSV attachments found")
            return
        
        print(f"📎 Attachment: {attachment.filename}")
        print(f"   ID: {attachment.id}")
        print(f"   Content Type: {attachment.content_type}")
        print(f"   Size: {attachment.size} bytes")
        print(f"   File Path: {attachment.file_path}")
        print(f"   File Hash: {attachment.file_hash}")
        print(f"   Content ID: {attachment.content_id}")
        print(f"   Content Disposition: {attachment.content_disposition}")
        
        # Check if file_path points to an actual file
        if attachment.file_path:
            file_path = Path(attachment.file_path)
            print(f"\n📁 Checking file path: {file_path}")
            if file_path.exists():
                print("   ✅ File exists!")
                print(f"   Size on disk: {file_path.stat().st_size} bytes")
            else:
                print("   ❌ File does not exist at this path")
        else:
            print("\n⚠️  No file_path stored for this attachment")
        
        # Check email message for more info
        message = session.query(EmailMessage).filter(
            EmailMessage.id == attachment.message_id
        ).first()
        
        if message:
            print(f"\n📧 Parent Email:")
            print(f"   Subject: {message.subject}")
            print(f"   From: {message.from_address}")
            print(f"   Date: {message.date_sent}")
            
            # Check if attachment data might be in the email body
            if message.body_text:
                print(f"   Body Text Length: {len(message.body_text)} chars")
            if message.body_html:
                print(f"   Body HTML Length: {len(message.body_html)} chars")
        
        # Look for any columns that might contain file data
        print("\n🔍 Checking for file content storage patterns...")
        
        # Query to check all columns in email_attachments table
        columns_query = text("""
            SELECT column_name, data_type, character_maximum_length
            FROM information_schema.columns
            WHERE table_name = 'email_attachments'
            ORDER BY ordinal_position
        """)
        
        result = session.execute(columns_query)
        columns = result.fetchall()
        
        print("\nEmail Attachments Table Schema:")
        for col_name, data_type, max_length in columns:
            print(f"   - {col_name}: {data_type} (max: {max_length})")
        
        # Check if we need to add a content column
        has_content_column = any(col[0] in ['content', 'file_content', 'data'] for col in columns)
        
        if not has_content_column:
            print("\n⚠️  No content/data column found in email_attachments table")
            print("📝 The attachments table tracks metadata but not actual file content")
            print("💡 To store real CSV data, we need to either:")
            print("   1. Add a 'content' column to store file data")
            print("   2. Save files to disk and use file_path")
            print("   3. Fetch content from email server on demand")
        
    except Exception as e:
        print(f"❌ Error checking attachment storage: {e}")
    finally:
        session.close()


def check_imap_attachment_content():
    """Check if we can fetch attachment content from IMAP."""
    print("\n" + "=" * 60)
    print("🌐 Checking IMAP Attachment Retrieval")
    print("-" * 60)
    
    print("📝 Current IMAP service capabilities:")
    print("   - fetch_message_headers() ✅")
    print("   - fetch_message_body() ✅") 
    print("   - fetch_message_attachments() ✅ (metadata only)")
    print("   - fetch_attachment_content() ❌ (not implemented)")
    
    print("\n💡 To fetch real CSV content, we need to:")
    print("   1. Enhance fetch_message_attachments() to get content")
    print("   2. Parse MIME parts to extract attachment data")
    print("   3. Decode base64/quoted-printable content")
    print("   4. Save or process the CSV data")


def main():
    """Main function."""
    print("📎 Email Attachment Storage Analysis")
    print("=" * 60)
    
    check_attachment_storage()
    check_imap_attachment_content()
    
    print("\n" + "=" * 60)
    print("🔧 Next Steps for Real Data Ingestion:")
    print("   1. Modify IMAP service to fetch attachment content")
    print("   2. Add content storage (database or filesystem)")
    print("   3. Update CSV processing tasks to use real content")
    print("   4. Parse actual CSV headers and data")


if __name__ == "__main__":
    main()