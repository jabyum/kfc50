import telebot
from telebot import types
import buttons as bt
from geopy.geocoders import Nominatim
import database as db
import time
bot = telebot.TeleBot("6571068957:AAEwA9k4Jule6IiL2L6_aF62zu8c_tSbivc")
# объект для расшифровки координат
#geolocator = Nominatim(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
# db.add_product(pr_name= "Кола", pr_quantity=10, pr_price=20000.0, pr_des="лучший", pr_photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzolUu5EuGCYGg--0U4LV8vuQ0w1nHKxvMjiPgIqxCSA&s")
# print(db.get_all_products())
# print(db.get_pr_id_name())
users = {}
user_products_cart = {}


@bot.message_handler(commands=["start", "send_message"])
def start(message):
    user_id = message.from_user.id
    checker = db.check_user(user_id)
    admin_id = 305896408

    if message.text == "/start":
        if checker == False:
            bot.send_message(user_id, "Здравствуйте! "
                                      "Добро пожаловаться в бот от KFC!\n"
                                      "Пройдите короткую регистрацию.\n\n"
                                      "Введите своё имя:")
            bot.register_next_step_handler(message, get_name)
        elif checker == True:
            bot.send_message(user_id, "Выберите действие:", reply_markup=bt.main_menu_kb())
    elif message.text == "/send_message":
        if user_id == admin_id:
            bot.send_message(message.chat.id, "Отправьте id пользователя")
            bot.register_next_step_handler(message, get_user_id)
def get_user_id(message):
    user_id = message.from_user.id
    to_id = message.text
    if to_id.isdigit():
        bot.send_message(message.chat.id, "Отправьте текст для пользователя")
        bot.register_next_step_handler(message, get_user_text, to_id)
    else:
        bot.send_message(message.chat.id, "Отправьте айди")
        bot.register_next_step_handler(message, get_user_id)
def get_user_text(message, to_id):
    user_id = message.from_user.id
    text = message.text
    bot.send_message(message.chat.id, "сообщение отправлено")
    bot.send_message(int(to_id), text)


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
        db.add_user(user_id=user_id, name=name, phone_number=phone_number)
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
    # if message.location:
    if message:
        # получаем широту и долготу
        # longitude = message.location.longitude
        # latitude = message.location.latitude
        # преобразуем широту и долготу в адрес
        # address = geolocator.reverse((latitude, longitude)).address
        mm = bot.send_message(user_id, "Главное меню", reply_markup=types.ReplyKeyboardRemove())
        actual_products = db.get_pr_id_name()
        time.sleep(2)
        bot.delete_message(chat_id=user_id, message_id=mm.id)
        bot.send_message(user_id, "Выберите продукт", reply_markup=bt.all_products(actual_products))
    else:
        bot.send_message(user_id, "Отправьте локацию через кнопку")
        # TODO ne rabotaet
        # bot.register_next_step_handler(message, get_location)
        bot.register_next_step_handler(message, products_menu)

