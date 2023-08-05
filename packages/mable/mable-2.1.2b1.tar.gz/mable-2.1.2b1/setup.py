# -*- coding: utf-8 -*-
# Copyright (c) 2020 Nekokatt
# Copyright (c) 2021-present davfsa
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import re
import types

import setuptools


def long_description():
    text = """<div align="center">
<h1>mable</h1>
<h1> Документация в разработке оповещение будет в дс </h1>
<a href="https://discord.gg/T2Mbw9u9gh"><img height="20" alt="Discord invite" src="https://discord.com/api/guilds/1069253926479724583/widget.png"></a>
</div>

Самоуверенный, статически типизированный микро-фреймворк Discord для Python3 и asyncio, который поддерживает REST версии Discord v10 и
API-интерфейсы шлюза.

Построенный на благих намерениях и надежде, что он будет расширяемым и многоразовым, а не препятствием для будущего
развития.

В настоящее время поддерживаются Python 3.8, 3.9, 3.10 и 3.11.

## Installation

Установите marble из PyPI с помощью следующей команды:

```bash
python -m pip install -U mable
# Windows users may need to run this instead...
py -3 -m pip install -U mable
```

----

## Bots

marble предоставляет две различные реализации бота по умолчанию в соответствии с вашими потребностями:
- [GatewayBot](#gatewaybot)
- [RESTBot](#restbot)

### GatewayBot

Шлюзовой бот - это тот, который будет подключаться к Discord через шлюз и получать
события через него. Простым примером запуска может быть следующий:

```py
import mable

bot = mable.GatewayBot(token="...")

@bot.listen()
async def ping(event: mable.GuildMessageCreateEvent) -> None:
    #If a non-bot user mentions your bot, respond with 'Pong!'.

    # Do not respond to bots nor webhooks pinging us, only user accounts
    if not event.is_human:
        return

    me = bot.get_me()

    if me.id in event.message.user_mentions_ids:
        await event.message.respond("Pong!")

bot.run()
```

Это будет отвечать только на сообщения, созданные в гильдиях. Вместо этого вы можете использовать `DM Message Create Event`, чтобы прослушивать только
Dm или `Message Create Event` для прослушивания как DMS, так и сообщений от гильдии.

Если вы хотите настроить используемые намерения, чтобы изменить, о каких событиях уведомляется ваш бот, то вы
можете передать kwarg `intents` конструктору `Gateway Bot`:
```py
import mable

# the default is to enable all unprivileged intents (all events that do not target the
# presence, activity of a specific member nor message content).
bot = mable.GatewayBot(intents=mable.Intents.ALL, token="...")
```

Приведенный выше пример включил бы все намерения, тем самым позволяя получать события, связанные с присутствием участников
(сначала вам нужно будет внести свое приложение в белый список, чтобы иметь возможность запустить бота, если вы это сделаете).

События определяются аннотацией типа в параметре event или, альтернативно, как тип, передаваемый
декоратору `@bot.listen()`, если вы не хотите использовать подсказки типа.

```py
import mable

bot = mable.GatewayBot("...")

@bot.listen()
async def ping(event: mable.MessageCreateEvent):
    ...

# or

@bot.listen(mable.MessageCreateEvent)
async def ping(event):
    ...
```

### RESTBot

Тестовый
бот создает сервер взаимодействия, на который Discord будет ** отправлять только ** события взаимодействия,
которые можно обрабатывать и на которые можно реагировать.

Примером простого "REST Both" может быть следующее:

```py
import asyncio

import mable


# This function will handle the interactions received
async def handle_command(interaction: mable.CommandInteraction):
    # Create an initial response to be able to take longer to respond
    yield interaction.build_deferred_response()

    await asyncio.sleep(5)

    # Edit the initial response
    await interaction.edit_initial_response("Edit after 5 seconds!")


# Register the commands on startup.
#
# Note that this is not a nice way to manage this, as it is quite spammy
# to do it every time the bot is started. You can either use a command handler
# or only run this code in a script using `RESTApp` or add checks to not update
# the commands if there were no changes
async def create_commands(bot: mable.RESTBot):
    application = await bot.rest.fetch_application()

    await bot.rest.set_application_commands(
        application=application.id,
        commands=[
            bot.rest.slash_command_builder("test", "My first test command!"),
        ],
    )


bot = mable.RESTBot(
    token="...",
    token_type="...",
    public_key="...",
)

bot.add_startup_callback(create_commands)
bot.set_listener(mable.CommandInteraction, handle_command)

bot.run()
```

В отличие от `GatewayBot`, регистрация слушателей выполняется через `.set_listener`, и она принимает тип взаимодействия
, который будет принимать обработчик.

Обратите внимание, что для того, чтобы приведенный выше код заработал, требуется небольшая настройка. Вам нужно будет разместить проект во
Всемирной паутине (страшно!), а затем зарегистрировать URL-адрес на [портале приложений Discord](https://discord.com/developers/applications )
для вашего приложения в разделе "URL конечной точки взаимодействия".

Быстрый способ загрузить своего бота в Интернет и сделать его доступным через Discord (** только для среды разработки **) - **это
с помощью такого инструмента, как [ngrok](https://ngrok.com/) или [localhost.run](https://localhost.run/). Более подробную информацию о том, как их использовать, можно найти на их соответствующих веб-сайтах.**

### Common helpful features

Обе реализации используют полезные аргументы, такие как настройка тайм-аутов для запросов
и включение прокси-сервера,
которые передаются непосредственно боту во время инициализации.

Также обратите внимание, что вы могли бы передать дополнительные параметры `bot.run` во время разработки, например:

```py
import mable

bot = mable.GatewayBot("...")
# or
bot = mable.RESTBot("...", "...")

bot.run(
    asyncio_debug=True,             # enable asyncio debug to detect blocking and slow code.

    coroutine_tracking_depth=20,    # enable tracking of coroutines, makes some asyncio
                                    # errors clearer.

    propagate_interrupts=True,      # Any OS interrupts get rethrown as errors.
)
```

Существует множество других полезных опций, которыми вы можете воспользоваться, если пожелаете. Ссылки на соответствующие документы можно увидеть
ниже:
- GatewayBot.run - ранее было сказано документация в разработке как только будет готово будет оповещение
- RESTBot.run - ранее было сказано документация в разработке как только будет готово будет оповещение

---

## REST-only applications

Возможно, вы захотите интегрироваться только с REST API, например, при написании веб-панели мониторинга.

Это относительно просто сделать:

```py
import mable
import asyncio

rest = mable.RESTApp()

async def print_my_user(token):
    await rest.start()
  
    # We acquire a client with a given token. This allows one REST app instance
    # with one internal connection pool to be reused.
    async with rest.acquire(token) as client:
        my_user = await client.fetch_my_user()
        print(my_user)

    await rest.close()
        
asyncio.run(print_my_user("user token acquired through OAuth here"))
```

---

## Optional Features

Дополнительные функции могут быть указаны при установке mable:

* `server` - Установите зависимости, необходимые для включения стандартной функциональности сервера взаимодействия mable (REST Both).
* `speedups` - подробно описано в [`mable[speedups]`](#maablespeedups).

Пример:

```bash
# To install mable with the speedups feature:
python -m pip install -U mable[speedups]

# To install mable with both the speedups and server features:
python -m pip install -U mable[speedups, server]
```

## Additional resources

Возможно, вы захотите использовать командный фреймворк поверх marble, чтобы вы могли быстро начать писать бота, не
внедряя свой собственный обработчик команд.

mable по умолчанию не включает в себя командную платформу, поэтому для этого вам потребуется выбрать стороннюю библиотеку:


## Повышение эффективности вашего приложения

По мере масштабирования вашего приложения вам, возможно, потребуется скорректировать некоторые параметры, чтобы оно работало нормально.

### Флаги оптимизации на Python

CPython предоставляет два флага оптимизации, которые удаляют внутренние проверки безопасности, полезные для разработки, и изменяют
другие внутренние настройки в интерпретаторе.

- `питон bot.py ` - без оптимизации - это значение по умолчанию.
- `python -O bot.py ` - оптимизация первого уровня - такие функции, как внутренние утверждения, будут отключены.
- `питон -ОО bot.py ` - оптимизация второго уровня - дополнительные функции (** включая все строки документации **) будут удалены из
  загруженный код во время выполнения.
**При запуске ботов в производственной среде рекомендуется минимум первый уровень оптимизации**.


Не стесняйтесь также присоединяться к нашему [Discord](https://discord.gg/T2Mbw9u9gh), чтобы напрямую задавать вопросы сопровождающим! Они будут
будем рады помочь вам и направить в правильном направлении.
"""
    return text


