#!/usr/bin/env python3

import unittest
from parameterized import parameterized


def access_nested_map(nested_map, path):
    """
    Access a value in a nested dictionary using a sequence of keys.

    Args:
        nested_map (dict): The nested dictionary to access.
        path (tuple): A sequence of keys representing the path to the value.

    Returns:
        The value reached by following the path in the nested_map.

    Example:
        >>> access_nested_map({"a": 1}, ("a",))
        1
        >>> access_nested_map({"a": {"b": 2}}, ("a", "b"))
        2
    """
    current = nested_map
    for key in path:
        current = current[key]
    return current


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns the correct value for given inputs"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "Key 'a' not found in the nested map"),
        ({"a": 1}, ("a", "b"), "Key 'b' not found in the nested map under path ('a',)"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """Test that KeyError is raised for invalid paths"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertIn(expected_key, str(context.exception))


if __name__ == "__main__":
    unittest.main()