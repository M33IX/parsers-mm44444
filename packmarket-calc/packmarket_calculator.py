from typing import NamedTuple, Dict, List, Tuple
from typing import Literal
from math import ceil

type BoxType = Literal[427] | Literal[201]
type ColorType = Literal["бурый"] | Literal["белый"]
type CardboardType = Literal["T-22", "T-23", "T-24", "T-25", "P-31"]

type CardboardPriceMatrix = Dict[ColorType, Dict[CardboardType, float]]

class Box(NamedTuple):
    Length: int
    """Длина коробки в миллиметрах"""
    Width: int
    """Ширина коробки в миллиметрах"""
    Height: int
    """Высота коробки в миллиметрах"""
    Type: Literal[427] | Literal[201]
    """Тип коробки: 427 или 201"""
    Color: Literal["бурый"] | Literal["белый"]
    '''Цвет коробки: "бурый" или "белый"'''
    Cardboard: CardboardType
    '''Тип материала: "T-23" или "T-24"'''
    Amount: int
    """Количество коробок"""
    PriceSingle: float
    """Цена за шт"""
    PriceTotal: float
    """Общая цена"""

def calculate_packmarket(
        length: int,
        width: int,
        height: int,
        amount: int,
        box_type: BoxType = 427,
        cardboard_type: CardboardType = "T-24",
        color: ColorType = "бурый"
    ) -> Box:
    cardboard_price =_get_cardboard_price(cardboard_type, color)
    box_area = _calculate_area(length, width, height, box_type)
    base_price = _get_base_price(box_area, cardboard_price)
    price_single = _calculate_single_price(base_price, amount)
    price_total = price_single * amount
    return Box(
        Length=length, 
        Width=width, 
        Height=height, 
        Type=box_type, 
        Color = color,
        Cardboard=cardboard_type,
        Amount=amount, 
        PriceSingle=price_single, 
        PriceTotal=price_total
        )

def _get_cardboard_price(cardboard_type: CardboardType, color: ColorType) -> float:
    prices: CardboardPriceMatrix = {
        'бурый': {
            'T-22': 35.24,
            'T-23': 40.0,
            'T-24': 45.0,
            'T-25': 50.4,
            'P-31': 80.69
        },
        'белый': {
            'T-22': 45.07,
            'T-23': 50.0,
            'T-24': 50.0,
            'T-25': 60.59,
            'P-31': 110.07
        }
    }
    return prices[color][cardboard_type]

def _calculate_area(length: int, width: int, height: int, type: BoxType) -> int:
    return 43500

def _get_base_price(box_area: int, cardboard_price: float) -> float:
    return box_area / 1000000 * cardboard_price

def _calculate_quantity_markup(amount: int) -> float:
    #Можно представить это как перечень (x, f(x)), где x - количество, коробок f(x) - наценка за 1 шт.
    sk: List[Tuple[int, float]] = [
        (100, 50), (500, 20), (1000, 10), (3000, 2.5),
        (10000, 1.85), (50000, 1.35), (100000, 0.75), (1000000, 0)
    ]
    """
    1. Найти проомежуток (a,b), в котором лежит нужное нам количество - x
    2. Посчитать наценку как (f(b)) + (f(a) - f(b)) * ((b - x) / (b - a))
    """
    for i in range(1, len(sk)):
        if amount < sk[i][0]:
            previous_level, current_level = sk[i - 1][1], sk[i][1]
            return current_level + (previous_level - current_level) * ((sk[i][0] - amount) / (sk[i][0] - sk[i - 1][0]))

    return 0.0

def _calculate_single_price(base_price: float, amount: int) -> float:
    price_raw = base_price + _calculate_quantity_markup(amount)
    price_sigle = ceil(price_raw * 100) / 100
    return price_sigle

if __name__ == '__main__':
    box = calculate_packmarket(200, 100, 50, 250)
    print(f'Коробка {box.Type}, {box.Length}x{box.Width}x{box.Height}, {box.Color}, {box.Amount} шт - {box.PriceSingle} руб. / {box.PriceTotal} руб.')