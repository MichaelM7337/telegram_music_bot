import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from downloader import download_youtube_video
from video_search import search

API_TOKEN = '6987658935:AAFd_tGI8-rAZA-Q5OCNN1ep6ramcTwnN_4'

bot = telebot.TeleBot(API_TOKEN)

botCommands = ['info', 'menu', 'list', 'stop']


@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id, "I am a bot and can be used to listen/store/search for music")
    # buttons = []
    # buttons.append(InlineKeyboardButton("Btn1", callback_data="btn1"))
    # buttons.append(InlineKeyboardButton("Btn2", callback_data="btn2"))
    # markup = types.InlineKeyboardMarkup(row_width=2)
    # #
    # markup.add(buttons[0], buttons[1])
    # bot.send_message(message.chat.id, text='List of commands', reply_markup=markup)

# @bot.message_handler(commands=['menu'])
# def send_menu(message):
    # buttons = []
    # buttons.append(InlineKeyboardButton("Btn1", callback_data="btn1"))
    # buttons.append(InlineKeyboardButton("Btn2", callback_data="btn2"))
    #
    # markup = types.InlineKeyboardMarkup(row_width=2)
    # markup.add(buttons[0], buttons[1])
    # bot.send_message(message.chat.id, text='List of commands', reply_markup=markup)


# @bot.callback_query_handler(func=lambda call: True)
# def callback_query(call):
#     if call.data == "cb_yes":
#         bot.answer_callback_query(call.id, "Answer is Yes")
#     elif call.data == "cb_no":
#         bot.answer_callback_query(call.id, "Answer is No")

buttons = []
markup_1 = types.InlineKeyboardMarkup(row_width=3)
markup_2 = types.InlineKeyboardMarkup(row_width=3)
#links =[]
@bot.message_handler(func=lambda message: True)
def message_handler(message):
    #bot.copy_message(message.chat.id, message)
    videos = search(message.text)
    n = 0
    while n <= videos[0].__len__()-1:
        title = videos[0][n]['title']
        buttons.append(InlineKeyboardButton(title, callback_data="btn" + videos[0][n]['link']))
        if n <= videos[0].__len__()/2 -1 :
        #links.append(videos[0][n]['link'])
            markup_1.add(buttons[n])
        else:
            markup_2.add(buttons[n])
        n+=1
    markup_1.add(InlineKeyboardButton('<', callback_data="BtnBack"), InlineKeyboardButton('♥', callback_data="BtnLike"),
               InlineKeyboardButton('>', callback_data="BtnForward"))
    markup_2.add(InlineKeyboardButton('<', callback_data="BtnBack"), InlineKeyboardButton('♥', callback_data="BtnLike"),
               InlineKeyboardButton('>', callback_data="BtnForward"))
    bot.send_message(message.chat.id, text='Запрошенные песни 1/2', reply_markup=markup_1)

@bot.callback_query_handler(func=lambda call:True)
def callback_buttons(call):
    if call.data == 'BtnForward':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Запрошенные песни 2/2", reply_markup=markup_2)
    elif call.data == 'BtnBack':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Запрошенные песни 1/2", reply_markup=markup_1)
    else:
        for i in buttons:
            if call.data == i.callback_data:
                #bot.answer_callback_query(call.id, i.text)
                bot.send_audio(chat_id=call.message.chat.id, audio=download_youtube_video((i.callback_data)[3:]))

# Start the bot
if __name__ == '__main__':
    bot.polling(none_stop=True)