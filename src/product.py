from abc import ABC, abstractmethod


class LoggingMixin:
    """
    Миксин для логирования создания объектов.
    """

    def __init__(self, *args, **kwargs):
        """
        Инициализация миксина с логированием параметров создания.
        """
        super().__init__(*args, **kwargs)
        class_name = self.__class__.__name__
        params = []

        # Собираем параметры из args
        if args:
            params.extend(repr(arg) for arg in args)

        # Собираем параметры из kwargs
        if kwargs:
            params.extend(f"{key}={repr(value)}" for key, value in kwargs.items())

        params_str = ", ".join(params)
        print(f"Создан объект {class_name}({params_str})")


class BaseProduct(ABC):
    """
    Абстрактный базовый класс для всех продуктов.

    Определяет общий интерфейс для всех продуктов.
    """

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Абстрактный конструктор для продуктов.

        Args:
            name: Название продукта
            description: Описание продукта
            price: Цена продукта
            quantity: Количество продукта
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Абстрактное свойство для названия продукта."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Абстрактное свойство для описания продукта."""
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        """Абстрактное свойство для цены продукта."""
        pass

    @price.setter
    @abstractmethod
    def price(self, value: float):
        """Абстрактный сеттер для цены."""
        pass

    @property
    @abstractmethod
    def quantity(self) -> int:
        """Абстрактное свойство для количества продукта."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Абстрактный метод строкового представления."""
        pass

    @abstractmethod
    def __add__(self, other) -> float:
        """Абстрактный метод сложения продуктов."""
        pass

    @classmethod
    @abstractmethod
    def new_product(cls, product_data: dict, products_list: list = None):
        """Абстрактный класс-метод создания нового продукта."""
        pass


class Product(LoggingMixin, BaseProduct):
    """
    Конкретный класс продукта, наследуемый от BaseProduct с миксином.

    Атрибуты:
        name (str): Название товара
        description (str): Описание товара
        __price (float): Приватная цена товара
        quantity (int): Количество товара в наличии
    """

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self._name = name
        self._description = description
        self.__price = price
        self._quantity = quantity
        super().__init__(name, description, price, quantity)

    def __str__(self):
        """Строковое представление продукта."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """
        Магический метод сложения для продуктов.

        Returns:
            float: Сумма произведений цены на количество для двух продуктов
        """
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных типов")

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
    def name(self) -> str:
        """Геттер для названия."""
        return self._name

    @property
    def description(self) -> str:
        """Геттер для описания."""
        return self._description

    @property
    def price(self) -> float:
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

    @property
    def quantity(self) -> int:
        """Геттер для количества."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        """Сеттер для количества."""
        if value < 0:
            raise ValueError("Количество не может быть отрицательным")
        self._quantity = value

    def __repr__(self):
        """Представление объекта для отладки."""
        return f"Product('{self.name}', '{self.description}', {self.price}, {self.quantity})"


class Smartphone(Product):
    """
    Класс для представления смартфона.

    Наследует от Product и добавляет:
        efficiency (float): Производительность
        model (str): Модель
        memory (int): Объем встроенной памяти (ГБ)
        color (str): Цвет
    """

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __repr__(self):
        """Представление объекта для отладки."""
        return (
            f"Smartphone('{self.name}', '{self.description}', {self.price}, {self.quantity}, "
            f"{self.efficiency}, '{self.model}', {self.memory}, '{self.color}')"
        )


class LawnGrass(Product):
    """
    Класс для представления газонной травы.

    Наследует от Product и добавляет:
        country (str): Страна-производитель
        germination_period (int): Срок прорастания (дни)
        color (str): Цвет
    """

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: int,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __repr__(self):
        """Представление объекта для отладки."""
        return (
            f"LawnGrass('{self.name}', '{self.description}', {self.price}, {self.quantity}, "
            f"'{self.country}', {self.germination_period}, '{self.color}')"
        )


class Container(ABC):
    """
    Абстрактный базовый класс для контейнеров, содержащих продукты.

    Определяет общий интерфейс для категорий и заказов.
    """

    @abstractmethod
    def get_total_price(self) -> float:
        """Абстрактный метод для получения общей стоимости."""
        pass

    @abstractmethod
    def get_products_count(self) -> int:
        """Абстрактный метод для получения количества продуктов."""
        pass

    @abstractmethod
    def __len__(self) -> int:
        """Абстрактный метод для получения длины контейнера."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Абстрактный метод строкового представления."""
        pass


class Category(Container):
    """
    Класс для представления категории товаров.

    Наследует от Container.

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
        self.__products = []

        # Добавляем продукты через метод для проверки типов
        for product in products:
            self.add_product(product)

        Category.category_count += 1

    def __str__(self):
        """Строковое представление категории."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __len__(self):
        """Возвращает количество продуктов в категории."""
        return len(self.__products)

    def __iter__(self):
        """Возвращает итератор для категории."""
        return CategoryIterator(self.__products)

    def add_product(self, product):
        """
        Метод для добавления товара в категорию.
        """
        if not isinstance(product, Product):
            raise TypeError(
                "Можно добавлять только объекты класса Product или его наследников"
            )

        self.__products.append(product)
        Category.product_count += 1

    def get_total_price(self) -> float:
        """Возвращает общую стоимость всех продуктов в категории."""
        return sum(product.price * product.quantity for product in self.__products)

    def get_products_count(self) -> int:
        """Возвращает количество уникальных продуктов в категории."""
        return len(self.__products)

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


class Order(Container):
    """
    Класс для представления заказа.

    Наследует от Container.

    Атрибуты:
        product (Product): Товар в заказе
        quantity (int): Количество товара в заказе
        order_id (str): Уникальный идентификатор заказа
    """

    order_count = 0

    def __init__(self, product: Product, quantity: int, order_id: str = None):
        if not isinstance(product, Product):
            raise TypeError(
                "Заказ может содержать только объекты класса Product или его наследников"
            )

        if quantity <= 0:
            raise ValueError("Количество товара в заказе должно быть положительным")

        if quantity > product.quantity:
            raise ValueError("Недостаточно товара на складе")

        self.product = product
        self.quantity = quantity
        self.order_id = order_id or f"ORDER_{Order.order_count + 1:06d}"

        Order.order_count += 1

    def get_total_price(self) -> float:
        """Возвращает общую стоимость заказа."""
        return self.product.price * self.quantity

    def get_products_count(self) -> int:
        """Возвращает количество продуктов в заказе (всегда 1)."""
        return 1

    def __len__(self) -> int:
        """Возвращает количество позиций в заказе (всегда 1)."""
        return 1

    def __str__(self) -> str:
        """Строковое представление заказа."""
        return f"Заказ {self.order_id}: {self.product.name} x {self.quantity} = {self.get_total_price()} руб."

    def __repr__(self) -> str:
        """Представление объекта для отладки."""
        return f"Order({repr(self.product)}, {self.quantity}, '{self.order_id}')"


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
