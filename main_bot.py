import os
import aiohttp
import discord
from discord.ext import commands
from urllib.parse import urlparse
import google_home

bot = commands.Bot(command_prefix="!")

async def get_ngrok_ip():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("http://localhost:4040/api/tunnels") as r:
                js = await r.json()
                tunnels = [urlparse(tunnel["public_url"]).netloc for tunnel in js["tunnels"]]
                return ' '.join(tunnels)
        except aiohttp.ClientConnectorError as e:
            return f"Connection error. This usually means ngrok isn't running.\n{str(e)}"

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author != bot.user:
        print(f"{message.author} sent '{message.content}' in {message.channel}")
        await bot.process_commands(message)

@bot.group()
async def alfred(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Invalid alfred command passed...")

@alfred.command()
async def say(ctx, *, message='test'):
    google_home.play_tts(message)
    await ctx.send(f'Now playing {message}')

# Gets the current url(s) of the ngrok tunnel
@alfred.command()
async def ip(ctx):
    ip = await get_ngrok_ip()
    await ctx.send(ip)

# Sends a dm to the user
@alfred.command()
async def dm(ctx, user: discord.User, *, message=None):
    if message and message.lower().startswith('ip'):
        message = ' '.join([await get_ngrok_ip(), message[2:].lstrip()])
    else:
        message = message or "This is a default DM message, as none was specified!"
    await user.send(message)

bot.run(os.environ["DISCORD_BOT_TOKEN"])
