import logging
from telegram.ext import Updater, CommandHandler
from telegram import ParseMode

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to store the channel ID
channel_id = None

def start(update, context):
    """Handler for the /start command."""
    update.message.reply_text('Welcome to the Channel Subscriber Bot!')

def set_channel(update, context):
    """Handler for the /setchannel command."""
    global channel_id
    channel_id = update.message.chat_id
    update.message.reply_text('Channel set successfully!')

def get_subscriber_count(update, context):
    """Handler for the /subscribers command."""
    global channel_id
    if channel_id:
        subscribers = context.bot.get_chat_members_count(channel_id)
        update.message.reply_text(f'The current subscriber count is: {subscribers}')
    else:
        update.message.reply_text('Please set the channel first using /setchannel')

def error(update, context):
    """Log errors."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # Set up the Telegram Bot token
    token = 'YOUR_TELEGRAM_BOT_TOKEN'
    
    # Create the Updater and pass it your bot's token
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('setchannel', set_channel))
    dp.add_handler(CommandHandler('subscribers', get_subscriber_count))

    # Log errors
    dp.add_error_handler(error)

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
