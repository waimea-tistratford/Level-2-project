#============================================================================
# Database schema and seed data configuration
#============================================================================


#----------------------------------------------------------------------------
# Table definitions
#----------------------------------------------------------------------------
# Define your tables with a name, a schema and optional seed/sample data,
# using this format, and then add the tables to the Table Registry below:
#
# class TableName:
#     NAME      = "name"
#     SCHEMA    = "CREATE TABLE name (...)"
#     SEED_DATA = "INSERT INTO name (...)" or None
#----------------------------------------------------------------------------

class RecipeTable:

    NAME = "recipes"

    SCHEMA = """
        CREATE TABLE recipes (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT NOT NULL,
            instructions    TEXT
        )
    """

    SEED_DATA = """
        INSERT INTO recipes (name, instructions)
        VALUES
            ("Spaghetti Bolognese", "placeholder"),
            ("Nachos",  "placeholder"),
            ("Tacos",   "placeholder")

    """

class IngredientTable:

    NAME = "ingredients"

    SCHEMA = """
        CREATE TABLE ingredients (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            quantity    TEXT NOT NULL,
            type        TEXT NOT NULL,

            recipe_id   INTEGER,

            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )
    """

    SEED_DATA = """
        INSERT INTO ingredients (name, quantity, type, recipe_id)
        VALUES
            ("Onion", "1 medium", "fruit_veg", 1),
            ("Tomatoes", "1 tin", "fruit_veg", 1),
            ("Lasagne Sheets", "1 box", "pasta", 1),
            ("Onion", "1 medium", "fruit_veg", 1),
            ("Onion", "1 medium", "fruit_veg", 1),

            ("Onion", "1 medium", "fruit_veg", 2),

            ("Onion", "1 medium", "fruit_veg", 3)
    """

class ShoppingTable:

    NAME = "shopping"

    SCHEMA = """
        CREATE TABLE shopping (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT NOT NULL,
            type            TEXT NOT NULL,
            qty             TEXT NOT NULL,
            have_it         INTEGER DEFAULT 0
        )
    """

    SEED_DATA = """
        INSERT INTO shopping (name, type, qty)
        VALUES
            ("Onion", "fruit_veg", "1 medium"),
            ("Cheese", "dairy", "500g"),
            ("Milk", "dairy", "1 litre"),
            ("Lasagne Sheets", "pasta", "1 box")

    """


class DaysTable:

    NAME = "days"

    SCHEMA = """
        CREATE TABLE days (
            id              TEXT UNIQUE NOT NULL,
            name            TEXT NOT NULL,
            recipe_id       INTEGER,

            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )
    """

    SEED_DATA = """
        INSERT INTO days (id, name, recipe_id)
        VALUES
            ("mon", "Monday", null),
            ("Tue", "Tuesday", 2),
            ("Wed", "Wednesday", null),
            ("Thu", "Thursday", null),
            ("Fri", "Friday", 2),
            ("Sat", "Saturday", 3),
            ("Sun", "Sunday", 1)
    """

#----------------------------------------------------------------------------
# Table registry
#----------------------------------------------------------------------------
# Register all of your tables by adding them to the TABLES list here:
#
# TABLES = [
#     Table1Name,
#     Table2Name,
#     etc.
# ]
#
# Note: The table order is important - Create the tables that have
# foreign keys *after* the tables they link to have been created
#----------------------------------------------------------------------------

TABLES = [
    RecipeTable,
    IngredientTable,
    ShoppingTable,
    DaysTable
]

