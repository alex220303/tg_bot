import configparser
import telebot
from article import FamilyLawStructure

# Чтение файла конфигурации
config = configparser.ConfigParser()
config.read('config.conf')

TOKEN = config['General']['token']
DEBUG_MODE = config.getboolean('General', 'debug_mode')
bot = telebot.TeleBot(TOKEN)

family = FamilyLawStructure()

@bot.message_handler(content_types=['text'])
def start(message):
    if (message.text == '/start'):
        markup = telebot.types.InlineKeyboardMarkup()
        btn1 = telebot.types.InlineKeyboardButton('Перейти на Консультант Плюс', url='https://www.consultant.ru/document/cons_doc_LAW_8982/ba7190a7c7918e934967e929e796d726c2647382/')
        markup.add(btn1)
        btn2 = telebot.types.InlineKeyboardButton('Вывести главы', callback_data='getChapters')
        # btn3 = telebot.types.InlineKeyboardButton('Вывести статью', callback_data='writeArticle')
        markup.add(btn2) 
        bot.send_message(message.chat.id, 'Select buttons', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callbackMessage(call):
    if call.data == 'getChapters':
        chapters = family.get_chapters()

        markup = telebot.types.InlineKeyboardMarkup()
        buttons = []
        for i, chapter in enumerate(chapters):
            buttons.append(telebot.types.InlineKeyboardButton(chapter, callback_data=f"chapter_{i}"))
            
            if i % 2:
                markup.row(buttons[i - 1], buttons[i])

        if len(chapters) % 2:
            markup.row(buttons[-1])

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите главу, которую хотите увидеть', reply_markup=markup)
    
    elif call.data.startswith('chapter_'):
        chapter_index = int(call.data.split('_')[1])
        chapters = family.get_chapters()
        selected_chapter = chapters[chapter_index]
        
        # Здесь вы можете добавить логику для обработки выбора главы,
        # например, отправить сообщение с кнопками статей для этой главы
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Вы выбрали главу: {selected_chapter}')
        
        # Отправка сообщения с кнопками статей для выбранной главы
        articles = family.get_articles_for_chapter(selected_chapter)
        markup = create_article_buttons(articles)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите статью, которую хотите увидеть', reply_markup=markup)

    elif call.data.startswith('article_'):
        article_index = int(call.data.split('_')[1])
        chapters = family.get_chapters()
        selected_chapter = chapters[chapter_index]
        
        # Здесь вы можете добавить логику для обработки выбора главы,
        # например, отправить сообщение с кнопками статей для этой главы
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Вы выбрали главу: {selected_chapter}')
        
        # Отправка сообщения с кнопками статей для выбранной главы
        articles = family.get_articles_for_chapter(selected_chapter)
        markup = create_article_buttons(articles)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите статью, которую хотите увидеть', reply_markup=markup)

def create_article_buttons(articles):
    markup = telebot.types.InlineKeyboardMarkup()
    buttons = []
    for i, article in enumerate(articles):
        buttons.append(telebot.types.InlineKeyboardButton(article, callback_data=f"article_{i}"))
        
        if i % 2:
            markup.row(buttons[i - 1], buttons[i])

    if len(articles) % 2:
        markup.row(buttons[-1])

    return markup

        

def main():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()
