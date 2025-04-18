import logging
from telegram.ext import Application, MessageHandler, filters

Bot_token = "your-token-here"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def echo(update, context):
    await update.message.reply_text(f"Я получил сообщение {update.message.text}")

def main():
    application = Application.builder().token(Bot_token).build()
    text_handler = MessageHandler(filters.TEXT, echo)
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()