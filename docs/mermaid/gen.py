import aiohttp
import asyncio
import base64
import glob
import io
import os
from PIL import Image


async def download_img(base64_string):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            'https://mermaid.ink/img/' + base64_string.decode("ascii")
        ) as resp:
            return Image.open(io.BytesIO(await resp.content.read()))


async def main():
    funcs = []
    files = []

    for file in glob.glob("*.mmd"):
        with open(file) as f:
            contents = f.read()
            graphbytes = contents.encode("ascii")
            base64_bytes = base64.b64encode(graphbytes)
            files.append(os.path.splitext(file)[0])
            funcs.append(download_img(base64_bytes))

    res = await asyncio.gather(*funcs)

    for file, image in zip(files, res):
        image.save(file + ".png")

if __name__ == "__main__":
    asyncio.run(main())
