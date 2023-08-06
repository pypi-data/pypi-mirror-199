from abc import ABC
from abc import abstractmethod
from typing import Final

from ..interfaces import Read


OPTIONAL_KEYS: Final = ('NAME', 'TYPE',
                        'COMMENT', 'DIMENSION', 'EDGE_WEIGHT_TYPE')


class Reader(ABC):
    file_path: str
    with_solution: bool = False
    max_nodes: int = 9999
    optional_keys: tuple[str, ...]

    def __init__(self,
                 file_path: str,
                 with_solution: bool = False,
                 max_nodes: int = 9999,
                 optional_keys: tuple[str, ...] = OPTIONAL_KEYS
                 ) -> None:
        if file_path is None:
            raise ValueError(
                'file_path is required on ReaderCVRPLib instantiation')

        self.file_path = file_path
        self.max_nodes = max_nodes
        self.optional_keys = optional_keys
        self.with_solution = with_solution

    @abstractmethod
    def read(self) -> Read:
        pass
