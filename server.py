# for dynamic displaying
import threading
import time
from turbo_flask import Turbo

# flask
import flask

# login/register
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

# forms
from forms.message import SendMessageForm
from forms.user import RegisterForm, LoginForm

# database
import sqlalchemy
from data import db_session
from data.message import Message
from data.user import User

app = flask.Flask(__name__)
app.secret_key = 'simple-messenger-secret-key'
login_manager = LoginManager()
login_manager.init_app(app)
turbo = Turbo(app)

def main():
    db_session.global_init('db/database.sqlite')
    app.run()


# updating messages
@app.context_processor
def inject_load():
    session = db_session.create_session()
    messages = session.query(Message).order_by(Message.id.desc())
    return {'messages': messages}


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.errorhandler(401)
def bad_request(_):
    return flask.redirect('/login')


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # session = db_session.create_session()
    # user = User(login='tester', username='tester')
    # user.set_password('123')
    # session.add(user)
    # session.commit()
    #
    # message = Message(text='Hello, World!')
    # message.user_id = user.id
    # message.user = user
    # session.add(message)
    # session.commit()
    # return "ok"
    print(current_user)
    form = SendMessageForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        message = Message(text=form.text.data)
        message.user = session.query(User).get(current_user.id)
        session.add(message)
        session.commit()
    return flask.render_template('index.html', form=form)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        if session.query(User).filter(User.login == form.login.data).first():
            return flask.render_template('register.html', title='Регистрация',
                                   form=form,
                                   error='Такой пользователь уже есть')
        user = User(
            login=form.login.data,
            username=form.username.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        login_user(user, remember=True)
        return flask.redirect('/')
    return flask.render_template('register.html', title='Регистрация', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.login == form.login.data).first()
        print(user)
        if not user:
            return flask.render_template('login.html',
                                         error='Неправильный логин',
                                         form=form)
        if not user.check_password(form.password.data):
            return flask.render_template('login.html',
                                         error='Неправильный пароль',
                                         form=form)
        login_user(user, remember=True)
        return flask.redirect('/')
    return flask.render_template('login.html', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return flask.redirect('/')


def update_load():
    with app.app_context():
        while True:
            time.sleep(0.2)
            turbo.push(turbo.replace(flask.render_template('load_messages.html'), 'load'))



th = threading.Thread(target=update_load)
th.daemon = True
th.start()

main()
