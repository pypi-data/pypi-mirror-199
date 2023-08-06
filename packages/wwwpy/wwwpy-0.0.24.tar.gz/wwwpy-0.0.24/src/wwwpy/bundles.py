import inspect
from pathlib import Path
from typing import List, Optional

from wwwpy.bundle import Bundle
from wwwpy.bundle import strategy_no_cache, ResourceGenerator, LambdaBundle
from wwwpy.common.bundle import bundle_definition
from wwwpy.resource import StringResource
from wwwpy.response import Response, Request


class Bundles:
    def __init__(self):
        self.list: List[Bundle] = []
        self.strategy = strategy_no_cache

    def to_response(self, request: Request) -> Response:
        return Response.application_zip(self.strategy(self.list))

    def add_resources(self, resource_generator: ResourceGenerator):
        self.list.append(LambdaBundle(resource_generator))

    def add_flat_folder(self, folder: Path, relative_to: Optional[Path] = None):
        self.add_resources(lambda: bundle_definition(folder, relative_to=relative_to))

    def add_file_content(self, filename: str, content: str):
        resource_list = [StringResource(filename, content)]
        self.list.append(LambdaBundle(lambda: resource_list))


def external_filename(stack_backtrack=1) -> Optional[Path]:
    wwwpy_root = Path(__file__).resolve().parent

    for stack in inspect.stack():
        source_path = Path(stack.filename).resolve()
        if not path_is_contained(source_path, wwwpy_root):
            stack_backtrack -= 1
            if stack_backtrack == 0:
                return source_path

    return None


def path_is_contained(child: Path, parent: Path):
    cl = len(child.parts)
    cp = len(parent.parts)
    if cl < cp:
        return False
    m = min(cl, cp)
    child_parts = child.parts[:m]
    parent_parts = parent.parts[:m]
    return child_parts == parent_parts
