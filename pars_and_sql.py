import requests
import bs4
import sqlite3
import time
import bot_tg
from threading import Thread


def check_if_new_src(new_url):
    try:
        conn = sqlite3.connect("sql_url_apart.db")
        cursor = conn.cursor()
        comand = cursor.execute(f'select * from get_urls where rowid=1')
        get_url_sql = comand.fetchone()[0]
        if get_url_sql == new_url:
            return timer()
        else:
            conn.commit()


            return new_url


    except sqlite3.Error as error:
        print("Error", error)

    finally:
        if (conn):
            conn.close()


def parser_page_appart():
    url = "https://ss.ge/en/real-estate/l/Flat/For-Rent?Sort.SortExpression=%22OrderDate%22%20DESC&RealEstateTypeId=5&RealEstateDealTypeId=1&MunicipalityId=95&CityIdList=95&PrcSource=2&PriceType=false&CurrencyId=2&PriceTo=700"
    get_url = requests.get(url)
    soup = bs4.BeautifulSoup(get_url.text, "html.parser")
    redy_url = "https://ss.ge" + soup.find("div", class_="latest_article_each_in").find("div", "latest_desc").a.get(
        'href')
    return redy_url


def add_url_apart_sql(new_url):
    try:
        conn = sqlite3.connect("sql_url_apart.db")
        cursor = conn.cursor()
        cursor.execute(f'update get_urls set ("url") = ("{new_url}") where rowid = 1 ')
        conn.commit()


    except sqlite3.Error as error:
        print("Error", error)

    finally:
        if (conn):
            conn.close()
            Thread(target=bot_tg.send_message_all).start()


def add_data_person_into_sql(id, name):
    try:

        conn = sqlite3.connect("sql_url_apart.db")
        cursor = conn.cursor()
        cursor.execute(f'insert into users_id values ("{id}","{name}","{False}")')

        conn.commit()

    except sqlite3.Error as error:
        print("Error", error)

    finally:
        if (conn):
            conn.close()





def change_tamlet_get(BOOLEAN,user_id):
    try:
        conn = sqlite3.connect("sql_url_apart.db")
        cursor = conn.cursor()
        if BOOLEAN:
            cursor.execute(f'update users_id set ("template_get") = ("{True}") where ("id") = ("{user_id}")  ')
        else:
            cursor.execute(f'update users_id set ("template_get") = ("{False}") where ("id") = ("{user_id}")  ')



        conn.commit()


    except sqlite3.Error as error:
        print("Error", error)

    finally:
        if (conn):
            conn.close()



def start_all():
    add_url_apart_sql(check_if_new_src(parser_page_appart()))


def timer():
    while True:
        time.sleep(10)
        start_all()
