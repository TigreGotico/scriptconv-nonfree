"""Phonemizer wrappers moved out of scriptconv for non-commercial or unlicensed parts.

Each module mirrors the scriptconv module it came from
(``scriptconv.phonemizers.ar``, ``.vi``, ``.africa``, ``.ghana``). The
classes subclass :class:`scriptconv.phonemizers.base.BasePhonemizer`, and
scriptconv's registry imports them lazily.
"""
