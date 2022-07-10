from dataclasses import dataclass, field
from typing import List


@dataclass
class AddressCoordinate:
    longitude: float
    latitude: float


@dataclass
class AddressData:
    coordinate: AddressCoordinate
    id: int
    type: str
    name: str


@dataclass
class Address:
    data: AddressData


@dataclass
class RawStation:
    id: int
    name: str
    status: str
    description: str
    boxes: int
    free_boxes: int
    free_bikes: int
    longitude: float
    latitude: float
    internal_id: int


@dataclass
class TransformedStation:
    id: int
    name: str
    active: bool
    description: str
    boxes: int
    free_boxes: int
    free_bikes: int
    free_ratio: float = field(init=False)
    coordinates: List[float]
    address: str = field(init=False)

    def __post_init__(self):
        self.free_ratio = self.free_boxes / self.boxes
