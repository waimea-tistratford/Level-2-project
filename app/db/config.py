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
            instructions    TEXT,
        )
    """

    SEED_DATA = """
        INSERT INTO recipes (name, instrsuctions)
        VALUES
            ("Spaghetti Bolognese",    "Fry the onion in olive oil in the electric frying pan at 180°C for 5-6 minutes.
                                        Add the grated carrots and cook for 2-3 minutes.
                                        Add the beef mince, breaking it up a
                                        Stir in the tomato paste and cook for 1 minute.
                                        Add the chopped tomatoes and stock. Reduce the heat to 120-140°C and simmer for 30-45 minutes, stirring occasionally.
                                        Cook the spaghetti separately in a pot of boiling salted water for 8-10 minutes, then drain.
                                        Add the cooked spaghetti to the mince and mix well. Top with cheese."),

            ("Nachos",                 "Heat the electric frying pan to medium-high and add a little oil.
                                        Add the onion and cook for 2-3 minutes.
                                        Add the mince and break it up with a wooden spoon. Cook until browned with no pink remaining.
                                        Add a splash of water. Cook for another 1-2 minutes.
                                        Add the beans and mixed vegetables. Cook for 2-3 minutes.
                                        Stir in the diced tomato for the last minute, or leave it fresh.
                                        Put tortilla chips in each bowl. Add the hot mince mixture and grated cheese.),

            ("tacos",                  "Heat the electric frying pan to 180°C and add a little oil.
                                        Add beef mince and cook for about 5-7 minutes, breaking it up until completely browned.
                                        Add grated carrot and cook for 2-3 minutes.
                                        Add taco seasoning and a small amount of water. Stir well and cook for another 2-3 minutes.
                                        Reduce the heat to 140°C and cook for a further 5 minutes, stirring occasionally.
                                        Warm the taco shells according to the packet instructions.
                                        Fill the taco shells with the mince mixture.
                                        Add cheese and any other toppings you like."),

    """

class IngredientTable:

    Name = "ingredient"

    SCHEMA = """
        CREATE TABLE ingredient (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            type        TEXT NOT NULL,
            qauntity    TEXT NOT NULL,
            have_it     INTEGER DEFAULT 0,
            recipe_id   INTEGER NOT NULL,

            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )
    """

    SEED_DATA = """
        INSERT INTO ingredient (name, type, quantity, have_it)
        VALUES
            ("Onion", "1 medium", "fruit_veg"),
            ("Olive oil", "1 tbsp", "misc"),
            ("Carrots", "2 medium", "fruit_veg"),
            ("Beef mince", "500 g", "meat"),
            ("Tomato paste", "2 tbsp", "misc"),
            ("Chopped tomatoes", "1can", "fruit_veg"),
            ("Spaghetti", "400 g", "misc"),
            ("Salt", "1 tsp", "misc"),
            ("Cheese", "100 g", "dairy"),
            ("Olive oil", "1 tbsp", "misc"),
            ("Onion", "1 medium", "fruit_veg"),
            ("Beef mince", "500 g", "meat"),
            ("Beans", "1 can", "misc"),
            ("Mixed vegetables", "200 g", "fruit_veg"),
            ("Diced tomatoes", "2 medium", "fruit_veg"),
            ("Tortilla chips", "200 g", "snacks"),
            ("Cheese", "150 g", "dairy"),
            ("Olive oil", "1 tbsp", "misc"),
            ("Beef mince", "500 g", "meat"),
            ("Carrot", "1 medium", "fruit_veg"),
            ("Taco seasoning", "30 g", "misc"),
            ("Taco shells", "12", "misc"),
            ("Cheese", "150 g", "dairy"),
    """

class ShoppingTable:

    Name = "shopping"

    SCHEMA = """
        CREATE TABLE shopping (
            ingredient_id  INTEGER NOT NULL,
            qauntity       TEXT NOT NULL,
            have_it        INTEGER DEFAULT 0,


            FOREIGN KEY (ingredient_id) REFERENCES ingredient(id)
        )
    """

    SEED_DATA = """
        INSERT INTO shopping (quantity, have_it)
        VALUES

    """    

# Add more table classes here...



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
    ShoppingTable
]

