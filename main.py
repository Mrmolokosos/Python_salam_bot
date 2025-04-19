import telebot

Token = ""
bot = telebot.TeleBot(Token)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Salom mashina rasmini olish uchun quydagi markalarni tanlang: /Mercedes, /Mazda, /BMW, /Toyota, /Ferrari")

@bot.message_handler(commands=['Mercedes'])
def send_image(message):
    with open("salom.jpg", "rb") as img:
        bot.send_photo(message.chat.id, img, caption='Merscedes')


@bot.message_handler(commands=['Mazda'])
def send_image(message):
    with open("salom2.jpg", "rb") as img:
        bot.send_photo(message.chat.id, img, caption='Mazda')


@bot.message_handler(commands=['BMW'])
def send_image(message):
    with open("salom3.jpg", "rb") as img:
        bot.send_photo(message.chat.id, img, caption='BMW')


@bot.message_handler(commands=['Toyota'])
def send_image(message):
    with open("salom4.jpg", "rb") as img:
        bot.send_photo(message.chat.id, img, caption='Toyota')


@bot.message_handler(commands=['Ferrari'])
def send_image(message):
    with open("salom5.jpg", "rb") as img:
        bot.send_photo(message.chat.id, img, caption='Ferrari')
bot.polling()