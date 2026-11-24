# How scriptconv finds these backends

<!-- agent-hint
covers: how scriptconv finds, imports and reports the classes of this package, and why it never picks them by default
source: scriptconv/phonemizers/registry.py and scriptconv/phonemizers/_moved.py in scriptconv, scriptconv_nonfree/__init__.py, scriptconv_nonfree/phonemizers/__init__.py, scriptconv_nonfree/phonemizers/ar.py
generated: no
verify: python -m doctest docs/how-it-works.md
see: docs/backends.md, docs/phonemizers.md in scriptconv
-->

This page explains how a `Phonemizer` value in scriptconv reaches a class in
scriptconv-nonfree. This package registers nothing itself: scriptconv holds
the registry, and this package holds the classes.

## The registry row

`PHONEMIZER_REGISTRY` in `scriptconv.phonemizers.registry` maps each
`Phonemizer` member to three strings: the module, the class name, and the
scriptconv extra that installs the class. For a backend of this package, the
module starts with `scriptconv_nonfree.`:

```python
>>> import sys
>>> import scriptconv.phonemizers
>>> "scriptconv_nonfree" in sys.modules
False
>>> from scriptconv.phonemizers import Phonemizer
>>> from scriptconv.phonemizers.registry import PHONEMIZER_REGISTRY
>>> PHONEMIZER_REGISTRY[Phonemizer.MANTOQ]
('scriptconv_nonfree.phonemizers.ar', 'MantoqPhonemizer', 'ar-phonemizers')

```

The first check shows that `import scriptconv` does not import this package.
These 6 members resolve to this package:

```python
>>> from scriptconv.phonemizers.registry import PHONEMIZER_REGISTRY
>>> [m.value for m, (module, _, _) in PHONEMIZER_REGISTRY.items()
...  if module.startswith("scriptconv_nonfree.")]
['viphoneme', 'africa_g2p', 'ghana_g2p', 'mantoq', 'halabi', 'iqra']

```

## The import on first use

`get_phonemizer_class(member)` imports the module of the row and returns the
class. `get_phonemizer(member, alphabet, model, **kwargs)` does the same, then
builds an instance:

- It gives `alphabet` to the constructor when the constructor has an
  `alphabet` parameter. The default is `Alphabet.IPA`. So `mantoq` gives IPA
  through `get_phonemizer`, although the class default is
  `Alphabet.BUCKWALTER`.
- It gives the other keyword arguments to the constructor, for example
  `allow_draft_rules=True` for `africa_g2p` and `ghana_g2p`.
- No backend of this package takes a `model`.

When the import fails, `get_phonemizer` raises an `ImportError` that names the
scriptconv extra of the row:

```python
from scriptconv.phonemizers import Phonemizer, get_phonemizer

get_phonemizer(Phonemizer.MANTOQ)
# ImportError: phonemizer 'mantoq' needs a missing backing package — install with `pip install scriptconv[ar-phonemizers]`
```

Each class also imports its engine on first use. When the engine is missing,
the class raises an `ImportError` with an install command.

## No language default

`phonemizer_for_lang(lang)` picks a backend when the caller names none. It
never picks a backend of this package, so a caller uses one only by its
`Phonemizer` value. The Arabic default is arbtok, and Arabic never falls back
to another backend:

```python
>>> from scriptconv.phonemizers.registry import LANG_DEFAULTS, PHONEMIZER_REGISTRY
>>> [m.value for m in LANG_DEFAULTS["ar"]]
['arbtok']
>>> [m.value for chain in LANG_DEFAULTS.values() for m in chain
...  if PHONEMIZER_REGISTRY[m][0].startswith("scriptconv_nonfree.")]
[]

```

## Deprecated import paths in scriptconv

scriptconv also gives each class of this package at a deprecated path in
scriptconv, for example `scriptconv.phonemizers.ar.MantoqPhonemizer`. The first use
of such a path warns with a `DeprecationWarning`:

```python
from scriptconv.phonemizers.ar import MantoqPhonemizer
# DeprecationWarning: scriptconv.phonemizers.ar.MantoqPhonemizer is deprecated and will be removed in scriptconv 0.1.0; import it from scriptconv_nonfree.phonemizers.ar (`pip install scriptconv[ar-phonemizers]`)
```

`scriptconv.phonemizers._moved.REMOVAL_VERSION` names the scriptconv release
that removes these paths. Import from `scriptconv_nonfree.phonemizers` or call
`get_phonemizer`.

## The identity of a backend

`identity(lang)` returns the `Phonemizer` value, the distribution and the
version of the engine, the resolved language and a revision hash. The engine
is the distribution that gives the phonemes. When the engine is code inside
this package, the distribution is `scriptconv-nonfree`:

```python
>>> from scriptconv.phonemizers import Phonemizer, get_phonemizer
>>> get_phonemizer(Phonemizer.HALABI).identity("ar").distribution
'scriptconv-nonfree'
>>> get_phonemizer(Phonemizer.GHANA_G2P).identity("twi").distribution
'ghana-g2p'

```

`mantoq` reports `mantoq` when a separate `mantoq` distribution is installed,
because that distribution then runs in place of the copy in this package.
`halabi` also runs the phonetiser of an installed `mantoq` when there is one.
`iqra` always runs the copy in this package. The scriptconv
[phonemizer page](https://github.com/TigreGotico/scriptconv/blob/dev/docs/phonemizers.md)
explains the contract, the registry and the revision.

---

[Index](index.md) · Previous: [Getting started](getting-started.md) · Next: [Backend reference](backends.md)
