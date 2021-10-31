from flask import Flask, request, redirect, render_template, flash, url_for, copy_current_request_context,session
from flask_wtf import CsrfProtect
#Models
from modelos import db, User, Post
#Forms
import forms
#configs
from config import DevelopmentConfig
#mail
from flask_mail import Mail, Message
import threading


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CsrfProtect(app)
mail = Mail()


def send_email(user_email, username):

    msg = Message(
        'Gracias por tu registro en nuestra web =D',
        sender = app.config['MAIL_USERNAME'],
        recipients = [user_email]
    )

    msg.html = render_template('email.html', user = username)

    mail.send(msg)


@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['index', 'posts']:
        return redirect(url_for('login'))
    elif 'username' in session and request.endpoint in ['register', 'login']:
        return redirect(url_for('index'))


def show_posts():
    post_list = Post.query.join(User).add_columns(
        User.username,
        Post.text,
        Post.created_date).order_by(Post.created_date.desc())
    return post_list


@app.route('/', methods = ['GET', 'POST'])
def index():
    post_form = forms.Post_form(request.form)
    if request.method == 'POST' and post_form.validate():
        user_id = session['user_id']
        post = Post(
            user_id = user_id,
            text = post_form.post.data)
        db.session.add(post)
        db.session.commit()

        succes_message = 'Se ha realizado la publicacion'
        flash(succes_message)
        
        

        return redirect(url_for('index'))
    username = session['username']
    all_posts = show_posts()
    return render_template('index.html', user = username, form = post_form, posts = all_posts)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    login_form = forms.Login(request.form)
    if request.method == 'POST' and login_form.validate():
        username = login_form.username.data
        password = login_form.password.data

        user = User.query.filter_by(username = username).first()
        if user is not None and user.verify_password(password):
            succes_message = 'bienvenido {}'.format(username)
            flash(succes_message)
            session['username']= username
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            error_message = 'usuario o contraseña no validos'
            flash(error_message)
    
    return render_template('login.html', form = login_form)


@app.route('/register', methods = ['GET', 'POST'])
def register():
    #importacion del formulario que se usara y almacenamiento en variable pasando como parametros el request.form para 
    register_form = forms.Register_form(request.form)
    if request.method == 'POST' and register_form.validate():
        try:
            #insercion de datos en la tabla Users mediante el modelo User
            user = User(
                register_form.username.data,
                register_form.email.data,
                register_form.password.data
            )

            db.session.add(user)
            db.session.commit()

            #configuracion para el envio del correo en segundo plano y evitar que la pagina se quede
            @copy_current_request_context
            def send_message(email, username):
                send_email(email, username)

            sender = threading.Thread(
                name = 'mail_sender',
                target = send_message,
                args = (user.email, user.username) 
            )

            sender.start()

            succes_message = 'The user has been create succesfully'
            flash(succes_message)

            #redireccion a la funcion que consideremos sea necesaria
            return redirect(url_for('index'))

        except Exception as ex:
            print(ex)
            return "Error"

    return render_template('register.html', form = register_form)

        

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    if 'username' in session:
        session.pop('username', 'user_id')
    return redirect(url_for('login'))


def page_not_found():
    return 'La pagina no existe', 400


if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    with app.app_context():
        db.create_all()

    app.run(port=3000)