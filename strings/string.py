import yaml
import os
from string import Formatter
from config import LANG

RTL_LANGS = ["ckb", "he"]
PREFIX = "" if LANG not in RTL_LANGS else "\u200f"

class String:
    def __init__(self):
        self.languages = {}
        self.reload_strings()

    def get_string(self, string):
        try:
            return "{}{}".format(PREFIX, self.languages[LANG][string])
        except KeyError:
            # a keyerror happened, the english file must have it
            return self.languages["en"][string]

    def reload_strings(self):
        for filename in os.listdir(r"./strings"):
            if filename.endswith(".yml"):
                language_name = filename[:-4]
                self.languages[language_name] = yaml.safe_load(
                    open(r"./strings/" + filename, encoding="utf8"))


strings = String()
