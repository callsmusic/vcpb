import yaml
import os
from string import Formatter
from config import LANG, CREDIT


class String:
    def __init__(self):
        self.languages = {}
        self.reload_strings()

    def get_string(self, string, c=False):
        credit = "\n\nMade with ❤️ by @su_Bots." if CREDIT and c else ""

        try:
            return self.languages[LANG][string] + credit
        except KeyError:
            # a keyerror happened, the english file must have it
            return self.languages["en"][string] + credit

    def reload_strings(self):
        for filename in os.listdir(r"./strings"):
            if filename.endswith(".yaml"):
                language_name = filename[:-5]
                self.languages[language_name] = yaml.safe_load(
                    open(r"./strings/" + filename, encoding="utf8"))


strings = String()
