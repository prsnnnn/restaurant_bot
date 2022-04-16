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
        markup1=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
        #markup1.add(emoji["time"]+' Забронировать столик',emoji["book"]+' Меню',emoji["ab"]+' О ресторане', emoji["feet"]+' Где нас найти',emoji["rev"]+' Отзывы',emoji['quest']+" Задать вопрос")
        markup1.add(emoji["time"]+' Забронювати столик',emoji["book"]+' Меню',emoji["ab"]+' Про ресторан', emoji["feet"]+' Де нас знайти?',emoji["rev"]+' Відгуки',emoji['quest']+" Задати питання")        
        send3=bot.send_message(chat_id, "Оберіть пункт меню:", reply_markup=markup1)
        bot.register_next_step_handler(send3,second)
        print(str(message.chat.id)+ str(user_name))
    def logg(message):
        global chat_id
        global NEW_USER
        global TO_FOUND
        chat_id=message.chat.id
        if message.text=='Авторизуватись':
            NEW_USER={"User ID":chat_id,"Name":"","Phone":"", "Password":"", "Mailing":0}
            s=bot.send_message(chat_id, "Введіте ваше ім'я")
            bot.register_next_step_handler(s,name)
        elif message.text=='Увійти':
            phlog(message)
    def phlog(message):
        global chat_id
        global TO_FOUND
        chat_id=message.chat.id
        marku=types.ReplyKeyboardMarkup(one_time_keyboard=True,request_contact=True,resize_keyboard=True)
        marku.add('Поделится номером')
        s=bot.send_message(chat_id,'Введіть Ваш номер телефону (380xxxxxxx)',reply_markup=marku)
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
                            k=bot.send_message(chat_id, "Введіть пароль")
                            bot.register_next_step_handler(k,passlog)
                            break
                        else:
                            fr=0
            except ValueError:
                print('sss')
            else:
                bot.send_message(chat_id, "Невірний номер телефону!")
                phlog(message)
        else:
            bot.send_message(chat_id, "Невірний номер телефону!")
            phlog(message)
        if fr==1:
            passlog(message)
        else:
            bot.send_message(chat_id, "Користувача не знайдено!")
            phlog(message)
    def passlog(message):
        global chat_id
        global FOUNDED
        chat_id=message.chat.id
        if str(message.text)==str(FOUNDED):
            bot.send_message(chat_id, "Ласкаво просимо!")
        else:
            bot.send_message(chat_id,'neverno')
    def name(message):
        global chat_id
        global NEW_USER
        chat_id=message.chat.id
        NEW_USER['Name']=message.text
        bphone = types.KeyboardButton(text="Поділиться номером телефону", request_contact=True)
        marku=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
        marku.add(bphone)
        s=bot.send_message(chat_id, 'Залиште, будь ласка, Ваш номер телефону:', reply_markup=marku)
        bot.register_next_step_handler(s,phone)
    def phone(message):
        global chat_id
        global NEW_USER
        chat_id=message.chat.id
        NEW_USER['Phone']=message.contact.phone_number
        s=bot.send_message(chat_id, 'Введіть пароль (мін. 6 символів)')
        bot.register_next_step_handler(s,password)
    def password(message):
        global chat_id
        global NEW_USER
        chat_id=message.chat.id
        if len(message.text)>5:
            NEW_USER['Password']=message.text
            telebot=mongo["telebot"]
            users=telebot["users"]
            res=users.insert_one(NEW_USER)
            bot.send_message(chat_id, "Авторизація успішна "+emoji['yep'])
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
                bot.send_message(chat_id, "Ви були заблоковані адміністратором у зв'язку з порушенням правил користування ботом")
                bl=1
                break
        if bl==0:
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
                global hello_text
                timen = time.localtime()
                hr = int(time.strftime("%H", timen))
                hello_text=''
                if hr>=0 and hr<=5:
                    hello_text=f"Доброї ночі {emoji['moon']}, {user_name}, я чат-бот найкращого ресторану "+emoji["robot"]
                elif hr>=22 and hr<=24:
                    hello_text=f"Доброї ночі {emoji['moon']}, {user_name}, я чат-бот найкращого ресторану "+emoji["robot"]
                elif hr>=6 and hr<=11:
                    hello_text=f"Добрий ранок {emoji['sun']}, {user_name}, я чат-бот найкращого ресторану "+emoji["robot"]
                elif hr>=12 and hr<=18:
                    hello_text=f"Доброго дня {emoji['city']}, {user_name}, я чат-бот найкращого ресторану "+emoji["robot"]
                elif hr>=19 and hr<=21:
                    hello_text=f"Доброго вечора {emoji['evn']}, {user_name}, я чат-бот найкращого ресторану "+emoji["robot"]
                send=bot.send_message(chat_id, hello_text)
                markup=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
                markup.add('Авторизуватись')
                send1=bot.send_message(chat_id, f"Перед початком використання бота необхідно пройти авторизацію\n", reply_markup=markup)
                bot.register_next_step_handler(send1, logg)
            elif f==1:
                mu1(message)
        #mu1(message)

    def gr(message):
        global message_id
        if message.text=="Главное меню" or message.text==emoji["back"]+" Назад":
            bot.delete_message(chat_id, message_id)
            mu1(message)
            
    def menu(message):
        global call_id
        global message_id
        chat_id=message.chat.id
        if message.text==emoji["back"]+" Назад":
            mu1(message)
        elif message.text=="Текстове меню":
            markup_backk1=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
            markup_backk1.add(emoji["back"]+" Назад")
            keyboard = types.InlineKeyboardMarkup()
            callback_button1 = types.InlineKeyboardButton(text=emoji["tochka"], callback_data="1")
            callback_button2 = types.InlineKeyboardButton(text=emoji["tochka"], callback_data="1")
            callback_button3 = types.InlineKeyboardButton(text=emoji["right"], callback_data="menu2")
            keyboard.add(callback_button1,callback_button2,callback_button3)
            pr="="*15
            img1 = open(r"1.png", 'rb')
            msg = bot.send_photo(chat_id=message.chat.id,photo=img1, parse_mode='Markdown', reply_markup=keyboard)
            call_id=int(message.chat.id)
            message_id=int(msg.message_id)
            bot.register_next_step_handler(msg, gr)
        elif message.text=="Завантажити (pdf)":
            mu_back=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
            mu_back.add(emoji["back"]+" Назад")
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
        order = preorders.find({},{"User ID":1,'Name':1,'Phone':1,"Persons":1,'Comment': 1, "Time":1, "Status":1})
        markup_ap=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
        markup_ap.add(emoji["yep"]+' Підтвердити',emoji['redc']+" Відхилити", emoji["back"]+" Назад")
        order_li=list(order)
        print(order_li)
        def backm(message):
            if message.text==emoji["back"]+" Назад":
                mu1(message)
        try:
            if len(order_li)==1:
                bot.send_message(chat_id, f"У вас 1 нове замовлення")
            elif len(order_li)>0 and len(order_li)!=1:
                bot.send_message(chat_id, f"У вас {len(order_li)} нових замовлень")
            link=f"[{order_li[0]['Name']}](tg://user?id={order_li[0]['User ID']})"
            #bot.send_message(chat_id,link, parse_mode='Markdown')
            #link="["+str(order_li[0]['UserName'])+"](tg://user?id="+str(order_li[0]['User ID'])+")"
            ord_txt=f'User ID: {order_li[0]["User ID"]}\nUser: {link}\nPhone: {order_li[0]["Phone"]}\nTime: {order_li[0]["Time"]}\nPersons: {order_li[0]["Persons"]}\nComment: {order_li[0]["Comment"]}'
            s=bot.send_message(chat_id, ord_txt, reply_markup=markup_ap,parse_mode='Markdown')
            bot.register_next_step_handler(s, approving)
        except IndexError:
            b=bot.send_message(chat_id, "Замовлень немає!")
            admin_menu(message)
    def approving(message):
        global chat_id
        global order
        global order_li
        chat_id=message.chat.id
        if message.text==emoji["yep"]+" Підтвердити":
            telebot=mongo["telebot"]
            completed_orders=telebot["completed orders"]
            preorders=telebot["pre-orders"]
            completed_order={"User ID":order_li[0]["User ID"],'Time': order_li[0]["Time"], "Persons":order_li[0]["Persons"],"Comment":order_li[0]["Comment"],"Status":1}
            delet={"User ID":order_li[0]["User ID"],'Time': order_li[0]["Time"], "Persons":order_li[0]["Persons"],"Comment":order_li[0]['Comment'],"Status":0}
            preorders.delete_one(delet)
            res=completed_orders.insert_one(completed_order)
            bot.send_message(chat_id, "Замовлення підтверждено")
            bot.send_message(completed_order['User ID'], f"{emoji['rocket']} Ваше замовлення підтверждено. \nОчікуємо на Вас у ресторані {emoji['star']}")
            finding_orders(message)
        elif message.text==emoji['redc']+" Відхилити":
            telebot=mongo["telebot"]
            completed_orders=telebot["completed orders"]
            preorders=telebot["pre-orders"]
            completed_order={"User ID":order_li[0]["User ID"],'Time': order_li[0]["Time"], "Persons":order_li[0]["Persons"],"Comment":order_li[0]["Comment"] ,"Status":0}
            delet={"User ID":order_li[0]["User ID"],'Time': order_li[0]["Time"], "Persons":order_li[0]["Persons"],"Comment":order_li[0]['Comment'],"Status":0}
            preorders.delete_one(delet)
            res=completed_orders.insert_one(completed_order)
            bot.send_message(chat_id, "Замовлення відхилено")
            bot.send_message(completed_order['User ID'], f"Ваше  замовлення відхилено :(\nМожливо, Ви надали хибну інформацію або порушили правила нашого ресторану")
            finding_orders(message)
        elif message.text==emoji['back']+" Назад":
            admin_menu(message)
    #==BLACKLIST==
    def choosing(message):
        global chat_id
        chat_id=message.chat.id
        if message.text==emoji["lo"]+" Заблокувати":
            mu_backk1=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
            mu_backk1.add(emoji['back']+" Назад")
            s3=bot.send_message(chat_id,'Введіть "User ID" чтобы заблокувати користувача', reply_markup=mu_backk1)
            bot.register_next_step_handler(s3, blocking)
        elif message.text==emoji["unlo"]+" Розблокувати":
            mu_backk2=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
            mu_backk2.add(emoji['back']+" Назад")
            s3=bot.send_message(chat_id,'Введіть "User ID" щоб розблокувати користувача', reply_markup=mu_backk2)
            bot.register_next_step_handler(s3, unblocking)
        elif message.text==emoji["back"]+" Назад":
            admin_menu(message)
    def blacklis(message):
        global chat_id
        chat_id=message.chat.id
        markup_ch=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
        markup_ch.add(emoji["lo"]+' Заблокувати', emoji["unlo"]+" Розблокувати", emoji["back"]+" Назад")
        s3=bot.send_message(chat_id,'Що ви хочете зробити? ', reply_markup=markup_ch)
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
                    bot.send_message(chat_id,"Користувач вже перебуває у блокуванні "+emoji["redc"])
                    fu=1
                    admin_menu(message)
                    break
            if fu==0:
                res=blacklist.insert_one(block_user)
                admin_menu(message)
                bot.send_message(chat_id,"Користувач був заблокований "+emoji["redc"])
        elif message.text==emoji["back"]+" Назад":
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
                    bot.send_message(chat_id,"Користувач був розблокований")
                    admin_menu(message)
                    fu=1
                    break
            if fu==0:
                bot.send_message(chat_id,"Користувач не був розблокований")
                admin_menu(message)
        elif message.text==emoji["back"]+" Назад":
            blacklis(message)
    #==Mailing==
    #Checking of right writing text to mail
    def checking(message):
        global chat_id
        global text_to_mail
        chat_id=message.chat.id
        if message.text==emoji["back"]+' Назад':
            admin_menu(message)
        else:
            text_to_mail=message.text
            bot.send_message(chat_id, f"Текст, який буде розісланий, виглядатиме так:\n (Имя), {text_to_mail}")
            s8=bot.send_message(chat_id, "Щоб підтвердити розсилку, введіть - ПІДТВЕРДИТИ")
            bot.register_next_step_handler(s8, mailing)
    #Mailing to Users
    def mailing(message):
        global chat_id
        global text_to_mail
        chat_id=message.chat.id
        if message.text=="ПІДТВЕРДИТИ":
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
            bot.send_message(chat_id, "Розсилання успішне!")
            admin_menu(message)
        if message.text=="ОТМЕНА":
            bot.send_message(chat_id,"Розсилання было скасовано!")
            admin_menu(message)
    def mail(message):
        global chat_id
        chat_id=message.chat.id
        markup_cancel=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
        markup_cancel.add(emoji["back"]+" Назад")
        s7=bot.send_message(chat_id,'Введіть текст для розсилки користувачам ', reply_markup=markup_cancel)
        bot.register_next_step_handler(s7, checking)
    def quest_answer(message):
        global q_li
        chat_id=message.chat.id
        telebot=mongo["telebot"]
        questions=telebot["questions"]
        question = questions.find({},{"User ID":1,'UserName':1,'Phone':1,'Question': 1, "Time":1, "Status":1})
        markup_ap=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
        markup_ap.add(emoji["back"]+" Назад", emoji['redc']+" Відхилити")
        q_li=list(question)
        print(q_li)
        def backm(message):
            if message.text==emoji["back"]+" Назад":
                mu1(message)
        try:
            if len(q_li)==1:
                bot.send_message(chat_id, f"У вас 1 нове запитання")
            elif len(q_li)>0 and len(q_li)!=1:
                bot.send_message(chat_id, f"У вас {len(q_li)} нових запитань")
            link=f"[{q_li[0]['UserName']}](tg://user?id={q_li[0]['User ID']})"
            q_txt=f'User ID: {q_li[0]["User ID"]}\nUser: {link}\nPhone: {q_li[0]["Phone"]}\nQuestion: {q_li[0]["Question"]}'
            s=bot.send_message(chat_id, q_txt, reply_markup=markup_ap,parse_mode='Markdown')
            bot.register_next_step_handler(s, quest_approving)
        except IndexError:
            b=bot.send_message(chat_id, "Запитань немає!")
            admin_menu(message)
    def quest_approving(message):
        global question
        global q_li
        chat_id=message.chat.id
        if message.text==emoji['redc']+" Відхилити":
            bot.send_message(q_li[0]["User ID"], f"Ваше звернення {q_li[0]['Time']}\nВідхилено адміністратором")
            bot.send_message(chat_id, "Питання відхилено")
            delet={"User ID":q_li[0]["User ID"],'Question': q_li[0]["Question"], "Time":q_li[0]["Time"], "Status":0}
            telebot=mongo["telebot"]
            questions=telebot["questions"]
            questions.delete_one(delet) 
            quest_answer(message)
        elif message.text==emoji["back"]+" Назад":
            admin_menu(message)
        else:
            anstxt=message.text
            telebot=mongo["telebot"]
            completed_q=telebot["completed questions"]
            questions=telebot["questions"]
            completed_question={"User ID":q_li[0]["User ID"],'Question': q_li[0]["Question"], "Time":q_li[0]["Time"], "Status":1}
            delet={"User ID":q_li[0]["User ID"],'Question': q_li[0]["Question"], "Time":q_li[0]["Time"], "Status":0}
            questions.delete_one(delet)
            res=completed_q.insert_one(completed_question)
            bot.send_message(chat_id, "Питання вирішено")
            bot.send_message(completed_question['User ID'], f"Ваше звернення {q_li[0]['Time']}\n{anstxt}")
            quest_answer(message)
    #Checking on having admin by user
    def admin_msg(message):
        if message.text==emoji["time"]+' Замовлення':
            finding_orders(message)
        elif message.text==emoji['quest']+' Запитання':
            quest_answer(message)
        elif message.text==emoji["lo"]+" Чорний список":
            blacklis(message)
        elif message.text==emoji['mai']+" Розсилання":
            mail(message)
        elif message.text==emoji["back"]+" Головне меню":
            mu1(message)
        else:
            admin_menu(message)
    def admin_menu(message):
        global chat_id
        markup_admin=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
        #orders blacklist mail back
        #markup_admin.add(emoji["time"]+' Заказы',emoji['quest']+' Вопросы', emoji["lo"]+" Черный список",emoji['mai']+" Рассылка",emoji["back"]+" Главное меню")
        markup_admin.add(emoji["time"]+' Замовлення',emoji['quest']+' Запитання', emoji["lo"]+" Чорний список",emoji['mai']+" Розсилання",emoji["back"]+" Головне меню")
        s8=bot.send_message(chat_id,'Оберіть пункт меню:', reply_markup=markup_admin)
        bot.register_next_step_handler(s8, admin_msg)
    def admin_main(message):
        global chat_id
        chat_id=message.chat.id
        if message.text=="111":
            bot.send_message(chat_id, "Доступ надано! Ласкаво просимо!")
            admin_menu(message)
        elif message.text==emoji["back"]+" Назад":
            mu1(message)
        elif message.text!="111":
            bot.send_message(chat_id, "Невірный ПІН-код! Повторіть спробу!")
            mu1(message)
    def admin(message):
        global chat_id
        chat_id=message.chat.id
        if message.text=="111":
            bot.delete_message(chat_id, message.message_id)
            bot.delete_message(chat_id, message.message_id-1)
            bot.delete_message(chat_id, message.message_id-2)
            bot.delete_message(chat_id, message.message_id-3)
            bot.send_message(chat_id, "Доступ надано! Ласкаво просимо!")
            admin_menu(message)
        elif message.text==emoji["back"]+" Назад":
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
            bot.send_message(chat_id, "Невірный ПІН-код! Повторіть спробу!")
            mu1(message)
    def second(message):
        global chat_id
        global admin_list
        chat_id=message.chat.id
        #==Orders==
        def ordd(message):
            global chat_id
            global tme
            chat_id=message.chat.id
            #phone=0
            tme=message.text
            spl_time=list(tme)
            if message.text==emoji["back"]+" Назад":
                mu1(message)
            elif spl_time[2]==":":
                time1=int(spl_time[0]+spl_time[1])
                time2=int(spl_time[3]+spl_time[4])
                if time1>=10 and time1<=22:
                    if str(time2)=='0' or str(time2)=='30':
                        mu_prs=types.ReplyKeyboardMarkup(one_time_keyboard=True,row_width=6,resize_keyboard=True)
                        mu_prs.add('1','2','3','4','5','6',emoji["back"]+" Головне меню")
                        s=bot.send_message(chat_id, "Укажіте кількість персон:", reply_markup=mu_prs)
                        bot.register_next_step_handler(s, prsns)
        def prsns(message):
            global chat_id
            global prs_count
            chat_id=message.chat.id
            if message.text==emoji["back"]+" Головне меню":
                mu1(message)
            else:
                prs_count=int(message.text)
                if prs_count>=1 and prs_count<=6:
                    mu_comm=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
                    mu_comm.add('Пропустити',emoji["back"]+" Головне меню")
                    s=bot.send_message(chat_id, "При потребі вкажіть коментар:", reply_markup=mu_comm)
                    bot.register_next_step_handler(s, comment)
                else:
                    ordd(message)
        def comment(message):
            global chat_id
            global tme
            global prs_count
            chat_id=message.chat.id
            user_comment=''
            if message.text=='Пропустити':
                user_comment=' '
                now=datetime.datetime.now()
                date=now.strftime("%d-%m-%Y %H:%M")
                telebot=mongo["telebot"]
                preorders=telebot["pre-orders"]
                users=telebot["users"]
                reg_users = users.find({},{'User ID': 1, 'Name':1,"Phone":1})
                for k in reg_users:
                    if k['User ID']==chat_id:
                        name=k['Name']
                        phone=k['Phone']
                        break
                li_order={"User ID":chat_id,"Name":name,'Phone':phone,"Time":tme,'Persons':prs_count,"Comment":user_comment, "Status":0}
                print(li_order)
                res=preorders.insert_one(li_order)
                bot.send_message(chat_id, "Дякуємо! Адміністратор зв'яжеться з Вами протягом 30 хвилин")
                mu1(message)
            elif message.text==emoji["back"]+" Главное меню":
                mu1(message)
            else:
                user_comment=message.text
                now=datetime.datetime.now()
                date=now.strftime("%d-%m-%Y %H:%M")
                telebot=mongo["telebot"]
                preorders=telebot["pre-orders"]
                users=telebot["users"]
                reg_users = users.find({},{'User ID': 1, 'Name':1,"Phone":1})
                for k in reg_users:
                    if k['User ID']==chat_id:
                        name=k['Name']
                        phone=k['Phone']
                        break
                li_order={"User ID":chat_id,"Name":name,'Phone':phone,"Time":tme,'Persons':prs_count,"Comment":user_comment, "Status":0}
                print(li_order)
                res=preorders.insert_one(li_order)
                bot.send_message(chat_id, "Дякуємо! Адміністратор зв'яжеться з Вами протягом 30 хвилин")
                mu1(message)
            
        #==Back Functions==
        def back3(message):
            if message.text==emoji["back"]+" Назад":
                mu1(message)
        def back4(message):
            if message.text=="Головне меню":
                mu1(message)
            elif message.text==emoji["feet"]+' Де нас знайти?':
                markup_back2=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
                markup_back2.add(emoji["back"]+" Назад")
                geo=f"[Відкрити в Google Maps {emoji['maps']}](https://www.google.com/maps/d/u/0/edit?mid=1ow0NsL2XrFkeyzPZnCuyBRrg-far5an2&usp=sharing)"
                s=bot.send_message(message.chat.id, geo, parse_mode='Markdown', reply_markup=markup_back2)
                bot.register_next_step_handler(s, gr)
        def photos(message):
            global chat_id
            chat_id=message.chat.id
            if message.text==emoji["back"]+" Назад":
                mu1(message)
            elif message.text==emoji["sofa"]+" Інтер'єр":
                markup_back2=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
                markup_back2.add("Головне меню")
                img1 = open(r"1.jpg", 'rb')
                img2 = open(r"2.jpg", 'rb')
                img3 = open(r"3.jpg", 'rb')
                bot.send_photo(chat_id, img1)
                bot.send_photo(chat_id, img2)
                s=bot.send_photo(chat_id, img3, reply_markup=markup_back2)
                bot.register_next_step_handler(s, back4)
        def question(message):
            chat_id=message.chat.id
            if message.text==emoji["back"]+" Назад":
                mu1(message)
            else:
                qtext=message.text
                telebot=mongo["telebot"]
                questions=telebot["questions"]
                users=telebot["users"]
                reg_users = users.find({},{'User ID': 1,"Name":1, "Phone":1})
                for k in reg_users:
                    if k['User ID']==chat_id:
                         name=k['Name']
                         phone=k['Phone']
                         break
                now=datetime.datetime.now()
                date=now.strftime("%d-%m-%Y %H:%M")
                li_q={"User ID":chat_id,"UserName":name,'Phone':"+"+phone,"Question":qtext, "Time":str(date), "Status":0}
                print(li_q)
                res=questions.insert_one(li_q)
                bot.send_message(chat_id, "Дякуємо за питання! Ви отримаєте відповідь протягом 30 минут")
                mu1(message)
        #Taking info from users
        if message.text==emoji["time"]+' Забронювати столик':
            markup_back1=types.ReplyKeyboardMarkup(one_time_keyboard=True,row_width=2,resize_keyboard=True)
            markup_back1.add('10:00','10:30','11:00','11:30','12:00','12:30','13:00','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00','19:30','20:00','20:30','21:00','21:30','22:00',emoji["back"]+" Назад")
            #send4=bot.send_message(chat_id, f'Для брони отправьте нам следующую информацию:\n-Дата \n-Время \n-Кол-во человек\nВ ближайшем времени мы Вам отправим информацию про возможность брони.', reply_markup=markup_back1)
            send4=bot.send_message(chat_id, f'Оберіть час', reply_markup=markup_back1)
            bot.register_next_step_handler(send4, ordd)
        elif message.text==emoji["book"]+" Меню":
            global call_id
            global message_id
            global txt_menu
            markup_choose1=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
            markup_choose1.add("Завантажити (pdf)",emoji["back"]+" Назад")
            keyboard = types.InlineKeyboardMarkup()
            p=bot.send_message(chat_id, "Меню:", reply_markup=markup_choose1)
            callback_button1 = types.InlineKeyboardButton(text=emoji["tochka"], callback_data="1")
            callback_button2 = types.InlineKeyboardButton(text=emoji["tochka"], callback_data="1")
            callback_button3 = types.InlineKeyboardButton(text=emoji["right"], callback_data="menu2")
            keyboard.add(callback_button1,callback_button2,callback_button3)
            pr="="*15
            img1 = open(r"1.png", 'rb')
            msg = bot.send_photo(chat_id=message.chat.id,photo=img1, parse_mode='Markdown', reply_markup=keyboard)
            call_id=int(message.chat.id)
            message_id=int(msg.message_id)
            #bot.register_next_step_handler(msg, gr)
            #markup_choose1.add("Текстовое меню", "Полное меню (pdf)",emoji["back"]+" Назад")
            bot.register_next_step_handler(p, menu)
        elif message.text==emoji["ab"]+" Про ресторан":
            markup_about=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
            markup_about.add(emoji["back"]+" Назад", emoji["sofa"]+" Інтер'єр")
            #se=bot.send_message(chat_id, 'Ресторан "Samara" вобрал в себя лучшие традиции европейской, испанской и средиземноморской кухни. Уютная, доброжелательная атмосфера и достойный сервис  - это основные преимущества ресторана. Все вышеперечисленное и плюс доступный уровень цен позволили заведению оказаться в списке лучших ресторанов  Киева. Секрет популярности прост - побывав здесь однажды и ощутив радушие и гостеприимство, теплый прием и заботливое обслуживание, гости непременно возвращаются вновь и рекомендуют  "Samara" своим друзьям.', reply_markup=markup_about)
            se=bot.send_message(chat_id,f"▫️MAN - це новий ресторан зі змішаною кухнею!\n\nРесторан увібрав у себе найкращі традиції європейської, іспанської та середземноморської кухні. Затишна, доброзичлива атмосфера та гідний сервіс - це основні переваги ресторану.\n\nСекрет популярності простий - побувавши тут одного разу і відчувши привітність та гостинність, теплий прийом та дбайливе обслуговування, гості неодмінно повертаються знову та рекомендують MAN своїм друзям.\n\n{emoji['house']} м. Дніпро, пр. Гагаріна 26, свічка Г\n{emoji['phone']} +38 (067) 067-06-70\n{emoji['clock']} 10:00 - 00:00\n{emoji['net']} https://dvman.dnepredu.com/uk/", reply_markup=markup_about)
            bot.register_next_step_handler(se,photos)
        elif message.text==emoji["feet"]+' Де нас знайти?':
            bot.send_message(chat_id, text="<a href='https://www.google.com/maps/d/u/0/edit?mid=1ow0NsL2XrFkeyzPZnCuyBRrg-far5an2&usp=sharing'>Открыть в Google Maps </a>"+f"{emoji['maps']}", parse_mode='HTML')
            mu1(message)
        elif message.text==emoji["rev"]+" Відгуки":
            markup2=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
            markup2.add('Переглянути статистику',emoji['rev']+' Залишити відгук',emoji["back"]+' Назад')
            send2=bot.send_message(chat_id, 'Оберіть, що хочете зробити', reply_markup=markup2)
            bot.register_next_step_handler(send2,third)
        elif message.text==emoji['quest']+' Задати питання':
            mark=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
            mark.add(emoji["back"]+' Назад')
            sen=bot.send_message(chat_id, 'Напишіть Ваше запитання: ', reply_markup=mark)
            bot.register_next_step_handler(sen,question)
        #Allowing admin using admin-panel to verify orders
        elif message.text=='/admin':
            for n in admin_list:
                if chat_id==n:
                    markup_back3=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
                    markup_back3.add(emoji["back"]+" Назад")
                    send6=bot.send_message(chat_id, "Введіть ПІН",reply_markup=markup_back3)
                    bot.register_next_step_handler(send6,admin)
    def t1(message):
        chat_id=message.chat.id
        markup2=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
        markup2.add('0', '1','2','3','4', '5',emoji["back"]+' Назад')
        send2=bot.send_message(chat_id, 'Оцініть наш ресторан від 0 до 5, де 0 відповідає відповіді "Жахливо", а 5 - відповіді "Чудово"', reply_markup=markup2)
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
                    bot.send_message(chat_id, "Дякуємо! Відгук було оновлено")
                    mu1(message)
                elif FOUNDED==0:
                    review={"User ID":chat_id,"Name":message.from_user.first_name,"Rating":GRADE,"Review":rew_text}
                    res=reviews.insert_one(review)
                    bot.send_message(chat_id, "Дякуємо за відгук!")
                    mu1(message)
            test(message)
        def rat_num(message):
            global chat_id
            global GRADE
            chat_id=message.chat.id
            if message.text=='0':
                bot.send_message(chat_id, "Жаль, що у Вас склалася така думка. Підкажіть, чого Ви поставили таку оцінку")
                GRADE=0
                bot.register_next_step_handler(message, rew_txt)
            elif message.text=='1':
                bot.send_message(chat_id, "Жаль, що у Вас склалася така думка. Підкажіть, чого Ви поставили таку оцінку")
                GRADE=1
                bot.register_next_step_handler(message, rew_txt)
            elif message.text=='2':
                bot.send_message(chat_id, "Жаль, що у Вас склалася така думка. Підкажіть, чого Ви поставили таку оцінку")
                GRADE=2
                bot.register_next_step_handler(message, rew_txt)
            elif message.text=='3':
                bot.send_message(chat_id, "Не так уже й погано! Розкажіть, що завадило поставити більш високу оцінку")
                GRADE=3
                bot.register_next_step_handler(message, rew_txt)
            elif message.text=='4':
                bot.send_message(chat_id, "Не так уже й погано! Розкажіть, що завадило поставити більш високу оцінку")
                GRADE=4
                bot.register_next_step_handler(message,rew_txt)
            elif message.text=='5':
                bot.send_message(chat_id, "Дякую за високу оцінку! Опишіть, будь ласка, Ваші враження після Вашого візиту до нас")
                GRADE=5
                bot.register_next_step_handler(message, rew_txt)
            elif message.text==emoji["back"]+' Назад':
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
            mu_bb=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
            mu_bb.add("Головне меню")
            p=bot.send_photo(chat_id, img, reply_markup=mu_bb)
            bot.register_next_step_handler(p, back5)
        except RuntimeError:
            mu_crash=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
            mu_crash.add("Головне меню")
            j=bot.send_message(chat_id, "Too much requests!", reply_markup=mu_crash)
            bot.register_next_step_handler(j, back5)
    def back5(message):
        if message.text=='Головне меню':
            mu1(message)
    def third(message):
        global FOUNDED
        global ind
        global GRADE
        global chat_id
        chat_id=message.chat.id
        #==Verification if there is a user wrote a review
        if message.text==emoji["rev"]+" Залишити відгук":
            t1(message)
        elif message.text=="Переглянути статистику":
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
                mu_back=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
                mu_back.add("Головне меню")
                if d>int(founded_user["Day"]):
                    if m>=int(founded_user["Month"]):
                        if y>=int(founded_user["Year"]):
                            main_stat(message)
                            timegraph.delete_one(founded_user)
                            res=timegraph.insert_one(time_user)
                        else:
                            s=bot.send_message(chat_id, f'Статистику можна отримувати раз на 24 години. Наступного разу, коли Ви зможете її подивитись:{date_today}',reply_markup=mu_back)
                            bot.register_next_step_handler(s, back5)
                    elif m<int(founded_user["Month"]):
                        s=bot.send_message(chat_id, f'Статистику можна отримувати раз на 24 години. Наступного разу, коли Ви зможете її подивитись:{date_today}',reply_markup=mu_back)
                        bot.register_next_step_handler(s, back5)
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
                            s=bot.send_message(chat_id, f'Статистику можна отримувати раз на 24 години. Наступного разу, коли Ви зможете її подивитись:{date_today}',reply_markup=mu_back)
                            bot.register_next_step_handler(s, back5)
        elif message.text==emoji["back"]+" Назад":
            mu1(message)
    first(message)
    
