"""Point the scriptconv registry at the classes this package holds."""

from unittest import mock

import pytest

from scriptconv.phonemizers.enums import Phonemizer as _P
from scriptconv.phonemizers.registry import PHONEMIZER_REGISTRY

_BASE = "scriptconv_nonfree.phonemizers"

MOVED = {
    _P.MANTOQ: (f"{_BASE}.ar", "MantoqPhonemizer", "ar-phonemizers"),
    _P.HALABI: (f"{_BASE}.ar", "HalabiPhonemizer", "ar-phonemizers"),
    _P.IQRA: (f"{_BASE}.ar", "IqraPhonemizer", "ar-phonemizers"),
    _P.VIPHONEME: (f"{_BASE}.vi", "VIPhonemePhonemizer", "vi"),
    _P.AFRICA_G2P: (f"{_BASE}.africa", "AfricaG2PPhonemizer", "africa"),
    _P.GHANA_G2P: (f"{_BASE}.ghana", "GhanaG2PPhonemizer", "ghana"),
}


@pytest.fixture(autouse=True, scope="session")
def _registry_points_here():
    with mock.patch.dict(PHONEMIZER_REGISTRY, MOVED):
        yield
