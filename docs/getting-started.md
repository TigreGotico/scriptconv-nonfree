# Getting started

<!-- agent-hint
covers: install a non-free backend through its scriptconv extra, phonemize Arabic and an African language, see which engine ran, and use the draft rule tables
source: pyproject.toml, scriptconv_nonfree/phonemizers/ar.py:MantoqPhonemizer, scriptconv_nonfree/phonemizers/africa.py:AfricaG2PPhonemizer
generated: no
verify: python -m doctest docs/getting-started.md
see: docs/how-it-works.md, docs/backends.md
-->

This page installs two backends of scriptconv-nonfree, phonemizes text with
each one, and shows which engine gave the phonemes. Each step shows the real
output. The backends are not for commercial use: read
[Licences](licences.md) first.

## 1. Install the backends

Install scriptconv with the extras of the backends. Each extra installs
scriptconv-nonfree and the dependencies of its backends:

```bash
uv pip install --prerelease=allow "scriptconv[ar-phonemizers,africa]"
```

`ar-phonemizers` gives the Arabic backends `mantoq`, `halabi` and `iqra`, and
also arbtok, the Arabic default of scriptconv. `africa` gives `africa_g2p` and
installs africa-g2p.

## 2. Phonemize Arabic

Ask the scriptconv registry for a backend by its `Phonemizer` value. Then give
the text and its language:

```python
>>> from scriptconv.phonemizers import Phonemizer, get_phonemizer
>>> mantoq = get_phonemizer(Phonemizer.MANTOQ)
>>> mantoq.phonemize_string("مَرْحَبًا بِالْعَالَمِ", "ar")
'marħabanaː bilʕaːlami'
>>> type(mantoq).__module__
'scriptconv_nonfree.phonemizers.ar'

```

mantoq reads the diacritics that the text carries and adds none. Text without
diacritics gives consonants without short vowels:

```python
>>> from scriptconv.phonemizers import Phonemizer, get_phonemizer
>>> get_phonemizer(Phonemizer.MANTOQ).phonemize_string("السلام عليكم", "ar")
'aːlslaːm ʕlikm'

```

Run a diacritizer before mantoq, for example the diacritize stage of
scriptconv.

## 3. Choose the alphabet

`get_phonemizer` asks for IPA by default. `Alphabet.HALABI` gives the native
notation of the Halabi phonetiser, which published mantoq models read:

```python
>>> from scriptconv.phonemizers import Alphabet, Phonemizer, get_phonemizer
>>> get_phonemizer(Phonemizer.MANTOQ, alphabet=Alphabet.HALABI).phonemize_string("مَرْحَبًا بِالْعَالَمِ", "ar")
'marHabanaa bilEaalami'

```

## 4. See which engine ran

`identity(lang)` names the engine and its version. mantoq runs the copy in
this package, so the distribution is `scriptconv-nonfree`:

```python
>>> from scriptconv.phonemizers import Phonemizer, get_phonemizer
>>> get_phonemizer(Phonemizer.MANTOQ).identity("ar").distribution
'scriptconv-nonfree'

```

## 5. Phonemize an African language

`africa_g2p` takes an ISO 639-3 code. The output puts a space between the
phonemes:

```python
>>> from scriptconv.phonemizers import Phonemizer, get_phonemizer
>>> africa = get_phonemizer(Phonemizer.AFRICA_G2P)
>>> africa.phonemize_string("akwaaba", "twi")
'a kʷ a a b a'
>>> africa.identity("twi").distribution
'africa-g2p'

```

## 6. Use a draft rule table

Each africa-g2p rule table records its source. The backend refuses a table
that an LLM drafted, and the error names the table and its `confidence`:

```python
>>> from scriptconv.phonemizers import Phonemizer, get_phonemizer
>>> get_phonemizer(Phonemizer.AFRICA_G2P).phonemize_string("aba", "aab")  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
scriptconv.phonemizers.base.UnsupportedLanguageError: africa-g2p: the africa-g2p ... rule table 'aab' for 'aab' has confidence 'llm-draft', so it is a draft. Pass allow_draft_rules=True to use it
>>> get_phonemizer(Phonemizer.AFRICA_G2P, allow_draft_rules=True).phonemize_string("aba", "aab")
'a b a'

```

## 7. A backend that is not installed

When the package of a backend is missing, `get_phonemizer` raises an
`ImportError` that names the scriptconv extra to install. This output comes
from a venv with scriptconv only:

```python
from scriptconv.phonemizers import Phonemizer, get_phonemizer

get_phonemizer(Phonemizer.MANTOQ)
# ImportError: phonemizer 'mantoq' needs a missing backing package — install with `pip install scriptconv[ar-phonemizers]`
```

## Next

[How it works](how-it-works.md) shows how scriptconv finds the classes of this
package. The [backend reference](backends.md) lists every backend with its
extra, languages and alphabets.

---

[Index](index.md) · Previous: [Index](index.md) · Next: [How it works](how-it-works.md)
