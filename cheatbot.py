# TOKEN = '1909760361:AAHGnNMU4fh5whCFNsDscHm8rGOoh0bBhdE'
# USERNAME = 'Bombsquadadsbot'
# app = Flask(__name__)
# dp = Dispatcher(bot, None, workers=0, use_context=True)

# bot.delete_webhook()
# url = "https://{}.pythonanywhere.com/{}".format(USERNAME, TOKEN)
# bot.set_webhook(url=url)

# # process updates
# @app.route('/{}'.format(TOKEN), methods=["POST"])
# def webhook():
#     json_string = request.stream.read().decode('utf-8')
#     update = Update.de_json(json.loads(json_string), bot)
#     dp.process_update(update)
#     return 'ok', 200

# dp.add_error_handler(error)
# if __name__ == '__main__':
#     main()

from traceback import format_exc
from flask import Flask, request, send_file
import json
import re
import telegram
from telegram import *
from telegram.ext import *
import time
from datetime import datetime, timedelta, timezone
import random
from decimal import Decimal
import pytz
import sqlite3
from persiantools.jdatetime import JalaliDate
from persiantools import characters, digits
from telegram.utils.helpers import mention_markdown, escape_markdown
import requests
import os

def iran_time():
    utc_now = datetime.now(timezone.utc)
    iran_time_aware = utc_now.astimezone(timezone(timedelta(hours=3, minutes=30)))
    return iran_time_aware

connect = sqlite3.connect('cheatbot_database.db')
cursor = connect.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS messagecounter(name, id, count, total_count, real_id)')
select_date = cursor.execute('SELECT * FROM messagecounter WHERE id="0"').fetchone()
if select_date == [] or select_date==None:
    cursor.execute(f'INSERT INTO messagecounter(name, id) VALUES("{(iran_time()).date()}", "0")')
connect.commit()
permenant_db = sqlite3.connect('permenant_cheatbot_database.db')
pcursor = permenant_db.cursor()
pcursor.execute('CREATE TABLE IF NOT EXISTS users(name, id, rank1, rank2, rank3, rank4, rank5, others)')

# datetime.timezone(timedelta(hours=3, minutes=30),'yoyo')

USERNAME = 'cheatbot'

rank1=175
rank2=200
rank3=225
rank4=260
rank5=350

SPAMMER = 7
SAVED_MESSAGE_COUNT = 10
SAVED_MESSAGE_TIME = 5
last_chats = {}
last_chat_time = time.time()
TOKEN = '1934284461:AAFOWpQIgI0kYp1vou4ZZpgX5oE9BmPPRGA'
bot = Bot(TOKEN)
admin = 116530269
group_id = -1001313152808
did_coin = {} # {28638234: (time)}
members ={
    # @arshi_83
    # '⁣سخنگوی وزارت هافبک گینه نو':
    # 1845249938,
    # 'ارشیا':
    #     404697026,
    'ارشیا'
        :7020777121,
    'Amir Abbas TG': 267856089,
    'Amir Abbas SH': 1152331945,
    'Amir Abbas SH2': 2092006372,
    'Ilia B': 959141083,
    'Ilia': 5490157471,
    'Sadra': 652080777,
    'MH': 973767329,
    'Matin': 1668665055,
    # 'Arshia': 404697026,
    '⁣Ahmad.r2t': 420129186,
    'Bagheri': 1297696568,
    'Mohammad Mahdi': 8142045436,
    'Ali': 112217018,
    '❦⇝𝑀𝑎𝑡𝑖𝑛⇜❦': 331798549,
    'Pouria': 1477365219,
    # 'M...': 6262780852,
    'Amirali': 966531936,
    # 'Amirmahdi Sh': 910995796,
    'H.R.M.Y': 5478738349,
    'Loghi 2':8094539526,
    # 'Farbod': 5693082086,
    'Farbod': 8348155039,
    'Parsa': 1162657023,
    'Eshasn': 5820972121,
    # 'Abolfazl': 876350604,
    'Taha': 107795826,
    'Iman': 116530269

}
mention_with_message={
    'arshia': 271435,
    'abbas t': 257026,
    'abbas s1': 292514,
    'abbas s2': 214464,
    'ilia b': 197369,
    'ilia s': 241738,
    'sadra': 268126,#5823,
    'mohammadhossein 1': 280879,
    'matin': 210193,
    'ahmad': 233570,
    'bagher': 245192,
    'behbood': 83405,
    'arjmand': 167735,
    'pouria': 203987,
    'mahdi': 184697,
    'mahdi 2': 565085,
    'mahdi 1': 565083,
    'amirali': 250031,
    'hamidreza': 233089,
    'farbod': 251093,
    'farbod 2': 565125,
    'parsa': 294575,
    'ehsan': 268212,
    'abolfazl': 386738,
    'iman': 291436
}
taghian_tag = False
QUES_COUNT, WAIT_TO_REPLY, END_EXAM = 0, 1, 2
FIND_ANSWERS = 0
FIND_FACTORIEL_ANSWERS = 0
FIND_COLON_ANSWERS = 0

messages = {'date': iran_time().date()}
# InlineKeyboards
end_exam = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("دریافت پاسخنامه", callback_data='answer_list'),
        InlineKeyboardButton("اتمام آزمون", callback_data='end_exam')
    ]
])


def get_gemini_response_file(user_input: str, api_key: str = None) -> str:
    """
    با API هوش مصنوعی گوگل ارتباط برقرار می‌کند و تاریخچه گفتگو را در یک فایل ذخیره می‌کند.
    
    Args:
        user_input (str): متنی که کاربر برای مدل ارسال می‌کند.
        api_key (str, optional): کلید API برای دسترسی به سرویس.
    
    Returns:
        str: پاسخ دریافتی از مدل هوش مصنوعی یا یک پیام خطا.
    """
    HISTORY_FILE = "conversation_history.json"
    if api_key is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "Error: API key not provided."
    
    # بارگذاری تاریخچه از فایل
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                # اگر فایل خالی یا خراب بود، تاریخچه را خالی در نظر می‌گیریم
                history = []
    
    MODEL_ID = "gemini-2.5-flash"
    GENERATE_CONTENT_API = "generateContent"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:{GENERATE_CONTENT_API}?key={api_key}"
    
    # اضافه کردن پیام جدید کاربر به تاریخچه
    history.append({"role": "user", "parts": [{"text": user_input}]})
    
    request_data = {
        "contents": history,
        "generationConfig": {
            "thinkingConfig": {
                "thinkingBudget": -1,
            },
        },
        "tools": [
            {
                "googleSearch": {}
            },
        ],
    }
    
    try:
        response = requests.post(url, json=request_data)
        response.raise_for_status()
        
        json_response = response.json()
        
        if 'candidates' in json_response and len(json_response['candidates']) > 0:
            response_text = json_response['candidates'][0]['content']['parts'][0]['text']
            
            # اضافه کردن پاسخ مدل به تاریخچه و ذخیره در فایل
            history.append({"role": "model", "parts": [{"text": response_text}]})
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=4)
            
            return response_text
    
    except requests.exceptions.RequestException as e:
        me(str(format_exc())[:1000])
        return f"Error: Request failed. Details: {e}"
    except (json.JSONDecodeError, IndexError, KeyError) as e:
        me(str(format_exc())[:1000])
        return f"Error: Invalid JSON response or structure. Details: {e}"
        
    return "Error: Could not retrieve a valid response from the API."


def mention_with_name(id, name):
    return f'<a href="tg://user?id={id}">{name}</a>'

def me(*text):
    bot.send_message(admin, str(' '.join(list(map(str, text)))))

def order_it(x):
    return int(x[2])

def de_tuplize(lst:list):
    out_lst = []
    for i in lst:
        out_lst.append(int(i[0]))
    return out_lst

def p2(a, b, c):
    delta = (b**2) - 4*(a*c)
    if a+b+c == 0:
        return f'1 , c/a:\n<code>1</code> or <code>{c/a}</code>'
    elif b == a+c:
        return f'-1, -c/a:\n<code>-1</code> or <code>{-c/a}</code>'
    if delta < 0:
        return 'ریشه حقیق ندارد'
    elif delta == 0:
        return f'-b/2a:\n<code>{-b/2*a}</code>'
    else:
        radical = delta**(1/2)
        return f'-{b} +- {radical} / {2*a}:\n<code>{((b*-1) + radical)/(2*a)}</code> or <code>{((b*-1) - radical)/ (2*a)}</code>'


def check_daily_list():
    try:
        with open('daily_list.json', 'r') as f:
            content = json.load(f)
            if datetime.strptime(content['time'], '%Y-%m-%d').date() < iran_time().date():
                content['matin']['voices']=[]
                content['taklers']=[]
                content['snipers']=[]
                content['counter']={}
                content['kits']={}
                content['medic'] = []
                content['fooocus_last_used'] = time.time()-99999
                content['promoted'] = [None, False] # [id, did the promote?, time of promote]
                content['time'] = datetime.strftime(iran_time(), '%Y-%m-%d')
                content['suicide_bomber'] = {}
                with open('daily_list.json','w') as t: t.write(json.dumps(content))
    except:
        print(format_exc())
        with open('daily_list.json', 'w') as f:
            the_dict = \
            {'time': datetime.strftime(iran_time(), '%Y-%m-%d'),
            'takl_time': (iran_time()).strftime('%Y-%m-%d %H'),
            'taklers': [],
            'snipers': [],
            'counter': {},
            'kits': {},
            'medic': [],
            'fooocus_last_used': time.time()-99999,
            'promoted': [None, False], # [id, did the promote?, time of promote]
            'suicide_bomber': {},
            "matin":{
                "voices":[]
            }}
            f.write(json.dumps(the_dict))


def format_e(n):
    a = '%E' % n
    return a.split('E')[0].rstrip('0').rstrip('.') + '*10^' + a.split('E')[1]