global call_id
global message

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global message
    global call_id
    global message_id
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
            img1 = open(r"1.png", 'rb')
            bot.delete_message(chat_id, message_id)
            msg = bot.send_photo(chat_id=call_id,photo=img1, parse_mode='Markdown', reply_markup=keyboard)
            message_id=int(msg.message_id)
        elif call.data == 'menu2':
            keyboard = types.InlineKeyboardMarkup()
            callback_button1 = types.InlineKeyboardButton(text=emoji['left'], callback_data="menu1")
            callback_button2 = types.InlineKeyboardButton(text=emoji['tochka'], callback_data="m")
            callback_button3 = types.InlineKeyboardButton(text=emoji['right'], callback_data="menu3")
            keyboard.add(callback_button1,callback_button2, callback_button3)
            pr="="*15
            img2 = open(r"2.png", 'rb')
            bot.delete_message(chat_id, message_id)
            msg = bot.send_photo(chat_id=call_id,photo=img2, parse_mode='Markdown', reply_markup=keyboard)
            message_id=int(msg.message_id)
        elif call.data == 'menu3':
            keyboard = types.InlineKeyboardMarkup()
            callback_button1 = types.InlineKeyboardButton(text=emoji['left'], callback_data="menu2")
            callback_button2 = types.InlineKeyboardButton(text=emoji['tochka'], callback_data="m")
            callback_button3 = types.InlineKeyboardButton(text=emoji['right'], callback_data="menu4")
            keyboard.add(callback_button1,callback_button2, callback_button3)
            pr="="*15
            img3 = open(r"3.png", 'rb')
            bot.delete_message(chat_id, message_id)
            msg = bot.send_photo(chat_id=call_id,photo=img3, parse_mode='Markdown', reply_markup=keyboard)
            message_id=int(msg.message_id)
        elif call.data == 'menu4':
            keyboard = types.InlineKeyboardMarkup()
            callback_button1 = types.InlineKeyboardButton(text=emoji['left'], callback_data="menu3")
            callback_button2 = types.InlineKeyboardButton(text=emoji['tochka'], callback_data="m")
            callback_button3 = types.InlineKeyboardButton(text=emoji['right'], callback_data="menu5")
            keyboard.add(callback_button1,callback_button2, callback_button3)
            pr="="*15
            img4 = open(r"4.png", 'rb')
            bot.delete_message(chat_id, message_id)
            msg = bot.send_photo(chat_id=call_id,photo=img4, parse_mode='Markdown', reply_markup=keyboard)
            message_id=int(msg.message_id)
        elif call.data == 'menu5':
            keyboard = types.InlineKeyboardMarkup()
            callback_button1 = types.InlineKeyboardButton(text=emoji['left'], callback_data="menu4")
            callback_button2 = types.InlineKeyboardButton(text=emoji['tochka'], callback_data="m")
            callback_button3 = types.InlineKeyboardButton(text=emoji['right'], callback_data="menu6")
            keyboard.add(callback_button1,callback_button2, callback_button3)
            pr="="*15
            img5 = open(r"5.png", 'rb')
            bot.delete_message(chat_id, message_id)
            msg = bot.send_photo(chat_id=call_id,photo=img5, parse_mode='Markdown', reply_markup=keyboard)
            message_id=int(msg.message_id)
        elif call.data == 'menu6':
            keyboard = types.InlineKeyboardMarkup()
            callback_button1 = types.InlineKeyboardButton(text=emoji['left'], callback_data="menu5")
            callback_button2 = types.InlineKeyboardButton(text=emoji['tochka'], callback_data="m")
            callback_button3 = types.InlineKeyboardButton(text=emoji['tochka'], callback_data="m")
            keyboard.add(callback_button1,callback_button2, callback_button3)
            pr="="*15
            img6 = open(r"6.png", 'rb')
            bot.delete_message(chat_id, message_id)
            msg = bot.send_photo(chat_id=call_id,photo=img6, parse_mode='Markdown', reply_markup=keyboard)
            message_id=int(msg.message_id)
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
