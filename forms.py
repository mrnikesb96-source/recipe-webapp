from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,EmailField, URLField,TextAreaField,FormField,FieldList,IntegerField
from wtforms.validators import DataRequired,EqualTo,Email,Optional


class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password",validators=[DataRequired(),
                                       EqualTo("password",message="Password must match")])
    submit = SubmitField("Sign up")

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Sign In")

class IngredientForm(FlaskForm):
    name = StringField("Ingredient",validators=[DataRequired()])
    quantity = StringField("Quantity",validators=[Optional()])
    unit = StringField("Unit",validators=[Optional()])

class InstructionForm(FlaskForm):
    step = TextAreaField("Steps",validators=[Optional()])

class RecipeForm(FlaskForm):
    img_url = URLField("Image URL",validators=[Optional()])
    title = StringField("Recipe Title",validators=[DataRequired()])
    ingredients = FieldList(FormField(IngredientForm), min_entries=2,max_entries=20)
    instructions = FieldList(FormField(InstructionForm),min_entries=2,max_entries=15)
    cook_time = IntegerField("Cook Time (mins)",validators=[DataRequired()])
    submit = SubmitField("Save Recipe") 
