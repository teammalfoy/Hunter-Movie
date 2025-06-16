import os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL_USERNAME")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    sub = await check_sub(msg.from_user.id)
    if not sub:
        btn = InlineKeyboardMarkup()
        btn.add(InlineKeyboardButton("🔔 Kanalga obuna bo'lish", url=f"https://t.me/{CHANNEL.replace('@','')}"))
        await msg.answer("Botdan foydalanish uchun kanalga obuna bo‘ling!", reply_markup=btn)
        return
    await msg.answer("🎬 Xush kelibsiz! Kodni yuboring:")

@dp.message_handler()
async def send_film(msg: types.Message):
    sub = await check_sub(msg.from_user.id)
    if not sub:
        btn = InlineKeyboardMarkup()
        btn.add(InlineKeyboardButton("🔔 Kanalga obuna bo'lish", url=f"https://t.me/{CHANNEL.replace('@','')}"))
        await msg.answer("Kanalga obuna bo‘ling!", reply_markup=btn)
        return

    kod = msg.text.strip()
    
    if kod == "123":
        await msg.reply_video("https://example.com/movie123.mp4", caption="🎥 Kino: Hunter Movie")
    else:
        await msg.reply("😕 Bunday kod topilmadi.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
