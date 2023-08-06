# aiovkmusic_x

### Описание

> *Асинхронная python библиотека для работы с VK музыкой, является форком aiovkmusic.*
___


* #### 
  Установка [aiovkmusic-x](https://pypi.org/project/aiovkmusic-x/) средствами [PyPi](https://pypi.org/): `pip install aiovkmusic-x`
* #### Для работы необходим [ffmpeg](https://ffmpeg.org/download.html).

___
Примеры использования:

```python
import asyncio
from aiovkmusic_x import Music, VKSession, Track, Playlist


async def main():
    # Создание сессии.
    # Двухэтапная аутентификация не поддерживается
    session = VKSession(
        login='<номер_телефона/электронная_почта>',
        password='<пароль_от_вконтакте>',
        session_file_path='session.json'
    )

    # self позволяет взять айди из сессии
    music = Music(user='self', session=session)

    tracks = music.search("Geoxor", official=True)
    for track in tracks:
        await music.download(track)



asyncio.run(main())
```

Используемые представления данных:

```python
class Playlist:
    id: int
    owner_id: int
    title: str
    plays: int
    url: str
    access_hash: str


class Track:
    id: int
    owner_id: int
    cover_url: str
    url: str
    artist: str
    title: str
    duration: int
    path: str
    fullname: str
```

___
