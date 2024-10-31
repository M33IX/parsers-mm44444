from typing import NamedTuple, Dict, List, Tuple
from typing import Literal
from math import ceil

type BoxType = Literal[427] | Literal[201]
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
    Type: Literal[427] | Literal[201]
    """Тип коробки: 427 или 201"""
    Color: Literal["бурый"] | Literal["белый"]
    '''Цвет коробки: "бурый" или "белый"'''
    Cardboard: CardboardType
    '''Тип материала: "T-23" или "T-24"'''
    Quantity: int
    """Количество коробок"""
    PriceSingle: float
    """Цена за шт"""
    PriceTotal: float
    """Общая цена"""
    
def calculate(
        length: int,
        width: int,
        height: int,
        quantity: int,
        box_type: BoxType = 427,
        cardboard_type: CardboardType = "T-24",
        color: ColorType = "бурый"
) -> Box:
    """Производит рассчет стоимости по заданным параметрам\n:
       @params:
        length: int - длина в миллиметрах
        width: int - ширина в миллиметрах
        height: int - высота в миллиметрах
        quantity: int - количество штук (минимум 100)
        box_type: Literal[427] | Literal[201] - форма коробки (427 или 201)
        cardboard_type: Literal["T-23", "T-24"] - тип картона ("T-23" или "T-24" на английском)
        color: Literal["бурый"] | Literal["белый"] - цвет
        @returns:
        Box(
            Length: int - длина
            Width: int - ширина
            Height: int - высота
            Type: Literal[427,201] - тип формы (427 или 201)
            Color: Literal['бурый', 'белый'] - цвет ('бурый' или 'белый')
            Quantity: int - количество
            PriceSingle: float - цена за штуку
            PriceTotal: float - итоговый ценник
        )
    """
    _check_input_parameters(
        length=length,
        width=width,
        height=height,
        quantity=quantity, 
        box_type=box_type,
        cardboard_type=cardboard_type,
        color=color
    )
    box = _calculate_packmarket(
        length=length,
        width=width,
        height=height,
        quantity=quantity, 
        box_type=box_type,
        cardboard_type=cardboard_type,
        color=color)
    return box

def _check_input_parameters(
        length: int,
        width: int,
        height: int,
        quantity: int,
        box_type: BoxType = 427,
        cardboard_type: CardboardType = "T-24",
        color: ColorType = "бурый"
) -> None:
    def _check_dimmensions() -> None:
        if width < 60: raise ValueError('Width must be more than 60mm')
        if length < 60: raise ValueError('Length must be more than 60mm')
        if height < 30: raise ValueError('Height must be more than 30mm')
        if length < width: raise ValueError('Length must be more than width')
    def _check_box_specific_dimmensions() -> None:
        if box_type == 201:
            if length + width > 3140: raise ValueError('This size is not available')
            if height + width > 1390: raise ValueError('This size is not available')
        if box_type == 427:
            if 2 * width + 3 * height > 1960: raise ValueError('This size is not available')
            if length + 4 * height > 1310: raise ValueError('This size is not available')
    
    if quantity < 100: raise ValueError('Quantity must be more than 100')
    if (box_type != 427) & (box_type != 201): raise ValueError('Box type must be 427 or 201')
    if (color != 'бурый') & (color != 'белый'): raise ValueError('Color must be "бурый" or "белый"')
    if (cardboard_type != 'T-24'): raise ValueError('Cardboard type must be "T-24"')
    _check_dimmensions()
    _check_box_specific_dimmensions()


def _calculate_packmarket(
        length: int,
        width: int,
        height: int,
        quantity: int,
        box_type: BoxType = 427,
        cardboard_type: CardboardType = "T-24",
        color: ColorType = "бурый"
    ) -> Box:
    cardboard_price =_get_cardboard_price(cardboard_type, color)
    box_area = _calculate_area(length, width, height, box_type)
    base_price = _get_base_price(box_area, cardboard_price)
    price_single = _calculate_single_price(base_price, quantity)
    price_total = price_single * quantity
    return Box(
        Length=length, 
        Width=width, 
        Height=height, 
        Type=box_type, 
        Color = color,
        Cardboard=cardboard_type,
        Quantity=quantity, 
        PriceSingle=price_single, 
        PriceTotal=price_total
        )

def _get_cardboard_price(cardboard_type: CardboardType, color: ColorType) -> float:
    prices: CardboardPriceMatrix = {
        'бурый': {
            'T-23': 40.0,
            'T-24': 45.0
        },
        'белый': {
            'T-23': 50.0,
            'T-24': 50.0
        }
    }
    return prices[color][cardboard_type]

def _calculate_area(length: int, width: int, height: int, box_type: BoxType) -> int:
    #Пока что будет под 0427 и 0201 короб. Дальше можно добавить по запросу
    if box_type == 427:
        return ((length + 4 * height + 70)*(2 * width + 3 * height + 40))
    
    if box_type == 201:
        return ((width + height + 8)*((length + width) * 2 + 60))
    return 43500

def _get_base_price(box_area: int, cardboard_price: float) -> float:
    return box_area / 1000000 * cardboard_price

def _calculate_quantity_markup(quantity: int) -> float:
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
        if quantity < sk[i][0]:
            previous_level, current_level = sk[i - 1][1], sk[i][1]
            return current_level + (previous_level - current_level) * ((sk[i][0] - quantity) / (sk[i][0] - sk[i - 1][0]))

    return 0.0

def _calculate_single_price(base_price: float, quantity: int) -> float:
    price_raw = base_price + _calculate_quantity_markup(quantity)
    price_sigle = ceil(price_raw * 100) / 100
    return price_sigle

if __name__ == '__main__':
    #Рассчет по всем параметрам
    box = calculate(
        length=300, 
        width=300, 
        height=1060, 
        quantity=100, 
        box_type=201,
        cardboard_type="T-24",
        color="бурый"
    )
    print(f'Коробка {box.Type}, {box.Length}x{box.Width}x{box.Height}, {box.Color}, {box.Quantity} шт - {box.PriceSingle} руб. / {box.PriceTotal} руб.')
    """
    если не задана форма, цвет и тип картона, то возьмутся дефолтные
    427, T-24, бурый
    """
    box=calculate(
        length=300, 
        width=300, 
        height=200, 
        quantity=100
    )
    print(box)