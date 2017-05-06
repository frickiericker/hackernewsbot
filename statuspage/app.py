from flask import Flask
import os
import psycopg2

from storydb.storydb import StoryRepository

DATABASE_URL = os.environ.get('DATABASE_URL', None)

app = Flask(__name__)

@app.route('/')
def top_page():
    return report_processing_status(StoryRepository(DATABASE_URL))

def report_processing_status(repository):
    num_stories = len(repository.get_stored_stories())
    num_pending = len(repository.get_pending_stories())
    num_processed = num_stories - num_pending
    return '{} stories, {} processed'.format(num_stories, num_processed)
