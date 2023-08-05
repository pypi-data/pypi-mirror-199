from abc import ABC, abstractmethod
from typing import List, Iterable, Callable, Iterator

from wwwpy.common.bundle import build_archive
from wwwpy.resource import Resource

ResourceGenerator = Callable[[], Iterator[Resource]]


class Bundle(ABC):

    @abstractmethod
    def list(self) -> Iterable[Resource]:
        pass


class WatchableBundle(Bundle, ABC):
    @abstractmethod
    def is_changed(self):
        pass


def flatten_bundles(bundle_list: List[Bundle]) -> Iterable[Resource]:
    for bundle in bundle_list:
        yield from bundle.list()


class LambdaBundle(Bundle):
    def __init__(self, resource_generator: ResourceGenerator):
        self.resource_generator = resource_generator

    def list(self) -> Iterable[Resource]:
        gen = self.resource_generator()
        yield from gen


def strategy_no_cache(bundles: List[Bundle]) -> bytes:
    return build_archive(flatten_bundles(bundles))
