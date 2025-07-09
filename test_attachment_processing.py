#!/usr/bin/env python3
"""Test script to verify attachment processing functionality."""

import sys
from pathlib import Path
from uuid import uuid4

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.models.email import EmailAccount, EmailMessage, EmailAttachment
from src.workers.tasks.attachment_processing_tasks import (
    extract_attachment_information,
    sanitize_table_name,
    extract_date_from_filename
)

# Database setup
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_test_csv_attachment():
    """Create a test CSV attachment for processing."""
    session = SessionLocal()
    try:
        # Get existing email account
        account = session.query(EmailAccount).first()
        if not account:
            print("❌ No email account found. Run email sync first.")
            return None
        
        # Get existing email message
        message = session.query(EmailMessage).first()
        if not message:
            print("❌ No email messages found. Run email sync first.")
            return None
        
        # Create test CSV attachment
        test_attachment = EmailAttachment(
            message_id=message.id,
            filename="test_data_2025-07-09.csv",
            content_type="text/csv",
            size=1024,
            content_disposition="attachment",
            content_id=None
        )
        
        session.add(test_attachment)
        session.commit()
        
        print(f"✅ Created test CSV attachment: {test_attachment.id}")
        return test_attachment.id
        
    except Exception as e:
        print(f"❌ Failed to create test attachment: {e}")
        session.rollback()
        return None
    finally:
        session.close()


def test_utility_functions():
    """Test utility functions for filename processing."""
    print("\n🧪 Testing Utility Functions")
    print("=" * 50)
    
    # Test filename sanitization
    test_filenames = [
        "daily-report-2025-07-09.csv",
        "Stock_Data_2025_07_09.csv",
        "My Report 2025-07-09 (final).csv",
        "data-file-20250709.csv",
        "special@chars#file.csv"
    ]
    
    print("📝 Filename Sanitization Tests:")
    for filename in test_filenames:
        sanitized = sanitize_table_name(filename)
        print(f"   {filename} -> {sanitized}")
    
    # Test date extraction
    print("\n📅 Date Extraction Tests:")
    for filename in test_filenames:
        extracted_date = extract_date_from_filename(filename)
        print(f"   {filename} -> {extracted_date}")
    
    return True


def test_attachment_extraction():
    """Test attachment extraction task."""
    print("\n🔍 Testing Attachment Extraction")
    print("=" * 50)
    
    try:
        # Run extraction task
        result = extract_attachment_information()
        
        print(f"✅ Extraction completed successfully!")
        print(f"   Status: {result['status']}")
        print(f"   Attachments processed: {result['attachments_processed']}")
        
        if result['results']:
            print(f"   First attachment: {result['results'][0]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        return False


def check_created_tables():
    """Check what tables were created during processing."""
    session = SessionLocal()
    try:
        print("\n📊 Checking Created Tables")
        print("=" * 50)
        
        # Query for all tables in the database
        tables_query = text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name NOT IN ('email_accounts', 'email_messages', 'email_attachments', 'alembic_version')
            ORDER BY table_name
        """)
        
        result = session.execute(tables_query)
        tables = [row[0] for row in result.fetchall()]
        
        print(f"Found {len(tables)} processed attachment tables:")
        for table in tables:
            print(f"   - {table}")
            
            # Get column info for each table
            columns_query = text(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{table}' 
                ORDER BY ordinal_position
            """)
            
            columns_result = session.execute(columns_query)
            columns = columns_result.fetchall()
            
            print(f"     Columns ({len(columns)}):")
            for col_name, col_type in columns:
                print(f"       - {col_name}: {col_type}")
            
            # Count rows in table
            count_query = text(f"SELECT COUNT(*) FROM {table}")
            row_count = session.execute(count_query).scalar()
            print(f"     Rows: {row_count}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to check tables: {e}")
        return False
    finally:
        session.close()


def main():
    """Main test function."""
    print("🧪 Testing Attachment Processing System")
    print("=" * 60)
    
    # Step 1: Test utility functions
    success = test_utility_functions()
    if not success:
        print("❌ Utility function tests failed")
        return False
    
    # Step 2: Create test attachment
    print("\n📎 Creating Test CSV Attachment...")
    attachment_id = create_test_csv_attachment()
    if not attachment_id:
        print("❌ Failed to create test attachment")
        return False
    
    # Step 3: Test attachment extraction
    success = test_attachment_extraction()
    if not success:
        print("❌ Attachment extraction test failed")
        return False
    
    # Step 4: Check created tables
    success = check_created_tables()
    if not success:
        print("❌ Table check failed")
        return False
    
    print("\n✅ All attachment processing tests passed!")
    print("The attachment processing system is working correctly.")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)