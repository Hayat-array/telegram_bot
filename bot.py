# # # import os
# # # import logging
# # # from dotenv import load_dotenv
# # # from datetime import datetime
# # # from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# # # from telegram.ext import (
# # #     Application,
# # #     CommandHandler,
# # #     MessageHandler,
# # #     CallbackQueryHandler,
# # #     ContextTypes,
# # #     filters,
# # # )

# # # # ==================== CONFIGURATION ====================
# # # # Load .env file (if present) so environment variables are available
# # # load_dotenv()

# # # # SECURITY FIX: Load token from environment variable
# # # BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8265225093:AAEbddlVpDJBcOqNUJYWb0hNfO8BgGBuhLw")
# # # AI_API_KEY = os.getenv("AI_API_KEY", "")

# # # # Setup logging
# # # logging.basicConfig(
# # #     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
# # #     level=logging.INFO
# # # )
# # # logger = logging.getLogger(__name__)

# # # # Log whether AI key is present (do NOT log the key itself)
# # # if AI_API_KEY:
# # #     logger.info("AI API key loaded from environment")
# # # else:
# # #     logger.info("AI API key NOT found in environment")

# # # # Store user stats and conversation history
# # # user_stats = {}
# # # conversation_history = {}


# # # # ==================== AI INTEGRATION ====================
# # # async def get_ai_response(user_id: int, user_message: str) -> str:
# # #     """Get AI response using the API key with conversation context"""
# # #     if not AI_API_KEY:
# # #         return "I'm not configured for AI responses yet. Please add an API key."
    
# # #     try:
# # #         import requests
        
# # #         # Build conversation history for context
# # #         if user_id not in conversation_history:
# # #             conversation_history[user_id] = []
        
# # #         # Keep only last 10 messages for context
# # #         if len(conversation_history[user_id]) > 10:
# # #             conversation_history[user_id] = conversation_history[user_id][-10:]
        
# # #         # System prompt guiding the assistant
# # #         system_content = (
# # #             "You are a helpful, friendly, and concise assistant. "
# # #             "Answer the user's question directly, be specific, and ask for clarification if needed."
# # #         )

# # #         messages = [
# # #             {"role": "system", "content": system_content}
# # #         ]

# # #         # Add history
# # #         for msg in conversation_history[user_id]:
# # #             messages.append(msg)

# # #         # Add current user message
# # #         messages.append({"role": "user", "content": user_message})

# # #         headers = {
# # #             "Authorization": f"Bearer {AI_API_KEY}",
# # #             "Content-Type": "application/json"
# # #         }

# # #         data = {
# # #             "model": "gpt-3.5-turbo",
# # #             "messages": messages,
# # #             "max_tokens": 200,
# # #             "temperature": 0.7,
# # #             "top_p": 0.9
# # #         }

# # #         logger.info(f"Sending AI request for user {user_id}: {user_message[:60]}")

# # #         response = requests.post(
# # #             "https://api.bluesminds.com/v1/chat/completions",
# # #             headers=headers,
# # #             json=data,
# # #             timeout=15
# # #         )

# # #         if response.status_code == 200:
# # #             result = response.json()
# # #             ai_response = result['choices'][0]['message']['content']

# # #             # Store conversation
# # #             conversation_history[user_id].append({"role": "user", "content": user_message})
# # #             conversation_history[user_id].append({"role": "assistant", "content": ai_response})

# # #             return ai_response

# # #         elif response.status_code == 401:
# # #             logger.error("Invalid AI API key")
# # #             return "❌ AI authentication failed. Please check the API key."

# # #         elif response.status_code == 429:
# # #             logger.warning("AI rate limited")
# # #             return "⏱️ AI rate limit reached. Try again shortly."

# # #         else:
# # #             logger.warning(f"AI API error {response.status_code}: {response.text[:200]}")
# # #             return "🤔 I'm having trouble thinking. Try again later!"

# # #     except Exception as e:
# # #         logger.error(f"AI request exception: {e}")
# # #         return "⚠️ AI service error. Please try again later."

# # # # ==================== COMMAND HANDLERS ====================
# # # async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# # #     """Handle /start command"""
# # #     user = update.effective_user
# # #     user_stats[user.id] = user_stats.get(user.id, 0) + 1
    
# # #     keyboard = [
# # #         [InlineKeyboardButton("📖 Help", callback_data='help')],
# # #         [InlineKeyboardButton("📊 Stats", callback_data='stats')],
# # #         [InlineKeyboardButton("📢 Send Story Reply", callback_data='story')]
# # #     ]
# # #     reply_markup = InlineKeyboardMarkup(keyboard)
    
# # #     welcome_text = f"""
# # # 👋 Hello {user.first_name}!

# # # Welcome to **MRM78 Bot** 🤖

# # # I can help you with:
# # # ✅ Auto-reply to your story reactions
# # # ✅ Analyze photos with AI
# # # ✅ Chat with you
# # # ✅ And more!

# # # Choose an option below or just send me a message:
# # #     """

# # #     await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
# # #     logger.info(f"User {user.first_name} ({user.id}) started the bot")

# # # async def story_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# # #     """Handle /story command - set up auto-reply"""
# # #     user = update.effective_user
    
# # #     if user.id not in user_stats:
# # #         user_stats[user.id] = 0
    
# # #     context.user_data['story_autoreply'] = True
    
# # #     story_text = """
# # # ✅ **Story Auto-Reply Enabled!**

# # # When someone reacts to your story, I'll send them:
# # # "👋 Thanks for watching my story! 😊"

# # # You can customize this message by sending:
# # # /setstoryreply <your custom message>
# # #     """
    
# # #     await update.message.reply_text(story_text, parse_mode='Markdown')
# # #     logger.info(f"Story autoreply enabled for user {user.id}")


# # # async def setstoryreply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# # #     """Set a custom story auto-reply message for the user"""
# # #     user = update.effective_user
# # #     text = ' '.join(context.args or [])
# # #     if not text:
# # #         await update.message.reply_text(
# # #             "Usage: /setstoryreply <your custom message>",
# # #             parse_mode='Markdown'
# # #         )
# # #         return

# # #     # store in user_data for persistence during runtime
# # #     context.user_data['story_reply_custom'] = text
# # #     await update.message.reply_text(
# # #         f"✅ Custom story reply set to:\n{text}",
# # #         parse_mode='Markdown'
# # #     )
# # #     logger.info(f"User {user.id} set custom story reply")

# # # async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# # #     """Handle /about command"""
# # #     ai_status = "✅ Enabled (Using AI!)" if AI_API_KEY else "❌ Disabled"
    
# # #     about_text = f"""
# # # ℹ️ **About MRM78 Bot**

# # # Version: 2.0
# # # Created: 2026
# # # Author: MRM78

# # # **Features:**
# # # ✨ Intelligent auto-replies
# # # 🤖 AI-powered responses
# # # 📱 Story reaction management
# # # 💡 Smart features

# # # **AI Status**: {ai_status}
# # # Powered by python-telegram-bot & Bluesminds API
# # #     """
    
