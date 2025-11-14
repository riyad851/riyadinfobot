import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode, ChatType
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold
from aiogram.client.default import DefaultBotProperties
from datetime import datetime
import aiohttp

# ✅ Bot Token and Config
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
ALLOWED_GROUPS = {-1002720090873}  # ✅ Add more using /allow

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

def unix_to_readable(timestamp):
    try:
        return datetime.fromtimestamp(int(timestamp)).strftime("%d-%m-%Y %H:%M:%S")
    except:
        return "N/A"

# ✅ /start
@dp.message(CommandStart())
async def start_handler(message: Message):
    if message.chat.type != ChatType.PRIVATE:
        return

    user = message.from_user

    btn = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 JOIN GROUP", url="https://t.me/riyadfflikesgroup")],
        [InlineKeyboardButton(text="👑 OWNER", url="https://t.me/riyadalhasan10")]
    ])

    # ✅ Try Profile Picture
    try:
        photos = await bot.get_user_profile_photos(user.id, limit=1)
        if photos.total_count > 0:
            pid = photos.photos[0][0].file_id
            return await message.answer_photo(
                pid,
                caption=f"👋 Hello {hbold(user.full_name)}!\n\n"
                        "🎮 * Riyad FF Info Bot *\n\n"
                        "Use:\n<code>/get region uid</code>\n\n"
                        "⚠️ Bot works only in Group",
                reply_markup=btn
            )
    except:
        pass

    await message.answer(
        f"👋 Hello {hbold(user.full_name)}!\n\n"
        "🎮 *Riyad FF Info Bot*\n\n"
        "Use:\n<code>/get bd UID</code>\n\n"
        "⚠️ Bot works only in Group!",
        reply_markup=btn
    )

# ✅ /allow
@dp.message(Command("allow"))
async def allow_group(message: Message):
    if message.from_user.id != OWNER_ID:
        return
    try:
        gid = int(message.text.split()[1])
        ALLOWED_GROUPS.add(gid)
        await message.answer(f"✅ Allowed Group: <code>{gid}</code>")
    except:
        await message.answer("❌ Usage: <code>/allow group_id</code>")

# ✅ /remove
@dp.message(Command("remove"))
async def remove_group(message: Message):
    if message.from_user.id != OWNER_ID:
        return
    try:
        gid = int(message.text.split()[1])
        ALLOWED_GROUPS.discard(gid)
        await message.answer(f"❌ Removed Group: <code>{gid}</code>")
    except:
        await message.answer("❌ Usage: <code>/remove group_id</code>")

