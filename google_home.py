import pychromecast
from gtts import gTTS
from slugify import slugify
from pathlib import Path
from urllib.parse import urlparse
import socket

chromecast_name = "Living Room speaker"

dirname = Path(__file__).parent.absolute()
Path(dirname, 'static', 'cache').mkdir(parents=True, exist_ok=True)

chromecasts = pychromecast.get_chromecasts()
cast = next(cc for cc in chromecasts[0] if cc.device.friendly_name == chromecast_name)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def play_tts(text, lang='en', slow=False):
    tts = gTTS(text=text, lang=lang, slow=slow)
    filename = slugify(text+"-"+lang+"-"+str(slow)) + ".mp3"
    tts_file = Path(dirname, 'static', 'cache', filename)
    if not tts_file.is_file():
        tts.save(tts_file)

    mp3_url = "http://" + get_ip() + ':5000/static/cache/' + filename 
    play_mp3(mp3_url)


def play_mp3(mp3_url):
    cast.wait()
    mc = cast.media_controller
    mc.play_media(mp3_url, 'audio/mp3')
    mc.block_until_active()