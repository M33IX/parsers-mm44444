from typing import NamedTuple, Literal,  Tuple, List
from .types import *
import requests
from bs4 import BeautifulSoup as Soup
import re
#                                                                            "0427"       300      300     100       t24              bury                                420
_REQUEST_URL_TEMPLATE: str = "https://app.ronbel.ru/korobka/client/samovyvoz/{box_type}/{length}/{width}/{height}/{cardboard_type}/{color}/print_no/options_no/price/{quantity}"
_MATCHING_PATTERN = r"(\d{1,3}(?: \d{3})*,\d{2})"

class UrlParameters(NamedTuple):
    length: int
    width: int
    height: int
    box_form: Literal['0427', '0201']
    cardboard_type: str
    color: Literal['bury']
    quantity: int

class Prices(NamedTuple):
    price_unit: float
    press_form: float
    price_total: float

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
    _check_input_parameters(
        length=length,
        width=width,
        height=height,
        quantity=quantity, 
        box_type=box_type,
        cardboard_type=cardboard_type,
        color=color
    )
    _check_input_parameters(**locals())

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
    def _check_dimmensions():
        if length < 0: raise ValueError('Negative length')
        if width < 0: raise ValueError('Negative width')
        if height < 0: raise ValueError('Negative height')
    if quantity < 0: raise ValueError('Negative quantity')
    if (box_type != "0427") & (box_type != "0201"): raise ValueError('Unknown box type. Must be "0201" or "0427"')
    if (color != 'бурый') & (color != 'белый'): raise ValueError('Unknown color. Must be "бурый" or "белый"')
    if (cardboard_type != 'T-24'): raise ValueError('Unknown cardboard type. Must be "T-24"')
    _check_dimmensions()

def _adjust_parameters_for_url_format(
        length: int,
        width: int,
        height: int,
        quantity: int,
        box_type: BoxType = "0427",
        cardboard_type: CardboardType = "T-24",
        color: ColorType = "бурый"
) -> UrlParameters:
    def _adjust_cardboard_type(input: str):
        return input.lower().replace("-", "")
    u_cardboard = _adjust_cardboard_type(cardboard_type)
    if color == 'бурый':
        u_color = 'bury'
    return UrlParameters(
        length=length,
        width=width,
        height=height,
        quantity=quantity,
        box_form=box_type,
        cardboard_type=u_cardboard,
        color=u_color
    )

def _send_request(params: UrlParameters) -> str | None:
    request_url = _REQUEST_URL_TEMPLATE.format(
        box_type = params.box_form,
        length = params.length,
        width = params.width,
        height = params.height,
        cardboard_type = params.cardboard_type,
        color = params.color,
        quantity=params.quantity
    )
    r = requests.get(request_url)
    if r.status_code == 200:
        return r.text
    else:
        raise ExternalError("External server error. Try again")

def _get_raw_data_from_response(response: str) -> str:
    #Никто не должен это видеть
    soup = Soup(response, 'html5lib')
    if "Ошибка" in response:
        error: str = soup.findAll('div', {"class" : "container"})[0].findAll('h3')[0].get_text()
        raise CalculationError('Cant make box with these parameters', description=error)
    
    raw_data = soup.findAll('div', {"itemprop":"offers"})[0].findAll('p')[0].get_text()

    return raw_data

def _parse_raw_data(raw_data: str) -> tuple:
    #И это тоже
    raw_prices: List[str] = re.findall(raw_data, _MATCHING_PATTERN)
    formatted_prices = [price.replace(' ', '').replace(',', '.') for price in raw_prices]
    return tuple(formatted_prices)

def _adjust_response_parameters_format(prices: tuple) -> Prices:
    #god bless
    price_unit =  float(prices[0])
    press_form = float(prices[1])
    price_total = float(prices[2])
    return Prices(
        price_unit=price_unit,
        press_form=press_form,
        price_total=price_total
    )   