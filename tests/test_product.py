import os
import sys
from unittest.mock import patch

import pytest

from src.product import Category, CategoryIterator, LawnGrass, Product, Smartphone

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class TestProductComprehensive:
    """Исчерпывающие тесты для класса Product"""

    def test_product_repr(self):
        """Тест repr для Product"""
        product = Product("Test", "Description", 100.0, 5)
        repr_str = repr(product)
        assert "Product(" in repr_str
        assert "Test" in repr_str
        assert "100.0" in repr_str

    def test_product_str_with_special_characters(self):
        """Тест str со специальными символами в названии"""
        product = Product("Test & Special % Chars", "Desc", 100.0, 5)
        str_result = str(product)
        assert "Test & Special % Chars" in str_result

    def test_product_initialization_edge_cases(self):
        """Тест инициализации Product с граничными значениями"""
        # Нулевая цена (должна быть разрешена при инициализации, но не через сеттер)
        product = Product("Test", "Desc", 0.0, 5)
        assert product.price == 0.0

        # Очень большие числа
        product = Product("Test", "Desc", 9999999.99, 99999)
        assert product.price == 9999999.99
        assert product.quantity == 99999

    def test_product_equality(self):
        """Тест сравнения продуктов"""
        product1 = Product("Same", "Desc", 100.0, 5)
        product2 = Product("Same", "Desc", 100.0, 5)
        product3 = Product("Different", "Desc", 100.0, 5)

        # Продукты с одинаковыми данными - разные объекты
        assert product1 is not product2
        assert product1.name == product2.name
        assert product3.name != product1.name


class TestSmartphoneComprehensive:
    """Исчерпывающие тесты для класса Smartphone"""

    def test_smartphone_repr(self):
        """Тест repr для Smartphone"""
        smartphone = Smartphone(
            "Test Phone", "Description", 50000.0, 10, 3.5, "Test Model", 256, "Black"
        )
        repr_str = repr(smartphone)
        assert "Smartphone(" in repr_str
        assert "Test Phone" in repr_str
        assert "3.5" in repr_str
        assert "Test Model" in repr_str

    def test_smartphone_inheritance(self):
        """Тест наследования Smartphone от Product"""
        smartphone = Smartphone("Phone", "Desc", 1000.0, 5, 2.5, "M", 64, "B")

        # Проверяем наследование атрибутов
        assert hasattr(smartphone, "name")
        assert hasattr(smartphone, "price")
        assert hasattr(smartphone, "quantity")
        assert hasattr(smartphone, "efficiency")
        assert hasattr(smartphone, "model")
        assert hasattr(smartphone, "memory")
        assert hasattr(smartphone, "color")

        # Проверяем что это экземпляр обоих классов
        assert isinstance(smartphone, Smartphone)
        assert isinstance(smartphone, Product)

    def test_smartphone_edge_cases(self):
        """Тест граничных случаев для Smartphone"""
        # Нулевая производительность
        smartphone = Smartphone("Phone", "Desc", 1000.0, 5, 0.0, "M", 64, "B")
        assert smartphone.efficiency == 0.0

        # Нулевая память
        smartphone = Smartphone("Phone", "Desc", 1000.0, 5, 2.5, "M", 0, "B")
        assert smartphone.memory == 0


class TestLawnGrassComprehensive:
    """Исчерпывающие тесты для класса LawnGrass"""

    def test_lawn_grass_repr(self):
        """Тест repr для LawnGrass"""
        lawn_grass = LawnGrass(
            "Test Grass", "Description", 2000.0, 50, "Test Country", 21, "Green"
        )
        repr_str = repr(lawn_grass)
        assert "LawnGrass(" in repr_str
        assert "Test Grass" in repr_str
        assert "Test Country" in repr_str
        assert "21" in repr_str

    def test_lawn_grass_inheritance(self):
        """Тест наследования LawnGrass от Product"""
        lawn_grass = LawnGrass("Grass", "Desc", 1000.0, 10, "C", 14, "G")

        # Проверяем наследование атрибутов
        assert hasattr(lawn_grass, "name")
        assert hasattr(lawn_grass, "price")
        assert hasattr(lawn_grass, "quantity")
        assert hasattr(lawn_grass, "country")
        assert hasattr(lawn_grass, "germination_period")
        assert hasattr(lawn_grass, "color")

        # Проверяем что это экземпляр обоих классов
        assert isinstance(lawn_grass, LawnGrass)
        assert isinstance(lawn_grass, Product)

    def test_lawn_grass_edge_cases(self):
        """Тест граничных случаев для LawnGrass"""
        # Нулевой срок прорастания
        lawn_grass = LawnGrass("Grass", "Desc", 1000.0, 10, "C", 0, "G")
        assert lawn_grass.germination_period == 0

        # Пустая страна
        lawn_grass = LawnGrass("Grass", "Desc", 1000.0, 10, "", 14, "G")
        assert lawn_grass.country == ""


