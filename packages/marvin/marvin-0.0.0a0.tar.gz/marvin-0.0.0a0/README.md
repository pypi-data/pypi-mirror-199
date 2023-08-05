#  Marvin 🤖💬


Marvin is an open-source, batteries-included library for deploying custom AI tools. 

> "Let’s build robots with Genuine People Personalities," they said. So they tried it out with me. I’m a personality prototype. You can tell, can’t you?
>
> -- [Marvin](https://www.youtube.com/clip/UgkxNj9p6jPFM8eWAmRJiKoPeOmvQxb8viQv)

## Highlights



🤖 Custom bots with names, personalities, and instructions

🔋 Batteries included - get up and running instantly

🔌 Plugin system lets bots run any software 

💬 Persistent threads with multiple bots

📡 Powered by GPT-4 or GPT-3.5

🌈 ChromaDB for vector search

🐍 Async Python API

🖥️ Interactive chat CLI

⚡️ FastAPI REST API

## Getting started

Launching a bot is simple!

1. **Install** Marvin by running `pip install marvin`

2. **Chat** by running `marvin chat`. You'll be prompted to provide an [OpenAI API key](https://platform.openai.com/account/api-keys) if it isn't already set. You can optionally provide your bot with a name, personality, or instructions to customize the conversation:

```shell
marvin chat -p "knows every Star Wars meme" Hello there
```
<img width="1034" alt="image" src="https://user-images.githubusercontent.com/153965/226232390-c98ffee3-c272-42fa-befb-70d94bebfda7.png">


## Python API

This example shows how to configure a bot programmatically, using Marvin's async API.

```python
from marvin import Bot

bot = Bot(personality='knows every Star Wars meme')

await bot.say('Hello there')
```

## Rest API

Launch the Marvin REST API by running `marvin server start`. You can visit `http://localhost:4200` to view the API documentation.

## UI

*Coming soon...*
## Plugins

Plugins add functionality to your bot beyond simple conversation. By default, bots have access to plugins that can search the web, visit URLs, and evaluate mathematical expressions. It's easy to add new plugins or develop your own.

```python
from marvin import Bot, Plugin

class RandomNumber(Plugin):
    def run(self, a:float, b:float) -> float:
        """Generate a random number between a and b"""
        return a + (b - a) * random.random()

bot = Bot(plugins=[RandomNumber()])

await bot.say('Use the plugin to pick a random number between 41 and 43')
```
