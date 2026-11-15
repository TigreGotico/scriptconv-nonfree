"""Frontend errors and ``PhonemizerIdentity`` for the wrappers this package holds."""
import sys
import tomllib
from importlib import metadata
from pathlib import Path

import pytest
from packaging.requirements import Requirement

from scriptconv.phonemizers import UnsupportedLanguageError
from scriptconv_nonfree.phonemizers.africa import AfricaG2PPhonemizer
from scriptconv_nonfree.phonemizers.ar import MantoqPhonemizer
from scriptconv_nonfree.phonemizers.ghana import GhanaG2PPhonemizer
from scriptconv_nonfree.phonemizers.vi import VIPhonemePhonemizer

ROOT = Path(__file__).resolve().parent.parent


class TestErrors:
    @pytest.mark.parametrize("resolve, lang", [
        (AfricaG2PPhonemizer.get_lang, "zzz"),
        (GhanaG2PPhonemizer.get_lang, "zzz"),
    ])
    def test_each_wrapper_with_its_own_check_raises_the_same_error(self, resolve, lang):
        with pytest.raises(UnsupportedLanguageError, match=lang):
            resolve(lang)


class TestIdentity:
    def test_vendored_code_reports_the_scriptconv_version(self):
        from scriptconv import version
        identity = MantoqPhonemizer().identity("ar")
        assert (identity.backend, identity.distribution, identity.version) == \
            ("mantoq", "scriptconv", metadata.version("scriptconv"))
        assert identity.version == version.VERSION_STR


class TestVietnameseNeedsAnOlderPython:
    def test_the_error_gives_the_reason(self, monkeypatch):
        monkeypatch.setitem(sys.modules, "viphoneme", None)
        monkeypatch.setattr(sys, "version_info", (3, 12, 0))
        with pytest.raises(ImportError) as refused:
            VIPhonemePhonemizer()
        assert "below 3.12" in str(refused.value) and "imp" in str(refused.value)
        assert "scriptconv[vi]" not in str(refused.value)

    def test_a_python_that_can_load_it_is_told_to_install_it(self, monkeypatch):
        monkeypatch.setitem(sys.modules, "viphoneme", None)
        monkeypatch.setattr(sys, "version_info", (3, 11, 9))
        with pytest.raises(ImportError, match=r"scriptconv\[vi\]"):
            VIPhonemePhonemizer()

    @pytest.mark.parametrize("python, installed", [("3.11", True), ("3.12", False), ("3.13", False)])
    def test_the_extra_installs_the_engine_only_where_it_loads(self, python, installed):
        project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
        engine = [Requirement(dep) for dep in project["optional-dependencies"]["vi"]
                  if not dep.startswith("scriptconv")]
        assert {dep.name for dep in engine} == {"viphoneme", "vinorm", "underthesea", "eng_to_ipa"}
        assert [dep.marker.evaluate({"python_version": python}) for dep in engine] == \
            [installed] * len(engine)
