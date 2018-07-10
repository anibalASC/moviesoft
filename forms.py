from wtforms import Form, BooleanField, StringField, SubmitField, PasswordField,validators

class RegistrationForms(Form):
    username = StringField('Username', [validators.length(min=4, max=26)])
    email = StringField('email', [validators.length(min=6, max=40)])
    password = PasswordField('New password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
