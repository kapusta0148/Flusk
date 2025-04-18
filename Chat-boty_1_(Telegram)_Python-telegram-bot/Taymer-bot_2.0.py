import logging
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update

Bot_token = "6996976499:AAFNBHJjKr3zoKLFoNhIWkOZAI5_GHkwnfM"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)


async def task(context: ContextTypes.DEFAULT_TYPE):
    """Выводит сообщение"""
    job = context.job
    await context.bot.send_message(job.chat_id, text=f'КУКУ! {job.data}с. прошли!')


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Удаляем задачу по имени. Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавляем задачу в очередь"""
    chat_id = update.effective_message.chat_id

    try:
        # Получаем время из аргумента команды
        due = float(context.args[0])
        if due < 0:
            await update.effective_message.reply_text('Время не может быть отрицательным!')
            return

        # Добавляем задачу в очередь и останавливаем предыдущую (если она была)
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(
            task,
            due,
            chat_id=chat_id,
            name=str(chat_id),
            data=due  # Передаем время как данные задачи
        )

        text = f'Вернусь через {due} с.!'
        if job_removed:
            text += ' Старая задача удалена.'
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text('Использование: /set_timer <секунды>')


async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаляет задачу, если пользователь передумал"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text)


def main():
    application = Application.builder().token(Bot_token).build()
    application.add_handler(CommandHandler("set_timer", set_timer))
    application.add_handler(CommandHandler("unset", unset))
    application.run_polling()


if __name__ == '__main__':
    main()