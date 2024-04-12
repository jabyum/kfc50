from telebot import types

def phone_bt():
    # создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # создаем сами кнопки
    phone = types.KeyboardButton("Поделиться контактами", request_contact=True)
    # добавляем кнопки в пространство
    kb.add(phone)
    return kb
def main_menu_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    products = types.KeyboardButton("🛒 Начать заказ")
    feedback = types.KeyboardButton("Отзыв")
    settings = types.KeyboardButton("Настройки")
    kb.add(products, feedback, settings)
    return kb
def location_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    location = types.KeyboardButton("Отправить локацию", request_location=True)
    kb.add(location)
    return kb
def all_products(actual_products):
    # создание пространства для инлайн кнопок
    kb = types.InlineKeyboardMarkup(row_width=2)
    # постоянные кнопки
    back = types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back")
    cart = types.InlineKeyboardButton(text="🛒 Корзина", callback_data="user_cart")
    # динамичные кнопки
    products = [types.InlineKeyboardButton(text=i[1], callback_data=i[0])
                for i in actual_products]
    kb.add(*products)
    kb.row(cart)
    kb.row(back)
    return kb
def exact_product(current_ammount=1, plus_or_minus=""):
    kb = types.InlineKeyboardMarkup(row_width=3)
    # постоянные кнопки
    back = types.InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")
    accept =  types.InlineKeyboardButton(text="Добавить в корзигу", callback_data="to_cart")
    minus = types.InlineKeyboardButton(text="➖", callback_data="minus")
    plus = types.InlineKeyboardButton(text="➕", callback_data="plus")
    count = types.InlineKeyboardButton(text=f"{current_ammount}", callback_data="none")
    # динамичная кнопка
    if plus_or_minus == "plus":
        new_ammount = current_ammount + 1
        count = types.InlineKeyboardButton(text=f"{new_ammount}", callback_data="none")
    elif plus_or_minus == "minus":
        if current_ammount > 1:
            new_ammount = current_ammount - 1
            count = types.InlineKeyboardButton(text=f"{new_ammount}", callback_data="none")
    kb.add(minus, count, plus)
    kb.row(accept)
    kb.row(back)
    return kb
def get_cart_kb(cart):
    kb = types.InlineKeyboardMarkup(row_width=1)
    # постоянные кнопки
    clear = types.InlineKeyboardButton(text="Очистить корзину", callback_data="clear_cart")
    back = types.InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")
    order = types.InlineKeyboardButton(text="Оформить заказ", callback_data="order")
    # динамичные
    products = [types.InlineKeyboardButton(text=f"❌ {i[0]}", callback_data=f"{i[0]}") for i in cart]
    kb.add(clear,back,order)
    kb.add(*products)
    return kb



