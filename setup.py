def getToken(chat_pass: str | None = None):
    """
    Gets a chat API token from the inputted chat_pass, which is obtained from running "chat_pass" in-game.

    Args:
        chat_pass (str | None, optional): The chat_pass to get the token from. If one is not given, prompts for it in the terminal. Defaults to None.
    """
    import requests
    import json
    from sys import path

    with open(f"{path[0]}/config.json") as f:
        config: dict = json.load(f)

    if not chat_pass:
        chat_pass = input("chat_pass password: ")

    if chat_pass != "":
        config["chat_token"] = json.loads(
            requests.post(
                url="https://www.hackmud.com/mobile/get_token.json",
                headers={"Content-Type": "application/json"},
                json={"pass": chat_pass},
            ).content
        )["chat_token"]

        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)


def getUsers():
    import requests
    import json
    from sys import path

    with open(f"{path[0]}/config.json") as f:
        config: dict = json.load(f)

    header: dict = config["header"]
    token: dict = config["chat_token"]

    config["users"] = json.loads(
        requests.post(
            url="https://www.hackmud.com/mobile/account_data.json",
            headers=header,
            json={"chat_token": token},
        ).content
    )["users"]

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)


if __name__ == "__main__":

    try:
        getToken()
        getUsers()
    except FileNotFoundError:
        import json
        from sys import path

        with open(f"{path[0]}/config.json", "w") as f:
            json.dump({"header": {"Content-Type": "application/json"}}, f)

        getToken()
        getUsers()
