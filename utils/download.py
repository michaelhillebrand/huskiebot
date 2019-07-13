import logging
from tempfile import NamedTemporaryFile

import requests
from requests import HTTPError


async def download(url):
    """
    Downloads file from url

    Parameters
    ----------
    url : str

    Returns
    -------
    NamedTemporaryFile

    """
    logging.info('Downloading file from {}'.format(url))
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        file = NamedTemporaryFile()
        for chunk in r.iter_content(chunk_size=4096):
            if chunk:  # filter out keep-alive new chunks
                file.write(chunk)
            # await asyncio.sleep(0.01)  # allows HuskieBot to respond to other requests
        file.flush()
        file.seek(0)
        logging.info('Downloaded file successfully from {}'.format(url))
        return file
    else:
        raise HTTPError('Received a non 200 status code: {}'.format(r.status_code))
