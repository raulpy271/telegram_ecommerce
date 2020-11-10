from .text_en import text_en
from .text_pt import text_pt
from ..utils.consts import default_language
from ..utils.utils import get_lang


all_languages = {
    "en" : text_en,
    "pt" : text_pt}


class Language():
    def __init__(self, dict_with_all_languages, language):
        self.default_language = language
        self.suported_languages = dict_with_all_languages.keys()
        self.all_text = dict_with_all_languages


    def get_text(self, key, context=None):
        language = get_lang(context)
        if language in self.suported_languages:
            return self.all_text[language][key]
        else:
            return self.all_text[self.default_language][key]


TEXT = Language(all_languages, default_language)
get_text = TEXT.get_text


