from sqlalchemy import Column, String, Boolean, Integer, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

from database.encryption import encrypt_api_key, decrypt_api_key

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./proxies.db")
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Proxy(Base):
    """Proxy configuration model for managing LLM providers."""
    __tablename__ = "proxies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    provider = Column(String, nullable=False)  # openai, google, ollama, etc
    model = Column(String, nullable=False)
    api_key_encrypted = Column(String, nullable=True)  # Encrypted key
    base_url = Column(String, nullable=True)  # Custom endpoint URL
    priority = Column(Integer, default=0)
    enabled = Column(Boolean, default=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_api_key(self, api_key: str):
        """Encrypt and store API key."""
        if api_key:
            self.api_key_encrypted = encrypt_api_key(api_key)

    def get_api_key(self) -> str:
        """Decrypt and retrieve API key."""
        if self.api_key_encrypted:
            return decrypt_api_key(self.api_key_encrypted)
        return ""

    def to_dict(self, include_key: bool = False):
        """Convert to dictionary."""
        data = {
            "id": self.id,
            "name": self.name,
            "provider": self.provider,
            "model": self.model,
            "base_url": self.base_url,
            "priority": self.priority,
            "enabled": self.enabled,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_key:
            data["api_key"] = self.get_api_key()
        return data


# Create tables
Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
