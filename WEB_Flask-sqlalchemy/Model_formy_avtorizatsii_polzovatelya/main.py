from flask import Flask, render_template, redirect, abort
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.categories import Category
from forms.user import RegisterForm, LoginForm, JobForm, DepartmentForm
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from data.departments import Department

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
db_session.global_init("db/mars_users.sqlite")

login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/departments")
def departments():
    with db_session.create_session() as session:
        departments = session.query(Department).all()
        return render_template("departments.html", departments=departments)


@app.route("/departments/add", methods=["GET", "POST"])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(
            title=form.title.data,
            chief=form.chief.data,
            members=form.members.data,
            email=form.email.data,
        )
        with db_session.create_session() as session:
            session.add(department)
            session.commit()
        return redirect("/departments")
    return render_template("department_form.html", form=form, title="Добавление отдела")


@app.route("/departments/<int:id>", methods=["GET", "POST"])
@login_required
def edit_department(id):
    form = DepartmentForm()
    with db_session.create_session() as session:
        department = session.query(Department).get(id)
        if not department:
            abort(404)
        if form.validate_on_submit():
            department.title = form.title.data
            department.chief = form.chief.data
            department.members = form.members.data
            department.email = form.email.data
            session.commit()
            return redirect("/departments")
        form.title.data = department.title
        form.chief.data = department.chief
        form.members.data = department.members
        form.email.data = department.email
    return render_template(
        "department_form.html", form=form, title="Редактирование отдела"
    )


@app.route("/departments/<int:id>/delete", methods=["POST"])
@login_required
def delete_department(id):
    with db_session.create_session() as session:
        department = session.query(Department).get(id)
        if department and (current_user.id == department.chief or current_user.id == 1):
            session.delete(department)
            session.commit()
    return redirect("/departments")


@app.route("/jobs/<int:id>/delete", methods=["POST", "GET"])
@login_required
def delete_job(id):
    with db_session.create_session() as db_sess:
        job = db_sess.query(Jobs).get(id)
        if not job:
            abort(404)
        if job.team_leader != current_user.id and current_user.id != 1:
            abort(403)
        db_sess.delete(job)
        db_sess.commit()
    return redirect("/")


@app.route("/jobs/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_job(id):
    form = JobForm()
    with db_session.create_session() as db_sess:
        job = db_sess.query(Jobs).get(id)
        if not job:
            abort(404)
        form.team_leader.choices = [
            (user.id, f"{user.name} {user.surname}")
            for user in db_sess.query(User).all()
        ]
        form.categories.choices = [
            (category.id, category.name) for category in db_sess.query(Category).all()
        ]
        if current_user.id != 1 and job.team_leader != current_user.id:
            abort(403)
        if form.validate_on_submit():
            job.team_leader = (
                form.team_leader.data if current_user.id == 1 else current_user.id
            )
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.start_date = form.start_date.data
            job.is_finished = form.is_finished.data
            job.categories.clear()
            for category_id in form.categories.data:
                category = db_sess.query(Category).get(category_id)
                if category:
                    job.categories.append(category)
            db_sess.commit()
            return redirect("/")
        form.job.data = job.job
        form.work_size.data = job.work_size
        form.collaborators.data = job.collaborators
        form.start_date.data = job.start_date
        form.is_finished.data = job.is_finished
        form.team_leader.data = job.team_leader
        form.categories.data = [c.id for c in job.categories]
    return render_template("add_job.html", form=form, title="Редактировать работу")


@app.route("/add_job", methods=["GET", "POST"])
@login_required
def add_job():
    form = JobForm()
    with db_session.create_session() as session:
        form.team_leader.choices = [
            (user.id, f"{user.name} {user.surname}")
            for user in session.query(User).all()
        ]
        form.categories.choices = [
            (category.id, category.name) for category in session.query(Category).all()
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
            for category_id in form.categories.data:
                category = session.query(Category).get(category_id)
                if category:
                    job.categories.append(category)
            session.add(job)
            session.commit()
            return redirect("/")
    return render_template("add_job.html", form=form)


@app.route("/")
def index():
    with db_session.create_session() as db_sess:
        jobs = db_sess.query(Jobs).all()
        return render_template("work_log.html", jobs=jobs)


@login_manager.user_loader
def load_user(user_id):
    with db_session.create_session() as session:
        return session.get(User, int(user_id))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Пароли не совпадают",
            )
        with db_session.create_session() as session:
            if session.query(User).filter(User.email == form.email.data).first():
                return render_template(
                    "register.html",
                    title="Регистрация",
                    form=form,
                    message="Такой пользователь уже есть",
                )
            user = User(
                email=form.email.data,
                name=form.name.data,
                surname=form.surname.data,
                age=form.age.data,
                position=form.position.data,
                speciality=form.speciality.data,
                address=form.address.data,
                about=form.about.data,
            )
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            login_user(user)
            return redirect("/")
    return render_template("register.html", title="Регистрация", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with db_session.create_session() as session:
            user = session.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect("/")
            return render_template(
                "login.html", message="Неверный логин или пароль", form=form
            )
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    app.run(port=5000, host="127.0.0.1")
