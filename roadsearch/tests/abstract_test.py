import unittest
from abc import ABC
import numpy as np


def euclid_dist(p, q):
    return np.sqrt((p[0] - q[0])**2 + (q[1] - p[1])**2)


def road_length(road):
    return sum([euclid_dist(road[i-1], road[i]) for i in range(1, len(road))])


class AbstractTest(unittest.TestCase, ABC):

    def check_elements(self, example, tuple):
        for elem in example:
            if tuple:
                self.assertEqual(len(elem), 2)
            else:
                self.assertEqual(float, type(elem))

    def size_decreases_until_minimum_allowed(self, length, min_length, example, function, is_tuple=False):
        self.assertEqual(len(example), length)
        for x in range(10):
            if len(example) < min_length:
                self.assertRaises(AssertionError, function, example)
            else:
                example = function(example)
                self.assertTrue(length - 5 <= len(example) < length or length == min_length)
                length = len(example)
                self.check_elements(example, is_tuple)


    def size_does_not_change(self, length, example, function, is_tuple=False):
        self.assertEqual(len(example), length)
        for x in range(10):
            example = function(example)
            self.assertEqual(length, len(example))
            self.check_elements(example, is_tuple)

