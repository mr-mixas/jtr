import io
import pytest

from unittest import mock

import jtr


def test_arg_file_absent(capsys, rpath):
    with pytest.raises(SystemExit) as e:
        jtr.App(args=(
            rpath('no/such/file'),
            rpath('no/such/file'),
        )).run()

    captured = capsys.readouterr()
    assert '' == captured.out
    assert 'tests/no/such/file' in captured.err

    assert e.value.code == 2


def test_vars_passed_as_file(capsys, rpath):
    exit_code = jtr.App(args=(
        rpath('shared/minimal.jinja'),
        rpath('shared/minimal.vars.json'),
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert exit_code == 0

    assert 'val\n' == captured.out


def test_vars_passed_as_stdin(capsys, rpath):
    vars_ = '{"key": "val"}'

    stdin_ = io.StringIO(vars_)
    stdin_.name = '-'

    with mock.patch('sys.stdin', stdin_):
        exit_code = jtr.App(args=(
            rpath('shared/minimal.jinja'),
        )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert exit_code == 0

    assert 'val\n' == captured.out


def test_logging(capsys, rpath):
    exit_code = jtr.App(args=(
        rpath('shared/minimal.jinja'),
        rpath('shared/minimal.vars.json'),
        '-l', 'DEBUG', '--log-level', 'DEBUG',
    )).run()

    captured = capsys.readouterr()
    assert 'INFO' in captured.err
    assert exit_code == 0

    assert 'val\n' == captured.out
