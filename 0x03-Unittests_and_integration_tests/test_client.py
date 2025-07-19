#!/usr/bin/env python3
"""A github org client"""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import fixtures


class TestGithubOrgClient(unittest.TestCase):
    """
    Tests for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    def test_org(self, org_name: str) -> None:
        """
        Test that GithubOrgClient.org returns the correct value.
        """
        expected_payload = {
            "login": org_name,
            "id": 12345,
            "repos_url": f"https://api.github.com/orgs/{org_name}/repos"
        }
        with patch(
                'client.get_json',
                return_value=expected_payload
                ) as mock_get_json:
            client = GithubOrgClient(org_name)
            result = client.org
            expected_url = f"https://api.github.com/orgs/{org_name}"
            mock_get_json.assert_called_once_with(expected_url)
            self.assertEqual(result, expected_payload)

    def test_public_repos_url(self) -> None:
        """
        Test that _public_repos_url returns the expected repos_url.
        """
        expected_url = "https://api.github.com/orgs/test_org/repos"
        with patch(
            'client.GithubOrgClient.org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": expected_url}
            client = GithubOrgClient("some_org")
            result = client._public_repos_url
            mock_org.assert_called_once()
            self.assertEqual(result, expected_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: Mock) -> None:
        """
        Test that public_repos returns the expected list.
        """
        test_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None},
            {"name": "repo4"},
        ]
        mock_get_json.return_value = test_repos_payload
        test_url = "https://api.github.com/orgs/test_org/repos"
        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = test_url
            client = GithubOrgClient("test_org")
            repos = client.public_repos()
            expected = ["repo1", "repo2", "repo3", "repo4"]
            self.assertEqual(repos, expected)
            mock_get_json.assert_called_once_with(test_url)
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({"license": None}, "my_license", False),
        ({}, "my_license", False),
    ])
    def test_has_license(self,
                         repo: dict, license_key: str, expected: bool
                         ) -> None:
        """
        Test GithubOrgClient.has_license.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        'org_payload': org_payload,
        'repos_payload': repos_payload,
        'expected_repos': expected_repos,
        'apache2_repos': apache2_repos
    }
    for org_payload, repos_payload, expected_repos, apache2_repos
    in fixtures.TEST_PAYLOAD
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Integration test for GithubOrgClient.public_repos """

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get with proper side effects."""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url == cls.org_payload["repos_url"]:
                mock_response = unittest.mock.Mock()
                mock_response.json.return_value = cls.repos_payload
                return mock_response
            elif url == "https://api.github.com/orgs/test_org":
                mock_response = unittest.mock.Mock()
                mock_response.json.return_value = cls.org_payload
                return mock_response
            raise ValueError(f"Unhandled URL: {url}")
        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher."""
        cls.get_patcher.stop()

    def test_public_repos_integration(self):
        """
        Test public_repos method in an integration setting.
        """
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test public_repos with a license filter in an integration setting.
        """
        client = GithubOrgClient("test_org")
        self.assertEqual(
            client.public_repos(license="apache-2.0"), self.apache2_repos
            )


if __name__ == "__main__":
    unittest.main()