class TestCategoryComprehensive:
    """Исчерпывающие тесты для класса Category"""

    @staticmethod
    def setup_method():
        """Сброс счетчиков перед каждым тестом"""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_repr(self):
        """Тест repr для Category"""
        category = Category("Test Category", "Test Description", [])
        repr_str = repr(category)
        assert "Category(" in repr_str
        assert "Test Category" in repr_str

    def test_category_str_with_many_products(self):
        """Тест str для категории со многими продуктами"""
        products = [Product(f"Product{i}", "Desc", 100.0, i) for i in range(1, 6)]
        category = Category("Test Category", "Test Description", products)

        str_result = str(category)
        assert "количество продуктов: 15 шт." in str_result  # 1+2+3+4+5=15

    def test_category_empty_description(self):
        """Тест категории с пустым описанием"""
        category = Category("Test Category", "", [])
        assert category.description == ""

    def test_category_special_characters_in_name(self):
        """Тест категории со специальными символами в названии"""
        category = Category("Test & Category % Special", "Desc", [])
        assert "Test & Category % Special" in category.name


class TestCategoryIteratorComprehensive:
    """Исчерпывающие тесты для CategoryIterator"""

    def test_iterator_reuse(self):
        """Тест повторного использования итератора"""
        products = [
            Product("Product1", "Desc1", 100.0, 5),
            Product("Product2", "Desc2", 200.0, 3),
        ]
        category = Category("Test Category", "Test Description", products)

        # Первая итерация
        first_iteration = list(category)
        assert len(first_iteration) == 2

        # Вторая итерация (должна работать снова)
        second_iteration = list(category)
        assert len(second_iteration) == 2

        # Обе итерации должны содержать одинаковые продукты
        assert first_iteration == second_iteration

    def test_iterator_with_empty_list(self):
        """Тест итератора с пустым списком"""
        iterator = CategoryIterator([])

        # Должен сразу вызвать StopIteration
        with pytest.raises(StopIteration):
            next(iterator)

    def test_multiple_iterators_independent(self):
        """Тест, что несколько итераторов независимы"""
        products = [
            Product("Product1", "Desc1", 100.0, 5),
            Product("Product2", "Desc2", 200.0, 3),
            Product("Product3", "Desc3", 300.0, 2),
        ]
        category = Category("Test Category", "Test Description", products)

        # Создаем два итератора
        iter1 = iter(category)
        iter2 = iter(category)

        # Они должны работать независимо
        assert next(iter1) == products[0]
        assert next(iter2) == products[0]
        assert next(iter1) == products[1]
        assert next(iter2) == products[1]


class TestClassMethodComprehensive:
    """Исчерпывающие тесты для класс-методов"""

    def test_new_product_with_none_list(self):
        """Тест new_product с None в качестве списка"""
        product_data = {
            "name": "New Product",
            "description": "New Description",
            "price": 500.0,
            "quantity": 10,
        }

        product = Product.new_product(product_data, None)
        assert product.name == "New Product"
        assert product.quantity == 10

    def test_new_product_with_empty_list(self):
        """Тест new_product с пустым списком"""
        product_data = {
            "name": "New Product",
            "description": "New Description",
            "price": 500.0,
            "quantity": 10,
        }

        product = Product.new_product(product_data, [])
        assert product.name == "New Product"
        assert product.quantity == 10

    def test_new_product_case_insensitive_duplicate(self):
        """Тест new_product с дубликатом в разном регистре"""
        existing_products = [Product("Existing Product", "Desc", 100.0, 5)]

        duplicate_data = {
            "name": "EXISTING PRODUCT",  # В верхнем регистре
            "description": "New Desc",
            "price": 150.0,
            "quantity": 3,
        }

        result = Product.new_product(duplicate_data, existing_products)
        assert result is existing_products[0]
        assert result.quantity == 8  # 5 + 3


class TestAdditionComprehensive:
    """Исчерпывающие тесты для сложения"""

    def test_add_self(self):
        """Тест сложения продукта с самим собой"""
        product = Product("Test", "Desc", 100.0, 5)
        result = product + product
        assert result == 1000.0  # 100 * 5 * 2

    def test_add_with_zero_quantity(self):
        """Тест сложения с нулевым количеством"""
        product1 = Product("Test1", "Desc", 100.0, 0)  # 0
        product2 = Product("Test2", "Desc", 200.0, 5)  # 1000
        result = product1 + product2
        assert result == 1000.0

    def test_add_with_zero_price(self):
        """Тест сложения с нулевой ценой"""
        product1 = Product("Test1", "Desc", 0.0, 10)  # 0
        product2 = Product("Test2", "Desc", 200.0, 5)  # 1000
        result = product1 + product2
        assert result == 1000.0


