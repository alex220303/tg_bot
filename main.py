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
    if message.text == '/start':
        markup = telebot.types.InlineKeyboardMarkup()
        btn2 = telebot.types.InlineKeyboardButton('Вывести главы', callback_data='getChapters')
        markup.add(btn2) 
        btn1 = telebot.types.InlineKeyboardButton('Перейти на Консультант Плюс', url='https://www.consultant.ru/document/cons_doc_LAW_8982/ba7190a7c7918e934967e929e796d726c2647382/')
        markup.add(btn1)

        bot.send_photo(message.chat.id, photo='https://www.advgazeta.ru/upload/iblock/139/semeynoe_zakonodatelstvo_ozhidayut_masshtabnye_popravki_1.jpg', caption='Семейный кодекс РФ Раздел II. ЗАКЛЮЧЕНИЕ И ПРЕКРАЩЕНИЕ БРАКА', reply_markup=markup)


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

        buttons.append(telebot.types.InlineKeyboardButton('Перейти на Консультант Плюс', url='https://www.consultant.ru/document/cons_doc_LAW_8982/ba7190a7c7918e934967e929e796d726c2647382/'))
        markup.row(buttons[-1])

        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption='Выберите главу, которую хотите увидеть', reply_markup=markup)
    
    elif call.data.startswith('chapter_'):
        chapter_index = int(call.data.split('_')[1])
        chapters = family.get_chapters()
        selected_chapter = chapters[chapter_index]
        
        articles = family.get_articles_for_chapter(selected_chapter)
        markup = create_article_buttons(articles, f'chapter_{chapter_index}')
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption='Выберите статью, которую хотите увидеть', reply_markup=markup)

    elif call.data.startswith('article_'):
        _article, _chapter = call.data.split('-')
        chapter_index = int(_chapter.split('_')[1])
        article_index = int(_article.split('_')[1])

        chapters = family.get_chapters()
        selected_chapter = chapters[chapter_index]

        articles = family.get_articles_for_chapter(selected_chapter)
        selected_article = articles[article_index]
        
        description, link = family.get_article_description_and_link(selected_chapter, selected_article)
        markup = create_article_buttons(articles, f'chapter_{chapter_index}')
        
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=f'{description}{link if link else ''}', parse_mode='html', reply_markup=markup)

def create_article_buttons(articles, chapter):
    markup = telebot.types.InlineKeyboardMarkup()
    buttons = []
    for i, article in enumerate(articles):
        buttons.append(telebot.types.InlineKeyboardButton(article, callback_data=f"article_{i}-{chapter}"))
        
        if i % 2:
            markup.row(buttons[i - 1], buttons[i])

    if len(articles) % 2:
        markup.row(buttons[-1])

    buttons.append(telebot.types.InlineKeyboardButton('Назад к главам', callback_data='getChapters'))
    markup.row(buttons[-1])

    return markup

        

def main():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()
