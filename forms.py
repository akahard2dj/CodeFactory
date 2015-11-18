from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, validators
from wtforms.validators import ValidationError

class ContactForm(Form):
    name = StringField("Name", [validators.DataRequired("Please enter your name")])
    email = StringField("E-mail", [validators.DataRequired("Please enter your email address"), validators.Email("Please enter your email address")])
    subject = StringField("Subject", [validators.DataRequired("Please enter a subject")])
    message = TextAreaField("Message", [validators.DataRequired("Please enter a message")])
    submit = SubmitField("Send")
