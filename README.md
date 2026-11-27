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

The backends are `mantoq`, `halabi` and `iqra` (extra `ar-phonemizers`),
`viphoneme` (`vi`), `africa_g2p` (`africa`) and `ghana_g2p` (`ghana`).
scriptconv never picks one of them by default.

## Licence

The package is `Apache-2.0 AND MIT AND CC-BY-NC-4.0 AND LicenseRef-AfricaG2P-Data`.
Its own glue code is Apache-2.0. The vendored mantoq code is MIT, except the
phonetiser and `num2words.py`. The two vendored copies of the Arabic phonetiser are
CC-BY-NC-4.0, which forbids commercial use. `LICENSE.africa-g2p-data.md`
states the terms of the africa-g2p rule tables, which the `africa` and `ghana`
backends load: they are not for commercial use. [Licences](docs/licences.md)
gives the restricted item of each backend and the licence of each file.

## Documentation

| Page | Read it for |
| --- | --- |
| [docs/getting-started.md](docs/getting-started.md) | install, the alphabets, the draft rule tables |
| [docs/how-it-works.md](docs/how-it-works.md) | how scriptconv finds and imports these backends |
| [docs/backends.md](docs/backends.md) | the languages, alphabets and parameters of each backend |
| [docs/licences.md](docs/licences.md) | the restricted item of each backend, the licence of each file |
| [docs/index.md](docs/index.md) | every page in reading order |
