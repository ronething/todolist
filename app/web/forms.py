# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from app.models import User


class TodoListForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 64)])
    status = RadioField('Done or Not Done', validators=[DataRequired()], choices=[("1", 'YES'), ("0", 'NO')])
    submit = SubmitField('submit')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(1, 24)])
    password = PasswordField('password', validators=[DataRequired(), Length(1, 24)])
    submit = SubmitField('Login')

    def validate_username(self, field):
        username = field.data
        count = User.query.filter_by(username=username).count()
        if count == 0:
            raise ValidationError("account doesn't exist")


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(1, 24)])
    password = PasswordField('password', validators=[DataRequired(), Length(1, 24)])
    confirm_password = PasswordField(
        label="confirm password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Password and Confirm Password inconsistent"),
            Length(1, 24)
        ]
    )
    submit = SubmitField('Register')

    def validate_username(self, field):
        username = field.data
        count = User.query.filter_by(username=username).count()
        if count == 1:
            raise ValidationError("username is already taken")
