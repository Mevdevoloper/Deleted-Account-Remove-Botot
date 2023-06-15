import logging
import os
import time
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define the bot token
BOT_TOKEN = os.getenv('5811021488:AAHNTgLlQSEAmk57qYCqBuFiGvb8Vd8iuss')
CHANNEL_USERNAME = os.getenv('CodeMasterTG')
ADMIN_ID = os.getenv('1848882121')

# Create a bot instance
bot = Bot(token=BOT_TOKEN)

# Define the command handlers
def start(update: Update, context):
    """Handler for the /start command"""
    user = update.effective_user
    if user:
        context.bot.send_message(chat_id=user.id, text="Welcome to the bot! Make sure to subscribe to the channel.")

def force_subscribe(update: Update, context):
    """Handler for the /force_subscribe command"""
    user = update.effective_user
    if user:
        if user.username in get_channel_subscribers():
            context.bot.send_message(chat_id=user.id, text="You are already subscribed to the channel.")
        else:
            context.bot.send_message(chat_id=user.id, text="Please subscribe to the channel first.")
            context.bot.send_message(chat_id=user.id, text=f"Click here to subscribe: t.me/{CHANNEL_USERNAME}")

def remove_deleted_accounts(update: Update, context):
    """Handler for the /remove_deleted command"""
    user = update.effective_user
    if user.id == int(ADMIN_ID):
        chat_id = update.effective_chat.id
        members = bot.get_chat_members(chat_id)
        deleted_accounts = []
        for member in members:
            if member.user.is_deleted:
                deleted_accounts.append(member.user.id)
        if deleted_accounts:
            bot.kick_chat_members(chat_id, deleted_accounts)
            context.bot.send_message(chat_id=user.id, text=f"Removed {len(deleted_accounts)} deleted accounts.")
        else:
            context.bot.send_message(chat_id=user.id, text="No deleted accounts found.")
    else:
        context.bot.send_message(chat_id=user.id, text="You are not authorized to use this command.")

def remove_inactive_accounts(update: Update, context):
    """Handler for the /remove_inactive command"""
    user = update.effective_user
    if user.id == int(ADMIN_ID):
        chat_id = update.effective_chat.id
        members = bot.get_chat_members(chat_id)
        inactive_accounts = []
        current_time = int(time.time())
        for member in members:
            last_seen_time = member.user.last_seen.date
            if last_seen_time and (current_time - last_seen_time) > 2592000:  # 30 days in seconds
                inactive_accounts.append(member.user.id)
        if inactive_accounts:
            bot.kick_chat_members(chat_id, inactive_accounts)
            context.bot.send_message(chat_id=user.id, text=f"Removed {len(inactive_accounts)} inactive accounts.")
        else:
            context.bot.send_message(chat_id=user.id, text="No inactive accounts found.")
    else:
        context.bot.send_message(chat_id=user.id, text="You are not authorized to use this command.")

def get_channel_subscribers():
    """Function to get the list of channel subscribers"""
    # Implement the logic to fetch the list of channel subscribers
    subscribers = ['username1', 'username2', 'username3']  # Replace with your actual logic
    return subscribers

def unknown_command(update: Update, context):
    """Handler for unknown commands"""
    update.message.reply_text("Sorry, I didn't understand that command.")

def main():
    """Main function to start the bot"""
    # Create an instance of the Updater
    updater = Updater(token=BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register the command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("force_subscribe", force_subscribe))
    dispatcher.add_handler(CommandHandler("remove_deleted", remove_deleted_accounts))
    dispatcher.add_handler(CommandHandler("remove_inactive", remove_inactive_accounts))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown_command))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
