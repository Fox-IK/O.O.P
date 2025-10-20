from product import (
    BaseProduct,
    Category,
    Container,
    LawnGrass,
    Order,
    Product,
    Smartphone,
)


def demonstrate_all_features():
    """Демонстрация всех функций проекта"""
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ ВСЕХ ФУНКЦИЙ ПРОЕКТА")
    print("=" * 70)

    # 1. Базовое создание продуктов и категорий (из первого задания)
    print("\n1. БАЗОВОЕ СОЗДАНИЕ ПРОДУКТОВ И КАТЕГОРИЙ")
    print("-" * 50)

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

    # 2. Приватные атрибуты и геттеры (из первого задания)
    print("\n2. ПРИВАТНЫЕ АТРИБУТЫ И ГЕТТЕРЫ")
    print("-" * 50)

    print("Список товаров через геттер:")
    print(category1.products)

    # 3. Добавление продуктов через метод (из первого задания)
    print("\n3. ДОБАВЛЕНИЕ ПРОДУКТОВ ЧЕРЕЗ МЕТОД")
    print("-" * 50)

    product4 = Product("HONOR Magic5", "512GB, Зеленый", 65000.0, 7)
    category1.add_product(product4)
    print("После добавления нового продукта:")
    print(category1.products)

    # 4. Работа с ценой (геттер/сеттер) (из первого задания)
    print("\n4. РАБОТА С ЦЕНОЙ (ГЕТТЕР/СЕТТЕР)")
    print("-" * 50)

    print(f"Текущая цена Xiaomi: {product3.price}")

    # Попытка установить отрицательную цену
    product3.price = -5000
    print(f"Цена после попытки установить отрицательную: {product3.price}")

    # Установка корректной цены
    product3.price = 35000.0
    print(f"Цена после корректного изменения: {product3.price}")

    # 5. Класс-метод с обработкой дубликатов (из первого задания)
    print("\n5. КЛАСС-МЕТОД С ОБРАБОТКОЙ ДУБЛИКАТОВ")
    print("-" * 50)

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

    # 6. Магические методы (из первого задания)
    print("\n6. МАГИЧЕСКИЕ МЕТОДЫ")
    print("-" * 50)

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

    # 7. Наследование - классы Smartphone и LawnGrass (из второго задания)
    print("\n7. КЛАССЫ-НАСЛЕДНИКИ: SMARTPHONE И LAWNGRASS")
    print("-" * 50)

    # Смартфон
    smartphone = Smartphone(
        name="iPhone 15 Pro",
        description="Флагманский смартфон Apple",
        price=120000.0,
        quantity=10,
        efficiency=3.5,
        model="15 Pro",
        memory=256,
        color="Титановый синий",
    )
    print(f"Смартфон: {smartphone}")
    print(
        f"  Доп. атрибуты: производительность={smartphone.efficiency}, модель={smartphone.model}, "
        f"память={smartphone.memory}ГБ, цвет={smartphone.color}"
    )

    # Газонная трава
    lawn_grass = LawnGrass(
        name="Газонная трава Премиум",
        description="Элитная газонная трава для загородного дома",
        price=2500.0,
        quantity=100,
        country="Германия",
        germination_period=14,
        color="Ярко-зеленый",
    )
    print(f"Газонная трава: {lawn_grass}")
    print(
        f"  Доп. атрибуты: страна={lawn_grass.country}, "
        f"срок прорастания={lawn_grass.germination_period} дней, цвет={lawn_grass.color}"
    )

    # 8. Ограничения сложения (из второго задания)
    print("\n8. ОГРАНИЧЕНИЯ СЛОЖЕНИЯ")
    print("-" * 50)

    smartphone2 = Smartphone(
        name="Samsung Galaxy S24",
        description="Флагманский смартфон Samsung",
        price=90000.0,
        quantity=15,
        efficiency=3.2,
        model="S24 Ultra",
        memory=512,
        color="Черный",
    )

    # Сложение смартфонов
    try:
        smartphones_total = smartphone + smartphone2
        print(f"Суммарная стоимость смартфонов: {smartphones_total} руб.")
    except TypeError as e:
        print(f"Ошибка при сложении смартфонов: {e}")

    # Попытка сложения объектов разных классов
    try:
        invalid_sum = smartphone + lawn_grass
        print(f"Результат: {invalid_sum}")
    except TypeError as e:
        print(f"Ошибка при сложении смартфона и травы: {e}")

    # 9. Абстрактные классы BaseProduct и Container (из третьего задания)
    print("\n9. АБСТРАКТНЫЕ КЛАССЫ")
    print("-" * 50)

    # Проверка, что нельзя создать экземпляр абстрактного класса
    print("BaseProduct - абстрактный класс, нельзя создать его экземпляр")
    print("Container - абстрактный класс, нельзя создать его экземпляр")

    # Проверка наследования
    print(f"\nProduct наследуется от BaseProduct: {issubclass(Product, BaseProduct)}")
    print(f"Smartphone наследуется от Product: {issubclass(Smartphone, Product)}")
    print(f"LawnGrass наследуется от Product: {issubclass(LawnGrass, Product)}")
    print(f"Category наследуется от Container: {issubclass(Category, Container)}")

    # 10. Класс Order (из третьего задания)
    print("\n10. КЛАСС ORDER (ЗАКАЗЫ)")
    print("-" * 50)

    # Создание заказа
    try:
        order = Order(smartphone, 2)
        print(f"Успешный заказ: {order}")
        print(f"Общая стоимость заказа: {order.get_total_price()} руб.")
    except Exception as e:
        print(f"Ошибка при создании заказа: {e}")

    # Попытка создания невалидного заказа
    print("\nПопытка заказа с недостаточным количеством:")
    try:
        Order(smartphone, 20)
    except ValueError as e:
        print(f"Ошибка: {e}")

    # 11. Полиморфизм Container (из третьего задания)
    print("\n11. ПОЛИМОРФИЗМ CONTAINER")
    print("-" * 50)

    # Создаем разные контейнеры
    electronics_category = Category("Электроника", "Техника", [smartphone, smartphone2])
    garden_category = Category("Сад", "Товары для сада", [lawn_grass])

    order1 = Order(smartphone, 1)
    order2 = Order(lawn_grass, 5)

    containers = [electronics_category, garden_category, order1, order2]

    print("Общий интерфейс Container:")
    for container in containers:
        print(f"  Контейнер: {container}")
        print(f"    Общая стоимость: {container.get_total_price()} руб.")
        print(f"    Количество продуктов: {container.get_products_count()}")
        print(f"    Длина: {len(container)}")

    # 12. Статистика и обратная совместимость
    print("\n12. СТАТИСТИКА И ОБРАТНАЯ СОВМЕСТИМОСТЬ")
    print("-" * 50)

    print(f"Общее количество категорий: {Category.category_count}")
    print(f"Общее количество товаров: {Category.product_count}")
    print(f"Общее количество заказов: {Order.order_count}")

    # Проверка что старый код работает
    print("\nПроверка обратной совместимости:")
    old_style_product = Product("Старый товар", "Описание", 500.0, 10)
    old_style_category = Category("Старая категория", "Описание", [old_style_product])

    print(f"Старый продукт: {old_style_product}")
    print(f"Старая категория: {old_style_category}")
    print("Старый код работает корректно!")

    # 13. Демонстрация класс-метода для Product (исправленная версия)
    print("\n13. ДЕМОНСТРАЦИЯ КЛАСС-МЕТОДА ДЛЯ PRODUCT")
    print("-" * 50)

    # Создание продукта через класс-метод
    product_data = {
        "name": "Новый продукт через класс-метод",
        "description": "Создан с помощью Product.new_product()",
        "price": 5000.0,
        "quantity": 25,
    }

    new_product = Product.new_product(product_data)
    print(f"Создан через класс-метод: {new_product}")
    print(f"Тип объекта: {type(new_product)}")


