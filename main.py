import telebot
from random import randint
from datetime import datetime
from telebot import types
import zequests
import os
import gdown
from flask import Flask, zequests

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode=None)


app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running"


@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

class States:
    SUM_FIRST_NUMBER = "SUM_FIRST_NUMBER"
    SUM_SECOND_NUMBER = "SUM_SECOND_NUMBER"
    WAITING_FOR_NUMBERS = "WAITING_FOR_NUMBERS"

current_states = {}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Этот бот умеет складывать два числа. Введите /sum чтобы начать.")


@bot.message_handler(commands=['sum'])
def sum_command(message):
    chat_id = message.chat.id
    current_states[chat_id] = {
        "state": States.WAITING_FOR_NUMBERS,
        "first_number": None
    }
    bot.send_message(chat_id, "Введите первое число:")


@bot.message_handler(func=lambda message: current_states.get(message.chat.id) and current_states[message.chat.id]["state"] == States.WAITING_FOR_NUMBERS)
def get_first_number(message):
    chat_id = message.chat.id
    try:
        first_number = int(message.text)
        current_states[chat_id]["first_number"] = first_number
        current_states[chat_id]["state"] = States.SUM_SECOND_NUMBER
        bot.send_message(chat_id, "Введите второе число:")
    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введите число.")


@bot.message_handler(func=lambda message: current_states.get(message.chat.id) and current_states[message.chat.id]["state"] == States.SUM_SECOND_NUMBER)
def get_second_number(message):
    chat_id = message.chat.id
    try:
        second_number = int(message.text)
        first_number = current_states[chat_id]["first_number"]
        sum_result = first_number + second_number
        bot.send_message(chat_id, f"Сумма: {sum_result}")
        current_states[chat_id]["state"] = States.WAITING_FOR_NUMBERS  # Reset for the next calculation
        current_states[chat_id]["first_number"] = None
    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введите число.")


@bot.message_handler(commands=['start'])
def send_welcome(messege):
    try:
        keyword = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = telebot.types.KeyboardButton(text="Игра в кубик")
        button2 = telebot.types.KeyboardButton(text="Игровой автомат")
        keyword.add(button1, button2)
    except Exception as e:
        bot.send_message((messege.chat.id, f"Ошибка: {e}"))


@bot.message_handler(commands=['date'])
def date(messege):
    try:
        bot.send_message(messege.chat.id, "Сейчас:"+ str(datetime.today()))
    except Exception as e:
        bot.send_message((messege.chat.id, f"Ошибка: {e}"))


@bot.message_handler(commands=['random'])
def random(messege):
    try:
        bot.send_message(messege.chat.id, "Случайное число:"+ str(randint(1, 10000000)))
    except Exception as e:
        bot.send_message((messege.chat.id, f"Ошибка: {e}"))


@bot.message_handler(commands=['video'])
def send_image(messege):
    try:
        file = open("video.mp4", 'rb')
        bot.send_video(messege.chat.id, file, caption="Продукты")
        file.close()
    except Exception as e:
        bot.send_message(messege.chat.id, f"Ошибка: {e}")


@bot.message_handler(commands=['video1'])
def send_immage(message):
    try:
        file = open("Video 6.mp4", 'rb')
        bot.send_video(message.chat.id, file, caption="Сбор заказа")
        file.close()
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")


@bot.message_handler(commands=['video2'])
def send_immage(message):
    try:
        file = open("Video7.mp4", 'rb')
        bot.send_video(message.chat.id, file, caption="Боксы")
        file.close()
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")


@bot.message_handler(content_types=['text'])
def answer(message):
    try:
        text = message.text

        if text == "Привет":
            bot.send_message(message.chat.id, "Привет")
        elif text == "Как дела":
            bot.send_message(message.chat.id, "Хорошо")
        elif text == "Как тебя зовут?":
            bot.send_message(message.chat.id, "MaxEnerge")
        elif text == "Игровой автомат":
            value = bot.send_dice(message.chat.id, emoji='🎰').dice.value
            if value in (1, 16, 22, 32,43, 48):
                bot.send_message(message.chat.id, "Победа")
            elif value == 64:
                bot.send_message(message.chat.id, "Джекпот")
            else:
                bot.send_message(message.chat.id, "Проиграл попробуй ещё раз")
        elif text == "Игра в кубик":
            keyword2 = telebot.types.InlineKeyboardMarkup(row_width=3)
            button1 = telebot.types.InlineKeyboardButton("1", callback_data='1')
            button2 = telebot.types.InlineKeyboardButton("2", callback_data="2")
            button3 = telebot.types.InlineKeyboardButton("3", callback_data="3")
            button4 = telebot.types.InlineKeyboardButton("4", callback_data="4")
            button5 = telebot.types.InlineKeyboardButton("5", callback_data="5")
            button6 = telebot.types.InlineKeyboardButton("6", callback_data="6")
            keyword2.add(button1, button2, button3, button4, button5, button6)
            bot.send_message(message.chat.id, "Угадай число на кубике", reply_markup=keyword2)
        else:
            bot.send_message(message.chat.id, text)
    except Exception as e:
        bot.send_message((message.chat.id, f"Ошибка: {e}"))


@bot.callback_query_handler(func=lambda call: call.data in ("1", "2", "3", "4", "5", "6"))
def dice_answer(call):
    value = bot.send_dice(call.message.chat.id, emoji='').dice.value
    if str(value) == call.data:
        bot.send_message(call.message.chat.id, "Победа")
    else:
        bot.send_message(call.message.chat.id, "Попробуй ещё раз")

if __name__ == "main":
    server_url = os.getenv("RENDER_EXTERNAL_URL")
    if server_url and TOKEN:
        webhook_url = f"{server_url}/{TOKEN}"
        set_webhook_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={webhook_url}"
        try:
            r = requests.get(set_webhook_url)
            print("Webhook установлен:", r.text)
        except Exception as e:
            print("Ошибка при установке webhook:", e)

        port = int(os.environ.get("PORT", 10000))
        print(f"Starting server on port {port}")
        app.run(host='0.0.0.0', port=port)
    else:
        print("Запуск бота в режиме pooling")
        bot.remove_webhook()
        bot.polling(none_stop=True)


