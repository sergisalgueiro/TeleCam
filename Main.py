# github.com/sergisalgueiro

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from time import sleep
import logging
import datetime
from random import randint, shuffle
import os


# Set up logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Conversation states
default = range(1)

# Define global vars
TOKEN = '457582840:AAEreJBalcgwJ4HAyvukOmmLlnPn42dzSH4'

go_away = 'https://images-na.ssl-images-amazon.com/images/I/51%2BvmGVtM6L._SL1001_.jpg'
# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.


def greeting_by_time(now):
    if 3 <= now.hour < 6:
        greeting = 'Bona Matinada '
    elif 6 <= now.hour < 12:
        greeting = 'Bon Mati '
    elif 12 <= now.hour < 15:
        greeting = 'Bon Migdia '
    elif 15 <= now.hour < 20:
        greeting = 'Bona tarda '
    elif 20 <= now.hour < 21:
        greeting = 'Bon Vespre '
    else:
        greeting = 'Bona nit '
    return greeting


def start(bot, update):
    """Send a message when the command /start is issued."""
    reply_keyboard = [['Vull el regal', 'No el vull', 'Veure fotos']]
    bot.send_chat_action(update.message.chat_id, 'typing')
    now = datetime.datetime.now()
    greeting = greeting_by_time(now)
    sleep(2)
    name = str(update.message.from_user.first_name)
    if name == 'Sergi':
        update.message.reply_text('Hola Amo!\n' + greeting,
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    else:
        update.message.reply_text(greeting + ': Invalid person.')
        bot.send_photo(chat_id=update.message.chat_id, photo=go_away)
        return exit_handler(bot, update)
    return default


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text('Benvingut, foto de gratis\nInici amb /start')
    bot.send_photo(chat_id=update.message.chat_id,
                   photo=fotos_array[randint(0, len(fotos_array) - 1)])
    sleep(10)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)



def exit_handler(bot, update):
    str_out = '/regal - desbloqueja el regal\n/eltemps - consulta la previsio del temps\n/pelis - busca pelis a IMDb' \
              '\n/cancel - surt del proces'
    update.message.reply_text(str_out, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())
    return exit_handler(bot, update)


def main():

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('regal', start), CommandHandler('eltemps', weather),
                      CommandHandler('pelis', pelis_bifurcacio), MessageHandler(Filters.text, other)],

        states={
            default: [RegexHandler('^(Vull el regal)$', regal), RegexHandler('^(No el vull)$', passos),
                    RegexHandler('^(Veure fotos)$', setup_foto), MessageHandler(Filters.text, other)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # on different commands - answer in Telegram
    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
	"""Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

	updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))

    main()
