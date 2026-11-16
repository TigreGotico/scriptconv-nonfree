"""Tests for the africa-g2p-backed phonemizer.

africa-g2p is in the ``test`` extra, so these tests call the real library.
The fixed expected strings are africa-g2p 0.3.5 output.
"""
import json
import sys
import tomllib
import unittest
from importlib import metadata
from pathlib import Path
from unittest import mock

import africa_g2p
import pytest
from scriptconv.phonemizers import (
    PHONEMIZER_REGISTRY,
    Alphabet,
    Phonemizer,
    UnsupportedLanguageError,
    get_phonemizer,
    get_phonemizer_class,
)

from scriptconv_nonfree.phonemizers.africa import AfricaG2PPhonemizer
from scriptconv_nonfree.phonemizers.ghana import GhanaG2PPhonemizer

# The confidence values served without allow_draft_rules, written out here
# rather than read from the module under test.
SERVED = ("omniglot", "high", "hand-verified", "medium", "tts-reviewed")

REGION_TABLES = ("hau-nigeria", "hau-niger", "dop-benin", "dop-benin2", "ngb-zaire",
                 "ngb-zaire2", "sag-congo", "sag-central_african_republic",
                 "sef-cote_d_ivoire", "sef-cote_d_ivoire2", "snk-senegal")


def _confidence_by_table():
    """Each rule table's ``confidence``, read from the installed JSON files."""
    languages = Path(africa_g2p.__file__).parent / "languages"
    return {path.stem: json.loads(path.read_text(encoding="utf-8")).get("confidence")
            for path in languages.glob("*.json")}


class TestAfricaG2PPhonemizer(unittest.TestCase):
    def test_ipa_output(self):
        p = AfricaG2PPhonemizer(alphabet=Alphabet.IPA)
        self.assertEqual(p.phonemize_string("ọmọ", "yor"), "ɔ m ɔ")

    def test_ipa_and_native_output_of_a_corrected_chart(self):
        ipa = AfricaG2PPhonemizer(alphabet=Alphabet.IPA)
        native = AfricaG2PPhonemizer(alphabet=Alphabet.AFRICA_G2P)
        self.assertEqual(ipa.phonemize_string("Akwaaba", "twi"), "a kʷ a a b a")
        self.assertEqual(native.phonemize_string("Akwaaba", "twi"), "a kw a a b a")

    def test_ethiopic_g_is_the_ipa_letter(self):
        # africa-g2p v0.2.4 fixed the Ethiopic tables, which wrote ASCII g
        # (U+0067) where IPA uses ɡ (U+0261).
        p = AfricaG2PPhonemizer(alphabet=Alphabet.IPA)
        self.assertEqual(p.phonemize_string("ግብር", "amh"), "ɡɨ bɨ rɨ")
        self.assertNotIn("g", p.phonemize_string("ገና", "amh"))

    def test_kabuverdianu_reads_letters_not_letter_names(self):
        # Before v0.2.4 the kea table read letter NAMES: kasa gave
        # 'ˈkapɐ a ˈɛs(i) a'.
        p = AfricaG2PPhonemizer(alphabet=Alphabet.IPA)
        self.assertEqual(p.phonemize_string("kasa", "kea"), "k a s a")
        self.assertEqual(p.phonemize_string("djuntu", "kea"), "d͡ʒ u n t u")

    def test_engine_is_cached_per_language(self):
        p = AfricaG2PPhonemizer()
        first = p._engine("yor")
        self.assertIs(p._engine("yor"), first)

    def test_the_engine_is_the_installed_africa_g2p(self):
        engine = AfricaG2PPhonemizer()._engine("yor")
        self.assertIs(type(engine.g2p), africa_g2p.G2P)

    def test_identity_names_the_africa_g2p_release(self):
        identity = AfricaG2PPhonemizer().identity("yor")
        self.assertEqual(
            (identity.backend, identity.distribution, identity.version, identity.lang),
            ("africa_g2p", "africa-g2p", metadata.version("africa-g2p"), "yor"))

    def test_get_lang_resolves_exact_iso_639_3_code(self):
        p = AfricaG2PPhonemizer()
        self.assertEqual(p.get_lang("yor"), "yor")
        # region subtag is stripped to the primary subtag before lookup
        self.assertEqual(p.get_lang("yor-NG"), "yor")

    def test_get_lang_rejects_unsupported_language(self):
        with self.assertRaisesRegex(UnsupportedLanguageError, "unsupported language 'zzz'"):
            AfricaG2PPhonemizer(allow_draft_rules=True).get_lang("zzz")

    def test_phonemize_string_rejects_unsupported_language(self):
        p = AfricaG2PPhonemizer()
        with self.assertRaises(ValueError):
            p.phonemize_string("hello", "zzz")

    def test_phonemize_returns_sentence_lists(self):
        p = AfricaG2PPhonemizer()
        out = p.phonemize("Ọmọ.", "yor")
        self.assertEqual(len(out), 1)
        self.assertTrue(all(isinstance(s, list) for s in out))

    def test_rejects_unsupported_alphabet(self):
        with self.assertRaises(ValueError):
            AfricaG2PPhonemizer(alphabet=Alphabet.VOSK)

    def test_a_missing_install_names_the_extra(self):
        with mock.patch.dict(sys.modules, {"africa_g2p": None}), \
                self.assertRaisesRegex(ImportError, r"scriptconv-nonfree\[africa\]"):
            AfricaG2PPhonemizer()


