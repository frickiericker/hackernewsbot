import os

DATABASE_URL = os.environ.get('DATABASE_URL', None)
STORIES_TO_KEEP = int(os.environ.get('STORIES_TO_KEEP', 1000))
STORY_WARMUP = int(os.environ.get('STORY_WARMUP', 6000))
HACKERNEWS_API_WAIT = float(os.environ.get('HACKERNEWS_API_WAIT', 0.5))

COLLECTOR_SLEEP = int(os.environ.get('COLLECTOR_SLEEP', 300))
CLEANER_SLEEP = int(os.environ.get('CLEANER_SLEEP', 300))
BROKER_SLEEP = int(os.environ.get('BROKER_SLEEP', 10))

MASTODON_INSTANCE = os.environ.get('MASTODON_INSTANCE', None)
MASTODON_CLIENT_ID = os.environ.get('MASTODON_CLIENT_ID', None)
MASTODON_CLIENT_SECRET = os.environ.get('MASTODON_CLIENT_SECRET', None)
MASTODON_EMAIL = os.environ.get('MASTODON_EMAIL', None)
MASTODON_PASSWORD = os.environ.get('MASTODON_PASSWORD', None)
