from unittest.mock import patch

import pytest

from src.main import (
    demonstrate_all_features,
    demonstrate_edge_cases,
    demonstrate_inheritance,
    demonstrate_magic_methods,
)
from src.product import Category, LawnGrass, Product, Smartphone


class TestMainFunctions:
    """Тесты для основных функций демонстрации"""

    def test_demonstrate_all_features(self, capsys):
        """Тест основной демонстрации функций"""
        demonstrate_all_features()
        captured = capsys.readouterr()

        # Проверяем, что вывод содержит ожидаемые разделы
        assert "ДЕМОНСТРАЦИЯ ВСЕХ ФУНКЦИЙ ПРОЕКТА" in captured.out
        assert "БАЗОВОЕ СОЗДАНИЕ ПРОДУКТОВ И КАТЕГОРИЙ" in captured.out
        assert "ПРИВАТНЫЕ АТРИБУТЫ И ГЕТТЕРЫ" in captured.out
        assert "ДОБАВЛЕНИЕ ПРОДУКТОВ ЧЕРЕЗ МЕТОД" in captured.out
        assert "РАБОТА С ЦЕНОЙ (ГЕТТЕР/СЕТТЕР)" in captured.out
        assert "КЛАСС-МЕТОД С ОБРАБОТКОЙ ДУБЛИКАТОВ" in captured.out
        assert "МАГИЧЕСКИЕ МЕТОДЫ" in captured.out
        assert "СТАТИСТИКА" in captured.out

    def test_demonstrate_edge_cases(self, capsys):
        """Тест демонстрации граничных случаев"""
        demonstrate_edge_cases()
        captured = capsys.readouterr()

        assert "ГРАНИЧНЫЕ СЛУЧАИ И ОБРАБОТКА ОШИБОК" in captured.out
        assert "Пустая категория" in captured.out
        assert "Товар без запаса" in captured.out

    def test_demonstrate_magic_methods(self, capsys):
        """Тест демонстрации магических методов"""
        demonstrate_magic_methods()
        captured = capsys.readouterr()

        assert "ДОПОЛНИТЕЛЬНАЯ ДЕМОНСТРАЦИЯ МАГИЧЕСКИХ МЕТОДОВ" in captured.out
        assert "Строковое представление продуктов" in captured.out
        assert "Сложение продуктов" in captured.out
        assert "Итерация по продуктам категории" in captured.out

    @patch(
        "builtins.input", return_value="y"
    )  # Мокаем input для подтверждения изменения цены
    def test_demonstrate_inheritance(self, mock_input, capsys):
        """Тест демонстрации наследования"""
        demonstrate_inheritance()
        captured = capsys.readouterr()

        assert "ДЕМОНСТРАЦИЯ НАСЛЕДОВАНИЯ И НОВЫХ ОГРАНИЧЕНИЙ" in captured.out
        assert "СОЗДАНИЕ ОБЪЕКТОВ РАЗНЫХ КЛАССОВ" in captured.out
        assert "СЛОЖЕНИЕ ОБЪЕКТОВ ОДНОГО КЛАССА" in captured.out
        assert "ПОПЫТКА СЛОЖЕНИЯ ОБЪЕКТОВ РАЗНЫХ КЛАССОВ" in captured.out


class TestProductCreation:
    """Тесты создания продуктов"""

    def test_product_creation_basic(self):
        """Тест базового создания продукта"""
        product = Product("Test Product", "Test Description", 1000.0, 10)

        assert product.name == "Test Product"
        assert product.description == "Test Description"
        assert product.price == 1000.0
        assert product.quantity == 10

    def test_product_str_representation(self):
        """Тест строкового представления продукта"""
        product = Product("Test Product", "Test Description", 1000.0, 10)
        expected_str = "Test Product, 1000.0 руб. Остаток: 10 шт."
        assert str(product) == expected_str

    def test_product_price_setter_negative(self, capsys):
        """Тест установки отрицательной цены"""
        product = Product("Test Product", "Test Description", 1000.0, 10)
        product.price = -500

        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 1000.0  # Цена не изменилась

    @patch("builtins.input", return_value="y")
    def test_product_price_setter_valid(self, mock_input):
        """Тест установки корректной цены"""
        product = Product("Test Product", "Test Description", 1000.0, 10)
        product.price = 1500.0

        assert product.price == 1500.0

    @patch("builtins.input", return_value="n")
    def test_product_price_setter_decline(self, mock_input):
        """Тест отмены изменения цены"""
        product = Product("Test Product", "Test Description", 1000.0, 10)
        product.price = 900.0  # Пытаемся понизить цену

        assert product.price == 1000.0  # Цена не изменилась


