import logging
import pickle
from typing import Any

from cogs import BASE_PATH
from personalities.base import Personality


class Settings(object):
    CURRENT_PERSONALITY = 'current_personality'
    LAST_PERSONALITY_CHANGE = 'last_personality_change'
    DANK_LAST_FETCH = 'dank_last_fetch'

    __PATH = f'{BASE_PATH}/settings.pkl'
    __DEFAULT = {
        CURRENT_PERSONALITY: Personality,
        LAST_PERSONALITY_CHANGE: None,
        DANK_LAST_FETCH: None
    }

    data = __DEFAULT

    def __init__(self):
        self.load()

    def _save(self) -> None:
        """Saves settings to disk."""
        logging.debug('Saving Settings')
        with open(self.__PATH, 'wb') as f:
            pickle.dump(self.data, f)

    def load(self) -> None:
        """Loads settings from disk into memory."""
        logging.debug('Loading Settings')
        try:
            with open(self.__PATH, 'rb') as f:
                self.data.update(pickle.load(f))
        except Exception as e:
            logging.warning(e)
            self._save()

    def get(self, key: str, default: Any = None) -> Any:
        """
        Gets current value for key in settings.

        Parameters
        ----------
        key: str
        default: Any (optional)

        Returns
        -------
        Any

        """
        logging.debug(f'Getting setting for {key}')
        return self.data.get(key, default)

    def save(self) -> None:
        """Saves settings to disk."""
        logging.debug('Manual saving')
        self._save()

    def set(self, key: str, value: Any) -> None:
        """
        Updates setting with given value.

        Parameters
        ----------
        key: str
        value: Any

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
        """
        Updates settings with given data.

        Given a dict, the function will merge the settings with each key-value pair.

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
