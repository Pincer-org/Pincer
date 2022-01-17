from pincer import Client

from cogs import OnReadyCog, SayCog, ErrorHandler


class Bot(Client):
    def __init__(self, *args, **kwargs):
        super().load_cogs(OnReadyCog, SayCog, ErrorHandler)
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    Bot("XXXYOURBOTTOKENHEREXXX").run()
