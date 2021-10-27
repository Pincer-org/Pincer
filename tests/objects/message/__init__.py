from pincer import __version__
from pincer.objects import Embed

print(Embed(
    title=f"Pincer - {__version__}",
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
).to_dict())
