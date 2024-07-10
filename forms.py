from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, SubmitField, BooleanField, PasswordField, FloatField, URLField, \
    DateField, EmailField, SelectField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import Input

class RegisterUser(FlaskForm):
    nickname = StringField("Nickname", validators=[DataRequired()])
    email = EmailField("example@gmail.com", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, message="Password min length is 8")])
    full_name = StringField("Full Name", validators=[DataRequired()])
    birthday = DateField("dd/mm/YYYY", format='%Y-%m-%d')
    submit = SubmitField("Submit")
    checkbox = BooleanField(validators=[DataRequired()])


class LoginUser(FlaskForm):
    email = StringField("example@gmail.com", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, message="Password min length is 8")])
    nickname = StringField("Nickname", validators=[DataRequired()])
    checkbox = BooleanField(validators=[DataRequired()])
    submit = SubmitField("Submit")


class AddProduct(FlaskForm):
    name = StringField("Product name", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    text = StringField("Text", validators=[DataRequired()])
    promo = SelectField("Promo", choices=[('promo', 'Promo'),
                                          ('no_promo', 'No Promo')])
    category_id = IntegerField("Category ID", validators=[DataRequired()])
    image_url = URLField("Product picture", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AddProductCategory(FlaskForm):
    category_name = StringField("Category name", validators=[DataRequired()])
    id = IntegerField("ID", validators=[DataRequired()])
    submit = SubmitField("Submit")


class SliderWidget(Input):
    input_type = 'range'

    def __call__(self, field, **kwargs):
        kwargs.setdefault('min', 0)
        kwargs.setdefault('max', 50.00)
        kwargs.setdefault('step', 0.1)
        if 'value' not in kwargs:
            kwargs['value'] = field.data or 0.0
        return super(SliderWidget, self).__call__(field, **kwargs)


class SliderForm(FlaskForm):
    slider = FloatField('Slider', widget=SliderWidget(), validators=[DataRequired()])
    submit = SubmitField('Submit')