#!/usr/bin/env python3
"""Process a single attachment to demonstrate the table creation."""

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
from src.workers.tasks.attachment_processing_tasks import (
    sanitize_table_name,
    extract_date_from_filename
)

# Database setup
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()


def process_attachment(attachment_id: str):
    """Process a single attachment and create its table."""
    session = SessionLocal()
    try:
        print(f"🔄 Processing attachment: {attachment_id}")
        
        # Get attachment
        attachment = session.query(EmailAttachment).filter(
            EmailAttachment.id == attachment_id
        ).first()
        
        if not attachment:
            print(f"❌ Attachment {attachment_id} not found")
            return False
        
        print(f"📎 Attachment: {attachment.filename}")
        
        # Generate table name and extract date
        table_name = sanitize_table_name(attachment.filename)
        attachment_date = extract_date_from_filename(attachment.filename)
        
        print(f"📋 Table name: {table_name}")
        print(f"📅 Attachment date: {attachment_date}")
        
        # Check if table exists
        table_exists_query = text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = :table_name
            )
        """)
        
        table_exists = session.execute(table_exists_query, {'table_name': table_name}).scalar()
        
        if table_exists:
            print(f"⚠️  Table {table_name} already exists")
        else:
            print(f"🏗️  Creating table {table_name}")
            
            # Determine headers based on filename
            if 'screener' in attachment.filename.lower():
                headers = ['symbol', 'company_name', 'sector', 'price', 'volume', 'change_percent']
            elif 'put' in attachment.filename.lower():
                headers = ['symbol', 'strike_price', 'expiration', 'premium', 'volume', 'open_interest']
            elif 'trendseeker' in attachment.filename.lower():
                headers = ['symbol', 'signal_type', 'price', 'target', 'stop_loss', 'confidence']
            else:
                headers = ['column1', 'column2', 'column3', 'column4', 'column5']
            
            print(f"📊 Headers: {headers}")
            
            # Create table
            columns = [Column('id', String, primary_key=True)]
            
            # Add data columns
            for header in headers:
                columns.append(Column(header, Text))
            
            # Add metadata columns
            columns.extend([
                Column('insertion_timestamp', DateTime(timezone=True), default=datetime.utcnow),
                Column('attachment_date', DateTime(timezone=True)),
                Column('source_attachment_id', String),
                Column('source_filename', String)
            ])
            
            # Create the table
            table = Table(table_name, metadata, *columns)
            table.create(engine)
            
            print(f"✅ Table {table_name} created with {len(headers)} data columns")
        
        # Insert sample data
        print(f"💾 Inserting sample data...")
        
        # Get column names for the table
        columns_query = text(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}' 
            AND column_name NOT IN ('id', 'insertion_timestamp', 'attachment_date', 'source_attachment_id', 'source_filename')
            ORDER BY ordinal_position
        """)
        
        result = session.execute(columns_query)
        data_columns = [row[0] for row in result.fetchall()]
        
        # Generate sample data
        for i in range(3):
            data_values = []
            for col in data_columns:
                if 'symbol' in col.lower():
                    data_values.append(f"SYMBOL{i+1}")
                elif 'price' in col.lower():
                    data_values.append(f"{100.50 + i * 5.25:.2f}")
                elif 'volume' in col.lower():
                    data_values.append(str(1000 + i * 500))
                elif 'percent' in col.lower():
                    data_values.append(f"{2.5 + i * 0.5:.2f}%")
                elif 'date' in col.lower():
                    data_values.append("2025-07-09")
                else:
                    data_values.append(f"sample_{col}_{i+1}")
            
            # Build insert statement
            data_column_placeholders = ', '.join([f':{col}' for col in data_columns])
            data_column_names = ', '.join(data_columns)
            
            insert_query = text(f"""
                INSERT INTO {table_name} 
                (id, {data_column_names}, insertion_timestamp, attachment_date, source_attachment_id, source_filename)
                VALUES 
                (:id, {data_column_placeholders}, :insertion_timestamp, :attachment_date, :source_attachment_id, :source_filename)
            """)
            
            # Build parameters
            params = {
                'id': str(uuid4()),
                'insertion_timestamp': datetime.utcnow(),
                'attachment_date': attachment_date,
                'source_attachment_id': str(attachment.id),
                'source_filename': attachment.filename
            }
            
            # Add data values
            for j, col in enumerate(data_columns):
                params[col] = data_values[j] if j < len(data_values) else None
            
            session.execute(insert_query, params)
        
        session.commit()
        
        # Verify data was inserted
        count_query = text(f"SELECT COUNT(*) FROM {table_name}")
        row_count = session.execute(count_query).scalar()
        
        print(f"✅ Inserted 3 sample rows (total rows: {row_count})")
        
        # Mark attachment as processed
        attachment.filename = f"PROCESSED_{attachment.filename}"
        session.commit()
        
        print(f"🏷️  Marked attachment as processed")
        
        return True
        
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        session.rollback()
        return False
    finally:
        session.close()


def list_unprocessed_attachments():
    """List all unprocessed CSV attachments."""
    session = SessionLocal()
    try:
        attachments = session.query(EmailAttachment).filter(
            (EmailAttachment.content_type.like('%csv%') | 
             EmailAttachment.filename.like('%.csv')),
            ~EmailAttachment.filename.like('%PROCESSED%')
        ).all()
        
        print(f"📋 Found {len(attachments)} unprocessed CSV attachments:")
        for i, attachment in enumerate(attachments):
            print(f"   {i+1}. {attachment.id} - {attachment.filename}")
        
        return attachments
        
    except Exception as e:
        print(f"❌ Failed to list attachments: {e}")
        return []
    finally:
        session.close()


def main():
    """Main function."""
    print("🚀 Single Attachment Processor")
    print("=" * 50)
    
    # List unprocessed attachments
    attachments = list_unprocessed_attachments()
    
    if not attachments:
        print("No unprocessed CSV attachments found.")
        return
    
    # Process the first attachment
    attachment_to_process = attachments[0]
    print(f"\n🎯 Processing: {attachment_to_process.filename}")
    
    success = process_attachment(str(attachment_to_process.id))
    
    if success:
        print("\n✅ Attachment processing completed successfully!")
    else:
        print("\n❌ Attachment processing failed!")


if __name__ == "__main__":
    main()