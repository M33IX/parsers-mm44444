# Packmarket Calculator
Полностью скопированный с пакмаркета калькулятор стоимости упаковки по параметрам

Использование:
```python
    from packmarket_calculator import calculate
    #Рассчет по всем заданным параметрам
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
```

### Возвращаемые значения:
    Метод возвращает структуру *Box*, которая наследуется от стандартной структуры Tuple.
    ```python
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
    ```
    Поэтому работают все методы по взаимодействию с кортежами
    Так же, имеется возможность доступа по имени параметра:

    ```python
     box = calculate(
        length=300, 
        width=300, 
        height=1060, 
        quantity=100, 
        box_type=201,
        cardboard_type="T-24",
        color="бурый"
    )
    print(box.Length)  #300
    print(box.Width) #300
    print(box.Height) #1060
    print(box.Quantity) #100
    print(box.Type) #201
    print(box.Color) #"бурый"
    print(box.Cardboard)# "T-24"
    print(box.PriceSingle) #127.57
    print(box.PriceTotal) #12757.0 
    ```