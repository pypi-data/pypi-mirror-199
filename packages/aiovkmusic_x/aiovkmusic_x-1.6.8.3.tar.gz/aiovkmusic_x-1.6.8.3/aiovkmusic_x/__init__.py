# -*- coding: utf-8 -*-
"""
aiovkmusic-x
"""
__version__ = "1.6.8.1"

from sys import stdout
from warnings import filterwarnings

from loguru import logger

from .model import Track, Playlist
from .music import Music
from .session import VKSession

filterwarnings("ignore", category=UserWarning, module='bs4')
logger.remove()
logger.add(
    sink=stdout,
    format="{level} {time:MMM DD HH:mm:ss.SSS}: {message}",
    enqueue=True
)
