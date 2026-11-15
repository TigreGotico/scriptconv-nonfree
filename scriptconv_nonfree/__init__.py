"""scriptconv phonemizer backends that cannot ship in the Apache-2.0 scriptconv wheel.

scriptconv imports the backend classes from ``scriptconv_nonfree.phonemizers``
lazily, when a caller asks for one. Nothing here is imported at package
import time.
"""
