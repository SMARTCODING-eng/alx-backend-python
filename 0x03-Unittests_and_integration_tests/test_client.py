#!/usr/bin/env python3
"""A github org client
"""
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient


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
        Tests that GithubOrgClient.org returns the correct value
        and that get_json is called once with the expected argument.
        """
        expected_payload = {
            "login": org_name,
            "id": 12345,
            "repos_url": f"https://api.github.com/orgs/{org_name}/repos"
        }
        with patch(
                'client.get_json', return_value=expected_payload
                ) as mock_get_json:
            client = GithubOrgClient(org_name)
            result = client.org
            expected_url = f"https://api.github.com/orgs/{org_name}"
            mock_get_json.assert_called_once_with(expected_url)
            self.assertEqual(result, expected_payload)

    def test_public_repos_url(self) -> None:
        """
        Tests that _public_repos_url returns the
        expected URL based on the mocked org payload.
        """
        expected_url = "https://api.github.com/orgs/test_org/repos"

        with patch(
                'client.GithubOrgClient.org', new_callable=PropertyMock
                ) as mock_org:
            mock_org.return_value = {"repos_url": expected_url}
            client = GithubOrgClient("some_org")
            result = client._public_repos_url

            mock_org.assert_called_once()
            self.assertEqual(result, expected_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: Mock) -> None:
        """
        ths check if Tests that GithubOrgClient.public_repos returns
        the expected list.
        Mocks get_json to return a chosen payload and
        GithubOrgClient._public_repos_url as a property.
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
                new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_url
            client = GithubOrgClient("test_org")
            repos = client.public_repos()
            expected_repos = ["repo1", "repo2", "repo3", "repo4"]
            self.assertEqual(repos, expected_repos)
            mock_get_json.assert_called_once_with(test_url)
            mock_public_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({"license": None}, "my_license", False),  # license is None
        ({}, "my_license", False),  # no license key
    ])
    def test_has_license(self,
                         repo: dict,
                         license_key: str,
                         expected_return: bool) -> None:
        """
        Tests the GithubOrgClient.has_license static method.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_return)


if __name__ == '__main__':
    unittest.main()
