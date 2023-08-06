import os
import re
from setuptools import setup,find_packages


requires = ["pycryptodome==3.16.0","aiohttp==3.8.3","asyncio==3.4.3","tinytag==1.8.1","Pillow==9.4.0","pytz==2023.2"]
_long_description = """

## iLiaShahpy

> Elegant, modern and asynchronous Rubika MTProto API framework in Python for users and bots

<p align="center">
    <img src="https://s2.uupload.ir/files/img_20230325_150407_843_hcgc_thumb.jpg" alt="iLiaShah" width="500">
    <br>
    <b>library iLiaShah</b>
    <br>
</p>

###  iLiaShah library documents soon...


### How to import the Rubik's library

``` bash
from iLiaShahpy import Messenger

Or

from iLiaShahpy import RoboRubika
```

### How to import the anti-advertising class

``` bash
from iLiaShahpy.Zedcontent import Antiadvertisement
```

### How to install the library

``` bash
pip install iLiaShahpy==3.8.3
```

### My ID in Telegram

``` bash
@Sourse_py
```
## An example:
``` python
from iLiaShahpy import Messenger

bot = Messenger("Your Auth Account")

gap = "your guid or gap or pv or channel"

bot.sendMessage(gap,"libraryiLiaShah")
```

## And Or:
``` python
from iLiaShahpy import RoboRubika

bot = RoboRubika("Your Auth Account")

gap = "your guid or gap or pv or channel"

bot.sendMessage(gap,"libraryiLiaShah")
```
Made by iLiaShah



### Key Features

- **Ready**: Install iLiaShahpy with pip and start building your applications right away.
- **Easy**: Makes the Rubika API simple and intuitive, while still allowing advanced usages.
- **Elegant**: Low-level details are abstracted and re-presented in a more convenient way.
- **Fast**: Boosted up by pycryptodome, a high-performance cryptography library written in C.
- **Async**: Fully asynchronous (also usable synchronously if wanted, for convenience).
- **Powerful**: Full access to Rubika's API to execute any official client action and more.


### Our channel in messengers

``` bash
Our channel in Ita

https://eitaa.com/Sourse_py

Our channel in Soroush Plus

https://splus.ir/Sourse_py

Our channel in Rubika

https://rubika.ir/Sourse_py

Our channel in the Gap

https://gap.im/Sourse_py

Our channel on Telegram

https://t.me/Sourse_py
```
"""

setup(
    name = "iLiaShahpy",
    version = "3.8.5",
    author = "iLiaShah",
    author_email = "iLiaShahmanam@gmail.com",
    description = (" library Robot Rubika"),
    license = "MIT",
    keywords = ["iLia","iLiaShahpy","iLiashahpy","iLiaShohpy","bot","Bot","BOT","Robot","ROBOT","robot","self","api","API","Api","rubika","Rubika","RUBIKA","Python","python","aiohttp","asyncio"],
    url = "",
    packages = ['iLiaShahpy'],
    long_description=_long_description,
    long_description_content_type = 'text/markdown',
    install_requires=requires,
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    "Programming Language :: Python :: Implementation :: PyPy",
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11'
    ],
)
