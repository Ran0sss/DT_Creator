"""Lanceur PyInstaller pour DT Creator via l’API bootstrap de Streamlit."""
from pathlib import Path
import sys
from streamlit.web import bootstrap

def main():
    bundle_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    app_path = bundle_dir / "dt_creator" / "app.py"
    flag_options = {
        "server.address": "127.0.0.1",
        "browser.gatherUsageStats": False,
    }
    # Evite de repasser par l’interface CLI Click dans le processus PyInstaller.
    bootstrap.run(str(app_path), False, [], flag_options)

if __name__ == "__main__":
    main()
