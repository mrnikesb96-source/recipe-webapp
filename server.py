import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import UserMixin,login_user,LoginManager,current_user,logout_user,login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship, DeclarativeBase,Mapped, mapped_column
from sqlalchemy import Integer,String,Text,ForeignKey
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


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User,int(user_id))  


@app.route("/")
def home():
    return render_template("index.html")









if __name__ == "__main__":
    app.run(debug=True)

