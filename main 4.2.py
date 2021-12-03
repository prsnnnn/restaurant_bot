import telebot
import time
from telebot import types
from config import TOKEN, admin_list, emoji
from requests import exceptions
from pymongo import MongoClient
import datetime
import os
import matplotlib.pyplot as plt
import random
import threading

bot=telebot.TeleBot(TOKEN)
mongo=MongoClient("localhost", port=27017)
bl=0
f=0

'''robot=u'\U0001F916'
feet=u'\U0001F463'
time=u'\U0001F551'
save=u'\U0001F4BE'
cam=u'\U0001F4F7'
rev=u'\U0001F4DD'
#back=u'\U0001F519'
back=u'\U000021A9'
mai=u'\U0001F4E9'
ab=u'\U0001F530'
lo=u'\U0001F512'
unlo=u'\U0001F513'
yep=u'\U00002705'
book=u'\U0001F4D6'
left=u'\U00002B05'
right=u'\U000027A1'
tochka=u'\U00002716'
maps=u'\U0001F5FA'
red=u'\U0001F534'
green=u'\U0001F7E2'
redc=u'\U000026D4'
'''



#==Starting decorator==
#@bot.message_handler(commands=["start", "help"],)
global message
global emoji
@bot.message_handler(content_types=['text'])
def starting(message):
    #==Main markup==
    global chat_id
    global emoji
    chat_id=message.chat.id
    def mu1(message):
        global chat_id
        chat_id=message.chat.id
        user_name=message.from_user.first_name
        markup1=types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup1.add('Забронировать столик '+emoji["time"],'Меню '+emoji["book"],'О ресторане '+emoji["ab"], 'Где нас найти '+emoji["feet"],'Отзывы '+emoji["rev"])
        send3=bot.send_message(chat_id, "Выберите пункт меню:", reply_markup=markup1)
        bot.register_next_step_handler(send3,second)
        print(message.chat.id)
    def logg(message):
        global chat_id
        global NEW_USER
        global TO_FOUND
        chat_id=message.chat.id
        if message.text=='Зарегестрироватся':
            NEW_USER={"User ID":chat_id,"Name":"","Phone":"", "Password":"", "Mailing":0}
            s=bot.send_message(chat_id, 'Введите ваше имя')
            bot.register_next_step_handler(s,name)
        elif message.text=='Войти':
            phlog(message)
    def phlog(message):
        global chat_id
        global TO_FOUND
        chat_id=message.chat.id
        s=bot.send_message(chat_id,'Введите Ваш номер телефона (380xxxxxxx)')
        TO_FOUND={'Phone':"","Password":""}
        bot.register_next_step_handler(s,login)
    def login(message):
        global chat_id
        global TO_FOUND
        global FOUNDED
        chat_id=message.chat.id
        fr=0
        if len(message.text)==12:
            try:
                if isinstance(int(message.text), int):
                    TO_FOUND['Phone']=int(message.text)
                    FOUNDED=''
                    telebot=mongo["telebot"]
                    users=telebot["users"]
                    reg_users = users.find({},{"Phone":1})
                    for reg_user in reg_users:
                        if TO_FOUND["Phone"]==reg_user["Phone"]:
                            fr=1
                            FOUNDED=reg_user['Phone']
                            k=bot.send_message(chat_id, "Введите пароль")
                            bot.register_next_step_handler(k,passlog)
                            break
                        else:
                            fr=0
            except ValueError:
                print('sss')
            else:
                bot.send_message(chat_id, "Неверный номер телефона!")
                phlog(message)
        else:
            bot.send_message(chat_id, "Неверный номер телефона!")
            phlog(message)
        if fr==1:
            passlog(message)
        else:
            bot.send_message(chat_id, "Пользователь не найден!")
            phlog(message)
    def passlog(message):
        global chat_id
        global FOUNDED
        chat_id=message.chat.id
        if str(message.text)==str(FOUNDED):
            bot.send_message(chat_id, "Добро пожаловать!")
        else:
            bot.send_message(chat_id,'neverno')
    def name(message):
        global chat_id
        global NEW_USER
        chat_id=message.chat.id
        NEW_USER['Name']=message.text
        s=bot.send_message(chat_id, 'Введите Ваш номер телефона (380xxxxxxx)')
        bot.register_next_step_handler(s,phone)
    def phone(message):
        global chat_id
        global NEW_USER
        chat_id=message.chat.id
        if len(message.text)==12:
            if isinstance(int(message.text), int):
                NEW_USER['Phone']=message.text
                s=bot.send_message(chat_id, 'Введите пароль (мин. 6 символов)')
                bot.register_next_step_handler(s,password)
            else:
                name(message)
        else:
            name(message)
    def password(message):
        global chat_id
        global NEW_USER
        chat_id=message.chat.id
        if len(message.text)>5:
            NEW_USER['Password']=message.text
            telebot=mongo["telebot"]
            users=telebot["users"]
            res=users.insert_one(NEW_USER)
            bot.send_message(chat_id, "Пользователь зарегистрирован")
            mu1(message)
        else:
            phone(message)
    def first(message):
        global chat_id
        global bl
        global f
        chat_id=message.chat.id
        telebot=mongo["telebot"]
        blacklist=telebot["Black List"]
        blocked_users=blacklist.find({},{"User ID":1})
        user_name=message.from_user.first_name
        for blocked_user in blocked_users:
            if int(blocked_user["User ID"])==chat_id:
                bot.send_message(chat_id, "Вы были заблокированы администратором в связи с нарушением правил использования бота")
                bl=1
                break
        if bl==0:
            #user_to_ins={"User ID":chat_id,"Name":,"Phone":"", "Password":""}
            telebot=mongo["telebot"]
            users=telebot["users"]
            reg_users = users.find({},{"User ID":1,"Name":1,"Phone":1, "Password":1})
            for reg_user in reg_users:
                if chat_id==reg_user["User ID"]:
                    f=1
                    break
                else:
                    f=0
            if f==0:
                #res=users.insert_one(user_to_ins)
                #user_name=message.from_user.first_name
                timen = time.localtime()
                hr = int(time.strftime("%H", timen))
                if hr>=0 and hr<=5:
                    send=bot.send_message(chat_id, f"Доброй ночи {emoji['moon']}, {user_name}, я чат бот самого лучшего ресторана "+emoji["robot"])
                    markup=types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    markup.add('Зарегестрироватся','Войти')
                    send1=bot.send_message(chat_id, f"Для начала работы с ботом необходимо пройти авторизацию\nВыберите что бы Вы хотели ", reply_markup=markup)
                    bot.register_next_step_handler(send1, logg)
                elif hr>=22 and hr<=24:
                    send=bot.send_message(chat_id, f"Доброй ночи {emoji['moon']}, {user_name}, я чат бот самого лучшего ресторана "+emoji["robot"])
                    markup=types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    markup.add('Зарегестрироватся','Войти')
                    send1=bot.send_message(chat_id, f"Для начала работы с ботом необходимо пройти авторизацию\nВыберите что бы Вы хотели ", reply_markup=markup)
                    bot.register_next_step_handler(send1, logg)
                elif hr>=6 and hr<=11:
                    send=bot.send_message(chat_id, f"Доброе утро {emoji['sun']}, {user_name}, я чат бот самого лучшего ресторана "+emoji["robot"])
                    markup=types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    markup.add('Зарегестрироватся','Войти')
                    send1=bot.send_message(chat_id, f"Для начала работы с ботом необходимо пройти авторизацию\nВыберите что бы Вы хотели ", reply_markup=markup)
                    bot.register_next_step_handler(send1, logg)
                elif hr>=12 and hr<=18:
                    send=bot.send_message(chat_id, f"Добрый день {emoji['city']}, {user_name}, я чат бот самого лучшего ресторана "+emoji["robot"])
                    markup=types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    markup.add('Зарегестрироватся','Войти')
                    send1=bot.send_message(chat_id, f"Для начала работы с ботом необходимо пройти авторизацию\nВыберите что бы Вы хотели ", reply_markup=markup)
                    bot.register_next_step_handler(send1, logg)
                elif hr>=19 and hr<=21:
                    send=bot.send_message(chat_id, f"Добрый вечер {emoji['evn']}, {user_name}, я чат бот самого лучшего ресторана "+emoji["robot"])
                    markup=types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    markup.add('Зарегестрироватся','Войти')
                    send1=bot.send_message(chat_id, f"Для начала работы с ботом необходимо пройти авторизацию\nВыберите что бы Вы хотели ", reply_markup=markup)
                    bot.register_next_step_handler(send1, logg)
            elif f==1:
                mu1(message)
        #mu1(message)

    def gr(message):
        if message.text=="Главное меню" or message.text=="Назад "+emoji["back"]:
            mu1(message)
    def menu(message):
        global call_id
        global mesage_id
        chat_id=message.chat.id
        if message.text=="Назад "+emoji["back"] or message.text=="Главное меню":
            mu1(message)
        elif message.text=="Текстовое меню":
            markup_backk1=types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup_backk1.add("Назад "+emoji["back"])
            keyboard = types.InlineKeyboardMarkup()
            #callback_button1 = types.InlineKeyboardButton(text="1", callback_data="menu1")
            #callback_button2 = types.InlineKeyboardButton(text="2", callback_data="menu2")
            callback_button1 = types.InlineKeyboardButton(text=emoji["tochka"], callback_data="1")
            callback_button2 = types.InlineKeyboardButton(text=emoji["tochka"], callback_data="1")
            callback_button3 = types.InlineKeyboardButton(text=emoji["right"], callback_data="menu2")
            keyboard.add(callback_button1,callback_button2,callback_button3)
            pr="="*15
            txt_menu=f"Яйца пашот со слабосолёным лососем на пшеничной булочкеи голландским соусом, 360 г\n{pr}\nСкрембл с копчёным лососем-терияки и киноа, 310 г \n{pr}\nБоул с тигровой креветкой, авокадо и яйцом, 280 г \n{pr}\nЯйцо запечённое вавокадо с семенамимикс и бебишпинатом, 200 г\n{pr}\nПерепелиные яйцана тосте из деревенскогохлеба с сальсой изпечёных овощейи индейкой су-видс кунжутным соусом, 360 г\n{pr}\nШакшука со страчетеллойи хрустящим багетом, 430 г\n{pr}\nЯйца пашот на чёрном тостес гуакамоле и копчёнымлососем-терияки под сырнымсоусом, 360 г"
            p=bot.send_message(chat_id, txt_menu,reply_markup=keyboard)
            call_id=int(message.chat.id)
            mesage_id=int(p.message_id)
            bot.register_next_step_handler(p, gr)
        elif message.text=="Полное меню (pdf)":
            mu_back=types.ReplyKeyboardMarkup(one_time_keyboard=True)
            mu_back.add("Назад "+emoji["back"])
            f = open("menu.pdf","rb")
            p=bot.send_document(message.chat.id,f, reply_markup=mu_back)
            bot.register_next_step_handler(p, gr)
    # ==Admin Orders checking==
    def finding_orders(message):
        global order
        global order_li
        global chat_id
        chat_id=message.chat.id
        telebot=mongo["telebot"]
        preorders=telebot["pre-orders"]
        order = preorders.find({},{"User ID":1,'UserName':1,'Phone':1,'Pre-order': 1, "Time":1, "Status":1})
        markup_ap=types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_ap.add('Подтвердить '+emoji["yep"],"Отклонить "+emoji['redc'], "Назад "+emoji['back'])
        order_li=list(order)
        print(order_li)
        def backm(message):
            if message.text=="Назад "+emoji["back"]:
                mu1(message)
        try:
            if len(order_li)==1:
                bot.send_message(chat_id, f"У вас 1 новый заказ")
            elif len(order_li)>0 and len(order_li)!=1:
                bot.send_message(chat_id, f"У вас {len(order_li)} новых заказов")
            link=f"[{order_li[0]['UserName']}](tg://user?id={order_li[0]['User ID']})"
            #bot.send_message(chat_id,link, parse_mode='Markdown')
            #link="["+str(order_li[0]['UserName'])+"](tg://user?id="+str(order_li[0]['User ID'])+")"
            ord_txt=f'User ID: {order_li[0]["User ID"]}\nUser: {link}\nPhone: +{order_li[0]["Phone"]}\nOrder: {order_li[0]["Pre-order"]}'
            s=bot.send_message(chat_id, ord_txt, reply_markup=markup_ap,parse_mode='Markdown')
            bot.register_next_step_handler(s, approving)
        except IndexError:
            b=bot.send_message(chat_id, "Заказов нету!")
            admin_menu(message)
    def approving(message):
        global chat_id
        global order
        global order_li
        chat_id=message.chat.id
        if message.text=="Подтвердить "+emoji["yep"]:
            telebot=mongo["telebot"]
            completed_orders=telebot["completed orders"]
            preorders=telebot["pre-orders"]
            completed_order={"User ID":order_li[0]["User ID"],'Pre-order': order_li[0]["Pre-order"], "Time":order_li[0]["Time"], "Status":1}
            delet={"User ID":order_li[0]["User ID"],'Pre-order': order_li[0]["Pre-order"], "Time":order_li[0]["Time"], "Status":0}
            preorders.delete_one(delet)
            res=completed_orders.insert_one(completed_order)
            bot.send_message(chat_id, "Заказ подтвержден")
            bot.send_message(completed_order['User ID'], f"Ваш заказ подтвержден {emoji['yep']}\nЖдем Вас в ресторане :)")
            finding_orders(message)
        elif message.text=="Отклонить "+emoji['redc']:
            telebot=mongo["telebot"]
            completed_orders=telebot["completed orders"]
            preorders=telebot["pre-orders"]
            completed_order={"User ID":order_li[0]["User ID"],'Pre-order': order_li[0]["Pre-order"], "Time":order_li[0]["Time"], "Status":0}
            delet={"User ID":order_li[0]["User ID"],'Pre-order': order_li[0]["Pre-order"], "Time":order_li[0]["Time"], "Status":0}
            preorders.delete_one(delet)
            res=completed_orders.insert_one(completed_order)
            bot.send_message(chat_id, "Заказ отклонен")
            bot.send_message(completed_order['User ID'], f"Ваш заказ отклонен :(\nВозможно, Вы дали ложную информацию либо нарушили правила нашего ресторана")
            finding_orders(message)
        elif message.text=="Назад "+emoji['back']:
            admin_menu(message)
    #==BLACKLIST==
    def choosing(message):
        global chat_id
        chat_id=message.chat.id
        if message.text=="Заблокировать "+emoji["lo"]:
            mu_backk1=types.ReplyKeyboardMarkup(one_time_keyboard=True)
            mu_backk1.add("Назад "+emoji['back'])
            s3=bot.send_message(chat_id,'Введите "User ID" чтобы заблокировать пользователя', reply_markup=mu_backk1)
            bot.register_next_step_handler(s3, blocking)
        elif message.text=="Разблокировать "+emoji["unlo"]:
            mu_backk2=types.ReplyKeyboardMarkup(one_time_keyboard=True)
            mu_backk2.add("Назад "+emoji['back'])
            s3=bot.send_message(chat_id,'Введите "User ID" чтобы разблокировать пользователя', reply_markup=mu_backk2)
            bot.register_next_step_handler(s3, unblocking)
        elif message.text=="Назад "+emoji["back"]:
            admin_menu(message)
    def blacklis(message):
        global chat_id
        chat_id=message.chat.id
        markup_ch=types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_ch.add('Заблокировать '+emoji["lo"], "Разблокировать "+emoji["unlo"], "Назад "+emoji["back"])
        s3=bot.send_message(chat_id,'Что Вы хотите сделать? ', reply_markup=markup_ch)
        bot.register_next_step_handler(s3, choosing)
    #Block user
    def blocking(message):
        #global blacklist
        global chat_id
        global back
        chat_id=message.chat.id
        if len(message.text)==9 and type(int(message.text))==int:
            fu=0
            block_id=int(message.text)
            telebot=mongo["telebot"]
            blacklist=telebot["Black List"]
            block_user={"User ID":block_id}
            blocked_users=blacklist.find({},{'User ID': 1,})
            for us in blocked_users:
                if us["User ID"]==block_user["User ID"]:
                    bot.send_message(chat_id,"Пользователь уже находится в блокировке "+emoji["redc"])
                    fu=1
                    admin_menu(message)
                    break
            if fu==0:
                res=blacklist.insert_one(block_user)
                admin_menu(message)
                bot.send_message(chat_id,"Пользователь был заблокирован "+emoji["redc"])
        elif message.text=="Назад "+emoji["back"]:
            blacklis(message)
    #Unblock user        
    def unblocking(message):
        global  chat_id
        chat_id=message.chat.id
        if len(message.text)==9 and type(int(message.text))==int:
            fu=0
            block_id=int(message.text)
            telebot=mongo["telebot"]
            blacklist=telebot["Black List"]
            unblock_user={"User ID":int(block_id)}
            blocked_users=blacklist.find({},{'User ID': 1,})
            for us in blocked_users:
                if us["User ID"]==unblock_user["User ID"]:
                    blacklist.delete_one(unblock_user)
                    bot.send_message(chat_id,"Пользователь был разблокирован")
                    admin_menu(message)
                    fu=1
                    break
            if fu==0:
                bot.send_message(chat_id,"Пользователь не был разблокирован")
                admin_menu(message)
        elif message.text=="Назад "+emoji["back"]:
            blacklis(message)
    #==Mailing==
    #Checking of right writing text to mail
    def checking(message):
        global chat_id
        global text_to_mail
        chat_id=message.chat.id
        if message.text=='Назад '+emoji['back']:
            admin_menu(message)
        else:
            text_to_mail=message.text
            bot.send_message(chat_id, f"Текст, который будет разослан, будет выглядеть так:\n (Имя), {text_to_mail}")
            s8=bot.send_message(chat_id, "Чтобы подтвердить рассылку введите - ПОДТВЕРДИТЬ")
            bot.register_next_step_handler(s8, mailing)
    #Mailing to Users
    def mailing(message):
        global chat_id
        global text_to_mail
        chat_id=message.chat.id
        if message.text=="ПОДТВЕРДИТЬ":
            telebot=mongo["telebot"]
            users=telebot["users"]
            reg_users = users.find({},{"Name":1,'User ID': 1, "Mailing": 1})
            for usr in reg_users:
                mail_id=usr["User ID"]
                name_usr=usr["Name"].title()
                if usr["Mailing"]==1:
                    bot.send_message(mail_id, f"{name_usr}, {text_to_mail}")
                else:
                    pass
            bot.send_message(chat_id, "Рассылка успешна!")
            admin_menu(message)
        if message.text=="ОТМЕНА":
            bot.send_message(chat_id,"Рассылка была отменена!")
            admin_menu(message)
    def mail(message):
        global chat_id
        chat_id=message.chat.id
        markup_cancel=types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_cancel.add("Назад "+emoji["back"])
        s7=bot.send_message(chat_id,'Введите текст для рассылки пользователям бота ', reply_markup=markup_cancel)
        bot.register_next_step_handler(s7, checking)
        
    #Checking on having admin by user
    def admin_msg(message):
        if message.text=='Заказы '+emoji["time"]:
            finding_orders(message)
        elif message.text=="Черный список "+emoji["lo"]:
            blacklis(message)
        elif message.text=="Рассылка "+emoji['mai']:
            mail(message)
        elif message.text=="Главное меню "+emoji["back"]:
            mu1(message)
        else:
            admin_menu(message)
    def admin_menu(message):
        global chat_id
        markup_admin=types.ReplyKeyboardMarkup(one_time_keyboard=True)
        #orders blacklist mail back
        markup_admin.add('Заказы '+emoji["time"], "Черный список "+emoji["lo"],"Рассылка "+emoji['mai'],"Главное меню "+emoji["back"])
        s8=bot.send_message(chat_id,'Выберите пункт меню:', reply_markup=markup_admin)
        bot.register_next_step_handler(s8, admin_msg)
    def admin_main(message):
        global chat_id
        chat_id=message.chat.id
        if message.text=="111":
            bot.send_message(chat_id, "Доступ предоставлен! Welcome!")
            admin_menu(message)
        elif message.text=="Назад "+emoji["back"]:
            mu1(message)
        elif message.text!="111":
            bot.send_message(chat_id, "Неверный ПИН-код! Повторите попытку!")
            mu1(message)
    def admin(message):
        global chat_id
        chat_id=message.chat.id
        if message.text=="111":
            bot.delete_message(chat_id, message.message_id)
            bot.delete_message(chat_id, message.message_id-1)
            bot.delete_message(chat_id, message.message_id-2)
            bot.delete_message(chat_id, message.message_id-3)
            bot.send_message(chat_id, "Доступ предоставлен! Welcome!")

            admin_menu(message)
        elif message.text=="Назад "+emoji["back"]:
            bot.delete_message(chat_id, message.message_id)
            bot.delete_message(chat_id, message.message_id-1)
            bot.delete_message(chat_id, message.message_id-2)
            bot.delete_message(chat_id, message.message_id-3)
            mu1(message)
        elif message.text!="111":
            bot.delete_message(chat_id, message.message_id)
            bot.delete_message(chat_id, message.message_id-1)
            bot.delete_message(chat_id, message.message_id-2)
            bot.delete_message(chat_id, message.message_id-3)
            bot.send_message(chat_id, "Неверный ПИН-код! Повторите попытку!!")
            mu1(message)
    def second(message):
        global chat_id
        global admin_list
        chat_id=message.chat.id
        #==Orders==
        def ordd(message):
            global chat_id
            chat_id=message.chat.id
            phone=0
            if message.text=="Назад "+emoji["back"]:
                mu1(message)
            else:
                user_order=message.text
                now=datetime.datetime.now()
                date=now.strftime("%d-%m-%Y %H:%M")
                print(user_order)
                telebot=mongo["telebot"]
                preorders=telebot["pre-orders"]
                users=telebot["users"]
                reg_users = users.find({},{'User ID': 1, "Phone":1})
                for k in reg_users:
                    if k['User ID']==chat_id:
                         phone=k['Phone']
                         break
                li_order={"User ID":chat_id,"UserName":message.from_user.first_name,'Phone':phone,"Pre-order":user_order, "Time":str(date), "Status":0}
                print(li_order)
                res=preorders.insert_one(li_order)
                bot.send_message(chat_id, "Спасибо! Администратор свяжется с Вами в течении 30 минут")
                mu1(message)
        #On and off mailing
        def on(message):
            global chat_id
            chat_id=message.chat.id
            if message.text=="/on":
                
                telebot=mongo["telebot"]
                users=telebot["users"]
                user_to_change={"User Name":message.from_user.first_name, "User ID":chat_id, "Mailing":0}
                new_user={"User Name":message.from_user.first_name, "User ID":chat_id, "Mailing":1}
                users.delete_one(user_to_change)
                res=users.insert_one(new_user)
                bot.send_message(chat_id, "Рассылка была успешно включена")
                mu1(message)
            elif message.text=="Назад "+emoji["back"] or message.text=="/start":
                mu1(message)
        def off(message):
            global chat_id
            chat_id=message.chat.id
            if message.text=="/off":
                
                telebot=mongo["telebot"]
                users=telebot["users"]
                user_to_change={"User Name":message.from_user.first_name, "User ID":chat_id, "Mailing":1}
                new_user={"User Name":message.from_user.first_name, "User ID":chat_id, "Mailing":0}
                users.delete_one(user_to_change)
                res=users.insert_one(new_user)
                bot.send_message(chat_id, "Рассылка была выключена")
                mu1(message)
            elif message.text=="Назад "+emoji["back"] or message.text=="/start":
                mu1(message)
        def sending(message):
            global chat_id
            chat_id=message.chat.id
            if message.text=="Назад "+emoji["back"]:
                mu1(message)
            else:
                telebot=mongo["telebot"]
                users=telebot["users"]
                reg_users = users.find({},{'User ID': 1, "Mailing":1})
                for usr in reg_users:
                    if usr["User ID"]==chat_id:
                        if usr["Mailing"]==0:
                            mu_back=types.ReplyKeyboardMarkup(one_time_keyboard=True)
                            mu_back.add("Назад "+emoji["back"])
                            sen=bot.send_message(chat_id, f'Наш бот использует рассылку для оповещения пользователей о скидках или ивентах.\nВ данный момент у Вас рассылка выключена {emoji["red"]}\nЕсли Вы хотите получать персональные скидки и акции введите "/on"', reply_markup=mu_back)       
                            bot.register_next_step_handler(sen, on)
                        elif usr["Mailing"]==1:
                            mu_back=types.ReplyKeyboardMarkup(one_time_keyboard=True)
                            mu_back.add("Назад "+emoji["back"])
                            sen=bot.send_message(chat_id, f'Наш бот использует рассылку для оповещения пользователей о скидках или ивентах.\nВ данный момент у Вас рассылка включена {emoji["green"]}\nЕсли Вы хотите отписатся от рассылки введите "/off"', reply_markup=mu_back)
                            bot.register_next_step_handler(sen, off)
        #==Back Functions==
        def back3(message):
            if message.text=="Назад "+emoji["back"]:
                mu1(message)
        def back4(message):
            if message.text=="Главное меню":
                mu1(message)
            elif message.text=="Где нас найти "+emoji["feet"]:
                markup_back2=types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup_back2.add("Назад "+emoji["back"])
                geo=f"[Открыть в Google Maps {emoji['maps']}](https://www.google.com/maps/d/u/0/edit?mid=1ow0NsL2XrFkeyzPZnCuyBRrg-far5an2&usp=sharing)"
                s=bot.send_message(message.chat.id, geo, parse_mode='Markdown', reply_markup=markup_back2)
                bot.register_next_step_handler(s, gr)
        def photos(message):
            global chat_id
            chat_id=message.chat.id
            if message.text=="Назад "+emoji["back"]:
                mu1(message)
            elif message.text=="Показать фото "+emoji["cam"]:
                markup_back2=types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup_back2.add("Главное меню")
                img1 = open(r"1.jpg", 'rb')
                img2 = open(r"2.jpg", 'rb')
                img3 = open(r"3.jpg", 'rb')
                bot.send_photo(chat_id, img1)
                bot.send_photo(chat_id, img2)
                s=bot.send_photo(chat_id, img3, reply_markup=markup_back2)
                bot.register_next_step_handler(s, back4)
            '''elif message.text=="Где нас найти "+emoji["feet"]:
                markup_back2=types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup_back2.add("Назад "+emoji["back"])
                geo=f"[Открыть в Google Maps {emoji['maps']}](https://www.google.com/maps/d/u/0/edit?mid=1ow0NsL2XrFkeyzPZnCuyBRrg-far5an2&usp=sharing)"
                s=bot.send_message(message.chat.id, geo, parse_mode='Markdown', reply_markup=markup_back2)
                bot.register_next_step_handler(s, gr)'''
        global feet
        global time
        global cam
        global rev
        global ab
        #Taking info from users
        if message.text=="Забронировать столик "+emoji["time"]:
            markup_back1=types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup_back1.add("Назад "+emoji["back"])
            send4=bot.send_message(chat_id, f'Для брони отправьте нам следующую информацию:\n-Дата \n-Время \n-Кол-во человек\nВ ближайшем времени мы Вам отправим информацию про возможность брони.', reply_markup=markup_back1)
            bot.register_next_step_handler(send4, ordd)
        elif message.text=="Меню "+emoji["book"]:
            global call_id
            global mesage_id
            global txt_menu
            markup_choose1=types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup_choose1.add("Текстовое меню", "Полное меню (pdf)","Назад "+emoji["back"])
            p=bot.send_message(chat_id, "Choose", reply_markup=markup_choose1)
            bot.register_next_step_handler(p, menu)
        elif message.text=="О ресторане "+emoji["ab"]:
            markup_about=types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup_about.add("Назад "+emoji["back"], "Показать фото "+emoji["cam"])
            se=bot.send_message(chat_id, 'Ресторан "Samara" вобрал в себя лучшие традиции европейской, испанской и средиземноморской кухни. Уютная, доброжелательная атмосфера и достойный сервис  - это основные преимущества ресторана. Все вышеперечисленное и плюс доступный уровень цен позволили заведению оказаться в списке лучших ресторанов  Киева. Секрет популярности прост - побывав здесь однажды и ощутив радушие и гостеприимство, теплый прием и заботливое обслуживание, гости непременно возвращаются вновь и рекомендуют  "Samara" своим друзьям.', reply_markup=markup_about)
            bot.register_next_step_handler(se,photos)
        elif message.text=='Где нас найти '+emoji["feet"]:
            #markup_back2=types.ReplyKeyboardMarkup(one_time_keyboard=True)
            #markup_back2.add("Назад "+emoji["back"])
            #geo=f"[Открыть в Google Maps {emoji['maps']}](https://www.google.com/maps/d/u/0/edit?mid=1ow0NsL2XrFkeyzPZnCuyBRrg-far5an2&usp=sharing)"
            bot.send_message(chat_id,f"[Открыть в Google Maps {emoji['maps']}](https://www.google.com/maps/d/u/0/edit?mid=1ow0NsL2XrFkeyzPZnCuyBRrg-far5an2&usp=sharing)")
            mu1(message)
            #s=bot.send_message(message.chat.id, geo, parse_mode='Markdown', reply_markup=markup_back2)
            #bot.register_next_step_handler(s, gr)
        elif message.text=="Отзывы "+emoji["rev"]:
            markup2=types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup2.add('Посмотреть статистику','Оставить отзыв '+emoji['rev'],'Назад '+emoji["back"])
            send2=bot.send_message(chat_id, 'Выберите то, что хотите сделать', reply_markup=markup2)
            bot.register_next_step_handler(send2,third)
        #Allowing admin using admin-panel to verify orders
        elif message.text=='/admin':
            for n in admin_list:
                if chat_id==n:
                    markup_back3=types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    markup_back3.add("Назад "+emoji["back"])
                    send6=bot.send_message(chat_id, "Введи ПИН",reply_markup=markup_back3)
                    bot.register_next_step_handler(send6,admin)
    def t1(message):
        chat_id=message.chat.id
        markup2=types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup2.add('0', '1','2','3','4', '5','Назад '+emoji["back"])
        send2=bot.send_message(chat_id, 'Оцените наш ресторан от 0 до 5, где 0 соответствует ответу "Ужасно", а 5 - ответу "Великолепно"', reply_markup=markup2)
        bot.register_next_step_handler(send2,t2)
    def t2(message):
        chat_id=message.chat.id
        def checker(message):
            global FOUNDED
            global ind
            global chat_id
            chat_id=message.chat.id
            FOUNDED=0
            telebot=mongo["telebot"]
            reviews=telebot["reviews"]
            user = reviews.find({},{"User ID":1,'Review': 1})
            for ind in user:
                if ind["User ID"] != chat_id:
                    FOUNDED=0
                elif ind["User ID"] == chat_id:
                    FOUNDED=1
                    break
        checker(message)
        #==Downloading review to DB==
        def rew_txt(message):
            global rew_text
            global GRADE
            global ind
            global chat_id
            chat_id=message.chat.id
            rew_text=message.text
            telebot=mongo["telebot"]
            reviews=telebot["reviews"]
            def test(message):
                global chat_id
                global GRADE
                chat_id=message.chat.id
                if FOUNDED==1:
                    reviews.delete_one(ind)
                    review={"User ID":chat_id,"Name":message.from_user.first_name,"Rating":GRADE,"Review":rew_text}
                    res=reviews.insert_one(review)
                    bot.send_message(chat_id, "Спасибо! Отзыв был обновлен. Мы постараемся быть лучше")
                elif FOUNDED==0:
                    review={"User ID":chat_id,"Name":message.from_user.first_name,"Rating":GRADE,"Review":rew_text}
                    res=reviews.insert_one(review)
                    bot.send_message(chat_id, "Спасибо за отзыв! Мы постараемся быть лучше!")
            test(message)
        def rat_num(message):
            global chat_id
            global GRADE
            chat_id=message.chat.id
            if message.text=='0':
                bot.send_message(chat_id, "Сожалеем что у Вас сложилось такое мнение. Подскажите, чего Вы поставили такую оценку")
                GRADE=0
                bot.register_next_step_handler(message, rew_txt)
            elif message.text=='1':
                bot.send_message(chat_id, "Сожалеем что у Вас сложилось такое мнение. Подскажите, чего Вы поставили такую оценку")
                GRADE=1
                bot.register_next_step_handler(message, rew_txt)
            elif message.text=='2':
                bot.send_message(chat_id, "Сожалеем что у Вас сложилось такое мнение. Подскажите, чего Вы поставили такую оценку")
                GRADE=2
                bot.register_next_step_handler(message, rew_txt)
            elif message.text=='3':
                bot.send_message(chat_id, "Не так уж и плохо! Расскажите, что помешало поставить более высокую оценку")
                GRADE=3
                bot.register_next_step_handler(message, rew_txt)
            elif message.text=='4':
                bot.send_message(chat_id, "Не так уж и плохо! Расскажите, что помешало поставить более высокую оценку")
                GRADE=4
                bot.register_next_step_handler(message,rew_txt)
            elif message.text=='5':
                bot.send_message(chat_id, "Спасибо за высокую оценку! Опишите пожалуйста Ваши впечатления после Вашего визита к нам")
                GRADE=5
                bot.register_next_step_handler(message, rew_txt)
            elif message.text=='Назад '+emoji["back"]:
                mu1(message)
        rat_num(message)
    #==Reviews==
    def main_stat(message):
        global chat_id
        chat_id=message.chat.id
        try:
            zero=0
            one=0
            two=0
            three=0
            four=0
            five=0
            telebot=mongo["telebot"]
            reviews=telebot["reviews"]
            users = reviews.find({},{'Rating': 1})
            for us in users:
                if int(us["Rating"])==0:
                    zero+=1
                elif int(us["Rating"])==1:
                    one+=1
                elif int(us["Rating"])==2:
                    two+=1
                elif int(us["Rating"])==3:
                    three+=1
                elif int(us["Rating"])==4:
                    four+=1
                elif int(us["Rating"])==5:
                    five+=1
            rates = ["0","1", "2", "3", "4", "5"]
            counts = [zero, one, two, three, four, five]
            c=sorted(counts)
            plt.bar(rates, counts, color="coral", width=0.52)
            for i, val in enumerate(counts):
                plt.text(i, val, float(val), horizontalalignment='center', verticalalignment='bottom', fontdict={'fontweight':500, 'size':12})
            plt.title("Number of reviews", fontsize=22)
            plt.title("Reviews!")
            plt.xlabel("Rate")
            plt.ylabel("Count")
            plt.ylim(0, c[len(c)-1]+1)
            try:    
                os.remove("graph.png")
            except FileNotFoundError:
                #mu_crash=types.ReplyKeyboardMarkup(one_time_keyboard=True)
                #mu_crash.add("Главное меню")
                bot.send_message(chat_id, "Too much requests!")
            def cr_img():
                plt.savefig('graph.png')
            cr_img()
            img = open(r"graph.png", 'rb')
            mu_bb=types.ReplyKeyboardMarkup(one_time_keyboard=True)
            mu_bb.add("Главное меню")
            p=bot.send_photo(chat_id, img, reply_markup=mu_bb)
            bot.register_next_step_handler(p, gr)
        except RuntimeError:
            mu_crash=types.ReplyKeyboardMarkup(one_time_keyboard=True)
            mu_crash.add("Главное меню")
            j=bot.send_message(chat_id, "Too much requests!", reply_markup=mu_crash)
            bot.register_next_step_handler(j, gr)
    def third(message):
        global FOUNDED
        global ind
        global GRADE
        global chat_id
        chat_id=message.chat.id
        #==Verification if there is a user wrote a review
        if message.text=="Оставить отзыв "+emoji["rev"]:
            t1(message)
        elif message.text=="Посмотреть статистику":
            #now=datetime.datetime.now()
            dt=datetime.datetime.today()
            #date=now.strftime("%H:%M")
            y=int(dt.year)
            m=int(dt.month)
            d=int(dt.day)
            date_today=f'{d+1}.{m}'
            if m==1 or m==3 or m==5 or m==7 or m==8 or m==10:
                if d==31:
                    date_today=f'01.0{m+1}'
            elif m==12:
                if d==31:
                    date_today=f'01.01'
            elif m==2:
                if d==28:
                    date_today=f'01.03'
            elif m==4 or m==6 or m==9 or m==11:
                if d==30:
                    date_today=f'01.{m+1}'
            else:
                date_today=f'{d+1}.{m}'
            ff=0
            telebot=mongo["telebot"]
            timegraph=telebot["time-graphic"]
            time_user={"User ID":chat_id,"Year":y,"Month":m, "Day":d}
            users_graph = timegraph.find({},{'User ID': 1,"Year":1,"Month":1, "Day":1})
            founded_user={"User ID":"","Month": "","Day":"","Year":""}
            for usr in users_graph:
                if usr["User ID"]==chat_id:
                    ff=1
                    founded_user["User ID"]=int(usr["User ID"])
                    founded_user["Month"]=int(usr["Month"])
                    founded_user["Day"]=int(usr["Day"])
                    founded_user["Year"]=int(usr["Year"])
                    break
            if ff==0:
                res=timegraph.insert_one(time_user)
                main_stat(message)
            elif ff==1:
                mu_back=types.ReplyKeyboardMarkup(one_time_keyboard=True)
                mu_back.add("Главное меню")
                if d>int(founded_user["Day"]):
                    if m>=int(founded_user["Month"]):
                        if y>=int(founded_user["Year"]):
                            main_stat(message)
                            timegraph.delete_one(founded_user)
                            res=timegraph.insert_one(time_user)
                        else:
                            s=bot.send_message(chat_id, f'Статистику можно получать раз в 24 часа. Следующий раз, когда Вы сможете ее посмотреть:{date_today}',reply_markup=mu_back)
                            bot.register_next_step_handler(s, gr)
                    elif m<int(founded_user["Month"]):
                        s=bot.send_message(chat_id, f'Статистику можно получать раз в 24 часа. Следующий раз, когда Вы сможете ее посмотреть:{date_today}',reply_markup=mu_back)
                        bot.register_next_step_handler(s, gr)
                elif d<=int(founded_user["Day"]):
                    if m>int(founded_user["Month"]):
                        timegraph.delete_one(founded_user)
                        res=timegraph.insert_one(time_user)
                        main_stat(message)
                    elif m<=int(founded_user["Month"]):
                        if y>int(founded_user["Year"]):
                            timegraph.delete_one(founded_user)
                            res=timegraph.insert_one(time_user)
                            main_stat(message)
                        else:
                            s=bot.send_message(chat_id, f'Статистику можно получать раз в 24 часа. Следующий раз, когда Вы сможете ее посмотреть:{date_today}',reply_markup=mu_back)
                            bot.register_next_step_handler(s, gr)
        elif message.text=="Назад "+emoji["back"]:
            mu1(message)
    first(message)
    
