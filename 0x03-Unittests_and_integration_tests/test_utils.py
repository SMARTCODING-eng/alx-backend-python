
#!/usr/bin/env python3
import unittest

def access_nested_map(nested_map, path):
    """"Access a value in a nested dictionary using a sequence of key.
    args:
        nested_map (dict): The nested dictionary to access.
        path (tuple): A sequence of keys  representing the path to the value.
        
        Returns:
        The value at the specified path in the nested dictionary.
        """
    current = nested_map
    for key in path:
        current = current[key]
    return current

class TestAccessNestedMap(unittest.TestCase):
    def test_access_nested_map_top_level(self):
        nested_map = {"a": 1}
        self.assertEqual(access_nested_map(nested_map, ("a",)), 1)

    def test_access_nested_map_nested_dict(self):
        nested_map = {"a": {"b": 2}}
        self.assertEqual(access_nested_map(nested_map, ("a",)), {"b": 2})


    def test_access_nested_map_nested_value(self):
        nested_map = {"a": {"b": 2}}
        self.assertEqual(access_nested_map(nested_map, ("a", "b")), 2)




if __name__ == "__main__":
    unittest.main()
