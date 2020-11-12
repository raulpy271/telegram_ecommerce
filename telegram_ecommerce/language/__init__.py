from .text_en import text_en
from .text_pt import text_pt
from ..utils.consts import default_language


all_languages = {
    "en" : text_en,
    "pt" : text_pt}


class Language():
    """this module imports all the text that is shown to the user.
The get_text method receives the key that contains the 
text that will be shown to the user. This method also receives 
the context which indicates the user's language."""


    def __init__(self, dict_with_all_languages, language):
        self.default_language = language
        self.suported_languages = dict_with_all_languages.keys()
        self.all_text = dict_with_all_languages


    def get_text(self, key, context=None):
        """ This method return the text, the langauge are passed in the context argument.
        >>> TEXT.get_text('OK', 'en')
        'OK'
        >>> TEXT.get_text('OK', 'pt')
        'Certo'
        """
        language = self.extract_lang(context)
        return self.all_text[language][key]


    def extract_lang(self, context):
        if hasattr(context, 'user_data'):
            user_data = context.user_data
            if "language" in user_data:
                return self.extract_lang(user_data["language"])
            return self.default_language
        elif context in self.suported_languages:
            return context
        else:
            return self.default_language


TEXT = Language(all_languages, default_language)
get_text = TEXT.get_text


