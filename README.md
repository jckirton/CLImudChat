# hackmud Python CLI Chat Client

## Setup

First, as per usual: clone this repository to wherever you want to work. *You want to work in this folder, with the contents of the repository.*

If you run `setup.sh` and have python installed, it should:

- Create a python venv called `.venv` in the workspace directory
- Install `requests` into the venv
- Run `setup.py` (input of `chat_pass` needed)
- Delete itself.

This should set everything up, including your chat token and user info, which will be stored in `config.json`.

When you need to update these, just run `setup.py` again.

## Usage

In VSCode make two shell instances, and put them side-by-side.

Then, in both shells, source `aliases.txt`

Then, in one shell, enter `monitor`; this shell is going to be where your chats are displayed.

In the other shell, you can use the `send` and `tell` aliases. Be careful with some characters in the message you send, you will have to escape some thing.

Syntax is `<send/tell> USER TARGET MSG`
