from pypresence import Presence
from bs4 import BeautifulSoup
import requests
import asyncio
import json
import os
import nest_asyncio
import time

with open("config.json","r") as f:
    cfg = json.loads(f.read())

access_token = "ac77486334a745bd6034a4b6a8b5a35cf9a1a0c8cf92ba403821479ec46e525df5e65cf6d2f4401f8a36c"
id = cfg['config'][0]['discord_id']
user_id = cfg['config'][0]['vk_id']

_songname = ''
_artist = ''

nest_asyncio.apply()

def load_image(songname, artist):
    # url_img = 'https://yandex.kz/images/search?text=' + songname + " " + artist
    url_img = "https://www.google.com/search?q=" + songname + " " + artist + "&tbm=isch"
    resp = requests.get(url_img)
    soup = BeautifulSoup(resp.text, 'html.parser')
    img = soup.find_all('img')[1]['src']
    print(img)

    return img

def get_song():
    request_url = f"https://api.vk.com/method/users.get?access_token={ access_token }&user_ids={ str(user_id) }&v=5.131&fields=status"
    request = requests.get(request_url).json()

    try:
        songname = request['response'][0]['status_audio']['title']
        artist = request['response'][0]['status_audio']['artist']

        return songname, artist
    except:
        return "NULL", "NULL"

async def update_status(RPC):
    global _songname, _artist
    songname, artist = get_song()

    if songname == "NULL" and artist == "NULL":
        os.system('cls')
        print('Трек либо не включен, либо вы ввели неверный vk id')
        RPC.clear()

    elif songname != _songname and artist != _artist:
        _songname, _artist = songname, artist
        image = load_image(songname, artist)

        RPC.update(
            details=songname,
            state=artist, 
            large_image=image,
            small_image="https://upload.wikimedia.org/wikipedia/commons/2/27/VK_%D0%9C%D1%83%D0%B7%D1%8B%D0%BA%D0%B0.png"
        )
    time.sleep(5)
    # await asyncio.sleep(5)

# async def main():
def main():
    try:
        RPC = Presence(id)
        RPC.connect()
    except:
        print("Неверный discord id")
        input()
    while True:
        update_status(RPC)
        # await update_status(RPC)

if __name__ == "__main__":
    asyncio.run(main())