# # #     await update.message.reply_text(about_text, parse_mode='Markdown')

# # # async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# # #     """Handle /stop command"""
# # #     await update.message.reply_text(
# # #         "👋 Bot stopped. Use /start to activate again.",
# # #         parse_mode='Markdown'
# # #     )

# # # async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# # #     """Handle /ai command - Show AI status"""
# # #     if not AI_API_KEY:
# # #         ai_text = """
# # # 🤖 **AI Status**: ❌ NOT CONFIGURED

# # # To enable AI responses:
# # # 1. Get an API key from Bluesminds or OpenAI
# # # 2. Add it to the `.env` file:
# # #    ```
# # #    AI_API_KEY=your_key_here
# # #    ```
# # # 3. Restart the bot

# # # Once enabled, I'll use AI to give smarter responses! 🧠
# # #         """
# # #     else:
# # #         ai_text = """
# # # 🤖 **AI Status**: ✅ ACTIVE

# # # Your bot is now using AI to power responses!

# # # **Features:**
# # # ✨ Smart contextual replies
# # # 💭 Natural conversations
# # # 🎯 Better understanding of requests
# # # 🚀 Continuous learning

# # # Try asking me anything! I'll use AI to help you.
# # #         """
    
# # #     await update.message.reply_text(ai_text, parse_mode='Markdown')

# # # async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# # #     """Clear conversation history for this user"""
# # #     user_id = update.effective_user.id
# # #     if user_id in conversation_history:
# # #         conversation_history[user_id] = []
# # #         await update.message.reply_text(
# # #             "🧹 Conversation history cleared! Starting fresh! 🆕",
# # #             parse_mode='Markdown'
# # #         )
# # #         logger.info(f"Cleared history for user {user_id}")
# # #     else:
# # #         await update.message.reply_text(
# # #             "✅ No history to clear!",
# # #             parse_mode='Markdown'
# # #         )

# # # async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# # #     """Test AI connection"""
# # #     if not AI_API_KEY:
# # #         await update.message.reply_text(
# # #             "❌ No API key configured!",
# # #             parse_mode='Markdown'
# # #         )
# # #         return
    
# # #     user_id = update.effective_user.id
# # #     await update.message.reply_text("🧪 Testing AI connection...", parse_mode='Markdown')
    
# # #     test_response = await get_ai_response(user_id, "Say hello!")
    
# # #     if test_response.startswith("❌") or test_response.startswith("⚠️"):
# # #         await update.message.reply_text(
# # #             f"❌ **Test Failed**\n{test_response}",
# # #             parse_mode='Markdown'
# # #         )
# # #     else:
# # #         await update.message.reply_text(
# # #             f"✅ **AI Connection Working!**\n\nBot said: {test_response}",
# # #             parse_mode='Markdown'
# # #         )


# # # async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
# # #     """Handle inline button callbacks from the welcome menu"""
# # #     query = update.callback_query
# # #     await query.answer()
# # #     data = query.data
# # #     # Create a minimal update wrapper so command handlers expecting
# # #     # `update.message` or `update.effective_user` work when called
# # #     class _MiniUpdate:
# # #         pass

# # #     mini = _MiniUpdate()
# # #     mini.message = query.message
# # #     # prefer callback sender if available
# # #     mini.effective_user = query.from_user or (query.message.from_user if query.message else None)

# # #     try:
# # #         if data == 'help':
# # #             await help_command(mini, context)
# # #         elif data == 'stats':
# # #             await stats_command(mini, context)
# # #         elif data == 'story':
# # #             await story_command(mini, context)
# # #         else:
# # #             # Fallback: reply to the message attached to the callback
# # #             if query.message:
# # #                 await query.message.reply_text("⚠️ Unknown action")
# # #             else:
# # #                 await query.answer(text="⚠️ Unknown action", show_alert=True)
# # #     except Exception as e:
# # #         logger.exception(f"Error handling callback '{data}': {e}")
# # #         # respond so the user knows something went wrong
# # #         if query.message:
# # #             await query.message.reply_text("❌ An error occurred handling that button. Try again.")
# # #         else:
# # #             await query.answer(text="❌ An error occurred. Try again.", show_alert=True)

# # # # ==================== MESSAGE HANDLERS ====================
# # # async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
# # #     """Handle incoming text messages"""
# # #     user = update.effective_user
# # #     user_text = update.message.text
    
# # #     # Track stats
# # #     if user.id not in user_stats:
# # #         user_stats[user.id] = 0
# # #     user_stats[user.id] += 1
    
# # #     logger.info(f"User {user.id} sent: {user_text}")
    
# # #     # Show typing indicator
# # #     await context.bot.send_chat_action(
# # #         chat_id=update.effective_chat.id, 
# # #         action="typing"
# # #     )
    
# # #     # Get AI response if API key is configured
# # #     if AI_API_KEY:
# # #         reply = await get_ai_response(user.id, user_text)
# # #         # AI responses may contain characters that break Markdown formatting;
# # #         # send AI replies without forcing Markdown parsing.
# # #         await update.message.reply_text(reply)
# # #         return
# # #     else:
# # #         # Fallback to smart replies if no AI
# # #         if any(keyword in user_text.lower() for keyword in ['hello', 'hi', 'hey']):
# # #             reply = f"👋 Hey {user.first_name}! How can I help you?"
        
# # #         elif any(keyword in user_text.lower() for keyword in ['how are you', 'how are you?', 'how you doing']):
# # #             reply = "😊 I'm doing great! Thanks for asking. How can I assist you today?"
        
# # #         elif any(keyword in user_text.lower() for keyword in ['thanks', 'thank you', 'thx']):
# # #             reply = "You're welcome! 🙏 Is there anything else I can help with?"
        
# # #         elif any(keyword in user_text.lower() for keyword in ['time', 'what time']):
# # #             current_time = datetime.now().strftime('%H:%M:%S')
# # #             reply = f"⏰ Current time: {current_time}"
        
# # #         else:
# # #             # Default response
# # #             reply = f"You said: **{user_text}**\n\nThanks for your message! 😊"
    
# # #     await update.message.reply_text(reply, parse_mode='Markdown')

# # # async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
# # #     """Handle incoming photos"""
# # #     user = update.effective_user
# # #     user_stats[user.id] = user_stats.get(user.id, 0) + 1
    
# # #     response = f"""
# # # 📸 **Nice photo, {user.first_name}!**

# # # I've received your image. Here's what I can do:
# # # ✅ Analyze with AI vision
# # # ✅ Extract text (OCR)
# # # ✅ Detect objects
# # # ✅ Describe content

# # # Use /help to see all features!
# # #     """
    
# # #     await update.message.reply_text(response, parse_mode='Markdown')
# # #     logger.info(f"User {user.id} sent a photo")

# # # async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
# # #     """Handle incoming stickers"""
# # #     user = update.effective_user
# # #     user_stats[user.id] = user_stats.get(user.id, 0) + 1
    
# # #     await update.message.reply_text("😄 Cool sticker! Keep the conversation going! 🎉")

# # # async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
# # #     """Handle errors"""
# # #     logger.error(f"Exception while handling an update: {context.error}")
    
