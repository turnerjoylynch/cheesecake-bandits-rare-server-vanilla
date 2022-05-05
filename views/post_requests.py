import sqlite3
import json
from models import Post
from datetime import datetime

POSTS = []

def create_post(post):
    """Adds a post to the database when user publishes

    Args:
        post (dictionary): The dictionary passed to the register post request

    Returns:
        json string: Contains the token of the newly created post
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Insert into Posts (user_id, category_id, title, publication_date, image_url, content, approved) values (?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            post['user_id'],
            post['category_id'],
            post['title'],
            post['publication_date'],
            post['image_url'],
            post['content'],
            post['approved'],
            datetime.now()
        ))

        id = db_cursor.lastrowid

        return json.dumps({
            'token': id,
            'valid': True
        })


def get_all_posts():
    """get all posts """
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id, 
            p.category_id, 
            p.title, 
            p.publication_date, 
            p.image_url, 
            p.content, 
            p.approved
        FROM post p
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
            # Post class above.
            post = Post(row['id'], row['user_id'], row['category_id'],
                            row['title'], row['publication_date'],
                            row['image_url'], row['content'], row['approved'])

            posts.append(post.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(posts)


def get_single_post(id):
    """ get single """
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id, 
            p.category_id, 
            p.title, 
            p.publication_date, 
            p.image_url, 
            p.content, 
            p.approved
        FROM post p
        WHERE p.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an post instance from the current row
        post = Post(data['id'], data['user_id'], data['category_id'],
                            data['title'], data['publication_date'],
                            data['image_url'], data['content'], data['approved'])

        return json.dumps(post.__dict__)


def post(post):
    """ create """
    # Get the id value of the last post in the list
    max_id = POSTS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the post dictionary
    post["id"] = new_id

    # Add the post dictionary to the list
    POSTS.append(post)

    # Return the dictionary with `id` property added
    return post


def delete_post(id):
    """delete post"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM post
        WHERE id = ?
        """, (id, ))


def update_post(id, new_post):
    """ update """
    # Iterate the POSTS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, post in enumerate(POSTS):
        if post["id"] == id:
            # Found the post. Update the value.
            POSTS[index] = new_post
            break


def get_posts_by_user_id(user_id):
    """ get by """
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        WHERE p.user_id = ?
        """, (user_id, ))

        posts = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'],
                            row['title'], row['publication_date'],
                            row['image_url'], row['content'], row['approved'])
            posts.append(post.__dict__)

    return json.dumps(posts)


def get_posts_by_approved(approved):
    """ get by """
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id, 
            p.category_id, 
            p.title, 
            p.publication_date, 
            p.image_url, 
            p.content, 
            p.approved
        WHERE a.approved = ?
        """, (approved, ))

        posts = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'],
                            row['title'], row['publication_date'],
                            row['image_url'], row['content'], row['approved'])
            posts.append(post.__dict__)

    return json.dumps(posts)
