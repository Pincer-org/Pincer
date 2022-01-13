# Pincer

[![PyPI - Downloads](https://img.shields.io/badge/dynamic/json?label=downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2FPincer)](https://pypi.org/project/Pincer)
![PyPI](https://img.shields.io/pypi/v/Pincer)
![PyPI - Format](https://img.shields.io/pypi/format/Pincer)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Pincer)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/Pincer-org/pincer/badges/quality-score.png?b=main)](https://scrutinizer-ci.com/g/Pincer-org/pincer/?branch=main)
[![Build Status](https://scrutinizer-ci.com/g/Pincer-org/Pincer/badges/build.png?b=main)](https://scrutinizer-ci.com/g/Pincer-org/Pincer/build-status/main)
[![Documentation Status](https://readthedocs.org/projects/pincer/badge/?version=latest)](https://pincer.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/Pincer-org/Pincer/branch/main/graph/badge.svg?token=T15T34KOQW)](https://codecov.io/gh/Pincer-org/Pincer)
![Lines of code](https://tokei.rs/b1/github/pincer-org/pincer?category=code&path=pincer)
![Repo Size](https://img.shields.io/github/repo-size/Pincer-org/Pincer)
![GitHub last commit](https://img.shields.io/github/last-commit/Pincer-org/Pincer)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/Pincer-org/Pincer?label=commits)
![GitHub](https://img.shields.io/github/license/Pincer-org/Pincer)
![Discord](https://img.shields.io/discord/881531065859190804)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![gitmoji](https://img.shields.io/badge/gitmoji-%20🚀%20💀-FFDD67.svg)

## :pushpin: Links

> <img src="../assets/svg/discord.svg" width="16px" alt="Discord Logo"> ｜Join the Discord server: https://discord.gg/pincer <br>
> <img src="../assets/svg/pypi.svg" width="16px" alt="PyPI Logo"> ｜The PyPI package: https://pypi.org/project/Pincer <br>
> <img src="../assets/svg/pincer.svg" width="16px" alt="Pincer Logo"> ｜Our website: https://pincer.dev <br>
> 📝 | ReadTheDocs: https://pincer.readthedocs.io

## ☄️ Installation

Use the following command to install Pincer into your Python environment:

```sh
pip install pincer
```

To install our version with Aiohttp Speedup, use:

```sh
pip install pincer[speed]
```

<details>

<summary>
    ⚙️ <i> Didn't work?</i>
</summary>

Depending on your Python installation, you might need to use one of the
following:

- Python is not in PATH

    ```sh
    path/to/python.exe -m pip install pincer
    ```

- Python is in PATH but pip is not

    ```sh
    python -m pip install pincer
    ```

- Unix systems can use pip3/python3 commands

    ```sh
    pip3 install pincer
    ```

    ```sh
    python3 -m pip install pincer
    ```

- Using multiple Python versions

    ```sh
    py -m pip install pincer
    ```

</details>

**Client base class example:**

```py
from pincer.client import Bot

# Note that both `Bot` and `Client` are valid!
bot = Bot("YOUR_TOKEN_HERE")
bot.run()
```

**An example on the `on_ready` event**

Pincer bots are required to inherit from the Client.

```py
from time import perf_counter
from pincer import Client

marker = perf_counter()


class Bot(Client):

    @Client.event
    async def on_ready():
        print(f"Logged in as {client.bot} after {perf_counter() - marker} seconds")


client = Bot("YOUR_TOKEN_HERE")
client.run()
```

### Interactions

Pincer makes developing application commands intuitive and fast.

```py
from typing import Annotation  # python 3.9+
from typing_extensions import Annotation  # python 3.8

from pincer import Client
from pincer.commands import command, CommandArg, Description
from pincer.objects import UserMessage, User


class Bot(Client):
    @Client.event
    async def on_ready(self) -> None:
        ...

    @command(description="Say something as the bot!")
    async def say(self, message: str):
        return message

    @user_command
    async def user_command(self, user: User):
        return f"The user is {user}"

    @message_command(name="Message command")
    async def message_command(self, message: UserMessage):
        return f"The message read '{message.content}'"

    @command(description="Add two numbers!")
    async def add(
        self,
        first: Annotation[int, Description("The first number")],
        second: Annotation[int, Description("The second number")]
    ):
        return f"The addition of `{first}` and `{second}` is `{first + second}`"


```

For more examples, you can take a look at the examples folder or check out our
bot:

> <https://github.com/Pincer-org/Pincer-bot>

You can also read the interactions guide for more information:
> <https://docs.pincer.dev/en/latest/interactions.html>

### Advanced Usage

#### Enable the debug mode

_If you want to see everything that is happening under the hood, either out of
curiosity or to get a deeper insight into the implementation of some features,
we provide debug logging!_

```py
import logging

logging.basicConfig(level=logging.DEBUG)
```

#### Middleware

_The middleware system was introduced in version `0.4.0-dev`. This system gives you the
freedom to create custom events and remove the already existing middleware created by
the developers. Your custom middleware directly receives the payload from
Discord. You can't do anything wrong without accessing the `override` attribute, but if
you do access it, the Pincer team will not provide any support for weird behavior.
So, in short, only use this if you know what you're doing. An example of using
the middleware system with a custom `on_ready` event can be found
[in our docs](https://pincer.readthedocs.io/en/latest/pincer.html#pincer.client.middleware).
._

## 🏷️ License

`© 2021 copyright Pincer`

This repository is licensed under the MIT License.

See LICENSE for details.
