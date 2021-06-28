from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, Email
from .models import Hero

class UserLoginForm(FlaskForm):
    # email, password, submit_button
    email = StringField("Email: ", validators = [DataRequired(), Email()])
    username = StringField("Username: ", validators = [DataRequired()])
    password = PasswordField("Password: ", validators = [DataRequired()])
    submit_button = SubmitField()

class HeroForm(FlaskForm):
    # A Form for the User to fill out for their Hero/Villan
    name = StringField("Name of Hero or Villan: ", validators = [DataRequired()])
    power = StringField("The Super Power(s): ", validators = [DataRequired()])
    is_a_hero = RadioField("Hero or Villain? ", choices =[(True, "Hero"), (False, "Villain")], validators = ([DataRequired()]))
    comics_appeared_in = IntegerField("Comics They Have Appeared In: ", validators = ([DataRequired()]))
    description = StringField("Description: ")
    back_story = StringField("Their Back Story: ")
    submit_button = SubmitField()