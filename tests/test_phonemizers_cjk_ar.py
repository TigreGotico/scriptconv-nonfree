import unittest

from scriptconv.phonemizers import Phonemizer, get_phonemizer_class


class TestLicensingStubs(unittest.TestCase):
    def test_mantoq_wrapper_constructs_from_vendored_copy(self):
        cls = get_phonemizer_class(Phonemizer.MANTOQ)
        p = cls()
        out = p.phonemize_string("مرحبا", "ar")
        self.assertTrue(out)
        self.assertNotIn("_", out)

    def test_quarantine_carries_license_notices(self):
        import pathlib
        base = pathlib.Path("scriptconv_nonfree/phonemizers/_vendored")
        self.assertTrue((base / "mantoq" / "LICENSE.md").is_file())
        self.assertTrue((base / "mantoq" / "LICENSE.mantoq").is_file())
        self.assertTrue((base / "mantoq" / "LICENSE.cc-by-nc-4.0").is_file())
        self.assertTrue((base / "iqra_phonetiser" / "LICENSE.md").is_file())
        self.assertTrue((base / "iqra_phonetiser" / "LICENSE.cc-by-nc-4.0").is_file())
        self.assertTrue((base / "africa_g2p" / "LICENSE.md").is_file())

    def test_quarantine_not_imported_at_package_import(self):
        import subprocess, sys
        code = ("import sys, scriptconv_nonfree, scriptconv_nonfree.phonemizers; "
                "bad=[m for m in sys.modules if '_vendored' in m]; "
                "print(bad); sys.exit(1 if bad else 0)")
        proc = subprocess.run([sys.executable, "-c", code],
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout)


if __name__ == "__main__":
    unittest.main()
