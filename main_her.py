#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from predict_style import Predictor

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    if user:
        name = user.first_name
    else:
        name = 'Анонимус'
    update.message.reply_text('Hi, {}!'.format(name))
    update.message.reply_text(
      'asdfkglihojpkl[]')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def action(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Здесь будет экшн')
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)
    
def get_style(update, context):
    global option
    option = update.message.text
    update.message.reply_text('Good! Now input coef')
def get_coef(update, context):
    global coef
    coef = update.message.number
    update.message.reply_text('Good! Now send me a pic :)')
    
def get_photo(update, context):
    """Echo the user message."""
    user = update.message.from_user
    # get photo file
    photo_file = update.message.photo[-1].get_file()
    # save photo
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text('Nice! Got your photo, styling...')
    
    # load saved photo
    global coef
    # send photo
    global option
    predictor = Predictor()
    if option in ['1', '2', '3', '4', '5', '6']:
      predictor.get_image_predict('user_photo.jpg', option, int(coef))
       
    
    res_photo = open('res_photo.jpg', 'rb')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=res_photo)

def main():
    """Start the bot."""
    print('Start')
    updater = Updater("1247859285:AAHSu4GPAOFVrpA8ZB_dJUnibLuE3UbSio4", use_context=True)
        # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("action", action))

    # on noncommand i.e message - echo the message on Telegram
#     dp.add_handler(MessageHandler(Filters.text, get_style))
#     dp.add_handler(MessageHandler(Filters.text, get_coef))
#     dp.add_handler(MessageHandler(Filters.photo, get_photo))

    # on noncommand i.e message - echo the message on Telegram
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()
    print('Finish')

option = ""

if __name__ == '__main__':
    main()
