# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

import aiohttp
import argparse
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


async def download_file(file):
    with open(file) as f:
        contents = f.read()
        graphbytes = contents.encode("ascii")
        base64_bytes = base64.b64encode(graphbytes)
        image = await download_img(base64_bytes)
        image.save(os.path.splitext(file)[0] + ".png")


async def download_all(directory):
    if not directory:
        directory = ""

    await asyncio.gather(*(
        download_file(file)
        for file in glob.glob(directory + "*.mmd")
    ))


def main():
    parser = argparse.ArgumentParser(
        description='Download rendered mermaid files.'
    )
    parser.add_argument(
        '--file',
        type=str,
        nargs='?',
        help='A file to download. If not specified all files are downloaded.',
        default=None
    )
    parser.add_argument(
        '--dir',
        type=str,
        nargs='?',
        help='Directory to search. Does not work with --file.',
        default=None
    )

    args = parser.parse_args()

    if "help" in args:
        print(args)
        return

    if args.file:
        asyncio.run(download_file(args.file))
        return

    asyncio.run(download_all(args.dir))


if __name__ == "__main__":
    main()
