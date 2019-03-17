import sys

from discord_bot import HuskieBot

if __name__ == '__main__':
    try:
        client = HuskieBot()
        client.run('NTU1NTEyNDY2OTM1OTA2MzA0.D2sqLA.8tSvTx9EFGw2IngO_y4byS49SQY')
        # client.run(sys.argv[1])
    except IndexError:
        print('Key not provided - Unable to start bot')
