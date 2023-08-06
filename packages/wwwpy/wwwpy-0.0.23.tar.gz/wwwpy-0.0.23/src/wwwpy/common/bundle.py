import zipfile
from io import BytesIO
from pathlib import Path
from typing import Iterator, Optional, Callable

from wwwpy.resource import PathResource
from wwwpy.resource import Resource, StringResource


def default_item_filter(item: Resource) -> Optional[Resource]:
    if not isinstance(item, PathResource):
        return item
    item: PathResource
    filepath = item.filepath
    if filepath.name == '.DS_Store':
        return None
    if filepath.name == '__pycache__' and filepath.is_dir():
        return None
    return item


def bundle_definition(
        folder: Path, relative_to: Optional[Path] = None,
        item_filter: Callable[[PathResource], Optional[PathResource]] = default_item_filter
) -> Iterator[PathResource]:
    if relative_to is None:
        relative_to = folder

    def recurse(path: Path):
        for f in path.glob('*'):
            rel = f.relative_to(relative_to)
            candidate = PathResource(str(rel), f)
            item = item_filter(candidate)
            if item is not None:
                if f.is_file():
                    yield item
                else:
                    yield from recurse(f)

    yield from recurse(folder)
    return iter(())


def build_archive(item_iterator: Iterator[Resource]) -> bytes:
    stream = BytesIO()
    zf = zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1)

    for item in item_iterator:
        if isinstance(item, PathResource):
            zf.write(item.filepath, item.arcname)
        elif isinstance(item, StringResource):
            zf.writestr(item.arcname, item.get_content())
        else:
            raise Exception(f'Unhandled class \n  type={type(item).__name__} \n  data={item}')
    zf.close()

    stream.seek(0)
    return stream.getbuffer().tobytes()
