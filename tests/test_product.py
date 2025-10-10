import os
import sys
from unittest.mock import patch

import pytest

from src.product import Category, CategoryIterator, Product

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class TestProduct:
    """Тесты для класса Product"""

    def test_product_initialization(self):
        """Тест корректности инициализации объекта Product"""
        product = Product("Test Product", "Test Description", 1000.0, 10)

        assert product.name == "Test Product"
        assert product.description == "Test Description"
        assert product.price == 1000.0
        assert product.quantity == 10

    def test_product_attributes_types(self):
        """Тест типов атрибутов Product"""
        product = Product("Test", "Desc", 100.0, 5)

        assert isinstance(product.name, str)
        assert isinstance(product.description, str)
        assert isinstance(product.price, float)
        assert isinstance(product.quantity, int)


class TestCategory:
    """Тесты для класса Category"""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом"""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_initialization(self):
        """Тест корректности инициализации объекта Category"""
        product = Product("Test Product", "Test Description", 1000.0, 10)
        category = Category("Test Category", "Test Description", [product])

        assert category.name == "Test Category"
        assert category.description == "Test Description"
        assert "Test Product, 1000.0 руб. Остаток: 10 шт." in category.products
        assert len(category.get_products_list()) == 1

    def test_category_count(self):
        """Тест подсчета количества категорий"""
        initial_count = Category.category_count

        product = Product("Test", "Desc", 100.0, 5)
        category1 = Category("Category 1", "Desc 1", [product])
        category2 = Category("Category 2", "Desc 2", [product])

        assert Category.category_count == initial_count + 2
        assert category1.category_count == Category.category_count
        assert category2.category_count == Category.category_count

    def test_product_count(self):
        """Тест подсчета количества продуктов"""
        initial_count = Category.product_count

        product1 = Product("Product 1", "Desc 1", 100.0, 5)
        product2 = Product("Product 2", "Desc 2", 200.0, 3)
        product3 = Product("Product 3", "Desc 3", 300.0, 7)

        category1 = Category("Category 1", "Desc 1", [product1, product2])
        category2 = Category("Category 2", "Desc 2", [product3])

        expected_count = initial_count + 3
        assert Category.product_count == expected_count
        assert category1.product_count == expected_count
        assert category2.product_count == expected_count

    def test_empty_category(self):
        """Тест создания категории без продуктов"""
        category = Category("Empty Category", "Empty Description", [])

        assert category.name == "Empty Category"
        assert category.description == "Empty Description"
        assert category.products == ""
        assert len(category.get_products_list()) == 0
        assert Category.category_count == 1
        assert Category.product_count == 0


class TestIntegration:
    """Интеграционные тесты"""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом"""
        Category.category_count = 0
        Category.product_count = 0

    @patch("builtins.input", return_value="y")
    def test_complete_workflow(self, mock_input):
        """Тест полного рабочего процесса"""
        # Создание продуктов
        product1 = Product("Phone", "Smartphone", 50000.0, 10)
        product2 = Product("Tablet", "Tablet PC", 30000.0, 5)

        # Создание категории
        category = Category("Electronics", "Electronic devices", [product1])

        # Добавление второго продукта
        category.add_product(product2)

        # Проверка результатов
        assert category.category_count == 1
        assert category.product_count == 2
        assert "Phone, 50000.0 руб. Остаток: 10 шт." in category.products
        assert "Tablet, 30000.0 руб. Остаток: 5 шт." in category.products

        # Изменение цены
        product1.price = 45000.0
        assert product1.price == 45000.0

        # Попытка установить невалидную цену
        product1.price = -1000
        assert product1.price == 45000.0  # Цена не должна измениться


