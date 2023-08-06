import os

import pytest


@pytest.fixture
def platform():
    return "ios"


@pytest.fixture(autouse=True)
def skip_by_platform(request, platform):
    if request.node.get_closest_marker('skip_platform'):
        if request.node.get_closest_marker('skip_platform').args[0] == platform:
            pytest.skip('skipped on this platform: {}'.format(platform))


@pytest.fixture
def local_pg_enabled():
    # only if the value is True we will treat as postgres enabled
    # any other value (including None) will be treated as postgres not enabled.
    return os.environ.get("LOCAL_POSTGRES_ENABLED_PYTHON_ENV") == "True"


@pytest.fixture(autouse=True)
def skip_if_local_postgres_not_enabled(request, local_pg_enabled):
    if request.node.get_closest_marker('skip_if_local_postgres_not_enabled'):
        if not local_pg_enabled:
            pytest.skip('skipped because local postgres is unavailable')
