import os

# pgsql database to use: postgres://user:pass@host:port/path
DATABASE_URL = os.environ.get('DATABASE_URL', None)

# Number of stories to keep in the database
STORIES_TO_KEEP = int(os.environ.get('STORIES_TO_KEEP', 1000))

# Wait this number of seconds before filtering a story
STORY_WARMUP = float(os.environ.get('STORY_WARMUP', 6000))

# Story is filtered out if its number of comments is less than this
STORY_MINIMUM_COMMENTS = int(os.environ.get('STORY_MINIMUM_COMMENTS', 1))

# Story is filtered out if its score is less than this
STORY_MINIMUM_SCORE = int(os.environ.get('STORY_MINIMUM_SCORE', 4))

# Drop stories unconditionally after this number of seconds
STORY_COOLDOWN = float(os.environ.get('STORY_COOLDOWN', 10000))

# Hacker news API root
HACKERNEWS_API = os.environ.get('HACKERNEWS_API',
                                'https://hacker-news.firebaseio.com/v0')

# Wait at least this number of seconds between requests
HACKERNEWS_API_WAIT = float(os.environ.get('HACKERNEWS_API_WAIT', 0.5))

# Timeout for hacker news API
HACKERNEWS_TIMEOUT = float(os.environ.get('HACKERNEWS_TIMEOUT', 5))

# Interval for the collector task
COLLECTOR_SLEEP = float(os.environ.get('COLLECTOR_SLEEP', 300))

# Interval for the clearner task
CLEANER_SLEEP = float(os.environ.get('CLEANER_SLEEP', 300))

# Interval for the broker task
BROKER_SLEEP = float(os.environ.get('BROKER_SLEEP', 10))

# Wait at least this number of seconds between social posts
POSTING_WAIT = float(os.environ.get('POSTING_WAIT', 5))

# Timeout for mastodon API
MASTODON_TIMEOUT = float(os.environ.get('MASTODON_TIMEOUT', 10))

# First mastodon instance and account
MASTODON_INSTANCE = os.environ.get('MASTODON_INSTANCE', None)
MASTODON_CLIENT_ID = os.environ.get('MASTODON_CLIENT_ID', None)
MASTODON_CLIENT_SECRET = os.environ.get('MASTODON_CLIENT_SECRET', None)
MASTODON_EMAIL = os.environ.get('MASTODON_EMAIL', None)
MASTODON_PASSWORD = os.environ.get('MASTODON_PASSWORD', None)

# Second mastodon instance and account
MASTODON_INSTANCE_2 = os.environ.get('MASTODON_INSTANCE_2', None)
MASTODON_CLIENT_ID_2 = os.environ.get('MASTODON_CLIENT_ID_2', None)
MASTODON_CLIENT_SECRET_2 = os.environ.get('MASTODON_CLIENT_SECRET_2', None)
MASTODON_EMAIL_2 = os.environ.get('MASTODON_EMAIL_2', None)
MASTODON_PASSWORD_2 = os.environ.get('MASTODON_PASSWORD_2', None)
