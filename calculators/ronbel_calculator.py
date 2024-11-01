from typing import NamedTuple
from .types import *

#TODO: Box
#                                                                            "0427"       300      300     100       t24              bury                                420
_REQUEST_URL_TEMPLATE: str = "https://app.ronbel.ru/korobka/client/samovyvoz/{box_type}/{length}/{width}/{height}/{cardboard_type}/{color}/print_no/options_no/price/{quantity}"

def calculate(
        length: int,
        width: int,
        height: int,
        quantity: int,
        box_type: BoxType = "0427",
        cardboard_type: CardboardType = "T-24",
        color: ColorType = "бурый"
        ) -> Box:
    """Производит рассчет стоимости по заданным параметрам\n:
       @params:
        length: int - длина в миллиметрах
        width: int - ширина в миллиметрах
        height: int - высота в миллиметрах
        quantity: int - количество штук (минимум 100)
        box_type: Literal["0427"] | Literal["0201"] - форма коробки ("0427" или "0201")
        cardboard_type: Literal["T-23", "T-24"] - тип картона ("T-23" или "T-24" на английском)
        color: Literal["бурый"] | Literal["белый"] - цвет
        @returns:
        Box(
            Length: int - длина
            Width: int - ширина
            Height: int - высота
            Type: Literal["0427","0201"] - тип формы ("0427" или "0201")
            Color: Literal['бурый', 'белый'] - цвет ('бурый' или 'белый')
            Quantity: int - количество
            PriceUnit: float - цена за штуку
            PriceTotal: float - итоговый ценник
        )
    """
    #Проверить входные параметры
    #Подогнать входные параметры под вид для запроса
    #Сделать запрос по урл
    #Спарсить со страницы ответ
    #Упаковать ответ в структуру Box
    pass

def _check_input_parameters(
        length: int,
        width: int,
        height: int,
        quantity: int,
        box_type: BoxType = "0427",
        cardboard_type: CardboardType = "T-24",
        color: ColorType = "бурый"
) -> None:
    pass

def _adjust_parameters_for_url_format():
    pass

def _send_request():
    pass

def _parse_response():
    pass

def _adjust_response_parameters_format():
    pass