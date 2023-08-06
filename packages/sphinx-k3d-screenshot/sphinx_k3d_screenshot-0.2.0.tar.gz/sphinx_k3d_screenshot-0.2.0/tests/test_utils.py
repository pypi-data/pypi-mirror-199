import os

import pytest

from sphinx_k3d_screenshot.utils import (
    assign_last_line_into_variable, set_camera_position,
    get_port
)

def test_assign_last_line_into_variable_1():
    # the last line of code is an expression
    code = "import k3d\nplot=k3d.plot()\nplot"
    new_code = assign_last_line_into_variable(code)
    assert new_code != code
    assert "myk3d" in new_code

def test_assign_last_line_into_variable_2():
    # the last line of code is an expression representing a function call
    code = "plot_something(1, 2, kw1=True, kw2=False)"
    new_code = assign_last_line_into_variable(code)
    assert new_code != code
    assert "myk3d" in new_code

def test_assign_last_line_into_variable_3():
    # the last line of code is of the type expression.servable()
    code = "some_variable.display()"
    new_code = assign_last_line_into_variable(code)
    assert new_code != code
    assert "myk3d" in new_code
    assert "display" not in new_code

def test_set_camera_position():
    code = "import k3d\nplot=k3d.plot()\nplot"
    new_code = assign_last_line_into_variable(code)
    new_code = set_camera_position(code, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert new_code != code
    assert (("myk3d.camera = [1, 2, 3, 4, 5, 6, 7, 8, 9]" in new_code) or
        ("myk3d.camera=[1, 2, 3, 4, 5, 6, 7, 8, 9]" in new_code))
    assert "myk3d.render()" in new_code

def test_get_port():
    assert get_port() is not None
