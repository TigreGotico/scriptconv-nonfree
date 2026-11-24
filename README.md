# scriptconv-nonfree

<!-- agent-hint
covers: what scriptconv-nonfree is, the quickstart, the backends it holds and its licence
source: pyproject.toml, scriptconv_nonfree/phonemizers/, LICENSE.africa-g2p-data.md, scriptconv/phonemizers/registry.py in scriptconv
generated: no
verify: python -m doctest README.md
see: docs/index.md, docs/getting-started.md, AGENTS.md
-->

scriptconv-nonfree holds the phonemizer backends of
[scriptconv](https://github.com/TigreGotico/scriptconv) whose code, data or
dependencies are for non-commercial use only, or carry no licence grant.
scriptconv keeps the registry, and its extras install this package, so you
call the backends through scriptconv as usual. Do not use them in a commercial
product.

## Quickstart

```bash
uv pip install --prerelease=allow "scriptconv[ar-phonemizers]"
```

```python
>>> from scriptconv.phonemizers import Phonemizer, get_phonemizer
>>> get_phonemizer(Phonemizer.MANTOQ).phonemize_string("مَرْحَبًا بِالْعَالَمِ", "ar")
'marħabanaː bilʕaːlami'

```

mantoq reads the diacritics of the text and adds none.
[Getting started](docs/getting-started.md) walks through the alphabets, the
African backends and the draft rule tables.

## Backends

| `Phonemizer` values | scriptconv extra | Restricted item |
| --- | --- | --- |
| `mantoq`, `halabi`, `iqra` | `ar-phonemizers` | the Arabic-Phonetiser of Nawar Halabi, CC-BY-NC-4.0 |
| `viphoneme` | `vi` | viphoneme and vinorm, "Free for non-commercial use" |
| `africa_g2p` | `africa` | the africa-g2p rule tables, with no licence grant |
| `ghana_g2p` | `ghana` | the same rule tables, which ghana-g2p loads |

scriptconv never picks one of these backends by default: the Arabic default
is arbtok. The [backend reference](docs/backends.md) gives the languages,
alphabets and parameters of each backend.

## Licence

The package is `Apache-2.0 AND MIT AND CC-BY-NC-4.0 AND LicenseRef-AfricaG2P-Data`.
Its own glue code is Apache-2.0. The vendored mantoq code is MIT, except the
phonetiser and `num2words.py`. The two vendored copies of the Arabic phonetiser are
CC-BY-NC-4.0, which forbids commercial use. `LICENSE.africa-g2p-data.md`
states the terms of the africa-g2p rule tables, which the `africa` and `ghana`
backends load: they are not for commercial use. [Licences](docs/licences.md)
gives the restricted item of each backend and the licence of each file.

## Documentation

The [documentation index](docs/index.md) lists every page in reading order.
The [scriptconv documentation](https://github.com/TigreGotico/scriptconv/tree/dev/docs)
explains the phonemizer contract and the other backends.