# ✅ /get
@dp.message(Command("get"))
async def get_player_info(message: Message):

    # ✅ If Private → Show Join Button
    if message.chat.type == ChatType.PRIVATE:
        join = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 JOIN GROUP", url="https://t.me/riyadfflikesgroup")],
            [InlineKeyboardButton(text="👑 OWNER", url="https://t.me/riyadalhasan10")]
        ])
        return await message.answer(
            "🚫 <b>The bot works only in Group!</b>\n\n"
            "👉 Join Group To Use This Command.",
            reply_markup=join
        )

    # ✅ If Group Not Allowed → Show Allow Request
    if message.chat.id not in ALLOWED_GROUPS:
        req = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👑 OWNER", url="https://t.me/riyadalhasan10")],
            [InlineKeyboardButton(text="➕ REQUEST TO ALLOW GROUP", url=f"https://t.me/riyadalhasan10?text=Allow%20Group%20ID%20{message.chat.id}")]
        ])
        return await message.reply(
            f"🚫 <b>This Group Is Not Authorized!</b>\n\n"
            f"🆔 Group ID: <code>{message.chat.id}</code>\n"
            "📩 Contact Owner To Allow This Group.",
            reply_markup=req
        )

    # ✅ Continue Normally
    args = message.text.split()
    if len(args) != 3:
        return await message.reply("❌ Use Format:\n<code>/get region uid</code>")
    
    region = args[1].lower()  # bd / ind / sg etc
    uid = args[2]

    processing = await message.reply("⏳ Fetching Player Info...")
    await asyncio.sleep(2)

    url = f"https://duranto-info-olive.vercel.app/player-info?uid={uid}&region={region}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                data = await r.json()

        b = data.get("basicInfo", {})
        c = data.get("clanBasicInfo", {})
        pet = data.get("petInfo", {})
        prof = data.get("profileInfo", {})
        soc = data.get("socialInfo", {})
        dcost = data.get("diamondCostRes", {})
        credit = data.get("creditScoreInfo", {})

        text = f"""
<b>📌 BASIC INFO</b>
👤 Name: {b.get('nickname','N/A')}
🆔 UID: {b.get('accountId','N/A')}
🌍 Region: {b.get('region','N/A')}
🎮 Level: {b.get('level','N/A')}
💖 Likes: {b.get('liked','N/A')}
🎖️ Title ID: {b.get('title','N/A')}
📈 EXP: {b.get('exp',0):,}
☢ Account Type: {b.get('accountType','N/A')}
📌 Release: {b.get('releaseVersion','N/A')}
🟢 Show BR Rank: {b.get('showBrRank','N/A')}
🟣 Show CS Rank: {b.get('showCsRank','N/A')}
🗓️ Created: {unix_to_readable(b.get('createAt',0))}
🔐 Last Login: {unix_to_readable(b.get('lastLoginAt',0))}
🏅 Badge Count: {b.get('badgeCnt','N/A')}
🖼 Banner ID: {b.get('bannerId','N/A')}
🔫 Weapon Skins: {", ".join(str(x) for x in b.get('weaponSkinShows',[]))}

<b>🏆 RANK INFO</b>
🎖️ BR Rank: {b.get('rank','N/A')} ({b.get('rankingPoints','N/A')} pts)
🥇 Max BR: {b.get('maxRank','N/A')}
🔥 CS Rank: {b.get('csRank','N/A')} ({b.get('csRankingPoints','N/A')} pts)
🥈 Max CS: {b.get('csMaxRank','N/A')}

<b>💠 DIAMOND & CREDIT</b>
💎 Diamond Cost: {dcost.get('diamondCost','N/A')}
🛡️ Credit Score: {credit.get('creditScore','N/A')}
⏳ Credit End: {unix_to_readable(credit.get('periodicSummaryEndTime',0))}
🎁 Reward State: {credit.get('rewardState','N/A')}

<b>🏰 GUILD INFO</b>
🏷️ Name: {c.get('clanName','N/A')}
🔢 Level: {c.get('clanLevel','N/A')}
👥 Members: {c.get('memberNum','N/A')} / {c.get('capacity','N/A')}
👑 Leader ID: {c.get('captainId','N/A')}

<b>🐾 PET INFO</b>
🆔 Pet ID: {pet.get('id','N/A')}
🎚️ Level: {pet.get('level','N/A')}
🎨 Skin: {pet.get('skinId','N/A')}
🧬 Skill: {pet.get('selectedSkillId','N/A')}
⭐ Exp: {pet.get('exp','N/A')}

<b>👕 PROFILE INFO</b>
🖼️ Avatar: {prof.get('avatarId','N/A')}
🎭 Skin Color: {prof.get('skinColor','N/A')}
👗 Clothes: {", ".join(str(x) for x in prof.get('clothes',[]))}
🧬 Skills: {", ".join(str(x) for x in prof.get('equipedSkills',[]))}

<b>🌐 SOCIAL INFO</b>
🗣️ Language: {soc.get('language','N/A').replace('Language_','')}
🎮 Mode Prefer: {soc.get('modePrefer','N/A').replace('ModePrefer_','')}
🏅 Rank Show: {soc.get('rankShow','N/A').replace('RankShow_','')}
📝 Bio: {soc.get('signature','').replace('[b][c]','').strip()}
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
