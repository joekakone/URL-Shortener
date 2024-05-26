import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = '=&zn8lo42ycteu*y_u@os&%xrn@o*4$@x^%g8s^mb%z^q19d-k'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Others Config
    BASE_URL = "https://knk.com/" if os.environ.get('ENV') == 'PROD' else 'http://127.0.0.1:5000'
