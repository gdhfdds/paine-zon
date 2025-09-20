import os
import json
import discord
from discord import app_commands
from discord.ext import commands
import asyncio

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

WHITELIST = [
    1303085976222171269,
    762640098788900886,
    1405957718002372800
]

WELCOME_CHANNEL_ID = 1287603286782937129  

# ملف نخزن فيه الأعضاء اللي استقبلوا الترحيب
WELCOME_FILE = "welcomed.json"

# تحميل البيانات
if os.path.exists(WELCOME_FILE):
    with open(WELCOME_FILE, "r") as f:
        welcomed_members = set(json.load(f))
else:
    welcomed_members = set()

# حفظ البيانات
def save_welcomed():
    with open(WELCOME_FILE, "w") as f:
        json.dump(list(welcomed_members), f)

@bot.event
async def on_member_join(member):
    if member.id in welcomed_members:
        return
    
    try:
        embed_dm = discord.Embed(
            title="🌟 مرحباً بك في السيرفر! 🌟",
            description="**✅ عليك أن تمر إلى التحقق حتى تتمكن من الدخول إلى الرومات.**",
            color=discord.Color.gold()
        )
        embed_dm.set_footer(text="💠 نتمنى لك قضاء وقت ممتع 💠")
        await member.send(embed=embed_dm)
        welcomed_members.add(member.id)
        save_welcomed()
        print(f"تم إرسال رسالة ترحيب في الخاص لـ {member.name}")
    except:
        print(f"❌ لا يمكن إرسال رسالة ترحيب لـ {member.name} (DM مغلق)")

    try:
        channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
        if channel:
            embed_channel = discord.Embed(
                title=f"👋 أهلاً {member.name}!",
                description="**🌟 نتمنى لك قضاء وقت ممتع معنا.\n✅ لا تنسى المرور عبر التحقق**.",
                color=discord.Color.blue()
            )
            await channel.send(embed=embed_channel)
            print(f"تم إرسال الترحيب في قناة السيرفر لـ {member.name}")
    except:
        print("تعذر إرسال رسالة الترحيب في القناة.")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    print("البوت جاهز للعمل ✅")
