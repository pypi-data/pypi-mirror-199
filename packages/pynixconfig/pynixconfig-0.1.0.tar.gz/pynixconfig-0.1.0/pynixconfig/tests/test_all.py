from pynixconfig import get_color_code, get_font_code, get_full_path
from pynixconfig import add_ls_colors, config, main, replace_ls_colors
import os


def test_color_code():
    assert get_color_code("red") == "31"
    assert get_color_code("blue") == "34"


def test_font_code():
    assert get_font_code("bold") == "1"


def test_get_full_path():
    assert get_full_path("~/.bashrc") == os.path.expanduser("~/.bashrc")


def test_config():
    assert config("31", "1") == "di=1;31"


def test_add_ls_colors():
    assert add_ls_colors("", "di=1;31") == '\nLS_COLORS="di=1;31"'


def test_replace_ls_colors():
    assert replace_ls_colors("di=1;31") == 'LS_COLORS="di=1;31"'


def integration_test():
    assert main("red", "bold") == 'LS_COLORS="di=1;31"'
