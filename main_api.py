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
import json
import logging
from numpy import sort
import numpy as np
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

Avail_rooms = json.loads(open("rooms.txt").read())
try:
    del Avail_rooms['NaN']
    del Avail_rooms['Saturday']
except:
    pass

bad_rooms = [' Zewail City New Camp, Nano Building, Room',
             ' Univ.of Sci & Tech, , Room',
             ' Zewail City New Camp, , Room',
             ' Univ.of Sci & Tech, Academic Building ZC2, Room',
             ' Zewail City New Camp, Service Building, Room']


try:
    for day in Avail_rooms.keys():
        for bad_r in bad_rooms:
            if bad_r in Avail_rooms[day].keys():
                del Avail_rooms[day][bad_r]         
except:
    pass

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update, context):
    """Send a message when the command /start is issued."""
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
    buttons = [[KeyboardButton(day) for day in days[:3]], [
        KeyboardButton(day) for day in days[3:]]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Choose the room!", reply_markup=ReplyKeyboardMarkup(buttons))

def transpose(list_of_lists):
    numpy_array = np.array(list_of_lists)
    transpose = numpy_array.T

    return transpose.tolist()

def messageHandler(update, context):
    print(str(update.message.text)[-3:])
    if update.message.text in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]:
        rooms = list(Avail_rooms[update.message.text].keys())
        rooms=sorted(rooms)
        rooms = [room.replace(" Zewail City New Camp, ","").replace("Room","").strip()+"\n"+str(update.message.text)[:3] for room in rooms if room !="NaN"]
        rooms+=["Back to days"]
        new_rooms=[[]]
        for i in range(len(rooms)):
            if i%2 ==0:
                new_rooms.append([])
            new_rooms[-1].append(KeyboardButton(rooms[i]))
        
        buttons = []
        context.bot.send_message(chat_id=update.effective_chat.id,
                                text="Welcome to my bot!", reply_markup=ReplyKeyboardMarkup(new_rooms))
    elif str(update.message.text)[-3:] in ["Sun", "Mon", "Tue", "Wed", "Thu"]:
        context.bot.send_message(chat_id=update.effective_chat.id,
                        text="Ok!")

    else:
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
        buttons = [[KeyboardButton(day) for day in days[:3]], [
            KeyboardButton(day) for day in days[3:]]]
        context.bot.send_message(chat_id=update.effective_chat.id,
                                text="Choose the room!", reply_markup=ReplyKeyboardMarkup(buttons))
        
def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        "", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, messageHandler))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
