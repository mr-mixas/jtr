import os
import pytest

pytest.register_assert_rewrite('tests.common')


@pytest.fixture
def content():
    def _reader(filename):
        with open(filename) as f:
            return f.read()

    return _reader


@pytest.fixture
def expected(request):
    filename = os.path.splitext(request.module.__file__)[0]
    filename += '.' + request.function.__name__ + '.exp'

    with open(filename) as f:
        return f.read()


@pytest.fixture
def rpath(request):
    def _path_resolver(filename):
        path = os.path.join(
            os.path.dirname(request.module.__file__),
            filename,
        )

        return os.path.relpath(
            path,
            os.path.join(os.path.dirname(__file__), '..'),
        )

    return _path_resolver
