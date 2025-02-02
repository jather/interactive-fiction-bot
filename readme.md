# interactive fiction bot

## What it is
A discord bot made with discord.py that allows you to play glulx games. You can create savefiles per-user per-game, and multiple games can be run at once in different channels. 

## Functionality
- [ ] "/add {game}" download new games (must be bot owner)
- [x] "/list" list available games
    - [ ] make it look better and show more information, multiple pages. be able to look at information for individual games.
- [x] "/start {game}" create a session for a game in the channel
- [x] "/stop" end the current session.

Use in-game commands for saving and restoring. 

## Instructions to run
You need to compile git (the interpreter for the glulx format, not the version control system) against RemGlk and put the executable in the top level directory.

You also need to create a discord bot and get the token. Once you've done all that:

### Install dependencies
```
$ python -m venv .venv
$ pip install -r requirements.txt
```
### Create .env file
contains:
```
api key
```
### 
run the bot