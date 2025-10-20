from sys import argv
from hackmudChatAPI import ChatAPI

chat = ChatAPI()

USER = argv[1]
TARGET = argv[2]

chat.tell(USER, TARGET, " ".join(argv[3:]))
