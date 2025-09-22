@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Performs integration tests for GithubOrgClient.public_repos using fixtures."""

    @classmethod
    def setUpClass(cls) -> None:
        """Mock requests.get to return payloads from fixtures."""
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                # Mock .json() method to return fixture for the URL
                return MagicMock(**{'json.return_value': route_payload[url]})
            raise Exception("URL not in fixtures")

        # Patch requests.get and start the patcher
        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Integration test for public_repos method."""
        gh_client = GithubOrgClient("google")
        self.assertEqual(gh_client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Integration test for public_repos method filtering by license."""
        gh_client = GithubOrgClient("google")
        self.assertEqual(
            gh_client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Stop the patcher after all tests are done."""
        cls.get_patcher.stop()
