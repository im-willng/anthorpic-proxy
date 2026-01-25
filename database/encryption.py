import os
from cryptography.fernet import Fernet

# Generate or load encryption key
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    # For development - generate a key (in production, load from secure storage)
    ENCRYPTION_KEY = Fernet.generate_key().decode()
    print(f"⚠️  Generated new encryption key. Set ENCRYPTION_KEY={ENCRYPTION_KEY} in .env")

cipher = Fernet(ENCRYPTION_KEY.encode() if isinstance(ENCRYPTION_KEY, str) else ENCRYPTION_KEY)


def encrypt_api_key(api_key: str) -> str:
    """Encrypt an API key for secure storage."""
    return cipher.encrypt(api_key.encode()).decode()


def decrypt_api_key(encrypted_key: str) -> str:
    """Decrypt an API key from storage."""
    try:
        return cipher.decrypt(encrypted_key.encode()).decode()
    except Exception as e:
        raise ValueError(f"Failed to decrypt API key: {e}")
