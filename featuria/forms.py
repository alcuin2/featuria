from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, \
    IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, \
    NumberRange
from featuria.models import User


class RegistrationForm(FlaskForm):

    fullname = StringField('Fullname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists.")


class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class UpdateForm(FlaskForm):

    fullname = StringField('Fullname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email already exists.")


class AddFeatureForm1(FlaskForm):

    client = SelectField('Select Client', coerce=int, choices=[], validators=[DataRequired()])
    submit = SubmitField('Next')


class AddFeatureForm2(FlaskForm):

    title = StringField('Title', validators=[DataRequired(), Length(min=4)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=20, max=500)])
    priority = SelectField('Priority', coerce=int, choices=[], validators=[DataRequired()])
    product_area = SelectField('Product Area', choices=[], validators=[DataRequired()])
    target_date = DateField('Target Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add Feature')


class UpdateFeatureForm(FlaskForm):

    title = StringField('Title', validators=[DataRequired(), Length(min=4)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=20, max=500)])
    priority = SelectField('Priority', coerce=int, choices=[], validators=[DataRequired()])
    product_area = SelectField('Product Area', choices=[], validators=[DataRequired()])
    target_date = DateField('Target Date', format='%Y-%m-%d', validators=[DataRequired()])
    status = SelectField('Status', coerce=str, choices=[("Pending", "Pending"), ("Completed", "Completed")],
                         validators=[DataRequired()])
    submit = SubmitField('Update Feature')


class AddClientForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField('Add Client')


class AddProductAreaForm(FlaskForm):

    title = StringField("Title", validators=[DataRequired()])
    submit = SubmitField("Add Product Area")


class PriorityRangeForm(FlaskForm):

    range = IntegerField("Priority Range", validators=[DataRequired(message="Integer field."),
                                                       NumberRange(min=10, max=20, message="Ranges between 10 and 20")])
    submit = SubmitField("Update Range")


class EditClientForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField('Update Client')


class EditProductAreaForm(FlaskForm):

    title = StringField('Name', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField('Update ProductArea')


