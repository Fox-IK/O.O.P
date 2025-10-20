import os
import sys
from abc import ABC
from unittest.mock import patch

import pytest

from src.product import (
    BaseProduct,
    Category,
    CategoryIterator,
    Container,
    LawnGrass,
    Order,
    Product,
    Smartphone,
)

# Добавляем путь к корневой директории проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


class TestBaseProduct:
    """Тесты для абстрактного базового класса BaseProduct."""

    def test_base_product_is_abstract(self):
        """Тест что BaseProduct является абстрактным классом."""
        assert issubclass(BaseProduct, ABC)

        # Проверяем что все абстрактные методы определены
        abstract_methods = {
            "__init__",
            "name",
            "description",
            "price",
            "quantity",
            "__str__",
            "__add__",
            "new_product",
        }

        for method_name in abstract_methods:
            method = getattr(BaseProduct, method_name, None)
            if method_name in ["name", "description", "price", "quantity"]:
                # Это свойства
                assert hasattr(
                    method, "fget"
                ), f"Property {method_name} should have getter"
                if method_name == "price":
                    assert hasattr(method, "fset"), "Price should have setter"
            else:
                assert hasattr(
                    method, "__isabstractmethod__"
                ), f"Method {method_name} should be abstract"

    def test_cannot_instantiate_base_product(self):
        """Тест что нельзя создать экземпляр абстрактного класса."""
        with pytest.raises(TypeError):
            BaseProduct("Test", "Description", 100.0, 5)


