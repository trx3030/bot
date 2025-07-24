import asyncio
import json
from playwright.async_api import async_playwright
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# تحميل الإيميلات وكلمات السر من ملف خارجي
with open("outlook.json", "r", encoding="utf-8") as f:
    CREDENTIALS = json.load(f)

TELEGRAM_TOKEN = "8049909443:AAHhg8_19QiEqJLjOB2j0JgLDtQls4K7fIs"

# تخزين المستخدم الحالي
user_sessions = {}

async def click_next(page):
    try:
        await page.click('input[type="submit"]', timeout=3000)
    except:
        try:
            await page.click('button:has-text("التالي")', timeout=3000)
        except:
            return False
    return True

async def fetch_last_outlook_email(email: str, password: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        page = await browser.new_page()
        try:
            await page.goto("https://outlook.live.com/owa/")
            await page.locator("#c-shellmenu_custom_outline_signin_bhvr100_right").click()
            await page.wait_for_timeout(1500)

            await page.fill('input[type="email"]', email)
            await page.wait_for_timeout(1000)

            if not await click_next(page):
                return "❌ لم يظهر زر (التالي) بعد الإيميل."

            await page.wait_for_timeout(1500)
            await page.fill('input[type="password"]', password)
            await page.wait_for_timeout(1000)

            if not await click_next(page):
                return "❌ لم يظهر زر (التالي) بعد كلمة السر."

            await page.wait_for_timeout(3000)
            try:
                await page.locator("button:has-text('لا')").click()
            except:
                pass

            try:
                await page.wait_for_selector('button[aria-label="التخطي إلى المحتوى الأساسي"]', timeout=10000)
                await page.locator('button[aria-label="التخطي إلى المحتوى الأساسي"]').click()
                await page.wait_for_timeout(1000)
            except:
                pass

            try:
                await page.wait_for_selector('button[name="أخرى"]', timeout=10000)
                await page.locator('button[name="أخرى"]').click()
                await page.wait_for_timeout(1000)
            except:
                return "❌ لم يظهر تبويب 'أخرى'."

            try:
                await page.wait_for_selector('span.fui-Avatar__initials', timeout=10000)
                avatar_element = page.locator('span.fui-Avatar__initials').first
                container = avatar_element.locator("xpath=../../../../..")
                await container.click()
            except:
                return "❌ لم يتم العثور على رسالة جديدة."

            try:
                await page.wait_for_selector('div[role="document"]', timeout=15000)
                content = await page.locator('div[role="document"]').inner_text()
            except:
                content = "❌ لم يتم استخراج نص الرسالة."

            return f"📨 محتوى الرسالة:\n\n{content.strip()}"

        except Exception as e:
            return f"❌ حصل خطأ:\n{e}"
        finally:
            await browser.close()

# بوت تليجرام
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_sessions[user_id] = None
    await update.message.reply_text("👋 أهلاً! أرسل الإيميل الآن لجلب آخر رسالة.")

async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    email = update.message.text.strip()
    if email in CREDENTIALS:
        password = CREDENTIALS[email]
        await update.message.reply_text(f"🔄 جاري الدخول إلى {email}...")
        result = await fetch_last_outlook_email(email, password)
    else:
        result = "❌ الإيميل غير موجود في قاعدة البيانات."
    await update.message.reply_text(result[:4000])

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_email))
    print("🤖 البوت شغال... ابدأ بـ /start")
    app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
