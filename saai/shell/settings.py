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
        self.disable_analyse=os.getenv('disable_analyse')
        print(f".. current lang {self.lang}, disable_analyse: {self.disable_analyse}")

    @property
    def is_disable_analyse(self):
        return self.disable_analyse is not None and self.disable_analyse=='true'

sett=Settings()

