
"""Lanceur PyInstaller pour DT Creator."""
import os
import sys
from pathlib import Path
from streamlit.web import bootstrap


def main():
    bundle_dir = Path(
        getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)
    )
    app_path = bundle_dir / "dt_creator" / "app.py"

    # Place le répertoire courant à côté de app.py.
    # Streamlit pourra ainsi trouver .streamlit/config.toml.
    os.chdir(app_path.parent)

    flag_options = {
        "global.developmentMode": False,
        "server.address": "127.0.0.1",
        "server.port": 8501,
        "server.headless": True,
        "browser.serverAddress": "localhost",
        "browser.serverPort": 8501,
        "browser.gatherUsageStats": False,
    }

    bootstrap.run(
        str(app_path),
        False,
        [],
        flag_options,
    )


if __name__ == "__main__":
    main()
