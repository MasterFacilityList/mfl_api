"""
This file will be removed once apps starts coming  in.
"""

from django.test import TestCase


class SampleTest(TestCase):
    def test_fake(self):
        ans = 1+1
        self.assertEquals(2, ans)