global call_id
global message

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global message
    global call_id
    global mesage_id
    global emoji
    chat_id=call.message.chat.id
    try:
        if call.data == 'menu1':
            keyboard = types.InlineKeyboardMarkup()
            callback_button1 = types.InlineKeyboardButton(text=emoji['tochka'], callback_data="m")
            callback_button2 = types.InlineKeyboardButton(text=emoji['tochka'], callback_data="m")
            callback_button3 = types.InlineKeyboardButton(text=emoji['right'], callback_data="menu2")
            keyboard.add(callback_button1,callback_button2,callback_button3)
            pr="="*15
            txt_menu=f"Яйца пашот со слабосолёным лососем на пшеничной булочке и голландским соусом, 360 г\n{pr}\nСкрембл с копчёным лососем-терияки и киноа, 310 г \n{pr}\nБоул с тигровой креветкой, авокадо и яйцом, 280 г \n{pr}\nЯйцо запечённое в авокадо с семенами микс и беби шпинатом, 200 г\n{pr}\nПерепелиные яйца на тосте из деревенского хлеба с сальсой изпечёных овощей и индейкой су-видс кунжутным соусом, 360 г\n{pr}\nШакшука со страчетеллой и хрустящим багетом, 430 г\n{pr}\nЯйца пашот на чёрном тосте с гуакамоле и копчёным лососем-терияки под сырным соусом, 360 г"
            msg = bot.edit_message_text(chat_id=call_id, message_id=mesage_id, text=txt_menu, parse_mode='Markdown', reply_markup=keyboard)
        elif call.data == 'menu2':
            keyboard = types.InlineKeyboardMarkup()
            callback_button1 = types.InlineKeyboardButton(text=emoji['left'], callback_data="menu1")
            callback_button2 = types.InlineKeyboardButton(text=emoji['tochka'], callback_data="m")
            callback_button3 = types.InlineKeyboardButton(text=emoji['right'], callback_data="menu3")
            keyboard.add(callback_button1,callback_button2, callback_button3)
            pr="="*15
            txt_menu=f'САЛАТ/ПЕРВЫЕ БЛЮДА НА ВЫБОР\n{pr}\nСалат из зелени и сезонных овощей, 180 г\n{pr}\nХолодный суп с курицей и овощами, 270 г\n{pr}\nХолодный суп со свеклой и грибами, 270 г\n{pr}\nМисо-суп с угрем и тофу, 200 г\n{pr}\nСуп Фо с телятиной, 300 г\n{pr}\nСуп овощной с риетом из тунца на белом тосте, 250/40 г'
            msg = bot.edit_message_text(chat_id=call_id, message_id=mesage_id, text=txt_menu, parse_mode='Markdown', reply_markup=keyboard)
        elif call.data == 'menu3':
            keyboard = types.InlineKeyboardMarkup()
            callback_button1 = types.InlineKeyboardButton(text=emoji['left'], callback_data="menu2")
            callback_button2 = types.InlineKeyboardButton(text=emoji['tochka'], callback_data="m")
            callback_button3 = types.InlineKeyboardButton(text=emoji['right'], callback_data="menu4")
            keyboard.add(callback_button1,callback_button2, callback_button3)
            pr="="*15
            txt_menu=f'ОСНОВНЫЕ БЛЮДА НА ВЫБОР\n{pr}\nРолл с морепродуктами в соусе креми-спайси и икройлетучей рыбы, 180 г\n{pr}\nТеплый ролл с лососем и авокадо, 160 г\n{pr}\nТамаго с угрем на подушке из капусты бок-чойи соусом цуме, 230 г\n{pr}\nСпагетти в сливочном соусе с морепродуктами, 270 г\n{pr}\nФишболы в сливочном соусе с припущенным шпинатом, 250 г\n{pr}\nПтитим с куриной печенью в соусе терияки, 250 г\n{pr}\nБифштекс с яйцом и картофельным пюре, 230 г'
            msg = bot.edit_message_text(chat_id=call_id, message_id=mesage_id, text=txt_menu, parse_mode='Markdown', reply_markup=keyboard)
        elif call.data == 'menu4':
            keyboard = types.InlineKeyboardMarkup()
            callback_button1 = types.InlineKeyboardButton(text=emoji['tochka'], callback_data="m")
            callback_button2 = types.InlineKeyboardButton(text=emoji['tochka'], callback_data="m")
            callback_button3 = types.InlineKeyboardButton(text=emoji['left'], callback_data="menu3")
            keyboard.add(callback_button3,callback_button2,callback_button1)
            pr="="*15
            txt_menu="4"
            msg = bot.edit_message_text(chat_id=call_id, message_id=mesage_id, text=txt_menu, parse_mode='Markdown', reply_markup=keyboard)

    except NameError or TypeError:
        bot.send_message(chat_id,'Issues with Telegram')
        print()


# ==Launching the bot==
if __name__ == '__main__':
    try:
        print('Telegram Bot is starting')
        bot.polling(none_stop=True)
        '''t = threading.Thread(target=cr_img)
        t.start()'''
        
    except exceptions.ConnectionError as e:
        print('Network Issues with Telegram')