def demonstrate_edge_cases():
    """Демонстрация граничных случаев и обработки ошибок"""
    print("\n" + "=" * 70)
    print("ГРАНИЧНЫЕ СЛУЧАИ И ОБРАБОТКА ОШИБОК")
    print("=" * 70)

    # 1. Пустая категория
    print("\n1. ПУСТАЯ КАТЕГОРИЯ")
    print("-" * 50)
    empty_category = Category("Пустая категория", "Нет товаров", [])
    print(f"Пустая категория: {empty_category}")
    print(f"Продукты в пустой категории: {len(empty_category)}")

    # 2. Продукты с нулевым количеством
    print("\n2. ПРОДУКТЫ С НУЛЕВЫМ КОЛИЧЕСТВОМ")
    print("-" * 50)
    zero_product = Product("Товар без запаса", "Описание", 1000.0, 0)
    print(f"Товар без запаса: {zero_product}")

    # 3. Ошибки при сложении
    print("\n3. ОШИБКИ ПРИ СЛОЖЕНИИ")
    print("-" * 50)
    try:
        product = Product("Test", "Desc", 100.0, 5)
        product + "не продукт"
    except TypeError as e:
        print(f"Ошибка при сложении: {e}")

    # 4. Ошибки при добавлении в категорию
    print("\n4. ОШИБКИ ПРИ ДОБАВЛЕНИИ В КАТЕГОРИЮ")
    print("-" * 50)
    try:
        category = Category("Test", "Test", [])
        category.add_product("not a product")
    except TypeError as e:
        print(f"Ошибка при добавлении: {e}")

    # 5. Ошибки при создании заказа
    print("\n5. ОШИБКИ ПРИ СОЗДАНИИ ЗАКАЗА")
    print("-" * 50)
    product = Product("Test Product", "Description", 1000.0, 5)

    try:
        Order("не продукт", 1)
    except TypeError as e:
        print(f"Ошибка типа: {e}")

    try:
        Order(product, -1)
    except ValueError as e:
        print(f"Ошибка количества: {e}")

    try:
        Order(product, 10)  # Больше чем есть
    except ValueError as e:
        print(f"Ошибка доступности: {e}")


def main():
    """Основная функция демонстрации"""
    try:
        demonstrate_all_features()
        demonstrate_class_method()
        demonstrate_edge_cases()

        print("\n" + "=" * 70)
        print("ДЕМОНСТРАЦИЯ ВСЕХ ФУНКЦИЙ ЗАВЕРШЕНА")
        print("=" * 70)

    except Exception as e:
        print(f"Произошла ошибка во время демонстрации: {e}")
        return 1

    return 0


def demonstrate_class_method():
    """Демонстрация класс-метода"""
    print("\n" + "=" * 70)
    print("ДЕМОНСТРАЦИЯ КЛАСС-МЕТОДА")
    print("=" * 70)

    # Пример использования класс-метода
    product_data = {
        "name": "Google Pixel 8",
        "description": "Смартфон с AI-функциями",
        "price": 75000.0,
        "quantity": 8,
    }

    new_product = Product.new_product(product_data)
    print(f"Создан через класс-метод: {new_product}")
    print(f"Тип объекта: {type(new_product)}")


if __name__ == "__main__":
    exit(main())
