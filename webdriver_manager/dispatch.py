from typing import Type

from .chrome import ChromeDriverManager
from .core.manager import DriverManager
from .firefox import GeckoDriverManager
from .microsoft import IEDriverManager, EdgeChromiumDriverManager
from .opera import OperaDriverManager

_BROWSER_ALIAS = {
    'msie': 'ie',
    'msedge': 'edge',
    'google': 'chrome',
    'gecko': 'firefox',
}
_BROWSER_MANAGERS = {
    'ie': IEDriverManager,
    'edge': EdgeChromiumDriverManager,
    'chrome': ChromeDriverManager,
    'firefox': GeckoDriverManager,
    'opera': OperaDriverManager,
}


def _parse_browser_name(name: str):
    original_name = name
    name = name.lower().strip()
    name = _BROWSER_ALIAS.get(name, name)
    if name in _BROWSER_MANAGERS:
        return name
    else:
        raise ValueError(f'Unknown browser name - {original_name!r}.')


def get_browser_manager_class(name) -> Type[DriverManager]:
    return _BROWSER_MANAGERS[_parse_browser_name(name)]


def get_browser_manager(browser_name: str, *args, **kwargs):
    return get_browser_manager_class(browser_name)(*args, **kwargs)
