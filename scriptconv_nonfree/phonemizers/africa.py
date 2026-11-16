"""africa-g2p-backed phonemizer.

Wraps ``AfricaPipeline`` from the installed ``africa-g2p`` distribution
(AfriSpeech, https://github.com/AfriSpeech/africa-g2p), a rule-based
grapheme-to-phoneme engine with one rule table per African language. One
backend, hundreds of ISO 639-3 codes.

Unlike most wrappers in this package, africa-g2p natively emits two kinds of
output for the same rule set:

* IPA (``output="ipa"``) — scriptconv's usual currency;
* native-orthography phoneme units (``output="grapheme"``) — the language's own
  writing units (e.g. ``ny``, ``kp``, ``ɔ``), which the upstream project notes
  trains TTS/ASR models better than IPA for these languages.

Both are exposed here as selectable alphabets — :attr:`Alphabet.IPA` and
:attr:`Alphabet.AFRICA_G2P` — the same shape as :class:`~scriptconv.phonemizers.zh.JiebaPhonemizer`
(pinyin vs. IPA) rather than a single fixed alphabet: africa-g2p is not a
one-notation engine like Cotovía or Vosk.

Each rule table records where its rules come from in a ``confidence`` field.
A table transcribed from a chart (Omniglot, or Hartell (ed.), *Alphabets of
Africa*, UNESCO 1993) is used as is. So is a ``tts-reviewed`` table: a chart
transcription with corrections that an LLM proposed and no native speaker has
checked, which measures closer to WikiPron than the chart it replaces (Ewe).
Any other table, for example one that an LLM drafted from corpus text
(``llm-draft``), is a draft: the backend refuses it unless the caller passes
``allow_draft_rules=True``. :class:`~scriptconv_nonfree.phonemizers.ghana.GhanaG2PPhonemizer`
applies the same rule to the table that ghana-g2p loads.

The code of africa-g2p is Apache-2.0. Its rule tables have no licence grant:
see ``LICENSE.africa-g2p-data.md`` in this distribution.

Optional extra: ``pip install scriptconv-nonfree[africa]``.
"""
from functools import lru_cache

from scriptconv.phonemizers.base import (
    BasePhonemizer,
    UnsupportedLanguageError,
    _check_alphabet,
    _primary_subtag,
)
from scriptconv.phonemizers.enums import Alphabet

__all__ = ["SERVED_CONFIDENCE", "AfricaG2PPhonemizer", "draft_status", "refuse_draft"]

SERVED_CONFIDENCE = frozenset({"omniglot", "high", "medium", "hand-verified", "tts-reviewed"})
"""The ``confidence`` values of africa-g2p tables that are served by default.

Each table with one of these values names an Omniglot chart or a page of
*Alphabets of Africa* in its ``source`` field; ``tts-reviewed`` is such a
chart with LLM-proposed corrections. Every other value is a draft, also a
value that a later africa-g2p adds."""


def _africa_g2p():
    """Import ``africa_g2p`` lazily, naming the extra when it is missing."""
    try:
        import africa_g2p
    except ImportError as e:
        raise ImportError(
            "africa-g2p is required for the African-language phonemizer. "
            "Install it with 'pip install scriptconv-nonfree[africa]' "
            "(or 'pip install scriptconv[africa]').") from e
    return africa_g2p


def draft_status(table: str) -> str | None:
    """The ``confidence`` of africa-g2p's rule *table* when it is a draft, else ``None``."""
    confidence = _africa_g2p().loader.load_rules(table).get("confidence")
    return None if confidence in SERVED_CONFIDENCE else str(confidence)


def refuse_draft(table: str, target_lang: str, backend: str) -> None:
    """Raise :class:`UnsupportedLanguageError` when africa-g2p's rule *table* is a draft."""
    status = draft_status(table)
    if status is not None:
        raise UnsupportedLanguageError(
            f"{backend}: the africa-g2p {_africa_g2p().__version__} rule table "
            f"{table!r} for {target_lang!r} has confidence {status!r}, so it is a "
            f"draft. Pass allow_draft_rules=True to use it")