def factoriel_func(factoreil_number, division_number = None):
    zarb=1
    tagh=1

    for i in range(1, factoreil_number + 1):
        zarb = zarb * i
    if division_number == None:
        return f'<code>{zarb}</code>'
    else:
        if division_number > factoreil_number:
            for i in range(1, round(division_number) + 1):
                tagh = tagh * i
            result = tagh / zarb

            return f'تقسیم کسری میشود ولی برعکسش میشه این (یعنی {division_number}! تقسیم بر {factoreil_number}!): \n<code>{result}</code>'

        elif division_number > 0:
            for i in range(1, round(division_number) + 1):
                tagh = tagh * i
            result = zarb / tagh
            return f'<code>{result}</code>'


def colon_func(k,q1,q2,f,r):

    if q1 == '?' or q1 == '؟':
        formule = (f*r**2) / (k*q2)
        return format_e(formule)
    elif q2 == '?' or q2 == '؟':
        formule = (f*r**2) / (k*q1)
        return format_e(formule)
    elif f == '?' or f == '؟':
        formule = (k*q1*q2) / r**2
        return format_e(formule)
    elif r == '?' or r == '؟':
        formule = (k*q1*q2/f)**(1/2)
        return format_e(formule)

def s(message_id, message, context: CallbackContext):
    try:
        context.bot.send_message(group_id, f'این پیامو بخون:\nhttps://t.me/c/1313152808/{message.reply_to_message.message_id}', reply_to_message_id=message_id, disable_web_page_preview=True)
    except:
        context.bot.send_message(group_id, f'این پیامو بخون:\nhttps://t.me/c/1313152808/{message.message_id}', reply_to_message_id=message_id, disable_web_page_preview=True)
    time.sleep(1)

def start(update: Update, context: CallbackContext):
    message = update.message
    msg_id = message.reply_text(
        'Well Well Well ...\nتعداد سوالارو ریپلای کن به این پیام')
    context.chat_data['ques_count_id'] = msg_id.message_id
    return QUES_COUNT


def inline_handler(update: Update, context: CallbackContext):
    query = update.callback_query

    if query.data == 'answer_list':
        try:
            for i in context.chat_data['exam']:
                context.bot.forward_message(
                    chat_id=query.message.chat_id, message_id=i, from_chat_id=query.message.chat_id)
            query.answer()
        except:
            query.answer()

    elif query.data == 'end_exam':
        try:
            query.answer('Good Luck!')
            query.edit_message_text('ایولا بروبچ موفق باشین😉')
            for i in context.chat_data['exam']:
                context.bot.forward_message(
                    chat_id=query.message.chat_id, message_id=i, from_chat_id=query.message.chat_id)
            return ConversationHandler.END
        except:
            query.answer()


def ques_count(update: Update, context: CallbackContext):
    message = update.message
    if str(message.reply_to_message.message_id) == str(context.chat_data['ques_count_id']):
        try:
            ques_count = int(message.text)
            if ques_count > 20:
                message.reply_text('بوز ممبری دیگه بالای 20 تا نمشه خیخی')
                return QUES_COUNT
            context.chat_data['exam'] = []
            for i in range(1, ques_count + 1):
                msg = context.bot.send_message(
                    chat_id=message.chat_id, text='#سوالات\n\nسوال {}-'.format(i))
                context.chat_data['exam'].append(int(msg.message_id))
                time.sleep(0.5)
            context.bot.send_message(
                chat_id=message.chat_id, text='بعد از اتمام آزمون، از دکمه زیر استفاده کنید تا پاسخنامه ارسال شود', reply_markup=end_exam)
            return ConversationHandler.END
        except:
            print('Bad News')
            return QUES_COUNT


def add_answer(update: Update, context: CallbackContext):
    message = update.message
    try:
        if int(message.reply_to_message.from_user.id) == 1934284461 and int(message.reply_to_message.message_id) in context.chat_data['exam']:

            message_content = message.reply_to_message.text_html
            context.bot.edit_message_text(text=message_content + '\n' + mention_with_name(message.from_user.id, message.from_user.first_name) +
                                          ': ' + message.text, chat_id=message.chat_id, message_id=message.reply_to_message.message_id, parse_mode=telegram.ParseMode.HTML)
    except:
        pass


def add_media_answer(update: Update, context: CallbackContext):
    message = update.message
    if int(message.reply_to_message.from_user.id) == 1934284461 and 'exam' in list(context.chat_data.keys()) and int(message.reply_to_message.message_id) in context.chat_data['exam']:

        message_content = message.reply_to_message.text_html
        context.bot.edit_message_text(text=message_content + '\n' + mention_with_name(message.from_user.id, message.from_user.first_name) +
                                      ': ' + f'<a href="{message.link}"><b><i>FILE</i></b></a>', chat_id=message.chat_id, message_id=message.reply_to_message.message_id, parse_mode=telegram.ParseMode.HTML)