def parse_meta():
    with open(os.path.join("mable", "_about.py")) as fp:
        code = fp.read()

    token_pattern = re.compile(r"^__(?P<key>\w+)?__.*=\s*(?P<quote>(?:'{3}|\"{3}|'|\"))(?P<value>.*?)(?P=quote)", re.M)

    groups = {}

    for match in token_pattern.finditer(code):
        group = match.groupdict()
        groups[group["key"]] = group["value"]

    return types.SimpleNamespace(**groups)


def parse_requirements_file(path):
    with open(path) as fp:
        dependencies = (d.strip() for d in fp.read().split("\n") if d.strip())
        return [d for d in dependencies if not d.startswith("#")]


metadata = parse_meta()

setuptools.setup(
    name="mable",
    version=metadata.version,
    description="Разумный Discord API для Python 3, построенный на asyncio и благих намерениях",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    author=metadata.author,
    maintainer=metadata.maintainer,
    maintainer_email=metadata.email,
    license=metadata.license,
    url='https://discord.gg/T2Mbw9u9gh',
    python_requires=">=3.8,>=3.9,>=3.10,>=3.11",
    packages=setuptools.find_namespace_packages(include=["mable*"]),
    entry_points={"console_scripts": ["mable = mable.cli:main"]},
    install_requires=parse_requirements_file("requirements.txt"),
    extras_require={
        "speedups": parse_requirements_file("speedup-requirements.txt"),
        "server": parse_requirements_file("server-requirements.txt"),
    },
    test_suite="tests",
    include_package_data=True,
    zip_safe=False,
    project_urls={
        "Discord": 'https://discord.gg/T2Mbw9u9gh',
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Communications :: Chat",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
)
