# scriptconv-nonfree documentation

<!-- agent-hint
covers: the reading order of every page in docs/
source: the pages in docs/
generated: no
verify: diff <(ls docs/*.md | xargs -n1 basename | grep -v '^index.md$' | sort) <(grep -oE '^[0-9]+\. \*\*\[[a-z-]+\.md\]' docs/index.md | grep -oE '[a-z-]+\.md' | sort)
see: README.md, AGENTS.md
-->

This index lists every page in reading order. scriptconv-nonfree holds the
scriptconv phonemizer backends whose code, data or dependencies are for
non-commercial use only, or carry no licence grant. The pages explain how to
install them, how scriptconv finds them, what each one does, and which
licence each one carries.

1. **[getting-started.md](getting-started.md)**: install the backends
   through their scriptconv extras, phonemize Arabic and Twi, see which engine
   ran, and use a draft rule table.
2. **[how-it-works.md](how-it-works.md)**: the scriptconv registry rows that
   point to this package, the import on first use, why no backend here is a
   language default, the deprecated import paths, and `identity()`.
3. **[backends.md](backends.md)**: every backend with its extra, languages,
   alphabets, parameters and licence, and the three Arabic backends side by
   side.
4. **[licences.md](licences.md)**: the restricted item of each backend, the
   africa-g2p data, and the licence of each file in the package.

The [scriptconv documentation](https://github.com/TigreGotico/scriptconv/tree/dev/docs)
explains the phonemizer contract, the registry, the other backends and the
text frontend.

---

[Index](index.md) · Previous: [README](../README.md) · Next: [Getting started](getting-started.md)
