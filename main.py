import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from downloader import youtubeSongDownloader
from video_search import search

API_TOKEN = '6987658935:AAFd_tGI8-rAZA-Q5OCNN1ep6ramcTwnN_4'

bot = telebot.TeleBot(API_TOKEN)

botCommands = ['info', 'menu', 'list', 'stop']


@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id, "I am a bot and can be used to listen/store/search for music")


buttons = []

def fill_markup(half):
    markup = types.InlineKeyboardMarkup(row_width=3)
    button_count = len(buttons)
    midpoint = int(button_count // 2)

    if half == 0:
        for i in range(midpoint):
            markup.add(buttons[int(i)])

    elif half == 1:
        for i in range(midpoint, button_count):
            markup.add(buttons[int(i)])
    markup.add(
  InlineKeyboardButton('<', callback_data="BtnBack"),
        InlineKeyboardButton('♥', callback_data="BtnLike"),
        InlineKeyboardButton('>', callback_data="BtnForward"))

    return markup

def fill_buttons(message):
    videos = search(message.text)
    for video in videos:
        title = video['title']
        link = video['link']
        buttons.append(InlineKeyboardButton(title, callback_data="btn" + link))

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    fill_buttons(message)
    bot.send_message(message.chat.id, text='Запрошенные песни 1/2', reply_markup=fill_markup(0))


@bot.callback_query_handler(func=lambda call: True)
def callback_buttons(call):
    if call.data == 'BtnForward':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Запрошенные песни 2/2", reply_markup=fill_markup(1))
    elif call.data == 'BtnBack':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Запрошенные песни 1/2", reply_markup=fill_markup(0))
    else:
        for i in buttons:
            if call.data == i.callback_data:
                buttons.clear()
                youtubeSongDownloader((i.callback_data)[3:])

                bot.send_audio(chat_id=call.message.chat.id, audio=open('Music//' + i.text + '.mp3', 'rb'))


# Start the bot
if __name__ == '__main__':
    bot.polling(none_stop=True)
