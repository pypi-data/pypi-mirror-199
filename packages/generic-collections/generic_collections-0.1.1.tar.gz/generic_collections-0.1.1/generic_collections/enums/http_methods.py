from enum import StrEnum


class HttpMethodEnum(StrEnum):
    POST: str = "POST"
    PUT: str = "PUT"
    DELETE: str = "DELETE"
    GET: str = "GET"
    PATCH: str = "PATCH"