class TestDraftTables(unittest.TestCase):
    def test_a_draft_only_language_is_refused_by_default(self):
        self.assertEqual(_confidence_by_table()["aab"], "llm-draft")
        p = AfricaG2PPhonemizer()
        with self.assertRaisesRegex(UnsupportedLanguageError, "'aab'.*'llm-draft'.*allow_draft_rules"):
            p.get_lang("aab")
        with self.assertRaisesRegex(UnsupportedLanguageError, "llm-draft"):
            p.phonemize_string("aba", "aab")

    def test_a_draft_only_language_runs_with_the_flag(self):
        p = AfricaG2PPhonemizer(allow_draft_rules=True)
        expected = africa_g2p.AfricaPipeline(lang="aab", output="ipa").run("aba", sep=" ")
        self.assertEqual(p.phonemize_string("aba", "aab"), expected)
        self.assertEqual(p.identity("aab").version, metadata.version("africa-g2p"))

    def test_the_refusal_names_the_africa_g2p_release(self):
        with self.assertRaisesRegex(UnsupportedLanguageError,
                                    f"africa-g2p {metadata.version('africa-g2p')} "):
            AfricaG2PPhonemizer().get_lang("aab")

    def test_the_corrected_charts_are_served_by_default(self):
        # Dagbani, Ewe, Fante, Ga and Twi: Omniglot charts with corrections an
        # LLM proposed. The Ewe table scores closer to WikiPron than the chart.
        confidence = _confidence_by_table()
        corrected = sorted(t for t, c in confidence.items() if c == "tts-reviewed")
        self.assertEqual(corrected, ["dag", "ewe", "fat", "gaa", "twi"])
        p = AfricaG2PPhonemizer()
        for table in corrected:
            self.assertEqual(p.get_lang(table), table)

    def test_get_phonemizer_passes_the_flag(self):
        p = get_phonemizer(Phonemizer.AFRICA_G2P, Alphabet.IPA, allow_draft_rules=True)
        expected = africa_g2p.AfricaPipeline(lang="aab", output="ipa").run("aba", sep=" ")
        self.assertEqual(p.phonemize_string("aba", "aab"), expected)

    def test_supported_langs_are_the_served_tables(self):
        confidence = _confidence_by_table()
        served = sorted(t for t, c in confidence.items() if c in SERVED)
        self.assertEqual(sorted(AfricaG2PPhonemizer.supported_langs()), served)
        self.assertEqual(sorted(AfricaG2PPhonemizer.supported_langs(allow_draft_rules=True)),
                         sorted(confidence))
        self.assertIn("twi", served)
        self.assertIn("aab", confidence)
        self.assertNotIn("aab", served)


