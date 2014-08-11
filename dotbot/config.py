import json

class ConfigReader(object):
    def __init__(self, config_file_path):
        self._config = self._read(config_file_path)

    def _read(self, config_file_path):
        try:
            with open(config_file_path) as fin:
                data = json.load(fin)
            return data
        except Exception as tExcept:
            print tExcept
            raise ReadingError('Could not read config file at {}'.format(config_file_path))

    def get_config(self):
        return self._config

class ReadingError(Exception):
    pass
