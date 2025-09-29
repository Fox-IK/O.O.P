import pytest

from product import Product, Category


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

    @staticmethod
    def setup_method():
        """Сброс счетчиков перед каждым тестом"""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_initialization(self):
        """Тест корректности инициализации объекта Category"""
        product = Product("Test Product", "Test Description", 1000.0, 10)
        category = Category("Test Category", "Test Description", [product])

        assert category.name == "Test Category"
        assert category.description == "Test Description"
        assert len(category.products) == 1
        assert category.products[0].name == "Test Product"

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
        assert len(category.products) == 0
        assert Category.category_count == 1
        assert Category.product_count == 0