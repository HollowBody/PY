from logging import getLogger

from telegram import Bot
from telegram import Update
from telegram import PhotoSize
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.ext import CallbackQueryHandler
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.utils.request import Request

#from archive_bot.db import init_db
#from archive_bot.db import add_message
#from archive_bot.db import count_messages
#from archive_bot.db import list_messages
#from echo.config import load_config
#from echo.utils import debug_requests


#config = load_config()

logger = getLogger(__name__)


GET_OFFER = 'offer'
GET_PRODUCT_INFO = 'info'
GET_MANUAL = 'manual'


def get_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Оформить каско', callback_data=GET_OFFER),],
            [InlineKeyboardButton(text='Информация о продукте', callback_data=GET_PRODUCT_INFO),],
            [InlineKeyboardButton(text='Инструкция', callback_data=GET_MANUAL),],
            ],)


#@debug_requests
def message_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    if user:
        name = user.first_name
    else:
        name = 'аноним'

    text = "Я телеграм-бот, который поможет тебе оформить страховку на автомобиль!\nВоспользуйся меню чтобы узнать подробности или перейти к оформлению!"
    reply_text = f'Привет, {name}!\n\n{text}'

    # Ответить пользователю
    update.message.reply_text(text=reply_text,
        reply_markup=get_keyboard(),)

    # Записать сообщение в БД
    if text:
        add_message(user_id=user.id,
            text=text,)


#@debug_requests
def callback_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    callback_data = update.callback_query.data

    if callback_data == GET_OFFER:
        text = f'Получение предложения, здесь будет новое меню с указанием марки модели и тд...'
    elif callback_data == GET_PRODUCT_INFO:
        text = f'Условия продукта страхования'
        photoLight = 'https://github.com/JRSY23/PY/blob/master/%D0%9B%D0%B0%D0%B9%D1%82.png?raw=true'
        photoOptimum = 'https://github.com/JRSY23/PY/blob/master/%D0%9E%D0%BF%D1%82%D0%B8%D0%BC%D1%83%D0%BC.png?raw=true'
    elif callback_data == GET_MANUAL:
        text = f'Инструкция \"Как пользоваться нашим ботом\" (Сделать ПДФ)'        
    else:
        text = 'Произошла ошибка'

    update.effective_message.reply_text(text=text,)
    if (photoLight!='' and photoOptimum !=''):
         update.effective_message.reply_photo(photo=photoLight,)
         update.effective_message.reply_photo(photo=photoOptimum,)
   


def main():
    logger.info('Start ArchiveBot')

    req = Request(connect_timeout=0.5,
        read_timeout=1.0,)
    bot = Bot(token='1201845137:AAHh2QcXRHAKcJ1HK7LVUroMlaRLSSYQj9s',
        request=req,
        base_url='https://telegg.ru/orig/bot',)
    updater = Updater(bot=bot,
        use_context=True,)

    # Проверить что бот корректно подключился к Telegram API
    info = bot.get_me()
    logger.info(f'Bot info: {info}')

    # Подключиться к СУБД
    #init_db()

    # Навесить обработчики команд
    updater.dispatcher.add_handler(MessageHandler(Filters.all, message_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))

    # Начать бесконечную обработку входящих сообщений
    updater.start_polling()
    updater.idle()
    logger.info('Stop ArchiveBot')


if __name__ == '__main__':
    main()