# # #     if isinstance(update, Update) and update.effective_message:
# # #         await update.effective_message.reply_text(
# # #             "❌ Oops! An error occurred. Please try again later."
# # #         )

# # # async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# # #     """Handle /help command"""
# # #     help_text = """
# # # 📚 **Available Commands:**

# # # /start - Start the bot
# # # /help - Show this help message
# # # /stats - View your statistics
# # # /story - Enable story auto-reply
# # # /ai - Check AI status & setup
# # # /test - Test AI connection
# # # /clear - Clear conversation history
# # # /about - About this bot
# # # /stop - Stop the bot

# # # **Features:**
# # # 🤖 AI Responses - Smart AI-powered answers
# # # 🖼️ Photo Analysis - Send a photo for AI analysis
# # # 💬 Chat - Just send me a message!
# # #     """
# # #     await update.message.reply_text(help_text, parse_mode='Markdown')


# # # async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# # #     """Handle /stats command"""
# # #     user = update.effective_user
# # #     count = user_stats.get(user.id, 0)
# # #     stats_text = f"""
# # # 📊 **Your Statistics:**
# # # 👤 User ID: {user.id}
# # # 👨 Name: {user.first_name}
# # # 💬 Messages: {count}
# # # ⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# # #     """
# # #     await update.message.reply_text(stats_text, parse_mode='Markdown')

# # # # ==================== MAIN FUNCTION ====================
# # # def main():
# # #     """Start the bot"""
# # #     try:
# # #         # Create application
# # #         app = Application.builder().token(BOT_TOKEN).build()
        
# # #         # Add command handlers
# # #         app.add_handler(CommandHandler("start", start_command))
# # #         app.add_handler(CommandHandler("help", help_command))
# # #         app.add_handler(CommandHandler("stats", stats_command))
# # #         app.add_handler(CommandHandler("story", story_command))
# # #         app.add_handler(CommandHandler("about", about_command))
# # #         app.add_handler(CommandHandler("ai", ai_command))
# # #         app.add_handler(CommandHandler("stop", stop_command))
# # #         app.add_handler(CommandHandler("clear", clear_command))
# # #         app.add_handler(CommandHandler("test", test_command))
# # #         app.add_handler(CommandHandler("setstoryreply", setstoryreply_command))

# # #         # Callback handler for inline buttons
# # #         app.add_handler(CallbackQueryHandler(callback_query_handler))
        
# # #         # Add message handlers
# # #         app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
# # #         app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
# # #         app.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))
        
# # #         # Add error handler
# # #         app.add_error_handler(error_handler)
        
# # #         logger.info("🤖 Bot started successfully!")
# # #         print("🤖 Bot is running... Press Ctrl+C to stop")
# # #         print("=" * 50)
        
# # #         # Start polling (synchronous call, blocks until interrupted)
# # #         app.run_polling(allowed_updates=Update.ALL_TYPES)
        
# # #     except KeyboardInterrupt:
# # #         logger.info("Bot stopped by user")
# # #         print("\n👋 Bot stopped gracefully")
# # #     except Exception as e:
# # #         logger.error(f"Fatal error: {e}")
# # #         print(f"\n❌ Error: {e}")
# # #         raise

# # # if __name__ == "__main__":
# # #     main()
# # import os
# # import logging
# # from dotenv import load_dotenv
# # from datetime import datetime
# # import requests
# # from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# # from telegram.ext import (
# #     Application,
# #     CommandHandler,
# #     MessageHandler,
# #     CallbackQueryHandler,
# #     ContextTypes,
# #     filters,
# # )

# # # ==================== CONFIGURATION ====================
# # load_dotenv()

# # BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# # AI_API_KEY = os.getenv("AI_API_KEY", "")
# # NUMVERIFY_API_KEY = os.getenv("NUMVERIFY_API_KEY", "")

# # if not BOT_TOKEN:
# #     raise RuntimeError("TELEGRAM_BOT_TOKEN not set in environment / .env file")

# # logging.basicConfig(
# #     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
# #     level=logging.INFO
# # )
# # logger = logging.getLogger(__name__)

# # if AI_API_KEY:
# #     logger.info("AI API key loaded from environment")
# # else:
# #     logger.info("AI API key NOT found in environment")

# # if NUMVERIFY_API_KEY:
# #     logger.info("Numverify API key loaded from environment")
# # else:
# #     logger.info("Numverify API key NOT found in environment")

# # user_stats = {}
# # conversation_history = {}


# # # ==================== AI INTEGRATION ====================
# # async def get_ai_response(user_id: int, user_message: str) -> str:
# #     if not AI_API_KEY:
# #         return "I'm not configured for AI responses yet. Please add an API key."

# #     try:
# #         if user_id not in conversation_history:
# #             conversation_history[user_id] = []

# #         if len(conversation_history[user_id]) > 10:
# #             conversation_history[user_id] = conversation_history[user_id][-10:]

# #         system_content = (
# #             "You are a helpful, friendly, and concise assistant. "
# #             "Answer the user's question directly, be specific, and ask for clarification if needed."
# #         )

# #         messages = [{"role": "system", "content": system_content}]
# #         messages.extend(conversation_history[user_id])
# #         messages.append({"role": "user", "content": user_message})

# #         headers = {
# #             "Authorization": f"Bearer {AI_API_KEY}",
# #             "Content-Type": "application/json"
# #         }

# #         data = {
# #             "model": "gpt-3.5-turbo",
# #             "messages": messages,
# #             "max_tokens": 200,
# #             "temperature": 0.7,
# #             "top_p": 0.9
# #         }

# #         logger.info(f"Sending AI request for user {user_id}: {user_message[:60]}")

# #         response = requests.post(
# #             "https://api.bluesminds.com/v1/chat/completions",
# #             headers=headers,
# #             json=data,
# #             timeout=15
# #         )

# #         if response.status_code == 200:
# #             result = response.json()
# #             ai_response = result['choices'][0]['message']['content']

# #             conversation_history[user_id].append({"role": "user", "content": user_message})
# #             conversation_history[user_id].append({"role": "assistant", "content": ai_response})

# #             return ai_response

# #         elif response.status_code == 401:
# #             logger.error("Invalid AI API key")
# #             return "❌ AI authentication failed. Please check the API key."

# #         elif response.status_code == 429:
# #             logger.warning("AI rate limited")
# #             return "⏱️ AI rate limit reached. Try again shortly."

# #         else:
# #             logger.warning(f"AI API error {response.status_code}: {response.text[:200]}")
# #             return "🤔 I'm having trouble thinking. Try again later!"

# #     except Exception as e:
# #         logger.error(f"AI request exception: {e}")
# #         return "⚠️ AI service error. Please try again later."


# # # ==================== NUMVERIFY INTEGRATION ====================
# # async def check_phone_number(phone_number: str) -> dict:
# #     """Validate a phone number using the numverify API"""
# #     try:
# #         response = requests.get(
# #             "http://apilayer.net/api/validate",
# #             params={
# #                 "access_key": NUMVERIFY_API_KEY,
# #                 "number": phone_number,
# #                 "format": 1
# #             },
# #             timeout=10
# #         )
# #         return response.json()
# #     except Exception as e:
# #         logger.error(f"Numverify request exception: {e}")
# #         return {"error": str(e)}


