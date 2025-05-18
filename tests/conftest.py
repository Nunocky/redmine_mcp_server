import os

from dotenv import load_dotenv

# プロジェクトルートの .env を明示的に指定
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
