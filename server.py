import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import UserMixin,login_user,LoginManager,current_user,logout_user,login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship, DeclarativeBase,Mapped, mapped_column
from sqlalchemy import Integer,String,Text,ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from forms import *

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("APP_SECRET_KEY")

class Base(DeclarativeBase):
    # tells sqlalchemy that any class that inherits from Base is a database model
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance/devrecipe.db" #binds where the database connection lives
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(model_class=Base, app=app) #binds db variable to the sqlalchemy database and 

login_manager = LoginManager()
login_manager.init_app(app) #connects the login_manager class to the app
login_manager.login_view = "login" #tells flask which endpoint to send users to if not logged in

class User(db.model,UserMixin):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    email: Mapped[str] = mapped_column(String(100),nullable=False)
    password: Mapped[str] = mapped_column(String(100),nullable=False)
    recipes: Mapped[list["Recipe"]] = relationship(back_populates="author")

class Recipe(db.model):
    __tablename__ = "recipes"
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    title: Mapped[str] = mapped_column(String(100),nullable=False)
    image_url: Mapped[str] = mapped_column(String(200),nullable=True)
    instructions: Mapped[str] = mapped_column(Text,nullable=True)
    accounts_id: Mapped[int] = mapped_column(
        Integer,ForeignKey("accounts.id",name="fk_recipe_account_id"),nullable=False
    )
    author: Mapped["User"] = relationship(back_populates="recipes") 
    ingredients: Mapped[list["Ingredient"]] = relationship(back_populates="recipe")

class Ingredient(db.model):
    __tablename__ = "ingredients"
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    name: Mapped[str] = mapped_column(String(100),nullable=False)
    quantity: Mapped[str] = mapped_column(String(20),nullable=True)
    unit = Mapped[str] = mapped_column(String(20),nullable=True)
    recipe_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("recipes.id",name="fk_ingredient_recipe_id"),nullable=False
    )
    recipe: Mapped["Recipe"] = relationship(back_populates="ingredients")


def unpack_instructions(fieldlist:FieldList):
    """Take FieldList obj and convert subform data to list"""
    return [
        subform.form.steps.data.strip()
        for subform in fieldlist
        if subform.form.steps.data.strip()
    ]

def unpack_ingredients(fieldlist:FieldList):
    """Unpack FieldList obj into a list of dictionaries"""
    list_ = []
    for subform in fieldlist:
        if subform.form.name.data.strip():
            new_ingredient = {
                "name":subform.form.name.data.strip(),
                "quantity": subform.form.quantity.data.strip(),
                "unit": subform.form.unit.data.strip()
            }
            list_.append(new_ingredient)
    return list_

def render_with_overlays(template, **context):
    """
    Wrapper around render_template that always injects
    login/register forms and overlay toggle variable.
    """
    return render_template(
        template,
        login_form=LoginForm(),
        register_form=RegisterForm(),
        show_login_overlay=False,
        show_register_overlay=False,
        **context  # merge in any extra context unique to this page
    )


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User,int(user_id))  


@app.route("/", methods=["POST","GET"])
def home():
    login_form = LoginForm()
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user_email = register_form.email.data
        user_password = register_form.password.data
        existing_acc = db.session.execute(db.select(User).where(getattr(User,"email") == user_email)).scalar()
        if not existing_acc:
            hashed_pass = generate_password_hash(user_password,"pbkdf2:sha256",salt_length=8)
            try:
                new_user = User(email=user_email,password=hashed_pass)
                db.session.add(new_user)
                db.session.commit()
                flash("Welcome! Sign-in","success")
                return render_with_overlays("index.html",show_login_overlay=True)
            except SQLAlchemyError:
                db.session.rollback()
                flash("Sorry an error occurred during account creation, try again later.","danger")
                return render_with_overlays("index",show_register_overlay=True)
                
        else:
            flash("Sorry this email is already registerd", "danger")
            return render_with_overlays("index.html",show_register_overlay=True)
    elif login_form.validate_on_submit():
        submitted_email = login_form.email.data
        submitted_password = login_form.password.data
        user = db.session.execute(db.select(User).where(User.email==submitted_email)).scalar()
        if user:
            valid = check_password_hash(user.password,submitted_password)
            if valid:
                login_user(user)
                flash("Welcome Back!","success")
                return render_with_overlays("recipe.html")
            else:
                flash("Email not found","danger")
                return render_with_overlays("index.html",show_login_overlay=True)
    return render_with_overlays("index.html")


@app.route("/browse")
def browse():
    return render_with_overlays("browse.html")

@app.route("/recipes",methods=["POST","GET"])
def recipes():
    return render_with_overlays("recipe.html")





if __name__ == "__main__":
    app.run(debug=True)

