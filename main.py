# --- Импорты ---
import time
from luckytools import LuckyTools
from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup
import re
import sys
from PIL import Image, ImageDraw, ImageFont
import io
import re
import asyncio
import random
from random import randint

# --- Переменные ---
ingridients = {
    "wrapper": {
        "Нори": 5,
        "Лосось": 75,
        "Икра": 50,
        "Кунжут": 30,
        "Огурец": 20,
        "Пропустить": 0
    },
    "rice": {
        "Обычный": 20,
        "Солёный": 25
    },
    "filling": {
        "Творожный сыр": 30,
        "Огурецы": 15,
        "Лук": 15,
        "Лосось": 50,
        "Авокадо": 40,
        "Креветка": 80,
        "Угорь": 100,
        "Манго": 50
    }
}

menu_18 = [
    {"name": "Ролл 'Жаркий Чили'", "description": "С угрем, спайси-соусом и перцем халапеньо.", "price_rub": 450.0},
    {"name": "Сет 'Выходной'", "description": "Смелый выбор для ценителей. Много лосося, много огня.",
     "price_rub": 1800.0}
]

# --- Декораторы ---
def require_working_hours(func):
    def wrapper(*args, **kwargs):
        current_hour = int(str(datetime.now()).split(" ")[1].split(":")[0])
        if 7 <= current_hour < 23:
            return func(*args, **kwargs)
        tools.fade_print(f"✕ Мы работаем с 7:00 до 23:00", white_tag=True, time_show=3,
                         color="ff0000")
        return None
    return wrapper


# --- Утилиты ---
def shitaem_total_recursive(cart, index=0):
    if index == len(cart):
        return 0
    return cart[index]["price_rub"] + shitaem_total_recursive(cart, index + 1)


async def process_order():
    tools.fade_print(f"⟳ Установка защищенного соединения...", white_tag=True, time_show=0.01, color="b5b5b5")
    await asyncio.sleep(1)
    tools.fade_print(f"⟳ Обработка...", white_tag=True, time_show=0.01, color="b5b5b5")
    await asyncio.sleep(1.5)
    tools.fade_print("✓ Транзакция подтверждена сервером", white_tag=True, time_show=0.5, color="00ff00")


def get_captcha(width=200, height=100): # https://docs-python.ru/packages/veb-frejmvork-flask-python/generatsiia-svoei-kapchi/
    code = ''.join([random.choice('АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ') for i in range(5)])
    # random_word = random.choice(["Тут была конф информация"])
    # code = random_word

    img = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('freesans.ttf',
                              size=50)
    x = 0;
    y = 12;
    for let in code:
        if x == 0:
            x = 5
        else:
            x = x + width / len(code)
        y = randint(3, 55)
        draw.text((x, y), let, font=font, fill=(randint(0, 200), randint(0, 200), randint(0, 200), 128))

    for i in range(40):
        draw.line([(randint(0, width), randint(0, height)),
                   (randint(0, width), randint(0, height))],
                  randint(0, 200), 2, 128)

    img.save("captha.png", "PNG")
    return code

def new_input(prompt_text, max_val=sys.maxsize, min_val=1):
    try:
        answer = input("› ")
        int_answer = int(answer)

        if min_val <= int_answer <= max_val:
            return int_answer

        tools.fade_print(f"✕ Ошибка ввода! Введите число от {min_val} до {max_val}.", white_tag=True, time_show=1.5,
                         color="ff0000")
    except ValueError:
        tools.fade_print("✕ Ошибка ввода! Попробуйте ещё раз.", white_tag=True, time_show=1.5, color="ff0000")
    return new_input(prompt_text, max_val, min_val)


