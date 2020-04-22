import datetime
import logging
import pickle

from cogs import BASE_PATH
from personalities.base import Personality


class Settings(object):

    path = f'{BASE_PATH}/settings.pkl'

    default = {
        'current_personality': Personality,
        'last_personality_change': datetime.datetime.utcnow(),
        'dank_last_fetch': None
    }

    data = default

    def __init__(self):
        self.load()

    def _save(self) -> None:
        """Saves settings to disk."""
        logging.debug('Saving Settings')
        with open(self.path, 'wb') as f:
            pickle.dump(self.data, f)

    def load(self) -> None:
        """Loads settings from disk into memory."""
        logging.debug('Loading Settings')
        try:
            with open(self.path, 'rb') as f:
                self.data = pickle.load(f)
        except Exception as e:
            logging.warning(e)
            self._save()

    def get(self, key: str):
        """Gets current value for key in settings.

        Parameters
        ----------
        key: str

        Returns
        -------
        None
        """
        logging.debug(f'Getting setting for {key}')
        return self.data[key]  # Intentional error is thrown

    def save(self) -> None:
        """Saves settings to disk."""
        logging.debug('Manual saving')
        return self._save()

    def set(self, key: str, value) -> None:
        """Updates setting with given value.

        Parameters
        ----------
        key: str
        value: any

        Returns
        -------
        None
        """
        logging.debug(f'Updating setting: {key} to {value}')
        # checks to see if rouge setting key passed
        if key not in self.data.keys():
            raise KeyError('Invalid settings passed')

        old_setting = self.data[key]

        try:
            self.data[key] = value
            self._save()
        except Exception as e:
            # catch values that can't be pickled
            self.data = old_setting
            raise e

    def update(self, data: dict) -> None:
        """Updates settings with given data.

        Parameters
        ----------
        data: dict

        Returns
        -------
        None
        """
        logging.debug('Updating settings')
        # checks to see if rouge settings value passed
        if not set(data.keys()) <= set(self.data.keys()):
            raise KeyError('Invalid settings passed')

        old_settings = self.data

        try:
            self.data.update(data)
            self._save()
        except Exception as e:
            # catch values that can't be pickled
            self.data = old_settings
            raise e
