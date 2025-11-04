import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode, ChatType
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold
from aiogram.client.default import DefaultBotProperties
from datetime import datetime
import aiohttp

# ✅ Bot Token and Config
BOT_TOKEN = "8194034175:AAGj9dhBRBgsH8JI3bPULtp-2g6IzKxat8Q"
OWNER_ID = 6871652662
ALLOWED_GROUPS = {-1002720090873}

# ✅ Correct Bot Initialization for Aiogram v3.7+
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# ✅ Helper Function
def unix_to_readable(timestamp):
    try:
        return datetime.fromtimestamp(int(timestamp)).strftime("%d-%m-%Y %H:%M:%S")
    except:
        return "N/A"

# ✅ /start Command
@dp.message(CommandStart())
async def start_handler(message: Message):
    if message.chat.type != ChatType.PRIVATE:
        return
    user = message.from_user
    btn = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Join Channel", url="https://t.me/riyadfflikesgroup")]
    ])
    await message.answer(
        f"👋 Hello {hbold(user.full_name)}!\n\n"
        "📌 Welcome to FF Player Info Bot\n\n"
        "👉 To get player info, use:\n<code>/get ind 8431487083</code>\n\n"
        "⚠️ Only works in allowed groups.",
        reply_markup=btn
    )

# ✅ /allow Command
@dp.message(Command("allow"))
async def allow_group(message: Message):
    if message.from_user.id != OWNER_ID:
        return
    try:
        group_id = int(message.text.split(" ")[1])
        ALLOWED_GROUPS.add(group_id)
        await message.answer(f"✅ Group <code>{group_id}</code> has been allowed.")
    except Exception:
        await message.answer("❌ Usage: <code>/allow groupid</code>")

# ✅ /remove Command
@dp.message(Command("remove"))
async def remove_group(message: Message):
    if message.from_user.id != OWNER_ID:
        return
    try:
        group_id = int(message.text.split(" ")[1])
        ALLOWED_GROUPS.discard(group_id)
        await message.answer(f"❌ Group <code>{group_id}</code> has been removed.")
    except Exception:
        await message.answer("❌ Usage: <code>/remove groupid</code>")

# ✅ /get Command
@dp.message(Command("get"))
async def get_player_info(message: Message):
    if message.chat.id not in ALLOWED_GROUPS:
        return
    args = message.text.split()
    if len(args) != 3:
        await message.reply("❌ Invalid format.\n✅ Use: <code>/get bd 2004537688</code>")
        return

    region, uid = args[1], args[2]
    processing = await message.reply("⏳ Fetching Details for UID...\nPlease wait 3 seconds...")
    await asyncio.sleep(3)

    url = f"https://danger-info-alpha.vercel.app/accinfo?uid={uid}&key=DANGERxINFO"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                data = await r.json()

        b = data.get("basicInfo", {})
        c = data.get("clanBasicInfo", {})
        p = data.get("petInfo", {})
        s = data.get("socialInfo", {})

        text = f"""<b>📋 Player Info:</b>
├─ 👤 Name: {b.get('nickname', 'N/A')}
├─ 🆔 UID: {b.get('accountId', 'N/A')}
├─ 🌍 Region: {b.get('region', 'N/A')}
├─ 🎮 Level: {b.get('level', 'N/A')}
├─ 🧪 EXP: {b.get('exp', 0):,}
├─ ❤️ Likes: {b.get('liked', 'N/A')}
├─ 📱 Account Type: {b.get('accountType', 'N/A')} ({b.get('releaseVersion', 'N/A')})
├─ 🏷️ Title ID: {b.get('title', 'N/A')}
├─ 🗓️ Created At: {unix_to_readable(b.get('createAt', 0))}
├─ 🔓 Last Login: {unix_to_readable(b.get('lastLoginAt', 0))}

<b>🏅 Rank Info:</b>
├─ 🎖️ BR Rank: {b.get('rank', 'N/A')} ({b.get('rankingPoints', 0)} pts)
├─ 🥇 Max BR Rank: {b.get('maxRank', 'N/A')}
├─ 🏆 CS Rank: {b.get('csRank', 'N/A')} ({b.get('csRankingPoints', 0)} pts)
├─ 🥈 Max CS Rank: {b.get('csMaxRank', 'N/A')}

<b>🎫 Elite & Stats:</b>
├─ 🎫 Elite Pass: {"Yes ✅" if b.get('hasElitePass') else "No ❌"}
├─ 🎖️ Badges: {b.get('badgeCnt', 0)}
├─ 💎 Diamond Cost: {data.get('diamondCostRes', {}).get('diamondCost', 'N/A')}
├─ 🛡️ Credit Score: {data.get('creditScoreInfo', {}).get('creditScore', 'N/A')}

<b>🏰 Guild Info:</b>
├─ 🏷️ Name: {c.get('clanName', 'N/A')}
├─ 👑 Leader ID: {c.get('captainId', 'N/A')}
├─ 👥 Members: {c.get('memberNum', 0)} / {c.get('capacity', 0)}
├─ 🔢 Level: {c.get('clanLevel', 'N/A')}

<b>🐾 Pet Info:</b>
├─ 🐶 Name: {p.get('name', 'N/A')}
├─ 🎚️ Level: {p.get('level', 'N/A')}
├─ 🎨 Skin ID: {p.get('skinId', 'N/A')}
├─ 🧬 Skill ID: {p.get('selectedSkillId', 'N/A')}

<b>🧬 Social Info:</b>
├─ 🚻 Gender: {s.get('gender', 'N/A').replace('Gender_', '')}
├─ 🌐 Language: {s.get('language', 'N/A').replace('Language_', '')}
├─ ⏱️ Time Online: {s.get('timeOnline', 'N/A').replace('TimeOnline_', '')}
├─ 🕰️ Time Active: {s.get('timeActive', 'N/A').replace('TimeActive_', '')}
└─ 📝 Signature: {s.get('signature', 'N/A').replace('[b][c][i]', '').strip()}
"""

        btn = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👑 𝘿𝙈  𝙊𝙒𝙉𝙀𝙍 ", url="https://t.me/riyadalhasan10")]
        ])
        await processing.edit_text(text, reply_markup=btn)

    except Exception as e:
        await processing.edit_text(f"❌ Failed to fetch data.\nError: {e}")

# ✅ Main Function
async def main():
    print("🤖 Bot is running...")
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())