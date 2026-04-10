from __future__ import annotations

import hashlib
import hmac
import json
from pathlib import Path


class AuthService:
    def __init__(self, storage_path: str = "users.json") -> None:
        self.storage_path = Path(storage_path)

    def register_user(self, username: str, password: str) -> None:
        username = username.strip().lower()
        if len(username) < 3:
            raise ValueError("El usuario debe tener al menos 3 caracteres.")
        if len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")

        users = self._load_users()
        if username in users:
            raise ValueError("Ese usuario ya existe.")

        users[username] = {
            "password_hash": self._hash_password(password),
        }
        self._save_users(users)

    def authenticate(self, username: str, password: str) -> bool:
        username = username.strip().lower()
        users = self._load_users()
        user = users.get(username)
        if not user:
            return False
        return hmac.compare_digest(user["password_hash"], self._hash_password(password))

    def user_exists(self, username: str) -> bool:
        return username.strip().lower() in self._load_users()

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def _load_users(self) -> dict:
        if not self.storage_path.exists():
            return {}
        try:
            return json.loads(self.storage_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

    def _save_users(self, users: dict) -> None:
        self.storage_path.write_text(
            json.dumps(users, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
