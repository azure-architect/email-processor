"""Essential data models."""

from __future__ import annotations

from datetime import datetime
from typing import Optional, Any, Dict
from uuid import UUID

from pydantic import BaseModel, EmailStr


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: str
    message: Optional[str] = None


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
    data: Optional[Dict[str, Any]] = None


class EmailAccountBase(BaseModel):
    name: str
    imap_server: str
    imap_port: int = 993
    username: str
    use_ssl: bool = True
    is_active: bool = True


class EmailAccountCreate(EmailAccountBase):
    password: str


class EmailAccountUpdate(BaseModel):
    name: Optional[str] = None
    imap_server: Optional[str] = None
    imap_port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    use_ssl: Optional[bool] = None
    is_active: Optional[bool] = None


class EmailAccountResponse(EmailAccountBase):
    id: UUID
    last_sync: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EmailMessageBase(BaseModel):
    subject: Optional[str] = None
    from_address: Optional[str] = None
    to_address: Optional[str] = None
    cc_address: Optional[str] = None
    bcc_address: Optional[str] = None
    reply_to: Optional[str] = None
    body_text: Optional[str] = None
    body_html: Optional[str] = None
    date_sent: Optional[datetime] = None
    date_received: Optional[datetime] = None
    size: Optional[int] = None
    is_read: bool = False
    is_flagged: bool = False
    is_deleted: bool = False
    is_draft: bool = False
    is_answered: bool = False


class EmailMessageCreate(EmailMessageBase):
    account_id: UUID
    message_id: str
    uid: int
    folder: str = "INBOX"


class EmailMessageUpdate(BaseModel):
    is_read: Optional[bool] = None
    is_flagged: Optional[bool] = None
    is_deleted: Optional[bool] = None
    is_draft: Optional[bool] = None
    is_answered: Optional[bool] = None
    processing_status: Optional[str] = None
    error_message: Optional[str] = None


class EmailMessageResponse(EmailMessageBase):
    id: UUID
    account_id: UUID
    message_id: str
    uid: int
    folder: str
    processed_at: Optional[datetime] = None
    processing_status: str
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EmailAttachmentBase(BaseModel):
    filename: str
    content_type: str
    size: int
    content_disposition: Optional[str] = None
    content_id: Optional[str] = None


class EmailAttachmentCreate(EmailAttachmentBase):
    message_id: UUID
    file_path: Optional[str] = None
    file_hash: Optional[str] = None


class EmailAttachmentResponse(EmailAttachmentBase):
    id: UUID
    message_id: UUID
    file_path: Optional[str] = None
    file_hash: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EmailSyncRequest(BaseModel):
    account_id: UUID
    folder: str = "INBOX"
    limit: Optional[int] = None


class EmailSyncResponse(BaseModel):
    account_id: UUID
    folder: str
    messages_processed: int
    messages_failed: int
    sync_started_at: datetime
    sync_completed_at: datetime
