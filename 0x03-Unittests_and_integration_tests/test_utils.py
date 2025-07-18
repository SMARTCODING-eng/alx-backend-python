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

    Raises:
        KeyError: If any key in the path is not found, or if a non-dictionary
                  value is encountered before the end of the path.

    Example:
        >>> access_nested_map({"a": 1}, ("a",))
        1
        >>> access_nested_map({"a": {"b": 2}}, ("a", "b"))
        2
    """
    current = nested_map
    for i, key in enumerate(path):
        if not isinstance(current, dict):
            raise KeyError(f"Key '{key}' not found in the nested map under path {path[:i]}")
        try:
            current = current[key]
        except KeyError:
            if i == 0:
                raise KeyError(f"Key '{key}' not found in the nested map")
            else:
                raise KeyError(f"Key '{key}' not found in the nested map under path {path[:i]}")
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
        ({'a': {'b': 2}}, ("a", "c"), "Key 'c' not found in the nested map under path ('a',)"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """Test that KeyError is raised for invalid paths"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(expected_key, context.exception.args[0])


if __name__ == "__main__":
    unittest.main()