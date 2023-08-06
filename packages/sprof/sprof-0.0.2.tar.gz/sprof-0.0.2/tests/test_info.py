"""
Tests for getting info from sprof project.
"""
import pytest

import sprof


@pytest.fixture(scope="class")
def spf_example_info(spf_example_project):
    """Return the info dict."""
    info = sprof.info(spf_example_project)
    return info


class TestInfo:
    """Test case for getting sprof project info."""

    def test_info(self, spf_example_info):
        """Get info, test basics."""
        assert isinstance(spf_example_info, dict)
        assert len(spf_example_info)
        assert spf_example_info["spf_version"] == sprof.__version__
