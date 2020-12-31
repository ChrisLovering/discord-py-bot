import json
import aiohttp
import discord
import pickle
from pathlib import Path
from discord.ext import commands
from urllib.parse import urlparse
from google_home import GoogleHome


dirname = Path(__file__).parent.absolute()
pickle_file = Path(dirname, 'user_langs.pkl')
if pickle_file.is_file():
    with open(pickle_file, 'rb') as f:
        user_langs = pickle.load(f)
else:
    user_langs = {}    

bot = commands.Bot(command_prefix="!", help_command=None)
debug = False
home_obj = GoogleHome()

async def check_server():
    if await home_obj.test_server():
        return True
    else:
        return 'The text to speech server is currently offline. Cancelling your request.'

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

@bot.listen('on_message')
async def on_message(message):
    if debug and message.author != bot.user:
        print(f"{message.author} sent '{message.content}' in {message.channel}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

# Top level command, this is so that this bot doesn't overlap with others that use !
@bot.group()
async def alfred(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Invalid alfred command passed...")

# Gets the current url(s) of the ngrok tunnel
@alfred.command()
async def ip(ctx):
    ip = await get_ngrok_ip()
    await ctx.send(ip)

@alfred.group()
async def lang(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Only subcommands are get, set or list")

@lang.command(name='list')
async def lang_list(ctx):
    home_obj.languages = home_obj.languages
    languages_list = [f'{code}: {lang}' for code, lang in home_obj.languages.items()]
    await ctx.author.send('\n'.join(['Supported languages are:']+languages_list))
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send("DM'd you the list as its quite long")

@lang.command(name='get')
async def lang_get(ctx):
    lang = user_langs.get(ctx.author.id, "en")
    await ctx.send(f'Your current language is {lang}-{home_obj.languages[lang]}')

@lang.command(name='set')
async def lang_set(ctx, lang):
    if lang in home_obj.languages:
        user_langs[ctx.author.id] = lang
        message = f'Set {ctx.author}s language to {lang}-{home_obj.languages[lang]}'
    else:
        message = f'Language {lang} could not be found. Do !alfred lang list for a list of supported languages'
    await ctx.send(message)

@alfred.group()
async def say(ctx, *, message='test'):
    if ctx.invoked_subcommand is None:
        res = await check_server()
        if res != True:
            await ctx.send(res)
            return
        lang = user_langs.get(ctx.author.id, "en")
        home_obj.play_tts(message, lang=lang)
        await ctx.send(f'Now playing {message} in {home_obj.languages[lang]}')

@say.command(name='slow')
async def say_slow(ctx, *, message='test'):
    res = await check_server()
    if res != True:
        await ctx.send(res)
        return
    lang = user_langs.get(ctx.author.id, "en")
    home_obj.play_tts(message, lang=lang, slow=True)
    await ctx.send(f'Now playing {message} slowly, in {home_obj.languages[lang]}')

# Sends a dm to the user
@alfred.group()
async def dm(ctx, user: discord.User, *, message=None):
    if ctx.invoked_subcommand is None:
        message = message or "This is a default DM message, as none was specified!"
        await user.send(message)

@dm.command(name='ip')
async def dm_ip(_, user: discord.User, *, message=None):
    message = ' '.join([await get_ngrok_ip(), message])
    await user.send(message)

with open('creds.json') as f:
    data = json.load(f)

bot.run(data['api_token'])
with open(pickle_file, 'wb') as f:
    pickle.dump(user_langs, f)