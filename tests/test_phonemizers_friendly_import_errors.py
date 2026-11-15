"""Pins the friendly-ImportError convention for the lazy backend import
inside the viphoneme wrapper.

The test shadows the backend module in ``sys.modules`` with ``None`` and
asserts the resulting exception is an ``ImportError`` whose message contains
an install instruction.
"""
import sys
import unittest
from unittest.mock import patch

from scriptconv.phonemizers import Phonemizer, get_phonemizer_class


class TestLazyBackendImportsAreFriendly(unittest.TestCase):
    def test_viphoneme(self):
        # Python 3.12 and later gives the reason instead of an install command.
        cls = get_phonemizer_class(Phonemizer.VIPHONEME)
        self.assertTrue(cls.__module__.startswith("scriptconv_nonfree."), cls.__module__)
        with patch("sys.version_info", (3, 11, 9)), \
                patch.dict(sys.modules, {"viphoneme": None}):
            with self.assertRaises(ImportError) as ctx:
                cls()
        self.assertIn("pip install", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
