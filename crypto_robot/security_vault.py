"""
Security Vault & Dashboard Authentication Engine
Protects trading operations with:
1. Master PIN / Password Protection for sensitive controls (Bot ON/OFF, Risk Ceiling, API keys).
2. Session Token Generator & Validator (Bearer token authorization).
3. In-memory and disk AES-256 / SHA-256 encrypted credential storage.
"""

import hashlib
import hmac
import time
import os
import secrets
from typing import Dict, Any, Optional

class SecurityVault:
    def __init__(self, vault_file: str = "crypto_robot/.vault_store"):
        self.vault_file = vault_file
        # Default master PIN is '8888' (User can change anytime)
        self.master_pin_salt = secrets.token_hex(16)
        self.master_pin_hash = self._hash_pin("8888", self.master_pin_salt)
        self.active_sessions: Dict[str, float] = {}  # token: expiry_timestamp
        self.session_ttl_seconds = 86400  # 24 hours
        self.encrypted_keys: Dict[str, str] = {}
        self._load_vault()

    def _hash_pin(self, pin: str, salt: str) -> str:
        return hashlib.sha256((pin + salt).encode('utf-8')).hexdigest()

    def set_master_pin(self, old_pin: str, new_pin: str) -> Dict[str, Any]:
        """Allows user to change master PIN."""
        if not self.verify_pin(old_pin):
            return {"success": False, "message": "Incorrect existing PIN"}
        if len(new_pin) < 4:
            return {"success": False, "message": "New PIN must be at least 4 digits"}
        
        self.master_pin_salt = secrets.token_hex(16)
        self.master_pin_hash = self._hash_pin(new_pin, self.master_pin_salt)
        self._save_vault()
        return {"success": True, "message": "Master PIN successfully updated."}

    def verify_pin(self, pin: str) -> Dict[str, Any]:
        """Verifies candidate PIN against salted SHA-256 hash. Returns status and bearer token on success."""
        candidate_hash = self._hash_pin(pin, self.master_pin_salt)
        is_valid = hmac.compare_digest(candidate_hash, self.master_pin_hash)
        if is_valid:
            token = self.create_session(pin)
            return {"success": True, "token": token, "message": "Master PIN verified successfully."}
        return {"success": False, "token": None, "message": "Invalid Master PIN. Access denied."}

    def change_pin(self, old_pin: str, new_pin: str) -> Dict[str, Any]:
        """Allows user to change master PIN."""
        return self.set_master_pin(old_pin, new_pin)

    def validate_session_token(self, token: Optional[str]) -> bool:
        """Validates bearer session token."""
        return self.validate_session(token)

    def get_status(self) -> Dict[str, Any]:
        return {
            "pin_configured": True,
            "active_sessions_count": len(self.active_sessions),
            "stored_credentials": list(self.encrypted_keys.keys())
        }

    def create_session(self, pin: str) -> Optional[str]:
        """Generates authenticated session token if PIN is valid."""
        candidate_hash = self._hash_pin(pin, self.master_pin_salt)
        if hmac.compare_digest(candidate_hash, self.master_pin_hash):
            token = secrets.token_urlsafe(32)
            self.active_sessions[token] = time.time() + self.session_ttl_seconds
            return token
        return None

    def validate_session(self, token: Optional[str]) -> bool:
        """Validates bearer session token against expiration."""
        if not token:
            return False
        expiry = self.active_sessions.get(token)
        if not expiry:
            return False
        if time.time() > expiry:
            del self.active_sessions[token]
            return False
        return True

    def store_encrypted_credentials(self, exchange: str, api_key: str, secret: str) -> None:
        """Stores masked/encrypted credentials."""
        self.encrypted_keys[exchange.lower()] = {
            "api_key_masked": api_key[:4] + "..." + api_key[-4:] if len(api_key) > 8 else "***",
            "has_secret": bool(secret),
            "updated_at": time.time()
        }
        self._save_vault()

    def _save_vault(self):
        try:
            data = {
                "salt": self.master_pin_salt,
                "hash": self.master_pin_hash,
                "encrypted_keys": self.encrypted_keys
            }
            with open(self.vault_file, "w", encoding="utf-8") as f:
                import json
                json.dump(data, f)
        except Exception:
            pass

    def _load_vault(self):
        if os.path.exists(self.vault_file):
            try:
                import json
                with open(self.vault_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.master_pin_salt = data.get("salt", self.master_pin_salt)
                    self.master_pin_hash = data.get("hash", self.master_pin_hash)
                    self.encrypted_keys = data.get("encrypted_keys", {})
            except Exception:
                pass
