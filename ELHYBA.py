from mody import Mody
import telebot
import gdshortener
import requests
from user_agent import generate_user_agent
import re

token = Mody.ELHYBA  #توكن
bot = telebot.TeleBot(token)

cookies = {
    'AppSession': '6j35pliejibipiidgqr4kueuv1',
    'csrfToken': '75aa4558310672a8042cc16fcbcdffd5477b8d9c9bf46f91e401c5a532675602c645e04878c56f8ea172da3e837c27734014460b3b55dc1bbce8277162ada3c8',
    'sls': '0',
    'tmz': 'Asia/Jerusalem',
    'ref': 'admin',
    'ab': '2',
    '_ga_6QVVMFTPT3': 'GS1.1.1687605103.1.0.1687605103.0.0.0',
    '_ga': 'GA1.1.1737572540.1687605104',
}



headers = {
    'authority': 'za.gl',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://za.gl',
    'referer': 'https://za.gl/',
    'sec-ch-ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': generate_user_agent(),
    'x-requested-with': 'XMLHttpRequest',
}

@bot.message_handler(commands=['start'])
def Welcome(message):
 name = message.from_user.first_name
 keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
 keyboard.add(
        telebot.types.InlineKeyboardButton(text='is.gd', callback_data='1'),
        telebot.types.InlineKeyboardButton(text='za.gl', callback_data='2'),
        telebot.types.InlineKeyboardButton(text='v.ht', callback_data='3')
    )
    
 bot.reply_to(message,'''مرحبا {}
بوت اختصار روابط متعدد اختر ما يناسبك من الازرار .. )؛'''.format(name),reply_markup=keyboard)
 
@bot.callback_query_handler(func=lambda call:True)
def all(call):
 if call.data == '1':
  bot.send_message(call.message.chat.id,'ارسل الرابط لأقوم بأختصار بدومين is.gd')
  bot.register_next_step_handler(call.message, one)
 elif call.data == '2':
  bot.send_message(call.message.chat.id,'ارسل الرابط لأقوم بأختصار بدومين za.gl')
  bot.register_next_step_handler(call.message, two)
 elif call.data == '3':
  bot.send_message(call.message.chat.id,'ارسل الرابط لأقوم بأختصار بدويمن v.ht')
  bot.register_next_step_handler(call.message, three)
  
def one(message):
 if re.search("(?P<url>https?://[^\s]+)", message.text):
 	s = gdshortener.ISGDShortener()
 	a = s.shorten(message.text)[0]
 	bot.reply_to(message,a)
 else:
 	bot.reply_to(message,'sorry ,This is not a link URL')
 
def two(message):
	global cookies
	global headers
	
	data = {
	'_method': 'POST',
	'_csrfToken': '75aa4558310672a8042cc16fcbcdffd5477b8d9c9bf46f91e401c5a532675602c645e04878c56f8ea172da3e837c27734014460b3b55dc1bbce8277162ada3c8',
	'url': message.text,
	'ad_type': '2',
	'_Token[fields]': 'fba2ac211af3a04684cf7ffe3e6afdc452d7f50f%3Aad_type',
	'_Token[unlocked]': 'adcopy_challenge%7Cadcopy_response%7Ccoinhive-captcha-token%7Cg-recaptcha-response',
	}
	response = requests.post('https://za.gl/links/shorten',cookies=cookies,headers=headers, data=data).json()['url']
	if re.search("(?P<url>https?://[^\s]+)", message.text):
	   bot.reply_to(message,response)
	else:
		bot.reply_to(message, "sorry ,This is not a link URL")

def three(message):
 if re.search("(?P<url>https?://[^\s]+)", message.text):
 	url = f'https://v.ht/api.php?url='+message.text
 	req = requests.get(url).text
 	bot.reply_to(message,req)
 else:
 	bot.reply_to(message,'sorry ,This is not a link URL')


print('تم تطورير الملف بواسطة مودي الهيبه @ELHYBA')
bot.infinity_polling()