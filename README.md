# huskiebot
Huskie's bot

## Getting Started
1. `sudo apt-get install python3-venv`
2. `python3 -m venv venv`
3. `source venv/bin/activate`
4. `git clone https://github.com/michaelhillebrand/huskiebot.git app`
5. `git checkout HuskieBot`
5. `pip install -r requirements.txt`
6. `cp .template.env .env`
7. Set `DISCORD_BOT_TOKEN` to your bot token
8. `python3 run.py`

## Branch Structure
feature/{branch-name} - For new features<br />
fix/{branch-name} - For bug fixes

## Documentation Format
```
"""
Summary line.

Extended description of function.

Parameters
----------
arg1 : int
    Description of arg1
arg2 : str
    Description of arg2

Returns
-------
int
    Description of return value

"""
```
