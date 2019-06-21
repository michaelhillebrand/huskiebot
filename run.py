import sys

from discord_bot import HuskieBot

if __name__ == '__main__':
    try:
        client = HuskieBot()
        key = open(sys.argv[1])
        client.run(key.read())
    except IndexError:
        print('Key not provided - Unable to start bot')
