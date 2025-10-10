from unittest.mock import patch

import pytest

from src.product import Category, Product


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
        # Теперь products - это строка, проверяем содержимое
        assert "Test Product, 1000.0 руб. Остаток: 10 шт." in category.products
        # Для проверки количества продуктов используем get_products_list()
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
        # Для пустой категории products возвращает пустую строку
        assert category.products == ""
        assert len(category.get_products_list()) == 0
        assert Category.category_count == 1
        assert Category.product_count == 0


class TestIntegration_1:
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
        # Проверяем через геттер products (строка)
        assert "Phone, 50000.0 руб. Остаток: 10 шт." in category.products
        assert "Tablet, 30000.0 руб. Остаток: 5 шт." in category.products
        # Проверяем количество через get_products_list()
        assert len(category.get_products_list()) == 2

        # Изменение цены
        product1.price = 45000.0
        assert product1.price == 45000.0

        # Попытка установить невалидную цену
        product1.price = -1000
        assert product1.price == 45000.0  # Цена не должна измениться


class TestProductEnhanced:
    """Тесты для расширенной функциональности класса Product"""

    def test_private_price_attribute(self):
        """Тест приватности атрибута цены"""
        product = Product("Test", "Desc", 100.0, 5)

        # Проверяем, что доступ через геттер работает
        assert product.price == 100.0

        # Проверяем, что прямой доступ к приватному атрибуту невозможен
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

        # Проверяем, что цена не изменилась
        assert product.price == 100.0

        # Проверяем сообщение об ошибке
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out

    def test_price_setter_zero(self, capsys):
        """Тест сеттера цены с нулевым значением"""
        product = Product("Test", "Desc", 100.0, 5)
        product.price = 0

        # Проверяем, что цена не изменилась
        assert product.price == 100.0

        # Проверяем сообщение об ошибке
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
        """Тест класс-метода new_product с дубликатом (дополнительное задание)"""
        existing_products = [Product("Existing Product", "Desc", 100.0, 5)]

        duplicate_data = {
            "name": "Existing Product",  # Такое же имя
            "description": "New Desc",
            "price": 150.0,  # Более высокая цена
            "quantity": 3,
        }

        # Создаем "новый" продукт, который должен объединиться с существующим
        result = Product.new_product(duplicate_data, existing_products)

        # Проверяем, что вернулся существующий продукт
        assert result is existing_products[0]
        # Проверяем, что количество объединилось
        assert result.quantity == 8  # 5 + 3
        # Проверяем, что выбрана максимальная цена
        assert result.price == 150.0

    def test_class_method_new_product_without_duplicate(self):
        """Тест класс-метода new_product без дубликата"""
        existing_products = [Product("Existing Product", "Desc", 100.0, 5)]

        new_product_data = {
            "name": "Different Product",  # Другое имя
            "description": "New Desc",
            "price": 150.0,
            "quantity": 3,
        }

        result = Product.new_product(new_product_data, existing_products)

        # Проверяем, что создан новый продукт
        assert result is not existing_products[0]
        assert result.name == "Different Product"
        assert result.quantity == 3

    @patch("builtins.input", return_value="y")
    def test_price_decrease_confirmation_approved(self, mock_input, capsys):
        """Тест подтверждения понижения цены (пользователь согласен)"""
        product = Product("Test", "Desc", 100.0, 5)
        product.price = 80.0  # Понижение цены

        # Проверяем, что цена изменилась
        assert product.price == 80.0

        # Проверяем, что был запрос подтверждения
        mock_input.assert_called_once()

    @patch("builtins.input", return_value="n")
    def test_price_decrease_confirmation_denied(self, mock_input, capsys):
        """Тест подтверждения понижения цены (пользователь отказал)"""
        product = Product("Test", "Desc", 100.0, 5)
        product.price = 80.0  # Понижение цены

        # Проверяем, что цена НЕ изменилась
        assert product.price == 100.0

        # Проверяем, что был запрос подтверждения
        mock_input.assert_called_once()


class TestCategoryEnhanced:
    """Тесты для расширенной функциональности класса Category"""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом"""
        Category.category_count = 0
        Category.product_count = 0

    def test_private_products_attribute(self):
        """Тест приватности атрибута products"""
        product = Product("Test", "Desc", 100.0, 5)
        category = Category("Test Category", "Test Description", [product])

        # Проверяем, что прямой доступ к приватному атрибуту невозможен
        with pytest.raises(AttributeError):
            _ = category.__products

    def test_products_getter_format(self):
        """Тест формата вывода геттера products"""
        product1 = Product("Product1", "Desc1", 100.0, 5)
        product2 = Product("Product2", "Desc2", 200.0, 10)
        category = Category("Test Category", "Test Description", [product1, product2])

        products_output = category.products

        # Проверяем формат вывода
        assert "Product1, 100.0 руб. Остаток: 5 шт." in products_output
        assert "Product2, 200.0 руб. Остаток: 10 шт." in products_output
        assert products_output.count("\n") == 2  # Две строки + последний перенос

    def test_add_product_method(self):
        """Тест метода add_product"""
        category = Category("Test Category", "Test Description", [])
        initial_product_count = Category.product_count

        product = Product("New Product", "Desc", 100.0, 5)
        category.add_product(product)

        # Проверяем, что продукт добавлен (через геттер)
        assert "New Product, 100.0 руб. Остаток: 5 шт." in category.products

        # Проверяем увеличение счетчика товаров
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

        # Попытка добавить не-Product объект
        with pytest.raises(
            TypeError, match="Можно добавлять только объекты класса Product"
        ):
            category.add_product("not a product")


class TestIntegration_2:
    """Интеграционные тесты"""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом"""
        Category.category_count = 0
        Category.product_count = 0

    @patch("builtins.input", return_value="y")  # Мок для подтверждения понижения цены
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

        # Изменение цены (понижение - требует подтверждения)
        product1.price = 45000.0
        assert product1.price == 45000.0

        # Попытка установить невалидную цену
        product1.price = -1000
        assert product1.price == 45000.0  # Цена не должна измениться

    def test_duplicate_handling_in_workflow(self):
        """Тест обработки дубликатов в рабочем процессе"""
        # Создаем начальные продукты
        initial_products = [
            Product("Laptop", "Gaming laptop", 100000.0, 3),
            Product("Mouse", "Wireless mouse", 5000.0, 10),
        ]

        # Создаем категорию с начальными продуктами
        category = Category("Computers", "Computer equipment", initial_products.copy())

        # Создаем дубликат через класс-метод
        duplicate_data = {
            "name": "Laptop",
            "description": "Updated description",
            "price": 120000.0,  # Более высокая цена
            "quantity": 2,
        }

        # Добавляем через класс-метод с проверкой дубликатов
        updated_product = Product.new_product(
            duplicate_data, category.get_products_list()
        )

        # Проверяем, что это тот же продукт
        assert updated_product is initial_products[0]
        # Проверяем обновленные данные
        assert updated_product.quantity == 5  # 3 + 2
        assert updated_product.price == 120000.0  # Максимальная цена

    @patch("builtins.input", return_value="n")  # Мок для отказа в понижении цены
    def test_price_decrease_denied_in_workflow(self, mock_input):
        """Тест отказа от понижения цены в рабочем процессе"""
        product = Product("Test Product", "Test Description", 1000.0, 5)

        # Попытка понизить цену (пользователь отказывает)
        product.price = 800.0

        # Проверяем, что цена НЕ изменилась
        assert product.price == 1000.0

        # Проверяем, что был запрос подтверждения
        mock_input.assert_called_once()