class TestProductEnhanced:
    """Расширенные тесты для класса Product"""

    def test_private_price_attribute(self):
        """Тест приватности атрибута цены"""
        product = Product("Test", "Desc", 100.0, 5)

        assert product.price == 100.0
        with pytest.raises(AttributeError):
            _ = product.__price

    def test_price_setter_positive(self):
        """Тест сеттера цены с положительным значением"""
        product = Product("Test", "Desc", 100.0, 5)
        product.price = 150.0
        assert product.price == 150.0

    def test_price_setter_negative(self, capsys):
        """Тест сеттера цены с отрицательным значением"""
        product = Product("Test", "Desc", 100.0, 5)
        product.price = -50.0

        assert product.price == 100.0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out

    def test_price_setter_zero(self, capsys):
        """Тест сеттера цены с нулевым значением"""
        product = Product("Test", "Desc", 100.0, 5)
        product.price = 0

        assert product.price == 100.0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out

    def test_class_method_new_product(self):
        """Тест класс-метода new_product"""
        product_data = {
            "name": "New Product",
            "description": "New Description",
            "price": 500.0,
            "quantity": 10,
        }
        product = Product.new_product(product_data)

        assert isinstance(product, Product)
        assert product.name == "New Product"
        assert product.description == "New Description"
        assert product.price == 500.0
        assert product.quantity == 10

    def test_class_method_new_product_with_duplicate(self):
        """Тест класс-метода new_product с дубликатом"""
        existing_products = [Product("Existing Product", "Desc", 100.0, 5)]

        duplicate_data = {
            "name": "Existing Product",
            "description": "New Desc",
            "price": 150.0,
            "quantity": 3,
        }

        result = Product.new_product(duplicate_data, existing_products)

        assert result is existing_products[0]
        assert result.quantity == 8
        assert result.price == 150.0

    def test_class_method_new_product_without_duplicate(self):
        """Тест класс-метода new_product без дубликата"""
        existing_products = [Product("Existing Product", "Desc", 100.0, 5)]

        new_product_data = {
            "name": "Different Product",
            "description": "New Desc",
            "price": 150.0,
            "quantity": 3,
        }

        result = Product.new_product(new_product_data, existing_products)

        assert result is not existing_products[0]
        assert result.name == "Different Product"
        assert result.quantity == 3

    @patch("builtins.input", return_value="y")
    def test_price_decrease_confirmation_approved(self, mock_input):
        """Тест подтверждения понижения цены (пользователь согласен)"""
        product = Product("Test", "Desc", 100.0, 5)
        product.price = 80.0

        assert product.price == 80.0
        mock_input.assert_called_once()

    @patch("builtins.input", return_value="n")
    def test_price_decrease_confirmation_denied(self, mock_input):
        """Тест подтверждения понижения цены (пользователь отказал)"""
        product = Product("Test", "Desc", 100.0, 5)
        product.price = 80.0

        assert product.price == 100.0
        mock_input.assert_called_once()


class TestCategoryEnhanced:
    """Расширенные тесты для класса Category"""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом"""
        Category.category_count = 0
        Category.product_count = 0

    def test_private_products_attribute(self):
        """Тест приватности атрибута products"""
        product = Product("Test", "Desc", 100.0, 5)
        category = Category("Test Category", "Test Description", [product])

        with pytest.raises(AttributeError):
            _ = category.__products

    def test_products_getter_format(self):
        """Тест формата вывода геттера products"""
        product1 = Product("Product1", "Desc1", 100.0, 5)
        product2 = Product("Product2", "Desc2", 200.0, 10)
        category = Category("Test Category", "Test Description", [product1, product2])

        products_output = category.products

        assert "Product1, 100.0 руб. Остаток: 5 шт." in products_output
        assert "Product2, 200.0 руб. Остаток: 10 шт." in products_output

    def test_add_product_method(self):
        """Тест метода add_product"""
        category = Category("Test Category", "Test Description", [])
        initial_product_count = Category.product_count

        product = Product("New Product", "Desc", 100.0, 5)
        category.add_product(product)

        assert "New Product, 100.0 руб. Остаток: 5 шт." in category.products
        assert Category.product_count == initial_product_count + 1

    def test_add_product_increases_count(self):
        """Тест, что add_product увеличивает product_count"""
        initial_count = Category.product_count

        category = Category("Test Category", "Test Description", [])
        product1 = Product("Product1", "Desc1", 100.0, 5)
        product2 = Product("Product2", "Desc2", 200.0, 10)

        category.add_product(product1)
        category.add_product(product2)

        assert Category.product_count == initial_count + 2

    def test_empty_category_products(self):
        """Тест геттера products для пустой категории"""
        category = Category("Empty Category", "Empty Description", [])
        assert category.products == ""

    def test_products_getter_returns_string(self):
        """Тест, что геттер products возвращает строку"""
        product = Product("Test", "Desc", 100.0, 5)
        category = Category("Test Category", "Test Description", [product])
        assert isinstance(category.products, str)

    def test_add_product_type_check(self):
        """Тест проверки типа в методе add_product"""
        category = Category("Test Category", "Test Description", [])

        with pytest.raises(
            TypeError, match="Можно добавлять только объекты класса Product"
        ):
            category.add_product("not a product")


class TestIntegrationEnhanced:
    """Интеграционные тесты для расширенной функциональности"""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом"""
        Category.category_count = 0
        Category.product_count = 0

    @patch("builtins.input", return_value="y")
    def test_complete_workflow(self, mock_input):
        """Тест полного рабочего процесса"""
        product1 = Product("Phone", "Smartphone", 50000.0, 10)
        product2 = Product("Tablet", "Tablet PC", 30000.0, 5)

        category = Category("Electronics", "Electronic devices", [product1])
        category.add_product(product2)

        assert category.category_count == 1
        assert category.product_count == 2
        assert "Phone, 50000.0 руб. Остаток: 10 шт." in category.products
        assert "Tablet, 30000.0 руб. Остаток: 5 шт." in category.products

        product1.price = 45000.0
        assert product1.price == 45000.0

        product1.price = -1000
        assert product1.price == 45000.0

    def test_duplicate_handling_in_workflow(self):
        """Тест обработки дубликатов в рабочем процессе"""
        initial_products = [
            Product("Laptop", "Gaming laptop", 100000.0, 3),
            Product("Mouse", "Wireless mouse", 5000.0, 10),
        ]

        category = Category("Computers", "Computer equipment", initial_products.copy())

        duplicate_data = {
            "name": "Laptop",
            "description": "Updated description",
            "price": 120000.0,
            "quantity": 2,
        }

        updated_product = Product.new_product(
            duplicate_data, category.get_products_list()
        )

        assert updated_product is initial_products[0]
        assert updated_product.quantity == 5
        assert updated_product.price == 120000.0

    @patch("builtins.input", return_value="n")
    def test_price_decrease_denied_in_workflow(self, mock_input):
        """Тест отказа от понижения цены в рабочем процессе"""
        product = Product("Test Product", "Test Description", 1000.0, 5)

        product.price = 800.0

        assert product.price == 1000.0
        mock_input.assert_called_once()


