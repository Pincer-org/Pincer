# <img src="../assets/svg/pincer.svg" height="24px" alt="Pincer Logo"> Pincer

<!--
![PyPI - Downloads](https://img.shields.io/badge/dynamic/json?label=downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2FPincer)](https://pypi.org/project/Pincer)
![PyPI](https://img.shields.io/pypi/v/Pincer)
![PyPI - Format](https://img.shields.io/pypi/format/Pincer)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Pincer)
-->

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/Pincer-org/pincer/badges/quality-score.png?b=main)](https://scrutinizer-ci.com/g/Pincer-org/pincer/?branch=main)
[![Build Status](https://scrutinizer-ci.com/g/Pincer-org/Pincer/badges/build.png?b=main)](https://scrutinizer-ci.com/g/Pincer-org/Pincer/build-status/main)
![Lines of code](https://img.shields.io/tokei/lines/github/Pincer-org/Pincer)
![GitHub last commit](https://img.shields.io/github/last-commit/Pincer-org/Pincer)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/Pincer-org/Pincer)
![GitHub](https://img.shields.io/github/license/Pincer-org/Pincer)
![Code Style](https://img.shields.io/badge/code%20style-pep8-green)
![Discord](https://img.shields.io/discord/881531065859190804)

An asynchronous Python API wrapper meant to replace discord.py

| :exclamation: | The package is currently within the planning phase |
| ------------- | :------------------------------------------------- |

## :pushpin: Links

> <img src="../assets/svg/discord.svg" width="16px" alt="Discord Logo"> ｜Join the Discord server: https://discord.gg/8WkYz3fNFm <br>
> <img src="../assets/svg/pypi.svg" width="16px" alt="PyPI Logo"> ｜The PyPI package: https://pypi.org/project/Pincer <br>
> <img src="../assets/svg/pincer.svg" width="16px" alt="Pincer Logo"> ｜Our website: https://pincer.dev <br>
> 📝 | ReadTheDocs: https://pincer.readthedocs.io

## ☄️ Installation

Use the following command to install Pincer into your Python environment:

```bash
pip install pincer
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

## Current Features

- Discord Gateway communication
- logging
- Http Client
- Events
- Event middleware
- Basic commands with basic argument parsing

**Client base class example:**

```py
from pincer.client import Bot

# Note that both `Bot` and `Client` are valid!
bot = Bot("...")
bot.run()
```

**An example on the `on_ready` event**

```py
from time import perf_counter
from pincer.client import Client

client = Client("...")


@client.event
async def on_ready():
    print(f"Logged in as {client.bot} after {perf_counter()} seconds")


client.run()
```

### Inherited client

You have the possibility to use your own class to inherit from the Pincer bot
base.

```py
from pincer import Client, command


class Bot(Client):
    def __init__(self) -> None:
        super(Bot, self).__init__(token="...")

    @Client.event
    async def on_ready(self) -> None:
        ...

    @command(description="Say something as the bot!")
    async def say(self, message: str):
        return message

    @command(description="Add two numbers!")
    async def add(self, first: int, second: int):
        return f"The addition of `{first}` and `{second}` is `{first + second}`"
```

See an advanced bot implementation:

> <https://github.com/Pincer-org/Pincer-bot>

### Advanced Usage

#### Enable the debug mode

_If you want to see everything that is happening under the hood, either out of
curiosity or to get a deeper insight into the implementation of some features,
we provide debug logging!_

```py
import logging

logging.basicConfig(level=logging.DEBUG)
```

**Note:** _A lot of printing can happen, including sensitive information, so
make sure to be aware of what you're doing if you're enabling it!_

#### Middleware

_From version 0.4.0-dev, the middleware system has been introduced. This system
gives you the full freedom to remove the already existing middleware which has
been created by the developers and create custom events. Your custom middleware
directly receives the payload from Discord. You can't really do anything wrong
without accessing the `override` attribute, but if you access this attribute the
Pincer team will not provide any support for weird behavior. So in short, only
use this if you know what you're doing. An example of using this with a custom
`on_ready` event can be found
[in our docs](https://pincer.readthedocs.io/en/latest/pincer.html#pincer.client.middleware)
._

## 🏷️ License

`© 2021 copyright Pincer`

This repository is licensed under the MIT License.

See LICENSE for details.
