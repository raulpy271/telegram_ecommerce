from .text_en import text_en
from .text_pt import text_pt

all_languages = {
    "English" : text_en,
    "Portuguese" : text_pt}


class Language():
    def __init__(self, dict_with_all_languages, default_language="en"):
        self.language = default_language
        self.suported_languages = dict_with_all_languages.keys()
        self.all_text = dict_with_all_languages


    def get_text(self, key):
        return self.all_text[self.language][key]


    def change_language(self, language):
        if language in self.suported_languages:
            self.language = language


TEXT = Language(all_languages, "pt")
get_text = TEXT.get_text


