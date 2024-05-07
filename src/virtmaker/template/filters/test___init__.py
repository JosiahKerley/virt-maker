from unittest import TestCase
from . import filter_random_word, filter_random_hostname


class Test(TestCase):
    def test_filter_random_word(self):
        max_length = 100
        min_length = 1
        word = filter_random_word(max_length=max_length, min_length=min_length)
        assert isinstance(word, str)
        assert len(word) <= max_length
        assert len(word) >= min_length

    def test_filter_random_hostname(self):
        for _ in range(32):
            hostname = filter_random_hostname()
            assert isinstance(hostname, str)
            assert len(hostname) <= 16
            assert len(hostname) >= 9
