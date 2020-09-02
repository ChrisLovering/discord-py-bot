import os
import aiohttp
import discord
from discord.ext import commands
from urllib.parse import urlparse

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.group()
async def alfred(ctx):
    print(f'{ctx.author} sent {ctx.message.content} in {ctx.channel}')
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid alfred command passed...')

# Gets the current url(s) of the ngrok tunnel
@alfred.command()
async def ip(ctx):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('http://localhost:4040/api/tunnels') as r:
                js = await r.json()
                tunnels = [urlparse(tunnel["public_url"]).netloc for tunnel in js["tunnels"]]
                await ctx.send(*tunnels)
        except aiohttp.ClientConnectorError as e:
            await ctx.send(f'Connection error (This usually means the server isn\'t running): {str(e)}')

bot.run(os.environ["DISCORD_BOT_TOKEN"])