class TestRegionTables(unittest.TestCase):
    def test_region_suffixed_tables_resolve_by_their_own_name(self):
        # 11 rule files carry a region suffix instead of a bare ISO 639-3
        # code; each is a chart table and resolves with no flag.
        confidence = _confidence_by_table()
        p = AfricaG2PPhonemizer()
        for code in REGION_TABLES:
            self.assertIn(confidence[code], ("high", "omniglot"), code)
            self.assertEqual(p.get_lang(code), code)

    def test_a_region_suffixed_code_phonemizes(self):
        p = AfricaG2PPhonemizer(alphabet=Alphabet.IPA)
        self.assertEqual(p.phonemize_string("ƙasa", "hau-nigeria"), "kʼ a s a")

    def test_an_underscore_is_read_as_a_hyphen(self):
        self.assertEqual(AfricaG2PPhonemizer().get_lang("HAU_NIGERIA"), "hau-nigeria")

    def test_a_bare_code_never_picks_a_region(self):
        # africa-g2p 0.3 adds a bare 'hau' table, an LLM draft. The chart
        # tables for Hausa stay under their region names.
        self.assertEqual(_confidence_by_table()["hau"], "llm-draft")
        with self.assertRaisesRegex(UnsupportedLanguageError, "'hau'.*'llm-draft'"):
            AfricaG2PPhonemizer().get_lang("hau")
        self.assertEqual(AfricaG2PPhonemizer(allow_draft_rules=True).get_lang("hau"), "hau")
        self.assertEqual(AfricaG2PPhonemizer(allow_draft_rules=True).get_lang("hau-NG"), "hau")


class TestDataLicence(unittest.TestCase):
    def test_the_licence_fields_keep_the_data_statement(self):
        root = Path(__file__).resolve().parent.parent
        project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"]
        self.assertIn("LicenseRef-AfricaG2P-Data", project["license"])
        self.assertIn("LICENSE.africa-g2p-data.md", project["license-files"])
        notice = (root / "LICENSE.africa-g2p-data.md").read_text(encoding="utf-8")
        self.assertIn("no licence grant", notice)
        self.assertIn("Omniglot", notice)
        self.assertIn("Alphabets of Africa", notice)

    def test_the_extras_install_one_africa_g2p_floor(self):
        root = Path(__file__).resolve().parent.parent
        extras = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))[
            "project"]["optional-dependencies"]
        floors = {extra: [d for d in deps if d.startswith("africa-g2p")]
                  for extra, deps in extras.items() if extra in ("africa", "ghana", "test")}
        self.assertEqual(floors, {extra: ["africa-g2p>=0.3.5"] for extra in floors})
        self.assertEqual(len(floors), 3)


class TestAfricaG2PRegistration(unittest.TestCase):
    def test_registered(self):
        self.assertIn(Phonemizer.AFRICA_G2P, PHONEMIZER_REGISTRY)

    def test_class_resolves(self):
        cls = get_phonemizer_class(Phonemizer.AFRICA_G2P)
        self.assertIs(cls, AfricaG2PPhonemizer)

    def test_get_phonemizer_builds_it(self):
        p = get_phonemizer(Phonemizer.AFRICA_G2P, Alphabet.IPA)
        self.assertIsInstance(p, AfricaG2PPhonemizer)
        self.assertFalse(p.allow_draft_rules)

    def test_no_lang_default_registered(self):
        # design decision: africa-g2p is not made a default for any language,
        # including African languages that currently have no LANG_DEFAULTS
        # entry at all — see the PR body for the reasoning.
        from scriptconv.phonemizers import LANG_DEFAULTS
        for candidates in LANG_DEFAULTS.values():
            self.assertNotIn(Phonemizer.AFRICA_G2P, candidates)


def _with_confidence(value):
    """Every africa-g2p rule table reads as having *value* as its confidence."""
    return mock.patch.object(africa_g2p.loader, "load_rules", return_value={"confidence": value})


BACKENDS = [(AfricaG2PPhonemizer, "yor"), (GhanaG2PPhonemizer, "nzi")]


@pytest.mark.parametrize("backend, lang", BACKENDS)
@pytest.mark.parametrize("value", SERVED)
def test_a_served_confidence_value_needs_no_flag(value, backend, lang):
    with _with_confidence(value):
        assert backend().get_lang(lang) == lang


@pytest.mark.parametrize("backend, lang", BACKENDS)
def test_llm_draft_needs_the_flag(backend, lang):
    with _with_confidence("llm-draft"):
        with pytest.raises(UnsupportedLanguageError, match="'llm-draft'.*allow_draft_rules"):
            backend().get_lang(lang)
        assert backend(allow_draft_rules=True).get_lang(lang) == lang


@pytest.mark.parametrize("backend, lang", BACKENDS)
def test_a_confidence_value_nobody_listed_needs_the_flag(backend, lang):
    with _with_confidence("native-reviewed"):
        with pytest.raises(UnsupportedLanguageError, match="'native-reviewed'"):
            backend().get_lang(lang)
        assert backend(allow_draft_rules=True).get_lang(lang) == lang


if __name__ == "__main__":
    unittest.main()
