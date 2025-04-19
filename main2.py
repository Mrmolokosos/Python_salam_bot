import telebot

Token = ""
bot = telebot.TeleBot(Token)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Salom video olish uchu /video deb yozing!")

@bot.message_handler(commands=['video'])
def send_video(message):
    with open("video.mp4", "rb") as video:
        bot.send_video(message.chat.id, video, caption='video')
bot.polling()