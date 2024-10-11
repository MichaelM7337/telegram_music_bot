import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
API_TOKEN = '6987658935:AAFd_tGI8-rAZA-Q5OCNN1ep6ramcTwnN_4'

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, """)

buttons = [[]]
buttons.append(InlineKeyboardButton("Btn1", callback_data="btn1"))
buttons.append(InlineKeyboardButton("Btn2", callback_data="btn2"))

markup = types.InlineKeyboardMarkup(row_width=2)
button = types.InlineKeyboardButton()

markup.add(button_foo, button_bar, button_a, button_b)

bot.send_message(message.chat.id, text='Some text', reply_markup=markup)

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for i in buttons:
        markup.add(i)
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_yes":
        bot.answer_callback_query(call.id, "Answer is Yes")
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "Answer is No")

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_markup())

@bot.inline_handler(func=lambda message: ['button'])
def show_choices(message):
    bot.message_handler(message)
# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
