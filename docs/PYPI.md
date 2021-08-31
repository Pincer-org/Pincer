# Pincer

<!--
[![PyPI - Downloads](https://img.shields.io/badge/dynamic/json?label=downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2FPincer)](https://pypi.org/project/Pincer)
![PyPI](https://img.shields.io/pypi/v/Pincer)
![PyPI - Format](https://img.shields.io/pypi/format/Pincer)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Pincer)
-->

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/Pincer-org/pincer/badges/quality-score.png?b=main)](https://scrutinizer-ci.com/g/Pincer-org/pincer/?branch=main)
[![Build Status](https://scrutinizer-ci.com/g/Pincer-org/Pincer/badges/build.png?b=main)](https://scrutinizer-ci.com/g/Pincer-org/Pincer/build-status/main)
![GitHub repo size](https://img.shields.io/github/repo-size/Pincer-org/Pincer)
![GitHub last commit](https://img.shields.io/github/last-commit/Pincer-org/Pincer)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/Pincer-org/Pincer)
![GitHub](https://img.shields.io/github/license/Pincer-org/Pincer)
![Code Style](https://img.shields.io/badge/code%20style-pep8-green)
![Discord](https://img.shields.io/discord/881531065859190804)

*An asynchronous python API wrapper meant to replace discord.py*

# The package is currently within the planning phase

## 📌 Links

> Join the discord server: https://discord.gg/8WkYz3fNFm

> The pypi package: https://pypi.org/project/Pincer/

> Our website: https://pincer.dev


## ☄️ Installation

Use the following command to install Pincer into your python environment:

```bash
pip install pincer
```

<details>
	<summary>
		⚙️ <i> Didn't work?</i>
	</summary>

Depending on your python installation, you might need to use one of the following.

*pip isn't in the path but python is*
```sh
python -m pip install pincer
```

*Unix system can use pip3/python3 command*
```sh
python3 -m pip install pincer
```

```sh
pip3 install pincer
```

*python isn't in the path*
```sh
path/to/python.exe -m pip install pincer
```

*Using multiple python versions*
```sh
py -m pip install pincer
```
</details>

## Current Features
- Dispatcher
- Logging
- HTTP Client
- Client base class 
- Basic events *Improved* 

**Client base class Example:**

```py
from pincer.client import Bot

# Note that both `Bot` and `Client` are valid!
bot = Bot("...")
bot.run()
```

**An example on `on_ready` event

```py
from time import perf_counter
from pincer.client import Client

client = Client("...")


@client.event
async def on_ready():
    print(f"Logged in as {client.bot} after {perf_counter()} seconds")


client.run()
```

### Enable the debug mode

*If you want to see everything that is happening under the hood, 
either for curiosity or the implementation of some features,
we provide a debug logging!*

```py
import logging

logging.basicConfig(level=logging.DEBUG)
```

**Note** *A lot of printing can happen, with sensitive information, 
make sure to be aware or what your doing if your enable it!*


## 🏷️ License

`© 2021 copyright Pincer`

This repository is licensed under the MIT License.

See LICENSE for details.
