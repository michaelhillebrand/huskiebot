# huskiebot

Huskie's bot

## Getting Started

1. `bin/setup.sh`: This installs necessary dependencies and sets up the project for use
2. Set `DISCORD_BOT_TOKEN` in your .env file, created during the setup script, to your discord bot token
3. `bin/run.sh`
4. To use the Salty Bet scraper, download the chrome driver for selenium here: https://sites.google.com/a/chromium.org/chromedriver/downloads. Place driver in the `/drivers` folder

### Commandline Arguments

```text
$ ./bin/run.sh --help # Or, if you have the virtual env enabled: `python run.py --help`
usage: run.py [-h] [--disable-cogs DISABLE_COGS]

Run the HuskieBot

optional arguments:
  -h, --help            show this help message and exit
  --disable-cogs DISABLE_COGS
                        A list of cog module names to not enable on bot startup. Comma separted list, no spaces
```
