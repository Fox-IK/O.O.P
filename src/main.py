from product import Category, Product

if __name__ == "__main__":
    product1 = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(product1.name)
    print(product1.description)
    print(product1.price)
    print(product1.quantity)

    print(product2.name)
    print(product2.description)
    print(product2.price)
    print(product2.quantity)

    print(product3.name)
    print(product3.description)
    print(product3.price)
    print(product3.quantity)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print(category1.name == "Смартфоны")
    print(category1.description)
    print(len(category1.products))
    print(category1.category_count)
    print(category1.product_count)

    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product4],
    )

    print(category2.name)
    print(category2.description)
    print(len(category2.products))
    print(category2.products)

    print(Category.category_count)
    print(Category.product_count)


def demonstrate_additional_features():
    """Демонстрация дополнительных функций"""
    print("=== ДЕМОНСТРАЦИЯ ДОПОЛНИТЕЛЬНЫХ ФУНКЦИЙ ===")

    # Создаем начальные продукты
    existing_products = [
        Product("Samsung Galaxy S23", "256GB, Черный", 80000.0, 10),
        Product("iPhone 14", "128GB, Синий", 70000.0, 15),
    ]

    print("Существующие продукты:")
    for product in existing_products:
        print(f"  - {product}")

    # Демонстрация класс-метода с проверкой дубликатов
    print("\n--- Проверка дубликатов через класс-метод ---")

    # Пытаемся создать продукт с таким же именем (должен объединиться)
    duplicate_product_data = {
        "name": "Samsung Galaxy S23",  # Такое же имя
        "description": "256GB, Белый",  # Другое описание
        "price": 85000.0,  # Более высокая цена
        "quantity": 5,  # Дополнительное количество
    }

    new_product = Product.new_product(duplicate_product_data, existing_products)
    print(f"Результат создания дубликата: {new_product}")
    print(
        f"Общее количество Samsung Galaxy S23: {existing_products[0].quantity}"
    )  # Должно быть 15

    # Создаем совершенно новый продукт
    new_product_data = {
        "name": "Google Pixel 7",
        "description": "128GB, Черный",
        "price": 60000.0,
        "quantity": 8,
    }

    truly_new_product = Product.new_product(new_product_data, existing_products)
    print(f"Результат создания нового продукта: {truly_new_product}")

    print("\nОбновленный список продуктов:")
    for product in existing_products:
        print(f"  - {product}")


def demonstrate_price_confirmation():
    """Демонстрация подтверждения изменения цены"""
    print("\n--- Подтверждение изменения цены ---")

    product = Product("Test Product", "Test Description", 1000.0, 5)
    print(f"Текущая цена: {product.price}")

    # Попытка понизить цену (требует подтверждения)
    print("Попытка понизить цену до 800...")
    # В реальном сценарии здесь будет запрос подтверждения через input
    # Для демонстрации мы симулируем это
    product.price = 800.0

    print(f"Цена после попытки понижения: {product.price}")


if __name__ == "__main__":
    # Основная демонстрация (как раньше)
    product1 = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print("=== ОСНОВНАЯ ДЕМОНСТРАЦИЯ ===")
    print(f"Продукт 1: {product1}")
    print(f"Продукт 2: {product2}")
    print(f"Продукт 3: {product3}")

    # Создание категории
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print(f"\nКатегория: {category1.name}")
    print(f"Описание: {category1.description}")
    print("Товары в категории:")
    print(category1.products)

    # Добавление нового продукта через метод
    product4 = Product("HONOR Magic5", "512GB, Зеленый", 65000.0, 7)
    category1.add_product(product4)

    print("После добавления нового продукта:")
    print(category1.products)

    print("\nОбщая статистика:")
    print(f"Категорий: {Category.category_count}")
    print(f"Товаров: {Category.product_count}")

    # Тестирование сеттера цены
    print("\n=== ТЕСТИРОВАНИЕ СЕТТЕРА ЦЕНЫ ===")
    print(f"Текущая цена Xiaomi: {product3.price}")

    # Попытка установить отрицательную цену
    product3.price = -5000
    print(f"Цена после попытки установить отрицательную: {product3.price}")

    # Установка корректной цены
    product3.price = 35000.0
    print(f"Цена после корректного изменения: {product3.price}")

    # Попытка установить нулевую цену
    product3.price = 0
    print(f"Цена после попытки установить нулевую: {product3.price}")

    # Демонстрация дополнительных функций
    demonstrate_additional_features()

    # Для демонстрации подтверждения цены раскомментируйте следующую строку:
    # demonstrate_price_confirmation()
