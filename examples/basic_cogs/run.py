from glob import glob

from pincer import Client

from cogs import OnReadyCog, SayCog, ErrorHandler


class Bot(Client):
    def __init__(self, *args, **kwargs):
        self.load_cogs()
        super().__init__(*args, **kwargs)

    def load_cogs(self):
        self.load_cog(OnReadyCog)
        self.load_cog(SayCog)
        self.load_cog(ErrorHandler)


if __name__ == "__main__":
    Bot("XXXYOURBOTTOKENHEREXXX").run()
