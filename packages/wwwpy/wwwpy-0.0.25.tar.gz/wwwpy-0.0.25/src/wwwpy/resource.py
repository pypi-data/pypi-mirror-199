from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Resource(ABC):
    arcname: str

    @abstractmethod
    def get_content(self) -> str:
        pass


@dataclass(frozen=True)
class StringResource(Resource):
    content: str

    def get_content(self) -> str:
        return self.content


@dataclass(frozen=True)
class PathResource(Resource):
    filepath: Path

    def get_content(self) -> str:
        return self.filepath.read_text()
