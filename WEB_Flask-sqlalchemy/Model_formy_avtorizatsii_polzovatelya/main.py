from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.jobs import Jobs
from forms.user import RegisterForm, LoginForm, JobForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

db_session.global_init("db/mars_users.sqlite")

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    session = db_session.create_session()
    form.team_leader.choices = [
        (user.id, f"{user.name} {user.surname}") for user in session.query(User).all()
    ]

    if form.validate_on_submit():
        job = Jobs(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            start_date=form.start_date.data,
            is_finished=form.is_finished.data,
        )
        session.add(job)
        session.commit()
        return redirect('/')
    return render_template('add_job.html', form=form)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("work_log.html", jobs=jobs)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.get(User, int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        login_user(user)

        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/')
        return render_template('login.html', message="Неверный логин или пароль", form=form)
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')



if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
