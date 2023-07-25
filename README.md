# VK music to Discord Status

## Настройка

Для запуска скрипта нужно настроить **"config.json"**, находящийся в папке **"vk-discord"**

- **discord_id** - ID приложения Discord, которое можно создать по [ссылке](https://discord.com/developers/applications).
P.S. В настройках Discord'a должен быть включен "Режим разработчика".

- **vk_id** - ID вашей страницы ВК, которое состоит из цифр, например, "7548438757". 
Можно узнать [здесь](https://id.vk.com/account/#/personal).

- **vk_api_token** - Ключ доступа API вашей группы ВК. Можно узнать в Настройках сообщества - Настройки - Работа с API.

- **search** - Поисковый сервис, в котором скрипт будет брать обложку для трека. По умолчанию: "google".
Варианты: "google", "yandex", "duck".

## Запуск

Запуск осуществляется командой

```cd vk-discord
python vk-discord/main.py
```
или запустить **"main.py"** 


## License

MIT