class TestProduct:
    """Тесты для класса Product."""

    def setup_method(self):
        """Сброс состояния перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_product_creation(self):
        """Тест создания продукта со всеми параметрами."""
        product = Product("Test Product", "Test Description", 1000.0, 5)

        assert product.name == "Test Product"
        assert product.description == "Test Description"
        assert product.price == 1000.0
        assert product.quantity == 5

    def test_product_repr(self):
        """Тест строкового представления для отладки."""
        product = Product("Test", "Description", 100.0, 5)
        repr_str = repr(product)

        assert "Product(" in repr_str
        assert "'Test'" in repr_str
        assert "'Description'" in repr_str
        assert "100.0" in repr_str
        assert "5" in repr_str

    def test_product_str(self):
        """Тест строкового представления для пользователя."""
        product = Product("Test Product", "Description", 150.5, 3)
        str_representation = str(product)

        assert "Test Product" in str_representation
        assert "150.5" in str_representation
        assert "3" in str_representation

    def test_product_price_setter_positive(self):
        """Тест установки положительной цены."""
        product = Product("Test", "Desc", 100.0, 5)
        product.price = 150.0
        assert product.price == 150.0

    @patch("builtins.input", return_value="y")
    def test_product_price_setter_decrease_with_confirmation(self, mock_input):
        """Тест понижения цены с подтверждением."""
        product = Product("Test", "Desc", 100.0, 5)
        product.price = 80.0
        assert product.price == 80.0
        mock_input.assert_called_once()

    @patch("builtins.input", return_value="n")
    def test_product_price_setter_decrease_without_confirmation(self, mock_input):
        """Тест понижения цены без подтверждения."""
        product = Product("Test", "Desc", 100.0, 5)
        product.price = 80.0
        # Цена не должна измениться
        assert product.price == 100.0
        mock_input.assert_called_once()

    def test_product_price_setter_negative(self):
        """Тест установки отрицательной цены."""
        product = Product("Test", "Desc", 100.0, 5)
        product.price = -50.0
        # Цена не должна измениться
        assert product.price == 100.0

    def test_product_price_setter_zero(self):
        """Тест установки нулевой цены."""
        product = Product("Test", "Desc", 100.0, 5)
        product.price = 0.0
        # Цена не должна измениться
        assert product.price == 100.0

    def test_product_quantity_setter_positive(self):
        """Тест установки положительного количества."""
        product = Product("Test", "Desc", 100.0, 5)
        product.quantity = 10
        assert product.quantity == 10

    def test_product_quantity_setter_negative(self):
        """Тест установки отрицательного количества."""
        product = Product("Test", "Desc", 100.0, 5)
        with pytest.raises(ValueError, match="Количество не может быть отрицательным"):
            product.quantity = -5

    def test_product_quantity_setter_zero(self):
        """Тест установки нулевого количества."""
        product = Product("Test", "Desc", 100.0, 5)
        product.quantity = 0
        assert product.quantity == 0

    def test_product_addition_same_type(self):
        """Тест сложения продуктов одного типа."""
        product1 = Product("Product1", "Desc", 100.0, 5)
        product2 = Product("Product2", "Desc", 200.0, 3)
        result = product1 + product2
        expected = (100.0 * 5) + (200.0 * 3)
        assert result == expected

    def test_product_addition_different_type(self):
        """Тест сложения продуктов разных типов."""
        product = Product("Product", "Desc", 100.0, 5)
        smartphone = Smartphone("Phone", "Desc", 50000.0, 2, 3.0, "M", 128, "B")
        with pytest.raises(TypeError, match="Нельзя складывать товары разных типов"):
            product + smartphone

    def test_product_addition_with_non_product(self):
        """Тест сложения продукта с не-продуктом."""
        product = Product("Product", "Desc", 100.0, 5)
        with pytest.raises(TypeError):
            product + "not a product"

    def test_new_product_without_duplicates(self):
        """Тест создания нового продукта без дубликатов."""
        product_data = {
            "name": "New Product",
            "description": "New Description",
            "price": 500.0,
            "quantity": 10,
        }
        product = Product.new_product(product_data)
        assert product.name == "New Product"
        assert product.description == "New Description"
        assert product.price == 500.0
        assert product.quantity == 10

    def test_new_product_with_duplicates(self):
        """Тест создания нового продукта с дубликатами."""
        existing_products = [Product("Existing Product", "Desc", 100.0, 5)]
        duplicate_data = {
            "name": "Existing Product",  # То же имя
            "description": "New Description",
            "price": 150.0,  # Более высокая цена
            "quantity": 3,
        }
        # Создаем "новый" продукт, который должен объединиться с существующим
        result = Product.new_product(duplicate_data, existing_products)
        # Должен вернуться существующий продукт
        assert result is existing_products[0]
        # Количество должно увеличиться
        assert result.quantity == 8  # 5 + 3
        # Цена должна обновиться до более высокой
        assert result.price == 150.0

    def test_new_product_with_duplicates_lower_price(self):
        """Тест создания дубликата с более низкой ценой."""
        existing_products = [Product("Existing Product", "Desc", 100.0, 5)]
        duplicate_data = {
            "name": "Existing Product",
            "description": "New Description",
            "price": 80.0,  # Более низкая цена
            "quantity": 3,
        }
        result = Product.new_product(duplicate_data, existing_products)
        # Цена не должна измениться
        assert result.price == 100.0
        # Количество должно увеличиться
        assert result.quantity == 8

    def test_new_product_with_empty_products_list(self):
        """Тест создания нового продукта с пустым списком продуктов."""
        product_data = {
            "name": "New Product",
            "description": "New Description",
            "price": 500.0,
            "quantity": 10,
        }
        product = Product.new_product(product_data, [])
        assert product.name == "New Product"
        assert product.quantity == 10

    def test_new_product_with_none_products_list(self):
        """Тест создания нового продукта с None в качестве списка продуктов."""
        product_data = {
            "name": "New Product",
            "description": "New Description",
            "price": 500.0,
            "quantity": 10,
        }
        product = Product.new_product(product_data, None)
        assert product.name == "New Product"
        assert product.quantity == 10

    def test_product_inherits_from_base_product(self):
        """Тест что Product наследуется от BaseProduct."""
        assert issubclass(Product, BaseProduct)


class TestSmartphone:
    """Тесты для класса Smartphone."""

    def test_smartphone_creation(self):
        """Тест создания смартфона со всеми параметрами."""
        smartphone = Smartphone(
            "Test Phone",
            "Test Description",
            50000.0,
            10,
            3.5,
            "Test Model",
            256,
            "Black",
        )
        assert smartphone.name == "Test Phone"
        assert smartphone.description == "Test Description"
        assert smartphone.price == 50000.0
        assert smartphone.quantity == 10
        assert smartphone.efficiency == 3.5
        assert smartphone.model == "Test Model"
        assert smartphone.memory == 256
        assert smartphone.color == "Black"

    def test_smartphone_repr(self):
        """Тест строкового представления смартфона для отладки."""
        smartphone = Smartphone("Phone", "Desc", 50000.0, 5, 3.5, "Model", 128, "Black")
        repr_str = repr(smartphone)
        assert "Smartphone(" in repr_str
        assert "'Phone'" in repr_str
        assert "3.5" in repr_str
        assert "'Model'" in repr_str
        assert "128" in repr_str
        assert "'Black'" in repr_str

    def test_smartphone_addition_same_type(self):
        """Тест сложения смартфонов одного типа."""
        phone1 = Smartphone("Phone1", "Desc", 50000.0, 2, 3.0, "M1", 128, "B")
        phone2 = Smartphone("Phone2", "Desc", 60000.0, 3, 3.5, "M2", 256, "W")
        result = phone1 + phone2
        expected = (50000.0 * 2) + (60000.0 * 3)
        assert result == expected

    def test_smartphone_addition_different_type(self):
        """Тест сложения смартфона с другим типом продукта."""
        smartphone = Smartphone("Phone", "Desc", 50000.0, 2, 3.0, "M", 128, "B")
        product = Product("Product", "Desc", 100.0, 5)
        with pytest.raises(TypeError):
            smartphone + product

    def test_smartphone_inherits_from_product(self):
        """Тест что Smartphone наследуется от Product."""
        assert issubclass(Smartphone, Product)


class TestLawnGrass:
    """Тесты для класса LawnGrass."""

    def test_lawn_grass_creation(self):
        """Тест создания газонной травы со всеми параметрами."""
        lawn_grass = LawnGrass(
            "Test Grass", "Test Description", 2000.0, 50, "Russia", 21, "Green"
        )
        assert lawn_grass.name == "Test Grass"
        assert lawn_grass.description == "Test Description"
        assert lawn_grass.price == 2000.0
        assert lawn_grass.quantity == 50
        assert lawn_grass.country == "Russia"
        assert lawn_grass.germination_period == 21
        assert lawn_grass.color == "Green"

    def test_lawn_grass_repr(self):
        """Тест строкового представления газонной травы для отладки."""
        lawn_grass = LawnGrass("Grass", "Desc", 1500.0, 25, "Germany", 14, "Dark Green")
        repr_str = repr(lawn_grass)
        assert "LawnGrass(" in repr_str
        assert "'Grass'" in repr_str
        assert "'Germany'" in repr_str
        assert "14" in repr_str
        assert "'Dark Green'" in repr_str

    def test_lawn_grass_addition_same_type(self):
        """Тест сложения газонных трав одного типа."""
        grass1 = LawnGrass("Grass1", "Desc", 1000.0, 10, "C1", 14, "G1")
        grass2 = LawnGrass("Grass2", "Desc", 1500.0, 5, "C2", 21, "G2")
        result = grass1 + grass2
        expected = (1000.0 * 10) + (1500.0 * 5)
        assert result == expected

    def test_lawn_grass_addition_different_type(self):
        """Тест сложения газонной травы с другим типом продукта."""
        lawn_grass = LawnGrass("Grass", "Desc", 1000.0, 10, "C", 14, "G")
        smartphone = Smartphone("Phone", "Desc", 50000.0, 2, 3.0, "M", 128, "B")
        with pytest.raises(TypeError):
            lawn_grass + smartphone

    def test_lawn_grass_inherits_from_product(self):
        """Тест что LawnGrass наследуется от Product."""
        assert issubclass(LawnGrass, Product)


class TestCategory:
    """Тесты для класса Category."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_creation(self):
        """Тест создания категории."""
        product = Product("Test Product", "Description", 100.0, 5)
        category = Category("Test Category", "Test Description", [product])
        assert category.name == "Test Category"
        assert category.description == "Test Description"
        assert len(category) == 1
        assert Category.category_count == 1

    def test_category_creation_empty(self):
        """Тест создания пустой категории."""
        category = Category("Empty Category", "Description", [])
        assert category.name == "Empty Category"
        assert len(category) == 0
        assert category.get_products_count() == 0
        assert category.get_total_price() == 0.0

    def test_category_str(self):
        """Тест строкового представления категории."""
        product = Product("Product", "Desc", 100.0, 5)
        category = Category("Category", "Description", [product])
        str_repr = str(category)
        assert "Category" in str_repr
        assert "количество продуктов: 5 шт." in str_repr

    def test_category_repr(self):
        """Тест представления категории для отладки."""
        category = Category("Test Category", "Test Description", [])
        repr_str = repr(category)
        assert "Category(" in repr_str
        assert "'Test Category'" in repr_str
        assert "'Test Description'" in repr_str

    def test_category_add_product(self):
        """Тест добавления продукта в категорию."""
        category = Category("Category", "Description", [])
        product = Product("Product", "Desc", 100.0, 5)
        initial_count = Category.product_count
        category.add_product(product)
        assert len(category) == 1
        assert Category.product_count == initial_count + 1

    def test_category_add_invalid_product(self):
        """Тест добавления невалидного продукта в категорию."""
        category = Category("Category", "Description", [])
        with pytest.raises(
            TypeError,
            match="Можно добавлять только объекты класса Product или его наследников",
        ):
            category.add_product("not a product")

    def test_category_products_property(self):
        """Тест свойства products."""
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)
        category = Category("Category", "Description", [product1, product2])
        products_str = category.products
        assert "Product1" in products_str
        assert "Product2" in products_str
        assert "100.0" in products_str
        assert "200.0" in products_str

    def test_category_get_products_list(self):
        """Тест метода get_products_list."""
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)
        category = Category("Category", "Description", [product1, product2])
        products_list = category.get_products_list()
        assert len(products_list) == 2
        assert product1 in products_list
        assert product2 in products_list

    def test_category_get_total_price(self):
        """Тест расчета общей стоимости категории."""
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)
        category = Category("Category", "Description", [product1, product2])
        total_price = category.get_total_price()
        expected = (100.0 * 2) + (200.0 * 3)
        assert total_price == expected

    def test_category_get_products_count(self):
        """Тест получения количества продуктов в категории."""
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)
        category = Category("Category", "Description", [product1, product2])
        assert category.get_products_count() == 2

    def test_category_iteration(self):
        """Тест итерации по категории."""
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)
        category = Category("Category", "Description", [product1, product2])
        products = list(category)
        assert len(products) == 2
        assert product1 in products
        assert product2 in products

    def test_category_multiple_iterations(self):
        """Тест множественных итераций по категории."""
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)
        category = Category("Category", "Description", [product1, product2])
        # Первая итерация
        first_iteration = list(category)
        assert len(first_iteration) == 2
        # Вторая итерация (должна работать с начала)
        second_iteration = list(category)
        assert len(second_iteration) == 2
        assert first_iteration == second_iteration

    def test_category_count_increment(self):
        """Тест увеличения счетчика категорий."""
        initial_count = Category.category_count
        # Создаем категории без присваивания переменным
        Category("Category1", "Desc", [])
        assert Category.category_count == initial_count + 1
        Category("Category2", "Desc", [])
        assert Category.category_count == initial_count + 2

    def test_category_inherits_from_container(self):
        """Тест что Category наследуется от Container."""
        assert issubclass(Category, Container)


