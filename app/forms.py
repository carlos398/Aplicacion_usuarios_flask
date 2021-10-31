from modelos import User
from wtforms import Form, StringField, TextField, validators, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.fields.simple import HiddenField


class Login(Form):
    def length_honeypot(form, field):
        if len(field.data):
            raise validators.ValidationError('El campo debe estar vacio')


    username = StringField('username', [
        validators.Required(message = 'The username is required'),
        validators.length(min=4, max=25, message='the username is out of the text range')

    ])

    password = PasswordField('Password', [
        validators.Required(message = 'The password is required')
    ])

    honeypot = HiddenField('', [length_honeypot])


class Register_form(Form):
        
    def length_honeypot(form, field):
        if len(field.data):
            raise validators.ValidationError('error')


    username = StringField('username', [
        validators.Required(message = 'The username is required'),
        validators.length(min=4, max=25, message='the username is out of the text range')

    ])

    password = PasswordField('Password', [
        validators.Required(message = 'The password is required')
    ])

    email = EmailField('Email', [
        validators.Required(message = 'The email is required'),
        validators.length(min=15, max=60, message = 'the email is out of text range')
    ])

    honeypot = HiddenField('', [length_honeypot])

    def validate_username(form, field):
        username = field.data
        user = User.query.filter_by(username = username).first()
        if user is not None:
            raise validators.ValidationError('The username is allready in use')

    def validate_email(form, field):
        email = field.data
        email = User.query.filter_by(email = email).first()
        if email is not None:
            raise validators.ValidationError('The email is allready in use try again')


class Post_form(Form):

    def length_honeypot(form, field):
        if len(field.data):
            raise validators.ValidationError('error')


    post = TextField('')

    honeypot = HiddenField('',[length_honeypot])


class Coment_form(Form):

    def length_honeypot(form, field):
        if len(field.data):
            raise validators.ValidationError('error')


    coment = TextField('')

    honeypot = HiddenField('',[length_honeypot])