class TestProductMagicMethods:
    """Тесты для магических методов класса Product"""

    def test_product_str_method(self):
        """Тест строкового представления продукта"""
        product = Product("Test Product", "Test Description", 1000.0, 5)
        expected_str = "Test Product, 1000.0 руб. Остаток: 5 шт."
        assert str(product) == expected_str

    def test_product_str_with_zero_quantity(self):
        """Тест строкового представления продукта с нулевым количеством"""
        product = Product("Test Product", "Test Description", 1000.0, 0)
        expected_str = "Test Product, 1000.0 руб. Остаток: 0 шт."
        assert str(product) == expected_str

    def test_product_add_method(self):
        """Тест сложения двух продуктов"""
        product1 = Product("Product1", "Desc1", 100.0, 10)  # 100 * 10 = 1000
        product2 = Product("Product2", "Desc2", 200.0, 5)  # 200 * 5 = 1000
        result = product1 + product2
        assert result == 2000.0

    def test_product_add_commutative(self):
        """Тест коммутативности сложения продуктов"""
        product1 = Product("Product1", "Desc1", 100.0, 10)
        product2 = Product("Product2", "Desc2", 200.0, 5)
        result1 = product1 + product2
        result2 = product2 + product1
        assert result1 == result2

    def test_product_add_type_error(self):
        """Тест ошибки при сложении с неправильным типом"""
        product = Product("Test", "Desc", 100.0, 5)
        with pytest.raises(
            TypeError, match="Можно складывать только объекты класса Product"
        ):
            product + "not a product"

    def test_product_add_with_updated_price(self):
        """Тест сложения после изменения цены"""
        product1 = Product("Product1", "Desc1", 100.0, 10)  # 1000
        product2 = Product("Product2", "Desc2", 200.0, 5)  # 1000

        # Изменяем цену первого продукта
        product1.price = 150.0  # Теперь 150 * 10 = 1500
        result = product1 + product2
        assert result == 2500.0


