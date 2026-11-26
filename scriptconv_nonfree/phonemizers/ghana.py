"""ghana-g2p-backed phonemizer.

Wraps ``ghana-g2p`` (GhanaNLP, https://github.com/GhanaNLP/ghana-g2p,
Apache-2.0), a grapheme-to-phoneme library for 42 Ghanaian languages. It is
built on africa-g2p's rule tables and adds three things for Ghanaian text:
Unicode codepoint normalisation (for example ``ʊ`` U+028A written for ``ʋ``
U+028B), a patch table of missing or corrected letters, and donor rule sets
for languages africa-g2p has no table for. Every result records whether its
rules are the language's own, an equivalent code, or a related donor.

Like :class:`~scriptconv_nonfree.phonemizers.africa.AfricaG2PPhonemizer`, it
emits IPA (:attr:`Alphabet.IPA`) or native-orthography phoneme units
(:attr:`Alphabet.AFRICA_G2P`).

ghana-g2p loads the installed ``africa-g2p``, the same distribution that
``AfricaG2PPhonemizer`` loads, so both backends read the same rule tables. A
language whose africa-g2p table is a draft is refused unless the caller
passes ``allow_draft_rules=True``, as in ``AfricaG2PPhonemizer``.

Optional extra: ``pip install scriptconv-nonfree[ghana]``.
"""

from scriptconv.phonemizers.base import (
    BasePhonemizer,
    UnsupportedLanguageError,
    _check_alphabet,
    _primary_subtag,
)
from scriptconv.phonemizers.enums import Alphabet

from scriptconv_nonfree.phonemizers.africa import draft_status, refuse_draft

__all__ = ["GhanaG2PPhonemizer"]


def _ghana_g2p():
    """Import ``ghana_g2p`` lazily, naming the extra when it is missing."""
    try:
        import ghana_g2p
    except ImportError as e:
        raise ImportError(
            "ghana-g2p is required for the Ghanaian phonemizer. Install it "
            "with 'pip install scriptconv-nonfree[ghana]' (or 'pip install scriptconv[ghana]')."
        ) from e
    return ghana_g2p


def _rule_tables() -> dict[str, str]:
    """ghana-g2p's language codes, each with the africa-g2p table it loads."""
    return {entry["code"]: entry["rules"] for entry in _ghana_g2p().languages()}


class GhanaG2PPhonemizer(BasePhonemizer):
    """
    Rule-based G2P for 42 Ghanaian languages, backed by ``ghana-g2p``.

    Languages are ghana-g2p's own ISO 639-3 codes (``twi``, ``ewe``, ``dag``,
    ``gaa``, ``hau``, ...), read at runtime from ``ghana_g2p.languages()``.
    A language whose africa-g2p table is a draft is refused unless the
    instance is built with ``allow_draft_rules=True``.
    One engine per language is created on first use and cached.
    """

    engine_distribution = "ghana-g2p"

    def __init__(self, alphabet: Alphabet = Alphabet.IPA, allow_draft_rules: bool = False):
        _check_alphabet(self, alphabet, [Alphabet.IPA, Alphabet.AFRICA_G2P])
        super().__init__(alphabet=alphabet)
        self.allow_draft_rules = allow_draft_rules
        self._cache: dict[str, object] = {}

    def _engine(self, resolved_lang: str):
        """Return, lazily creating and caching, the engine for *resolved_lang*. A language on a draft africa-g2p
        table is refused unless the instance was built with ``allow_draft_rules=True``."""
        if resolved_lang not in self._cache:
            if not self.allow_draft_rules:
                refuse_draft(_rule_tables()[resolved_lang], resolved_lang, "ghana-g2p")
            self._cache[resolved_lang] = _ghana_g2p().GhanaG2P(resolved_lang)
        return self._cache[resolved_lang]

    @classmethod
    def supported_langs(cls, allow_draft_rules: bool = False) -> list[str]:
        """Return ghana-g2p's codes, those on a draft table only with *allow_draft_rules*."""
        return [code for code, table in _rule_tables().items()
                if allow_draft_rules or draft_status(table) is None]

    @classmethod
    def get_lang(cls, target_lang: str) -> str:
        """
        Resolve *target_lang* to a ghana-g2p ISO 639-3 code. A language on a
        draft table resolves too: the instance refuses it at first use.

        Only the primary subtag is matched, exactly (``twi-GH`` -> ``twi``).
        ISO 639-1 tags are not mapped (``ee`` is not ``ewe``).

        Raises:
            UnsupportedLanguageError: If ghana-g2p has no such language.
        """
        key = _primary_subtag(target_lang)
        tables = _rule_tables()
        if key not in tables:
            raise UnsupportedLanguageError(f"ghana-g2p: unsupported language {target_lang!r}")
        return key

    def phonemize_string(self, text: str, lang: str) -> str:
        engine = self._engine(self.get_lang(lang))
        if self.alphabet == Alphabet.IPA:
            return engine.ipa(text, sep=" ")
        return engine.grapheme(text, sep=" ")
