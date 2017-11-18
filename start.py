# -*- coding: utf-8 -*-
from telegram.ext import Updater  # пакет называется python-telegram-bot, но Python-
from telegram.ext import CommandHandler  # модуль почему-то просто telegram ¯\_(ツ)_/¯
from telegram.ext import MessageHandler
from telegram.ext import RegexHandler
import sqlite3
import hashlib
from cleaner import Porter
from operator import attrgetter

DB_FAQ_KAI = "db_001.db"

needed_column = 2

col_indx = (needed_column * 2) - 1


def start(bot, update):
    # подробнее об объекте update: https://core.telegram.org/bots/api#update
    print(update.message.chat.username)
    con = sqlite3.connect(DB_FAQ_KAI)
    cur = con.cursor()
    results = search(cur, update, "About_military", "Question")
    sort = sorted(results, key=lambda k: k['matchedCount'])[-3:]
    # выдаёт только ВопросОтвет
    # qwe=[]
    for id, item in enumerate(sort):
        # qwe.append(item['question'][1])
        t = item['question'][1]
        bot.sendMessage(chat_id=update.message.chat_id, text=str(t))
    con.close()


def search(cur, update, table, column):
    resByAllWordsArr = []  # [[][][]]
    justMmm = []
    for word in str(update.message.text).split(" "):  # TODO: or 2 or 3 spaces
        cur.execute("SELECT * "
                    "FROM " + table + " "
                                      "WHERE " + column + " LIKE '%" + word + "%'")
        # resArray=
        temp = cur.fetchall()
        resByAllWordsArr.append(temp)  # append добавляет мссив в первую ячейку
        justMmm += temp
    r = []

    for resByWordArr in list(set(
            justMmm)):  # TODO:[[][][]] #list(set(resAllWords)) - все вопросы которые сматчились в поиске предыдущем, ни не повторяются
        for resArr in resByAllWordsArr:  # []
            for machedQuestion in resArr:
                if (machedQuestion == resByWordArr):
                    temp_hash = hashlib.md5(str(machedQuestion[0]).encode("utf-8")).digest()
                    firstStepForThisItem = True
                    for q in r:
                        # Done q1, q2, q3=q# todo: how q['hash']
                        if q['hash'] == temp_hash:  # or q1==temp_hash or q2==temp_hash:
                            firstStepForThisItem = False
                            q['matchedCount'] += 1
                    # t=any ( tt )
                    if (firstStepForThisItem):  # count ==0
                        r.append({'hash': temp_hash, 'question': machedQuestion, 'matchedCount': 1})
                        # else:

    return r

def word_cleaner(lst):
    except_words = ['', 'и', 'да', 'также', 'тоже', 'а', 'но', 'зато', 'однако', 'однако же', 'все же', 'или', 'что',
               'чтобы', 'как', 'когда',
               'лишь', 'едва', 'чтобы', 'дабы', 'если', 'если бы', 'коли', 'хотя', 'хоть', 'пускай', 'как',
               'как будто', 'эт', 'бы']

    lst = lst.replace(',', '').replace('!', '').replace('?', '').replace('-', '').replace('.', '')
    lst = lst.split(' ')

    for souz in except_words:
        lst = [Porter.stem(x) for x in lst if souz != x]

    return lst

    # todo resOne= resArray.split(",")[1].split("'")[1]
    # todo count maches


# @kai7_bot
updater = Updater(token='461661232:AAExDNSsp3zQfL3oAovRhi3TVQKZWEJr7aI')  # тут токен, который выдал вам Ботский Отец!

# start_handler = CommandHandler('', start)  # этот обработчик реагирует
# только на команду /start
start_handler = RegexHandler('.+', start)

updater.dispatcher.add_handler(start_handler)  # регистрируем в госреестре обработчиков
updater.start_polling()  # поехали!
input("starting done")