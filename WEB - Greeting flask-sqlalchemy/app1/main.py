from flask import Flask
import datetime
from data.jobs import Jobs
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
    job = Jobs()
    job.team_leader = 1
    job.job = "deployment of residential modules 1 and 2"
    job.work_size = 15
    job.collaborators = "2, 3"
    job.start_date = datetime.datetime.now()
    job.is_finished = False
    db_sess = db_session.create_session()
    #db_sess.add(job)
    #db_sess.add(user)
    #db_sess.commit()
    for user in db_sess.query(User).all():
        print(user)


if __name__ == '__main__':
    main()

