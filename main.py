import configparser
import telebot

# Чтение файла конфигурации
config = configparser.ConfigParser()
config.read('config.conf')

TOKEN = config['General']['token']
DEBUG_MODE = config.getboolean('General', 'debug_mode')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Здесь можно добавить логику обработки сообщений от пользователя
    # Например, анализ содержимого сообщения и предоставление соответствующей информации
    bot.reply_to(message, "Спасибо за твое сообщение. Я сейчас соберу информацию и верну тебе ответ.")

def main():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()
