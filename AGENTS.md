# AGENTS.md

scriptconv-nonfree holds the scriptconv phonemizer backends whose code, data
or dependencies are for non-commercial use only, or carry no licence grant.
scriptconv keeps the `Phonemizer` values and the registry; this package holds
the classes that the registry imports on first use.

## Map

| Path | Holds |
|---|---|
| `scriptconv_nonfree/phonemizers/ar.py` | `mantoq`, `halabi` and `iqra`, and the IqraEval text rules |
| `scriptconv_nonfree/phonemizers/vi.py` | `viphoneme` |
| `scriptconv_nonfree/phonemizers/africa.py`, `ghana.py` | `africa_g2p` and `ghana_g2p`, and the draft-table rule |
| `scriptconv_nonfree/phonemizers/_vendored/mantoq/` | mantoq with the Halabi phonetiser (CC-BY-NC-4.0 and MIT) |
| `scriptconv_nonfree/phonemizers/_vendored/iqra_phonetiser/` | The IqraEval fork of the phonetiser (CC-BY-NC-4.0) |
| `LICENSE.africa-g2p-data.md` | The terms of the africa-g2p rule tables |
| `docs/` | The documentation. [docs/index.md](docs/index.md) gives the reading order |

## Setup and tests

```bash
uv venv -p 3.11
uv pip install --prerelease=allow -e '.[test]'
pytest tests/
```

CI runs the suite on Python 3.11, 3.12 and 3.13
(`.github/workflows/build-tests.yml`). The `vi` extra installs viphoneme on
Python 3.11 only, because vinorm imports the `imp` module that Python 3.12
removed.

## Rules that the code, the tests or the docs enforce

- scriptconv names each class by its module path and class name in
  `PHONEMIZER_REGISTRY`. Renaming or moving a class breaks scriptconv. See
  [docs/how-it-works.md](docs/how-it-works.md).
- `tests/conftest.py` points the scriptconv registry at the classes of this
  checkout. Keep its `MOVED` rows equal to the rows of scriptconv.
- Importing the package imports no backend. Each wrapper imports its engine
  on first use, and a missing engine raises an `ImportError` with an install
  command (`tests/test_phonemizers_friendly_import_errors.py`).
- `mantoq` keeps the output that published mantoq models read. The two
  phonetiser copies stay separate, because `iqra` follows the IqraEval
  reference and `mantoq` follows mantoq
  (`_vendored/iqra_phonetiser/LICENSE.md`).
- `africa_g2p` and `ghana_g2p` refuse a draft rule table unless the caller
  passes `allow_draft_rules=True`. `SERVED_CONFIDENCE` in `africa.py` lists the
  served values, and the tests pin the output of africa-g2p 0.3.5 and
  ghana-g2p 0.1.1. See [docs/backends.md](docs/backends.md).
- Each vendored file names its source and licence, and `license-files` in
  `pyproject.toml` lists each licence notice. See
  [docs/licences.md](docs/licences.md).
- The examples of each docs page give the output that the page shows. Run
  the `verify` command in the agent hint of the page.

## Before a push

```bash
pytest tests/
for page in README.md docs/*.md; do python -m doctest "$page" || echo "FAIL $page"; done
```

Run each page in its own process: the first example of
`docs/how-it-works.md` checks that nothing imported this package before it.
The `test` extra installs what the examples need. CI also runs ruff, which
reports only, and actionlint, which fails the job on a broken workflow file.
