import os
import aiohttp
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.group()
async def alfred(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid chris command passed...')

@alfred.command()
async def ip(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:4040/api/tunnels') as r:
            if r.status == 200:
                js = await r.json()
                tunnels = [f'{tunnel["name"]}: {tunnel["public_url"]}'for tunnel in js["tunnels"]]
                await ctx.send(tunnels)

bot.run(os.environ["DISCORD_BOT_TOKEN"])