from __future__ import annotations

import json
from datetime import date, datetime, timedelta
from typing import Annotated

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from .auth import AuthService
from .document_parser import analyze_document as analyze_uploaded_document
from .local_calendar import LocalCalendarService
from .models import DeliveryItem

app = FastAPI(title="Organizador de Entregas")
app.add_middleware(SessionMiddleware, secret_key="calendario-academico-seguro")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def _current_user(request: Request) -> str | None:
    user = request.session.get("user")
    return str(user) if user else None


def _base_context(request: Request, year: int | None = None, month: int | None = None) -> dict:
    today = date.today()
    year = year or today.year
    month = month or today.month
    current_user = _current_user(request)
    calendar_data = LocalCalendarService().get_month_view(current_user or "__guest__", year, month)
    return {
        "request": request,
        "current_user": current_user,
        "is_authenticated": bool(current_user),
        "deliveries": [],
        "error": None,
        "success": None,
        "raw_payload": "[]",
        "default_reminder_days": 5,
        "calendar_data": calendar_data,
    }


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, year: int | None = None, month: int | None = None):
    if not _current_user(request):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": None,
                "success": None,
            },
        )
    return templates.TemplateResponse("index.html", _base_context(request, year=year, month=month))


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/analyze", response_class=HTMLResponse)
async def analyze_document(
    request: Request,
    file: UploadFile = File(...),
    reminder_days: int = Form(5),
):
    if not _current_user(request):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Debes iniciar sesion para usar la aplicacion.", "success": None},
            status_code=401,
        )
    try:
        content = await file.read()
        reminder_days = max(0, reminder_days)
        deliveries = analyze_uploaded_document(
            file.filename,
            content,
            today=date.today(),
            reminder_days=reminder_days,
        )
        raw_payload = json.dumps([item.to_dict() for item in deliveries], ensure_ascii=False)
        success = f"Se detectaron {len(deliveries)} items para organizar." if deliveries else "No se detectaron items."
        return templates.TemplateResponse(
            "index.html",
            {
                **_base_context(request),
                "deliveries": deliveries,
                "success": success,
                "raw_payload": raw_payload,
                "default_reminder_days": reminder_days,
            },
        )
    except Exception as exc:
        return templates.TemplateResponse(
            "index.html",
            {
                **_base_context(request),
                "error": str(exc),
                "default_reminder_days": reminder_days,
            },
            status_code=400,
        )


@app.post("/sync", response_class=HTMLResponse)
async def sync_calendar(
    request: Request,
    subjects: Annotated[list[str], Form(...)],
    categories: Annotated[list[str], Form(...)],
    titles: Annotated[list[str], Form(...)],
    due_dates: Annotated[list[str], Form(...)],
    source_lines: Annotated[list[str], Form(...)],
    reminder_days_list: Annotated[list[int], Form(...)],
):
    current_user = _current_user(request)
    if not current_user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Debes iniciar sesion para guardar eventos.", "success": None},
            status_code=401,
        )
    try:
        deliveries = _build_deliveries_from_form(
            subjects=subjects,
            categories=categories,
            titles=titles,
            due_dates=due_dates,
            source_lines=source_lines,
            reminder_days_list=reminder_days_list,
        )
        created_events = LocalCalendarService().add_delivery_items(current_user, deliveries)
        return templates.TemplateResponse(
            "index.html",
            {
                **_base_context(request),
                "deliveries": deliveries,
                "success": f"Se agregaron {created_events} eventos a tu calendario propio.",
                "raw_payload": json.dumps([item.to_dict() for item in deliveries], ensure_ascii=False),
            },
        )
    except Exception as exc:
        return templates.TemplateResponse(
            "index.html",
            {
                **_base_context(request),
                "error": str(exc),
            },
            status_code=400,
        )


@app.post("/calendar/clear", response_class=HTMLResponse)
async def clear_local_calendar(request: Request):
    current_user = _current_user(request)
    if not current_user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Debes iniciar sesion para limpiar el calendario.", "success": None},
            status_code=401,
        )
    LocalCalendarService().clear_all(current_user)
    return templates.TemplateResponse(
        "index.html",
        {
            **_base_context(request),
            "success": "Se limpiaron todos los eventos del calendario propio.",
        },
    )


@app.post("/register", response_class=HTMLResponse)
async def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    try:
        AuthService().register_user(username, password)
        request.session["user"] = username.strip().lower()
        return templates.TemplateResponse(
            "index.html",
            {
                **_base_context(request),
                "success": "Cuenta creada correctamente.",
            },
        )
    except Exception as exc:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": str(exc),
                "success": None,
            },
            status_code=400,
        )


@app.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    if not AuthService().authenticate(username, password):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Usuario o contraseña incorrectos.",
                "success": None,
            },
            status_code=401,
        )

    request.session["user"] = username.strip().lower()
    return templates.TemplateResponse(
        "index.html",
        {
            **_base_context(request),
            "success": "Sesion iniciada correctamente.",
        },
    )


@app.post("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    request.session.clear()
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "error": None,
            "success": "Sesion cerrada.",
        },
    )


def _apply_reminder_days(item: DeliveryItem, reminder_days: int) -> DeliveryItem:
    due_date = datetime.fromisoformat(item.due_date_iso).date()
    item.reminder_days = reminder_days
    item.reminder_date_iso = (due_date - timedelta(days=reminder_days)).isoformat()
    return item


def _build_deliveries_from_form(
    subjects: list[str],
    categories: list[str],
    titles: list[str],
    due_dates: list[str],
    source_lines: list[str],
    reminder_days_list: list[int],
) -> list[DeliveryItem]:
    if not (
        len(subjects)
        == len(categories)
        == len(titles)
        == len(due_dates)
        == len(source_lines)
        == len(reminder_days_list)
    ):
        raise ValueError("Los datos del formulario no coinciden entre actividades.")

    deliveries: list[DeliveryItem] = []
    for subject, category, title, due_date, source_line, reminder_days in zip(
        subjects,
        categories,
        titles,
        due_dates,
        source_lines,
        reminder_days_list,
    ):
        item = DeliveryItem(
            subject=subject,
            category=category,
            title=title,
            due_date_iso=due_date,
            reminder_date_iso=due_date,
            source_line=source_line,
            reminder_days=max(0, reminder_days),
        )
        deliveries.append(_apply_reminder_days(item, item.reminder_days))

    return deliveries
