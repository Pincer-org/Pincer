# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from pincer.objects.message import Embed

DICT = {
    'title': 'Pincer - 0.6.4',
    'description': (
        '🚀 An asynchronous python API wrapper meant '
        'to replace discord.py\n> Snappy discord api '
        'wrapper written with aiohttp & websockets'
    ),
    'fields': [
        {
            'name': '**Github Repository**',
            'value': '> https://github.com/Pincer-org/Pincer'
        }
    ],
    'image': {
        'url': (
            'https://repository-images.githubusercontent.com/'
            '400871418/045ebf39-7c6e-4c3a-b744-0c3122374203'
        )
    },
    'thumbnail': {
        'url': 'https://pincer.dev/img/icon.png'
    }
}

EMBED = Embed(
    title="Pincer - 0.6.4",
    description=(
        "🚀 An asynchronous python API wrapper meant to replace"
        " discord.py\n> Snappy discord api wrapper written "
        "with aiohttp & websockets"
    )
).add_field(
    name="**Github Repository**",
    value="> https://github.com/Pincer-org/Pincer"
).set_thumbnail(
    url="https://pincer.dev/img/icon.png"
).set_image(
    url=(
        "https://repository-images.githubusercontent.com"
        "/400871418/045ebf39-7c6e-4c3a-b744-0c3122374203"
    )
)


def has_key_vals(actual, required):
    return all(actual.get(key) == val for key, val in required.items())


class TestDispatch:

    def test_embed_to_dict(self):
        """
        Tests whether or not the dispatch class its string conversion
        is correct.
        """
        assert has_key_vals(EMBED.to_dict(), DICT)

    def test_embed_from_dict(self):
        assert has_key_vals(
            Embed.from_dict(DICT).to_dict(),
            DICT
        )