class TestOrder:
    """Тесты для класса Order."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Order.order_count = 0

    def test_order_creation(self):
        """Тест создания заказа."""
        product = Product("Test Product", "Description", 1000.0, 10)
        order = Order(product, 3)
        assert order.product == product
        assert order.quantity == 3
        assert order.get_total_price() == 3000.0
        assert Order.order_count == 1

    def test_order_creation_with_order_id(self):
        """Тест создания заказа с указанием ID."""
        product = Product("Product", "Desc", 1000.0, 10)
        order = Order(product, 2, "CUSTOM_ORDER_001")
        assert order.order_id == "CUSTOM_ORDER_001"

    def test_order_creation_auto_order_id(self):
        """Тест автоматической генерации ID заказа."""
        product = Product("Product", "Desc", 1000.0, 10)
        order1 = Order(product, 1)
        order2 = Order(product, 1)
        assert order1.order_id != order2.order_id
        assert "ORDER_" in order1.order_id
        assert "ORDER_" in order2.order_id

    def test_order_creation_insufficient_quantity(self):
        """Тест создания заказа с недостаточным количеством."""
        product = Product("Product", "Desc", 1000.0, 5)
        with pytest.raises(ValueError, match="Недостаточно товара на складе"):
            Order(product, 10)

    def test_order_creation_zero_quantity(self):
        """Тест создания заказа с нулевым количеством."""
        product = Product("Product", "Desc", 1000.0, 5)
        with pytest.raises(
            ValueError, match="Количество товара в заказе должно быть положительным"
        ):
            Order(product, 0)

    def test_order_creation_negative_quantity(self):
        """Тест создания заказа с отрицательным количеством."""
        product = Product("Product", "Desc", 1000.0, 5)
        with pytest.raises(
            ValueError, match="Количество товара в заказе должно быть положительным"
        ):
            Order(product, -1)

    def test_order_creation_invalid_product(self):
        """Тест создания заказа с невалидным продуктом."""
        with pytest.raises(
            TypeError,
            match="Заказ может содержать только объекты класса Product или его наследников",
        ):
            Order("not a product", 1)

    def test_order_str(self):
        """Тест строкового представления заказа."""
        product = Product("Test Product", "Description", 1000.0, 10)
        order = Order(product, 3)
        str_repr = str(order)
        assert "Заказ" in str_repr
        assert "Test Product" in str_repr
        assert "3" in str_repr
        assert "3000" in str_repr

    def test_order_repr(self):
        """Тест представления заказа для отладки."""
        product = Product("Product", "Desc", 1000.0, 10)
        order = Order(product, 2, "TEST_ORDER")
        repr_str = repr(order)
        assert "Order(" in repr_str
        assert "Product(" in repr_str
        assert "2" in repr_str
        assert "'TEST_ORDER'" in repr_str

    def test_order_get_total_price(self):
        """Тест расчета общей стоимости заказа."""
        product = Product("Product", "Desc", 500.0, 10)
        order = Order(product, 4)
        assert order.get_total_price() == 2000.0

    def test_order_get_products_count(self):
        """Тест получения количества продуктов в заказе."""
        product = Product("Product", "Desc", 1000.0, 10)
        order = Order(product, 3)
        # В заказе всегда 1 продукт (но может быть разное количество)
        assert order.get_products_count() == 1

    def test_order_len(self):
        """Тест длины заказа."""
        product = Product("Product", "Desc", 1000.0, 10)
        order = Order(product, 3)
        # Длина заказа всегда 1 (одна позиция)
        assert len(order) == 1

    def test_order_count_increment(self):
        """Тест увеличения счетчика заказов."""
        product = Product("Product", "Desc", 1000.0, 10)
        initial_count = Order.order_count
        # Создаем заказы без присваивания переменным
        Order(product, 1)
        assert Order.order_count == initial_count + 1
        Order(product, 1)
        assert Order.order_count == initial_count + 2

    def test_order_inherits_from_container(self):
        """Тест что Order наследуется от Container."""
        assert issubclass(Order, Container)


class TestCategoryIterator:
    """Тесты для итератора категории."""

    def test_iterator_creation(self):
        """Тест создания итератора."""
        products = [
            Product("Product1", "Desc1", 100.0, 2),
            Product("Product2", "Desc2", 200.0, 3),
        ]
        iterator = CategoryIterator(products)
        assert iterator.products == products
        assert iterator.index == 0

    def test_iterator_iteration(self):
        """Тест итерации по элементам."""
        products = [
            Product("Product1", "Desc1", 100.0, 2),
            Product("Product2", "Desc2", 200.0, 3),
            Product("Product3", "Desc3", 300.0, 1),
        ]
        iterator = CategoryIterator(products)
        # Преобразуем итератор в список
        result = list(iterator)
        assert result == products

    def test_iterator_stop_iteration(self):
        """Тест остановки итерации."""
        products = [Product("Product1", "Desc1", 100.0, 2)]
        iterator = CategoryIterator(products)
        # Первый элемент
        product1 = next(iterator)
        assert product1 == products[0]
        # Должен вызвать StopIteration
        with pytest.raises(StopIteration):
            next(iterator)

    def test_iterator_empty_list(self):
        """Тест итератора с пустым списком."""
        iterator = CategoryIterator([])
        with pytest.raises(StopIteration):
            next(iterator)


class TestContainerInterface:
    """Тесты интерфейса Container."""

    def test_container_is_abstract(self):
        """Тест что Container является абстрактным классом."""
        assert issubclass(Container, ABC)
        # Проверяем абстрактные методы
        abstract_methods = {
            "get_total_price",
            "get_products_count",
            "__len__",
            "__str__",
        }
        for method_name in abstract_methods:
            method = getattr(Container, method_name)
            assert hasattr(method, "__isabstractmethod__")

    def test_cannot_instantiate_container(self):
        """Тест что нельзя создать экземпляр абстрактного класса."""
        with pytest.raises(TypeError):
            Container()

    def test_category_implements_container(self):
        """Тест что Category реализует интерфейс Container."""
        product = Product("Product", "Desc", 100.0, 5)
        category = Category("Category", "Description", [product])
        # Проверяем что все абстрактные методы реализованы
        assert hasattr(category, "get_total_price")
        assert hasattr(category, "get_products_count")
        assert hasattr(category, "__len__")
        assert hasattr(category, "__str__")
        # Проверяем что методы работают
        assert isinstance(category.get_total_price(), (int, float))
        assert isinstance(category.get_products_count(), int)
        assert isinstance(len(category), int)
        assert isinstance(str(category), str)

    def test_order_implements_container(self):
        """Тест что Order реализует интерфейс Container."""
        product = Product("Product", "Desc", 1000.0, 10)
        order = Order(product, 3)
        # Проверяем что все абстрактные методы реализованы
        assert hasattr(order, "get_total_price")
        assert hasattr(order, "get_products_count")
        assert hasattr(order, "__len__")
        assert hasattr(order, "__str__")
        # Проверяем что методы работают
        assert isinstance(order.get_total_price(), (int, float))
        assert isinstance(order.get_products_count(), int)
        assert isinstance(len(order), int)
        assert isinstance(str(order), str)


class TestIntegration:
    """Интеграционные тесты."""

    def setup_method(self):
        """Сброс состояния перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0
        Order.order_count = 0

    def test_complete_workflow(self):
        """Тест полного рабочего процесса."""
        # 1. Создание продуктов
        smartphone = Smartphone(
            "iPhone 15", "Flagship smartphone", 120000.0, 10, 3.5, "15 Pro", 256, "Blue"
        )
        lawn_grass = LawnGrass(
            "Premium Grass",
            "High quality lawn grass",
            5000.0,
            50,
            "Germany",
            14,
            "Dark Green",
        )
        # 2. Создание категории
        electronics_category = Category(
            "Electronics", "Electronic devices", [smartphone]
        )
        garden_category = Category("Garden", "Garden products", [lawn_grass])
        # 3. Создание заказов
        order1 = Order(smartphone, 2)
        order2 = Order(lawn_grass, 5)
        # 4. Проверка статистики
        assert Category.category_count == 2
        assert Category.product_count == 2
        assert Order.order_count == 2
        # 5. Проверка расчетов
        assert electronics_category.get_total_price() == 120000.0 * 10
        assert garden_category.get_total_price() == 5000.0 * 50
        assert order1.get_total_price() == 120000.0 * 2
        assert order2.get_total_price() == 5000.0 * 5

    def test_polymorphism_with_containers(self):
        """Тест полиморфизма с контейнерами."""
        product = Product("Product", "Desc", 100.0, 5)
        smartphone = Smartphone("Phone", "Desc", 50000.0, 2, 3.0, "M", 128, "B")
        category = Category("Category", "Desc", [product, smartphone])
        order = Order(smartphone, 1)
        containers = [category, order]
        # Все контейнеры должны иметь общий интерфейс
        for container in containers:
            total_price = container.get_total_price()
            products_count = container.get_products_count()
            length = len(container)
            string_repr = str(container)
            assert isinstance(total_price, (int, float))
            assert isinstance(products_count, int)
            assert isinstance(length, int)
            assert isinstance(string_repr, str)


