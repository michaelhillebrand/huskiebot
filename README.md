# huskiebot

Huskie's bot

## Getting Started

1. `bin/setup.sh`: This installs necessary dependencies and sets up the project for use
2. Set `DISCORD_BOT_TOKEN` in your .env file, created during the setup script, to your discord bot token
3. `bin/run.sh`

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

## Contributing

See the [Contributing](./CONTRIBUTING.md) guide for info on how to start contributing to the project.
