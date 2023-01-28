import telebot
from telebot import types

from config import bot_token, owner_id
from chatgpt import OpenAI
from database import *
from analysis import statistic

print('Active')
bot = telebot.TeleBot(bot_token)
openai = OpenAI()
search_table()


# First launch
@bot.message_handler(commands=["start", "help"])
def start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в ChatGPT в телеграмме!\n\n'
                                      'Настройка бота:\n\n'
                                      '/translate - '
                                      'Выберите хотите ли вы автоматически переводить Русский текст на Английский '
                                      '(Ответ от бота тоже будет на Русском языке)\nПо умолчанию: Отключен\n\n'
                                      '/temperature -'
                                      'Выберите точность ответа '
                                      '(0 - Точный но медленный ответ от бота. 10 - Неточный но более быстрый ответ от бота)\n'
                                      'По умолчанию: 5')


# Changing the translation function
@bot.message_handler(commands=["translate"])
def translate(message):
    get_value = Database(message.from_user.id)

    markup = types.InlineKeyboardMarkup()
    if get_value.get_translate():
        translate_off = types.InlineKeyboardButton("Отключить", callback_data='off')
        markup.add(translate_off)
        bot.send_message(message.chat.id,
                         'Режим перевода включен', reply_markup=markup)
    else:
        translate_on = types.InlineKeyboardButton("Включить", callback_data='on')
        markup.add(translate_on)
        bot.send_message(message.chat.id,
                         'Режим перевода отключен\n\nПри включении не рекомендуется делать запросы боту,'
                         'перевод которых будет неуместен', reply_markup=markup)


@bot.message_handler(commands=["temperature"])
def temperature(message):
    get_value = Database(message.from_user.id)

    markup = types.InlineKeyboardMarkup()
    switch = types.InlineKeyboardButton("Изменить", callback_data='swt')
    markup.add(switch)
    bot.send_message(message.chat.id, f'Текущая точность ответа: {int(get_value.get_temperature() * 10)}', reply_markup=markup)


@bot.message_handler(commands=["analysis"])
def analysis(message):
    if message.from_user.id == owner_id:
        bot.send_message(owner_id, statistic())


# Inline button
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    req = call.data.split('_')
    get_value = Database(call.from_user.id)

    if req[0] == 'swt':
        save_value(call.from_user.id, switch=True)
        bot.send_message(call.message.chat.id, 'Введите точность ответа '
                                               '(0 - Точный но медленный ответ от бота. 10 - Неточный но более быстрый ответ от бота)\n'
                                               f'Текущее значение: {int(get_value.get_temperature() * 10)}')

    if req[0] == 'on':
        save_value(call.from_user.id, translate=True)
        markup = types.InlineKeyboardMarkup()
        translate_off = types.InlineKeyboardButton("Отключить", callback_data='off')
        markup.add(translate_off)
        bot.edit_message_text('Режим перевода включен', reply_markup=markup,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)

    if req[0] == 'off':
        save_value(call.from_user.id, translate=False)
        markup = types.InlineKeyboardMarkup()
        translate_on = types.InlineKeyboardButton("Включить", callback_data='on')
        markup.add(translate_on)
        bot.edit_message_text('Режим перевода отключен\n\nПри включении не рекомендуется делать запросы боту,'
                              'перевод которых будет неуместен', reply_markup=markup,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    get_value = Database(message.from_user.id)
    # Choice of answer accuracy
    if get_value.get_switch():
        try:
            num = int(message.text.strip())
            if 0 <= num <= 10:
                save_value(message.from_user.id, switch=False, temperature=num / 10)
                bot.send_message(message.chat.id, f'Установлено значение: {num}')
            else:
                bot.send_message(message.chat.id, 'Пожалуйста введите число от 0 до 10')
        except ValueError:
            bot.send_message(message.chat.id, 'Пожалуйста введите число от 0 до 10')
    # Interaction with
    else:
        bot.send_message(message.chat.id, 'Подождите...')
        try:
            # Request in Russian
            if get_value.get_translate():
                bot.send_message(message.chat.id, openai.translate_chatgpt(message.text, get_value.get_temperature()))
            else:
                bot.send_message(message.chat.id, openai.chatgpt(message.text, get_value.get_temperature()))
        except:
            bot.send_message(message.chat.id, 'Пожалуйста отправьте запрос повторно')
        # Deleting a message "Подождите..."
        bot.delete_message(message.chat.id, message.id + 1)
bot.polling(none_stop=True, interval=0, timeout=20)
