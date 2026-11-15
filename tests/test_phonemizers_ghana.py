"""Tests for the ghana-g2p-backed phonemizer.

ghana-g2p is in the ``test`` extra, so these tests call the real library.
The fixed expected strings are ghana-g2p 0.1.1 output on africa-g2p 0.3.5.
``Akwaaba`` / ``a kʷ a a b a`` is also the example in ghana-g2p's own README.
"""
import sys
import unittest
from importlib import metadata

import ghana_g2p.core
from scriptconv.phonemizers import (
    Alphabet,
    Phonemizer,
    UnsupportedLanguageError,
    get_phonemizer_class,
)

from scriptconv_nonfree.phonemizers.africa import AfricaG2PPhonemizer
from scriptconv_nonfree.phonemizers.ghana import GhanaG2PPhonemizer

# ghana-g2p languages whose africa-g2p 0.3.5 table is tts-reviewed: their own
# table, or the gaa (ada) and ewe (lip) tables they borrow.
ON_A_DRAFT_TABLE = {"ada", "dag", "ewe", "fat", "gaa", "lip", "twi"}


class TestGhanaG2PPhonemizer(unittest.TestCase):
    def test_twi_ipa(self):
        p = GhanaG2PPhonemizer(alphabet=Alphabet.IPA, allow_draft_rules=True)
        self.assertEqual(p.phonemize_string("Akwaaba", "twi"), "a kʷ a a b a")

    def test_twi_native_units(self):
        p = GhanaG2PPhonemizer(alphabet=Alphabet.AFRICA_G2P, allow_draft_rules=True)
        self.assertEqual(p.phonemize_string("Akwaaba", "twi"), "a kw a a b a")

    def test_ewe_y_is_the_palatal_glide(self):
        # ghana-g2p corrects africa-g2p's Ewe <y>, once IPA y, to /j/.
        p = GhanaG2PPhonemizer(allow_draft_rules=True)
        self.assertEqual(p.phonemize_string("yaa", "ewe"), "j a a")

    def test_dagbani_reads_through_the_engine(self):
        # africa-g2p 0.3.4 stopped writing Dagbani double vowels as long
        # vowels, so the expected string comes from the library itself. In
        # "Dagbani" the IPA (ɡ͡b) and the native units (gb) differ.
        expected = ghana_g2p.GhanaG2P("dag").ipa("Dagbani", sep=" ")
        p = GhanaG2PPhonemizer(allow_draft_rules=True)
        self.assertEqual(p.phonemize_string("Dagbani", "dag"), expected)

    def test_a_chart_table_needs_no_flag(self):
        self.assertEqual(GhanaG2PPhonemizer().phonemize_string("Akwaaba", "nzi"),
                         "a k w a a b a")

    def test_supported_langs_are_the_42_ghanaian_codes(self):
        langs = GhanaG2PPhonemizer.supported_langs(allow_draft_rules=True)
        self.assertEqual(len(langs), 42)
        for code in ("twi", "ewe", "gaa", "dag", "hau"):
            self.assertIn(code, langs)

    def test_get_lang_strips_region_only(self):
        p = GhanaG2PPhonemizer()
        self.assertEqual(p.get_lang("nzi-GH"), "nzi")
        with self.assertRaises(ValueError):
            p.get_lang("ee")

    def test_engine_is_cached_per_language(self):
        p = GhanaG2PPhonemizer()
        first = p._engine("twi")
        self.assertIs(p._engine("twi"), first)

    def test_rejects_unsupported_alphabet(self):
        with self.assertRaises(ValueError):
            GhanaG2PPhonemizer(alphabet=Alphabet.VOSK)

    def test_registry_resolves_the_member(self):
        self.assertIs(get_phonemizer_class(Phonemizer.GHANA_G2P), GhanaG2PPhonemizer)


class TestOneAfricaG2P(unittest.TestCase):
    def test_both_backends_read_one_africa_g2p(self):
        # ghana-g2p imports africa_g2p.G2P; the africa backend must run the
        # same class from the same installed distribution.
        engine = AfricaG2PPhonemizer()._engine("yor")
        self.assertIs(type(engine.g2p), ghana_g2p.core.G2P)
        loaded_by_ghana = sys.modules[ghana_g2p.core.G2P.__module__.partition(".")[0]]
        self.assertEqual(AfricaG2PPhonemizer().identity("yor").version,
                         loaded_by_ghana.__version__)
        self.assertEqual(loaded_by_ghana.__version__, metadata.version("africa-g2p"))


class TestDraftTables(unittest.TestCase):
    def test_a_language_on_a_draft_table_is_refused_by_default(self):
        with self.assertRaisesRegex(UnsupportedLanguageError,
                                    "ghana-g2p: .*'twi'.*'tts-reviewed'.*allow_draft_rules"):
            GhanaG2PPhonemizer().phonemize_string("Akwaaba", "twi")

    def test_a_donor_draft_table_is_named(self):
        # Adangme borrows the Ga table.
        with self.assertRaisesRegex(UnsupportedLanguageError, "table 'gaa' for 'ada'"):
            GhanaG2PPhonemizer().get_lang("ada")

    def test_supported_langs_leave_out_the_draft_tables(self):
        every = set(GhanaG2PPhonemizer.supported_langs(allow_draft_rules=True))
        self.assertEqual(every - set(GhanaG2PPhonemizer.supported_langs()), ON_A_DRAFT_TABLE)

    def test_each_backend_refuses_the_same_draft_table(self):
        with self.assertRaisesRegex(UnsupportedLanguageError, "'tts-reviewed'"):
            AfricaG2PPhonemizer().get_lang("ewe")
        with self.assertRaisesRegex(UnsupportedLanguageError, "'tts-reviewed'"):
            GhanaG2PPhonemizer().get_lang("ewe")


if __name__ == "__main__":
    unittest.main()
