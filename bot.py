import config
import telebot
import apiai, json

bot = telebot.TeleBot(config.token)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('Привет', 'Пока', 'Хайль Гидра')

@bot.message_handler(commands = ['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup = keyboard1)

@bot.message_handler(commands = ['Хайль Гидра'])
def start_message(message):
	bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup = keyboard1)

@bot.message_handler(content_types = ['text'])
def send_text(message):
	request = apiai.ApiAI('bc05779f82f04e249c5d7011739abe62').text_request()
	request.lang = 'ru'

	request.session_id = 'TestBot'
	if message.text.lower() == 'привет':
		bot.send_message(message.chat.id, 'Привет, друг')
	elif message.text.lower() == 'пока':
		bot.send_message(message.chat.id, 'Прощай, Санек..')
	elif message.text.lower() == 'люблю':
		bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAMoXujAVuiydTSBFOD2suwkrPm49NUAAkgDAALGzGMCF5HWtlHzZjIaBA')
	else:
		request.query = message.text
		responseJson = json.loads(request.getresponse().read().decode('utf-8'))
		response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
		if response:
			bot.send_message(message.chat.id, response)
		else:
			bot.send_message(message.chat.id, 'Я вас не понял')

@bot.message_handler(content_types = ['sticker'])
def send_id_sticker(message):
	print(message)

bot.polling()
