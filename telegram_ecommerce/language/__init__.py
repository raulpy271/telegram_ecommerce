"""Message catalogs and locale selection for the Telegram interface.

Add a ``text_<locale>.py`` module containing a ``text_<locale>`` mapping to
register a translation. Locale tags use BCP 47 externally and underscores in
Python module names (for example ``text_zh_Hant.py`` for ``zh-Hant``).
"""

from importlib import import_module
from pkgutil import iter_modules

from telegram_ecommerce.utils.consts import default_language


def normalize_locale(value):
    """Return a canonical language tag, or ``None`` for invalid input."""
    if not isinstance(value, str):
        return None
    parts = value.strip().replace("_", "-").split("-")
    if not parts or not parts[0].isalpha() or not 2 <= len(parts[0]) <= 3:
        return None
    if any(not part.isalnum() or not 2 <= len(part) <= 8 for part in parts[1:]):
        return None
    normalized = [parts[0].lower()]
    for part in parts[1:]:
        if len(part) == 4 and part.isalpha():
            normalized.append(part.title())
        elif len(part) == 2 and part.isalpha():
            normalized.append(part.upper())
        else:
            normalized.append(part.lower())
    return "-".join(normalized)


def load_catalogs():
    """Discover packaged translation modules without a hand maintained registry."""
    catalogs = {}
    for module in iter_modules(__path__):
        if not module.name.startswith("text_"):
            continue
        locale = normalize_locale(module.name.removeprefix("text_"))
        if locale is None or locale in catalogs:
            raise ValueError(f"Invalid or duplicate locale module: {module.name}")
        translations = getattr(
            import_module(f"{__name__}.{module.name}"), module.name, None
        )
        if not isinstance(translations, dict):
            raise TypeError(f"{module.name} must export a dictionary of messages")
        catalogs[locale] = translations
    return catalogs


class Language:
    """Resolve UI messages with English fallback for incomplete catalogs."""

    def __init__(self, catalogs, default):
        default = normalize_locale(default)
        if default not in catalogs:
            raise ValueError("The default language must have a catalog")
        self.default_language = default
        self.all_text = catalogs
        self.suported_languages = catalogs.keys()  # Compatibility with existing callers.
        for locale, messages in catalogs.items():
            if not isinstance(messages, dict):
                raise TypeError(f"Catalog {locale} must be a dictionary")
            for key, value in messages.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    raise TypeError(f"Catalog {locale} must contain string keys and values")

    def resolve_locale(self, value):
        locale = normalize_locale(value)
        while locale:
            if locale in self.all_text:
                return locale
            locale = locale.rpartition("-")[0] or None
        return self.default_language

    def extract_lang(self, context):
        if hasattr(context, "user_data"):
            selected = context.user_data.get("language")
            if selected:
                return self.resolve_locale(selected)
            return self.default_language
        return self.resolve_locale(context)

    def get_text(self, key, context=None):
        locale = self.extract_lang(context)
        if key in self.all_text[locale]:
            return self.all_text[locale][key]
        try:
            return self.all_text[self.default_language][key]
        except KeyError as error:
            raise KeyError(f"Missing message in {locale} and {self.default_language}: {key}") from error

    def display_name(self, locale):
        """Use a native name where provided, otherwise show the language tag."""
        locale = self.resolve_locale(locale)
        return self.all_text[locale].get("_language_name", locale)


TEXT = Language(load_catalogs(), default_language)
get_text = TEXT.get_text
