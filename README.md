# Organizadorcitotrululu

Aplicacion web en FastAPI para leer planes de curso en `.docx` o `.pdf`, detectar lecturas y actividades con fecha, y organizarlas dentro de un calendario mensual editable.

## Archivos listos para despliegue

- `requirements.txt`
- `Procfile`
- `render.yaml`
- `railway.json`
- `run.py`

## Variables de entorno

- `PORT`: puerto publico del servicio. Si no existe, usa `5000`.
- `HOST`: por defecto `0.0.0.0`.
- `SESSION_SECRET`: clave de sesion para produccion.
- `APP_DATA_DIR`: carpeta donde se guardan `users.json`, eventos y configuraciones.
- `GOOGLE_SERVICE_ACCOUNT_JSON`: opcional si luego quieres reactivar Google Calendar.
- `GOOGLE_CALENDAR_ID`: opcional para Google Calendar.

## Ejecutar local

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

## Deploy en Render

1. Sube este proyecto a GitHub.
2. Entra a [Render](https://render.com/) y pulsa `New +`.
3. Elige `Blueprint` o `Web Service`.
4. Conecta el repositorio.
5. Render detectara `render.yaml`.
6. En `Environment`, define:
   - `SESSION_SECRET` con un valor largo y privado.
   - `APP_DATA_DIR` con `/tmp/organizador-data` o la ruta de tu disco persistente.
7. Pulsa `Create Web Service`.
8. Cuando termine, Render te dara una URL publica tipo:
   - `https://tu-app.onrender.com`

## Deploy en Railway

1. Entra a [Railway](https://railway.com/).
2. Crea un proyecto nuevo con `Deploy from GitHub repo`.
3. Selecciona este repositorio.
4. Railway leera `railway.json`.
5. En `Variables`, agrega:
   - `SESSION_SECRET`
   - `APP_DATA_DIR=/data` si vas a usar volumen persistente
6. En `Settings` -> `Networking`, pulsa `Generate Domain`.
7. Railway te dara una URL publica tipo:
   - `https://tu-app.up.railway.app`

## Persistencia recomendada

- Render: monta un disco persistente y apunta `APP_DATA_DIR` a esa ruta.
- Railway: crea un volumen y apunta `APP_DATA_DIR=/data`.

## Verificacion rapida

- `GET /health` debe responder `{"status":"ok"}`
- La app debe abrir desde cualquier dispositivo con la URL publica del proveedor.
- Los archivos subidos se procesan en memoria; no dependen de rutas locales del computador.
