import subprocess
import sys

env = {"STREAMLIT_SERVER_HEADLESS": "true", "STREAMLIT_BROWSER_SERVER_ADDRESS": "localhost"}
result = subprocess.run(
    [sys.executable, "-m", "streamlit", "run", r"f:\adsense\LocalChronicles\app.py"],
    env={**subprocess.os.environ, **env},
    cwd=r"f:\adsense\LocalChronicles"
)
