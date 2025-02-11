import sqlite3
import json
from models import Post

POSTS = [
    {
        "id": 1,
        "title": "Filler",
        "userId": 2,
        "categoryId": 2,
        "publicationDate": "5/7/2022",
        "content": "filler",
    }
]
# hardcoded database object


def get_all_posts():
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.title,
            a.user_id,
            a.category_id,
            a.publication_date,
            a.content
        FROM Posts a
        """)

        # Initialize an empty list to hold all post representations
        posts = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an post instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # post class above.
            post = Post(row['id'], row['title'], row['user_id'], row['category_id'],
                        row['publication_date'],
                        row['content'])

            posts.append(post.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(posts)


def get_single_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.title,
            a.user_id,
            a.category_id,
            a.publication_date,
            a.content
        FROM post a
        WHERE a.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an post instance from the current row
        post = Post(data['id'], data['title'], data['user_id'],
                    data['category_id'],
                    data['publication_date'], data['content'])

        return json.dumps(post.__dict__)


def create_post(new_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            INSERT INTO Posts
                (title,user_id,category_id,publication_date,content)
            VALUES
                (?, ?, ?, ?, ?);
            """, (
            new_post['title'],
            new_post['user_id'],
            new_post['category_id'],
            # currently does not display anything on database may need to be filled in directly via form.
            new_post['publication_date'],
            new_post['content'],))

        id = db_cursor.lastrowid

        new_post['id'] = id
        print(new_post)
    return json.dumps(new_post)


def delete_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM post
        WHERE id = ?
        """, (id, ))


def update_post(id, new_post):
    # Iterate the postS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, post in enumerate(POSTS):
        if post["id"] == id:
            # Found the post. Update the value.
            POSTS[index] = new_post
            break
