from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

db_session.global_init("db/mars_users.sqlite")

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.get(User, int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('templates/register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")

        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('templates/register.html', title='Регистрация', form=form,
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
        return redirect('/success')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/success')
        return render_template('login.html', message="Неверный логин или пароль", form=form)
    return render_template('login.html', form=form)


@app.route('/success')
def success():
    return "<h2>Регистрация прошла успешно! 🚀 Добро пожаловать в миссию!</h2>"


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
