#TODO implement https://github.com/MagicStack/asyncpg for caching files

import pychromecast
from gtts import gTTS, lang
from slugify import slugify
from pathlib import Path
import socket
import aiohttp

class GoogleHome():
    
    def __init__(self):
        self.chromecast_name = "Living Room speaker"
        self.languages = self.get_langs()
        self.dirname = Path(__file__).parent.absolute()
        Path(self.dirname, 'static', 'cache').mkdir(parents=True, exist_ok=True)

        self.chromecasts = pychromecast.get_chromecasts()
        self.cast = next(cc for cc in self.chromecasts[0] if cc.device.friendly_name == self.chromecast_name)

    @staticmethod
    def get_ip():
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            try:
                s.connect(('10.255.255.255', 1))
                IP = s.getsockname()[0]
            except Exception:
                IP = '127.0.0.1'
        return IP

    @classmethod
    async def test_server(cls):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f'http://{cls.get_ip()}:5000/test/') as r:
                    js = await r.json()
                    if js.get('detail', None):
                        return True
                    return False
            except aiohttp.ClientConnectorError:
                return False
        
    @staticmethod
    def get_langs():
        return lang.tts_langs()

    def play_tts(self, text, lang='en', slow=False):
        tts = gTTS(text=text, lang=lang, slow=slow)
        filename = slugify(text+"-"+lang+"-"+str(slow)) + ".mp3"
        tts_file = Path(self.dirname, 'static', 'cache', filename)
        if not tts_file.is_file():
            tts.save(tts_file)

        mp3_url = "http://" + self.get_ip() + ':5000/static/cache/' + filename 
        self.play_mp3(mp3_url)


    def play_mp3(self, mp3_url):
        self.cast.wait()
        mc = self.cast.media_controller
        mc.play_media(mp3_url, 'audio/mp3')
        mc.block_until_active()

if __name__ == "__main__":
    print(GoogleHome.get_langs())