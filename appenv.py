import os

DATABASE_URL = os.environ.get('DATABASE_URL', None)
STORIES_TO_KEEP = int(os.environ.get('STORIES_TO_KEEP', 1000))

STORY_WARMUP = float(os.environ.get('STORY_WARMUP', 6000))
STORY_COOLDOWN = float(os.environ.get('STORY_COOLDOWN', 10000))
STORY_MINIMUM_COMMENTS = int(os.environ.get('STORY_MINIMUM_COMMENTS', 1))
STORY_MINIMUM_SCORE = int(os.environ.get('STORY_MINIMUM_SCORE', 5))

HACKERNEWS_API_WAIT = float(os.environ.get('HACKERNEWS_API_WAIT', 0.5))
COLLECTOR_SLEEP = float(os.environ.get('COLLECTOR_SLEEP', 300))
CLEANER_SLEEP = float(os.environ.get('CLEANER_SLEEP', 300))
BROKER_SLEEP = float(os.environ.get('BROKER_SLEEP', 10))
POSTING_WAIT = float(os.environ.get('POSTING_WAIT', 5))

HACKERNEWS_TIMEOUT = os.environ.get('HACKERNEWS_TIMEOUT', 5.0)
MASTODON_TIMEOUT = os.environ.get('MASTODON_TIMEOUT', 10.0)

MASTODON_INSTANCE = os.environ.get('MASTODON_INSTANCE', None)
MASTODON_CLIENT_ID = os.environ.get('MASTODON_CLIENT_ID', None)
MASTODON_CLIENT_SECRET = os.environ.get('MASTODON_CLIENT_SECRET', None)
MASTODON_EMAIL = os.environ.get('MASTODON_EMAIL', None)
MASTODON_PASSWORD = os.environ.get('MASTODON_PASSWORD', None)
