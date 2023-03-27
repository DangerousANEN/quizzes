import datetime
from flask import (
    Flask,
    render_template,
    request,
    make_response,
    session
)

app = Flask(__name__)

# http://127.0.0.1:8080/
# http://127.0.0.1:8080/index

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_lyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)


def load_user(user_id):
    """Загрузка пользователя"""
    pass


@app.route('/')
@app.route('/index')
def index():
    """Простая HTML-страница"""
    return """<div id="container_demo" >
    
    <a class="hiddenanchor" id="tologin"></a>
    <div id="wrapper">
    
        <div id="login" class="animate form">
            <form  action="mysuperscript.php" autocomplete="on">
                <h1>Вход</h1>
                <p>
                    <label for="username" class="uname" data-icon="u" > введите ваше имя </label>
                    <input id="username" name="username" required="required" type="text" >
                </p>
                
                <p>
                    <label for="password" class="youpasswd" data-icon="p"> введите пароль </label>
                    <input id="password" name="password" required="required" type="password">
                </p>
                
                <p class="keeplogin">
                    <input type="checkbox" name="loginkeeping" id="loginkeeping" value="loginkeeping" />
                    <label for="loginkeeping">Запомнить логин и пароль </label>
                </p>
                
                <p class="login button">
                    <input type="submit" value="Войди в аккаунт" />
                </p>
                
            </form>
        </div>

        <div id="subscribe" class="animate form">
            <form  action="mysuperscript.php" autocomplete="on">
                <h1> Регистрация </h1>
                <p>
                    <label for="usernamesignup" class="uname" data-icon="u">Придумайте имя</label>
                    <input id="usernamesignup" name="usernamesignup" required="required" type="text">
                </p>
                
                <p>
                    <label for="emailsignup" class="youmail" data-icon="e" > Введите вашу почту</label>
                    <input id="emailsignup" name="emailsignup" required="required" type="text" >
                </p>
                
                <p>
                    <label for="passwordsignup" class="youpasswd" data-icon="p">Придумайте пароль </label>
                    <input id="passwordsignup" name="passwordsignup" required="required" type="password" >
                </p>
                
                <p>
                    <label for="passwordsignup_confirm" class="youpasswd" data-icon="p">Повторите пароль</label>
                    <input id="passwordsignup_confirm" name="passwordsignup_confirm" required="required" type="password">
                </p>
                
                <p class="signin button">
                    <input type="submit" value="Зарегистрироваться"/>
                </p>
                
                <p class="change_link">
                </p>
                
            </form>
        </div>
    </div>
</div>"""


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
    