def bot_cammands(update: Update, context: CallbackContext):
    global taghian_tag
    message = update.message
    if message.text == None: return
    msg = update.message.text.split()
    if len(msg) <= 1:
        message.reply_text('جونم؟ (پیامای بعدیتو نخواهم فهمید هیهیهیهی)')
        return
    elif msg[1] in ['سوال']:
        try:
            x = {}
            for i in range(1, len(context.chat_data['exam']) + 1):
                x[(context.chat_data['exam'][i-1])] = i
            for key, val in x.items():
                if str(val) == str(msg[2]):
                    message_answer = context.bot.forward_message(
                        chat_id=message.chat_id, message_id=key, from_chat_id=message.chat_id)
                    context.bot.send_message(
                        chat_id=message.chat_id, text=f'<a href="t.me/c/{str(message.chat_id)[2:]}/{key}">پیامی که فوروارد شده.</a>', reply_to_message_id=message_answer.message_id, parse_mode=ParseMode.HTML)
        except:
            message.reply_text('آزمونی در حال اجرا نیست.', reply_to_message_id=message.message_id)
    elif msg[1] in ['پاسخنامه']:
        try:
            for i in context.chat_data['exam']:
                context.bot.forward_message(
                    chat_id=message.chat_id, message_id=i, from_chat_id=message.chat_id)
                time.sleep(0.5)
        except:
            message.reply_text('آزمونی درحال اجرا نیست.', reply_to_message_id=message.message_id)

    elif msg[1] == 'کمک':
        message.reply_text('برای ساخت پاسخنامه بنویس /start و بفرست یا روی همین متن آبی کلیک کن\nبرای حل معدله درجه دو بنویس <code>معادله</code> و بر اساس راهنما پیش برو\nبرای دریافت فاکتوریل بنویس <code>فاکتوریل</code> و بر اساس راهنما پیش برو', reply_to_message_id=message.message_id, parse_mode=ParseMode.HTML)
    elif 'ماشین حساب' in ' '.join(msg[1:]):
        try:
            soal = message.text.split('\n')
            x = soal[1].replace(' ', '')
            for i in x:
                if i in ['1','2','3','4','5','6','7','8','9','0',' ','*','/','+','-','%','.',')', '(']:
                    pass
                else:
                    message.reply_text("تنها مجاز به استفاده از <code>'1','2','3','4','5','6','7','8','9','0',' ','*','/','+','-','%','.',')','('</code> میباشید", reply_to_message_id=message.message_id, parse_mode=ParseMode.HTML)
                    return
            message.reply_text(eval(x), reply_to_message_id=message.message_id)
        except:
            message.reply_text('محاسبات خود را با این فرمت ارسال کنید: \n<code>بات ماشین حساب\n2*2</code>', reply_to_message_id=message.message_id, parse_mode=ParseMode.HTML)
    elif msg[1] == 'بنویس' or msg[1] == 'بگو':
        x = ' '.join(msg[2:])
        context.bot.send_message(chat_id=message.chat_id, text=x)

    elif msg[1] == 'بنظرت':
        answer = random.choice(['به احتمال 99 درصد آره', 'به احتمال 99 درصد نه', 'آره','نه','نمیدونم والا',f'از بچه ها بپرس'])
        message.reply_text(answer)
    elif ' '.join(msg[1:]) == 'تگ قطعی':

        if taghian_tag==True:
            return
        if message.from_user.id == 267856089:
            taghian_tag = True
        l = list(mention_with_message.values())
        s(l[0], message, context)
        s(l[1], message, context)
        s(l[2], message, context)
        s(l[3], message, context)
        time.sleep(5)
        s(l[4], message, context)
        s(l[5], message, context)
        s(l[6], message, context)
        s(l[7], message, context)
        time.sleep(5)
        s(l[8], message, context)
        s(l[9], message, context)
        s(l[10], message, context)
        s(l[11], message, context)
        time.sleep(5)
        s(l[12], message, context)
        s(l[13], message, context)
        s(l[14], message, context)
        s(l[15], message, context)
        time.sleep(5)
        s(l[16], message, context)
        s(l[17], message, context)
        s(l[18], message, context)
        s(l[19], message, context)
        time.sleep(5)
        s(l[20], message, context)


        # try:
        #     for message_id in mention_with_message.values():
        #         context.bot.send_message(group_id, f'این پیامو بخون:\nhttps://t.me/c/1313152808/{message.reply_to_message.message_id}', reply_to_message_id=message_id, disable_web_page_preview=True)
        # except:
        # print(format_exc())
        # list_of_message_ids = list(mention_with_message.values()).copy()
        # x=100
        # while x<=len(list_of_message_ids):
        #     context.bot.send_message(116530269, f'این پیامو بخون:\nhttps://t.me/c/1313152808/{message.message_id}', disable_web_page_preview=True)#, reply_to_message_id=list_of_message_ids[0])
        #     list_of_message_ids.pop(0)
        #     time.sleep(3)
        #     print(x)


        # if len(list_of_message_ids)==4:
        #     reply_mention(list_of_message_ids[0],context,message);reply_mention(list_of_message_ids[1],context,message);reply_mention(list_of_message_ids[2],context,message);reply_mention(list_of_message_ids[3],context,message)
        # elif len(list_of_message_ids)==5:
        #     reply_mention(list_of_message_ids[0],context,message);reply_mention(list_of_message_ids[1],context,message);reply_mention(list_of_message_ids[2],context,message);reply_mention(list_of_message_ids[3],context,message);reply_mention(list_of_message_ids[4],context,message)
        # elif len(list_of_message_ids)==6:
        #     reply_mention(list_of_message_ids[0],context,message);reply_mention(list_of_message_ids[1],context,message);reply_mention(list_of_message_ids[2],context,message);reply_mention(list_of_message_ids[3],context,message);reply_mention(list_of_message_ids[4],context,message);reply_mention(list_of_message_ids[5],context,message)
        # elif len(list_of_message_ids)==7:
        #     reply_mention(list_of_message_ids[0],context,message);reply_mention(list_of_message_ids[1],context,message);reply_mention(list_of_message_ids[2],context,message);reply_mention(list_of_message_ids[3],context,message);reply_mention(list_of_message_ids[4],context,message);reply_mention(list_of_message_ids[5],context,message);reply_mention(list_of_message_ids[6],context,message)
        # else:
        #     message.reply_text('تعریف نشده، تعریف کنید.')

        # for message_ids in mention_with_message.values():
        #     context.bot.send_message(group_id, f'این پیامو بخون:\nhttps://t.me/c/1313152808/{message.message_id}', reply_to_message_id=message_ids, disable_web_page_preview=True)
        #     time.sleep(3)
    elif ' '.join(msg[1:]) in ['نجاتش بده', 'محافظ', 'محافظت', 'سیو', 'محافظت کن', 'هیل']:
        if message.reply_to_message==None:
            message.reply_text('روی ینفر ریپلای کن')
            return
        with open('daily_list.json', 'r') as f: content = json.load(f)
        if message.reply_to_message.from_user.id in content['medic']:
            message.reply_text('از قبل تحت محافظت بوده.')
            return
        for i,j in content['kits'].get(str(message.from_user.id), [[None, 999]]):
            if i == 'medic' and j<3:
                content['medic'].append(message.reply_to_message.from_user.id)
                for i in range(len(content['kits'][str(message.from_user.id)])):
                    if content['kits'][str(message.from_user.id)][i][0] == 'medic': content['kits'][str(message.from_user.id)][i][1]+=1
                message.reply_text('از شخص مورد نظر محافظت خواهد شد.')
                with open('daily_list.json', 'w') as f: f.write(json.dumps(content))
                try:

                    context.bot.restrict_chat_member(group_id, message.reply_to_message.from_user.id, until_date=time.time()+40, permissions =ChatPermissions(True,True,True,True,True,True,True,True))
                    me('done')
                except Exception as e:
                    me(e)
                    pass
            elif i == 'medic' and not j<3:
                if i==None:
                    message.reply_text('مدیک نداری خوشتیپ')
                    return
                message.reply_text('دیگه نمیتونی بیشتر از این بقیرو نجات بدی')
    elif msg[1] == 'تگ' and int(message.from_user.id) in members.values():
        if taghian_tag==True and message.from_user.id == 267856089:
            return
        if message.from_user.id == 267856089:
            taghian_tag = True
        tagged = ''
        x=0

        for name, id in members.items():
            tagged += f'{mention_markdown(id, name, 2)} \| '
            x+=1
            if x==4:
                if message.reply_to_message==None:
                    message.reply_text(tagged.strip(' \| '), parse_mode=telegram.ParseMode.MARKDOWN_V2, quote=True)
                else:
                    context.bot.send_message(message.chat.id, tagged.strip(' \| '), parse_mode=telegram.ParseMode.MARKDOWN_V2, reply_to_message_id=message.reply_to_message.message_id)
                x=0
                tagged=''

        if message.reply_to_message==None:
            message.reply_text(tagged.strip(' \| '), parse_mode=telegram.ParseMode.MARKDOWN_V2, quote=True)
        else:
            context.bot.send_message(message.chat.id, tagged.strip(' \| '), parse_mode=telegram.ParseMode.MARKDOWN_V2, reply_to_message_id=message.reply_to_message.message_id)

    elif msg[1]=='تکل':
        check_daily_list()
        with open('daily_list.json', 'r') as f: content = json.load(f)
        n = iran_time()
        is_able_to_takl = False
        for i,j in content['kits'].get(str(message.from_user.id), [[None, 999]]):
            if i=='takler' and j<3:
                is_able_to_takl = True
                break

        if datetime.strptime(content['takl_time'], '%Y-%m-%d %H')==datetime(n.year, n.month, n.day, n.hour) and not is_able_to_takl:
            message.reply_text('این ساعت تکل رفتم برو ساعت قبل بیا')
        else:
            if is_able_to_takl:
                for i in range(len(content['kits'][str(message.from_user.id)])):
                    if content['kits'][str(message.from_user.id)][i][0] == 'takler': content['kits'][str(message.from_user.id)][i][1] += 1
                with open('daily_list.json', 'w') as f: f.write(json.dumps(content))
            members_copy = members.copy()
            id = random.choice(list(members_copy.values()))

            members_copy.pop('Amir Abbas SH2')
            name = list(members_copy.keys())[list(members_copy.values()).index(id)]

            restrict_minutes = random.choices([7,8,9,10,60], weights=[30,30,30,30,1], k=1)[0]
            until_date = time.time()+(restrict_minutes*60)
            taklers_id = []
            try:
                if content['taklers']!=[]:
                    for j in content['taklers']:
                        taklers_id.append(str(list(j.keys())[0]))
                    if str(message.from_user.id) in taklers_id:
                        for i in content['taklers']:
                            if str(list(i.keys())[0]) == str(message.from_user.id):
                                takles_per_user = content['taklers'][content['taklers'].index(i)][str(message.from_user.id)]
                                if not is_able_to_takl: takles_per_user += 1
                                if takles_per_user > 3 and not is_able_to_takl:
                                    message.reply_text('عامو بسته دیگه امروز 3 بار تکل رفتی')
                                    return
                                content['taklers'][content['taklers'].index(i)][str(message.from_user.id)] = takles_per_user

                                break

                    else:
                        content['taklers'].append({str(message.from_user.id):1})
                        takles_per_user = 1
                else:
                    content['taklers'].append({str(message.from_user.id):1})
                    takles_per_user = 1
                if name == 'Amir Abbas SH':
                    context.bot.restrict_chat_member(group_id, members['Amir Abbas SH2'], until_date=until_date, permissions =ChatPermissions(can_send_messages=False, can_send_media_messages=False))
                elif name == 'Amir Abbas SH2':
                    context.bot.restrict_chat_member(group_id, members['Amir Abbas SH'], until_date=until_date, permissions =ChatPermissions(can_send_messages=False, can_send_media_messages=False))
                context.bot.restrict_chat_member(group_id, id, until_date=until_date, permissions =ChatPermissions(can_send_messages=False, can_send_media_messages=False))
                content['takl_time']=datetime.strftime(n, '%Y-%m-%d %H')

                with open('daily_list.json', 'w') as f: f.write(json.dumps(content))
                message.reply_text(f'روی {mention_markdown(id, escape_markdown(name, 2))} تکل رفتم و برای {restrict_minutes} دقیقه مصدوم شد\n\({takles_per_user}\/3\)',parse_mode=telegram.ParseMode.MARKDOWN_V2)
            except:
                print(format_exc())
                message.reply_text(f'روی {mention_markdown(id, escape_markdown(name, 2))} تکل رفتم ولی برای {restrict_minutes} دقیقه مصدوم نشد، خودت خفه شو داش چون ادمینی\nاما جایزه، جایزه اینه که بازم میتونید ینفر دیگرو مصدوم کنید اما با دقت عمل کنید، آیا واقعا اینکارو میخواید *همین الان* بکنید؟\!',parse_mode=telegram.ParseMode.MARKDOWN_V2)
    elif msg[1]=='اسنایپ' or ' '.join(msg[1:]) in ['کونش بذار', 'کونش بزار']:
        check_daily_list()
        with open('daily_list.json', 'r') as f: content = json.load(f)
        is_sniper = False
        for i,j in content['kits'].get(str(message.from_user.id), [[None, 999]]):
            if i=='sniper' and j<1:
                is_sniper = True
                break
        if message.reply_to_message == None:
            message.reply_text('هدف رو با ریپلای کردن نشون بده')
            return
        if message.from_user.id in content['snipers'] and not is_sniper:
            message.reply_text('امروز اسنایپ کردی برگرد خانتان')
            return
        chance=random.randint(1,10) # chance: 1/endpoint_range
        snipe = random.randint(1,10)
        bot.send_message(admin, str(chance)+' snipe:'+str(snipe))
        if (content['promoted'][0]!=None and message.from_user.id == content['promoted'][0]): chance = snipe
        if is_sniper:
            chance = snipe
            for i in range(len(content['kits'][str(message.from_user.id)])):
                if content['kits'][str(message.from_user.id)][i][0] == 'sniper': content['kits'][str(message.from_user.id)][i][1] += 1
            content['kits'][str(message.from_user.id)]

        if chance==snipe:
            die_minutes=random.randint(40,55)
            msg_reply = message.reply_to_message.from_user.id
            for i,j in content['kits'].get(str(msg_reply), [[None, 999]]):
                if i=='medic':
                    message.reply_text('خاک شدی مشتی، داوشمون کیت مدیک داشت')
                    return
            if msg_reply in content['medic']:
                message.reply_text('ایشون محافظ تنش بود')
                with open('daily_list.json', 'w') as f: f.write(json.dumps(content))
                return
            try:

                if message.reply_to_message.from_user.id in [members['Amir Abbas SH'], members['Amir Abbas SH2']]: context.bot.restrict_chat_member(group_id, members['Amir Abbas SH'], until_date=time.time()+(die_minutes*60), permissions =ChatPermissions(can_send_messages=False, can_send_media_messages=False)); context.bot.restrict_chat_member(group_id, members['Amir Abbas SH2'], until_date=time.time()+(die_minutes*60), permissions =ChatPermissions(can_send_messages=False, can_send_media_messages=False))

                else: context.bot.restrict_chat_member(group_id, message.reply_to_message.from_user.id, until_date=time.time()+(die_minutes*60), permissions =ChatPermissions(can_send_messages=False, can_send_media_messages=False))
            except: return
            message.reply_text(random.choice(['تیر صاف رفت تو کونش','Terrorists win.','هدف با موفقیت میل شد', 'عااااااااح (صدای هدف بعد از اصابت تیر)']))
            message.reply_video('CgACAgQAAxkBAAJAO2VD0y1kge6Dkj6DEMvOmv9RY4t9AAL4EAAC8fhgU2MI6xznmkmcMwQ', caption=f'مدت زمان مرگ: {die_minutes} دقیقه')


        else:
            message.reply_text(random.choice(['متاسفانه هدف تکون خورد و تیر اصابت نکرد. ایشالا دفعه بعدی', 'تیر از بیخ گوشش رد شد', 'Enemy lost. Better luck next time.','متاسفانه هدف تیر رو ناکام گذاشت','تیر نتونست به هدف رخنه کنه','هدف به تیر تسلیم نشد','داوشمون bulletproof عه']))
        content['snipers'].append(message.from_user.id)
        with open('daily_list.json', 'w') as f: f.write(json.dumps(content))
    elif msg[1] == 'خودکشی':
        if message.from_user.id in [members['Amir Abbas SH'], members['Amir Abbas SH2']]: context.bot.restrict_chat_member(group_id, members['Amir Abbas SH'], until_date=time.time()+3600, permissions =ChatPermissions(can_send_messages=False, can_send_media_messages=False)); context.bot.restrict_chat_member(group_id, members['Amir Abbas SH2'], until_date=time.time()+3600, permissions =ChatPermissions(can_send_messages=False, can_send_media_messages=False))
        elif message.from_user.id in [members['⁣سخنگوی وزارت هافبک گینه نو'], members['MH']]: context.bot.restrict_chat_member(group_id, members['⁣سخنگوی وزارت هافبک گینه نو'], until_date=time.time()+3600, permissions =ChatPermissions(can_send_messages=False, can_send_media_messages=False)); context.bot.restrict_chat_member(group_id, members['MH'], until_date=time.time()+3600, permissions =ChatPermissions(can_send_messages=False, can_send_media_messages=False))
        elif message.from_user.id in [members['Mohammad Mahdi'], members['Loghi 2']]: context.bot.restrict_chat_member(group_id, members['Mohammad Mahdi'], until_date=time.time()+3600, permissions =ChatPermissions(can_send_messages=False, can_send_media_messages=False)); context.bot.restrict_chat_member(group_id, members['Loghi 2'], until_date=time.time()+3600, permissions =ChatPermissions(can_send_messages=False, can_send_media_messages=False))

        try:
            context.bot.restrict_chat_member(group_id, message.from_user.id, until_date=time.time()+3600, permissions =ChatPermissions(can_send_messages=False, can_send_media_messages=False))
        except: pass
        message.reply_text('به امید دیدار، سرباز')

    elif msg[1]=='انتحاری':
        if message.reply_to_message == None:
            message.reply_text('هدف رو با ریپلای کردن نشون بده')
            return
        check_daily_list()
        with open('daily_list.json', 'r') as f: content = json.load(f)
        if str(message.from_user.id) in content['suicide_bomber'].keys():
            message.reply_text('امروز انتحاری زدی دا. برو ریوایو شو دیروز بیا')
            return
        else:
            try:
                chance = random.choice([1,1,1,1,1,1,1,1,0,0])
                ban_minutes = random.randint(10, 20)
                self_ban_minutes = random.randint(15, 20)
                if admin in [int(message.reply_to_message.from_user.id), int(message.from_user.id)]: raise Exception
                if chance: context.bot.restrict_chat_member(group_id, message.reply_to_message.from_user.id, until_date=time.time()+(ban_minutes*60), permissions =ChatPermissions(can_send_messages=False, can_send_media_messages=False))
                context.bot.restrict_chat_member(group_id, message.from_user.id, until_date=time.time()+(self_ban_minutes*60), permissions =ChatPermissions(can_send_messages=False, can_send_media_messages=False))
                message.reply_text(f'هدف با موفقیت میل شد. شما با این کار حتما به بهشت خواهید رفت. (خیخی)\n{self_ban_minutes} دقیقه شما | {ban_minutes} دقیقه طرف مقابل' if chance else f'هدف جاخالی داد و شما ریدید. اما حتما به بهشت خواهید رفت. (خیخی)\n{self_ban_minutes} دقیقه شما')
                if str(message.from_user.id) in content['suicide_bomber']:
                    content['suicide_bomber'][str(message.from_user.id)].append(message.reply_to_message.from_user.id if chance else 0)
                else:
                    content['suicide_bomber'][str(message.from_user.id)] = [message.reply_to_message.from_user.id if chance else 0]

            except:
                message.reply_text('متاسفانه خارج از اختیارات منه (احتمالا ادمینه)')
            
        with open('daily_list.json', 'w') as f: f.write(json.dumps(content))


    elif msg[1] in ['عروج', 'تعالی']:
        check_daily_list()
        with open('daily_list.json', 'r') as f: content = json.load(f)
        if content['promoted'][1]==True:
            message.reply_text('امروز ینفر تعالی پیدا کرد. برای امروز کافیه.')
            return
        while True:
            name = random.choice(list(members.keys()))
            if name in ['Eshasn', '❦⇝𝑀𝑎𝑡𝑖𝑛⇜❦', 'Ali', 'Amir Abbas SH2', 'ارشیا', '⁣سخنگوی وزارت هافبک گینه نو']:
                continue
            break
        id = members[name]
        content['promoted'] = [id, True, time.time()]
        context.bot.promote_chat_member(chat_id=group_id, user_id=id, can_manage_chat=True, can_pin_messages=True, can_manage_voice_chats=True)
        message.reply_text(f'بسیار عالی\nهم اکنون {mention_markdown(id, escape_markdown(name, 2))} برای 20 دقیقه میتونه به recent action ها دسترسی داشته باشه و پیام پین کنه\n**واسنایپش حتما به هدف میخوره**', parse_mode='markdown')
        with open('daily_list.json', 'w') as f: f.write(json.dumps(content))
    elif ' '.join(msg[1:]) in ['یک یا دو', 'سکه']:
        if message.from_user.id in did_coin.keys():
            if time.time() - did_coin[message.from_user.id] < 3600:
                message.reply_text('آدم یه بار بختشو امتحان میکنه پسرجان', quote=True)
                return
            else:
                did_coin.pop(message.from_user.id)
        message.reply_text(f'{random.choice([1,2])}')
        did_coin[message.from_user.id] = time.time()


    elif 'دروغ تو کارشه' in ' '.join(msg[1:]):
        if message.reply_to_message==None: message.reply_text('کیو میگی سید؟ روش ریپلای کن'); return
        if (message.reply_to_message.from_user.id == members['Amir Abbas SH'] or
        message.reply_to_message.from_user.id == members['Amir Abbas SH2']):
            message.reply_text(f'{random.choice(["داداش عباص که دروغ تو کارش نی", "عباص و دروغ؟", "میدونی که... عباص سرش بره راستگوییش نمیره", "همممم این پیام عباص یکم بوداره"])}')
        else:
            messages = [f"هممم {mention_with_name(members['Amir Abbas SH2'], 'عباص')}\nسید من بوی دروغ رو حس نمیکنم، تو حسش میکنی؟", 'اینطور که بوش میاد... دروغ تو کارش نیست.', 'اینطور که بوش میاد... دروغ تو کارشه.']
            message.reply_text(f'{random.choice(messages)}', parse_mode='html')
    elif 'آیدی' in ' '.join(msg[1:]):
        try:
            text = int(message.text.replace('ربات آیدی ', ''))
            message.reply_text(f'{mention_with_name(text, "name")}', parse_mode='html')
        except:
            message.reply_text('درخواست شما سلاسینمتبل شد')
            print(format_exc())
    elif 'دیتابیس' in ' '.join(msg[1:]) and int(message.from_user.id)==admin:
        text = cursor.execute('SELECT * FROM messagecounter').fetchall()
        msg=''
        for i in text:
            msg += f'{i}\n'
        message.reply_text(msg)
    elif 'اسفندیار' in ' '.join(msg[1:]):
        days = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه']
        dates = 'فروردین اردیبهشت خرداد تیر مرداد شهریور مهر آبان آذر دی بهمن اسفند'.split()
        the_date = digits.en_to_fa(str(JalaliDate.today())).split('-') # year-month-day
        text = f'ساعت {digits.en_to_fa(str(iran_time().hour))} {days[JalaliDate.weekday(JalaliDate.today())]} {the_date[2]} {dates[JalaliDate.today().month-1]} {the_date[0]} هم گذشتو دیگه برنمیگرده...'
        # message.reply_text(f'امروز {days[JalaliDate.weekday(JalaliDate.today())]} {digits.en_to_fa(JalaliDate.today().day)} {dates[digits.en_to_fa(JalaliDate.today().month)]} سال {digits.en_to_fa(JalaliDate.today()).year} {"-".join(the_date[::-1])} ساعت {digits.en_to_fa(str(datetime.now().hour))} گذشت و دیگه برنمیگرده...')
        message.reply_text(text)
    elif msg[1]=='اوضاع':
        name_and_others = dict(pcursor.execute('SELECT name,others FROM users').fetchall())

        name_and_others= {key: int(value) for key, value in name_and_others.items() if value != None}
        name_and_others= dict(sorted(name_and_others.items(), key=lambda item: item[1]))
        string_='افراد نوب و کم پیام:\n'
        for name,others in name_and_others.items():
            if int(others)==0:continue
            else:
                string_+=f'\n▶️<b>{name}</b>: '+f'<code>{others}</code>'
        message.reply_text(string_,quote=True, parse_mode='html')


    elif msg[1]=='وضعیت':
        name_and_rank=pcursor.execute('SELECT name,rank1,rank2,rank3,rank4,rank5 FROM users').fetchall()
        string=[f'{rank1}: Mega Messanger\n{rank2}: Ultra Messanger\n{rank3}: WTF Messanger\n{rank4}: 404 Not Found Rank Messanger\n{rank5}: ⛔️Void']
        for user in name_and_rank:
            edited_user=[]
            for i in user:
                if i!=None: edited_user.append(i)
                else: edited_user.append(0)
            if not any(edited_user[1:]): continue
            for page in range(5):
                try:

                    if len(string[page])<3800:
                        string[page]+=f'\n▶️<b>{edited_user[0]}</b>:'+'<code>'+\
                        (f'\n{rank1}: {edited_user[1]}' if edited_user[1]!=0 else '')+\
                        (f'\n{rank2}: {edited_user[2]}' if edited_user[2]!=0 else '')+\
                        (f'\n{rank3}: {edited_user[3]}' if edited_user[3]!=0 else '')+\
                        (f'\n{rank4}: {edited_user[4]}' if edited_user[4]!=0 else '')+\
                        (f'\n⛔️{rank5}⛔️: {edited_user[5]}' if edited_user[5]!=0 else '')+'</code>'
                    else: continue
                except Exception as e:
                    # x = bot.send_message(116530269, text =str(format_exc()) + str(page))
                    break
        for i in string:
            message.reply_text(i,quote=True, parse_mode='html')


    else:
        if 'انتخاب' in ' '.join(msg[1:]) or 'ترین' == msg[2] or msg[1].endswith('ترین'):
            messageid = message.message_id
            messagelink = str(message.link)
            msg = f'<a href="{messagelink.replace(str(messageid), str(random.randint(messageid-99, messageid)))}">ایناهاش</a>'
            message.reply_text(msg, parse_mode='html')
        else:
            message.reply_text(random.choice(['آره داشتی میگفتی', 'بر لب جوی بشین و گذر عمر ببین', 'آره داش موافقم', 'نه اصلا حرفشو نزن', 'شاید🤷‍♂️', 'بیا برو آقا مگه ما مسخره شماییم؟']), reply_to_message_id=message.message_id)
