from flask import Flask
import os
import psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL', None)

app = Flask(__name__)

@app.route('/')
def top_page():
    with psycopg2.connect(DATABASE_URL) as database:
        return get_database_status(database)

def get_database_status(database):
    stories = get_story_statuses()
    num_processed = sum(1 for ident, serial, processed if processed)
    return '{} stories, {} processed'.format(len(stories), num_processed)

def get_story_statuses(database):
    with database.cursor() as cursor:
        cursor.execute('SELECT * FROM processingStatus;')
        return cursor.fetchall()
