from typing import Any, TypedDict
from typing_extensions import Required, NotRequired


class Params(TypedDict, total=False):
    file_path: Required[str]
    max_nodes: NotRequired[int]
    optional_keys: NotRequired[tuple[str, ...]]
    with_solution: NotRequired[bool]


class Solution(TypedDict):
    cost: Required[int]
    routes: Required[tuple[tuple[int, ...], ...]]


class Read(TypedDict, total=False):
    depot: Required[int]
    nodes: Required[tuple[int, ...]]
    clients: Required[tuple[int, ...]]
    coords: Required[tuple[tuple[float, float], ...]]
    demands: Required[tuple[int, ...]]
    total_demand: Required[int]
    vehicle_capacity: Required[int]
    k_routes: Required[int]
    tightness_ratio: Required[float]
    solution: NotRequired[Solution]
    optional_data: NotRequired[dict[str, Any]]
