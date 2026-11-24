# Licences

<!-- agent-hint
covers: the non-commercial or missing licence of each backend, why it puts the backend here, and the licence of each file
source: pyproject.toml (license, license-files), LICENSE, LICENSE.africa-g2p-data.md, scriptconv_nonfree/phonemizers/_vendored/mantoq/LICENSE.md, scriptconv_nonfree/phonemizers/_vendored/iqra_phonetiser/LICENSE.md
generated: no
verify: python -c "import os,re,sys,tomllib; page=open('docs/licences.md').read(); spdx=tomllib.load(open('pyproject.toml','rb'))['project']['license']; b=chr(96); paths=re.findall(b+'(scriptconv_nonfree/[^'+b+']+|LICENSE[.]africa[^'+b+']*)'+b, page); sys.exit(not (b+spdx+b in page and paths and all(os.path.exists(p) for p in paths)))"
see: docs/backends.md, README.md in scriptconv
-->

This page states the licence that puts each backend in scriptconv-nonfree,
and the licence of each file in the package. It is a summary of the licence
files, not legal advice. In short: none of these backends is for commercial
use.

## Why this package exists

The scriptconv wheel holds only permissive code: Apache-2.0, MIT and the
CMUdict licence. Its extras pull no non-commercial distribution of their own,
as the scriptconv
[Licensing section](https://github.com/TigreGotico/scriptconv/blob/dev/README.md#licensing)
states.

A backend comes to this package when its code, its data or a dependency is for
non-commercial use only, or has no licence grant. scriptconv keeps the
`Phonemizer` value and the registry row, and its extra installs this package.

## The restricted item of each backend

The three Arabic backends run code in this package under CC-BY-NC-4.0:

| Backend | Code |
| --- | --- |
| `mantoq` | the phonetiser in `buck/phonetise_buckwalter.py` of the vendored mantoq, from Arabic-Phonetiser |
| `halabi` | the same phonetiser |
| `iqra` | the vendored IqraEval fork of the phonetiser |

The IqraEval fork carries no licence file of its own, so the CC-BY-NC-4.0
terms of Arabic-Phonetiser govern it. Each phonetiser copy runs only when a
caller asks for its backend: scriptconv never picks one by default.

The other backends are here because of a dependency or its data:

| Backend | Restricted item | Terms |
| --- | --- | --- |
| `viphoneme` | viphoneme and vinorm | "Free for non-commercial use", licence name `AILAB` |
| `africa_g2p` | the rule tables of africa-g2p | no licence grant |
| `ghana_g2p` | the same rule tables, which ghana-g2p loads | no licence grant |

## The africa-g2p data

The code of africa-g2p is Apache-2.0. Its rule tables
(`africa_g2p/languages/*.json` and `africa_g2p/data/*.json` in the installed
package) have no licence grant, and the africa-g2p wheel ships no licence
file.

The tables come from the charts of Omniglot (© Simon Ager) and from Hartell
(ed.), *Alphabets of Africa* (© UNESCO 1993). The draft tables name an LLM
draft from the text of AfriSpeech/africa-corpus, and the notice gives no terms
for them.

This package holds no copy of the tables. `LICENSE.africa-g2p-data.md` quotes
the upstream data notice and states the terms: the tables are not for
commercial use, and a redistribution keeps their attributions. The licence
expression of this package names that notice `LicenseRef-AfricaG2P-Data`.

## The files of this package

The SPDX expression of the package is
`Apache-2.0 AND MIT AND CC-BY-NC-4.0 AND LicenseRef-AfricaG2P-Data`.

| Files in `scriptconv_nonfree/phonemizers/_vendored/mantoq/` | Licence | Notice |
| --- | --- | --- |
| `scriptconv_nonfree/phonemizers/_vendored/mantoq/buck/phonetise_buckwalter.py` | CC-BY-NC-4.0 | `LICENSE.md` and `LICENSE.cc-by-nc-4.0`, from nawarhalabi/Arabic-Phonetiser |
| `scriptconv_nonfree/phonemizers/_vendored/mantoq/num2words.py` | Apache-2.0 | `LICENSE`, written for scriptconv on ovos-number-parser |
| every other file | MIT | `LICENSE.mantoq`, from mush42/mantoq |

| Other files | Licence | Notice |
| --- | --- | --- |
| `scriptconv_nonfree/phonemizers/_vendored/iqra_phonetiser/` | CC-BY-NC-4.0 | `LICENSE.md` and `LICENSE.cc-by-nc-4.0` in that directory, from Iqra-Eval/MSA_phonetiser |
| `LICENSE.africa-g2p-data.md` | the notice of the africa-g2p data | the file itself |
| every other file | Apache-2.0 | `LICENSE` |

The wheel carries the licence files that `license-files` in `pyproject.toml`
names.

---

[Index](index.md) · Previous: [Backend reference](backends.md) · Next: [Index](index.md)
