from telebot import TeleBot
import threading
import time

bot = TeleBot("7763337851:AAF4RmDULesSfGvL-fpTPu0xrw7r18M_vco")

def send_photos(chat_id):
    for i in range(1, 6):
        photo_path = f"{i}.jpg"
        try:
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo)
            time.sleep(1)
        except FileNotFoundError:
            bot.send_message(chat_id, f"Файл {photo_path} не найден.")
            break

def send_videos(chat_id):
    for i in range(1, 6):
        video_path = f"{i}.mp4"
        try:
            with open(video_path, 'rb') as video:
                bot.send_video(chat_id, video)
            time.sleep(1)
        except FileNotFoundError:
            bot.send_message(chat_id, f"Файл {video_path} не найден.")
            break

def long_task(chat_id):
    bot.send_message(chat_id, "Работа началась....")
    send_photos(chat_id)
    send_videos(chat_id)
    bot.send_message(chat_id, "Работа закончилась")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Используйте команду /task для начала.")

@bot.message_handler(commands=['task'])
def task_handler(message):
    chat_id = message.chat.id
    thread = threading.Thread(target=long_task, args=(chat_id,))
    thread.start()
    bot.send_message(chat_id, "Работа началась! Подождите..... ")

bot.polling()