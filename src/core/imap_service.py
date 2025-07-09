from __future__ import annotations

import email
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from imapclient import IMAPClient
from imapclient.exceptions import IMAPClientError

from src.core.config import settings

logger = logging.getLogger(__name__)


class IMAPService:
    """IMAP email service for connecting to and retrieving emails from mail servers."""

    def __init__(self, server: str, port: int, username: str, password: str, use_ssl: bool = True):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.use_ssl = use_ssl
        self.client: Optional[IMAPClient] = None

    async def connect(self) -> bool:
        """Connect to IMAP server."""
        try:
            self.client = IMAPClient(self.server, port=self.port, ssl=self.use_ssl)
            self.client.login(self.username, self.password)
            logger.info(f"Connected to IMAP server: {self.server}:{self.port}")
            return True
        except IMAPClientError as e:
            logger.error(f"Failed to connect to IMAP server: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error connecting to IMAP server: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from IMAP server."""
        if self.client:
            try:
                self.client.logout()
                logger.info("Disconnected from IMAP server")
            except Exception as e:
                logger.warning(f"Error during IMAP disconnect: {e}")
            finally:
                self.client = None

    async def list_folders(self) -> List[str]:
        """List all available folders."""
        if not self.client:
            raise RuntimeError("Not connected to IMAP server")
        
        try:
            folders = self.client.list_folders()
            return [folder[2] for folder in folders]
        except IMAPClientError as e:
            logger.error(f"Failed to list folders: {e}")
            raise

    async def select_folder(self, folder: str = "INBOX") -> Dict[str, int]:
        """Select a folder and return folder info."""
        if not self.client:
            raise RuntimeError("Not connected to IMAP server")
        
        try:
            folder_info = self.client.select_folder(folder)
            logger.info(f"Selected folder: {folder} ({folder_info.get(b'EXISTS', 0)} messages)")
            return {
                "exists": folder_info.get(b"EXISTS", 0),
                "recent": folder_info.get(b"RECENT", 0),
                "unseen": folder_info.get(b"UNSEEN", 0),
            }
        except IMAPClientError as e:
            logger.error(f"Failed to select folder {folder}: {e}")
            raise

    async def search_messages(
        self,
        criteria: str = "ALL",
        folder: str = "INBOX",
        limit: Optional[int] = None
    ) -> List[int]:
        """Search for messages matching criteria."""
        if not self.client:
            raise RuntimeError("Not connected to IMAP server")
        
        try:
            await self.select_folder(folder)
            message_ids = self.client.search(criteria)
            
            if limit:
                message_ids = message_ids[-limit:]  # Get most recent messages
            
            logger.info(f"Found {len(message_ids)} messages matching criteria: {criteria}")
            return message_ids
        except IMAPClientError as e:
            logger.error(f"Failed to search messages: {e}")
            raise

    async def fetch_message_headers(self, message_id: int) -> Dict[str, str]:
        """Fetch message headers."""
        if not self.client:
            raise RuntimeError("Not connected to IMAP server")
        
        try:
            response = self.client.fetch([message_id], ["ENVELOPE", "FLAGS", "INTERNALDATE"])
            message_data = response[message_id]
            
            envelope = message_data[b"ENVELOPE"]
            flags = message_data[b"FLAGS"]
            internal_date = message_data[b"INTERNALDATE"]
            
            return {
                "subject": envelope.subject.decode("utf-8") if envelope.subject else "",
                "from": envelope.from_[0].name.decode("utf-8") + " <" + envelope.from_[0].mailbox.decode("utf-8") + "@" + envelope.from_[0].host.decode("utf-8") + ">" if envelope.from_ else "",
                "to": ", ".join([addr.mailbox.decode("utf-8") + "@" + addr.host.decode("utf-8") for addr in envelope.to]) if envelope.to else "",
                "cc": ", ".join([addr.mailbox.decode("utf-8") + "@" + addr.host.decode("utf-8") for addr in envelope.cc]) if envelope.cc else "",
                "bcc": ", ".join([addr.mailbox.decode("utf-8") + "@" + addr.host.decode("utf-8") for addr in envelope.bcc]) if envelope.bcc else "",
                "reply_to": envelope.reply_to[0].mailbox.decode("utf-8") + "@" + envelope.reply_to[0].host.decode("utf-8") if envelope.reply_to else "",
                "date": internal_date.isoformat() if internal_date else "",
                "flags": [flag.decode("utf-8") for flag in flags],
                "message_id": envelope.message_id.decode("utf-8") if envelope.message_id else "",
            }
        except Exception as e:
            logger.error(f"Failed to fetch message headers for ID {message_id}: {e}")
            raise

    async def fetch_message_body(self, message_id: int) -> Tuple[Optional[str], Optional[str]]:
        """Fetch message body (text and HTML)."""
        if not self.client:
            raise RuntimeError("Not connected to IMAP server")
        
        try:
            response = self.client.fetch([message_id], ["BODY[]"])
            raw_message = response[message_id][b"BODY[]"]
            
            # Parse the email message
            msg = email.message_from_bytes(raw_message)
            
            text_body = None
            html_body = None
            
            # Handle multipart messages
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain" and not text_body:
                        text_body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                    elif content_type == "text/html" and not html_body:
                        html_body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
            else:
                # Single part message
                content_type = msg.get_content_type()
                payload = msg.get_payload(decode=True)
                if payload:
                    decoded_payload = payload.decode("utf-8", errors="ignore")
                    if content_type == "text/plain":
                        text_body = decoded_payload
                    elif content_type == "text/html":
                        html_body = decoded_payload
            
            return text_body, html_body
        except Exception as e:
            logger.error(f"Failed to fetch message body for ID {message_id}: {e}")
            raise

    async def fetch_message_attachments(self, message_id: int) -> List[Dict[str, str]]:
        """Fetch message attachments metadata."""
        if not self.client:
            raise RuntimeError("Not connected to IMAP server")
        
        try:
            response = self.client.fetch([message_id], ["BODY[]"])
            raw_message = response[message_id][b"BODY[]"]
            
            # Parse the email message
            msg = email.message_from_bytes(raw_message)
            
            attachments = []
            
            if msg.is_multipart():
                for part in msg.walk():
                    content_disposition = part.get("Content-Disposition", "")
                    if "attachment" in content_disposition:
                        filename = part.get_filename()
                        if filename:
                            attachments.append({
                                "filename": filename,
                                "content_type": part.get_content_type(),
                                "size": len(part.get_payload(decode=True) or b""),
                                "content_disposition": content_disposition,
                                "content_id": part.get("Content-ID", ""),
                            })
            
            return attachments
        except Exception as e:
            logger.error(f"Failed to fetch attachments for message ID {message_id}: {e}")
            raise

    async def mark_as_read(self, message_ids: List[int]) -> bool:
        """Mark messages as read."""
        if not self.client:
            raise RuntimeError("Not connected to IMAP server")
        
        try:
            self.client.add_flags(message_ids, [b"\\Seen"])
            logger.info(f"Marked {len(message_ids)} messages as read")
            return True
        except IMAPClientError as e:
            logger.error(f"Failed to mark messages as read: {e}")
            return False

    async def mark_as_unread(self, message_ids: List[int]) -> bool:
        """Mark messages as unread."""
        if not self.client:
            raise RuntimeError("Not connected to IMAP server")
        
        try:
            self.client.remove_flags(message_ids, [b"\\Seen"])
            logger.info(f"Marked {len(message_ids)} messages as unread")
            return True
        except IMAPClientError as e:
            logger.error(f"Failed to mark messages as unread: {e}")
            return False

    async def delete_messages(self, message_ids: List[int]) -> bool:
        """Delete messages."""
        if not self.client:
            raise RuntimeError("Not connected to IMAP server")
        
        try:
            self.client.add_flags(message_ids, [b"\\Deleted"])
            self.client.expunge()
            logger.info(f"Deleted {len(message_ids)} messages")
            return True
        except IMAPClientError as e:
            logger.error(f"Failed to delete messages: {e}")
            return False

    async def get_message_count(self, folder: str = "INBOX") -> int:
        """Get total message count in folder."""
        if not self.client:
            raise RuntimeError("Not connected to IMAP server")
        
        try:
            folder_info = await self.select_folder(folder)
            return folder_info["exists"]
        except Exception as e:
            logger.error(f"Failed to get message count for folder {folder}: {e}")
            raise

    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()


def create_imap_service(
    server: str = None,
    port: int = None,
    username: str = None,
    password: str = None,
    use_ssl: bool = None
) -> IMAPService:
    """Create IMAP service with configuration from environment or parameters."""
    return IMAPService(
        server=server or settings.IMAP_SERVER,
        port=port or settings.IMAP_PORT,
        username=username or settings.IMAP_USERNAME,
        password=password or settings.IMAP_PASSWORD,
        use_ssl=use_ssl if use_ssl is not None else settings.IMAP_USE_SSL,
    )