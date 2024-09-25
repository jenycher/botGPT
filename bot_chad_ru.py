import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from settings import BOT_TOKEN
from settings import CHAD_API_KEY

# Ключи для доступа
TELEGRAM_API_KEY = BOT_TOKEN
CHAD_API_KEY = CHAD_API_KEY
CHAD_API_URL = 'https://ask.chadgpt.ru/api/public/gpt-4o-mini'

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Приветственное сообщение
async def start(update: Update, context):
    await update.message.reply_text('Привет! Я бот, использующий ChadGPT. Задай свой вопрос.')

# Обработка ошибок
def handle_error(update: Update, context):
    logger.error(f'Произошла ошибка: {context.error}')

# Функция для обращения к ChadGPT API
def get_chadgpt_response(message):
    request_json = {
        "message": message,
        "api_key": CHAD_API_KEY
    }
    try:
        response = requests.post(url=CHAD_API_URL, json=request_json)
        if response.status_code == 200:
            resp_json = response.json()
            if resp_json['is_success']:
                return resp_json['response']
            else:
                return f"Ошибка: {resp_json['error_message']}"
        else:
            return f"Ошибка HTTP: {response.status_code}"
    except Exception as e:
        return f"Ошибка запроса: {str(e)}"

# Обработка сообщений пользователя
async def handle_message(update: Update, context):
    user_message = update.message.text
    response_message = get_chadgpt_response(user_message)
    await update.message.reply_text(response_message)

# Основная функция запуска бота
def main():
    # Инициализация приложения
    application = ApplicationBuilder().token(TELEGRAM_API_KEY).build()

    # Команды и обработчики
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Обработка ошибок
    application.add_error_handler(handle_error)

    # Запуск бота (polling)
    application.run_polling()  # Запускаем опрос (polling) и обрабатываем входящие сообщения

if __name__ == '__main__':
    main()