class TestCategoryCreation:
    """Тесты создания категорий"""

    def test_category_creation_basic(self):
        """Тест базового создания категории"""
        product = Product("Test Product", "Test Description", 1000.0, 10)
        category = Category("Test Category", "Test Description", [product])

        assert category.name == "Test Category"
        assert category.description == "Test Description"

    def test_category_str_representation(self):
        """Тест строкового представления категории"""
        product1 = Product("Product 1", "Desc 1", 1000.0, 5)
        product2 = Product("Product 2", "Desc 2", 2000.0, 3)
        category = Category("Test Category", "Test Description", [product1, product2])

        expected_str = "Test Category, количество продуктов: 8 шт."
        assert str(category) == expected_str

    def test_category_add_product(self):
        """Тест добавления продукта в категорию"""
        category = Category("Test Category", "Test Description", [])
        product = Product("Test Product", "Test Description", 1000.0, 10)

        category.add_product(product)

        # Проверяем, что продукт добавлен
        assert "Test Product" in category.products

    def test_category_add_invalid_product(self):
        """Тест добавления невалидного продукта в категорию"""
        category = Category("Test Category", "Test Description", [])

        with pytest.raises(
            TypeError,
            match="Можно добавлять только объекты класса Product или его наследников",
        ):
            category.add_product("invalid product")


class TestClassMethod:
    """Тесты класс-метода"""

    def test_new_product_no_duplicates(self):
        """Тест создания нового продукта без дубликатов"""
        product_data = {
            "name": "New Product",
            "description": "New Description",
            "price": 1000.0,
            "quantity": 5,
        }

        product = Product.new_product(product_data)

        assert product.name == "New Product"
        assert product.description == "New Description"
        assert product.price == 1000.0
        assert product.quantity == 5

    def test_new_product_with_duplicates(self):
        """Тест создания продукта с дубликатами"""
        existing_product = Product("Existing Product", "Old Description", 800.0, 10)
        existing_products = [existing_product]

        duplicate_data = {
            "name": "Existing Product",
            "description": "New Description",
            "price": 1000.0,
            "quantity": 5,
        }

        # При создании дубликата должен вернуться существующий продукт с обновленным количеством
        result = Product.new_product(duplicate_data, existing_products)

        assert result == existing_product
        assert result.quantity == 15  # 10 + 5
        assert result.price == 1000.0  # Цена обновилась на более высокую


class TestMagicMethods:
    """Тесты магических методов"""

    def test_product_addition_same_type(self):
        """Тест сложения продуктов одного типа"""
        product1 = Product("Product 1", "Desc 1", 1000.0, 2)
        product2 = Product("Product 2", "Desc 2", 500.0, 3)

        total = product1 + product2

        # (1000 * 2) + (500 * 3) = 2000 + 1500 = 3500
        assert total == 3500.0

    def test_product_addition_different_types(self):
        """Тест сложения продуктов разных типов"""
        product = Product("Product", "Desc", 1000.0, 2)
        smartphone = Smartphone(
            "Smartphone", "Desc", 1500.0, 3, 2.5, "Model X", 128, "Black"
        )

        with pytest.raises(TypeError, match="Нельзя складывать товары разных типов"):
            _ = product + smartphone

    def test_category_iterator(self):
        """Тест итерации по категории"""
        product1 = Product("Product 1", "Desc 1", 1000.0, 2)
        product2 = Product("Product 2", "Desc 2", 500.0, 3)
        category = Category("Test Category", "Test Description", [product1, product2])

        products = list(category)

        assert len(products) == 2
        assert products[0] == product1
        assert products[1] == product2


