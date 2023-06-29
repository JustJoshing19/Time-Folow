from dotenv import load_dotenv
from os import environ

class Config:
    load_dotenv()
    appEmail: str = environ["APPEMAIL"]
    appPassword: str = environ["APPPASSWORD"]