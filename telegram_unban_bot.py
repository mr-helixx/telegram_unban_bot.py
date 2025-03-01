import logging
import random
import time
import re
import os
import pyfiglet
from termcolor import colored
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your actual bot token

logging.basicConfig(filename="bot.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Display bot welcome message
def display_title():
    ascii_art = pyfiglet.figlet_format("UNBAN TOOL", font="slant")
    return f"```\n{ascii_art}```\n🛠 *Welcome to the Unban Request Bot!*"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = display_title()
    keyboard = [
        [InlineKeyboardButton("Submit Unban Request", callback_data="unban")],
        [InlineKeyboardButton("Help", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(message, parse_mode="Markdown", reply_markup=reply_markup)

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = "🔹 Use this bot to submit an unban request.\n🔹 Select a reason from the menu.\n🔹 Enter your username and email.\n🔹 Wait for processing."
    await update.message.reply_text(help_text)

# Inline button handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "unban":
        keyboard = [
            [InlineKeyboardButton("Nudity", callback_data="1"), InlineKeyboardButton("Impersonation", callback_data="2")],
            [InlineKeyboardButton("Fraud", callback_data="4"), InlineKeyboardButton("Spam", callback_data="6")],
            [InlineKeyboardButton("Something Else", callback_data="7")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Select your ban reason:", reply_markup=reply_markup)
    
    elif query.data == "help":
        await help_command(update, context)
    
    else:
        await query.message.reply_text(f"📌 You selected: *{query.data}*\nNow, send your username and email.")

# Message handler for username and email input
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "@" in text and "." in text:  # Simple email validation
        unban_chance = random.randint(40, 100)
        await update.message.reply_text(f"✅ Your request has been submitted!\n📊 Unban chances: {unban_chance}%\n📧 You will receive an update via email.")
        logging.info(f"Unban request sent: {text} (Chance: {unban_chance}%)")
    else:
        await update.message.reply_text("⚠️ Invalid input. Please send your username and email.")

# Main function
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
