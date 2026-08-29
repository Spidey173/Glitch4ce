"""WTForms form classes for authentication and input validation."""
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Optional, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    """Player login form supporting password verification or guest fallback."""
    username = StringField(
        'Player Codename',
        validators=[
            DataRequired(message="Codename is required."),
            Length(min=2, max=30, message="Codename must be between 2 and 30 characters.")
        ]
    )
    password = PasswordField(
        'Passcode (Optional for Guest)',
        validators=[Optional(), Length(min=4, max=100)]
    )
    remember_me = BooleanField('Keep Link Active')
    submit = SubmitField('ACTIVATE GAMING')


class RegisterForm(FlaskForm):
    """Player registration form for protected accounts."""
    username = StringField(
        'Player Codename',
        validators=[
            DataRequired(message="Codename is required."),
            Length(min=2, max=30, message="Codename must be between 2 and 30 characters.")
        ]
    )
    password = PasswordField(
        'Security Passcode',
        validators=[
            DataRequired(message="Password is required."),
            Length(min=6, max=100, message="Password must be at least 6 characters.")
        ]
    )
    confirm_password = PasswordField(
        'Confirm Passcode',
        validators=[
            DataRequired(message="Please confirm your password."),
            EqualTo('password', message="Passcodes must match.")
        ]
    )
    submit = SubmitField('REGISTER ACCOUNT')

    def validate_username(self, field):
        """Ensure username is unique."""
        user = User.query.filter_by(username=field.data.strip()).first()
        if user and user.password_hash is not None:
            raise ValidationError('This codename is already registered with a password. Please log in.')
