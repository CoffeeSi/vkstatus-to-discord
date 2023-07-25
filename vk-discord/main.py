from pypresence import Presence
from bs4 import BeautifulSoup
import requests
import aiohttp
import asyncio
import json
import os
import nest_asyncio

#применение nest_asyncio
nest_asyncio.apply()

#импорт конфига
with open("config.json","r") as f:
    cfg = json.loads(f.read())

class Music:
    """Require config file config.json"""
    def __init__(self, config):
        self.cfg = config
        self.id = self.cfg['config'][0]['discord_id']               #извлечение Discord Applcation ID
        self.user_id = self.cfg['config'][0]['vk_id']               #извлечение ID профиля ВК
        self.access_token = self.cfg['config'][0]['vk_api_token']   #извлечение токена VK API
        self.search_engine = self.cfg['config'][0]['search']        #извлечение поискового сервиса
        self._songname = None
        self._artist = None

        #проверка Discord Applcation ID
        try:
            self.RPC = Presence(self.id)
            self.RPC.connect()
        except:
            print("Неверный DiscordID")
            input()
            raise IndexError

    #асинхронная функция поиска обложки трека из Интернета
    async def search_image(self, songname, artist):
        if self.search_engine == 'google':
            query = songname + " " + artist
            url_img = "https://www.google.com/search?q=" + query + "&tbm=isch"
            image = await self.load_image(url_img)
        elif self.search_engine == 'yandex':
            query = songname + " " + artist
            url_img = 'https://yandex.kz/images/search?text=' + query
            image = await self.load_image(url_img)
        elif self.search_engine == 'duck':
            query = songname + " " + artist
            url_img = 'https://duckduckgo.com/?q=' + query + '&iax=images&ia=images'
            image = await self.load_image(url_img)
        else:
            #если поисковый сервис не выбран, то обложка трека не выводится
            image = None

        # async with aiohttp.ClientSession() as session:
        #     async with session.get(url_img) as response:
        #         html = await response.text()
        #         soup = BeautifulSoup(html, 'html.parser')
        #         print(soup.text)
        #         image = soup.find_all('img')[1]['src']
        #         await session.close()

        return image
    
    #асинхронная функция загрузки изображения
    async def load_image(self, url):
        resp = requests.get(url)
        html = resp.text
        soup = BeautifulSoup(html, 'html.parser')
        image = soup.find_all('img')[1]['src']
        return image
    
    #асинхронная функция получения трека, играющего в данный момент в ВК
    async def get_song_token(self):
        #шаблон запроса VK API
        request = f"https://api.vk.com/method/users.get" \
                  f"?access_token={ self.access_token }&" \
                  f"user_ids={ str(self.user_id) }&v=5.131&fields=status"
        #подключение aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(request) as response:
                html = await response.json()
                #проверка на воспроизведение трека в ВК
                try:
                    status_audio = html['response'][0]['status_audio']
                    songname = status_audio['title']
                    artist = status_audio['artist']
                except:
                    songname = "NULL"
                    artist = "NULL"
        
        #вывод название трека и артиста
        return songname, artist

    #асинхронная функция обновления статуса Discord
    async def update_status(self):
        #получение названия трека и артиста
        songname, artist = await self.get_song_token()
        #если трек не включен, то выводит предупреждение
        if songname == "NULL" and artist == "NULL":
            os.system('cls')
            print('Трек либо не включен, либо вы ввели неверный vk id')
            self.RPC.clear()
        #еслли трек работает, то создается задача поиска обложки и её загрузка 
        elif songname != self._songname and artist != self._artist:
            self._songname, self._artist = songname, artist
            task = asyncio.create_task(self.search_image(songname, artist))
            image = await task

            #вывод названия трека в консоль(можно выключить, удалив строку ниже)
            print(songname," - ", artist)

            #обновление самого статуса
            self.RPC.update(
                details=songname,
                state=artist, 
                large_image=image,
                small_image="https://upload.wikimedia.org/wikipedia/commons/2/27/VK_%D0%9C%D1%83%D0%B7%D1%8B%D0%BA%D0%B0.png"
            )
        #задержка 2 секунды
        await asyncio.sleep(2)


async def main():
    music = Music(cfg)
    #бесконечный цикл обновления статуса Discord
    while True:
        await music.update_status()

if __name__ == "__main__":
    #запуск асихронной функции main
    asyncio.run(main())