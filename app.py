from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, LoginManager, UserMixin, current_user, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

app = Flask(__name__, template_folder='templates')
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
    return render_template('index.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


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
    return render_template('login.html', title='Sign In', form=form)


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
    return render_template('account.html', title='My Account', form=form)


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
    return render_template('quiz.html', title='Quiz', questions=questions, options=options)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run()
