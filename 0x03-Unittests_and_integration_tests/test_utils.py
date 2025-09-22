#!/usr/bin/env python3
"""
Test for utils functions: access_nested_map, get_json, memoize
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
import requests
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'")
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_message):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_message)


class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch("requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        # Mock the return value of requests.get().json() to be test_payload
        mock_get.return_value.json.return_value = test_payload

        result = get_json(test_url)
        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # Patch a_method to monitor how many times it is called
        with patch.object(TestClass, 'a_method') as mock_method:
            test = TestClass()
            # Call a_property twice
            result1 = test.a_property()
            result2 = test.a_property()

            # Check that a_method is only called once
            mock_method.assert_called_once()

            # Check that the return value is correct both times
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