def products_menu(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Выберите продукт", reply_markup=bt.all_products())

def feedback(message):
    user_id = message.from_user.id
    admins_group_id = -4137671137
    feedback_text = message.text
    full_text = (f"<b>Айди юзера</b>:{user_id}\n"
                 f"<b>Текст отзыва</b>: {feedback_text}")
    bot.send_message(user_id, "Спасибо за отзыв!")
    bot.send_message(admins_group_id, full_text, parse_mode="HTML")

@bot.callback_query_handler(lambda call: call.data in ["back", "user_cart", "plus", "minus",
                                                       "none", "to_cart", "clear_cart", "main_menu",
                                                       "order"])
def for_call(call):
    user_id = call.message.chat.id
    if call.data == "back":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Отправьте геолокацию или выберите адрес",
                         reply_markup=bt.location_kb())
        bot.register_next_step_handler(call.message, get_location)
    elif call.data == "user_cart":
        bot.delete_message(user_id, call.message.message_id)
        user_cart = db.get_user_cart(user_id)
        full_text = f"Ваша корзина \n\n"
        total_amount = 0
        for i in user_cart:
            full_text += f"{i[0]} x{i[1]} = {i[2]}\n"
            total_amount += i[2]
        full_text += f"\n\nИтоговая сумма {total_amount}"
        cart = db.get_cart_id_name(user_id)
        pr_name = []
        for i in cart:
            pr_name.append(i[0])
        user_products_cart[user_id] = pr_name
        bot.send_message(user_id, full_text, reply_markup=bt.get_cart_kb(cart))
    elif call.data == "plus":
        current_ammount = users[user_id]["pr_count"]
        users[user_id]["pr_count"] += 1
        bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.id,
                                      reply_markup=bt.exact_product(current_ammount, "plus"))
    elif call.data == "minus":
        current_ammount = users[user_id]["pr_count"]
        if current_ammount > 1:
            users[user_id]["pr_count"] -= 1
            bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.id,
                                      reply_markup=bt.exact_product(current_ammount, "minus"))
        else:
            pass
    elif call.data == "none":
        pass
    elif call.data == "to_cart":
        db.add_to_cart(user_id, users[user_id]["pr_id"], users[user_id]["pr_name"], users[user_id]["pr_count"],
                       users[user_id]["pr_price"])
        users.pop(user_id)
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        bot.send_message(user_id, "Продукт успешно добавлен в корзину")
        actual_products = db.get_pr_id_name()
        bot.send_message(user_id, "Выберите продукт", reply_markup=bt.all_products(actual_products))
    elif call.data == "clear_cart":
        db.delete_user_cart(user_id)
        bot.send_message(user_id, "Ваша корзина очищена")
        actual_products = db.get_pr_id_name()
        bot.send_message(user_id, "Выберите продукт", reply_markup=bt.all_products(actual_products))
    elif call.data == "main_menu":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        actual_products = db.get_pr_id_name()
        bot.send_message(user_id, "Выберите продукт", reply_markup=bt.all_products(actual_products))
    elif call.data == "order":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        user_cart = db.get_user_cart(user_id)
        full_text = f"Новый заказ от юзера {user_id}: \n\n"
        total_amount = 0
        for i in user_cart:
            full_text += f"{i[0]} x{i[1]} = {i[2]}\n"
            total_amount += i[2]
        full_text += f"\n\nИтоговая сумма {total_amount}"
        bot.send_message(-4137671137, full_text)
        bot.send_message(user_id, "Ваш заказ оформлен")
        db.delete_user_cart(user_id)
        user_products_cart.pop(user_id)


@bot.callback_query_handler(lambda call: call.message.chat.id in user_products_cart.keys() and call.data in user_products_cart.get(call.message.chat.id))
def call_for_delete_cart(call):
    user_id = call.message.chat.id
    print("1")
    db.delete_exact_product_from_cart(user_id, call.data)
    user_products_cart[user_id].remove(str(call.data))
    user_cart = db.get_user_cart(user_id)
    full_text = f"Ваша корзина \n\n"
    total_amount = 0
    for i in user_cart:
        full_text += f"{i[0]} x{i[1]} = {i[2]}\n"
        total_amount += i[2]
    full_text += f"\n\nИтоговая сумма {total_amount}"
    cart = db.get_cart_id_name(user_id)
    bot.edit_message_text(chat_id=user_id, message_id=call.message.id, text=full_text,
                          reply_markup=bt.get_cart_kb(cart))



@bot.callback_query_handler(lambda call: int(call.data) in db.get_all_id())
def calls_for_products(call):
    user_id = call.message.chat.id
    product = db.get_exact_produdct(int(call.data))
    bot.delete_message(user_id, call.message.id)
    users[user_id] = {"pr_id": call.data, "pr_name": product[0], "pr_count": 1, "pr_price": product[1]}
    bot.send_photo(user_id, photo=product[3], caption=f"{product[0]}\n"
                                                      f"Описание: {product[2]}\n"
                                                      f"Цена: {product[1]}\n"
                                                      f"Выбрите количество: ", reply_markup=bt.exact_product())

bot.polling(non_stop=True)
