from __future__ import annotations

from typing import TYPE_CHECKING

from .bootstrap import Bootstrap
from .bundle import Bundle
from .bundles import Bundles
from .resource import Resource, StringResource, PathResource
from .response import Response
from .routes import Routes, Route
from .webserver import Webserver
from .webservers.available_webservers import available_webservers

if True:  # workaround to stop Pycharm reordering Config import
    pass

from .config import Config

if TYPE_CHECKING:
    from .webservers.flask import WsFlask
    from .webservers.fastapi import WsFastapi


def ws_flask() -> WsFlask:
    from .webservers.flask import WsFlask
    return WsFlask()


def ws_fastapi() -> WsFastapi:
    from .webservers.fastapi import WsFastapi
    return WsFastapi()


__version__ = '0.0.24'
