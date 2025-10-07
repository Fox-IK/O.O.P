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
        self.__price = price  # Приватный атрибут
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data: dict, products_list: list = None):
        """
        Класс-метод для создания нового продукта из словаря.
        С дополнительной функциональностью: проверка дубликатов.

        Args:
            product_data (dict): Словарь с данными продукта
            products_list (list, optional): Список существующих продуктов для проверки дубликатов

        Returns:
            Product: Новый объект класса Product или обновленный существующий
        """
        # Проверка на дубликаты (дополнительное задание)
        if products_list:
            for existing_product in products_list:
                if existing_product.name.lower() == product_data["name"].lower():
                    # Объединяем количество
                    existing_product.quantity += product_data["quantity"]
                    # Выбираем максимальную цену
                    if product_data["price"] > existing_product.price:
                        existing_product.price = product_data["price"]
                    return existing_product

        # Создаем новый продукт
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    @property
    def price(self):
        """Геттер для цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float):
        """
        Сеттер для цены с проверкой положительного значения
        и подтверждением понижения цены (дополнительное задание).

        Args:
            new_price (float): Новая цена товара
        """
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        # Дополнительное задание: подтверждение понижения цены
        if new_price < self.__price:
            confirmation = input(
                f"Цена понижается с {self.__price} до {new_price}. Подтвердите изменение (y/n): "
            )
            if confirmation.lower() != "y":
                print("Изменение цены отменено.")
                return

        self.__price = new_price

    def __str__(self):
        """Строковое представление продукта."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __repr__(self):
        """Представление объекта для отладки."""
        return f"Product('{self.name}', '{self.description}', {self.price}, {self.quantity})"


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
        self.__products = products  # Приватный атрибут

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product):
        """
        Метод для добавления товара в категорию.

        Args:
            product (Product): Объект товара для добавления
        """
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError("Можно добавлять только объекты класса Product")

    @property
    def products(self):
        """
        Геттер для списка товаров.

        Returns:
            str: Строка с информацией о всех товарах категории
        """
        products_str = ""
        for product in self.__products:
            products_str += f"{product}\n"
        return products_str

    def get_products_list(self):
        """
        Метод для получения списка продуктов (для внутреннего использования).

        Returns:
            list: Список объектов Product
        """
        return self.__products

    def __str__(self):
        """Строковое представление категории."""
        return f"{self.name}, количество продуктов: {len(self.__products)}"

    def __repr__(self):
        """Представление объекта для отладки."""
        return f"Category('{self.name}', '{self.description}', {len(self.__products)} продуктов)"