@lru_cache(maxsize=1)
def _served_tables() -> tuple[str, ...]:
    return tuple(table for table in _africa_g2p().available_languages()
                 if draft_status(table) is None)


class AfricaG2PPhonemizer(BasePhonemizer):
    """
    Rule-based G2P phonemizer backed by africa-g2p, by ISO 639-3 code.

    The languages are africa-g2p's rule tables, read at runtime from
    ``africa_g2p.available_languages()``. A draft table is refused unless the
    instance is built with ``allow_draft_rules=True``.

    Per-language engines are created lazily on first use and cached for the
    lifetime of the instance.
    """

    engine_distribution = "africa-g2p"

    def __init__(self, alphabet: Alphabet = Alphabet.IPA, allow_draft_rules: bool = False):
        _check_alphabet(self, alphabet, [Alphabet.IPA, Alphabet.AFRICA_G2P])
        _africa_g2p()
        super().__init__(alphabet=alphabet)
        self.allow_draft_rules = allow_draft_rules
        self._cache: dict[str, object] = {}

    def _engine(self, resolved_lang: str):
        """Return, lazily creating and caching, the pipeline for *resolved_lang*."""
        if resolved_lang not in self._cache:
            output = "ipa" if self.alphabet == Alphabet.IPA else "grapheme"
            self._cache[resolved_lang] = _africa_g2p().AfricaPipeline(
                lang=resolved_lang, output=output)
        return self._cache[resolved_lang]

    @classmethod
    def supported_langs(cls, allow_draft_rules: bool = False) -> list[str]:
        """Return africa-g2p's rule tables, the drafts only with *allow_draft_rules*."""
        if allow_draft_rules:
            return _africa_g2p().available_languages()
        return list(_served_tables())

    def get_lang(self, target_lang: str) -> str:
        """
        Resolve *target_lang* to an africa-g2p rule table.

        Two exact lookups, in order, and no fuzzing (africa-g2p keys its rule
        files by name, not by BCP-47 macrolanguage/region mapping, so
        :meth:`BasePhonemizer.match_lang`'s closest-match search does not
        apply):

        1. the whole tag, lowercased, first as written and then with ``_``
           read as ``-``. 11 of the rule files carry a region suffix rather
           than a bare ISO 639-3 code (``hau-nigeria``, ``hau-niger``,
           ``dop-benin``, ``dop-benin2``, ``ngb-zaire``, ``ngb-zaire2``,
           ``sag-congo``, ``sag-central_african_republic``,
           ``sef-cote_d_ivoire``, ``sef-cote_d_ivoire2``, ``snk-senegal``).
        2. the primary subtag (``twi-GH`` -> ``twi``).

        A bare code never resolves to a region-suffixed table. Picking one
        region for ``hau`` would be a claim about which variety a caller
        meant, and this wrapper does not make it. ``hau`` resolves only to
        a bare ``hau`` table, which africa-g2p 0.3 ships as a draft.

        Raises:
            UnsupportedLanguageError: If africa-g2p has no rule table for
                *target_lang*, or if the table is a draft and the instance
                was not built with ``allow_draft_rules=True``.
        """
        tables = _africa_g2p().available_languages()
        lowered = target_lang.lower()
        # Two of the names keep an underscore of their own
        # (sef-cote_d_ivoire, sag-central_african_republic), so the tag is
        # tried as written before ``_`` is read as ``-``.
        for table in (lowered, lowered.replace("_", "-"), _primary_subtag(target_lang)):
            if table in tables:
                if not self.allow_draft_rules:
                    refuse_draft(table, target_lang, "africa-g2p")
                return table
        raise UnsupportedLanguageError(f"africa-g2p: unsupported language {target_lang!r}")

    def phonemize_string(self, text: str, lang: str) -> str:
        return self._engine(self.get_lang(lang)).run(text, sep=" ")
