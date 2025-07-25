#!/usr/bin/env python3
"""Generic utilities for github org client.
"""
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
    """
    This is an example testcases that uses parameterized
    expanssion to test if the code is correct
    """
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
    """Get JSON from remote URL.
    """
    response = requests.get(url)
    return response.json()


class TestGetJson(unittest.TestCase):
    """
    This is a class that mock http call and
    get http from a remote json.
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_requests_get):
        """The function try to get http request from json"""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_requests_get.return_value = mock_response
        result = get_json(test_url)
        mock_requests_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


def memoize(fn: Callable) -> Callable:
    """Decorator to memoize a method.
    Example
    -------
    class MyClass:
        @memoize
        def a_method(self):
            print("a_method called")
            return 42
    >>> my_object = MyClass()
    >>> my_object.a_method
    a_method called
    42
    >>> my_object.a_method
    42
    """
    attr_name = "_{}".format(fn.__name__)
    @wraps(fn)
    def memoized(self):
        """"memoized wraps"""
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return property(memoized)


class TestMemoize(unittest.TestCase):
    """
    This code test if the function memoize
    is correctly used
    """
    def test_memoize(self):
        """This function check if correct out will be return"""
        class TestClass:
            """the test class"""
            def a_method(self):
                """the wrap function in the TestClass"""
                return 42

            @memoize
            def a_property(self):
                """the wrap fuction for a_property"""
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
