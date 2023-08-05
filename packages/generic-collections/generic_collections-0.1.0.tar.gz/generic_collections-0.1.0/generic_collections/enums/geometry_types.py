from enum import StrEnum


class GeometryTypeEnum(StrEnum):
    LineString: str = "LineString"
    Point: str = "Point"
    Polygon: str = "Polygon"
    MultiPoint: str = "MultiPoint"
    MultiLineString: str = "MultiLineString"
    MultiPolygon: str = "MultiPolygon"
    LinearRing: str = "LinearRing"
