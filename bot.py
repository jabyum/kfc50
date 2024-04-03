import telebot
import buttons as bt
from geopy.geocoders import Nominatim
bot = telebot.TeleBot("6571068957:AAEwA9k4Jule6IiL2L6_aF62zu8c_tSbivc")
# объект для расшифровки координат
geolocator = Nominatim(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15")

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Здравствуйте! "
                              "Добро пожаловаться в бот от KFC!\n"
                              "Пройдите короткую регистрацию.\n\n"
                              "Введите своё имя:")
    bot.register_next_step_handler(message, get_name)
def get_name(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, "Поделитесь своими контактными данными",
                     reply_markup=bt.phone_bt())
    print(message.contact)
    bot.register_next_step_handler(message, get_phone_number, name)
def get_phone_number(message, name):
    user_id = message.from_user.id
    # проверяем, отправил ли пользоваться свой номер через кнопку
    if message.contact:
        phone_number = message.contact.phone_number
        print(phone_number)
        bot.send_message(user_id, "Номер принят. Регистрация завершена."
                                  "Выберите действие:", reply_markup=bt.main_menu_kb())
    # возвращаем пользователя в эту же функцию, если он отправил не через кнопку
    else:
        bot.send_message(user_id, "Отправьте свои контакты через кнопку")
        bot.register_next_step_handler(message, get_phone_number, name)
@bot.message_handler(content_types=['text'])
def main_menu(message):
    user_id = message.from_user.id
    if message.text == "🛒 Начать заказ":
        bot.send_message(user_id, "Отправьте геолокацию или выберите адрес",
                         reply_markup=bt.location_kb())
        bot.register_next_step_handler(message, get_location)

    elif message.text == "🛍 Корзина":
        pass
    elif message.text == "Отзыв":
        bot.send_message(user_id, "Напишите свой отзыв")
        bot.register_next_step_handler(message, feedback)
    elif message.text == "Настройки":
        pass

def get_location(message):
    user_id = message.from_user.id
    if message.location:
        # получаем широту и долготу
        longitude = message.location.longitude
        latitude = message.location.latitude
        # преобразуем широту и долготу в адрес
        address = geolocator.reverse((latitude, longitude)).address
        bot.send_message(user_id, f"Ваш адрес {address}")
        bot.register_next_step_handler(message, products_menu)
    else:
        bot.send_message(user_id, "Отправьте локацию через кнопку")
        bot.register_next_step_handler(message, get_location)

def products_menu(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Выберите продукт")

def feedback(message):
    user_id = message.from_user.id
    admins_group_id = -4137671137
    feedback_text = message.text
    full_text = (f"<b>Айди юзера</b>:{user_id}\n"
                 f"<b>Текст отзыва</b>: {feedback_text}")
    bot.send_message(user_id, "Спасибо за отзыв!")
    bot.send_message(admins_group_id, full_text, parse_mode="HTML")
bot.polling(non_stop=True)
