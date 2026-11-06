# Interface localization

The bot ships with English (`en`) and Portuguese (`pt`) translations. Its catalog loader accepts additional BCP 47 language tags, so adding many languages does not require changing a central registry. A language is offered to users only when a catalog exists; English text fills missing keys in partial catalogs.

To add a language, create `telegram_ecommerce/language/text_<tag>.py`, replacing hyphens with underscores. For example, `text_zh_Hant.py` exports a dictionary named `text_zh_Hant`. Copy the keys from `text_en.py`, translate the values, and set `_language_name` to the native language name. Run `python -m unittest tests.test_language` to check discovery, fallback, and selection.

The `/language` command displays buttons for up to 12 installed catalogs. With more catalogs, it asks for a language tag, keeping the keyboard manageable. Codes are also accepted with fewer catalogs. A locale with a region or script, such as `pt-BR`, resolves to its parent catalog (`pt`) when an exact catalog is absent. Unsupported codes resolve to the default English catalog for message lookup, but cannot be selected through `/language`.

This infrastructure can accommodate 100+ catalogs. Shipping 100+ languages still requires translated and reviewed text for each catalog; machine generated text should be reviewed by native speakers before use in payment flows.
