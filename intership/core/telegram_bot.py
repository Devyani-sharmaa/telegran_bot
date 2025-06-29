import os
import sys
import django
from asgiref.sync import sync_to_async
from telegram.ext import ApplicationBuilder, CommandHandler

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intership.settings')
django.setup()

# Import Django model
from core.models import TelegramUser

# Save user to DB
@sync_to_async
def save_user(username):
    print(f"[DB] Saving user: {username}")
    TelegramUser.objects.get_or_create(username=username)

# /start command
async def start(update, context):
    print("[BOT] /start command received")
    username = update.effective_user.username
    print(f"[BOT] Username: {username}")
    if username:
        await save_user(username)
        await update.message.reply_text(f"Hi {username}, you're now registered!")
    else:
        await update.message.reply_text("Could not retrieve your username.")

# Run bot
def run_bot():
    from decouple import config
    TOKEN = config("TELEGRAM_BOT_TOKEN")  # ✅ Make sure .env has this

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("[BOT] Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    run_bot()
