# scriptconv-nonfree

The scriptconv phonemizer backends whose code, data or dependencies are for non-commercial use only, or carry no licence grant.

## Where this fits

[scriptconv](https://github.com/TigreGotico/scriptconv) is the text conversion library. Its wheel holds only Apache-2.0 code. Each backend in this package has a non-commercial licence, or data with no licence grant, somewhere in its chain, so it ships here instead.

scriptconv keeps the registry. A backend keeps its `Phonemizer` value and its routing entry in scriptconv, and scriptconv imports the class from this package only when a caller asks for that backend. The scriptconv extra of each backend installs this package:

```bash
pip install scriptconv[ar-phonemizers]
```

```python
from scriptconv.phonemizers import Phonemizer, get_phonemizer

get_phonemizer(Phonemizer.MANTOQ).phonemize_string("مرحبا", "ar")
```

This package depends on scriptconv. scriptconv never imports this package when it is imported itself.

## Backends

| `Phonemizer` value | Class | Module | Restricted item in the chain |
| --- | --- | --- | --- |
| `mantoq` | `MantoqPhonemizer` | `scriptconv_nonfree.phonemizers.ar` | the vendored Halabi phonetiser in mantoq (CC-BY-NC-4.0) |
| `halabi` | `HalabiPhonemizer` | `scriptconv_nonfree.phonemizers.ar` | the same vendored phonetiser (CC-BY-NC-4.0) |
| `iqra` | `IqraPhonemizer` | `scriptconv_nonfree.phonemizers.ar` | the vendored IqraEval phonetiser (CC-BY-NC-4.0) |
| `viphoneme` | `VIPhonemePhonemizer` | `scriptconv_nonfree.phonemizers.vi` | viphoneme and vinorm, which PyPI marks "Free for non-commercial use" |
| `africa_g2p` | `AfricaG2PPhonemizer` | `scriptconv_nonfree.phonemizers.africa` | the africa-g2p language data, which has no licence grant |
| `ghana_g2p` | `GhanaG2PPhonemizer` | `scriptconv_nonfree.phonemizers.ghana` | the same africa-g2p language data, which ghana-g2p loads |

Each backend's own dependencies install with the extra of the same name, for example `pip install scriptconv-nonfree[vi]`.

## The African backends

The `africa` extra installs `africa-g2p>=0.3.5` from PyPI (AfriSpeech/africa-g2p). The `ghana` extra installs `ghana-g2p>=0.1.1` (GhanaNLP/ghana-g2p) with the same africa-g2p floor. ghana-g2p loads the same installed africa-g2p, so the two backends always read the same rule tables. `identity()` of `AfricaG2PPhonemizer` gives the africa-g2p version, and `identity()` of `GhanaG2PPhonemizer` gives the ghana-g2p version.

Each africa-g2p rule table has a `confidence` field. A table with `omniglot`, `high`, `medium` or `hand-verified` is transcribed from an Omniglot chart or from Hartell (ed.), *Alphabets of Africa* (UNESCO, 1993). Every other value is a draft. In africa-g2p 0.3.5, 352 tables are `llm-draft` (an LLM drafted them from corpus text) and 5 are `tts-reviewed` (an LLM corrected the chart transcription, and no native speaker has checked it). The `tts-reviewed` tables are Dagbani, Ewe, Fante, Ga and Twi.

Both backends refuse a language whose table is a draft. The error is `UnsupportedLanguageError`, and its message names the table, its `confidence` value and the africa-g2p version. To use draft tables, build the backend with `allow_draft_rules=True`:

```python
from scriptconv.phonemizers import Phonemizer, get_phonemizer

get_phonemizer(Phonemizer.AFRICA_G2P, allow_draft_rules=True).phonemize_string("Akwaaba", "twi")
```

`supported_langs()` lists only the chart tables. `supported_langs(allow_draft_rules=True)` lists all of them.

## Licence

The package holds files under several licences. The SPDX expression is `Apache-2.0 AND MIT AND CC-BY-NC-4.0 AND LicenseRef-AfricaG2P-Data`.

| Files | Licence | Notice |
| --- | --- | --- |
| `scriptconv_nonfree/phonemizers/_vendored/mantoq/buck/phonetise_buckwalter.py` | CC-BY-NC-4.0 | `LICENSE.md` and `LICENSE.cc-by-nc-4.0` in `_vendored/mantoq/`. Upstream: nawarhalabi/Arabic-Phonetiser. |
| `scriptconv_nonfree/phonemizers/_vendored/mantoq/num2words.py` | Apache-2.0 | `LICENSE`. Written for scriptconv on top of ovos-number-parser. |
| every other file in `scriptconv_nonfree/phonemizers/_vendored/mantoq/` | MIT | `LICENSE.mantoq` in that directory. Upstream: mush42/mantoq. |
| `scriptconv_nonfree/phonemizers/_vendored/iqra_phonetiser/` | CC-BY-NC-4.0 | `LICENSE.md` and `LICENSE.cc-by-nc-4.0` in that directory. Upstream: Iqra-Eval/MSA_phonetiser, a fork of Arabic-Phonetiser. |
| every other file | Apache-2.0 | `LICENSE` |

`LicenseRef-AfricaG2P-Data` is the language data of the installed africa-g2p distribution, which the `africa` and `ghana` backends load. This package holds no copy of it. The code of africa-g2p is Apache-2.0, but its rule tables have no licence grant. `LICENSE.africa-g2p-data.md` states the terms and quotes the upstream data notice.

The CC-BY-NC-4.0 files and the africa-g2p data are not for commercial use. The dependencies of each backend keep their own licences.