# # async def validatephone_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     """Handle /validatephone command"""
# #     if not NUMVERIFY_API_KEY:
# #         await update.message.reply_text(
# #             "❌ Numverify API key not configured. Add NUMVERIFY_API_KEY to your .env file.",
# #             parse_mode='Markdown'
# #         )
# #         return

# #     if not context.args:
# #         await update.message.reply_text(
# #             "Usage: /validatephone <number with country code>\nExample: /validatephone +14158586273",
# #             parse_mode='Markdown'
# #         )
# #         return

# #     number = context.args[0]
# #     await update.message.reply_text("🔎 Checking number...", parse_mode='Markdown')

# #     result = await check_phone_number(number)

# #     if result.get("error"):
# #         await update.message.reply_text(f"⚠️ Error checking number: {result['error']}")
# #         return

# #     if result.get("valid"):
# #         text = (
# #             f"✅ **Valid Number**\n\n"
# #             f"📞 Number: {result.get('international_format', number)}\n"
# #             f"🌍 Country: {result.get('country_name', 'N/A')}\n"
# #             f"📡 Carrier: {result.get('carrier', 'N/A')}\n"
# #             f"📶 Line Type: {result.get('line_type', 'N/A')}\n"
# #             f"📍 Location: {result.get('location', 'N/A')}"
# #         )
# #     else:
# #         text = "❌ **Invalid number.** Please check the format and include the country code (e.g. +1...)."

# #     await update.message.reply_text(text, parse_mode='Markdown')


# # # ==================== COMMAND HANDLERS ====================
# # async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     user = update.effective_user
# #     user_stats[user.id] = user_stats.get(user.id, 0) + 1

# #     keyboard = [
# #         [InlineKeyboardButton("📖 Help", callback_data='help')],
# #         [InlineKeyboardButton("📊 Stats", callback_data='stats')],
# #         [InlineKeyboardButton("📢 Send Story Reply", callback_data='story')]
# #     ]
# #     reply_markup = InlineKeyboardMarkup(keyboard)

# #     welcome_text = f"""
# # 👋 Hello {user.first_name}!

# # Welcome to **MRM78 Bot** 🤖

# # I can help you with:
# # ✅ Auto-reply to your story reactions
# # ✅ Analyze photos with AI
# # ✅ Validate phone numbers
# # ✅ Chat with you
# # ✅ And more!

# # Choose an option below or just send me a message:
# #     """

# #     await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
# #     logger.info(f"User {user.first_name} ({user.id}) started the bot")


# # async def story_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     user = update.effective_user

# #     if user.id not in user_stats:
# #         user_stats[user.id] = 0

# #     context.user_data['story_autoreply'] = True

# #     story_text = """
# # ✅ **Story Auto-Reply Enabled!**

# # When someone reacts to your story, I'll send them:
# # "👋 Thanks for watching my story! 😊"

# # You can customize this message by sending:
# # /setstoryreply <your custom message>
# #     """

# #     await update.message.reply_text(story_text, parse_mode='Markdown')
# #     logger.info(f"Story autoreply enabled for user {user.id}")


# # async def setstoryreply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     user = update.effective_user
# #     text = ' '.join(context.args or [])
# #     if not text:
# #         await update.message.reply_text(
# #             "Usage: /setstoryreply <your custom message>",
# #             parse_mode='Markdown'
# #         )
# #         return

# #     context.user_data['story_reply_custom'] = text
# #     await update.message.reply_text(
# #         f"✅ Custom story reply set to:\n{text}",
# #         parse_mode='Markdown'
# #     )
# #     logger.info(f"User {user.id} set custom story reply")


# # async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     ai_status = "✅ Enabled (Using AI!)" if AI_API_KEY else "❌ Disabled"
# #     numverify_status = "✅ Enabled" if NUMVERIFY_API_KEY else "❌ Disabled"

# #     about_text = f"""
# # ℹ️ **About MRM78 Bot**

# # Version: 2.1
# # Created: 2026
# # Author: MRM78

# # **Features:**
# # ✨ Intelligent auto-replies
# # 🤖 AI-powered responses
# # 📱 Story reaction management
# # 📞 Phone number validation
# # 💡 Smart features

# # **AI Status**: {ai_status}
# # **Numverify Status**: {numverify_status}
# # Powered by python-telegram-bot, Bluesminds API & Numverify API
# #     """

# #     await update.message.reply_text(about_text, parse_mode='Markdown')


# # async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     await update.message.reply_text(
# #         "👋 Bot stopped. Use /start to activate again.",
# #         parse_mode='Markdown'
# #     )


# # async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     if not AI_API_KEY:
# #         ai_text = """
# # 🤖 **AI Status**: ❌ NOT CONFIGURED

# # To enable AI responses:
# # 1. Get an API key from Bluesminds or OpenAI
# # 2. Add it to the `.env` file:
# # 3. Restart the bot

# # Once enabled, I'll use AI to give smarter responses! 🧠
# #         """
# #     else:
# #         ai_text = """
# # 🤖 **AI Status**: ✅ ACTIVE

# # Your bot is now using AI to power responses!

# # **Features:**
# # ✨ Smart contextual replies
# # 💭 Natural conversations
# # 🎯 Better understanding of requests
# # 🚀 Continuous learning

# # Try asking me anything! I'll use AI to help you.
# #         """

# #     await update.message.reply_text(ai_text, parse_mode='Markdown')


# # async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     user_id = update.effective_user.id
# #     if user_id in conversation_history:
# #         conversation_history[user_id] = []
# #         await update.message.reply_text(
# #             "🧹 Conversation history cleared! Starting fresh! 🆕",
# #             parse_mode='Markdown'
# #         )
# #         logger.info(f"Cleared history for user {user_id}")
# #     else:
# #         await update.message.reply_text(
# #             "✅ No history to clear!",
# #             parse_mode='Markdown'
# #         )


# # async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     if not AI_API_KEY:
# #         await update.message.reply_text(
# #             "❌ No API key configured!",
# #             parse_mode='Markdown'
# #         )
# #         return

# #     user_id = update.effective_user.id
# #     await update.message.reply_text("🧪 Testing AI connection...", parse_mode='Markdown')

# #     test_response = await get_ai_response(user_id, "Say hello!")

# #     if test_response.startswith("❌") or test_response.startswith("⚠️"):
# #         await update.message.reply_text(
# #             f"❌ **Test Failed**\n{test_response}",
# #             parse_mode='Markdown'
# #         )
# #     else:
# #         await update.message.reply_text(
# #             f"✅ **AI Connection Working!**\n\nBot said: {test_response}",
# #             parse_mode='Markdown'
# #         )


# # async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     query = update.callback_query
# #     await query.answer()
# #     data = query.data

# #     class _MiniUpdate:
# #         pass

