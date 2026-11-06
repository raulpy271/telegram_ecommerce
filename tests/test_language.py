import os
import unittest
from types import SimpleNamespace

os.environ.setdefault("BOT_TOKEN", "test-token")
for name in ("DB_USER", "DB_PASSWORD", "DB_HOST", "DB_NAME"):
    os.environ.setdefault(name, "test")

from telegram_ecommerce.language import Language, TEXT, normalize_locale
from telegram_ecommerce.handlers.language import get_selected_language, language_options


class LanguageTests(unittest.TestCase):
    def test_catalogs_are_discovered(self):
        self.assertIn("en", TEXT.all_text)
        self.assertIn("pt", TEXT.all_text)

    def test_locale_normalization_and_parent_fallback(self):
        self.assertEqual(normalize_locale(" PT_br "), "pt-BR")
        self.assertEqual(TEXT.resolve_locale("pt-BR"), "pt")
        self.assertEqual(TEXT.resolve_locale("xx"), "en")
        self.assertIsNone(normalize_locale("../../en"))

    def test_partial_catalog_falls_back_by_key(self):
        language = Language({"en": {"greeting": "Hello", "bye": "Goodbye"},
                             "fr": {"greeting": "Bonjour"}}, "en")
        self.assertEqual(language.get_text("greeting", "fr-CA"), "Bonjour")
        self.assertEqual(language.get_text("bye", "fr-CA"), "Goodbye")
        with self.assertRaises(KeyError):
            language.get_text("unknown", "fr")

    def test_more_than_100_catalogs_can_be_resolved(self):
        catalogs = {"en": {"hello": "Hello"}}
        codes = ["".join((chr(97 + first), chr(97 + second), chr(97 + third)))
                 for first in range(5) for second in range(5) for third in range(5)]
        catalogs.update({code: {"hello": str(index)} for index, code in enumerate(codes)})
        # The registry and lookup have no fixed language-count limit.
        language = Language(catalogs, "en")
        self.assertEqual(len(language.suported_languages), 126)
        self.assertEqual(language.get_text("hello", codes[42]), "42")

    def test_context_selected_locale(self):
        context = SimpleNamespace(user_data={"language": "pt-BR"})
        self.assertEqual(TEXT.extract_lang(context), "pt")

    def test_language_selection(self):
        self.assertEqual(get_selected_language("pt"), "pt")
        self.assertEqual(get_selected_language("Português (pt)"), "pt")
        self.assertEqual(len(language_options()), 2)
        with self.assertRaises(ValueError):
            get_selected_language("xx")


if __name__ == "__main__":
    unittest.main()
