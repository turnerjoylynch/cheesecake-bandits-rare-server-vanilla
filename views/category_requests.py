import sqlite3
import json

from models import Category


CATEGORIES = []


def create_category(new_category):
    # Get the id value of the last animal in the list
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Categories
            ( label, )
        VALUES
            ( ?,);
        """, (new_category['label'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_category['id'] = id

    return json.dumps(new_category)


def get_all_categories():
    """get all categories """
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM Categories c
        """)

        # Initialize an empty list to hold all post representations
        categories = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an post instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Post class above.
            category = Category(row['id'], row['label'])

            categories.append(category.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(categories)

# Function with a single parameter


def get_single_category(id):

    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM Categories c
        WHERE c.id = ?
        """, (id, ))

        # Convert rows of data into a Python list
        data = db_cursor.fetchone()

        # Iterate list of data returned from database

        # Create an post instance from the current row.
        # Note that the database fields are specified in
        # exact order of the parameters defined in the
        # Post class above.
        category = Category(data['id'], data['label'])

        return json.dumps(category.__dict__)
    # Variable to hold the found animal, if it exists
    # requested_category = None

    # # Iterate the ANIMALS list above. Very similar to the
    # # for..of loops you used in JavaScript.
    # for category in CATEGORIES:
    #     # Dictionaries in Python use [] notation to find a key
    #     # instead of the dot notation that JavaScript used.
    #     if category["id"] == id:
    #         requested_category = category

    # return requested_category


def delete_category(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Categories
        WHERE id = ?
        """, (id, ))