the_last_message=time.time()
def all_filter(update: Update, context: CallbackContext):
    global last_chat_time
    global the_last_message
    if update.message==None:
        return
    user_id = update.message.from_user.id if update.message != None else update.edited_message.from_user.id
    chat_id = update.message.chat_id if update.message != None else update.edited_message.chat_id
    if not chat_id in last_chats:
        last_chats[chat_id] = []
    last_chats[chat_id].append(user_id)

    now = time.time()
    if last_chat_time + SAVED_MESSAGE_TIME < now:
        last_chats[chat_id] = []
    else:
        if len(last_chats[chat_id]) > SAVED_MESSAGE_COUNT:
            del last_chats[chat_id][0]
        if last_chats[chat_id].count(user_id) > SPAMMER:
            update.message.delete()
            return
    last_chat_time = now

    if abs(the_last_message-now)>300:
        the_last_message=now
        with open('daily_list.json', 'r') as f: content = json.load(f)
        if content['promoted'][1]==True and content['promoted'][0]!=None:
            if abs(content['promoted'][2]-now)>1200:
                try:
                    context.bot.promote_chat_member(group_id, content['promoted'][0])
                    content['promoted'][0]=None
                    with open('daily_list.json', 'w') as f: f.write(json.dumps(content))
                except: context.bot.send_message(admin, str(format_exc()))
    # save number of chats
    user_id = update.message.from_user.id

    global cursor
    global connect
    global id_count
    id_count = {}
    try:
        user_db = pcursor.execute(f'SELECT name FROM users WHERE id=="{user_id}"').fetchone()
        if user_db == None or user_db =='' or user_db==[]:
            raise Exception('Doesn\'t Exists In DB.')
    except:
        user_db = pcursor.execute(f'INSERT INTO users(name, id) VALUES("{update.message.from_user.full_name}","{user_id}")').fetchone()
    permenant_db.commit()
    old_date = cursor.execute('SELECT name FROM messagecounter WHERE id=="0"')
    old_date = datetime.strptime(old_date.fetchone()[0], '%Y-%m-%d').date()
    now_date = iran_time().date()
    if old_date<now_date:
        cursor.execute('DELETE FROM messagecounter')
        connect.commit()
        cursor.execute(f'INSERT INTO messagecounter(name, id) VALUES("{now_date}", "0")')
        connect.commit()

    everyone = cursor.execute('SELECT id, count FROM messagecounter').fetchall()

    # print('injaaaaaaa everyone', everyone)
    if everyone!=None or everyone!=[] or everyone!='' or everyone!=[('0', None)]:
        for count_and_id in everyone:
                id = int(count_and_id[0])
                if id==0: continue
                count = int(count_and_id[1])
                id_count[id] = [count, '']
    if int(user_id) not in id_count.keys():
        try: real_id = update.message.from_user.username
        except: real_id = None
        cursor.execute(f'INSERT INTO messagecounter(id, count, name, real_id) VALUES("{user_id}", "1", "{update.message.from_user.first_name}", "{real_id}")')
        connect.commit()
        count = 1
        id_count[int(user_id)] = [count, '']
        # id_count[user_id][0] = 1
        # id_count[user_id][1] = update.message.from_user.first_name
    else:
        count = cursor.execute(f'SELECT count FROM messagecounter WHERE id="{user_id}"').fetchone()
        count = int(count[0])+1
        cursor.execute(f'UPDATE messagecounter SET count="{count}" WHERE id="{user_id}"')
        connect.commit()
        # id_count[user_id][0] = count
        # id_count[user_id][1] = update.message.from_user.first_name

    # rank1=86
    # rank2=200
    # rank3=225
    # rank4=260
    # rank5=350
    if count == rank1:
        with open('daily_list.json', 'r') as f: content=json.load(f)
        content['counter'][str(update.message.from_user.id)] = ['rank1']
        with open('daily_list.json', 'w') as f: f.write(json.dumps(content))
        update.message.reply_text(f'{rank1} تا پیام شد!\nرنک شما: Mega Messanger',quote=True)
        user_rank1 = pcursor.execute(f'SELECT rank1 FROM users WHERE id="{user_id}"').fetchone()
        if user_rank1==(None,) or user_rank1==[]:
            pcursor.execute(f'UPDATE users SET rank1="1" WHERE id="{user_id}"')
        else:
            user_rank1 = pcursor.execute(f'UPDATE users SET rank1="{int(user_rank1[0])+1}" WHERE id="{user_id}"').fetchone()
        permenant_db.commit()

    elif count == rank2:
        with open('daily_list.json', 'r') as f: content=json.load(f)
        content['counter'][str(update.message.from_user.id)].append('rank2')
        with open('daily_list.json', 'w') as f: f.write(json.dumps(content))
        update.message.reply_text(f'ایول دادا با این پیامت امروز {rank2} تا پیام دادی\nرنک شما: Ultra Messanger',quote=True)
        user_rank2 = pcursor.execute(f'SELECT rank2 FROM users WHERE id="{user_id}"').fetchone()
        if user_rank2==None or user_rank2==[]:
            pcursor.execute(f'UPDATE users SET rank2="1" WHERE id="{user_id}"')
        else:
            user_rank2 = pcursor.execute(f'UPDATE users SET rank2="{int(user_rank2[0])+1}" WHERE id="{user_id}"').fetchone()
        permenant_db.commit()

    elif count == rank3:
        with open('daily_list.json', 'r') as f: content=json.load(f)
        content['counter'][str(update.message.from_user.id)].append('rank3')
        with open('daily_list.json', 'w') as f: f.write(json.dumps(content))
        update.message.reply_text(f'بنازم باو دسخوش\nپیامات به {rank3} تا رسید امروز!\nرنک شما: WTF Messanger',quote=True)
        user_rank3 = pcursor.execute(f'SELECT rank3 FROM users WHERE id="{user_id}"').fetchone()
        if user_rank3==(None,) or user_rank3==[]:
            pcursor.execute(f'UPDATE users SET rank3="1" WHERE id="{user_id}"')
        else:
            user_rank3 = pcursor.execute(f'UPDATE users SET rank3="{int(user_rank3[0])+1}" WHERE id="{user_id}"').fetchone()
        permenant_db.commit()

    elif count == rank4:
        with open('daily_list.json', 'r') as f: content=json.load(f)
        content['counter'][str(update.message.from_user.id)].append('rank4')
        with open('daily_list.json', 'w') as f: f.write(json.dumps(content))
        update.message.reply_text(f'ربات به ارور برخورد چون این حجم از پیامایی که امروز فرستادیرو نمیتونه بخونه!\nپیامات {rank4} تا شد😵\nرنک شما:404 Not Found Rank Messanger',quote=True)
        user_rank4 = pcursor.execute(f'SELECT rank4 FROM users WHERE id="{user_id}"').fetchone()
        if user_rank4==(None,) or user_rank4==[]:
            pcursor.execute(f'UPDATE users SET rank4="1" WHERE id="{user_id}"')
        else:
            user_rank4 = pcursor.execute(f'UPDATE users SET rank4="{int(user_rank4[0])+1}" WHERE id="{user_id}"').fetchone()
        permenant_db.commit()

    elif count == rank5:
        with open('daily_list.json', 'r') as f: content=json.load(f)
        content['counter'][str(update.message.from_user.id)].append('rank5')
        with open('daily_list.json', 'w') as f: f.write(json.dumps(content))
        update.message.reply_text(f'این یک پیام سری از طرف رباته\nشما به پر زرترین شخص ماه نائل شدید، تبریک میگم.\nاز اینجا به بعد رنکی نیست،شما وارد خلا میشید و کسی از بعدش خبر نداره...',quote=True)
        user_rank5 = pcursor.execute(f'SELECT rank5 FROM users WHERE id="{user_id}"').fetchone()
        if user_rank5==(None,) or user_rank5==[]:
            pcursor.execute(f'UPDATE users SET rank5="1" WHERE id="{user_id}"')
        else:
            user_rank5 = pcursor.execute(f'UPDATE users SET rank5="{int(user_rank5[0])+1}" WHERE id="{user_id}"').fetchone()
        permenant_db.commit()


    # Group Messages Counter
    database_file = "cheatbot_database.db"
    table_name = "groupmessagecount"


    connection = sqlite3.connect(database_file)
    cursor_g = connection.cursor()

    # cursor_g.execute('CREATE TABLE IF NOT EXISTS groupmessagecount("0-1" INTEGER, "1-2" INTEGER,"2-3" INTEGER,"3-4" INTEGER,"4-5" INTEGER,"5-6" INTEGER,"6-7" INTEGER,"7-8" INTEGER,"8-9" INTEGER,"9-10" INTEGER,"10-11" INTEGER,"11-12" INTEGER,"12-13" INTEGER,"13-14" INTEGER,"14-15" INTEGER,"15-16" INTEGER,"16-17" INTEGER,"17-18" INTEGER,"18-19" INTEGER,"19-20" INTEGER,"20-21" INTEGER,"21-22" INTEGER,"22-23" INTEGER,"23-24" INTEGER,"time")')
    database_time = cursor_g.execute('select time from groupmessagecount').fetchone()[0]
    database_time = datetime.strptime(database_time, "%Y-%m-%d %H")
    # print(database_time, type(database_time))
    nowtime = iran_time()
    # print(database_time, type(database_time), database_time.date())
    if nowtime.date() == database_time.date():
        if nowtime.strftime("%Y-%m-%d %H") == database_time.strftime("%Y-%m-%d %H"):


            # Fetch the current value from the database
            column_name = f'{nowtime.hour}-{nowtime.hour+1}'
            cursor_g.execute(f'SELECT "{column_name}" FROM {table_name}')
            current_value = cursor_g.fetchone()[0]

            cursor_g.execute(f"UPDATE {table_name} SET '{column_name}' = ?", (current_value+1,))
            connection.commit()
        else:
            cursor_g.execute(f'UPDATE groupmessagecount set time = "{nowtime.strftime("%Y-%m-%d %H")}"')
            column_name = f'{nowtime.hour}-{nowtime.hour+1}'
            cursor_g.execute(f'SELECT "{column_name}" FROM {table_name}')
            current_value = cursor_g.fetchone()[0]

            cursor_g.execute(f"UPDATE {table_name} SET '{column_name}' = ?", (current_value+1,))
            connection.commit()

    else:
        cursor_g.execute(f'UPDATE groupmessagecount set time = "{nowtime.strftime("%Y-%m-%d %H")}"')
        for i in range(1,24):
            cursor_g.execute(f'UPDATE groupmessagecount set "{i}-{i+1}" = 0')
        cursor_g.execute(f'UPDATE groupmessagecount set "{nowtime.hour}-{nowtime.hour+1}" = 1')
        connection.commit()
    if update.message.photo!=[]:
        photo_handler(update)
