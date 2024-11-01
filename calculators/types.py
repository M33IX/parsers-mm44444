from typing import Literal, NamedTuple, Dict

type BoxType = Literal["0427"] | Literal["0201"]
type ColorType = Literal["бурый"] | Literal["белый"]
type CardboardType = Literal["T-23", "T-24"]

type CardboardPriceMatrix = Dict[ColorType, Dict[CardboardType, float]]

class Box(NamedTuple):
    Length: int
    """Длина коробки в миллиметрах"""
    Width: int
    """Ширина коробки в миллиметрах"""
    Height: int
    """Высота коробки в миллиметрах"""
    Type: Literal["0427"] | Literal["0201"]
    """Тип коробки: "0427" или "0201" """
    Color: Literal["бурый"] | Literal["белый"]
    '''Цвет коробки: "бурый" или "белый"'''
    Cardboard: CardboardType
    '''Тип материала: "T-23" или "T-24"'''
    Quantity: int
    """Количество коробок"""
    PriceUnit: float
    """Цена за шт"""
    PriceTotal: float
    """Общая цена"""

__all__ = ['Box', 'BoxType', 'ColorType', 'CardboardType']