# #     mini = _MiniUpdate()
# #     mini.message = query.message
# #     mini.effective_user = query.from_user or (query.message.from_user if query.message else None)

# #     try:
# #         if data == 'help':
# #             await help_command(mini, context)
# #         elif data == 'stats':
# #             await stats_command(mini, context)
# #         elif data == 'story':
# #             await story_command(mini, context)
# #         else:
# #             if query.message:
# #                 await query.message.reply_text("⚠️ Unknown action")
# #             else:
# #                 await query.answer(text="⚠️ Unknown action", show_alert=True)
# #     except Exception as e:
# #         logger.exception(f"Error handling callback '{data}': {e}")
# #         if query.message:
# #             await query.message.reply_text("❌ An error occurred handling that button. Try again.")
# #         else:
# #             await query.answer(text="❌ An error occurred. Try again.", show_alert=True)


# # # ==================== MESSAGE HANDLERS ====================
# # async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     user = update.effective_user
# #     user_text = update.message.text

# #     if user.id not in user_stats:
# #         user_stats[user.id] = 0
# #     user_stats[user.id] += 1

# #     logger.info(f"User {user.id} sent: {user_text}")

# #     await context.bot.send_chat_action(
# #         chat_id=update.effective_chat.id,
# #         action="typing"
# #     )

# #     if AI_API_KEY:
# #         reply = await get_ai_response(user.id, user_text)
# #         await update.message.reply_text(reply)
# #         return
# #     else:
# #         if any(keyword in user_text.lower() for keyword in ['hello', 'hi', 'hey']):
# #             reply = f"👋 Hey {user.first_name}! How can I help you?"

# #         elif any(keyword in user_text.lower() for keyword in ['how are you', 'how are you?', 'how you doing']):
# #             reply = "😊 I'm doing great! Thanks for asking. How can I assist you today?"

# #         elif any(keyword in user_text.lower() for keyword in ['thanks', 'thank you', 'thx']):
# #             reply = "You're welcome! 🙏 Is there anything else I can help with?"

# #         elif any(keyword in user_text.lower() for keyword in ['time', 'what time']):
# #             current_time = datetime.now().strftime('%H:%M:%S')
# #             reply = f"⏰ Current time: {current_time}"

# #         else:
# #             reply = f"You said: **{user_text}**\n\nThanks for your message! 😊"

# #     await update.message.reply_text(reply, parse_mode='Markdown')


# # async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     user = update.effective_user
# #     user_stats[user.id] = user_stats.get(user.id, 0) + 1

# #     response = f"""
# # 📸 **Nice photo, {user.first_name}!**

# # I've received your image. Here's what I can do:
# # ✅ Analyze with AI vision
# # ✅ Extract text (OCR)
# # ✅ Detect objects
# # ✅ Describe content

# # Use /help to see all features!
# #     """

# #     await update.message.reply_text(response, parse_mode='Markdown')
# #     logger.info(f"User {user.id} sent a photo")


# # async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     user = update.effective_user
# #     user_stats[user.id] = user_stats.get(user.id, 0) + 1

# #     await update.message.reply_text("😄 Cool sticker! Keep the conversation going! 🎉")


# # async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
# #     logger.error(f"Exception while handling an update: {context.error}")

# #     if isinstance(update, Update) and update.effective_message:
# #         await update.effective_message.reply_text(
# #             "❌ Oops! An error occurred. Please try again later."
# #         )


# # async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     help_text = """
# # 📚 **Available Commands:**

# # /start - Start the bot
# # /help - Show this help message
# # /stats - View your statistics
# # /story - Enable story auto-reply
# # /setstoryreply - Set a custom story reply message
# # /validatephone - Validate a phone number
# # /ai - Check AI status & setup
# # /test - Test AI connection
# # /clear - Clear conversation history
# # /about - About this bot
# # /stop - Stop the bot

# # **Features:**
# # 🤖 AI Responses - Smart AI-powered answers
# # 🖼️ Photo Analysis - Send a photo for AI analysis
# # 📞 Phone Validation - Check phone number details
# # 💬 Chat - Just send me a message!
# #     """
# #     await update.message.reply_text(help_text, parse_mode='Markdown')


# # async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     user = update.effective_user
# #     count = user_stats.get(user.id, 0)
# #     stats_text = f"""
# # 📊 **Your Statistics:**
# # 👤 User ID: {user.id}
# # 👨 Name: {user.first_name}
# # 💬 Messages: {count}
# # ⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# #     """
# #     await update.message.reply_text(stats_text, parse_mode='Markdown')


# # # ==================== MAIN FUNCTION ====================
# # def main():
# #     try:
# #         app = Application.builder().token(BOT_TOKEN).build()

# #         app.add_handler(CommandHandler("start", start_command))
# #         app.add_handler(CommandHandler("help", help_command))
# #         app.add_handler(CommandHandler("stats", stats_command))
# #         app.add_handler(CommandHandler("story", story_command))
# #         app.add_handler(CommandHandler("about", about_command))
# #         app.add_handler(CommandHandler("ai", ai_command))
# #         app.add_handler(CommandHandler("stop", stop_command))
# #         app.add_handler(CommandHandler("clear", clear_command))
# #         app.add_handler(CommandHandler("test", test_command))
# #         app.add_handler(CommandHandler("setstoryreply", setstoryreply_command))
# #         app.add_handler(CommandHandler("validatephone", validatephone_command))

# #         app.add_handler(CallbackQueryHandler(callback_query_handler))

# #         app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
# #         app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
# #         app.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))

# #         app.add_error_handler(error_handler)

# #         logger.info("🤖 Bot started successfully!")
# #         print("🤖 Bot is running... Press Ctrl+C to stop")
# #         print("=" * 50)

# #         app.run_polling(allowed_updates=Update.ALL_TYPES)

# #     except KeyboardInterrupt:
# #         logger.info("Bot stopped by user")
# #         print("\n👋 Bot stopped gracefully")
# #     except Exception as e:
# #         logger.error(f"Fatal error: {e}")
# #         print(f"\n❌ Error: {e}")
# #         raise


# # if __name__ == "__main__":
# #     main()
# import os
# import logging
# from dotenv import load_dotenv
# from datetime import datetime
# import requests
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import (
#     Application,
#     CommandHandler,
#     MessageHandler,
#     CallbackQueryHandler,
#     ContextTypes,
#     filters,
# )

# # ==================== CONFIGURATION ====================
# load_dotenv()

# BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# if not BOT_TOKEN:
#     raise RuntimeError("TELEGRAM_BOT_TOKEN not set in environment / .env file")

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )
# logger = logging.getLogger(__name__)

# if GROQ_API_KEY:
#     logger.info("Groq API key loaded from environment")
# else:
#     logger.info("Groq API key NOT found in environment")

# user_stats = {}
# conversation_history = {}


# # ==================== AI INTEGRATION (GROQ) ====================
# async def get_ai_response(user_id: int, user_message: str) -> str:
#     """Get AI response from Groq with conversation context"""
#     if not GROQ_API_KEY:
#         return "I'm not configured for AI responses yet. Please add a Groq API key."

