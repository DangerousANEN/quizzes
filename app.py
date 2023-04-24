from flask import Flask, render_template, redirect, url_for, flash, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, LoginManager, UserMixin, current_user, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
import email_validator

app = Flask(__name__, template_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'super-secret-key'
db = SQLAlchemy(app)
login_manager = LoginManager(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    with db.session() as session:
        return session.get(User, int(user_id))


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm',
                                                                             message='Passwords must match')])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')


class AccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


@app.route('/')
def index():
    # проверяем, есть ли cookie с именем theme
    if request.cookies.get('theme') == 'dark':
        # если cookie существует и равен dark, отображаем темную тему
        return render_template('index.html', theme='dark', title='Home')
    else:
        # если cookie не существует или не равен dark, отображаем светлую тему
        return render_template('index.html', theme='light', title='Home')

@app.route('/toggle-theme')
def toggle_theme():
    # проверяем, есть ли cookie с именем theme
    if request.cookies.get('theme') == 'dark':
        # если cookie существует и равен dark, удаляем его
        resp = make_response(render_template('index.html', theme='light'))
        resp.set_cookie('theme', '', expires=0)
        return resp
    else:
        # если cookie не существует или не равен dark, создаем его
        resp = make_response(render_template('index.html', theme='dark'))
        resp.set_cookie('theme', 'dark', expires=None)
        return resp


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    # проверяем, есть ли cookie с именем theme
    if request.cookies.get('theme') == 'dark':
        # если cookie существует и равен dark, отображаем темную тему
        return render_template('register.html', theme='dark', title='Register', form=form)
    else:
        return render_template('register.html', theme='light', title='Register', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            flash('You have been logged in!', 'success')
            return redirect(url_for('account'))
        else:
            flash('Invalid username or password', 'danger')
    if request.cookies.get('theme') == 'dark':
        return render_template('login.html', theme='dark',  title='Sign In', form=form)
    else:
        return render_template('login.html', theme='light', title='Sign In', form=form)

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        if user and user.password == form.password.data:
            user.username = form.username.data
            db.session.commit()
            flash('Your changes have been saved!', 'success')
            return redirect(url_for('account'))
        else:
            flash('Invalid password', 'danger')
    if request.cookies.get('theme') == 'dark':
        return render_template('account.html', theme='dark', title='My Account', form=form)
    else:
        return render_template('account.html', theme='light', title='My Account', form=form)


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    questions = ['What is the capital of France?', 'What is the highest mountain in the world?']
    options = {
        'What is the capital of France?': ['Paris', 'Berlin', 'London'],
        'What is the highest mountain in the world?': ['Mount Everest', 'Mount Kilimanjaro', 'Mount Fuji']
    }
    if request.method == 'POST':
        score = 0
        for question in questions:
            answer = request.form.get(question)
            if answer and answer in options[question]:
                score += 1
        flash(f'You have scored {score} out of {len(questions)}', 'info')
        return redirect(url_for('quiz'))
    if request.cookies.get('theme') == 'dark':
        return render_template('quiz.html', title='Quiz', theme='dark', questions=questions, options=options)
    else:
        return render_template('quiz.html', title='Quiz', theme='light', questions=questions, options=options)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run()
