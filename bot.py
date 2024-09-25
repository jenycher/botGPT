import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import openai
from settings import BOT_TOKEN
from settings import OPENAI_API_KEY
from settings import OPENAI_ORG

import os

# Установите ваш API-ключ OpenAI
openai.api_key = OPENAI_API_KEY
openai.organization=OPENAI_ORG


# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Функция приветственного сообщения
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я бот, использующий ChatGPT. Задайте мне любой вопрос!")

# Функция для обработки сообщений пользователя
async def handle_message(update: Update, context):
    user_message = update.message.text

    # Отправляем запрос к ChatGPT
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-0125",  # или "gpt-4", если у вас доступ
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ]
        )
        bot_response = response['choices'][0]['message']['content']
    except Exception as e:
        bot_response = f"Произошла ошибка при обращении к ChatGPT: {str(e)}"  # Вывод текста ошибки

    # Отправляем ответ обратно пользователю
    await update.message.reply_text(bot_response)

# Обработка ошибок
async def error_handler(update: Update, context):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте снова.")

# Основная функция запуска бота
def main():
    telegram_token = BOT_TOKEN

    # Создаем приложение бота
    application = Application.builder().token(telegram_token).build()

    # Добавляем обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Добавляем обработчик ошибок
    application.add_error_handler(error_handler)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
