import dotenv


def pytest_configure():
    dotenv.load_dotenv()
