import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

token = "7604539016:AAHbUJhVMHBzXjhqe47hyQGQPA6FXYBghtw"
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = InlineKeyboardMarkup()


    markup.add(InlineKeyboardButton('Video yuborish', callback_data="video"))
    markup.add(InlineKeyboardButton('Audio yuborish', callback_data="audio"))
    markup.add(InlineKeyboardButton('Image yuborish', callback_data="image"))
    bot.send_message(message.chat.id, "quyidagi tugmalardan birini tanlang: ", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "video")
def callback_hello(call):
    with open("video.mp4", "rb") as video:
        bot.send_video(call.message.chat.id, video, caption='video')


@bot.callback_query_handler(func=lambda call: call.data == "audio")
def callback_hello(call):
    with open("audio.mp3", "rb") as audio:
        bot.send_audio(call.message.chat.id, audio, caption='audio')


@bot.callback_query_handler(func=lambda call: call.data == "image")
def callback_hello(call):
   with open("salom3.jpg", "rb") as img:
        bot.send_photo(call.message.chat.id, img, caption='Merscedes')
bot.polling()