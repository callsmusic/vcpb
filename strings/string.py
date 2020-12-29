import yaml
import os
from string import Formatter
from config import LANG


class String:
    def __init__(self):
        self.languages = {}
        self.reload_strings()

    def get_string(self, string):
        try:
            return self.languages[LANG][string]
        except KeyError:
            # a keyerror happened, the english file must have it
            return self.languages["en"][string]

    def reload_strings(self):
        for filename in os.listdir(r"./strings"):
            if filename.endswith(".yaml"):
                language_name = filename[:-5]
                self.languages[language_name] = yaml.safe_load(
                    open(r"./strings/" + filename, encoding="utf8"))


strings = String()
