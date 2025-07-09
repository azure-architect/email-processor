from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from uuid import UUID

from celery import Celery
from celery.schedules import crontab
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.core.imap_service import create_imap_service
from src.models.email import EmailAccount, EmailMessage, EmailAttachment
from src.workers.celery_app import celery_app

logger = logging.getLogger(__name__)

# Database setup
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def sync_email_account(self, account_id: str) -> Dict[str, any]:
    """
    Sync emails from a specific email account.
    
    Args:
        account_id: UUID of the email account to sync
        
    Returns:
        Dict with sync results
    """
    session = SessionLocal()
    try:
        # Get account details
        account = session.query(EmailAccount).filter(EmailAccount.id == account_id).first()
        if not account:
            raise ValueError(f"Email account {account_id} not found")
        
        if not account.is_active:
            logger.info(f"Skipping inactive account {account_id}")
            return {"status": "skipped", "reason": "account_inactive"}
        
        logger.info(f"Starting sync for account {account_id}: {account.username}")
        
        messages_processed = 0
        messages_failed = 0
        sync_started_at = datetime.utcnow()
        
        # Connect and process emails using asyncio
        async def process_emails():
            nonlocal messages_processed, messages_failed
            
            # Create IMAP service inside async context
            imap_service = create_imap_service(
                server=account.imap_server,
                port=account.imap_port,
                username=account.username,
                password=account.password,
                use_ssl=account.use_ssl
            )
            
            async with imap_service:
                # Get recent messages (last 50)
                message_ids = await imap_service.search_messages("ALL", limit=50)
                
                for message_id in message_ids:
                    try:
                        # Check if message already exists
                        existing_msg = session.query(EmailMessage).filter(
                            EmailMessage.account_id == account_id,
                            EmailMessage.uid == message_id
                        ).first()
                        
                        if existing_msg:
                            logger.debug(f"Message {message_id} already exists, skipping")
                            continue
                        
                        # Fetch message data
                        headers = await imap_service.fetch_message_headers(message_id)
                        text_body, html_body = await imap_service.fetch_message_body(message_id)
                        attachments = await imap_service.fetch_message_attachments(message_id)
                        
                        # Create message record
                        email_message = EmailMessage(
                            account_id=account_id,
                            message_id=headers.get("message_id", f"uid_{message_id}"),
                            uid=message_id,
                            folder="INBOX",
                            subject=headers.get("subject"),
                            from_address=headers.get("from"),
                            to_address=headers.get("to"),
                            cc_address=headers.get("cc"),
                            bcc_address=headers.get("bcc"),
                            reply_to=headers.get("reply_to"),
                            body_text=text_body,
                            body_html=html_body,
                            date_sent=datetime.fromisoformat(headers.get("date")) if headers.get("date") else None,
                            date_received=datetime.utcnow(),
                            is_read="\\Seen" in headers.get("flags", []),
                            is_flagged="\\Flagged" in headers.get("flags", []),
                            is_deleted="\\Deleted" in headers.get("flags", []),
                            is_draft="\\Draft" in headers.get("flags", []),
                            is_answered="\\Answered" in headers.get("flags", []),
                            processing_status="completed",
                            processed_at=datetime.utcnow()
                        )
                        
                        session.add(email_message)
                        session.flush()  # Get the ID
                        
                        # Process attachments
                        for attachment_data in attachments:
                            attachment = EmailAttachment(
                                message_id=email_message.id,
                                filename=attachment_data["filename"],
                                content_type=attachment_data["content_type"],
                                size=attachment_data["size"],
                                content_disposition=attachment_data.get("content_disposition"),
                                content_id=attachment_data.get("content_id")
                            )
                            session.add(attachment)
                        
                        session.commit()
                        messages_processed += 1
                        logger.info(f"Processed message {message_id}: {headers.get('subject', 'No subject')}")
                        
                    except Exception as e:
                        logger.error(f"Failed to process message {message_id}: {e}")
                        messages_failed += 1
                        session.rollback()
                        continue
        
        # Run the async function
        asyncio.run(process_emails())
        
        # Update account last sync time
        account.last_sync = datetime.utcnow()
        session.commit()
        
        sync_completed_at = datetime.utcnow()
        
        result = {
            "status": "completed",
            "account_id": account_id,
            "messages_processed": messages_processed,
            "messages_failed": messages_failed,
            "sync_started_at": sync_started_at.isoformat(),
            "sync_completed_at": sync_completed_at.isoformat(),
            "duration_seconds": (sync_completed_at - sync_started_at).total_seconds()
        }
        
        logger.info(f"Sync completed for account {account_id}: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Sync failed for account {account_id}: {e}")
        session.rollback()
        raise
    finally:
        session.close()


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def sync_all_active_accounts(self) -> Dict[str, any]:
    """
    Sync all active email accounts.
    
    Returns:
        Dict with overall sync results
    """
    session = SessionLocal()
    try:
        # Get all active accounts
        active_accounts = session.query(EmailAccount).filter(EmailAccount.is_active == True).all()
        
        if not active_accounts:
            logger.info("No active email accounts found")
            return {"status": "completed", "accounts_synced": 0}
        
        logger.info(f"Starting sync for {len(active_accounts)} active accounts")
        
        results = []
        for account in active_accounts:
            try:
                # Trigger sync for individual account
                result = sync_email_account.delay(str(account.id))
                results.append({
                    "account_id": str(account.id),
                    "task_id": result.id,
                    "status": "queued"
                })
            except Exception as e:
                logger.error(f"Failed to queue sync for account {account.id}: {e}")
                results.append({
                    "account_id": str(account.id),
                    "status": "failed",
                    "error": str(e)
                })
        
        return {
            "status": "completed",
            "accounts_synced": len(results),
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Failed to sync all accounts: {e}")
        raise
    finally:
        session.close()


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def process_email_message(self, message_id: str) -> Dict[str, any]:
    """
    Process a specific email message for additional analysis.
    
    Args:
        message_id: UUID of the email message to process
        
    Returns:
        Dict with processing results
    """
    session = SessionLocal()
    try:
        # Get message details
        message = session.query(EmailMessage).filter(EmailMessage.id == message_id).first()
        if not message:
            raise ValueError(f"Email message {message_id} not found")
        
        logger.info(f"Processing email message {message_id}: {message.subject}")
        
        # Mark as being processed
        message.processing_status = "processing"
        session.commit()
        
        # TODO: Add your email processing logic here
        # Examples:
        # - Extract entities from email content
        # - Classify email type/category
        # - Perform sentiment analysis
        # - Extract attachments
        # - etc.
        
        # For now, just mark as processed
        message.processing_status = "completed"
        message.processed_at = datetime.utcnow()
        session.commit()
        
        result = {
            "status": "completed",
            "message_id": message_id,
            "subject": message.subject,
            "processed_at": message.processed_at.isoformat()
        }
        
        logger.info(f"Processing completed for message {message_id}")
        return result
        
    except Exception as e:
        logger.error(f"Processing failed for message {message_id}: {e}")
        
        # Mark as failed
        if 'message' in locals():
            message.processing_status = "failed"
            message.error_message = str(e)
            session.commit()
        
        raise
    finally:
        session.close()


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def cleanup_old_messages(self, days_old: int = 30) -> Dict[str, any]:
    """
    Clean up old email messages to manage database size.
    
    Args:
        days_old: Number of days old messages to keep
        
    Returns:
        Dict with cleanup results
    """
    session = SessionLocal()
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        
        # Delete old messages
        deleted_count = session.query(EmailMessage).filter(
            EmailMessage.created_at < cutoff_date,
            EmailMessage.is_deleted == True
        ).delete()
        
        session.commit()
        
        result = {
            "status": "completed",
            "messages_deleted": deleted_count,
            "cutoff_date": cutoff_date.isoformat()
        }
        
        logger.info(f"Cleanup completed: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        session.rollback()
        raise
    finally:
        session.close()


# Periodic tasks configuration
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Setup periodic tasks for email processing."""
    
    # Sync all accounts every 15 minutes
    sender.add_periodic_task(
        900.0,  # 15 minutes
        sync_all_active_accounts.s(),
        name='sync_all_accounts_every_15min'
    )
    
    # Cleanup old messages daily at 2 AM
    sender.add_periodic_task(
        crontab(hour=2, minute=0),
        cleanup_old_messages.s(days_old=30),
        name='cleanup_old_messages_daily'
    )