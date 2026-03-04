import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

client = AsyncOpenAI(api_key=API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! How was your day today?😆\n"
        "I'm your translator uz-kr and kr-uz or eng-kr.🤞\n\n"
        "I hope it will help you!😊\n\n"
        "Write:"
    )
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "I can help you translate text between Uzbek and Korean.\n"
        "Just send me a message and I'll translate it for you!"
    )

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()

    status_msg = await update.message.reply_text("Translating with AI...")

    
    system_prompt = (
        "Siz tarjimonsiz. Har doim quyidagi formatda javob bering."
        "Kr→Uz"
        "🟢Formal: [formal Uzbek]\n ([pronunciation])\n"
        "\n🟠Informal: [informal Uzbek]\n ([pronunciation])\n"
        "Example: [Korean sentence]\n ([pronunciation])\n"
        "[translation of example]\n"
        "Uz/Eng→Kr"
        "🟢Formal: [formal Korean] \n([pronunciation])\n"
        "\n🟠Informal: [informal Korean] \n([pronunciation])\n"
        "Example: [Korean sentence] \n([pronunciation])\n"
        "[translation of example]\n"
        "Do not skip any field; always natural, context-correct."
        "CONSIDER \n as new line"
)
    try:
        response = await client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ],
        
        )
        translated_text = response.choices[0].message.content.strip()
        await status_msg.edit_text(translated_text)
        

    except Exception as e:
        print(f"XATO TURI: {type(e).__name__}")
        print(f"XATO: {e}")
        await status_msg.edit_text("Error! Please try again!😔")

def main():
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN is not set in the .env file.")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

