#     try:
#         if user_id not in conversation_history:
#             conversation_history[user_id] = []

#         if len(conversation_history[user_id]) > 10:
#             conversation_history[user_id] = conversation_history[user_id][-10:]

#         system_content = (
#             "You are a helpful, friendly, and concise assistant. "
#             "Answer the user's question directly, be specific, and ask for clarification if needed."
#         )

#         messages = [{"role": "system", "content": system_content}]
#         messages.extend(conversation_history[user_id])
#         messages.append({"role": "user", "content": user_message})

#         headers = {
#             "Authorization": f"Bearer {GROQ_API_KEY}",
#             "Content-Type": "application/json"
#         }

#         data = {
#             "model": "llama-3.3-70b-versatile",
#             "messages": messages,
#             "max_tokens": 500,
#             "temperature": 0.7,
#             "top_p": 0.9
#         }

#         logger.info(f"Sending AI request for user {user_id}: {user_message[:60]}")

#         response = requests.post(
#             "https://api.groq.com/openai/v1/chat/completions",
#             headers=headers,
#             json=data,
#             timeout=15
#         )

#         if response.status_code == 200:
#             result = response.json()
#             ai_response = result['choices'][0]['message']['content']

#             conversation_history[user_id].append({"role": "user", "content": user_message})
#             conversation_history[user_id].append({"role": "assistant", "content": ai_response})

#             return ai_response

#         elif response.status_code == 401:
#             logger.error("Invalid Groq API key")
#             return "❌ AI authentication failed. Please check the API key."

#         elif response.status_code == 429:
#             logger.warning("Groq rate limited")
#             return "⏱️ AI rate limit reached. Try again shortly."

#         else:
#             logger.warning(f"Groq API error {response.status_code}: {response.text[:200]}")
#             return "🤔 I'm having trouble thinking. Try again later!"

#     except Exception as e:
#         logger.error(f"AI request exception: {e}")
#         return "⚠️ AI service error. Please try again later."


# # ==================== COMMAND HANDLERS ====================
# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.effective_user
#     user_stats[user.id] = user_stats.get(user.id, 0) + 1

#     keyboard = [
#         [InlineKeyboardButton("📖 Help", callback_data='help')],
#         [InlineKeyboardButton("📊 Stats", callback_data='stats')],
#         [InlineKeyboardButton("📢 Send Story Reply", callback_data='story')]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)

#     welcome_text = f"""
# 👋 Hello {user.first_name}!

# Welcome to **MRM78 Bot** 🤖

# I can help you with:
# ✅ Auto-reply to your story reactions
# ✅ AI-powered chat (Groq)
# ✅ And more!

# Choose an option below or just send me a message:
#     """

#     await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
#     logger.info(f"User {user.first_name} ({user.id}) started the bot")


# async def story_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.effective_user

#     if user.id not in user_stats:
#         user_stats[user.id] = 0

#     context.user_data['story_autoreply'] = True

#     story_text = """
# ✅ **Story Auto-Reply Enabled!**

# When someone reacts to your story, I'll send them:
# "👋 Thanks for watching my story! 😊"

# You can customize this message by sending:
# /setstoryreply <your custom message>
#     """

#     await update.message.reply_text(story_text, parse_mode='Markdown')
#     logger.info(f"Story autoreply enabled for user {user.id}")


# async def setstoryreply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.effective_user
#     text = ' '.join(context.args or [])
#     if not text:
#         await update.message.reply_text(
#             "Usage: /setstoryreply <your custom message>",
#             parse_mode='Markdown'
#         )
#         return

#     context.user_data['story_reply_custom'] = text
#     await update.message.reply_text(
#         f"✅ Custom story reply set to:\n{text}",
#         parse_mode='Markdown'
#     )
#     logger.info(f"User {user.id} set custom story reply")


# async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     ai_status = "✅ Enabled (Groq AI)" if GROQ_API_KEY else "❌ Disabled"

#     about_text = f"""
# ℹ️ **About MRM78 Bot**

# Version: 2.1
# Created: 2026
# Author: MRM78

# **Features:**
# ✨ Intelligent auto-replies
# 🤖 AI-powered responses (Groq)
# 📱 Story reaction management

# **AI Status**: {ai_status}
# Powered by python-telegram-bot & Groq
#     """

#     await update.message.reply_text(about_text, parse_mode='Markdown')


# async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(
#         "👋 Bot stopped. Use /start to activate again.",
#         parse_mode='Markdown'
#     )


# async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if not GROQ_API_KEY:
#         ai_text = """
# 🤖 **AI Status**: ❌ NOT CONFIGURED

# To enable AI responses:
# 1. Get a free API key from https://console.groq.com
# 2. Add it to the `.env` file:
#    ```
#    GROQ_API_KEY=gsk_your_key_here
#    ```
# 3. Restart the bot

# Once enabled, I'll use AI to give smarter responses! 🧠
#         """
#     else:
#         ai_text = """
# 🤖 **AI Status**: ✅ ACTIVE (Groq)

# Your bot is now using AI to power responses!

# **Features:**
# ✨ Smart contextual replies
# 💭 Natural conversations
# 🎯 Better understanding of requests

# Try asking me anything!
#         """

#     await update.message.reply_text(ai_text, parse_mode='Markdown')


# async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_id = update.effective_user.id
#     if user_id in conversation_history:
#         conversation_history[user_id] = []
#         await update.message.reply_text(
#             "🧹 Conversation history cleared! Starting fresh! 🆕",
#             parse_mode='Markdown'
#         )
#         logger.info(f"Cleared history for user {user_id}")
#     else:
#         await update.message.reply_text(
#             "✅ No history to clear!",
#             parse_mode='Markdown'
#         )


# async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if not GROQ_API_KEY:
#         await update.message.reply_text(
#             "❌ No API key configured!",
#             parse_mode='Markdown'
#         )
#         return

#     user_id = update.effective_user.id
#     await update.message.reply_text("🧪 Testing AI connection...", parse_mode='Markdown')

#     test_response = await get_ai_response(user_id, "Say hello!")

#     if test_response.startswith("❌") or test_response.startswith("⚠️"):
#         await update.message.reply_text(
#             f"❌ **Test Failed**\n{test_response}",
#             parse_mode='Markdown'
#         )
#     else:
#         await update.message.reply_text(
#             f"✅ **AI Connection Working!**\n\nBot said: {test_response}",
#             parse_mode='Markdown'
#         )


# async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()
#     data = query.data

#     class _MiniUpdate:
#         pass

#     mini = _MiniUpdate()
#     mini.message = query.message
#     mini.effective_user = query.from_user or (query.message.from_user if query.message else None)

#     try:
#         if data == 'help':
#             await help_command(mini, context)
#         elif data == 'stats':
#             await stats_command(mini, context)
#         elif data == 'story':
#             await story_command(mini, context)
#         else:
#             if query.message:
#                 await query.message.reply_text("⚠️ Unknown action")
#             else:
#                 await query.answer(text="⚠️ Unknown action", show_alert=True)
#     except Exception as e:
#         logger.exception(f"Error handling callback '{data}': {e}")
#         if query.message:
#             await query.message.reply_text("❌ An error occurred handling that button. Try again.")
#         else:
#             await query.answer(text="❌ An error occurred. Try again.", show_alert=True)


