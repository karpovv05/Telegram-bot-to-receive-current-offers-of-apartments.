import pars_and_sql
import telebot
import sqlite3


token_bot = ''                                       #Впишите токен от BotFather!
bot = telebot.TeleBot(token_bot)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Hi,friend!\n"
                                      "Бот присылает ссылки на сдающиеся квартиры Грузии. \n"
                                      "Нажмите на /help что бы увидеть настройки Бота.")
    pars_and_sql.add_data_person_into_sql(message.from_user.id, message.from_user.first_name)

@bot.message_handler(commands=["help"])
def start(message):
    bot.send_message(message.chat.id, "Привет! \n"
                                      "Настройка бота \n"
                                      "Нажми --> /template_change_True что бы включить уведомления\n"
                                      "Нажми --> /template_change_False что бы выключить уведомления")
    pars_and_sql.add_data_person_into_sql(message.from_user.id, message.from_user.first_name)

@bot.message_handler(content_types=['text'])
def temlate_requests(message):
    if message.text == "/template_change_True":
        pars_and_sql.change_tamlet_get(True,message.from_user.id)
        bot.send_message(message.from_user.id,'ОК)')

    if message.text == "/template_change_False":
        pars_and_sql.change_tamlet_get(False,message.from_user.id)

        bot.send_message(message.from_user.id,'ОК(')






def send_message_all():
    conn = sqlite3.connect("sql_url_apart.db")
    conn = conn.cursor()
    get_data = conn.execute('select * from users_id').fetchall()
    url = conn.execute('select * from get_urls').fetchone()
    conn.close()

    """Id/name/get_url?"""
    id_list = [i[0] for i in get_data if i[2] == "True"]  # Можно отсортировать кому отправлять!
    for id in id_list:
        try:
            bot.send_message(id, url)
            print(id)

        except telebot.apihelper.ApiTelegramException as error:
            pars_and_sql.change_tamlet_get(False, id)
            print("Error:",error)



def start_bot():
    bot.infinity_polling(none_stop=True)

