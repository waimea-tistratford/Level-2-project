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
    
@app.post("/recipe/new")
def add_recipe():
    name = request.form.get("name", "").strip()
    ingredients = request.form.getlist("ingredients")

    with connect_db() as db:
        cursor = db.execute(
            "INSERT INTO recipes (name) VALUES (?)",
            (name,)
        )

        recipe_id = cursor.lastrowid

        for ingredient in ingredients:
            ingredient = ingredient.strip()

            if ingredient:
                db.execute(
                    """INSERT INTO ingredients
                       (name, quantity, type, recipe_id)
                       VALUES (?, ?, ?, ?)""",
                    (ingredient, "", "", recipe_id)
                )

    return redirect("/day/recipe")

@app.post("/recipe/delete/<int:id>")
def delete_a_recipe(id):
    with connect_db() as db:
        db.execute("DELETE FROM ingredients WHERE recipe_id = ?", (id,))
        db.execute("DELETE FROM recipes WHERE id = ?", (id,))

    return redirect("/day/recipe")


@app.post("/day/recipe/remove")
def remove_day_recipe():
    day_id = request.form.get("day")

    with connect_db() as db:
        sql = """
            UPDATE days
            SET recipe_id = NULL
            WHERE id = ?
        """
        db.execute(sql, (day_id,))

    return redirect("/")

@app.post("/day/recipe/add")
def assign_day_recipe():
    day_id = request.form.get("day")
    recipe_id = request.form.get("recipe_id")

    with connect_db() as db:
        sql = """
            UPDATE days
            SET recipe_id = ?
            WHERE id = ?
        """
        db.execute(sql, (recipe_id, day_id))

    return redirect("/")


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
            WHERE recipes.id NOT IN (
                SELECT recipe_id
                FROM days
                WHERE recipe_id IS NOT NULL
                  AND id != ?
            )
            ORDER BY recipes.name ASC
        """

        rows = db.execute(sql, (day,)).fetchall()

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

    return render_template(
        "pages/recipe_select.jinja",
        recipes=list(recipes_dict.values()),
        day=day
    )

@app.get("/shopping")
def show_shoppinglist():

    with connect_db() as db:
        sql = """
            SELECT DISTINCT
                ingredients.id,
                ingredients.name
            FROM ingredients
            JOIN days
                ON days.recipe_id = ingredients.recipe_id
            ORDER BY ingredients.name ASC
        """

        ingredients = db.execute(sql).fetchall()

    return render_template(
        "pages/shopping_list.jinja",
        ingredients=ingredients
    )
    
@app.post("/shopping/delete/<int:id>")
def delete_shopping_item(id):

    with connect_db() as db:
        db.execute(
            "INSERT INTO shopping (name, type, qty, have_it) "
            "SELECT name, type, quantity, 1 FROM ingredients WHERE id = ?",
            (id,)
        )

    return redirect("/shopping")
    
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