# # ==================== MESSAGE HANDLERS ====================
# async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.effective_user
#     user_text = update.message.text

#     if user.id not in user_stats:
#         user_stats[user.id] = 0
#     user_stats[user.id] += 1

#     logger.info(f"User {user.id} sent: {user_text}")

#     await context.bot.send_chat_action(
#         chat_id=update.effective_chat.id,
#         action="typing"
#     )

#     if GROQ_API_KEY:
#         reply = await get_ai_response(user.id, user_text)
#         await update.message.reply_text(reply)
#         return
#     else:
#         if any(keyword in user_text.lower() for keyword in ['hello', 'hi', 'hey']):
#             reply = f"👋 Hey {user.first_name}! How can I help you?"

#         elif any(keyword in user_text.lower() for keyword in ['how are you', 'how are you?', 'how you doing']):
#             reply = "😊 I'm doing great! Thanks for asking. How can I assist you today?"

#         elif any(keyword in user_text.lower() for keyword in ['thanks', 'thank you', 'thx']):
#             reply = "You're welcome! 🙏 Is there anything else I can help with?"

#         elif any(keyword in user_text.lower() for keyword in ['time', 'what time']):
#             current_time = datetime.now().strftime('%H:%M:%S')
#             reply = f"⏰ Current time: {current_time}"

#         else:
#             reply = f"You said: **{user_text}**\n\nThanks for your message! 😊"

#     await update.message.reply_text(reply, parse_mode='Markdown')


# async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.effective_user
#     user_stats[user.id] = user_stats.get(user.id, 0) + 1

#     response = f"""
# 📸 **Nice photo, {user.first_name}!**

# Photo received! Currently I can chat about it via text — image analysis isn't enabled in this version.

# Use /help to see all features!
#     """

#     await update.message.reply_text(response, parse_mode='Markdown')
#     logger.info(f"User {user.id} sent a photo")


# async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.effective_user
#     user_stats[user.id] = user_stats.get(user.id, 0) + 1

#     await update.message.reply_text("😄 Cool sticker! Keep the conversation going! 🎉")


# async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
#     logger.error(f"Exception while handling an update: {context.error}")

#     if isinstance(update, Update) and update.effective_message:
#         await update.effective_message.reply_text(
#             "❌ Oops! An error occurred. Please try again later."
#         )


# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     help_text = """
# 📚 **Available Commands:**

# /start - Start the bot
# /help - Show this help message
# /stats - View your statistics
# /story - Enable story auto-reply
# /setstoryreply - Set a custom story reply message
# /ai - Check AI status & setup
# /test - Test AI connection
# /clear - Clear conversation history
# /about - About this bot
# /stop - Stop the bot

# **Features:**
# 🤖 AI Responses - Smart AI-powered answers (Groq)
# 💬 Chat - Just send me a message!
#     """
#     await update.message.reply_text(help_text, parse_mode='Markdown')


# async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.effective_user
#     count = user_stats.get(user.id, 0)
#     stats_text = f"""
# 📊 **Your Statistics:**
# 👤 User ID: {user.id}
# 👨 Name: {user.first_name}
# 💬 Messages: {count}
# ⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#     """
#     await update.message.reply_text(stats_text, parse_mode='Markdown')


# # ==================== MAIN FUNCTION ====================
# def main():
#     try:
#         app = Application.builder().token(BOT_TOKEN).build()

#         app.add_handler(CommandHandler("start", start_command))
#         app.add_handler(CommandHandler("help", help_command))
#         app.add_handler(CommandHandler("stats", stats_command))
#         app.add_handler(CommandHandler("story", story_command))
#         app.add_handler(CommandHandler("about", about_command))
#         app.add_handler(CommandHandler("ai", ai_command))
#         app.add_handler(CommandHandler("stop", stop_command))
#         app.add_handler(CommandHandler("clear", clear_command))
#         app.add_handler(CommandHandler("test", test_command))
#         app.add_handler(CommandHandler("setstoryreply", setstoryreply_command))

#         app.add_handler(CallbackQueryHandler(callback_query_handler))

#         app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
#         app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
#         app.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))

#         app.add_error_handler(error_handler)

#         logger.info("🤖 Bot started successfully!")
#         print("🤖 Bot is running... Press Ctrl+C to stop")
#         print("=" * 50)

#         app.run_polling(allowed_updates=Update.ALL_TYPES)

#     except KeyboardInterrupt:
#         logger.info("Bot stopped by user")
#         print("\n👋 Bot stopped gracefully")
#     except Exception as e:
#         logger.error(f"Fatal error: {e}")
#         print(f"\n❌ Error: {e}")
#         raise


# if __name__ == "__main__":
#     main()
import os
import logging
import time
from dotenv import load_dotenv
from datetime import datetime
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# ==================== CONFIGURATION ====================
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN not set in environment / .env file")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

if GROQ_API_KEY:
    logger.info("Groq API key loaded from environment")
else:
    logger.info("Groq API key NOT found - bot will run in basic mode")

# In-memory storage (resets on restart - upgrade to Redis/DB later if needed)
user_stats = {}
conversation_history = {}
user_last_message = {}

# Async HTTP client for Groq
http_client = httpx.AsyncClient(timeout=15.0)

# ==================== AI INTEGRATION (GROQ) ====================
async def get_ai_response(user_id: int, user_message: str) -> str:
    """Get AI response from Groq with conversation context"""
    if not GROQ_API_KEY:
        return "🤖 AI is not configured. Add GROQ_API_KEY to your environment variables."

    try:
        # Initialize or trim conversation history
        if user_id not in conversation_history:
            conversation_history[user_id] = []
        
        # Keep last 10 exchanges (20 messages) for context
        conversation_history[user_id] = conversation_history[user_id][-20:]

        system_content = (
            "You are a helpful, friendly, and concise assistant. "
            "Answer directly, be specific, and ask for clarification if needed."
        )

        messages = [{"role": "system", "content": system_content}]
        messages.extend(conversation_history[user_id])
        messages.append({"role": "user", "content": user_message})

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0.7,
            "top_p": 0.9
        }

        logger.info(f"Sending AI request for user {user_id}: {user_message[:60]}...")

        response = await http_client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content']

            # Store in history
            conversation_history[user_id].append({"role": "user", "content": user_message})
            conversation_history[user_id].append({"role": "assistant", "content": ai_response})

            return ai_response

        elif response.status_code == 401:
            logger.error("Invalid Groq API key")
            return "❌ AI authentication failed. Check your GROQ_API_KEY."

        elif response.status_code == 429:
            logger.warning("Groq rate limited")
            return "⏱️ Rate limit reached. Please try again in a moment."

        else:
            logger.warning(f"Groq API error {response.status_code}: {response.text[:200]}")
            return "🤔 I'm having trouble connecting to AI. Try again later."

    except httpx.TimeoutException:
        logger.error("Groq API timeout")
        return "⏱️ AI response timed out. Please try again."
    except Exception as e:
        logger.error(f"AI request exception: {e}")
        return "⚠️ AI service error. Please try again later."


