# -*- coding: utf-8 -*-
from telegram.ext import Updater  # пакет называется python-telegram-bot, но Python-
from telegram.ext import CommandHandler  # модуль почему-то просто telegram ¯\_(ツ)_/¯
from telegram.ext import MessageHandler
from telegram.ext import RegexHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, bot,ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.update import Update, Message
import sqlite3
import hashlib
from cleaner import Porter
from operator import attrgetter
from Db import Db
# import threading

needed_column = 2   

col_indx = (needed_column * 2) - 1



def start(bot, update):# нам сёда пришел поисковый запрос от Юзера
    # подробнее об объекте update: https://core.telegram.org/bots/api#update
    print(update.message.chat.username)

    results = search(update.message.text, "T_Question_Answer", "Question")# TODO: поменять бд
    sort = sorted(results, key=lambda k: k['matchedCount'])[:3]
    # выдаёт только ВопросОтвет
    for item in sort:
        keyboard = [[InlineKeyboardButton("Показать ответ:", callback_data=item['question'][0])]]
        reply = InlineKeyboardMarkup(keyboard)
        t = item['question'][1]
        update.message.reply_text(str(t), reply_markup=reply)
        
    gg= str(update.message.message_id)+';' + str(sort[0]['question'][0])+','+str(sort[1]['question'][0])+','+str(sort[2]['question'][0] )
    keyboard = [[InlineKeyboardButton("Показать еще!", callback_data= gg)]]# TODO: ссылка на мессадж
    reply = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("____У нас есть еще:)_____", reply_markup=reply)
        # bot.sendMessage(chat_id=update.message.chat_id, text=str(t), reply_markup=reply)

def giveAnswer (bot, update):
    print('[giveAnswer]:')
    query = update.callback_query
    print('[giveAnswer]' +query.message.text)
    query = update.callback_query

    if query.find(';')!=-1:
        bot.edit_message_text(text="Тра-ля ЛЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯ",
                            chat_id=query.message.chat_id,
                            message_id=query.split(';')[0]), 

    #print(update.message.chat.username+' [giveAnswer]'+'\r\n'+query.message.text+'\r\n')
    t='<b>'+query.message.text+'</b> \r\n'+Db().GetByColumnName('db_001.db', 'T_Question_Answer', 'id',query.data)[0][2]
    bot.edit_message_text(text=t,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id, 
                          parse_mode=ParseMode.HTML)

def search(text, table, column):
    resByAllWordsArr = []  # [[][][]]
    justMmm = []
    for word in word_cleaner(text):  # TODO: or 2 or 3 spaces
        temp = Db().search_by_word_with_like('db_001.db', table, column, word)
        resByAllWordsArr.append(temp)  # append добавляет мссив в первую ячейку
        justMmm += temp
    r = []

    for resByWordArr in list(set(justMmm)): #list(set(resAllWords)) - все вопросы которые сматчились в поиске предыдущем, ни не повторяются
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

    counter = 0
    for souz in except_words:
        for x in lst:
            if souz != x:
                try:
                    lst.replace(x, Porter.stem(x))
                except AttributeError:
                    counter += 1
            else:
                lst.remove(x)

    return lst
    # todo count maches


# @kai7_bot 
updater = Updater(token='461661232:AAExDNSsp3zQfL3oAovRhi3TVQKZWEJr7aI')  # тут токен, который выдал вам Ботский Отец!

# start_handler = CommandHandler('', start)  # этот обработчик реагирует
# только на команду /start
start_handler = RegexHandler('.+', start)

updater.dispatcher.add_handler(start_handler)  # регистрируем в госреестре обработчиков
updater.dispatcher.add_handler(CallbackQueryHandler(giveAnswer))
updater.start_polling()  # поехали!

#updater.idle()
input("started")

