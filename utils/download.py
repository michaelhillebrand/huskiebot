import logging
from tempfile import NamedTemporaryFile

import aiohttp
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
    logging.info(f'Downloading file from {url}')
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                file = NamedTemporaryFile()
                async for chunk, _ in r.content.iter_chunks():
                    file.write(chunk)
                file.flush()
                file.seek(0)
                logging.info(f'Downloaded file successfully from {url}')
                return file
            else:
                raise HTTPError(f'Received a non 200 status code: {r.status}')
