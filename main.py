import gspread
from datetime import date
import telebot
import config

TOKEN = config.TOKEN
googlesheet_id = config.googlesheet_id
bot = telebot.TeleBot(TOKEN)
gc = gspread.service_account()
sh = gc.open_by_key(googlesheet_id)
#Проверка 1 строки таблицы
#print(sh.sheet1.get("A1:E1"))

# приветствуем пользователя и говорим что умеем..
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
                 "Привет, я буду записывать ваши расходы в гугл таблицу. Введите расход через дефис в виде [КАТЕГОРИЯ-ЦЕНА-КОММЕНТАРИЙ]:")
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    try:
        today = date.today().strftime("%d.%m.%Y")
        #  разделяем сообщение на 3 части, категория, цена, соментарий
        category, price, coment = message.text.split("-", 2)
        text_message = f'На {today} в таблицу добавлена запись: категория {category}, сумма {price} руб'
        bot.send_message(message.chat.id, text_message)
        user = message.from_user.first_name
        username = message.from_user.username

        # открываем Google таблицу и добавляем запись
        sh = gc.open_by_key(googlesheet_id)
        sh.sheet1.append_row([today, category, price, user,username, coment])
    except:
        # если пользователь ввел неправильную информацию, оповещаем его и просим вводить повторно
        bot.send_message(message.chat.id, 'ОШИБКА! Неправильный формат данных!')
    bot.send_message(message.chat.id, 'Введите расход через дефис в виде [КАТЕГОРИЯ-ЦЕНА-КОММЕНТАРИЙ]:')
if __name__ == '__main__':
    bot.polling(none_stop=True)