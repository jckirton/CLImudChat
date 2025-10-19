import json
import os
from sys import path, argv
from chat import ChatAPI
from typing import TypedDict, NotRequired
import time


class ChatMessage(TypedDict):
    id: str
    t: float
    from_user: str
    msg: NotRequired[str]
    channel: NotRequired[str]
    is_leave: NotRequired[bool]
    is_join: NotRequired[bool]
    to_user: NotRequired[str]


def flush(chatsCache, allChats):
    with open(chatsCache, "w") as f:
        json.dump(allChats, f, indent=4)


def fetch(
    chat: ChatAPI,
    allChats: dict[str, list[dict]],
    seconds: int | float = 10,
    importData: dict[str, list[dict]] | None = None,
):
    fetched: dict[str, list[dict]]

    if importData:
        fetched = importData
    else:
        fetched = chat.read(after=seconds)

    newChats: dict[str, list[dict]] = {}.copy()
    for user in fetched:
        fetched[user].sort(key=lambda message: message["t"])
        newChats[user] = []
        if user not in allChats:
            allChats[user] = []
        for msg in fetched[user]:
            if msg not in allChats[user]:
                allChats[user].append(msg)
                newChats[user].append(msg)

    return {"fetched": fetched, "new": newChats}


def renderMessage(message: ChatMessage, user):
    is_join = message.get("is_join", False)
    is_leave = message.get("is_leave", False)
    msg = message.get("msg", None)
    channel = message.get("channel", None)
    to_user = message.get("to_user", None)

    import termcolor
    import regex

    COLOR_CHARS = {
        "0": (int("CA", base=16), int("CA", base=16), int("CA", base=16)),
        "1": (int("FF", base=16), int("FF", base=16), int("FF", base=16)),
        "2": (int("1E", base=16), int("FF", base=16), int("00", base=16)),
        "3": (int("00", base=16), int("70", base=16), int("DD", base=16)),
        "4": (int("B0", base=16), int("35", base=16), int("EE", base=16)),
        "5": (int("FF", base=16), int("80", base=16), int("00", base=16)),
        "6": (int("FF", base=16), int("80", base=16), int("00", base=16)),
        "7": (int("FF", base=16), int("80", base=16), int("00", base=16)),
        "8": (int("FF", base=16), int("80", base=16), int("00", base=16)),
        "9": (int("FF", base=16), int("80", base=16), int("00", base=16)),
        "a": (int("00", base=16), int("00", base=16), int("00", base=16)),
        "b": (int("3F", base=16), int("3F", base=16), int("3F", base=16)),
        "c": (int("67", base=16), int("67", base=16), int("67", base=16)),
        "d": (int("7D", base=16), int("00", base=16), int("00", base=16)),
        "e": (int("8E", base=16), int("34", base=16), int("34", base=16)),
        "f": (int("A3", base=16), int("4F", base=16), int("00", base=16)),
        "g": (int("72", base=16), int("54", base=16), int("37", base=16)),
        "h": (int("A8", base=16), int("86", base=16), int("00", base=16)),
        "i": (int("B2", base=16), int("93", base=16), int("4A", base=16)),
        "j": (int("93", base=16), int("95", base=16), int("00", base=16)),
        "k": (int("49", base=16), int("52", base=16), int("25", base=16)),
        "l": (int("29", base=16), int("94", base=16), int("00", base=16)),
        "m": (int("23", base=16), int("38", base=16), int("1B", base=16)),
        "n": (int("00", base=16), int("53", base=16), int("5B", base=16)),
        "o": (int("32", base=16), int("4A", base=16), int("4C", base=16)),
        "p": (int("00", base=16), int("73", base=16), int("A6", base=16)),
        "q": (int("38", base=16), int("5A", base=16), int("6C", base=16)),
        "r": (int("01", base=16), int("00", base=16), int("67", base=16)),
        "s": (int("50", base=16), int("7A", base=16), int("A1", base=16)),
        "t": (int("60", base=16), int("1C", base=16), int("81", base=16)),
        "u": (int("43", base=16), int("31", base=16), int("4C", base=16)),
        "v": (int("8C", base=16), int("00", base=16), int("69", base=16)),
        "w": (int("97", base=16), int("39", base=16), int("84", base=16)),
        "x": (int("88", base=16), int("00", base=16), int("24", base=16)),
        "y": (int("76", base=16), int("2E", base=16), int("4A", base=16)),
        "z": (int("10", base=16), int("12", base=16), int("15", base=16)),
        "A": (int("FF", base=16), int("FF", base=16), int("FF", base=16)),
        "B": (int("CA", base=16), int("CA", base=16), int("CA", base=16)),
        "C": (int("9B", base=16), int("9B", base=16), int("9B", base=16)),
        "D": (int("FF", base=16), int("00", base=16), int("00", base=16)),
        "E": (int("FF", base=16), int("83", base=16), int("83", base=16)),
        "F": (int("FF", base=16), int("80", base=16), int("00", base=16)),
        "G": (int("F3", base=16), int("AA", base=16), int("6F", base=16)),
        "H": (int("FB", base=16), int("C8", base=16), int("03", base=16)),
        "I": (int("FF", base=16), int("D8", base=16), int("63", base=16)),
        "J": (int("FF", base=16), int("F4", base=16), int("04", base=16)),
        "K": (int("F3", base=16), int("F9", base=16), int("98", base=16)),
        "L": (int("1E", base=16), int("FF", base=16), int("00", base=16)),
        "M": (int("B3", base=16), int("FF", base=16), int("9B", base=16)),
        "N": (int("00", base=16), int("FF", base=16), int("FF", base=16)),
        "O": (int("8F", base=16), int("E6", base=16), int("FF", base=16)),
        "P": (int("00", base=16), int("70", base=16), int("DD", base=16)),
        "Q": (int("A4", base=16), int("E3", base=16), int("FF", base=16)),
        "R": (int("00", base=16), int("00", base=16), int("FF", base=16)),
        "S": (int("7A", base=16), int("B2", base=16), int("F4", base=16)),
        "T": (int("B0", base=16), int("35", base=16), int("EE", base=16)),
        "U": (int("E6", base=16), int("C4", base=16), int("FF", base=16)),
        "V": (int("FF", base=16), int("00", base=16), int("EC", base=16)),
        "W": (int("FF", base=16), int("96", base=16), int("E0", base=16)),
        "X": (int("FF", base=16), int("00", base=16), int("70", base=16)),
        "Y": (int("FF", base=16), int("6A", base=16), int("98", base=16)),
        "Z": (int("0C", base=16), int("11", base=16), int("2B", base=16)),
    }

    regexColor = r"`([a-zA-Z0-9])([^`]*)`"

    content: str

    if msg:
        content = msg
    elif is_join:
        content = "user joined channel"
    elif is_leave:
        content = "user left channel"

    content = termcolor.colored(content, COLOR_CHARS["S"])

    coloredText = regex.findall(regexColor, content)

    for sect in coloredText:
        content = content.replace(
            f"`{sect[0]}{sect[1]}`",
            termcolor.colored(sect[1], COLOR_CHARS[sect[0]]) + "[38;2;122;178;244m",
        )

    timestr = termcolor.colored(
        time.strftime("%Y-%m-%d %H%M", time.localtime(message["t"])), COLOR_CHARS["C"]
    )

    sender = message["from_user"]
    border = termcolor.colored(":::", COLOR_CHARS["c"])
    body = border + content + border

    if is_join or is_leave:
        channel = termcolor.colored(channel, COLOR_CHARS["N"])
    elif not channel and to_user:
        if sender != user:
            channel = termcolor.colored("from", COLOR_CHARS["N"])
        elif to_user == sender:
            channel = termcolor.colored("to self", COLOR_CHARS["N"])
        else:
            channel = termcolor.colored("to", COLOR_CHARS["N"])
            sender = to_user
    else:
        channel = termcolor.colored(channel, COLOR_CHARS["V"])

    return f"{timestr} {channel} {sender} {body}"


