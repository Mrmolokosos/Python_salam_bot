import telebot

Token = ""
bot = telebot.TeleBot(Token)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Salom video olish uchu /audio deb yozing!")

@bot.message_handler(commands=['audio'])
def send_audio(message):
    with open("audio.mp3", "rb") as video:
        bot.send_audio(message.chat.id, video, caption='Ваша музыка')
bot.polling()