def imagine_handler(update: Update, context: CallbackContext):
    if not len(update.message.text.split())>=2:
        update.message.reply_text('بعد از این دستور، متن خود را که میخواهید به تصویر تبدیل شه رو بنویسید.')
        return
    check_daily_list()
    pure_prompt = ' '.join(update.message.text.split()[1:])
    if not pure_prompt.isascii():
        update.message.reply_text('انگلیسی بنویسید')
        return
    with open('daily_list.json', 'r') as f: content=json.load(f)
    if abs(content['fooocus_last_used']-time.time())<420:
        update.message.reply_text('لطفا نهایتا 7 دقیقه دیگر امتحان کنید')
        return
    update.message.reply_text('در حال انجام...')
    content['fooocus_last_used'] = time.time()
    fal_key_id = 'c88f08ec-486a-4ae1-a8f6-1dfb7c0b77b5'
    fal_key_secret = '520d233fbf84fe4fb5df0e28cb3ee0f0'
    url = "https://110602490-fooocus.gateway.alpha.fal.ai/"
    headers = {
        "Authorization": f"Key {fal_key_id}:{fal_key_secret}",
        "Content-Type": "application/json"}
    prompt_data = {"prompt": f"{pure_prompt}"}
    response = requests.post(url, headers=headers, json=prompt_data)

    if response.status_code == 200:
        bot.send_message(admin, f"{response.json()}")
        r = requests.get(response.json()['images'][0]['url'])
        open('fooocus_image.jpg', 'wb').write(r.content)
        update.message.reply_photo(open('fooocus_image.jpg', 'rb'))
        with open('daily_list.json', 'w') as f: f.write(json.dumps(content))
        return
    else:
        bot.send_message(admin, f"Error: {response.status_code}")
        update.message.reply_text('ارور داشت')
        return
