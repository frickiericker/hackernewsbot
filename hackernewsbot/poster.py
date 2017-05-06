MESSAGE_TEMPLATE = '{title}\n{uri}\n{score} | {comments}'

def _make_toot_text(story):
    return MESSAGE_TEMPLATE.format(
        title=story.title,
        uri=story.uri,
        score=_plural(story.score, 'point'),
        comments=_plural(len(story.comments), 'comment'))

def _plural(number, thing):
    if number == 1:
        return '{} {}'.format(number, thing)
    else:
        return '{} {}s'.format(number, thing)

class MastodonPoster:
    def __init__(self, mastodon_api):
        self._mastodon = mastodon_api

    def post(self, story):
        self._mastodon.post_status({
            'status': _make_toot_text(story),
            'visibility': 'unlisted'
        })
