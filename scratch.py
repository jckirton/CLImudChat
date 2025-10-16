import viewChats
import json
import os
from sys import path, argv
from chat import ChatAPI
from typing import TypedDict, NotRequired
import time

chat = ChatAPI()

cacheDir = f"{path[0]}/cache"
chatsCache = f"{cacheDir}/chatHistory.json"

try:
    os.mkdir(cacheDir)
except FileExistsError:
    pass
try:
    with open(chatsCache) as f:
        allChats = json.load(f)
        for username in allChats:
            allChats[username].sort(key=lambda message: message["t"])
except FileNotFoundError:
    allChats = {}
    for username in chat.users:
        allChats[username] = []

with open("chatHistory.json") as f:
    viewChats.fetch(chat, allChats, importData=json.load(f))
    viewChats.flush(chatsCache, allChats)