def photo_handler(update: Update):
    if update.message.caption == None: return
    if update.message.caption.startswith('/id '):
        check_daily_list()
        pure_prompt = ' '.join(update.message.caption.split()[1:])
        if not pure_prompt.isascii():
            update.message.reply_text('انگلیسی بنویسید')
            return
        if len(pure_prompt.split())<=2:
            update.message.reply_text('متن را در کپشن وارد کنید (بیشتر از دو حرف)')
            return
        with open('daily_list.json', 'r') as f: content=json.load(f)
        if abs(content['fooocus_last_used']-time.time())<420:
            update.message.reply_text('لطفا نهایتا 7 دقیقه دیگر امتحان کنید')
            return
        content['fooocus_last_used'] = time.time()
        bot.get_file(update.message.photo[-1]).download('input_illusion_diffusion.jpg')
        input_image_url = f'https://{USERNAME}.pythonanywhere.com/illusion_diffusion_image.jpg'
        fal_key_id = 'c88f08ec-486a-4ae1-a8f6-1dfb7c0b77b5'
        fal_key_secret = '520d233fbf84fe4fb5df0e28cb3ee0f0'
        url = f'https://54285744-illusion-diffusion.gateway.alpha.fal.ai/fal/queue/submit?fal_webhook=https://{USERNAME}.pythonanywhere.com/illusion_diffusion_result/{update.message.chat_id}/{update.message.message_id}'
        update.message.reply_text('در حال انجام...')
        headers = {
            "Authorization": f"Key {fal_key_id}:{fal_key_secret}",
            "Content-Type": "application/json"}
        prompt_data = {"prompt": f"{pure_prompt}",
                       "image_url": input_image_url}
        response = requests.post(url, headers=headers, json=prompt_data)
        if response.status_code != 200:
            update.message.reply_text(f'ارور داشت: {response.status_code}', )
            return
        with open('daily_list.json', 'w') as f: f.write(json.dumps(content))


