import os
import aiohttp
import discord
from discord.ext import commands
from urllib.parse import urlparse

bot = commands.Bot(command_prefix="!")

async def get_ngrok_ip():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("http://localhost:4040/api/tunnels") as r:
                js = await r.json()
                tunnels = [urlparse(tunnel["public_url"]).netloc for tunnel in js["tunnels"]]
                return *tunnels
        except aiohttp.ClientConnectorError as e:
            return f"Connection error. This usually means ngrok isn't running.\n{str(e)}"

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.group()
async def alfred(ctx):
    print(f"{ctx.author} sent {ctx.message.content} in {ctx.channel}")
    if ctx.invoked_subcommand is None:
        await ctx.send("Invalid alfred command passed...")

# Gets the current url(s) of the ngrok tunnel
@alfred.command()
async def ip(ctx):
    await ctx.send(await get_ngrok_ip())

# Sends a dm to the user
@alfred.command()
async def dm(ctx, user: discord.User, *, message=None):
    message = message or "This is a default DM message, as none was specified!"
    await user.send(message)

bot.run(os.environ["DISCORD_BOT_TOKEN"])