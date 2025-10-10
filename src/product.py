class Product:
    """
    Класс для представления товара.

    Атрибуты:
        name (str): Название товара
        description (str): Описание товара
        __price (float): Приватная цена товара
        quantity (int): Количество товара в наличии
    """

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self):
        """Строковое представление продукта."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """
        Магический метод сложения для продуктов.

        Args:
            other (Product): Другой объект Product

        Returns:
            float: Сумма произведений цены на количество для двух продуктов

        Raises:
            TypeError: Если other не является объектом Product
        """
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")

        return (self.price * self.quantity) + (other.price * other.quantity)

    @classmethod
    def new_product(cls, product_data: dict, products_list: list = None):
        """
        Класс-метод для создания нового продукта из словаря.
        С проверкой дубликатов.
        """
        if products_list:
            for existing_product in products_list:
                if existing_product.name.lower() == product_data["name"].lower():
                    existing_product.quantity += product_data["quantity"]
                    if product_data["price"] > existing_product.price:
                        existing_product.price = product_data["price"]
                    return existing_product

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
        и подтверждением понижения цены.
        """
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        # Подтверждение понижения цены
        if new_price < self.__price:
            try:
                confirmation = input(
                    f"Цена понижается с {self.__price} до {new_price}. Подтвердите изменение (y/n): "
                )
                if confirmation.lower() != "y":
                    print("Изменение цены отменено.")
                    return
            except EOFError:
                # Для тестов, где input недоступен
                pass

        self.__price = new_price

    def __repr__(self):
        """Представление объекта для отладки."""
        return f"Product('{self.name}', '{self.description}', {self.price}, {self.quantity})"


class Category:
    """
    Класс для представления категории товаров.

    Атрибуты:
        name (str): Название категории
        description (str): Описание категории
        __products (list): Приватный список товаров категории
    """

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def __str__(self):
        """Строковое представление категории."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self):
        """Возвращает итератор для категории."""
        return CategoryIterator(self.__products)

    def add_product(self, product):
        """Метод для добавления товара в категорию."""
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError("Можно добавлять только объекты класса Product")

    @property
    def products(self):
        """Геттер для списка товаров в виде строки."""
        products_str = ""
        for product in self.__products:
            products_str += f"{product}\n"
        return products_str

    def get_products_list(self):
        """Метод для получения списка продуктов."""
        return self.__products

    def __repr__(self):
        """Представление объекта для отладки."""
        return f"Category('{self.name}', '{self.description}', {len(self.__products)} продуктов)"


class CategoryIterator:
    """
    Класс-итератор для перебора товаров в категории.
    """

    def __init__(self, products: list):
        self.products = products
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.products):
            product = self.products[self.index]
            self.index += 1
            return product
        else:
            raise StopIteration
