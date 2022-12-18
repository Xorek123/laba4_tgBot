import logging
import requests

from telegram import Update, ForceReply,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler,ContextTypes

TOKEN = "Токен"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("BTC", callback_data="BTC"),
            InlineKeyboardButton("ETH", callback_data="ETH"),
        ],
        [
            InlineKeyboardButton("DOGE", callback_data="DOGE"),
            InlineKeyboardButton("BNB", callback_data="BNB"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Цена крипты в долларах:", reply_markup=reply_markup)

def echo(update: Update, context: CallbackContext) -> None:
    data = update.message.text
    request = 'https://cryptingup.com/api/assets/'
    request += data
    try:
        info = requests.get(request).json()
        info = "Цена в долларах: " + str(info['asset']['quote']['USD']['price'])
        update.message.reply_text(info)
    except KeyError:
        update.message.reply_text("Такой крипты не существует")


def button(update: Update, context: ContextTypes) -> None:
    query = update.callback_query
    query.answer()
    request = 'https://cryptingup.com/api/assets/'
    request += query.data
    info = requests.get(request).json()
    info = "Цена в долларах: " + str(info['asset']['quote']['USD']['price'])
    query.edit_message_text(info)


def main() -> None:
    updater = Updater(TOKEN)#TOKEN

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

