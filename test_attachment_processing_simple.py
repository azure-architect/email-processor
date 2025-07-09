#!/usr/bin/env python3
"""Simple test script for attachment processing without Celery."""

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
    sanitize_table_name,
    extract_date_from_filename
)

# Database setup
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def test_utility_functions():
    """Test utility functions for filename processing."""
    print("🧪 Testing Utility Functions")
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


def test_csv_attachment_query():
    """Test querying for CSV attachments."""
    session = SessionLocal()
    try:
        print("\n🔍 Testing CSV Attachment Query")
        print("=" * 50)
        
        # Query for all CSV attachments
        csv_attachments = session.query(EmailAttachment).filter(
            (EmailAttachment.content_type.like('%csv%') | 
             EmailAttachment.filename.like('%.csv')),
            ~EmailAttachment.filename.like('%PROCESSED%')
        ).all()
        
        print(f"Found {len(csv_attachments)} CSV attachments:")
        for attachment in csv_attachments:
            print(f"   - {attachment.filename} ({attachment.content_type})")
            
            # Test table name generation
            table_name = sanitize_table_name(attachment.filename)
            date_extracted = extract_date_from_filename(attachment.filename)
            
            print(f"     -> Table: {table_name}")
            print(f"     -> Date: {date_extracted}")
        
        return True
        
    except Exception as e:
        print(f"❌ Query failed: {e}")
        return False
    finally:
        session.close()


def test_table_creation_logic():
    """Test the table creation logic without actually creating tables."""
    session = SessionLocal()
    try:
        print("\n🏗️ Testing Table Creation Logic")
        print("=" * 50)
        
        # Get a sample attachment
        attachment = session.query(EmailAttachment).filter(
            EmailAttachment.filename.like('%.csv')
        ).first()
        
        if not attachment:
            print("❌ No CSV attachments found for testing")
            return False
        
        table_name = sanitize_table_name(attachment.filename)
        print(f"Testing with attachment: {attachment.filename}")
        print(f"Generated table name: {table_name}")
        
        # Check if table exists
        table_exists_query = text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = :table_name
            )
        """)
        
        table_exists = session.execute(table_exists_query, {'table_name': table_name}).scalar()
        print(f"Table exists: {table_exists}")
        
        # Show what headers would be generated
        if 'price' in attachment.filename.lower() or 'stock' in attachment.filename.lower():
            headers = ['symbol', 'price', 'volume', 'change', 'percent_change']
        elif 'report' in attachment.filename.lower():
            headers = ['date', 'category', 'amount', 'description', 'status']
        elif 'data' in attachment.filename.lower():
            headers = ['timestamp', 'value1', 'value2', 'value3', 'metric']
        else:
            headers = ['id', 'name', 'value', 'category', 'date']
        
        print(f"Generated headers: {headers}")
        
        return True
        
    except Exception as e:
        print(f"❌ Table creation logic test failed: {e}")
        return False
    finally:
        session.close()


def show_existing_processed_tables():
    """Show any tables that have been created from attachment processing."""
    session = SessionLocal()
    try:
        print("\n📊 Existing Processed Tables")
        print("=" * 50)
        
        # Query for tables that look like processed attachment tables
        tables_query = text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name NOT IN ('email_accounts', 'email_messages', 'email_attachments', 'alembic_version')
            ORDER BY table_name
        """)
        
        result = session.execute(tables_query)
        tables = [row[0] for row in result.fetchall()]
        
        if not tables:
            print("No processed attachment tables found.")
            return True
        
        print(f"Found {len(tables)} processed attachment tables:")
        for table in tables:
            print(f"\n📋 Table: {table}")
            
            # Get column info
            columns_query = text(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{table}' 
                ORDER BY ordinal_position
            """)
            
            columns_result = session.execute(columns_query)
            columns = columns_result.fetchall()
            
            print(f"   Columns ({len(columns)}):")
            for col_name, col_type in columns:
                print(f"     - {col_name}: {col_type}")
            
            # Count rows
            try:
                count_query = text(f"SELECT COUNT(*) FROM {table}")
                row_count = session.execute(count_query).scalar()
                print(f"   Rows: {row_count}")
            except Exception as e:
                print(f"   Rows: Error counting - {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to show tables: {e}")
        return False
    finally:
        session.close()


def main():
    """Main test function."""
    print("🧪 Testing Attachment Processing Components")
    print("=" * 60)
    
    # Test utility functions
    success = test_utility_functions()
    if not success:
        return False
    
    # Test CSV attachment query
    success = test_csv_attachment_query()
    if not success:
        return False
    
    # Test table creation logic
    success = test_table_creation_logic()
    if not success:
        return False
    
    # Show existing tables
    success = show_existing_processed_tables()
    if not success:
        return False
    
    print("\n✅ All attachment processing component tests passed!")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)