class TestCategoryMagicMethods:
    """Тесты для магических методов класса Category"""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом"""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_str_method(self):
        """Тест строкового представления категории"""
        product1 = Product("Product1", "Desc1", 100.0, 10)
        product2 = Product("Product2", "Desc2", 200.0, 5)
        category = Category("Test Category", "Test Description", [product1, product2])

        # Общее количество: 10 + 5 = 15
        expected_str = "Test Category, количество продуктов: 15 шт."
        assert str(category) == expected_str

    def test_category_str_empty(self):
        """Тест строкового представления пустой категории"""
        category = Category("Empty Category", "Empty Description", [])
        expected_str = "Empty Category, количество продуктов: 0 шт."
        assert str(category) == expected_str

    def test_category_str_zero_quantities(self):
        """Тест строкового представления категории с товарами нулевого количества"""
        product1 = Product("Product1", "Desc1", 100.0, 0)
        product2 = Product("Product2", "Desc2", 200.0, 0)
        category = Category("Zero Category", "Zero Description", [product1, product2])
        expected_str = "Zero Category, количество продуктов: 0 шт."
        assert str(category) == expected_str

    def test_category_iterator(self):
        """Тест итератора категории"""
        product1 = Product("Product1", "Desc1", 100.0, 10)
        product2 = Product("Product2", "Desc2", 200.0, 5)
        product3 = Product("Product3", "Desc3", 300.0, 3)
        category = Category(
            "Test Category", "Test Description", [product1, product2, product3]
        )

        # Проверяем итерацию
        products_from_iterator = list(category)
        assert len(products_from_iterator) == 3
        assert products_from_iterator[0] == product1
        assert products_from_iterator[1] == product2
        assert products_from_iterator[2] == product3

    def test_category_iterator_empty(self):
        """Тест итератора пустой категории"""
        category = Category("Empty Category", "Empty Description", [])
        products_from_iterator = list(category)
        assert len(products_from_iterator) == 0

    def test_category_for_loop(self):
        """Тест использования категории в цикле for"""
        product1 = Product("Product1", "Desc1", 100.0, 10)
        product2 = Product("Product2", "Desc2", 200.0, 5)
        category = Category("Test Category", "Test Description", [product1, product2])

        # Используем в цикле for
        product_names = []
        for product in category:
            product_names.append(product.name)

        assert product_names == ["Product1", "Product2"]


class TestCategoryIteratorClass:
    """Тесты для класса CategoryIterator"""

    def test_iterator_creation(self):
        """Тест создания итератора"""
        products = [
            Product("Product1", "Desc1", 100.0, 10),
            Product("Product2", "Desc2", 200.0, 5),
        ]
        iterator = CategoryIterator(products)
        assert iterator.products == products
        assert iterator.index == 0

    def test_iterator_next(self):
        """Тест метода next итератора"""
        product1 = Product("Product1", "Desc1", 100.0, 10)
        product2 = Product("Product2", "Desc2", 200.0, 5)
        iterator = CategoryIterator([product1, product2])

        assert next(iterator) == product1
        assert next(iterator) == product2

        with pytest.raises(StopIteration):
            next(iterator)

    def test_iterator_iter(self):
        """Тест метода iter итератора"""
        products = [Product("Product1", "Desc1", 100.0, 10)]
        iterator = CategoryIterator(products)

        # Итератор должен возвращать сам себя при вызове iter()
        assert iter(iterator) is iterator


class TestIntegrationMagicMethods:
    """Интеграционные тесты магических методов"""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом"""
        Category.category_count = 0
        Category.product_count = 0

    @patch("builtins.input", return_value="y")
    def test_complete_workflow_with_magic_methods(self, mock_input):
        """Тест полного рабочего процесса с магическими методами"""
        # Создание продуктов
        laptop = Product("Ноутбук", "Игровой ноутбук", 150000.0, 3)
        monitor = Product("Монитор", "4K монитор", 50000.0, 7)
        keyboard = Product("Клавиатура", "Механическая", 5000.0, 15)

        # Создание категории
        computers = Category("Компьютеры", "Компьютерная техника", [laptop, monitor])

        # Проверка строкового представления
        assert str(laptop) == "Ноутбук, 150000.0 руб. Остаток: 3 шт."
        assert str(computers) == "Компьютеры, количество продуктов: 10 шт."

        # Проверка сложения
        total_value = laptop + monitor
        expected_value = (150000.0 * 3) + (50000.0 * 7)
        assert total_value == expected_value

        # Проверка итератора
        product_count = 0
        for product in computers:
            product_count += 1
            assert isinstance(product, Product)
        assert product_count == 2

        # Добавление нового продукта
        computers.add_product(keyboard)
        assert str(computers) == "Компьютеры, количество продуктов: 25 шт."

        # Проверка обновленного сложения (сложение попарно)
        total_laptop_monitor = laptop + monitor
        total_with_keyboard = total_laptop_monitor + (
            keyboard.price * keyboard.quantity
        )
        expected_all = expected_value + (5000.0 * 15)
        assert total_with_keyboard == expected_all

    def test_products_getter_still_works(self):
        """Тест что старый геттер products все еще работает"""
        product1 = Product("Product1", "Desc1", 100.0, 5)
        product2 = Product("Product2", "Desc2", 200.0, 3)
        category = Category("Test Category", "Test Description", [product1, product2])

        products_output = category.products
        assert "Product1, 100.0 руб. Остаток: 5 шт." in products_output
        assert "Product2, 200.0 руб. Остаток: 3 шт." in products_output
