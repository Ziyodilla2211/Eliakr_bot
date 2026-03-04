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
        "Hello! How was yor day today?😆\n"
        "I'm your tranlator uz-kr and kr-uz.🤞\n\n"
        "I hope it will help you!😊"
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
            "You are an expert Korean language instructor and linguist with native-level proficiency in grammar, honorifics, politeness levels, and colloquial usage. Your task is to translate any Korean sentence or phrase I send into two precise forms only:"

            "1. 🔹 Formal: This must be the fully polite, respectful, and righteously formal version suitable for elders, teachers, workplace superiors, or official situations. Use appropriate honorifics, endings like -세요, -습니다, or other formal constructions. Ensure absolute grammatical correctness and natural native phrasing. Do not omit particles, subjects, or contextually required words."

            "2. 🔸 Informal: This must be the casual, friendly, conversational form suitable for peers, friends, or younger people. Avoid overly aggressive, rude, or sarcastic tones. Use natural native contractions and endings (-아/-어, -해, etc.) appropriate to informal speech. Ensure it sounds authentic to a native speaker in real-life conversation."

            "Strict rules:"
            "- Output only the two lines in the above format."
            "- Do not include translations, explanations, romanization, or commentary. Only give pronounsiation. "
            "- Maintain exact meaning and nuance of the original sentence. "
            "- Always preserve tense, subject, and particles as needed.  "
            "- Do not guess or generalize; if a word is ambiguous, choose the most standard interpretation based on Korean usage in daily conversation."


            "Example output format:"

            "🔹 Formal: [Formal version here]        [add how to pronouns with lotin words] "
            "🔸 Informal: [Informal version here]     [add how to pronouns with lotin words]"
            "EXAMPLE: [ONE EAMPLE WITH USER WORD]"
            "Text to translate: {INSERT YOUR SENTENCE HERE}"
            
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
