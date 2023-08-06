# -*- coding: utf-8 -*-

import pytest

pytest_plugins = 'pytester'

def pytest_addoption(parser):
    group = parser.getgroup('ry')
    group.addoption(
        '--ry',
        action="stroe",
        default=True,
        help='Set the value for the fixture "bar".'
    )
    # parser.addini('HELLO', 'Dummy pytest.ini setting')

@pytest.fixture(autouse=True)
def bar(request):
    demo = request.config.getoption('ry')
    if demo:
        print(request.config)
        print(1)
        yield
        print(2)