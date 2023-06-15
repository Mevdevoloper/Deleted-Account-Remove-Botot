import logging
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot, Update, URL


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define the bot token
BOT_TOKEN = '5811021488:AAHNTgLlQSEAmk57qYCqBuFiGvb8Vd8iuss'

# Create a bot instance
bot = Bot(token=BOT_TOKEN)

# Define the command handlers
def start(update: Update, context):
    """Handler for the /start command"""
    update.message.reply_text("I'm a Deleted Account Bot!")

def remove_deleted_accounts(update: Update, context):
    """Handler for the /remove_deleted command"""
    # Retrieve the list of members in the group
    chat_id = update.effective_chat.id
    members = bot.get_chat_members(chat_id)

    # Iterate through the members and check for deleted accounts
    for member in members:
        if member.user.is_deleted:
            # Remove the deleted account from the group
            bot.kick_chat_member(chat_id, member.user.id)

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
    dispatcher.add_handler(CommandHandler("remove_deleted", remove_deleted_accounts))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown_command))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