def chatMonitor(
    user: str,
    /,
    filter_sender: str | list | None = None,
    filter_channel: str | list | None = None,
    chat: ChatAPI = ChatAPI(),
    cacheDir=f"{path[0]}/cache",
    allChats: dict[str, list[dict]] | None = None,
    live: bool = True,
):
    chatsCache = f"{cacheDir}/chatHistory.json"

    if allChats is None:
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

    fetch(chat, allChats, 600)
    flush(chatsCache, allChats)

    # print(filter_sender, filter_channel)

    if filter_sender == "" or filter_sender == "none" or filter_sender == ["none"]:
        filter_sender = None
    if filter_channel == "" or filter_channel == "none" or filter_channel == ["none"]:
        filter_channel = None

    # print(filter_sender, filter_channel)

    if type(filter_sender) is str:
        filter_sender = [filter_sender]
    if type(filter_channel) is str:
        filter_channel = [filter_channel]

    # print(filter_sender, filter_channel)

    if filter_channel:
        for channel in filter_channel:
            if channel == "tells":
                filter_channel[filter_channel.index(channel)] = "tell"

    # print(filter_sender, filter_channel)

    if filter_sender and filter_channel:
        for message in allChats[user]:
            if (
                message["from_user"] in filter_sender
                and message.get("channel", "tell") in filter_channel
            ):
                print(renderMessage(message, user), flush=True)
            else:
                pass

        try:
            while live:
                newChats = fetch(chat, allChats, 120)["new"]
                flush(chatsCache, allChats)
                if len(newChats[user]) > 0:
                    for message in newChats[user]:
                        if (
                            message["from_user"] in filter_sender
                            and message.get("channel", "tell") in filter_channel
                        ):
                            print(renderMessage(message, user), flush=True)
                        else:
                            pass
                time.sleep(2)
        except KeyboardInterrupt:
            flush(chatsCache, allChats)

    elif filter_sender:
        for message in allChats[user]:
            if message["from_user"] in filter_sender:
                print(renderMessage(message, user), flush=True)
            else:
                pass

        try:
            while live:
                newChats = fetch(chat, allChats, 120)["new"]
                flush(chatsCache, allChats)
                if len(newChats[user]) > 0:
                    for message in newChats[user]:
                        if message["from_user"] in filter_sender:
                            print(renderMessage(message, user), flush=True)
                        else:
                            pass
                time.sleep(2)
        except KeyboardInterrupt:
            flush(chatsCache, allChats)

    elif filter_channel:
        for message in allChats[user]:
            if message.get("channel", "tell") in filter_channel:
                print(renderMessage(message, user), flush=True)
            else:
                pass

        try:
            while live:
                newChats = fetch(chat, allChats, 120)["new"]
                flush(chatsCache, allChats)
                if len(newChats[user]) > 0:
                    for message in newChats[user]:
                        if message.get("channel", "tell") in filter_channel:
                            print(renderMessage(message, user), flush=True)
                        else:
                            pass
                time.sleep(2)
        except KeyboardInterrupt:
            pass
            # flush(chatsCache, allChats)
    else:
        for message in allChats[user]:
            print(renderMessage(message, user), flush=True)

        try:
            while live:
                newChats = fetch(chat, allChats, 120)["new"]
                flush(chatsCache, allChats)
                if len(newChats[user]) > 0:
                    for message in newChats[user]:
                        print(renderMessage(message, user), flush=True)
                time.sleep(2)
        except KeyboardInterrupt:
            flush(chatsCache, allChats)


if __name__ == "__main__":
    if len(argv) > 1:
        user = argv[1]
    else:
        user = input("Input user: ")

    if len(argv) > 2:
        filterSender = argv[2]
    elif len(argv) < 2:
        filterSender = input("Filter message sender? ")
    else:
        filterSender = None

    if filterSender:
        filterSender = "".join(filterSender.split(" ")).split(",")

    if len(argv) > 3:
        filterChannel = argv[3]
    elif len(argv) < 2:
        filterChannel = input("Filter channel? ")
    else:
        filterChannel = None

    if filterChannel:
        filterChannel = "".join(filterChannel.split(" ")).split(",")

    # print(argv, user, filterSender, filterChannel)

    chatMonitor(user, filterSender, filterChannel)
