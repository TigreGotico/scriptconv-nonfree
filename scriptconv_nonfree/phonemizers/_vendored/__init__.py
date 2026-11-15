"""Vendored upstream code under its own licence, stated in its directory.

* ``mantoq/`` — Arabic G2P (github.com/mush42/mantoq, MIT). Its phonetisation
  core (``buck/phonetise_buckwalter.py``) is **CC BY-NC 4.0** (Nawar Halabi's
  Arabic-Phonetiser): non-commercial use only. ``num2words.py`` is Apache-2.0,
  written for scriptconv. See ``mantoq/LICENSE.md``, ``mantoq/LICENSE.mantoq``
  and ``mantoq/LICENSE.cc-by-nc-4.0``.
* ``iqra_phonetiser/`` — the IqraEval fork of Arabic-Phonetiser,
  **CC BY-NC 4.0**. See ``iqra_phonetiser/LICENSE.md``.

Nothing imports these at package import time; they load only when a caller
requests the corresponding phonemizer.
"""
