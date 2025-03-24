from flask import Flask

from data.news import News
from data.users import User
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blog.db")
    user = User()
    user.surname = "Gusine"
    user.name = "Bombombini"
    user.age = 7
    user.position = "Gusine"
    user.speciality = "Italian_WW2_plane"
    user.address = "Italy_Venice"
    user.email = "BomBombini@gusine.com"
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


if __name__ == '__main__':
    main()
