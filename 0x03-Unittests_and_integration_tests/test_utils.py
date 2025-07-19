#!/usr/bin/env python3

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
import requests
from functools import wraps
from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
)

__all__ = [
    "access_nested_map",
    "get_json",
    "memoize",
]

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
    for key in path:
        if not isinstance(nested_map, Mapping):
            raise KeyError(key)
        nested_map = nested_map[key]
    return nested_map

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a"), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map 
        returns the correct value for given inputs"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a"), "a"),    
        ({"a": 1}, ("a", "b"), "b"),       
        ({'a': {'b': 2}}, ("a", "c"), "c"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """Test that KeyError is raised for invalid paths"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(expected_key, context.exception.args[0])

def get_json(url: str) -> Dict:
    response = requests.get(url)
    return response.json()

class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_requests_get):
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_requests_get.return_value = mock_response
        result = get_json(test_url)
        mock_requests_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


def memoize(fn: Callable) -> Callable:
    attr_name = "_{}".format(fn.__name__)
    @wraps(fn)
    def memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return property(memoized)

class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_a_method:
            mock_a_method.return_value = 42
            test_instance = TestClass()

            result1 = test_instance.a_property
            result2 = test_instance.a_property

            mock_a_method.assert_called_once()

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

if __name__ == "__main__":
    unittest.main()