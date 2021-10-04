from glob import glob

from pincer import Client


class Bot(Client):
    def __init__(self, *args, **kwargs):
        self.load_cogs()
        super().__init__(*args, **kwargs)

    def load_cogs(self):
        """Load all cogs from the `cogs` directory."""
        for cog in glob("cogs/*.py"):
            self.load_cog(cog.replace("/", ".").replace("\\", ".")[:-3])


if __name__ == "__main__":
    Bot("XXXYOURBOTTOKENHEREXXX").run()
