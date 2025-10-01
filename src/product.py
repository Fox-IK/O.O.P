class Product:
    """
    Класс для представления товара.

    Атрибуты:
        name (str): Название товара
        description (str): Описание товара
        price (float): Цена товара
        quantity (int): Количество товара в наличии
    """

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """
    Класс для представления категории товаров.

    Атрибуты:
        name (str): Название категории
        description (str): Описание категории
        products (list): Список товаров категории
    """

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.products = products

        Category.category_count += 1
        Category.product_count += len(products)
