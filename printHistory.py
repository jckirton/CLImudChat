if __name__ == "__main__":
    from sys import argv
    from viewChats import chatMonitor

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

    chatMonitor(user, filterSender, filterChannel, live=False, write=False)