class TestErrorMessages:
    """Тесты сообщений об ошибках"""

    def test_addition_error_message(self):
        """Тест сообщения об ошибке при сложении разных типов"""
        smartphone = Smartphone("Phone", "Desc", 1000.0, 5, 2.5, "M", 64, "B")
        lawn_grass = LawnGrass("Grass", "Desc", 500.0, 10, "C", 14, "G")

        with pytest.raises(TypeError) as exc_info:
            smartphone + lawn_grass

        assert "Нельзя складывать товары разных типов" in str(exc_info.value)

    def test_add_product_error_message(self):
        """Тест сообщения об ошибке при добавлении не-продукта"""
        category = Category("Test Category", "Test Description", [])

        with pytest.raises(TypeError) as exc_info:
            category.add_product("invalid")

        assert (
            "Можно добавлять только объекты класса Product или его наследников"
            in str(exc_info.value)
        )


class TestPriceSetterComprehensive:
    """Исчерпывающие тесты для сеттера цены"""

    def test_price_increase_no_confirmation(self):
        """Тест увеличения цены без подтверждения"""
        product = Product("Test", "Desc", 100.0, 5)

        # Увеличение цены не требует подтверждения
        product.price = 150.0
        assert product.price == 150.0

    @patch("builtins.input", return_value="Y")  # Заглавная Y
    def test_price_decrease_uppercase_confirmation(self, mock_input):
        """Тест подтверждения понижения цены с заглавной Y"""
        product = Product("Test", "Desc", 100.0, 5)
        product.price = 80.0
        assert product.price == 80.0

    @patch("builtins.input", return_value="yes")  # Длинный ответ
    def test_price_decrease_long_confirmation(self, mock_input):
        """Тест подтверждения понижения цены с длинным ответом"""
        product = Product("Test", "Desc", 100.0, 5)
        product.price = 80.0
        # Должен отказать, так как ожидается только 'y'
        assert product.price == 100.0

    @patch("builtins.input", return_value="y")
    def test_price_setter_with_very_small_value(self, mock_input):
        """Тест сеттера цены с очень маленьким значением"""
        product = Product("Test", "Desc", 100.0, 5)

        # Очень маленькая, но положительная цена
        product.price = 0.01
        assert product.price == 0.01

        # Отрицательная цена (должна быть отклонена)
        product.price = -0.01
        assert product.price == 0.01


class TestIntegrationScenarios:
    """Сложные интеграционные сценарии"""

    def test_complex_category_operations(self):
        """Тест сложных операций с категориями"""
        # Создаем разнообразные продукты
        basic_products = [
            Product(f"Basic{i}", f"Desc{i}", i * 100.0, i) for i in range(1, 4)
        ]
        smartphones = [
            Smartphone(
                f"Phone{i}",
                f"Desc{i}",
                i * 50000.0,
                i,
                i * 0.5,
                f"Model{i}",
                i * 64,
                f"Color{i}",
            )
            for i in range(1, 3)
        ]
        lawn_grasses = [
            LawnGrass(
                f"Grass{i}",
                f"Desc{i}",
                i * 2000.0,
                i * 10,
                f"Country{i}",
                i * 7,
                f"Color{i}",
            )
            for i in range(1, 3)
        ]

        # Создаем категорию со всеми продуктами
        all_products = basic_products + smartphones + lawn_grasses
        category = Category("Mixed Category", "Mixed products", all_products)

        # Проверяем общее количество
        assert len(category.get_products_list()) == 7

        # Проверяем строковое представление
        str_result = str(category)
        assert "Mixed Category, количество продуктов:" in str_result

        # Проверяем итерацию
        iterated_products = list(category)
        assert len(iterated_products) == 7

        # Проверяем сложение для каждого типа
        basic_sum = basic_products[0] + basic_products[1]
        phone_sum = smartphones[0] + smartphones[1]
        grass_sum = lawn_grasses[0] + lawn_grasses[1]

        assert basic_sum > 0
        assert phone_sum > 0
        assert grass_sum > 0

    def test_category_counters_accuracy(self):
        """Тест точности счетчиков категорий и продуктов"""
        # Сбрасываем счетчики
        Category.category_count = 0
        Category.product_count = 0

        # Создаем несколько категорий с продуктами
        categories = []
        for i in range(3):
            products = [Product(f"P{i}{j}", "Desc", 100.0, 1) for j in range(i + 1)]
            category = Category(f"Category{i}", "Desc", products)
            categories.append(category)

        # Проверяем счетчики
        assert Category.category_count == 3
        assert Category.product_count == 6  # 1 + 2 + 3 = 6

        # Добавляем еще продукты в существующие категории
        categories[0].add_product(Product("New1", "Desc", 100.0, 1))
        categories[1].add_product(Product("New2", "Desc", 100.0, 1))

        # Проверяем обновленные счетчики
        assert Category.product_count == 8  # 6 + 2 = 8
