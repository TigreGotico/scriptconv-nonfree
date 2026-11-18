"""Long digit runs through the mantoq number step.

The Arabic number tables reach تريليون, 10**12, so 15 digits is the largest run
they speak as one quantity. A longer run is read digit by digit: no speaker
reads 20000 digits as one number, and ``int()`` refuses a run over 4300 digits
outright, which turned any long run into a crash.
"""
import time
import unittest
from importlib import import_module

from scriptconv_nonfree.phonemizers import ar as ar_phonemizers

# the module itself, not the function the package re-exports under the same name
numbers = import_module(
    "scriptconv_nonfree.phonemizers._vendored.mantoq.num2words")

MAX_QUANTITY_DIGITS = 15  # 10**15 - 1, the reach of تريليون, 10**12
DECIMAL_SEPARATOR_WORD = "فاصلة"

# num2words() output recorded from the code before a long run was read digit by
# digit: the largest number the tables speak as one quantity, plus common ones.
UNCHANGED = {
    "9" * MAX_QUANTITY_DIGITS: (
        "تسعمئة وتسعة وتسعون تريليون وتسعمئة وتسعة وتسعون مليار وتسعمئة "
        "وتسعة وتسعون مليون وتسعمئة وتسعة وتسعون ألف وتسعمئة وتسعة وتسعون"),
    "2026": "ألفان وستة وعشرون",
    "3.5": "ثلاثة فاصلة خمسة",
    "100": "مئة",
}

# A digit run one digit over what the tables speak as one quantity.
OVER_THE_CAP = "1234567890123456"


def digit_by_digit(digits: str) -> str:
    """A digit run as the single-digit readings num2words itself gives."""
    return " ".join(numbers.num2words(digit) for digit in digits)


def phonemize(text: str):
    phonemizer = ar_phonemizers.MantoqPhonemizer()
    started = time.monotonic()
    out = phonemizer.phonemize(text, "ar")
    return out, time.monotonic() - started


class TestLongDigitRuns(unittest.TestCase):
    def test_4301_digit_run_phonemizes(self):
        out, elapsed = phonemize("7" * 4301)
        self.assertTrue(out)
        self.assertLess(elapsed, 5.0, "4301 digits took %.1fs" % elapsed)

    def test_20000_digit_run_phonemizes(self):
        out, elapsed = phonemize("7" * 20000)
        self.assertTrue(out)
        self.assertLess(elapsed, 5.0, "20000 digits took %.1fs" % elapsed)

    def test_one_digit_over_the_cap_reads_digit_by_digit(self):
        self.assertEqual(len(OVER_THE_CAP), MAX_QUANTITY_DIGITS + 1)
        self.assertEqual(numbers.num2words(OVER_THE_CAP),
                         digit_by_digit(OVER_THE_CAP))

    def test_overlong_integer_part_of_a_decimal(self):
        digits = "8" * 5000
        expected = digit_by_digit(digits) + " " + DECIMAL_SEPARATOR_WORD + \
            " " + digit_by_digit("25")
        self.assertEqual(numbers.num2words(digits + ".25"), expected)

    def test_runs_within_the_cap_keep_their_output(self):
        for number, expected in UNCHANGED.items():
            self.assertEqual(numbers.num2words(number), expected, number)

    def test_the_number_step_uses_the_cap_the_tests_assume(self):
        self.assertEqual(getattr(numbers, "MAX_QUANTITY_DIGITS", None),
                         MAX_QUANTITY_DIGITS)


if __name__ == "__main__":
    unittest.main()
