import json
import telebot
from random import randint
from datetime import datetime
import time
import random
import telebot
import requests
import os
import gdown
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image, ImageOps
from flask import Flask, request

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


def load_photo(message, name):
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    save_path = name
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)

history_file = "history.json"
history = {}

if os.path.exists(history_file):
    try:
        with open(history_file, "r", encoding='utf-8') as f:
            history = json.load(f)
    except Exception:
        history = {}

def save_history():
    try:
        with open(history_file, "w", encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Ошибка сохранения истории: ", e)
        
def chat(user_id, text):
    try:
        if str(user_id) not in history:
            history[str(user_id)] = [
                {"role": "system", "content": "Ты — дружелюбный помощник."}
            ]

        history[str(user_id)].append({"role": "user", "content": text})

        if len(history[str(user_id)]) > 16:
            history[str(user_id)] = [history[str(user_id)][0]] + history[str(user_id)][-15:]

        url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('API_KEY')}"
        }
        data = {
            "model": "deepseek-ai/DeepSeek-R1-0528",
            "messages": history[str(user_id)]
        }

        response = requests.post(url, headers=headers, json=data)
        data = response.json()

        if 'choices' in data and data['choices']:
            content = data['choices'][0]['message']['content']
            history[str(user_id)].append({"role": "assistant", "content": content})

            if len(history[str(user_id)]) > 16:
                history[str(user_id)] = [history[str(user_id)][0]] + history[str(user_id)][-15:]

            save_history()

            if '</think>' in content:
                return content.split('</think>', 1)[1]
            return content
        else:
            return f"Ошибка API: {data}"
    except Exception as e:
        return f"Ошибка при запросе: {e}"


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
def handle_text(message):
    try:
        text = message.text
        if text == "Игра в кубик":
            keyboard2 = telebot.types.InlineKeyboardMarkup(row_width=3)
            button1 = telebot.types.InlineKeyboardButton("1", callback_data='1')
            button2 = telebot.types.InlineKeyboardButton("2", callback_data='2')
            button3 = telebot.types.InlineKeyboardButton("3", callback_data='3')
            button4 = telebot.types.InlineKeyboardButton("4", callback_data='4')
            button5 = telebot.types.InlineKeyboardButton("5", callback_data='5')
            button6 = telebot.types.InlineKeyboardButton("6", callback_data='6')
            keyboard2.add(button1, button2, button3, button4, button5, button6)
            bot.send_message(message.chat.id, "Угадай число на кубике", reply_markup=keyboard2)
        elif text == "Игровой автомат":
            value = bot.send_dice(message.chat.id, emoji='🎰').dice.value
            if value in (1, 22, 43, 16, 32, 48):
                bot.send_message(message.chat.id, "Победа!")
            elif value == 64:
                bot.send_message(message.chat.id, "Jackpot!")
            else:
                bot.send_message(message.chat.id, "Попробуй еще раз")       
        elif text == "Распознавание цифр":
            send1 = bot.send_message(message.chat.id, "Загрузите изображение цифры")
            bot.register_next_step_handler(send1, ident_number)
        elif text == "Распознавание животных":
            send2 = bot.send_message(message.chat.id, "Загрузите изображение кошки или собаки")
            bot.register_next_step_handler(send2, ident_cat_dog)
        else:
            bot.send_message(message.chat.id, "Думаю над ответом...")
            answer = chat(message.chat.id, message.text)
            bot.send_message(message.chat.id, answer, parse_mode='Markdown')
            bot.delete_message(message.chat.id, message.id+1)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")


@bot.callback_query_handler(func=lambda call: call.data in ("1", "2", "3", "4", "5", "6"))
def dice_answer(call):
    value = bot.send_dice(call.message.chat.id, emoji='').dice.value
    if str(value) == call.data:
        bot.send_message(call.message.chat.id, "Победа")
    else:
        bot.send_message(call.message.chat.id, "Попробуй ещё раз")

if __name__ == "__main__":
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
