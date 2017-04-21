from flask import Flask
import os
import psycopg2

from storydb.storydb import StoryRepository

DATABASE_URL = os.environ.get('DATABASE_URL', None)

app = Flask(__name__)

@app.route('/')
def top_page():
    return report_processing_status(StoryRepository(DATABASE_URL))

def get_database_status(database):
    stories = get_story_statuses(database)
    num_processed = sum(1 for ident, serial, processed in stories if processed)
    return '{} stories, {} processed'.format(len(stories), num_processed)

def report_processing_status(repository):
    num_stories = len(repository.get_stored_stories())
    num_pending = len(repository.get_pending_stories())
    num_processed = num_stories - num_pending
    return '{} stories, {} processed'.format(num_stories, num_processed)
