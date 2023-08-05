from decimal import Decimal

from pydantic import BaseModel


class Point(BaseModel):
    x: Decimal
    y: Decimal
