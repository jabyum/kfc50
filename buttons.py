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
    cart = types.KeyboardButton("🛍 Корзина")
    feedback = types.KeyboardButton("Отзыв")
    settings = types.KeyboardButton("Настройки")
    kb.add(products, cart, feedback, settings)
    return kb
def location_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    location = types.KeyboardButton("Отправить локацию", request_location=True)
    kb.add(location)
    return kb
