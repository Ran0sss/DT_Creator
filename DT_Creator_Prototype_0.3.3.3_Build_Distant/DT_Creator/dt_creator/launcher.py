"""Entrée du lanceur packagé Streamlit."""
import os
import sys
from pathlib import Path
from streamlit.web import cli as stcli

def main():
    bundle_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    app_path = bundle_dir / "dt_creator" / "app.py"
    sys.argv = [
        "streamlit", "run", str(app_path),
        "--server.address=127.0.0.1",
        "--browser.gatherUsageStats=false",
    ]
    stcli.main()

if __name__ == "__main__":
    main()
