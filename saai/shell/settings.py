import logging
logger = logging.getLogger(__name__)

class Settings(object):
    def __init__(self):
        from dotenv import load_dotenv
        from pathlib import Path
        import os
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
        self.lang=os.getenv("lang")
        print(f".. current lang {self.lang}")

sett=Settings()

