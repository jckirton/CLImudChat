from sys import argv
from chat import ChatAPI

chat = ChatAPI()

USER = argv[1]
CHANNEL = argv[2]

chat.send(USER, CHANNEL, " ".join(argv[3:]))
