from src.product import Category, Product


def demonstrate_all_features():
    """Демонстрация всех функций проекта"""
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ ВСЕХ ФУНКЦИЙ ПРОЕКТА")
    print("=" * 60)

    # 1. Базовое создание продуктов и категорий
    print("\n1. БАЗОВОЕ СОЗДАНИЕ ПРОДУКТОВ И КАТЕГОРИЙ")
    print("-" * 40)

    product1 = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print("Созданные продукты:")
    print(f"  - {product1}")
    print(f"  - {product2}")
    print(f"  - {product3}")

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print(f"\nСозданная категория: {category1}")
    print(f"Описание: {category1.description}")

    # 2. Приватные атрибуты и геттеры
    print("\n2. ПРИВАТНЫЕ АТРИБУТЫ И ГЕТТЕРЫ")
    print("-" * 40)

    print("Список товаров через геттер:")
    print(category1.products)

    # 3. Добавление продуктов через метод
    print("\n3. ДОБАВЛЕНИЕ ПРОДУКТОВ ЧЕРЕЗ МЕТОД")
    print("-" * 40)

    product4 = Product("HONOR Magic5", "512GB, Зеленый", 65000.0, 7)
    category1.add_product(product4)
    print("После добавления нового продукта:")
    print(category1.products)

    # 4. Работа с ценой (геттер/сеттер)
    print("\n4. РАБОТА С ЦЕНОЙ (ГЕТТЕР/СЕТТЕР)")
    print("-" * 40)

    print(f"Текущая цена Xiaomi: {product3.price}")

    # Попытка установить отрицательную цену
    product3.price = -5000
    print(f"Цена после попытки установить отрицательную: {product3.price}")

    # Установка корректной цены
    product3.price = 35000.0
    print(f"Цена после корректного изменения: {product3.price}")

    # 5. Класс-метод с обработкой дубликатов
    print("\n5. КЛАСС-МЕТОД С ОБРАБОТКОЙ ДУБЛИКАТОВ")
    print("-" * 40)

    existing_products = [
        Product("Samsung Galaxy S23", "256GB, Черный", 80000.0, 10),
        Product("iPhone 14", "128GB, Синий", 70000.0, 15),
    ]

    print("Существующие продукты:")
    for product in existing_products:
        print(f"  - {product}")

    # Создаем дубликат
    duplicate_data = {
        "name": "Samsung Galaxy S23",
        "description": "256GB, Белый",
        "price": 85000.0,
        "quantity": 5,
    }

    new_product = Product.new_product(duplicate_data, existing_products)
    print(f"\nРезультат создания дубликата: {new_product}")
    print(f"Общее количество Samsung Galaxy S23: {existing_products[0].quantity}")

    # 6. Магические методы
    print("\n6. МАГИЧЕСКИЕ МЕТОДЫ")
    print("-" * 40)

    # __str__
    print("Строковое представление:")
    print(f"  Продукт: {product1}")
    print(f"  Категория: {category1}")

    # __add__
    total_value = product1 + product2
    print(
        f"\nСложение продуктов: {product1.name} + {product2.name} = {total_value} руб."
    )

    # Итератор
    print("\nИтерация по категории:")
    for i, product in enumerate(category1, 1):
        print(f"  {i}. {product}")

    # 7. Статистика
    print("\n7. СТАТИСТИКА")
    print("-" * 40)

    # Создаем вторую категорию для демонстрации счетчиков
    tv_product = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром",
        [tv_product],
    )

    print(f"Вторая категория: {category2}")  # Используем переменную
    print(f"Общее количество категорий: {Category.category_count}")
    print(f"Общее количество товаров: {Category.product_count}")


def demonstrate_edge_cases():
    """Демонстрация граничных случаев"""
    print("\n" + "=" * 60)
    print("ГРАНИЧНЫЕ СЛУЧАИ И ОБРАБОТКА ОШИБОК")
    print("=" * 60)

    # Пустая категория
    empty_category = Category("Пустая категория", "Нет товаров", [])
    print(f"Пустая категория: {empty_category}")
    print("Продукты в пустой категории:")
    for product in empty_category:
        print("  (нет продуктов)")

    # Продукты с нулевым количеством
    zero_product = Product("Товар без запаса", "Описание", 1000.0, 0)
    print(f"\nТовар без запаса: {zero_product}")

    # Ошибка при сложении
    try:
        product = Product("Test", "Desc", 100.0, 5)
        # Убираем присваивание ненужной переменной result
        _ = product + "не продукт"  # Должно вызвать TypeError
    except TypeError as e:
        print(f"\nОшибка при сложении: {e}")

    # Ошибка при добавлении не-продукта
    try:
        category = Category("Test", "Test", [])
        category.add_product("not a product")
    except TypeError as e:
        print(f"Ошибка при добавлении: {e}")


def demonstrate_magic_methods():
    """Демонстрация магических методов"""
    print("\n" + "=" * 60)
    print("ДОПОЛНИТЕЛЬНАЯ ДЕМОНСТРАЦИЯ МАГИЧЕСКИХ МЕТОДОВ")
    print("=" * 60)

    # Создаем продукты для демонстрации
    product1 = Product("iPhone 15", "256GB, Black", 80000.0, 10)
    product2 = Product("Samsung Galaxy", "512GB, White", 70000.0, 15)
    product3 = Product("Xiaomi Phone", "128GB, Blue", 30000.0, 20)

    # Демонстрация __str__ для Product
    print("--- Строковое представление продуктов ---")
    print(f"Продукт 1: {product1}")
    print(f"Продукт 2: {product2}")
    print(f"Продукт 3: {product3}")

    # Демонстрация __add__ для Product
    print("\n--- Сложение продуктов ---")
    total_value = product1 + product2
    print(f"Общая стоимость iPhone и Samsung: {total_value} руб.")

    # Сложение трех продуктов (попарно)
    total_all = (product1 + product2) + (product3.price * product3.quantity)
    print(f"Общая стоимость всех трех продуктов: {total_all} руб.")

    # Создаем категорию
    category = Category(
        "Смартфоны",
        "Мобильные телефоны различных брендов",
        [product1, product2, product3],
    )

    # Демонстрация __str__ для Category
    print("\n--- Строковое представление категории ---")
    print(f"Категория: {category}")

    # Демонстрация итератора
    print("\n--- Итерация по продуктам категории ---")
    print("Продукты в категории:")
    for i, product in enumerate(category, 1):
        print(f"  {i}. {product}")


if __name__ == "__main__":
    # Основная демонстрация
    demonstrate_all_features()

    # Демонстрация граничных случаев
    demonstrate_edge_cases()

    # Дополнительная демонстрация магических методов
    demonstrate_magic_methods()

    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 60)
