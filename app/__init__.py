#===========================================================
# PROJECT NAME HERE
# By YOUR NAME HERE
#===========================================================

from flask import Flask, request, session, render_template, flash, redirect, send_file, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os import getenv
from io import BytesIO
import html
from app.helpers import *


# Create the app
app = Flask(__name__)


#===========================================================
# App Routes Handlers
#===========================================================

#-----------------------------------------------------------
# Home page - Show all notes
#-----------------------------------------------------------
@app.get("/")
def show_recipes():
    sql = """
        SELECT
            days.id,
            days.`name` AS d_name,
            days.recipe_id,
            recipes.`name` AS r_name,
            ingredients.`name` AS i_name,
            ingredients.recipe_id AS i_id

        FROM days
        LEFT JOIN recipes
            ON recipes.id = days.recipe_id
        LEFT JOIN ingredients
            ON ingredients.recipe_id = recipes.id
    """

    params = ()

    with connect_db() as db:
        days = db.execute(sql, params).fetchall()

    return render_template("pages/day_list.jinja", days=days)
    
@app.get("/recipe/new")
def add_recipe():
        return render_template("pages/recipe_form.jinja")        

@app.get("/day/recipe")
def get_recipes():
    day = request.args.get("day")

    with connect_db() as db:
        sql = """
            SELECT
                recipes.id AS r_id,
                recipes.name AS r_name,
                ingredients.id AS i_id,
                ingredients.name AS i_name
            FROM recipes
            LEFT JOIN ingredients
                ON ingredients.recipe_id = recipes.id
            ORDER BY recipes.name DESC
        """

        rows = db.execute(sql).fetchall()

    # Group ingredients under each recipe
    recipes_dict = {}

    for row in rows:
        r_id = row["r_id"]

        if r_id not in recipes_dict:
            recipes_dict[r_id] = {
                "id": r_id,
                "name": row["r_name"],
                "ingredients": []
            }

        if row["i_id"] is not None:
            recipes_dict[r_id]["ingredients"].append(row["i_name"])

    recipes = list(recipes_dict.values())

    return render_template(
        "pages/recipe_select.jinja",
        recipes=recipes,
        day=day
    )
    
@app.get("/shopping")
def show_shoppinglist():
    with connect_db() as db:
        sql = """
            SELECT id, name, instructions
            FROM recipes  
            ORDER BY name DESC
        """
        params = ()
        recipes = db.execute(sql, params).fetchall()



        return render_template("pages/shopping_list.jinja",)




        # flash("Test message")
        # flash("Test SUCCESS message", "success")
        # flash("Test INFO message", "info")
        # flash("Test WARNING message", "warning")
        # flash("Test ERROR message", "error")
#===========================================================
# Configure the app
#===========================================================
load_dotenv()
app.config.from_prefixed_env()
init_logging(app)
init_text_filters(app)
init_date_filters(app)
init_error_handlers(app)
init_database()
register_commands(app)

