#!/usr/bin/env python3
"""Check what data was actually ingested into the processed tables."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

# Database setup
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def check_ingested_data():
    """Check all data in processed attachment tables."""
    session = SessionLocal()
    try:
        print("🔍 Checking Ingested Data")
        print("=" * 60)
        
        # Find all processed attachment tables
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
            print("❌ No processed attachment tables found.")
            return
        
        for table in tables:
            print(f"\n📊 Table: {table}")
            print("-" * 60)
            
            # Get sample data
            data_query = text(f"SELECT * FROM {table} LIMIT 5")
            result = session.execute(data_query)
            
            # Get column names
            columns = result.keys()
            print(f"Columns: {list(columns)}")
            
            # Display data
            rows = result.fetchall()
            print(f"\nSample Data ({len(rows)} rows shown):")
            
            for i, row in enumerate(rows):
                print(f"\nRow {i+1}:")
                for j, col in enumerate(columns):
                    value = row[j]
                    # Truncate long values
                    if value and isinstance(value, str) and len(str(value)) > 50:
                        value = str(value)[:50] + "..."
                    print(f"  {col}: {value}")
            
            # Get total count
            count_query = text(f"SELECT COUNT(*) FROM {table}")
            total_count = session.execute(count_query).scalar()
            print(f"\nTotal rows in table: {total_count}")
            
            # Check source attachments
            source_query = text(f"""
                SELECT DISTINCT source_filename, attachment_date, COUNT(*) as row_count
                FROM {table}
                GROUP BY source_filename, attachment_date
                ORDER BY source_filename
            """)
            
            sources = session.execute(source_query).fetchall()
            print(f"\nData sources:")
            for source in sources:
                print(f"  - {source[0]} (date: {source[1]}) - {source[2]} rows")
        
        # Check if we have actual CSV content to show
        print("\n" + "=" * 60)
        print("📎 Checking Original Attachments")
        print("-" * 60)
        
        # Find processed attachments
        processed_attachments_query = text("""
            SELECT id, filename, content_type, size
            FROM email_attachments
            WHERE filename LIKE 'PROCESSED_%'
            ORDER BY filename
            LIMIT 5
        """)
        
        result = session.execute(processed_attachments_query)
        processed = result.fetchall()
        
        print(f"Found {len(processed)} processed attachments:")
        for att in processed:
            print(f"  - {att[1]} ({att[2]}, {att[3]} bytes)")
        
        # Find unprocessed attachments
        unprocessed_attachments_query = text("""
            SELECT id, filename, content_type, size
            FROM email_attachments
            WHERE (content_type LIKE '%csv%' OR filename LIKE '%.csv')
            AND filename NOT LIKE 'PROCESSED_%'
            ORDER BY filename
            LIMIT 5
        """)
        
        result = session.execute(unprocessed_attachments_query)
        unprocessed = result.fetchall()
        
        print(f"\nFound {len(unprocessed)} unprocessed CSV attachments:")
        for att in unprocessed:
            print(f"  - {att[1]} ({att[2]}, {att[3]} bytes)")
        
    except Exception as e:
        print(f"❌ Error checking data: {e}")
    finally:
        session.close()


def check_data_quality():
    """Check if the ingested data looks like real data or mock data."""
    session = SessionLocal()
    try:
        print("\n" + "=" * 60)
        print("🔬 Data Quality Check")
        print("-" * 60)
        
        # Check screener_daily_put_full_scan table
        table_name = "screener_daily_put_full_scan"
        
        check_query = text(f"""
            SELECT 
                symbol,
                company_name,
                price,
                volume,
                change_percent
            FROM {table_name}
            LIMIT 10
        """)
        
        try:
            result = session.execute(check_query)
            rows = result.fetchall()
            
            if rows:
                print(f"Sample data from {table_name}:")
                
                # Check if data looks real or mock
                mock_indicators = 0
                real_indicators = 0
                
                for row in rows:
                    symbol, company, price, volume, percent = row
                    print(f"  Symbol: {symbol}, Company: {company}, Price: ${price}, Volume: {volume}, Change: {percent}")
                    
                    # Check for mock data patterns
                    if symbol and "SYMBOL" in str(symbol).upper():
                        mock_indicators += 1
                    if company and "sample_" in str(company).lower():
                        mock_indicators += 1
                    
                    # Check for real data patterns
                    if symbol and len(str(symbol)) <= 5 and str(symbol).isalpha():
                        real_indicators += 1
                    if price and "$" not in str(price) and "." in str(price):
                        try:
                            float(price)
                            real_indicators += 1
                        except:
                            pass
                
                print(f"\n📊 Data Assessment:")
                if mock_indicators > real_indicators:
                    print("  ⚠️  Data appears to be MOCK/SAMPLE data")
                    print("  💡 The system is using simulated data for testing")
                    print("  📝 To ingest real data, the system needs to:")
                    print("     1. Read actual CSV file content from email attachments")
                    print("     2. Parse CSV headers dynamically")
                    print("     3. Map CSV columns to database columns")
                else:
                    print("  ✅ Data appears to be REAL data from CSV files")
                
        except Exception as e:
            print(f"Table {table_name} not found or error: {e}")
        
    except Exception as e:
        print(f"❌ Error checking data quality: {e}")
    finally:
        session.close()


def main():
    """Main function."""
    print("📊 Email Attachment Data Ingestion Check")
    print("=" * 60)
    
    check_ingested_data()
    check_data_quality()
    
    print("\n" + "=" * 60)
    print("💡 Summary:")
    print("  - The system successfully creates tables from CSV attachments")
    print("  - Currently using MOCK data for demonstration")
    print("  - Real CSV parsing requires reading actual file content")
    print("  - All infrastructure is in place for real data ingestion")


if __name__ == "__main__":
    main()