def get_age_and_name():
    try:
        tools.fade_print("Импорт данных меню из JSON...", white_tag=True, time_show=0.01)
        with open("info.json", "r", encoding="utf-8") as file:
            information = json.load(file)
        tools.fade_print("✓ Импорт успешно завершён", white_tag=True, time_show=0.01)
    except (FileNotFoundError, json.JSONDecodeError):
        tools.fade_print("✕ JSON не найден или повреждён.",
                         white_tag=True, time_show=1.5, color="ffb300")
        with open("info.json", "w", encoding="utf-8") as file:
            info_def = {
                "admin@tatsumaki.xyz": {
                    "name": "Администратор",
                    "age": 21,
                    "phone": "79999999999",
                    "password": "admin"
                }
            }
            json.dump(info_def, file, indent=4, ensure_ascii=False)
            information = info_def

    tools.fade_print("Пожалуйста введите своё ФИО или 1, для входа:", white_tag=True, time_show=0.01)
    name = input("› ")
    if name == "1":
        tools.fade_print("Пожалуйста введите свой email:", white_tag=True,
                         time_show=0.01)
        email = input("› ").lower()
        if email in information:
            user_data = information[email]
            
            tools.fade_print("Пожалуйста введите пароль:", white_tag=True, time_show=0.01)
            password_input = input("› ")
            
            if user_data.get("password") == password_input:
                return user_data["age"], user_data["name"], user_data["phone"], email
            else:
                tools.fade_print("✕ Неверный пароль.", white_tag=True, time_show=3, color="ff0000")
                return get_age_and_name()
        else:
            tools.fade_print("✕ Почта не найдена.",
                             white_tag=True,
                             time_show=3, color="ff0000")
            return get_age_and_name()

    age = None
    while age is None:
        try:
            tools.fade_print("Пожалуйста введите свой возраст (только число):", white_tag=True, time_show=0.01)
            age_input = int(input("› "))
            if 3 < age_input < 123:
                age = age_input
            else:
                tools.fade_print("✕ Возраст должен быть в разумных пределах (4-122). Попробуйте ещё раз.",
                                 white_tag=True,
                                 time_show=3, color="ff0000")
        except ValueError:
            tools.fade_print("✕ Ошибка ввода! Попробуйте ещё раз.", white_tag=True, time_show=3, color="ff0000")

    number = None
    while number is None:
        tools.fade_print("Пожалуйста введите свой номер телефона:", white_tag=True,
                         time_show=0.01)
        number_raw = input("› ").strip()

        if bool(re.fullmatch(r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$", number_raw)):
            normalized_number = re.sub(r"[^\d]", "", number_raw)
            if normalized_number.startswith("8"):
                normalized_number = "7" + normalized_number[1:]
            elif normalized_number.startswith("+7"):
                normalized_number = normalized_number[1:]

            if len(normalized_number) == 11 and normalized_number.startswith("7"):
                number = normalized_number
            else:
                tools.fade_print("✕ Номер телефона введен неверно. Поддерживается только +7/8.",
                                 white_tag=True,
                                 time_show=3, color="ff0000")
        else:
            tools.fade_print("✕ Номер телефона введен неверно. Поддерживается только +7/8.",
                             white_tag=True,
                             time_show=3, color="ff0000")

    email = None
    while email is None:
        tools.fade_print("Пожалуйста введите свой email:", white_tag=True,
                         time_show=0.01)
        email_input = input("› ").lower()
        if bool(re.fullmatch(r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
, email_input)):
            if email_input in information:
                tools.fade_print("✕ Эта почта уже зарегистрирована. Попробуйте войти.",
                                 white_tag=True, time_show=3, color="ffb300")
                return get_age_and_name()
            tools.fade_print("Придумайте пароль для входа:", white_tag=True, time_show=0.01)
            password_input = input("› ")
            email = email_input
            information[email] = {
                "name": name.title(),
                "age": age,
                "phone": number,
                "password": password_input
            }
            try:
                with open("info.json", "w", encoding="utf-8") as file:
                    json.dump(information, file, indent=4, ensure_ascii=False)
            except IOError:
                tools.fade_print("✕ Ошибка сохранения данных пользователя.",
                                 white_tag=True, time_show=3, color="ff0000")

            return age, name, number, email
        else:
            tools.fade_print(f"✕ Почта введена неверно.",
                             white_tag=True,
                             time_show=3, color="ff0000")


def display_image_from_url(url, w=180):
    def pil_to_ascii_color(image):  # Нашел эту штуку в интернете
        char = "█"  # https://ru.piliapp.com/symbol/square/
        W = w

        width, height = image.size
        aspect_ratio = height / width
        new_height = int(W * aspect_ratio * 0.55)
        resized_image = image.resize((W, new_height))

        pixels = resized_image.getdata()
        output_string = []

        def get_color_code(r, g, b):
            r_i = int(r / 255 * 5)
            g_i = int(g / 255 * 5)
            b_i = int(b / 255 * 5)
            color_index = 16 + (r_i * 36) + (g_i * 6) + b_i
            return f"\033[38;5;{color_index}m"

        for i, pixel in enumerate(pixels):
            r, g, b = pixel[:3]
            color_code = get_color_code(r, g, b)
            output_string.append(f"{color_code}{char}")
            if (i + 1) % W == 0:
                output_string.append("\033[0m\n")

        return "".join(output_string) + "\033[0m"

    try:
        if not url:
            tools.fade_print("| (Нет ссылки на изображение)", white_tag=True, time_show=0.01, color="b5b5b5")
            return

        response = requests.get(url, stream=True, timeout=5)
        response.raise_for_status()

        image = Image.open(io.BytesIO(response.content)).convert("RGB")
        ascii_art = pil_to_ascii_color(image)
        print(ascii_art)

    except requests.exceptions.RequestException:
        tools.fade_print("| Загрузка... ---", white_tag=True, time_show=0.01, color="ffb300")
        img = Image.open(url).convert("RGB")
        ascii_art = pil_to_ascii_color(img)
        print(ascii_art)
        return
    except Exception:
        tools.fade_print("| Ошибка обработки изображения с помощью PIL.", white_tag=True, time_show=0.01,
                         color="ffb300")


def open_constructor(menu, cart, age, balance, bonus):
    tools.fade_print("⇌ Конструктор роллов", white_tag=True, time_show=0.01, color="ffffff")
    price = 0
    new_roll_details = {}

    for section_name, ingredients in ingridients.items():
        list_ingredients = list(ingredients.items())
        tools.fade_print(f"⇌ Выберите {section_name} (Текущая цена: {price} руб):", white_tag=True, time_show=0.01,
                         color="ffffff")

        for i, (name, cost) in enumerate(list_ingredients):
            tools.fade_print(f"| {i + 1}. {name} - {cost} руб.", white_tag=True, time_show=0.01, color="b5b5b5")

        tools.fade_print(f"| {len(list_ingredients) + 1}. Назад в меню", white_tag=True, time_show=0.01, color="b5b5b5")

        selection_index = new_input("", max_val=len(list_ingredients) + 1)

        if selection_index == len(list_ingredients) + 1:
            return main_menu(menu, cart, age, balance, bonus)

        selected_item = list_ingredients[selection_index - 1]
        new_roll_details[section_name] = selected_item
        price += selected_item[1]

    description_text = (
        f"Обертка: {new_roll_details['wrapper'][0]} ({new_roll_details['wrapper'][1]} руб), "
        f"Рис: {new_roll_details['rice'][0]} ({new_roll_details['rice'][1]} руб), "
        f"Начинка: {new_roll_details['filling'][0]} ({new_roll_details['filling'][1]} руб)."
    )

    cart.append({
        "product_id": "0000",
        "name": f"Кастомный ролл ({new_roll_details['wrapper'][0]})",
        "category": "Конструктор роллов",
        "description": description_text,
        "image_url": None,
        "weight": "250 гр",
        "price_rub": float(price),
        "rating": None
    })

    tools.fade_print(f"Итоговая цена: {price} рублей. ✓ Успешно добавлено в корзину.", white_tag=True, time_show=2,
                     color="ffffff")
    main_menu(menu, cart, age, balance, bonus)


def open_menu_standart(menu, cart, age, balance, bonus):
    print("\n" * 2)

    categories = []
    for item in menu:
        if not item["category"] in categories:
            categories.append(item["category"])

    tools.fade_print("⇌ Выберите категорию:", white_tag=True, time_show=0.01, color="ffffff")
    for i, cat in enumerate(categories):
        tools.fade_print(f"| {i + 1}. {cat}", white_tag=True, time_show=0.01, color="b5b5b5")

    tools.fade_print(f"| {len(categories) + 1}. Назад в меню", white_tag=True, time_show=0.01, color="b5b5b5")

    selection_index = new_input("", max_val=len(categories) + 1)
    if selection_index == len(categories) + 1:
        return main_menu(menu, cart, age, balance, bonus)

    selected_category = categories[selection_index - 1]

    rolls_in_category = [item for item in menu if item["category"] == selected_category]

    print("\n" * 1)
    tools.fade_print(f"⇌ Выберите блюдо из категории '{selected_category}':", white_tag=True, time_show=0.01,
                     color="ffffff")
    for i, roll in enumerate(rolls_in_category):
        tools.fade_print(f"| {i + 1}. {roll['name']} - {roll['price_rub']} руб.", white_tag=True, time_show=0.01,
                         color="b5b5b5")

    tools.fade_print(f"| {len(rolls_in_category) + 1}. Назад к категориям", white_tag=True, time_show=0.01,
                     color="b5b5b5")

    roll_index = new_input("", max_val=len(rolls_in_category) + 1)
    if roll_index == len(rolls_in_category) + 1:
        return open_menu_standart(menu, cart, age, balance, bonus)

    selected_roll = rolls_in_category[roll_index - 1]

    print("\n")

    display_image_from_url(selected_roll['image_url'])

    tools.fade_print(f"⇌ {selected_roll['name']}", white_tag=True, time_show=0.01, color="ffffff")
    tools.fade_print(f"| Категория: {selected_roll['category']}", white_tag=True, time_show=0.01, color="b5b5b5")
    tools.fade_print(f"| Описание: {selected_roll['description']}", white_tag=True, time_show=0.01, color="b5b5b5")
    tools.fade_print(f"| Вес: {selected_roll['weight']}", white_tag=True, time_show=0.01, color="b5b5b5")
    tools.fade_print(f"| Рейтинг: {selected_roll['rating'] if selected_roll['rating'] else 'Нет'}", white_tag=True,
                     time_show=0.01, color="b5b5b5")
    tools.fade_print(f"|-- Цена: {selected_roll['price_rub']} руб. ------", white_tag=True, time_show=0.01,
                     color="b5b5b5")

    tools.fade_print(f"| 1. Добавить в корзину", white_tag=True, time_show=0.01, color="b5b5b5")
    tools.fade_print(f"| 2. Назад в главное меню", white_tag=True, time_show=0.01, color="b5b5b5")

    action_choice = new_input("", max_val=2)

    if action_choice == 1:
        cart.append(selected_roll)
        tools.fade_print(f"✓ Успешно добавлено в корзину.", white_tag=True, time_show=1.5)
        return main_menu(menu, cart, age, balance, bonus)
    else:
        return main_menu(menu, cart, age, balance, bonus)


def open_adult_menu(menu, cart, age, balance, bonus):
    print("\n" * 2)
    tools.fade_print("!!! ВЗРОСЛОЕ МЕНЮ (18+) !!!", white_tag=True, time_show=0.01, color="ff0000")
    tools.fade_print("⇌ Выберите блюдо:", white_tag=True, time_show=0.01, color="ffffff")

    for i, item in enumerate(menu_18):
        tools.fade_print(f"| {i + 1}. {item['name']} ({item['description']}) - {item['price_rub']} руб.",
                         white_tag=True, time_show=0.01, color="b5b5b5")

    tools.fade_print(f"| {len(menu_18) + 1}. Назад в меню", white_tag=True, time_show=0.01, color="b5b5b5")

    roll_index = new_input("", max_val=len(menu_18) + 1)
    if roll_index == len(menu_18) + 1:
        return main_menu(menu, cart, age, balance, bonus)

    selected_item = menu_18[roll_index - 1].copy()

    selected_item["product_id"] = f"A{roll_index:03d}"
    selected_item["category"] = "Взрослое меню (18+)"
    selected_item["weight"] = "Различный"
    selected_item["image_url"] = None
    selected_item["rating"] = "5.0"

    cart.append(selected_item)
    tools.fade_print(f"✓ '{selected_item['name']}' успешно добавлено в корзину.", white_tag=True, time_show=2)
    main_menu(menu, cart, age, balance, bonus)


def open_menu(menu, cart, age, balance, bonus):
    print("\n" * 2)
    tools.fade_print("⇌ Выберите раздел меню:", white_tag=True, time_show=0.01, color="ffffff")
    tools.fade_print("| 1. Основное меню", white_tag=True, time_show=0.01, color="b5b5b5")
    tools.fade_print("| 2. Конструктор роллов", white_tag=True, time_show=0.01, color="b5b5b5")

    option_count = 2
    if age >= 18:
        option_count += 1
        tools.fade_print("| 3. Взрослое меню (18+)", white_tag=True, time_show=0.01, color="ff0000")

    tools.fade_print(f"| {option_count + 1}. Назад в главное меню", white_tag=True, time_show=0.01, color="b5b5b5")

    while True:
        answer = new_input("", max_val=option_count + 1)

        if answer == 1:
            return open_menu_standart(menu, cart, age, balance, bonus)
        elif answer == 2:
            return open_constructor(menu, cart, age, balance, bonus)
        elif answer == 3 and age >= 18:
            return open_adult_menu(menu, cart, age, balance, bonus)
        elif answer == option_count + 1:
            return main_menu(menu, cart, age, balance, bonus)
        else:
            tools.fade_print("✕ Некорректный выбор. Попробуйте ещё раз.", white_tag=True, time_show=1.5, color="ff0000")


# --- Корзина и оплата ---
def pay_card(cart, final_price):
    asyncio.run(shitaem_total_recursive("банковской карты"))
    print("\n" * 1)
    tools.fade_print("- Оформление заказа (Карта) -", white_tag=True, time_show=0.01, color="ffffff")

    for item in cart:
        tools.fade_print(f"| {item['name']} - {item['price_rub']} руб", white_tag=True, time_show=0.01, color="b5b5b5")

    tools.fade_print(f"- Итого: {final_price} руб.", white_tag=True, time_show=0.01, color="ffffff")
    tools.fade_print(f"- Статус: Ожидание оплаты.", white_tag=True, time_show=0.01, color="ffffff")
    tools.fade_print(f"Для оплаты, переведите {final_price} рублей на номер:", white_tag=True, time_show=0.01,
                     color="b5b5b5")
    tools.fade_print(f"--- +7 923 504 68-72 ---", white_tag=True, time_show=0.01)
    tools.fade_print(f"После перевода, заказ будет принят. Мы свяжемся с вами для уточнения деталей.", white_tag=True,
                     time_show=0.01, color="b5b5b5")


def pay_cash(cart, final_price):
    asyncio.run(process_order())
    print("\n" * 1)
    tools.fade_print("- Оформление заказа (Наличными) -", white_tag=True, time_show=0.01, color="ffffff")

    for item in cart:
        tools.fade_print(f"| {item['name']} - {item['price_rub']} руб", white_tag=True, time_show=0.01, color="b5b5b5")

    tools.fade_print(f"- Итого: {final_price} руб.", white_tag=True, time_show=0.01, color="ffffff")
    tools.fade_print(f"- Статус: Оплата при получении.", white_tag=True, time_show=0.01, color="ffffff")
    tools.fade_print("Ваш заказ принят. Ожидайте звонка оператора.", white_tag=True, time_show=0.01, color="b5b5b5")


def open_cart(menu, cart, age, balance, bonus):
    print("\n" * 2)
    if not cart:
        tools.fade_print("⇌ Корзина пуста.", white_tag=True, time_show=0.01, color="ffffff")
        tools.fade_print("| 1. Назад", white_tag=True, time_show=0.01, color="b5b5b5")
        if new_input("", max_val=1) == 1:
            return main_menu(menu, cart, age, balance, bonus)
        return main_menu(menu, cart, age, balance, bonus)

    final_price = shitaem_total_recursive(cart)

    tools.fade_print("⇌ Ваша Корзина", white_tag=True, time_show=0.01, color="ffffff")
    for i, item in enumerate(cart):
        tools.fade_print(f"| {i + 1}. {item['name']} ({item['category']}) - {item['price_rub']} руб", white_tag=True,
                         time_show=0.01, color="b5b5b5")

    tools.fade_print(f"| --- Итого: {final_price} руб ---------", white_tag=True, time_show=0.01, color="ffffff")
    tools.fade_print(f"| 1. Оформить заказ", white_tag=True, time_show=0.01, color="b5b5b5")
    tools.fade_print(f"| 2. Назад", white_tag=True, time_show=0.01, color="b5b5b5")

    action_choice = new_input("", max_val=2)

    if action_choice == 2:
        return main_menu(menu, cart, age, balance, bonus)

    tools.fade_print("\n⇌ Выберите способ оплаты", white_tag=True, time_show=0.01, color="ffffff")
    tools.fade_print(f"| 1. Оплата картой", white_tag=True, time_show=0.01, color="b5b5b5")
    tools.fade_print(f"| 2. Наличными при получении", white_tag=True, time_show=0.01, color="b5b5b5")

    payment_choice = new_input("", max_val=2)

    if payment_choice == 1:
        pay_card(cart, final_price)
    elif payment_choice == 2:
        pay_cash(cart, final_price)


# --- Основное меню ---
def main_menu(menu, cart, age, balance, bonus):
    print("\n" * 5)
    tools.fade_print("⇌ Главное меню", white_tag=True, time_show=0.01, color="ffffff")
    tools.fade_print("| 1. Меню", white_tag=True, time_show=0.01, color="b5b5b5")
    tools.fade_print(f"| 2. Корзина ({len(cart)})", white_tag=True, time_show=0.01, color="b5b5b5")
    tools.fade_print(f"| 3. Моя KASHOLKA)", white_tag=True, time_show=0.01,
                     color="b5b5b5")

    max_option = 3

    answer = new_input("", max_val=max_option)

    if answer == 1:
        return open_menu(menu, cart, age, balance, bonus)
    elif answer == 2:
        return open_cart(menu, cart, age, balance, bonus)
    elif answer == 3:
        return open_cash(menu, cart, age, balance, bonus)


# --- Кошелек ---
# Мистер мужчина, вы обронили кошелку
def open_cash(menu, cart, age, balance, bonus):
    tools.fade_print("⇌ Кошелек", white_tag=True, time_show=0.01, color="ffffff")
    tools.fade_print(f"| Баланс: {balance}", white_tag=True, time_show=0.01, color="b5b5b5")
    tools.fade_print(f"- Инфо: В данный момент нельзя потратить, он в разработке.", time_show=0.01)
    tools.fade_print(f"| 1. Назад", white_tag=True, time_show=0.01, color="b5b5b5")
    input()
    return main_menu(menu, cart, age, balance, bonus)


@require_working_hours
def run_app():
    cart = []
    balance = 0
    bonus = 50

    user_data = get_age_and_name()
    if user_data is None:
        return

    age, name, phone, email = user_data

    menu = []
    try:
        tools.fade_print("Импорт данных меню из JSON...", white_tag=True, time_show=0.01)
        with open("menu.json", "r", encoding="utf-8") as file:
            menu = json.load(file)
        tools.fade_print("✓ Импорт успешно завершён", white_tag=True, time_show=0.01)
    except (FileNotFoundError, json.JSONDecodeError):
        tools.fade_print("✕ JSON не найден или повреждён.",
                         white_tag=True, time_show=1.5, color="ffb300")
        return

    main_menu(menu, cart, age, balance, bonus)


if __name__ == "__main__":
    tools = LuckyTools(prefix_short="⌊ УниКапча ⌉ »", show_init=False)
    while True:
        code = get_captcha(600,100)
        display_image_from_url("captha.png")
        tools.fade_print("Введите код  или debug", white_tag=True, time_show=1)
        enter = input("> ")
        if enter.lower() == code.lower() or enter=="debug":
            tools.fade_print("Верный код, спасибо за прохождение проверки!", white_tag=True, time_show=1)
            tools = LuckyTools(prefix_short="⌊ Tatsumaki ⌉ »", show_init=False)
            run_app()
        else:
            tools.fade_print("✕ Неверно введен код, попробуйте ещё раз!",
                             white_tag=True, time_show=1.5, color="ffb300")