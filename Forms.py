from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, \
    SelectMultipleField
from wtforms.validators import (
    DataRequired, Length, Email, EqualTo, InputRequired)


class Register(FlaskForm):
    Name = StringField("Please Enter Your Name", validators=[
                       DataRequired(), Length(min=3)])
    Email = StringField(
        "Please Enter Your Email (if available)", validators=[Email()])
    College = StringField(
        "Please Enter Name of Your College", validators=[DataRequired()])
    Events = SelectField("Select A Event", choices=[('1', "Frontliners of FrontEnd"), ('2', "Battles of BackEnd"),
                                                    ('3', "Hackathon(Limited Entries)"), ('4',
                                                                                          "Rap Cypher(Clean)"),
                                                    ('5', "Flash")])
    Group = StringField("Please Choose a Group Name",
                        validators=[Length(min=2)])
    Phone = StringField("Please Enter Your Contact Number",
                        validators=[Length(min=10, max=13)])
    Volunteer = StringField("Volunteer", validators=[DataRequired()])
    Submit = SubmitField('Register')


class Volunteer(FlaskForm):
    Name = StringField("Please Enter Your Name", validators=[
                       DataRequired(), Length(min=3)])
    Password = PasswordField("Set a Password", validators=[DataRequired()])
    Confirm = PasswordField("Confirm Your Password",
                            validators=[DataRequired(), EqualTo('Password', message="Please Check Your Password")])
    Job = SelectField("Please Choose A Job",
                      choices=[('1', "Call and Confirm"), ('2', "Crowd Management"), ('3', "Information Center"),
                               ('4', "Event Management"), ('5', "Ceremonial Duties")])
    Contact = StringField("Please Provide Contact Number",
                          validators=[DataRequired()])
    Register = SubmitField('Register')


class LoginForm(FlaskForm):
    Name = StringField("Enter Your Name", validators=[DataRequired()])
    Password = PasswordField("Enter Your Password",
                             validators=[DataRequired()])
    Remember = BooleanField('Remember Me')
    Login = SubmitField('Register')
