"""Vendored upstream code under its own licence, stated in its directory.

* ``mantoq/`` — Arabic G2P (github.com/mush42/mantoq, MIT). Its phonetisation
  core (``buck/phonetise_buckwalter.py``) is **CC BY-NC 4.0** (Nawar Halabi's
  Arabic-Phonetiser): non-commercial use only. ``num2words.py`` is Apache-2.0,
  written for scriptconv. See ``mantoq/LICENSE.md``, ``mantoq/LICENSE.mantoq``
  and ``mantoq/LICENSE.cc-by-nc-4.0``.
* ``iqra_phonetiser/`` — the IqraEval fork of Arabic-Phonetiser,
  **CC BY-NC 4.0**. See ``iqra_phonetiser/LICENSE.md``.
* ``africa_g2p/`` — African-language G2P (github.com/AfriSpeech/africa-g2p),
  pinned at release ``v0.2.4`` (commit e3642dea). The **code** is Apache-2.0.
  The **data** (``languages/`` and ``data/``) has no licence grant: it is
  derived from Omniglot script charts (© Simon Ager) and Hartell (ed.),
  *Alphabets of Africa* (UNESCO/SIL, 1993). See ``africa_g2p/LICENSE.md`` and
  ``africa_g2p/DATA_LICENSE.md``.

Nothing imports these at package import time; they load only when a caller
requests the corresponding phonemizer.
"""
