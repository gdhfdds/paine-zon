import os
import discord
from discord import app_commands
from discord.ext import commands
import asyncio

# جلب التوكن من Environment Variables
TOKEN = os.getenv("TOKEN")

# إعداد الـ intents للبوت
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# قائمة الأعضاء المسموح لهم باستخدام البوت (Whitelist)
WHITELIST = [
    1303085976222171269,  # أول ID
    762640098788900886,   # ثاني ID
    1405957718002372800   # ثالث ID
]

# ID القناة اللي يرسل فيها الترحيب داخل السيرفر
WELCOME_CHANNEL_ID = 1287603286782937129  # غيره بالـ ID الصحيح عندك

# تخزين الأعضاء اللي استقبلوا ترحيب بالخاص
welcomed_members = set()

# عند دخول عضو جديد
@bot.event
async def on_member_join(member):
    # ✅ التحقق إذا أرسلنا لهذا العضو من قبل
    if member.id in welcomed_members:
        return
    
    # رسالة Embed في الخاص
    try:
        embed_dm = discord.Embed(
            title="🌟 مرحباً بك في السيرفر! 🌟",
            description="**✅ عليك أن تمر إلى التحقق حتى تتمكن من الدخول إلى الرومات.**",
            color=discord.Color.gold()
        )
        embed_dm.set_footer(text="💠 نتمنى لك قضاء وقت ممتع 💠")
        await member.send(embed=embed_dm)
        welcomed_members.add(member.id)  # تسجيل العضو بعد الإرسال
        print(f"تم إرسال رسالة ترحيب في الخاص لـ {member.name}")
    except:
        print(f"❌ لا يمكن إرسال رسالة ترحيب لـ {member.name} (DM مغلق)")

    # رسالة Embed في قناة السيرفر
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

# تسجيل الأوامر عند تشغيل البوت
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    print("البوت جاهز للعمل ✅")

# أمر /send يرسل رسالة لكل عضو (Whitelist فقط)
@bot.tree.command(name="send", description="إرسال رسالة لجميع الأعضاء (Whitelist فقط)")
@app_commands.describe(message="اكتب الرسالة التي تريد إرسالها")
async def send(interaction: discord.Interaction, message: str):
    if interaction.user.id in WHITELIST:
        await interaction.response.defer(ephemeral=True)  # تأخير الرد
        sent_count = 0
        for member in interaction.guild.members:
            if not member.bot:
                try:
                    await member.send(message)  # الرسالة فقط
                    sent_count += 1
                    await asyncio.sleep(1)  # تأخير 1 ثانية لتجنب الحظر
                except:
                    print(f"لا يمكن إرسال رسالة لـ {member.name} (DM مغلق)")
        await interaction.followup.send(
            f"✅ تم إرسال الرسائل لـ {sent_count} عضو/أعضاء.", ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "❌ أنت غير مسموح لك باستخدام هذا الأمر.", ephemeral=True
        )

# تشغيل البوت
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ لم يتم العثور على التوكن! تأكد من إضافته في Environment Variables باسم TOKEN.")

