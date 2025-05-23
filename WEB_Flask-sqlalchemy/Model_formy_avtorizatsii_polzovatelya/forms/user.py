from flask_wtf import FlaskForm
from wtforms import (PasswordField,
                     StringField, TextAreaField, SelectField, IntegerField, SelectMultipleField, DateTimeField, BooleanField, SubmitField)
from wtforms.validators import DataRequired, EqualTo, Length, Email
import datetime
from data import db_session
from data.jobs import Jobs
from data.users import User
from data.categories import Category


class RegisterForm(FlaskForm):
    email = StringField('Login / email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])

    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Specialty', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])

    about = TextAreaField("About yourself")
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class JobForm(FlaskForm):
    team_leader = SelectField('Руководитель', coerce=int, validators=[DataRequired()])
    job = StringField('Название работы', validators=[DataRequired(), Length(min=2, max=100)])
    work_size = IntegerField('Объем работы (часы)', validators=[DataRequired()])
    collaborators = StringField('Сотрудники (через запятую)', validators=[Length(max=255)])
    start_date = DateTimeField('Дата начала работы', default=datetime.datetime.now, format='%Y-%m-%d %H:%M:%S')
    is_finished = BooleanField('Завершена работа?')
    categories = SelectMultipleField('Категории', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Добавить работу')

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        session = db_session.create_session()

        users = session.query(User).all()
        self.team_leader.choices = [(user.id, user.name) for user in users]

        categories = session.query(Category).all()
        self.categories.choices = [(category.id, category.name) for category in categories]

    def save_job(self):
        session = db_session.create_session()
        job = Jobs(
            team_leader=self.team_leader.data,
            job=self.job.data,
            work_size=self.work_size.data,
            collaborators=self.collaborators.data,
            start_date=self.start_date.data,
            is_finished=self.is_finished.data
        )

        for category_id in self.categories.data:
            category = session.query(Category).get(category_id)
            job.categories.append(category)

        session.add(job)
        session.commit()


class DepartmentForm(FlaskForm):
    title = StringField('Название отдела', validators=[DataRequired(), Length(min=2, max=100)])
    chief = SelectField('Руководитель отдела', coerce=int, validators=[DataRequired()])
    members = StringField('Список участников (ID через запятую)', validators=[Length(max=255)])
    email = StringField('Контактный e-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        with db_session.create_session() as session:
            users = session.query(User).all()
            self.chief.choices = [(user.id, f"{user.surname} {user.name}") for user in users]