class TestEdgeCases:
    """Тесты граничных случаев."""

    def test_product_with_very_high_price(self):
        """Тест продукта с очень высокой ценой."""
        product = Product("Expensive", "Desc", 9999999.99, 1)
        assert product.price == 9999999.99

    def test_product_with_very_low_price(self):
        """Тест продукта с очень низкой ценой."""
        product = Product("Cheap", "Desc", 0.01, 1000)
        assert product.price == 0.01

    def test_product_with_large_quantity(self):
        """Тест продукта с большим количеством."""
        product = Product("Bulk", "Desc", 10.0, 1000000)
        assert product.quantity == 1000000

    def test_category_with_many_products(self):
        """Тест категории со многими продуктами."""
        products = [Product(f"Product{i}", f"Desc{i}", i * 10.0, i) for i in range(100)]
        category = Category("Large Category", "Description", products)
        assert len(category) == 100
        assert category.get_products_count() == 100

    def test_order_with_different_product_types(self):
        """Тест заказов с разными типами продуктов."""
        smartphone = Smartphone("Phone", "Desc", 50000.0, 5, 3.0, "M", 128, "B")
        lawn_grass = LawnGrass("Grass", "Desc", 1000.0, 10, "C", 14, "G")
        product = Product("Product", "Desc", 100.0, 20)
        # Все типы продуктов должны работать с Order
        order1 = Order(smartphone, 1)
        order2 = Order(lawn_grass, 2)
        order3 = Order(product, 3)
        assert order1.get_total_price() == 50000.0
        assert order2.get_total_price() == 2000.0
        assert order3.get_total_price() == 300.0

    def test_string_representations_special_characters(self):
        """Тест строковых представлений со специальными символами."""
        product = Product("Продукт с Ünicødé", "Описание с 🚀 эмодзи", 100.0, 5)
        category = Category("Категория с spéciål chãrs", "Описание", [product])
        # Должно работать без ошибок
        str_product = str(product)
        str_category = str(category)
        repr_product = repr(product)
        repr_category = repr(category)
        assert isinstance(str_product, str)
        assert isinstance(str_category, str)
        assert isinstance(repr_product, str)
        assert isinstance(repr_category, str)


