python
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai

# Устанавливаем API-ключи
telegram_bot_api_token = "6873716305:AAF4RBk8lPlNo1cOCIHdW9hAj21NDpkliSc"
openai_api_key = "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"

# Инициализируем Telegram бота и OpenAI API
updater = Updater(telegram_bot_api_token, use_context=True)
openai.api_key = openai_api_key

# Настройки логгирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Функция для обработки команды /start
def start(update, context):
    update.message.reply_text('Привет, я ваш помощник! Напишите мне что-нибудь, и я постараюсь на него ответить.')

# Функция для обработки всех сообщений пользователя
def echo(update, context):
    # Получаем текст сообщения пользователя
    user_input = update.message.text

    # Генерируем ответ с помощью OpenAI API
    response = openai.Completion.create(engine="davinci-codex", prompt=user_input, max_tokens=100)

    # Извлекаем текст ответа из JSON-ответа сервера ChatGPT
    ai_output = response.choices[0].text

    # Отправляем ответ пользователю
    update.message.reply_text(ai_output)

# Обработчик ошибок
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# Создаем обработчики сообщений для бота
start_handler = CommandHandler('start', start)
message_handler = MessageHandler(Filters.text & ~Filters.command, echo)
dispatcher = updater.dispatcher

# Добавляем обработчики сообщений в диспетчер
dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)

# Запуск бота
updater.start_polling()

# Запускаем бесконечный цикл для получения сообщений от пользователя
updater.idle()
