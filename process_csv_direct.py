#!/usr/bin/env python3
"""Process CSV attachments directly without Celery."""

import base64
import sys
from datetime import datetime
from pathlib import Path
from uuid import uuid4

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sqlalchemy import Column, DateTime, MetaData, String, Table, Text, create_engine, text
from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.models.email import EmailAttachment
from src.workers.tasks.attachment_processing_tasks import sanitize_table_name, extract_date_from_filename
from src.workers.tasks.csv_file_reader import CSVFileReader

# Database setup
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()


def process_csv_attachment(attachment_id: str):
    """Process a single CSV attachment with real data."""
    session = SessionLocal()
    try:
        # Get attachment
        attachment = session.query(EmailAttachment).filter(
            EmailAttachment.id == attachment_id
        ).first()
        
        if not attachment:
            print(f"❌ Attachment {attachment_id} not found")
            return False
        
        print(f"\n📎 Processing: {attachment.filename}")
        
        # Check if we have content
        if not attachment.content:
            print("❌ No content stored for this attachment")
            return False
        
        # Decode content
        csv_content = base64.b64decode(attachment.content)
        print(f"📄 Content size: {len(csv_content)} bytes")
        
        # Parse CSV
        headers, encoding, delimiter = CSVFileReader.parse_csv_headers(csv_content)
        print(f"📊 Headers ({len(headers)}): {headers[:5]}..." if len(headers) > 5 else f"📊 Headers: {headers}")
        print(f"🔤 Encoding: {encoding}, Delimiter: '{delimiter}'")
        
        # Parse data
        csv_data = CSVFileReader.parse_csv_data(csv_content, headers, encoding, delimiter)
        print(f"📈 Rows: {len(csv_data)}")
        
        if csv_data:
            print(f"\n🔍 Sample row:")
            for key, value in list(csv_data[0].items())[:5]:
                print(f"   {key}: {value}")
        
        # Generate table name
        table_name = sanitize_table_name(attachment.filename)
        attachment_date = extract_date_from_filename(attachment.filename)
        
        print(f"\n📋 Table: {table_name}")
        print(f"📅 Date: {attachment_date}")
        
        # Check if table exists
        table_exists_query = text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = :table_name
            )
        """)
        
        table_exists = session.execute(table_exists_query, {'table_name': table_name}).scalar()
        
        if not table_exists:
            print(f"🏗️  Creating table {table_name}...")
            
            # Create table with actual CSV columns
            columns = [Column('id', String, primary_key=True)]
            
            for header in headers:
                columns.append(Column(header, Text))
            
            columns.extend([
                Column('insertion_timestamp', DateTime(timezone=True), default=datetime.utcnow),
                Column('attachment_date', DateTime(timezone=True)),
                Column('source_attachment_id', String),
                Column('source_filename', String)
            ])
            
            table = Table(table_name, metadata, *columns)
            table.create(engine)
            
            print(f"✅ Table created with {len(headers)} data columns")
        else:
            print(f"⚠️  Table {table_name} already exists")
        
        # Insert data
        print(f"\n💾 Inserting {len(csv_data)} rows...")
        
        insert_count = 0
        for row_dict in csv_data:
            try:
                # Build insert statement
                column_names = ['id'] + headers + ['insertion_timestamp', 'attachment_date', 'source_attachment_id', 'source_filename']
                placeholders = ', '.join([f':{col}' for col in column_names])
                columns_str = ', '.join(column_names)
                
                insert_query = text(f"""
                    INSERT INTO {table_name} ({columns_str})
                    VALUES ({placeholders})
                """)
                
                # Build parameters
                params = {
                    'id': str(uuid4()),
                    'insertion_timestamp': datetime.utcnow(),
                    'attachment_date': attachment_date,
                    'source_attachment_id': str(attachment.id),
                    'source_filename': attachment.filename
                }
                
                # Add CSV data
                for header in headers:
                    params[header] = row_dict.get(header, None)
                
                session.execute(insert_query, params)
                insert_count += 1
                
                # Show progress
                if insert_count % 10 == 0:
                    print(f"   Inserted {insert_count} rows...")
                
            except Exception as e:
                print(f"❌ Error inserting row {insert_count + 1}: {e}")
                continue
        
        session.commit()
        print(f"✅ Successfully inserted {insert_count} rows")
        
        # Show sample of inserted data
        sample_query = text(f"SELECT * FROM {table_name} LIMIT 3")
        result = session.execute(sample_query)
        rows = result.fetchall()
        
        print(f"\n📊 Sample inserted data:")
        for i, row in enumerate(rows):
            print(f"\nRow {i+1}:")
            for j, col in enumerate(result.keys()):
                if j < 5:  # Show first 5 columns
                    value = row[j]
                    if value and len(str(value)) > 50:
                        value = str(value)[:50] + "..."
                    print(f"   {col}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        session.rollback()
        return False
    finally:
        session.close()


def main():
    """Main function."""
    print("🚀 Direct CSV Processor (Real Data)")
    print("=" * 50)
    
    session = SessionLocal()
    try:
        # Get first unprocessed CSV attachment
        attachment = session.query(EmailAttachment).filter(
            EmailAttachment.filename.like('%.csv'),
            ~EmailAttachment.filename.like('PROCESSED_%'),
            EmailAttachment.content.isnot(None)
        ).first()
        
        if not attachment:
            print("❌ No unprocessed CSV attachments with content found")
            return False
        
        # Process it
        success = process_csv_attachment(str(attachment.id))
        
        if success:
            # Mark as processed
            attachment.filename = f"PROCESSED_{attachment.filename}"
            session.commit()
            print(f"\n🏷️  Marked as processed: {attachment.filename}")
        
        return success
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        session.close()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)