from datetime import datetime, timezone

HACKERNEWS_ITEM_URI = 'https://news.ycombinator.com/item?id={id}'

class Item(object):
    def __init__(self, item_id):
        self._id = item_id

    @property
    def id(self):
        return self._id

    @property
    def uri(self):
        return HACKERNEWS_ITEM_URI.format(id=self._id)

class Story(Item):
    def __init__(self, story_id, time=None, deleted=False, dead=False, kids=[],
                 score=None, title=None, **others):
        super().__init__(story_id)
        if time:
            self._time = datetime.fromtimestamp(time, timezone.utc)
        else:
            self._time = None
        self._deleted = deleted
        self._dead = dead
        self._comments = kids
        self._score = score
        self._title = title

    @property
    def time(self):
        return self._time

    @property
    def deleted(self):
        return self._deleted

    @property
    def dead(self):
        return self._dead

    @property
    def comments(self):
        return self._comments

    @property
    def score(self):
        return self._score

    @property
    def title(self):
        return self._title
