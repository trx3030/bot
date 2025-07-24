from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from playwright.async_api import async_playwright

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is working!")

if __name__ == "__main__":
    import asyncio

    async def main():
        app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()
        app.add_handler(CommandHandler("start", start))
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            await browser.close()
        await app.run_polling()

    asyncio.run(main())