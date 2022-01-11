import sqlite3
import os

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging

# structural log 
class StructuredMessage(object):
    def __init__(self, message, **kwargs):
        self.message = message
        self.kwargs = kwargs

    def __str__(self):
        return '%s >>> %s' % (self.message, json.dumps(self.kwargs))

struct_message = StructuredMessage

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    try:
        connection = sqlite3.connect('database.db')
        connection.row_factory = sqlite3.Row
    
        # TODO : increment the number of connection
        countrow = connection.execute('SELECT * FROM counts').fetchone()
        count = countrow['connectioncount']
        count = count + 1
        connection.execute('Update counts set connectioncount = ? where id = ?',(count, 1))
        connection.commit()
        return connection
    except:
        app.logger.exception("An error occured")

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.error(struct_message('post retrieved', status='404 not found'))
      # app.logger.error("Non-existing Article 404 Page retrieved!")
      return render_template('404.html'), 404
    else:
      app.logger.info(struct_message('post retrieved', post_id=post['id'], post_title=post['title'], post_created=post['created']))
      # app.logger.info("Article \"%s\" retrieved!", post['title'])
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info(struct_message('page retrieved', page_title='About Us'))
    # app.logger.info("Page \"About Us\" retrieved!")
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            app.logger.info(struct_message('post created', post_title=title))
            # app.logger.info("Article \"%s\" created!", title)

            return redirect(url_for('index'))

    return render_template('create.html')

# Define the healthz endpoint
@app.route("/healthz")
def healthcheck():
    if os.path.exists('database.db'):
        return jsonify({"result": "OK - healthy"})
    else:
        return jsonify({"result": "Error - Missing {}".format('database.db')}), 500


# Define the metrics endpoint
@app.route("/metrics")
def metrics():
    # TODO : retrieve the post_count from the database
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute('SELECT * FROM posts')
    post_count = len(cur.fetchall())
    # TODO : retrieve the number of connection to the database
    cur.execute('SELECT * FROM counts')
    db_connection_count_row = cur.fetchone()
    db_connection_count=db_connection_count_row['connectioncount']
    connection.close()

    response = app.response_class(
        response=json.dumps({"db_connection_count": db_connection_count, "post_count":post_count}),
        status=200,
        mimetype='application/json'
    )
    return response

# start the application on port 3111
if __name__ == "__main__":
   FORMAT = '%(levelname)s:%(name)s:%(asctime)s %(message)s'
   logging.basicConfig(format=FORMAT, level=logging.DEBUG, datefmt='%m/%d/%Y %H:%M:%S')
   app.run(host='0.0.0.0', port='3111')
