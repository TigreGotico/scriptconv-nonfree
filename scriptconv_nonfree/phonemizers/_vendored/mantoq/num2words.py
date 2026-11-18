"""Arabic number verbalization for the mantoq pipeline.

Digits are folded to ASCII (Arabic-Indic ٠-٩ and Extended Arabic-Indic ۰-۹
forms included) and verbalized with ``ovos_number_parser``'s Arabic locale.
Number words are emitted undiacritized; the tashkeel step upstream of g2p
diacritizes them together with the rest of the sentence.
"""
import re
from functools import partial

NUM_REGEX = re.compile(r"\d+(?:\.\d+)?")
PERCENT_NO_DIAC = "بالمئة"

# The longest digit run that is still one quantity the Arabic number tables
# speak with their own scale words: the top entry of ``_SCALES_AR`` is
# تريليون, 10**12 (``ovos_number_parser/numbers_ar.py``), so 15 digits
# (10**15 - 1) is the largest value they compose. Beyond it the tables recycle
# their scale words ("ألف تريليون"), and no speaker reads such a run as one
# quantity: it is read digit by digit, each digit with its own word.
MAX_QUANTITY_DIGITS = 15
# The word pronounce_number puts between the parts of a decimal (فاصلة).
DECIMAL_SEPARATOR_WORD = "فاصلة"

# Arabic-Indic (U+0660-0669) and Extended Arabic-Indic (U+06F0-06F9) -> ASCII
_DIGIT_TABLE = {0x0660 + i: str(i) for i in range(10)}
_DIGIT_TABLE.update({0x06F0 + i: str(i) for i in range(10)})
# Arabic decimal / thousands separators used with Arabic-Indic digits
_DIGIT_TABLE[0x066B] = "."   # ARABIC DECIMAL SEPARATOR
_DIGIT_TABLE[0x066C] = ""    # ARABIC THOUSANDS SEPARATOR


def normalize_digits(text: str) -> str:
    """Fold Arabic-Indic digit glyphs and numeric separators to ASCII forms."""
    return text.translate(_DIGIT_TABLE)


def _read_digit_by_digit(digits: str) -> str:
    """Read a digit run as separate digits, one number word each."""
    from ovos_number_parser import pronounce_number
    return " ".join(pronounce_number(int(digit), lang="ar")
                    for digit in digits)


def _convert_num2words(m: re.Match, *, apply_tashkeel):
    from ovos_number_parser import pronounce_number
    number = m.group(0)
    whole, _, fraction = number.partition(".")
    if len(whole) > MAX_QUANTITY_DIGITS:
        # Too long to be one quantity. ``int()`` would also refuse a run over
        # its own string-conversion limit, so the digits are read one by one.
        words = _read_digit_by_digit(whole)
        if fraction:
            words += " " + DECIMAL_SEPARATOR_WORD + " " + \
                _read_digit_by_digit(fraction)
        return words
    value = float(number) if fraction else int(number)
    return pronounce_number(value, lang="ar")


def num2words(text: str, handle_percent=True, apply_tashkeel: bool = True) -> str:
    """
    Converts numbers in `text` to Arabic words.
    Simple conversion. Does not check if the number is date/currency...etc.

    Args:
        text: input text that may contain numbers
        apply_tashkeel: kept for API compatibility; number words are always
            emitted undiacritized and picked up by the sentence-level
            tashkeel step.
    """
    text = normalize_digits(text)
    output = NUM_REGEX.sub(
        partial(_convert_num2words, apply_tashkeel=apply_tashkeel), text
    )
    if handle_percent:
        output = output.replace("%", f" {PERCENT_NO_DIAC}")
    return re.sub(r"\s+", " ", output).strip()
