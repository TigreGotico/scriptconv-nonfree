# Backend reference

<!-- agent-hint
covers: every backend of this package with its Phonemizer value, class, module, scriptconv extra, languages, alphabets, parameters, licence and downloads
source: scriptconv_nonfree/phonemizers/*.py, pyproject.toml, scriptconv/phonemizers/registry.py in scriptconv
generated: no
verify: python -m doctest docs/backends.md && python -c "import re,sys; from scriptconv.phonemizers.registry import PHONEMIZER_REGISTRY as R; rows={(v,(m,c,e)) for v,c,m,e in re.findall(r'^\| \`(\w+)\` \| \`(\w+)\` \| \`([\w.]+)\` \| \`([\w-]+)\` \|', open('docs/backends.md').read(), re.M)}; want={(p.value,t) for p,t in R.items() if t[0].startswith('scriptconv_nonfree.')}; sys.exit(rows!=want)"
see: docs/licences.md, docs/phonemizers.md in scriptconv
-->

This page lists every backend that scriptconv-nonfree holds. For each one it
gives the extra to install, the languages, the alphabets, the parameters and
the restricted item that puts it in this package.

## The table

Install a backend with its scriptconv extra, for example
`uv pip install --prerelease=allow "scriptconv[ghana]"`. The scriptconv extra
installs this package with the extra of the same name, which holds the
dependencies of the backend.

| `Phonemizer` value | Class | Module | scriptconv extra | Languages |
| --- | --- | --- | --- | --- |
| `mantoq` | `MantoqPhonemizer` | `scriptconv_nonfree.phonemizers.ar` | `ar-phonemizers` | `ar` |
| `halabi` | `HalabiPhonemizer` | `scriptconv_nonfree.phonemizers.ar` | `ar-phonemizers` | `ar` |
| `iqra` | `IqraPhonemizer` | `scriptconv_nonfree.phonemizers.ar` | `ar-phonemizers` | `ar` |
| `viphoneme` | `VIPhonemePhonemizer` | `scriptconv_nonfree.phonemizers.vi` | `vi` | `vi` |
| `africa_g2p` | `AfricaG2PPhonemizer` | `scriptconv_nonfree.phonemizers.africa` | `africa` | the rule tables of africa-g2p, by ISO 639-3 code |
| `ghana_g2p` | `GhanaG2PPhonemizer` | `scriptconv_nonfree.phonemizers.ghana` | `ghana` | the 42 languages of ghana-g2p |

No backend of this package downloads a file. The Arabic phonetisers are in
this package, and africa-g2p and ghana-g2p hold their rule tables in their
wheels.

## Three Arabic backends on one phonetiser

`mantoq`, `halabi` and `iqra` run the Arabic-Phonetiser of Nawar Halabi at
three points:

| Backend | Input | Native output (`Alphabet.HALABI`) |
| --- | --- | --- |
| `mantoq` | Arabic text; digits become words | the mantoq tokens that published mantoq models read |
| `halabi` | fully diacritized Arabic text | the raw phonetiser output, with the vowel digits and `+` between words |
| `iqra` | fully diacritized Arabic text | the `phoneme_ref` notation of the IqraEval shared task |

All three read the diacritics that the text carries and add none, so run a
diacritizer first. `Alphabet.IPA`, the default of `get_phonemizer`, converts
the native output with `scriptconv.notation`:

```python
>>> from scriptconv.phonemizers import Alphabet, Phonemizer, get_phonemizer
>>> text = "مَرْحَبًا بِالْعَالَمِ"
>>> for member in (Phonemizer.MANTOQ, Phonemizer.HALABI, Phonemizer.IQRA):
...     print(member.value, get_phonemizer(member, alphabet=Alphabet.HALABI).phonemize_string(text, "ar"))
mantoq marHabanaa bilEaalami
halabi m a r H a b a n aa + b i0 l E aa l a m i0
iqra m a r H a b aa b i l E aa l a m
>>> for member in (Phonemizer.MANTOQ, Phonemizer.HALABI, Phonemizer.IQRA):
...     print(member.value, get_phonemizer(member).phonemize_string(text, "ar"))
mantoq marħabanaː bilʕaːlami
halabi m a r ħ a b a n aː b i l ʕ aː l a m i
iqra marħabaːbilʕaːlam

```

All three write the letter ث as `^`, which `Alphabet.IPA` gives as `θ`.

### mantoq

`MantoqPhonemizer` runs the pipeline of mantoq (github.com/mush42/mantoq):
it writes digits as Arabic words with ovos-number-parser, then runs the
phonetiser and the mantoq tokenizer. It uses an installed `mantoq`
distribution when there is one, and the copy in
`scriptconv_nonfree/phonemizers/_vendored/mantoq` when there is not. The copy
has no diacritizer.

The class default is `Alphabet.BUCKWALTER`, a historical name for the mantoq
tokens. `Alphabet.HALABI` gives the same string, and `Alphabet.IPA` converts
it.

### halabi

`HalabiPhonemizer` calls the phonetiser directly, with no step before it. It
takes `Alphabet.HALABI`, the class default, or `Alphabet.IPA`. The native
output keeps the vowel digits (`i0`, `u1`), the vowels of an emphatic context
in upper case, and `+` between words.

### iqra

`IqraPhonemizer` runs the phonetiser of the IqraEval shared task
(Iqra-Eval/MSA_phonetiser), a fork of the phonetiser with its own changes,
from the copy in `scriptconv_nonfree/phonemizers/_vendored/iqra_phonetiser`.
Before the phonetiser, it applies four rules to the text:

1. It drops the tanwīn everywhere.
2. It drops the silent alif after the plural wāw (wāw al-jamāʿah).
3. It reads an utterance-initial definite article `ال` with a hamza and
   fatḥa.
4. It drops the final short vowel of the last word of each phrase (waqf).

It takes `Alphabet.HALABI`, the class default, or `Alphabet.IPA`. The native
output has a space between the phonemes, no vowel digits and no word marks.

Licence of the three backends: the phonetiser is CC-BY-NC-4.0, which forbids
commercial use. The other mantoq files are MIT.

## viphoneme

`VIPhonemePhonemizer` is Vietnamese G2P through viphoneme
(github.com/v-nhandt21/Viphoneme). The output is IPA with a tone digit after
each syllable:

```python
>>> from scriptconv.phonemizers import Phonemizer, get_phonemizer
>>> get_phonemizer(Phonemizer.VIPHONEME).phonemize_string("Xin chào các bạn", "vi")
'sin1 caw2 kak5 ban6 . '

```

viphoneme depends on vinorm, which imports the `imp` module that Python 3.12
removed. So the backend runs on Python 3.11 only, and the `vi` extra installs
nothing on Python 3.12 and later.

Licence: viphoneme and vinorm state "Free for non-commercial use" in their
PyPI metadata, with the licence name `AILAB`.

## africa_g2p

`AfricaG2PPhonemizer` wraps the rule-based G2P of africa-g2p
(AfriSpeech/africa-g2p), with one rule table for each language. It takes
`Alphabet.IPA`, the default, or `Alphabet.AFRICA_G2P`, the phoneme units of
the language's own spelling:

```python
>>> from scriptconv.phonemizers import Alphabet, Phonemizer, get_phonemizer
>>> get_phonemizer(Phonemizer.AFRICA_G2P).phonemize_string("akwaaba", "twi")
'a kʷ a a b a'
>>> get_phonemizer(Phonemizer.AFRICA_G2P, alphabet=Alphabet.AFRICA_G2P).phonemize_string("akwaaba", "twi")
'a kw a a b a'

```

Each rule table has a `confidence` field. The backend serves the tables whose
value is in `SERVED_CONFIDENCE`: `omniglot`, `high`, `medium` and
`hand-verified` name an Omniglot chart or Hartell (ed.), *Alphabets of
Africa* (UNESCO, 1993), and `tts-reviewed` is such a chart with corrections
that an LLM proposed. Every other value is a draft, for example `llm-draft`.
The backend refuses a draft table with `UnsupportedLanguageError` unless you
build it with `allow_draft_rules=True`. With africa-g2p 0.3.5:

```python
>>> from scriptconv_nonfree.phonemizers.africa import AfricaG2PPhonemizer, draft_status
>>> len(AfricaG2PPhonemizer.supported_langs()), len(AfricaG2PPhonemizer.supported_langs(allow_draft_rules=True))
(398, 750)
>>> draft_status("aab"), draft_status("twi")
('llm-draft', None)

```

The five `tts-reviewed` tables are Dagbani (`dag`), Ewe (`ewe`), Fante
(`fat`), Ga (`gaa`) and Twi (`twi`). No native speaker has checked their
corrections.

`get_lang` looks up the whole tag in lower case, then the tag with `_` read as
`-`, then the primary subtag (`twi-GH` gives `twi`). It does not fuzz the
match. Eleven tables carry a region in their name, for example `hau-nigeria`,
and a bare code never resolves to one of them: `hau` resolves only to the
draft table `hau`.

The module also exports `draft_status(table)`, which gives the `confidence`
of a draft table or `None`, and `refuse_draft(table, target_lang, backend)`,
which raises for a draft table.

Licence: the code of africa-g2p is Apache-2.0, but its rule tables have no
licence grant and are not for commercial use. See
[Licences](licences.md#the-africa-g2p-data).

## ghana_g2p

`GhanaG2PPhonemizer` wraps ghana-g2p (GhanaNLP/ghana-g2p), which builds on the
rule tables of africa-g2p for 42 Ghanaian languages. It normalises look-alike
code points, patches missing letters, and borrows a related rule set for a
language that africa-g2p lacks. It loads the same installed africa-g2p as
`africa_g2p`. The alphabets are the same as for `africa_g2p`:

```python
>>> from scriptconv.phonemizers import Phonemizer, get_phonemizer
>>> get_phonemizer(Phonemizer.GHANA_G2P).phonemize_string("akwaaba", "twi")
'a kʷ a a b a'
>>> get_phonemizer(Phonemizer.GHANA_G2P).get_lang("twi-GH")
'twi'

```

`get_lang` matches only the primary subtag, exactly, and does not map ISO
639-1 codes: `ee` is not `ewe`. A language whose africa-g2p table is a draft
is refused unless you pass `allow_draft_rules=True`. All 42 languages of
ghana-g2p 0.1.1 are served by default.

Licence: ghana-g2p is Apache-2.0, but it loads the rule tables of africa-g2p,
which have no licence grant.

---

[Index](index.md) · Previous: [How it works](how-it-works.md) · Next: [Licences](licences.md)
