#!/usr/bin/env python3
"""Test script to verify IMAP connection and basic functionality."""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.imap_service import create_imap_service
from src.core.config import settings


async def test_imap_connection():
    """Test IMAP connection and basic operations."""
    print("🔧 Testing IMAP Connection")
    print("=" * 50)
    
    # Display configuration (without password)
    print(f"📧 Server: {settings.IMAP_SERVER}")
    print(f"🔌 Port: {settings.IMAP_PORT}")
    print(f"👤 Username: {settings.IMAP_USERNAME}")
    print(f"🔐 SSL: {settings.IMAP_USE_SSL}")
    print(f"🔑 Password: {'*' * len(settings.IMAP_PASSWORD) if settings.IMAP_PASSWORD else 'NOT SET'}")
    print()
    
    if not all([settings.IMAP_SERVER, settings.IMAP_USERNAME, settings.IMAP_PASSWORD]):
        print("❌ Missing IMAP configuration. Please check your .env file.")
        return False
    
    try:
        # Create IMAP service
        imap_service = await create_imap_service()
        
        # Test connection
        print("🔄 Connecting to IMAP server...")
        async with imap_service:
            print("✅ Connected successfully!")
            
            # Test folder listing
            print("\n📁 Listing folders...")
            folders = await imap_service.list_folders()
            print(f"Found {len(folders)} folders:")
            for folder in folders[:10]:  # Show first 10 folders
                print(f"  - {folder}")
            if len(folders) > 10:
                print(f"  ... and {len(folders) - 10} more")
            
            # Test INBOX selection
            print("\n📬 Selecting INBOX...")
            inbox_info = await imap_service.select_folder("INBOX")
            print(f"INBOX contains {inbox_info['exists']} messages")
            print(f"Recent: {inbox_info['recent']}, Unseen: {inbox_info['unseen']}")
            
            # Test message search (get last 5 messages)
            print("\n🔍 Searching for recent messages...")
            message_ids = await imap_service.search_messages("ALL", limit=5)
            print(f"Found {len(message_ids)} recent messages")
            
            # Test fetching headers for first message
            if message_ids:
                print(f"\n📋 Fetching headers for message ID: {message_ids[0]}")
                headers = await imap_service.fetch_message_headers(message_ids[0])
                print(f"Subject: {headers.get('subject', 'No subject')}")
                print(f"From: {headers.get('from', 'Unknown sender')}")
                print(f"Date: {headers.get('date', 'Unknown date')}")
                
                # Test fetching message body
                print(f"\n📄 Fetching body for message ID: {message_ids[0]}")
                text_body, html_body = await imap_service.fetch_message_body(message_ids[0])
                
                if text_body:
                    print(f"Text body length: {len(text_body)} characters")
                    print(f"Text preview: {text_body[:200]}...")
                if html_body:
                    print(f"HTML body length: {len(html_body)} characters")
                
                # Test fetching attachments
                print(f"\n📎 Checking attachments for message ID: {message_ids[0]}")
                attachments = await imap_service.fetch_message_attachments(message_ids[0])
                if attachments:
                    print(f"Found {len(attachments)} attachments:")
                    for att in attachments:
                        print(f"  - {att['filename']} ({att['content_type']}, {att['size']} bytes)")
                else:
                    print("No attachments found")
            
            print("\n✅ All IMAP tests completed successfully!")
            return True
            
    except Exception as e:
        print(f"❌ IMAP connection test failed: {e}")
        return False


async def main():
    """Main test function."""
    success = await test_imap_connection()
    
    if success:
        print("\n🎉 IMAP connection test passed!")
        print("Your email server configuration is working correctly.")
        sys.exit(0)
    else:
        print("\n💥 IMAP connection test failed!")
        print("Please check your email server configuration in .env file.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())