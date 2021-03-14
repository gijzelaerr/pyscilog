from pyscilog import init
from unittest import TestCase


class TestPyscilog(TestCase):
    def test_init(self):
        init('test')