def msg_filter(update: Update, context: CallbackContext):
    message = update.message
    if message == None: return
    msg_shimi = re.sub(r'[^ش,ی,م]+', '', message.text)
    msg_shimi = re.compile(r'(.)\1{1,}', re.IGNORECASE).sub(r'\1', msg_shimi)
    msg_split = message.text.split()


    # if message.text.split()[0] in ['مرسی', 'ممنون', 'دمت', 'دمتگرم','سپاس']:
    #     answer_list = random.choice(['فدت', 'قربونت','خواهش دازپش', 'بزرگواری','کار داپشتی بازم بگو'])
    #     message.reply_text(answer_list, reply_to_message_id=message.message_id, parse_mode=ParseMode.HTML)
    # elif 'دوستشو اوکی'in message.text:
    #     answer_list = random.choice(['کوفت و دوستشو اوکی کن','درد و دوستشو اوکی کن','مرض و دوستشو اوکی کن','نوب صگِ دوستو اوکی کن'])
    #     message.reply_text(answer_list, reply_to_message_id=message.message_id, parse_mode=ParseMode.HTML)

    # elif '200' in message.text: message.reply_text('داری 200 دستی بدی؟', reply_to_message_id=message.message_id, parse_mode=ParseMode.HTML)
    # elif 'انقد'in message.text: message.reply_text('🤏انقد', reply_to_message_id=message.message_id, parse_mode=ParseMode.HTML)

    if ('شیمی' in message.text.replace('', '').replace('‌', '') or 'shimi' in message.text.replace('', '').replace('‌', '').lower() or any(x in message.text for x in ['شیمی', 'shimi', 'shymy', 'shymi', 'shimy','sheme','shemi','shime']) or any(xx in message.text for xx in ['شیمی','shimi']) ) and message.from_user.username == 'AmirRook1':
        message.reply_text(f'زجه بزن شیمی فن حقیر\n(گفتش: {message.text})')
        message.delete()
        return

    elif len(msg_split) >= 2 and message.text.startswith('کیت'):
        with open('daily_list.json', 'r') as f: content=json.load(f)
        if msg_split[1] not in ['مدیک','اسنایپر', 'تکلر']:
            message.reply_text('کیت باید یکی از این سه مورد باشه:\nمدیک\nاسنایپر\nتکلر')
            return
        a = content['counter'].get(str(message.from_user.id), False)
        if a != False:
            me(a)
            if b:=(content['kits'].get(str(message.from_user.id), False)) == False:
                me([msg_split[1].replace('تکلر', 'takler').replace('اسنایپر', 'sniper').replace('مدیک', 'medic'), 0])
                content['kits'][str(message.from_user.id)] = [[msg_split[1].replace('تکلر', 'takler').replace('اسنایپر', 'sniper').replace('مدیک', 'medic'), 0]]
                message.reply_text(f'کیت انتخاب شده: {msg_split[1]}')

            else:
                me(b)
                if len(a)>len(content['kits'][str(message.from_user.id)]):
                    selected_kits = []
                    for i,j in content['kits'][str(message.from_user.id)]:
                        selected_kits.append(i)
                    me(selected_kits)
                    if msg_split[1].replace('تکلر', 'takler').replace('اسنایپر', 'sniper').replace('مدیک', 'medic') in selected_kits:
                        message.reply_text('شما قبلا این کیت رو انتخاب کردید')
                        return
                    else:
                        content['kits'][str(message.from_user.id)].append([msg_split[1].replace('تکلر', 'takler').replace('اسنایپر', 'sniper').replace('مدیک', 'medic'), 0])
                        message.reply_text(f'کیت انتخاب شده: {msg_split[1]}')
                else:
                    message.reply_text('شما قبلا کیت انتخاب کردید')

        else:
            message.reply_text('رنکت هنوز به درجه انتخاب کیت نرسیده خوشتیپ')
        with open('daily_list.json', 'w') as f: f.write(json.dumps(content))

    elif ('@sportbaadnews' in message.text.lower() or '@futball120' in message.text.lower()) and int(message.from_user.id) == 420129186:
        message.reply_text('آخه گوزوووو')
        return

    elif ('تخمم' == message.text or 'کیرم' == message.text or 'به تخمم' in message.text or 'به کیرم' in message.text) and str(message.from_user.id) == '267856089':
        message.reply_text(random.choice(['404 Not Found', 'پس به هیچجات گرفتی', 'خخخخخ جوک با نمکی بود']))
        return

    elif message.text == 'خ' and message.reply_to_message != None:
        new_msg = message.reply_to_message.text
        for i in 'ا آ ب پ ت ث ج چ ح خ د ذ ر ز ژ س ش ص ض ط ظ ع غ ف ق ک گ ل م ن و ه ی ء ئ'.split():
            new_msg = new_msg.replace(i, 'خ')
        context.bot.send_message(message.chat_id, new_msg, reply_to_message_id=message.reply_to_message.message_id)

    elif any([i in message.text for i in ['شوخوش', 'شو خوش', 'شوبخیر', 'شو بخیر', 'شب بخیر', 'شبخوش', 'شب خوش']]):
        context.bot.forward_message(message.chat_id, 116530269, 14324)
        return
    elif any([i in message.text for i in  ['صوخوش', 'صو خوش', 'صوبخیر', 'صو بخیر', 'صبح بخیر', 'صب بخیر', 'صببخیر', 'صب خوش']]):
        context.bot.forward_message(message.chat_id, 116530269, 14326)
        return

    # elif 'حاج خانوم' in message.text and str(message.from_user.id) == '959141083':
    #     answer_list = random.choice(['حاج خانوم؟حاج خانوم؟حاج خانوم؟حاج خانوم؟حاج خانوم؟حاج خانوم؟حاج خانوم؟حاج خانوم؟حاج خانوم؟حاج خانوم؟حاج خانوم؟حاج خانوم؟حاج خانوم؟حاج خانوم؟', 'نه دا فشاری نمیشم با حاج خانوم گفتنت', 'کوفت و درد و مرگ و مرض و زهر مار با حاج خانوم گفتنت'])
    #     message.reply_text(answer_list, reply_to_message_id=message.message_id, parse_mode=ParseMode.HTML)
    elif message.text in ['مگه نه؟', 'مگه نه ؟']:
        message.reply_text('دقیقا', reply_to_message_id=message.message_id, parse_mode=ParseMode.HTML)
    elif any(x in message.text for x in ['تتلو','هیدن','پیشرو','ویلسون','پوتک','رپر','ام جی']):
        message.reply_text('بره گمشه', reply_to_message_id=message.message_id, parse_mode=ParseMode.HTML)
    elif 'پیام نشمار' == message.text.strip():
        connect_ = sqlite3.connect('cheatbot_database.db')
        cursor_ = connect_.cursor()
        ids=de_tuplize(cursor_.execute('select id from messagecounter').fetchall()[1:])
        bad_guys = {}
        for id in members.values():
            if id not in ids:
                bad_guys[str(list(members.keys())[list(members.values()).index(id)])] = id

        everything = connect_.execute('SELECT name, id, count FROM messagecounter').fetchall()
        everything.remove((f'{iran_time().date()}', '0', None))
        ordered = sorted(everything, key=order_it, reverse=False)
        low_bad_guys = {}
        for name, id, count in ordered:
            if int(id) in members.values():
                low_bad_guys[str(list(members.keys())[list(members.values()).index(int(id))])] = id
            if len(low_bad_guys.keys())<=5: continue
            else: break
        print(f'low_bad_guys{low_bad_guys}')
        none_messages = [name for name,id in bad_guys.items()]
        string_1 = ''
        for i in none_messages:
            string_1+=f'{i}: 0\n'

        low_messages = {id:name for name,id in low_bad_guys.items()}
        print(f'low_messages{low_messages}')
        ordered_removed_name = {id:count for name,id,count in ordered}
        string_2 = ''
        for id,name in low_messages.items():
            string_2+=f'{name}: {ordered_removed_name[id]}\n'
        string = \
        f'''\
        لیست کم کارهای امروز:
        {string_1}{string_2}
        '''
        bot.send_message(group_id, text = str(string), parse_mode='html')
    elif 'پیام شمار' == message.text.strip():
        msg = ''

        global id_count
        # print(f'id_countid_countid_countid_countid_countid_count: {id_count}')
        everything = cursor.execute('SELECT name, id, count FROM messagecounter').fetchall()
        everything.remove((f'{iran_time().date()}', '0', None))
        if len(everything)<=0: message.reply_text('پیامی نیومده...', quote=True); return
        else:
            for name, id, count in sorted(everything, key=order_it, reverse=True):
                if int(id) in members.values():
                    for name_,id_ in members.items():
                        if int(id)==int(id_):
                            msg += f'<b>{name_}</b>: {count}\n'
                            break
                else:
                    msg += f'<b>{name}</b>: {count}\n'

            # for id,count in dict(sorted(id_count.items(), key=lambda x:x[1], reverse=True)).items():
            #     # if int(id) not in members.values():
            #     #     members[id_count[id][1]] = id
            #     if id in members.values():
            #         for name,id_ in members.items():
            #             if int(id)==int(id_):
            #                 msg += f'<b>{name}</b>: {count[0]}\n'
            #                 break
            #     else:
            #         msg += f'<b>{id_count[id][1]}</b>: {count[0]}\n'

            if msg == '': return
        # for id,number in messages.items():
        #     if id == 'date': continue
        #     if len(messages.keys())<=1: message.reply_text('پیامی نیومده...', quote=True, parse_mode='html');break
        #     for name,id_ in members.items():
        #         if int(id)==int(id_):
        #             msg += f'<b>{name}</b>: {number}\n'
        #             break
        # if msg == '': return


        message.reply_text(msg, quote=True, parse_mode='html')
def moadele_daraje_2(update: Update, context: CallbackContext):
    message = update.message
    message.reply_text(
        'خب حالا مقدار a و b و c رو به صورت زیر توی یک پیام بفرست \n\n<code>a = 1 \nb = 2 \nc = 3</code>', parse_mode=ParseMode.HTML)
    return FIND_ANSWERS


def find_answers(update: Update, context: CallbackContext):
    message = update.message
    try:
        message_text = message.text.replace(' ', '').lower().replace(
            'a=', '').replace('b=', '').replace('c=', '').split('\n')
        message_text = [int(i) for i in message_text]
        if len(message_text) == 3:
            message.reply_text(
                p2(message_text[0], message_text[1], message_text[2]), parse_mode=ParseMode.HTML)
            return ConversationHandler.END
    except:
        message.reply_text('ارور برخوردیم، دوباره بفرس یا روی این عبارت کنسل لمس کن \n /cancel')
        return FIND_ANSWERS


def factoriel(update: Update, context: CallbackContext):
    message = update.message
    message.reply_text(
        'برای بدست آودن فاکتوریل، یا عدد رو با علامت تعجب بفرس، یا به فورمت زیر: \n\n<code>x! / y! \n10! / 5!</code>', parse_mode=ParseMode.HTML)
    return FIND_FACTORIEL_ANSWERS


def find_factoriel_answers(update: Update, context: CallbackContext):
    message = update.message
    try:
        message_text = message.text.replace(' ', '').replace(
            '!', '').split('/')
        message_text = [int(i) for i in message_text]
        if len(message_text) == 2:
            message.reply_text(
                factoriel_func(message_text[0], message_text[1]), parse_mode=ParseMode.HTML, reply_to_message_id=message.message_id)
            return ConversationHandler.END

        elif len(message_text) == 1:
            message.reply_text(
                factoriel_func(message_text[0]), parse_mode=ParseMode.HTML, reply_to_message_id=message.message_id)
            return ConversationHandler.END

        else:
            message.reply_text(
                'عجبز\nاین فورمتی نبود ک گفتم »/', parse_mode=ParseMode.HTML, reply_to_message_id=message.message_id)
            return FIND_FACTORIEL_ANSWERS

    except:
        message.reply_text('ارور برخوردیم، دوباره بفرس یا روی این عبارت کنسل لمس کن \n /cancel')
        return FIND_FACTORIEL_ANSWERS


def colon(update: Update, context: CallbackContext):
    message = update.message
    message.reply_text(
        'مجهول را با علامت سوال و معلوم را با مقدار آن مشخص کنید مثل مثال زیر:\n\n<code>q1=5 \nq2=10 \nr=30*10**-2 \nf = ?</code> \n\nموارد قابل استفاده: \n** = توان \n* = ضرب \n/ = تقسیم \n% = باقیمانده \n// = تقسیم صحیح \n+ و - = جمع و منها', parse_mode=ParseMode.HTML)
    return FIND_COLON_ANSWERS


