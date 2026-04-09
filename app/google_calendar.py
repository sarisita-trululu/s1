from __future__ import annotations

import json
import os
from datetime import datetime, time, timedelta
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .models import DeliveryItem

SCOPES = ["https://www.googleapis.com/auth/calendar"]


class GoogleCalendarService:
    def __init__(
        self,
        credentials_path: str = "credentials.json",
        token_path: str = "token.json",
        calendar_id: str = "primary",
        service_account_path: str = "service_account.json",
        config_path: str = "google_calendar_config.json",
    ) -> None:
        self.credentials_path = Path(os.getenv("GOOGLE_CREDENTIALS_PATH", credentials_path))
        self.token_path = Path(os.getenv("GOOGLE_TOKEN_PATH", token_path))
        self.service_account_path = Path(service_account_path)
        self.config_path = Path(config_path)
        self.calendar_id = self._resolve_calendar_id(calendar_id)

    def create_delivery_events(self, deliveries: list[DeliveryItem]) -> list[dict]:
        service = self._build_service()
        created_events: list[dict] = []

        for item in deliveries:
            created_events.append(self._create_due_event(service, item))
            created_events.append(self._create_prep_event(service, item))

        return created_events

    def get_status(self) -> dict:
        config = self._load_local_config()
        calendar_id = self.calendar_id

        if os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"):
            return {
                "configured": True,
                "can_sync": True,
                "needs_oauth": False,
                "mode": "service_account",
                "calendar_id": calendar_id,
                "message": "Google Calendar configurado con Service Account por variable de entorno.",
            }

        if self.service_account_path.exists():
            return {
                "configured": True,
                "can_sync": True,
                "needs_oauth": False,
                "mode": "service_account",
                "calendar_id": calendar_id,
                "message": "Google Calendar configurado con Service Account.",
            }

        if self.credentials_path.exists() and self.token_path.exists():
            return {
                "configured": True,
                "can_sync": True,
                "needs_oauth": False,
                "mode": "oauth",
                "calendar_id": calendar_id,
                "message": "Google Calendar conectado por OAuth.",
            }

        if self.credentials_path.exists():
            return {
                "configured": True,
                "can_sync": True,
                "needs_oauth": True,
                "mode": "oauth",
                "calendar_id": calendar_id,
                "message": "Credenciales OAuth cargadas. Falta autorizar la cuenta de Google.",
            }

        return {
            "configured": False,
            "can_sync": False,
            "needs_oauth": False,
            "mode": config.get("mode", ""),
            "calendar_id": calendar_id,
            "message": "Falta configurar Google Calendar. Sube credentials.json o una Service Account desde esta pagina.",
        }

    def save_credentials_file(self, filename: str, content: bytes, calendar_id: str = "primary") -> str:
        payload = json.loads(content.decode("utf-8"))
        calendar_id = calendar_id.strip() or "primary"

        if payload.get("type") == "service_account":
            self.service_account_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            if self.credentials_path.exists():
                self.credentials_path.unlink()
            self._save_local_config(mode="service_account", calendar_id=calendar_id)
            return "Se guardo la Service Account de Google Calendar."

        if "installed" in payload or "web" in payload:
            self.credentials_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            if self.service_account_path.exists():
                self.service_account_path.unlink()
            if self.token_path.exists():
                self.token_path.unlink()
            self._save_local_config(mode="oauth", calendar_id=calendar_id)
            return "Se guardo credentials.json. Ahora autoriza la cuenta de Google."

        raise ValueError("El archivo no parece ser un JSON valido de Google OAuth ni de Service Account.")

    def connect_oauth(self) -> str:
        if not self.credentials_path.exists():
            raise FileNotFoundError("Primero sube credentials.json desde la pagina.")

        self._build_service()
        return "La cuenta de Google Calendar se autorizo correctamente."

    def disconnect(self) -> str:
        removed = False
        for path in (self.token_path, self.credentials_path, self.service_account_path, self.config_path):
            if path.exists():
                path.unlink()
                removed = True
        return "Se elimino la configuracion de Google Calendar." if removed else "No habia configuracion para eliminar."

    def _build_service(self):
        service_account_creds = self._load_service_account_credentials()
        if service_account_creds:
            return build("calendar", "v3", credentials=service_account_creds)

        creds = None
        if self.token_path.exists():
            creds = Credentials.from_authorized_user_file(str(self.token_path), SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not self.credentials_path.exists():
                    raise FileNotFoundError("No se encontro credentials.json en la raiz del proyecto.")
                flow = InstalledAppFlow.from_client_secrets_file(str(self.credentials_path), SCOPES)
                creds = flow.run_local_server(port=0)

            self.token_path.write_text(creds.to_json(), encoding="utf-8")

        return build("calendar", "v3", credentials=creds)

    def _load_service_account_credentials(self):
        raw_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        if raw_json:
            info = json.loads(raw_json)
            return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)

        service_account_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
        if service_account_file and Path(service_account_file).exists():
            return service_account.Credentials.from_service_account_file(service_account_file, scopes=SCOPES)

        if self.service_account_path.exists():
            return service_account.Credentials.from_service_account_file(
                str(self.service_account_path),
                scopes=SCOPES,
            )

        return None

    def _create_due_event(self, service, item: DeliveryItem) -> dict:
        due_date = datetime.fromisoformat(item.due_date_iso).date()
        event = {
            "summary": f"{item.subject} - {item.category.title()} - {item.title}",
            "description": (
                f"Materia: {item.subject}\n"
                f"Categoria: {item.category}\n"
                f"Tarea detectada automaticamente.\n\n"
                f"Texto original: {item.source_line}"
            ),
            "start": {"date": due_date.isoformat()},
            "end": {"date": (due_date + timedelta(days=1)).isoformat()},
            "reminders": {
                "useDefault": False,
                "overrides": [{"method": "popup", "minutes": 60 * 24 * item.reminder_days}],
            },
        }
        return service.events().insert(calendarId=self.calendar_id, body=event).execute()

    def _create_prep_event(self, service, item: DeliveryItem) -> dict:
        prep_dt = datetime.combine(datetime.fromisoformat(item.reminder_date_iso).date(), time(9, 0))
        event = {
            "summary": f"Preparar {item.subject} - {item.category.title()} - {item.title}",
            "description": (
                f"Materia: {item.subject}\n"
                f"Categoria: {item.category}\n"
                f"Recordatorio automatico {item.reminder_days} dias antes de la entrega.\n"
                f"Entrega final: {item.due_date_iso}"
            ),
            "start": {"dateTime": prep_dt.isoformat(), "timeZone": "America/Bogota"},
            "end": {"dateTime": prep_dt.replace(hour=10).isoformat(), "timeZone": "America/Bogota"},
            "reminders": {"useDefault": True},
        }
        return service.events().insert(calendarId=self.calendar_id, body=event).execute()

    def _load_local_config(self) -> dict:
        if not self.config_path.exists():
            return {}
        try:
            return json.loads(self.config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

    def _save_local_config(self, mode: str, calendar_id: str) -> None:
        self.config_path.write_text(
            json.dumps({"mode": mode, "calendar_id": calendar_id}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _resolve_calendar_id(self, fallback: str) -> str:
        env_calendar_id = os.getenv("GOOGLE_CALENDAR_ID")
        if env_calendar_id:
            return env_calendar_id
        local_config = self._load_local_config()
        return local_config.get("calendar_id", fallback)
