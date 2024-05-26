import datetime

from app import app, db, bcrypt
from app.models import User, Url
from app.utils import transform_url

with app.app_context():
    db.create_all()

    try:
        #### Create User ####
        print("Create User")
        password = bcrypt.generate_password_hash("1234").decode("utf-8")
        user = User(id=1,
                    username="joekakone",
                    email="joseph.kakone@gmail.com",
                    password=password)
        db.session.add(user)
        db.session.commit()

        #### Create URLs ####
        print("Create URLs")
        data = [
            [1, 'Joseph Konka', 'https://josephkonka.com/'],
            [2, 'Algo Jungle', 'https://joekakone.github.io/algojungle/'],
            [3, 'Flask Documentation', 'https://flask.palletsprojects.com/en/3.0.x/'],
            [4, 'Keras Examples', 'https://keras.io/examples/']
        ]

        for url in data:
            # Create URL item in database
            url = Url(id=url[0],
                      name=url[1],
                      long_url=url[2],
                      short_url=transform_url(url[0]),
                      created_date=datetime.datetime.now(),
                      user_id=1)
            db.session.add(url)

        db.session.commit()
    except Exception as e:
        pass
