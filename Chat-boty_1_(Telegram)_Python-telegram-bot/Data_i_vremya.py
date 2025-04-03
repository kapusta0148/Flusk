import logging
from telegram.ext import Application, CommandHandler
import datetime as dt

Bot_token = "your-token-here"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def time(update, context):
    await update.message.reply_text(dt.datetime.now().strftime("%H:%M"))

async def date(update, context):
    await update.message.reply_text(dt.datetime.now().strftime("%d.%m.%Y"))

def main():
    application = Application.builder().token(Bot_token).build()
    application.add_handler(CommandHandler("time", time))
    application.add_handler(CommandHandler("date", date))
    application.run_polling()


if __name__ == '__main__':
    main()