class TestErrorMessages:
    """Тесты сообщений об ошибках."""

    def test_product_addition_error_message(self):
        """Тест сообщения об ошибке при сложении разных типов."""
        product = Product("Product", "Desc", 100.0, 5)
        smartphone = Smartphone("Phone", "Desc", 50000.0, 2, 3.0, "M", 128, "B")
        with pytest.raises(TypeError, match="Нельзя складывать товары разных типов"):
            product + smartphone

    def test_category_add_product_error_message(self):
        """Тест сообщения об ошибке при добавлении не-продукта в категорию."""
        category = Category("Category", "Description", [])
        with pytest.raises(
            TypeError,
            match="Можно добавлять только объекты класса Product или его наследников",
        ):
            category.add_product("invalid")

    def test_order_creation_error_messages(self):
        """Тест сообщений об ошибках при создании заказа."""
        product = Product("Product", "Desc", 1000.0, 5)
        with pytest.raises(
            TypeError,
            match="Заказ может содержать только объекты класса Product или его наследников",
        ):
            Order("invalid", 1)
        with pytest.raises(
            ValueError, match="Количество товара в заказе должно быть положительным"
        ):
            Order(product, 0)
        with pytest.raises(ValueError, match="Недостаточно товара на складе"):
            Order(product, 10)


if __name__ == "__main__":
    # Запуск тестов
    exit_code = pytest.main([__file__, "-v", "--tb=short"])
    sys.exit(exit_code)
