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
markup_1 = types.InlineKeyboardMarkup(row_width=3)
markup_2 = types.InlineKeyboardMarkup(row_width=3)


def fill_markup(half):
    markup = types.InlineKeyboardMarkup(row_width=3)
    if half == 0:
        i = 0
        while i <= buttons.__len__() / 2 - 1:
            markup.add(buttons[i])
            i += 1
    elif half == 1:
        i = 10
        while i <= buttons.__len__() - 1:
            markup.add(buttons[i])
            i += 1
    markup.add(InlineKeyboardButton('<', callback_data="BtnBack"), InlineKeyboardButton('♥', callback_data="BtnLike"),
               InlineKeyboardButton('>', callback_data="BtnForward"))
    return markup


def fill_buttons(message):
    videos = search(message.text)
    n = 0
    while n <= videos[0].__len__() - 1:
        title = videos[0][n]['title']
        buttons.append(InlineKeyboardButton(title, callback_data="btn" + videos[0][n]['link']))
        n += 1


#links =[]
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