class TestInheritance:
    """Тесты наследования"""

    def test_smartphone_creation(self):
        """Тест создания смартфона"""
        smartphone = Smartphone(
            "Test Smartphone",
            "Test Description",
            1000.0,
            10,
            3.5,
            "Model X",
            256,
            "Black",
        )

        assert smartphone.name == "Test Smartphone"
        assert smartphone.efficiency == 3.5
        assert smartphone.model == "Model X"
        assert smartphone.memory == 256
        assert smartphone.color == "Black"

    def test_lawn_grass_creation(self):
        """Тест создания газонной травы"""
        lawn_grass = LawnGrass(
            "Test Grass", "Test Description", 500.0, 20, "Germany", 14, "Green"
        )

        assert lawn_grass.name == "Test Grass"
        assert lawn_grass.country == "Germany"
        assert lawn_grass.germination_period == 14
        assert lawn_grass.color == "Green"

    def test_smartphone_addition(self):
        """Тест сложения смартфонов"""
        smartphone1 = Smartphone(
            "Phone 1", "Desc", 1000.0, 2, 3.0, "Model A", 128, "Black"
        )
        smartphone2 = Smartphone(
            "Phone 2", "Desc", 1500.0, 3, 3.5, "Model B", 256, "White"
        )

        total = smartphone1 + smartphone2

        # (1000 * 2) + (1500 * 3) = 2000 + 4500 = 6500
        assert total == 6500.0

    def test_mixed_type_addition(self):
        """Тест сложения объектов разных классов-наследников"""
        smartphone = Smartphone(
            "Smartphone", "Desc", 1000.0, 2, 3.0, "Model A", 128, "Black"
        )
        lawn_grass = LawnGrass("Grass", "Desc", 500.0, 3, "Germany", 14, "Green")

        with pytest.raises(TypeError, match="Нельзя складывать товары разных типов"):
            _ = smartphone + lawn_grass


class TestStatistics:
    """Тесты статистики"""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом"""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_count(self):
        """Тест счетчика категорий"""
        initial_count = Category.category_count

        # Создаем новую категорию
        product = Product("Test Product", "Test Description", 1000.0, 10)
        Category("Test Category", "Test Description", [product])

        assert Category.category_count == initial_count + 1

    def test_product_count(self):
        """Тест счетчика продуктов"""
        initial_count = Category.product_count

        product = Product("Test Product", "Test Description", 1000.0, 10)
        Category("Test Category", "Test Description", [product])

        assert Category.product_count == initial_count + 1


class TestEdgeCases:
    """Тесты граничных случаев"""

    def test_empty_category(self):
        """Тест пустой категории"""
        category = Category("Empty Category", "No products", [])

        assert str(category) == "Empty Category, количество продуктов: 0 шт."
        products = list(category)
        assert len(products) == 0

    def test_zero_quantity_product(self):
        """Тест продукта с нулевым количеством"""
        product = Product("Zero Product", "Description", 1000.0, 0)

        assert product.quantity == 0
        assert "Остаток: 0 шт." in str(product)

    def test_product_with_same_name_different_cases(self):
        """Тест продуктов с одинаковыми именами в разных регистрах"""
        product1 = Product("product", "Description", 1000.0, 5)

        # Класс-метод должен считать их одинаковыми продуктами (регистронезависимое сравнение)
        existing_products = [product1]
        new_product_data = {
            "name": "PRODUCT",  # В верхнем регистре
            "description": "New Description",
            "price": 1500.0,
            "quantity": 2,
        }

        result = Product.new_product(new_product_data, existing_products)

        # Должен вернуть существующий продукт и обновить его
        assert result == product1
        assert result.quantity == 7  # 5 + 2
        assert result.price == 1500.0  # Цена обновилась


@patch("builtins.input", return_value="y")
def test_main_execution(mock_input, capsys):
    """Тест выполнения main скрипта"""
    # Имитируем выполнение main скрипта
    demonstrate_all_features()
    demonstrate_edge_cases()
    demonstrate_magic_methods()
    demonstrate_inheritance()

    captured = capsys.readouterr()

    # Проверяем, что все основные разделы присутствуют в выводе
    assert "ДЕМОНСТРАЦИЯ ВСЕХ ФУНКЦИЙ ПРОЕКТА" in captured.out
    assert "ГРАНИЧНЫЕ СЛУЧАИ И ОБРАБОТКА ОШИБОК" in captured.out
    assert "ДОПОЛНИТЕЛЬНАЯ ДЕМОНСТРАЦИЯ МАГИЧЕСКИХ МЕТОДОВ" in captured.out
    assert "ДЕМОНСТРАЦИЯ НАСЛЕДОВАНИЯ И НОВЫХ ОГРАНИЧЕНИЙ" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
