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
| `africa_g2p` | `AfricaG2PPhonemizer` | `scriptconv_nonfree.phonemizers.africa` | the vendored africa-g2p language data, which has no licence grant |
| `ghana_g2p` | `GhanaG2PPhonemizer` | `scriptconv_nonfree.phonemizers.ghana` | the africa-g2p language data that ghana-g2p loads |

Each backend's own dependencies install with the extra of the same name, for example `pip install scriptconv-nonfree[vi]`.

## Licence

The package holds files under several licences. The SPDX expression is `Apache-2.0 AND MIT AND CC-BY-NC-4.0 AND LicenseRef-AfricaG2P-Data`.

| Files | Licence | Notice |
| --- | --- | --- |
| `scriptconv_nonfree/phonemizers/_vendored/mantoq/buck/phonetise_buckwalter.py` | CC-BY-NC-4.0 | `LICENSE.md` and `LICENSE.cc-by-nc-4.0` in `_vendored/mantoq/`. Upstream: nawarhalabi/Arabic-Phonetiser. |
| `scriptconv_nonfree/phonemizers/_vendored/mantoq/num2words.py` | Apache-2.0 | `LICENSE`. Written for scriptconv on top of ovos-number-parser. |
| every other file in `scriptconv_nonfree/phonemizers/_vendored/mantoq/` | MIT | `LICENSE.mantoq` in that directory. Upstream: mush42/mantoq. |
| `scriptconv_nonfree/phonemizers/_vendored/iqra_phonetiser/` | CC-BY-NC-4.0 | `LICENSE.md` and `LICENSE.cc-by-nc-4.0` in that directory. Upstream: Iqra-Eval/MSA_phonetiser, a fork of Arabic-Phonetiser. |
| `scriptconv_nonfree/phonemizers/_vendored/africa_g2p/` code (`*.py`) | Apache-2.0 | `LICENSE`. Upstream AfriSpeech/africa-g2p declares Apache-2.0 in its `pyproject.toml`. |
| `scriptconv_nonfree/phonemizers/_vendored/africa_g2p/languages/*.json`, `data/*.json` | `LicenseRef-AfricaG2P-Data`: no licence grant | `DATA_LICENSE.md` and `LICENSE.md` in that directory |
| every other file | Apache-2.0 | `LICENSE` |

The CC-BY-NC-4.0 files and the africa-g2p data are not for commercial use. The dependencies of each backend keep their own licences.
