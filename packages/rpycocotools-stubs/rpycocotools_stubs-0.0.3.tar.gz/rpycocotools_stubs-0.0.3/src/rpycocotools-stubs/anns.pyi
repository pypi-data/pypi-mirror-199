from typing import TypeAlias

from typing_extensions import Self

class Annotation:
    id: int
    image_id: int
    category_id: int
    segmentation: Polygons | PolygonsRS | Rle | EncodedRle
    area: float
    bbox: Bbox
    iscrowd: int
    def __init__(self: Self,
                 id: int,
                 image_id: int,
                 category_id: int,
                 segmentation: Polygons | PolygonsRS | Rle | EncodedRle,
                 area: float,
                 bbox: Bbox,
                 iscrowd: int,
                 ) -> None: ...

class Category:
    id: int
    name: str
    supercategory: str
    def __init__(self: Self, id: int, name: str, supercategory: str) -> None: ...

class Bbox:
    left: float
    top: float
    width: float
    height: float
    def __init__(self: Self, left: float, top: float, width: float, height: float) -> None: ...

class Image:
    id: int
    width: int
    height: int
    file_name: str
    def __init__(self: Self, id: int, width: int, height: int, file_name: str) -> None: ...

Polygons: TypeAlias = list[list[float]]

class PolygonsRS:
    size: list[int]
    counts: list[list[float]]
    def __init__(self: Self, size: list[int], counts: list[list[float]]) -> None: ...

class Rle:
    size: list[int]
    counts: list[int]
    def __init__(self: Self, size: list[int], counts: list[int]) -> None: ...

class EncodedRle:
    size: list[int]
    counts: str
    def __init__(self: Self, size: list[int], counts: str) -> None: ...
