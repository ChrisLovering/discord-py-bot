# Discord.py Bot
This repo contains a simple discord bot using [discord.py](https://discordpy.readthedocs.io/en/latest/).

The intended use case for this bot is to run on the same device as an [ngrok tunnel](https://ngrok.com/product).
ngrok tunnels have a different url each time you start the program (free version), this bot can scrape the url and send it on request.

Anything in addtion to the above use case is just me experiementing with discord.py

## pip requirements
These files contain the pip requirements for all of the python scripts in this repo

[`requirements.txt`](requirements.txt) is a hand-crafted file of all top-level dependancies.

[`requirements_freeze.txt`](requirements_freeze.txt) is the output from `pip freeze`