# ==================== RATE LIMITING ====================
async def check_rate_limit(user_id: int) -> bool:
    """Returns True if user is allowed to send message"""
    now = time.time()
    if user_id in user_last_message:
        if now - user_last_message[user_id] < 2:  # 2 second cooldown
            return False
    user_last_message[user_id] = now
    return True


# ==================== COMMAND HANDLERS ====================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_stats[user.id] = user_stats.get(user.id, 0) + 1

    keyboard = [
        [InlineKeyboardButton("📖 Help", callback_data='help')],
        [InlineKeyboardButton("📊 Stats", callback_data='stats')],
        [InlineKeyboardButton("🤖 AI Status", callback_data='ai_status')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = f"""
👋 Hello {user.first_name}!

Welcome to **MRM78 Bot** 🤖

I can help you with:
✅ AI-powered chat (Groq)
✅ Smart conversations
✅ And more!

Choose an option below or just send me a message!
    """

    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    logger.info(f"User {user.first_name} ({user.id}) started the bot")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📚 **Available Commands:**

/start - Start the bot
/help - Show this help message
/stats - View your statistics
/ai - Check AI status & setup
/test - Test AI connection
/clear - Clear conversation history
/about - About this bot

**Features:**
🤖 AI Responses - Smart AI-powered answers
💬 Chat - Just send me a message!
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    count = user_stats.get(user.id, 0)
    stats_text = f"""
📊 **Your Statistics:**
👤 User ID: {user.id}
👤 Name: {user.first_name}
💬 Messages: {count}
🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    await update.message.reply_text(stats_text, parse_mode='Markdown')


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ai_status = "✅ Enabled" if GROQ_API_KEY else "❌ Disabled"

    about_text = f"""
ℹ️ **About MRM78 Bot**

Version: 2.5 (Async)
Created: 2026
Author: MRM78

**Features:**
✨ Intelligent auto-replies
🤖 AI-powered responses (Groq)
💬 Natural conversations

**AI Status**: {ai_status}
Powered by python-telegram-bot & Groq
    """

    await update.message.reply_text(about_text, parse_mode='Markdown')


async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not GROQ_API_KEY:
        ai_text = """
🤖 **AI Status**: ❌ NOT CONFIGURED

To enable AI responses:
1. Get a free API key from https://console.groq.com
2. Add it to your environment variables:
   `GROQ_API_KEY=gsk_your_key_here`
3. Restart the bot
        """
    else:
        ai_text = """
🤖 **AI Status**: ✅ ACTIVE (Groq)

Your bot is using AI to power responses!

**Features:**
✨ Smart contextual replies
💭 Natural conversations
🎯 Better understanding

Try asking me anything!
        """

    await update.message.reply_text(ai_text, parse_mode='Markdown')


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in conversation_history and conversation_history[user_id]:
        conversation_history[user_id] = []
        await update.message.reply_text("🧹 Conversation history cleared! Starting fresh! 🆕")
        logger.info(f"Cleared history for user {user_id}")
    else:
        await update.message.reply_text("✅ No history to clear!")


async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not GROQ_API_KEY:
        await update.message.reply_text("❌ No API key configured!")
        return

    user_id = update.effective_user.id
    await update.message.reply_text("🧪 Testing AI connection...")

    test_response = await get_ai_response(user_id, "Say a brief hello!")

    if test_response.startswith("❌") or test_response.startswith("⚠️") or test_response.startswith("⏱️"):
        await update.message.reply_text(f"❌ **Test Failed**\n{test_response}")
    else:
        await update.message.reply_text(f"✅ **AI Connection Working!**\n\nBot said: {test_response}")


# ==================== CALLBACK QUERY HANDLER ====================
async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    try:
        if data == 'help':
            await help_command(update, context)
        elif data == 'stats':
            await stats_command(update, context)
        elif data == 'ai_status':
            await ai_command(update, context)
        else:
            await query.edit_message_text("⚠️ Unknown action")
    except Exception as e:
        logger.exception(f"Error handling callback '{data}': {e}")
        await query.answer(text="❌ An error occurred. Try again.", show_alert=True)


# ==================== MESSAGE HANDLERS ====================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Rate limiting
    if not await check_rate_limit(user.id):
        await update.message.reply_text("⏳ Please wait a moment before sending another message.")
        return

    user_text = update.message.text
    user_stats[user.id] = user_stats.get(user.id, 0) + 1

    logger.info(f"User {user.id} sent: {user_text}")

    # Show typing indicator
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    # AI response if key is available
    if GROQ_API_KEY:
        reply = await get_ai_response(user.id, user_text)
        await update.message.reply_text(reply)
        return

    # Fallback responses if no AI
    text_lower = user_text.lower()
    if any(k in text_lower for k in ['hello', 'hi', 'hey']):
        reply = f"👋 Hey {user.first_name}! How can I help you?"
    elif any(k in text_lower for k in ['how are you', 'how you doing']):
        reply = "😊 I'm doing great! Thanks for asking. How can I assist you today?"
    elif any(k in text_lower for k in ['thanks', 'thank you', 'thx']):
        reply = "You're welcome! 🙏 Is there anything else I can help with?"
    elif any(k in text_lower for k in ['time', 'what time']):
        current_time = datetime.now().strftime('%H:%M:%S')
        reply = f"⏰ Current time: {current_time}"
    else:
        reply = f"You said: **{user_text}**\n\nThanks for your message! 😊"

    await update.message.reply_text(reply, parse_mode='Markdown')


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_stats[user.id] = user_stats.get(user.id, 0) + 1

    response = f"""
📸 **Nice photo, {user.first_name}!**

Photo received! Image analysis isn't enabled in this version, but I can chat about it via text.

Use /help to see all features!
    """
    await update.message.reply_text(response, parse_mode='Markdown')
    logger.info(f"User {user.id} sent a photo")


async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_stats[user.id] = user_stats.get(user.id, 0) + 1
    await update.message.reply_text("😄 Cool sticker! Keep the conversation going! 🎉")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Exception while handling an update: {context.error}")

    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "❌ Oops! An error occurred. Please try again later."
        )


# ==================== MAIN FUNCTION ====================
def main():
    try:
        app = Application.builder().token(BOT_TOKEN).build()

        # Command handlers
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("stats", stats_command))
        app.add_handler(CommandHandler("about", about_command))
        app.add_handler(CommandHandler("ai", ai_command))
        app.add_handler(CommandHandler("clear", clear_command))
        app.add_handler(CommandHandler("test", test_command))

        # Callback handler
        app.add_handler(CallbackQueryHandler(callback_query_handler))

        # Message handlers
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        app.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))

        # Error handler
        app.add_error_handler(error_handler)

        logger.info("🤖 Bot started successfully!")
        print("🤖 Bot is running... Press Ctrl+C to stop")
        print("=" * 50)

        # drop_pending_updates=True prevents message flood on restart
        app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        print("\n👋 Bot stopped gracefully")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()