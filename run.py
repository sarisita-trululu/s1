import os
import sys

import uvicorn


def _set_console_title(title: str) -> None:
    if os.name == "nt":
        try:
            import ctypes

            ctypes.windll.kernel32.SetConsoleTitleW(title)
        except Exception:
            pass
        return

    try:
        sys.stdout.write(f"\33]0;{title}\a")
        sys.stdout.flush()
    except Exception:
        pass


if __name__ == "__main__":
    _set_console_title("Nuby Arango Perez API")
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    reload_enabled = os.environ.get("UVICORN_RELOAD", "").lower() in {"1", "true", "yes"}
    uvicorn.run("app.main:app", host=host, port=port, reload=reload_enabled)
