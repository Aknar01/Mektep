from flaskapp import *
from flask import request, session, redirect, url_for, render_template, flash
from models import User, Question
import add_delete
from flask_mail import Mail, Message
import random
import string

app.config['MAIL_SERVER'] = 'imap.gmail.com'  # Замените на сервер вашей почты
app.config['MAIL_PORT'] = 993  # Порт вашего почтового сервера (обычно 587 для TLS)
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'asanovaknar03@gmail.com'  # Замените на вашу почту
app.config['MAIL_PASSWORD'] = 'asanovak200364777'  # Замените на пароль от вашей почты

mail = Mail(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/test")
def test():
    questions = Question.query.all()
    return render_template('test.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    questions = Question.query.all()
    score = 0
    for question in questions:
        user_answer = request.form.get(f"question_{question.id}")
        if user_answer and user_answer.lower() == question.answer.lower():
            score += 1
    result = f'Вы набрали {score} из {len(questions)} баллов.'
    return render_template('result.html', result=result)

def check_auth():
    if 'authenticated' not in session:
        return False
    return True

@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if not check_auth():
        return redirect(url_for('login'))
    if request.method == 'POST':
        question = request.form['question']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        option5 = request.form['option5']
        answer = request.form['answer']
        if answer not in [option1, option2, option3, option4]:
            return render_template('add_question.html', error="Дұрыс жауап жоқ")
        new_question = Question(question=question, option1=option1, option2=option2, option3=option3, option4=option4, option5=option5, answer=answer)
        db.session.add(new_question)
        db.session.commit()
    return render_template('add_question.html')

# Удаление вопроса
@app.route('/delete_question/<int:question_id>')
def delete_question(question_id):
    if not check_auth():
        return redirect(url_for('login'))
    question_to_delete = Question.query.get_or_404(question_id)
    db.session.delete(question_to_delete)
    db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route("/user/<int:user_id>")
def user(user_id, context=None):
    query = db.session.query(User.user_id == user_id).first()

    if query:
        return render_template("user-page.html", context=query)
    else:
        query = db.session.query(User).filter(User.user_id == user_id).first()
        return render_template("user-page.html", context=query)

# Панель администратора
@app.route('/admin')
def admin_panel():
    questions = Question.query.all()
    return render_template('admin.html', questions=questions)


@app.route("/login", methods = ["GET", "POST"])
def login(context=None):
    if request.method == "POST":
        username = request.form['email']
        password = request.form['password']

        # Проверка учетных данных администратора
        if username == 'admin' and password == 'admin':
            session['authenticated'] = True
            session['admin_authenticated'] = True
            session['uid'] = '0'
            session['login'] = 'admin'
            session['number'] = ''
            session['name'] = 'admin'
            session['sname'] = ''

            return redirect(url_for('admin_panel'))
        user = db.session.query(User).filter_by(login=request.form['email'], password=request.form['password']).first()
        if user:
            session['authenticated'] = True
            session['admin_authenticated'] = False
            session['uid'] = user.user_id
            session['login'] = user.login
            session['name'] = user.name
            session['sname'] = user.surname
            session['number'] = user.number

            return redirect(url_for("user", user_id=user.user_id))
        else:
            return render_template("login.html", context="The login or username were wrong")

    return render_template("login.html", context=context)


@app.route("/logout")
def logout():

    session.pop('authenticated', None)
    session.pop('uid', None)
    session.pop('login', None)
    return redirect(url_for('index'))


@app.route('/register', methods = ["GET", "POST"])
def register(context=None):
    if request.method == "POST":
        login = request.form['email']
        fname = request.form['name']
        sname = request.form['surname']
        pass1 = request.form['password']
        pass2 = request.form['password_conf']
        number = request.form['number']

        data = db.session.query(User).filter_by(login=request.form['email']).first()

        if data:
            return redirect(url_for("register", error="Already registered!"))
        elif pass1!=pass2:
            return redirect(url_for("register", error="Passowords do not match!"))
        else:
            add_delete.add_user(User(login=login,
                                     name=fname,
                                     surname=sname,
                                     password=pass1,
                                     number=number))

            return redirect(url_for("login", context="Succesfully registered!"))
    return render_template("register.html", context=context)

# Генерация случайного пароля
def generate_password():
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(10))
    return password

@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = db.session.query(User).filter_by(login=email).first()

        if user:
            new_password = generate_password()
            user.password = new_password
            db.session.commit()

            msg = Message('Password Reset', sender='asanovaknar03@gmail.com', recipients=[email])
            msg.body = f'Your new password is: {new_password}'
            mail.send(msg)

            flash('Check your email for the new password.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Email not found. Please try again.', 'error')
            return redirect(url_for('forgot_password'))

    return render_template('forgot.html')
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(port=5000, debug=True)


