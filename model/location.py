from dataclasses import dataclass


@dataclass
class Location:
    Location: str
    Latitude: float
    Longitude: float

    def __str__(self):
        return self.Location

    def __hash__(self):
        return hash(self.Location)