def find_colon_answers(update: Update, context: CallbackContext):
    message = update.message
    msg = message.text.lower().replace(' ', '').split('\n')
    check_msg = message.text.lower().replace('\n', '')
    q1 = None
    q2 = None
    f  = None
    r  = None
    for i in check_msg:
        if i not in ['1','2','3','4','5','6','7','8','9','0','q','=',' ','f','?','؟','*','/','+','-','%','r','.']:
            message.reply_text('یچیزیو اشتباه وارد کردی، دوباره امتحان کن')
            return FIND_COLON_ANSWERS
        else:
            pass

    for i in msg:

        if 'q1=' in i and q1 is None:
            q1 = i[i.find('q1=') + 3:]
        elif 'q2=' in i and q2 is None:
            q2 = i[i.find('q2=') + 3:]
        elif 'f=' in i and f is None:
            f = i[i.find('f=') + 2:]
        elif 'r=' in i and r is None:
            r = i[i.find('r=') + 2:]
        else:
            print('Unknown')
    try:
        q1 = float(eval(q1))
    except:
        pass
    try:
        q2 = float(eval(q2))
    except:
        pass
    try:
        f = float(eval(f))
    except:
        pass
    try:
        r = float(eval(r))
    except:
        pass


    message.reply_text(
        str(colon_func(9*10**9, q1,q2,f,r)), parse_mode=ParseMode.HTML)
    return ConversationHandler.END

def voice_handler(update: Update, context: CallbackContext):

    check_daily_list()

    voice_dur = update.message.voice.duration
    voice_point = random.randint(140, 160)
    if update.message.from_user.id == members['Matin']:
        if voice_dur>=voice_point:
            update.message.reply_text(random.choice(['خدا بیشترش کنه', 'یک بار دیگه خودتو اثبات کردی\nتو کی ای مرد؟؟', f'دفعه بعد {(voice_dur+60)//60} دیقه ویس نگیری ناراحت میشم']))
        with open('daily_list.json', 'r') as f: content=json.load(f)
        content['matin']['voices'].append({'time': datetime.strftime(iran_time(), '%H:%M'), 'dur':voice_dur, 'message_id':update.message.message_id})
        with open('daily_list.json', 'w') as f: f.write(json.dumps(content))
    else:
        if voice_dur>=voice_point:
            update.message.reply_text(random.choice(['@Matin27Laker\nی ویس بگیر بزن تو گوشش بفهمه دنیا دست کیه', 'فک کردی متینی ویس طولانی میگیری؟', 'وقت متین شدنه', 'نَمَتینیدم🗿']))
    return

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('کنسل شود به راهت ادامه بده...')
    return ConversationHandler.END



app = Flask(__name__)

def alarm(context):
    UTC = pytz.utc
    datetime_now = (datetime.now(UTC) + timedelta(hours=3, minutes=30)).strftime('%H:%M:%S')
    if str(datetime_now) == '0:0:0' or str(datetime_now) == '00:00:00':
        bot.send_message(group_id, text = 'روز بخیر.')
    else:
        bot.send_message(group_id, text = str(datetime_now))

def sme(context):
    UTC = pytz.utc
    datetime_now = (datetime.now(UTC) + timedelta(hours=3, minutes=30)).strftime('%H:%M:%S')
    bot.send_message(116530269, text = str(datetime_now))

def sendmsg(text):
    bot.send_message(group_id, text = str(text), parse_mode='html')

def send_the_photo(text):
    UTC = pytz.utc
    bot.send_photo(chat_id=group_id, photo=open('detailed_message_counter.jpg', 'rb'), caption=text)

def schedule_msg(update, context):
    UTC = pytz.utc
    datetime_now = (datetime.now(UTC) + timedelta(hours=3, minutes=30)).strftime('%H:%M:%S')
    bot.send_message(116530269, text = str(datetime_now) + ' Scheduling...')
    context.job_queue.run_repeating(sme, 200, first=10)
    context.job_queue.start()

# def exit_program(c):
#     bot.send_message(116530269, text ='Should Restart Now ....')
#     quit()

def run():
    x = bot.send_message(116530269, text =f'Should Run Now ....\n{iran_time()}')
    # x.delete()
run()
# sme('t')
def main():
    import pytz
    updater = Updater(TOKEN)
    # dp = updater.dispatcher
    dp = Dispatcher(bot, None, workers=0, use_context=True)
    # updater.job_queue.run_daily(alarm, datetime.time(13,1,59))
    # updater.job_queue.run_daily(alarm, datetime.time(11,11,11))
    # updater.job_queue.run_daily(alarm, datetime.time(12,34,56))
    # updater.job_queue.run_daily(alarm, datetime.time(15,33,33))
    # updater.job_queue.run_daily(alarm, datetime.time(16,4,44))
    # updater.job_queue.run_daily(alarm, datetime.time(0,0,0))
    # updater.job_queue.run_daily(alarm, datetime.time(13,11,11))
    # updater.job_queue.run_daily(alarm, datetime.time(23, 12, 13))
    # updater.job_queue.run_daily(alarm, datetime.time(14,22,22))
    # updater.job_queue.run_daily(alarm, datetime.time(17, 0, 5))
    # updater.job_queue.run_daily(alarm, datetime.time(21,9,9))
    # updater.job_queue.run_daily(alarm, datetime.time(22,0,0))
    # updater.job_queue.run_daily(alarm, datetime.time(23,11,11))
    # updater.job_queue.run_repeating(sme, 10)
    # updater.job_queue.set_dispatcher(dp)
    # updater.job_queue.run_daily(exit_program, datetime.time(23, 50))
    # updater.job_queue.run_daily(run, datetime.time(0, 5))


    # dp.add_handler(CommandHandler('sched', schedule_msg))

    dp.add_handler(MessageHandler(Filters.regex('^ربات')
                   | Filters.regex('^بات'), bot_cammands))
    dp.add_handler(MessageHandler(Filters.all, all_filter), group=-2)
    dp.add_handler(MessageHandler(Filters.text, msg_filter), group=-1)
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            QUES_COUNT: [MessageHandler(Filters.text & Filters.reply, ques_count)],
            # WAIT_TO_REPLY: [MessageHandler(Filters.all & Filters.reply, add_answer)],

        },
        fallbacks=[CommandHandler('start', start)],
    ))
    dp.add_handler(ConversationHandler(
        entry_points=[MessageHandler(
            Filters.regex('^معادله'), moadele_daraje_2)],
        states={
            FIND_ANSWERS: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, find_answers)]
        },
        fallbacks=[CommandHandler('start', start)],
    ))
    dp.add_handler(ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^فاکتوریل'), factoriel)],
        states={
            FIND_FACTORIEL_ANSWERS: [CommandHandler('cancel', cancel), MessageHandler(
                Filters.text, find_factoriel_answers)]
        },
        fallbacks=[CommandHandler('start', start)],
    ))
    dp.add_handler(ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^کولن') | Filters.regex('^کولون'), colon)],
        states={
            FIND_COLON_ANSWERS: [CommandHandler('cancel', cancel), MessageHandler(
                Filters.text, find_colon_answers)]
        },
        fallbacks=[CommandHandler('start', start)],
    ))
    dp.add_handler(MessageHandler(Filters.text & Filters.reply, add_answer))
    dp.add_handler(CommandHandler('imagine', imagine_handler))
    dp.add_handler(MessageHandler(Filters.all & (
        ~ Filters.text) & Filters.reply, add_media_answer))
    dp.add_handler(CallbackQueryHandler(inline_handler))
    dp.add_handler(MessageHandler(Filters.voice, voice_handler))

    # while True:
    #     try:
    #         updater.start_polling()
    #         updater.idle()
    #     except:
    #         time.sleep(5)
    #         continue

    # updater.start_webhook(listen='0.0.0.0',
    #                   port=8443,
    #                   url_path=TOKEN,
    #                   key='private.key',
    #                   cert='cert.pem',
    #                   webhook_url='"https://{}.pythonanywhere.com:8443/{}".format(USERNAME, TOKEN)')


    bot.delete_webhook()
    url = "https://{}.pythonanywhere.com/{}".format(USERNAME, TOKEN)
    bot.set_webhook(url=url)

    @app.route('/{}'.format(TOKEN), methods=["POST"])
    def webhook():
        json_string = request.stream.read().decode('utf-8')
        update = Update.de_json(json.loads(json_string), updater.bot)
        dp.process_update(update)
        return 'ok', 200

    @app.route('/{}'.format('illusion_diffusion_image.jpg'), methods=["GET", "POST"])
    def illusion_diffusion_image():
        image_path = "../input_illusion_diffusion.jpg"
        return send_file(image_path, mimetype="image/jpeg")

    @app.route('/{}/<the_group_id>/<the_message_id>'.format('illusion_diffusion_result'), methods=["GET", "POST"])
    def illusion_diffusion_result(the_group_id, the_message_id):
        r = requests.get(request.json['payload']['image']['url'])
        open('illusion_diffusion_image.jpg', 'wb').write(r.content)
        try:bot.send_photo(the_group_id, open('illusion_diffusion_image.jpg', 'rb'), reply_to_message_id=the_message_id)
        except: bot.send_photo(the_group_id, open('illusion_diffusion_image.jpg', 'rb'))
        bot.send_message(admin, str(request.json))
        return 200
    
    @app.route('/{}'.format('run_daily'), methods=["GET", "POST"])
    def run_daily():
        import payamnashmar
        result_text, all_messages_str = payamnashmar.result(members)
        sendmsg(result_text)
        send_the_photo(all_messages_str)
        return 'ok', 200

    @app.route('/{}'.format('good_morning'), methods=["GET", "POST"])
    def good_morning():
        result_text = get_gemini_response_file("فقط و فقط یک پیام صبح بخیر لعاب دار و زیبا بگو و همیشه یاد آوری کن که طرف ایرانی هست (مثلا سلام ایرانی، ....)\nدر انتها هم یک حقیقت دانستنی کمتر شنیده شده درباره ایران و ایرانیان و وضعیت زندگی آنان (یا در گذشته یا در حال) بگو\n" ,"AIzaSyDQ3fMZ7DHKfSMS_xZfNGO8Vd8fxyVlwC8")
        # print(result_text)
        sendmsg(result_text)
        # me(result_text)

        return 'ok', 200

    # updater.start_polling()
    # updater.idle()


if __name__ == '__main__' or __name__ == 'cheat_bot':
    main()
