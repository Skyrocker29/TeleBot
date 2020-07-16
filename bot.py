import config
import telebot
import apiai, json

bot = telebot.TeleBot(config.token)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('Привет', 'Работаем', 'Деньги_нужны', 'До_свидания')

@bot.message_handler(commands = ['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Слушай меня, слушай!', reply_markup = keyboard1)

@bot.message_handler(content_types = ['text'])
def send_text(message):
	request = apiai.ApiAI('bc05779f82f04e249c5d7011739abe62').text_request()
	request.lang = 'ru'

	request.session_id = 'TestBot'
	if message.text.lower() == 'привет':
		bot.send_message(message.chat.id, 'Как обстановка? Всё в порядке?')
	elif message.text.lower() == 'работаем':
		bot.send_message(message.chat.id, 'Помощь нужна? Часа хватит?')
	elif message.text.lower() == r'деньги_нужны':
		bot.send_sticker(message.chat.id, 'Как? Послушай меня, послушай! Деньги это грязь!')
	elif message.text.lower() == r'до_свидания':
		bot.send_sticker(message.chat.id, 'До завтра, мужики!')
	else:
		request.query = message.text
		responseJson = json.loads(request.getresponse().read().decode('utf-8'))
		response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
		if response:
			bot.send_message(message.chat.id, response)
		else:
			bot.send_message(message.chat.id, 'Ну что ты мне даешь епона мать?!')

#@bot.message_handler(content_types = ['sticker'])
def send_id_sticker(message):
	print(message)

bot.polling()
