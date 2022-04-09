"""
A simple discord bot which displays the use case of sending a welcome image when a user joins a guild!
This is a simple example of a more worked out bot.
"""
import logging
from glob import glob
from importlib import import_module
from os import getenv
from time import perf_counter

from dotenv import load_dotenv

from pincer import Client, Cog


class Bot(Client):
    loaded_cogs = 0

    def __init__(self, *args, **kwargs):
        cog_loading_started = perf_counter()
        self.load_packages()
        cog_loading_ended = perf_counter()
        self.cogs_load_time = round((cog_loading_ended - cog_loading_started) * 100, 2)
        super().__init__(*args, **kwargs)

    @Client.event
    async def on_ready(self):
        print(f"Successfully running bot on {self.bot}!")
        print(f"Loaded {self.loaded_cogs} cog(s) in {self.cogs_load_time}ms")

    @staticmethod
    def _process_package_location(location: str) -> str:
        """Convert a file path to a python importable path"""
        return location.replace("/", ".").replace("\\", ".")[:-3]

    def load_packages(self):
        """
        Goes through all files in the Cogs directory, and loads the classes that inherit
        from pincer.Cog.

        Side effects: Imports all files that it maps over in this file.
        """
        for container in glob("cogs/*.py"):
            module = import_module(self._process_package_location(container))

            for definition in dir(module):
                if definition.startswith("_"):
                    continue

                if obj := getattr(module, definition, None):
                    parents = getattr(obj, "__bases__", None) or []

                    if Cog in parents:
                        self.load_cog(obj)
                        self.loaded_cogs += 1
                        logging.info(
                            "Successfully loaded %s (%s)" % (definition, container)
                        )


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.WARN)
    Bot(getenv("BOT_TOKEN")).run()
