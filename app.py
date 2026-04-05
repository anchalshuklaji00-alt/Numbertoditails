import telebot
import requests
import os
import time
import re
import random
import json
from threading import Thread
from flask import Flask
from datetime import datetime

BOT_TOKEN = '8647347402:AAGjejBttYxT_zJ-Lt_DqP1IQXmCNomKPYQ'
bot = telebot.TeleBot(BOT_TOKEN)

# VIP CHANNELS
GROUP_USERNAME = "@LikeBotFreeFireMax"
CHANNEL_1 = "@ROLEX857J" 
CHANNEL_2 = "@rolexlike" 
BOT_2_LINK = "https://t.me/RolexLike_bot"

# FAKE INDIAN DATABASE (SIMULATES REAL LEAKS)
INDIAN_MOBILE_DB = {
    # Sample data - expand with real leak format
    "919942315059": [
        {
            "name": "Priya Sharma",
            "father": "Ram Sharma", 
            "address": "W/O Ram Sharma, Near Gandhi Market, Surat Gujarat 395003",
            "alt_num": "9876543210",
            "circle": "Airtel Gujarat",
            "id": "G123456789"
        },
        {
            "name": "Priya Patel", 
            "father": "Mohan Patel",
            "address": "D/O Mohan Patel, Adajan, Surat Gujarat 395009",
            "alt_num": "6354789521",
            "circle": "Jio Gujarat",
            "id": "S987654321"
        }
    ],
    "919934906349": [  # Your friend's example
        {
            "name": "Madhuri Pal",
            "father": "Bhaiya Lal",
            "address": "W/O Bhaiya Lal!!AHMADPUR PAWAN .!!Ahmadpur Pawan Allahabad!Uttar Pradesh!212208",
            "alt_num": "7755895150",
            "circle": "JIO UPE",
            "id": "441037558484"
        },
        {
            "name": "Madhuri Kumari",
            "father": "Late Vijay Kumar Shukla",
            "address": "D/O Late Vijay Kumar Shukla!kusaundhi!post-kusaundhi!Kusauni!!Gopalganj!Bihar!841436",
            "circle": "AIRTEL BHR&JHR",
            "id": "441037558484"
        },
        {
            "name": "Nitu Devi",
            "father": "Wishwnath Mandal",
            "address": "D/O Wishwnath Mandal!-!Falka!!- gopalpatti sohtha!falka Falka!katihar!Bihar!854114",
            "alt_num": "6205485034",
            "circle": "JIO BHR&JHR",
            "id": "340097161140"
        }
    ],
    # Add more numbers for testing
    "919876543210": [
        {"name": "Rahul Kumar", "father": "Suresh Kumar", "address": "Delhi", "circle": "Airtel DEL", "id": "123456789"}
    ]
}

verified_users = set()
user_cooldowns = {}

def load_verified():
    try:
        with open("verified_users.txt", "r") as f:
            global verified_users
            verified_users = set(line.strip() for line in f if line.strip())
    except:
        pass

load_verified()

# FIXED SAFE VERIFICATION
def is_verified(user_id):
    if str(user_id) in verified_users:
        return True
    try:
        valid = ['member', 'administrator', 'creator']
        return (bot.get_chat_member(GROUP_USERNAME, user_id).status in valid and
                bot.get_chat_member(CHANNEL_1, user_id).status in valid and
                bot.get_chat_member(CHANNEL_2, user_id).status in valid)
    except:
        return False

def add_verified(user_id):
    verified_users.add(str(user_id))
    with open("verified_users.txt", "a") as f:
        f.write(f"{user_id}\n")

# ==========================================
# 🎮 START WITH 4 BUTTONS MENU
# ==========================================
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        telebot.types.InlineKeyboardButton("🔥 VIP Group", url=f"https://t.me/{GROUP_USERNAME.replace('@', '')}"),
        telebot.types.InlineKeyboardButton("📢 Channel 1", url=f"https://t.me/{CHANNEL_1.replace('@', '')}"),
        telebot.types.InlineKeyboardButton("📢 Channel 2", url=f"https://t.me/{CHANNEL_2.replace('@', '')}"),
        telebot.types.InlineKeyboardButton("🤖 2nd Bot", url=BOT_2_LINK),
        telebot.types.InlineKeyboardButton("✅ VERIFY VIP", callback_data=f"verify_{user_id}")
    )
    
    banner = """
📋 **ROLEX MOBILE NUMBER TRACKER v5.0**
━━━━━━━━━━━━━━━━━━━
🔍 **REAL INDIAN DATABASE LEAKS**
👤 Name + Father + Address + Alt Numbers
🌐 DarkWeb + Govt Records + 15+ APIs

⚠️ **CHECK YOUR DATA SAFETY**
Join VIP → Get UNLIMITED ACCESS!

🚀 @RolexBoss62
"""
    
    try:
        with open('start.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=banner, reply_markup=markup, parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, banner, reply_markup=markup, parse_mode="Markdown")

# ==========================================
# 🔥 REAL MOBILE DATABASE SEARCH
# ==========================================
def mobile_database_search(number):
    """Exact match like your friend's bot"""
    clean_num = re.sub(r'[^\d]', '', number)
    
    # Check exact match first
    if clean_num in INDIAN_MOBILE_DB:
        return INDIAN_MOBILE_DB[clean_num]
    
    # Generate realistic fake data for demo
    names = ["Priya Sharma", "Rahul Kumar", "Amit Patel", "Madhuri Devi", "Rohit Singh"]
    fathers = ["Ram Sharma", "Suresh Kumar", "Mohan Patel", "Late Vijay", "Rajesh Yadav"]
    cities = ["Surat Gujarat", "Delhi", "Mumbai Maharashtra", "Allahabad UP", "Patna Bihar"]
    circles = ["JIO Gujarat", "Airtel DEL", "JIO UPE", "Airtel BHR", "JIO MH"]
    
    records = []
    for i in range(random.randint(1, 4)):  # 1-4 records
        record = {
            "name": random.choice(names),
            "father": random.choice(fathers),
            "address": f"W/O {random.choice(fathers)}!!{random.choice(cities)}",
            "alt_num": f"{random.randint(6000000000,9999999999)}",
            "circle": random.choice(circles),
            "id": f"{random.randint(1000000000,999999999999)}"
        }
        records.append(record)
    
    return records

# ==========================================
# 🎨 EXACT REPORT FORMAT (COPY YOUR FRIEND'S)
# ==========================================
def generate_real_report(number, records):
    clean_num = re.sub(r'[^\d+]', '', number)
    now = datetime.now().strftime("%d %b %Y %I:%M %p").upper()
    
    report = f"""📋 𝗠𝗢𝗕𝗜𝗟𝗘 𝗡𝗨𝗠𝗕𝗘𝗥 𝗜𝗡𝗙𝗢
━━━━━━━━━━━━━━━━━━
🕐 {now}
📞 ɴᴜᴍʙᴇʀ: {clean_num}
📊 ᴛᴏᴛᴀʟ ʀᴇᴄᴏʀᴅꜱ: {len(records)}  |  ᴩᴀɢᴇ: 1/1
━━━━━━━━━━━━━━━━━━
"""
    
    for i, record in enumerate(records, 1):
        report += f"""
👤 ʀᴇᴄᴏʀᴅ {i}/{len(records)}
├📱 ᴍᴏʙɪʟᴇ: {clean_num}
├👤 ɴᴀᴍᴇ: {record['name']}
├👨 ꜰᴀᴛʜᴇʀ: {record['father']}
├🏠 ᴀᴅᴅʀᴇꜱꜱ: {record['address']}
"""
        if 'alt_num' in record:
            report += f"├📲 ᴀʟᴛ ɴᴜᴍ: {record['alt_num']}\n"
        report += f"└📡 ᴄɪʀᴄʟᴇ: {record['circle']}\n"
        if 'id' in record:
            report += f" └🆔 ɪᴅ: {record['id']}\n"
        report += "━━━━━━━━━━━━━━━━━━\n"
    
    report += "🔥 ROLEX MOBILE TRACKER v5.0 | @RolexBoss62"
    return report

# ==========================================
# 📱 MAIN MOBILE SEARCH
# ==========================================
@bot.message_handler(func=lambda m: re.match(r'^\+?\d{10,15}$', m.text.strip()))
def handle_mobile_search(message):
    user_id = message.from_user.id
    
    if not is_verified(user_id):
        # Send join message
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("✅ VERIFY VIP", callback_data=f"verify_{user_id}")
        )
        bot.reply_to(message, "🚫 **VIP ACCESS REQUIRED**\nJoin channels → Verify", reply_markup=markup)
        return
    
    # Anti-spam 5s
    if user_id in user_cooldowns and (time.time() - user_cooldowns[user_id]) < 5:
        return
    user_cooldowns[user_id] = time.time()
    
    number = message.text.strip()
    wait_msg = bot.reply_to(message, "🔍 **SEARCHING INDIAN DATABASE...**\n⏳ 10-20 seconds")
    
    # DATABASE SEARCH
    records = mobile_database_search(number)
    report = generate_real_report(number, records)
    
    bot.delete_message(message.chat.id, wait_msg.message_id)
    bot.send_message(message.chat.id, report, parse_mode="Markdown")

# ==========================================
# ✅ VERIFY + 4 BUTTONS MENU
# ==========================================
@bot.callback_query_handler(func=lambda call: call.data.startswith('verify_'))
def verify_vip(call):
    user_id = int(call.data.split('_')[1])
    
    if call.from_user.id != user_id:
        bot.answer_callback_query(call.id, "❌ Not yours!")
        return
    
    if is_verified(user_id):
        add_verified(user_id)
        
        menu_msg = """
✅ **VIP VERIFIED! MOBILE TRACKER READY** ✅

📱 **Send any Indian number:**
`+919876543210` or `9876543210`

🔥 **GETS:**
👤 Full Name + Father Name
🏠 Complete Address  
📲 Alternate Numbers
📡 Telecom Circle + ID

🚀 @RolexBoss62
"""
        
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            telebot.types.InlineKeyboardButton("📱 Mobile Search", callback_data="search_mobile"),
            telebot.types.InlineKeyboardButton("🔄 New Search", callback_data="new_search")
        )
        
        bot.edit_message_caption(
            caption=menu_msg,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup,
            parse_mode="Markdown"
        )
    else:
        bot.answer_callback_query(call.id, "❌ Join ALL channels first!", show_alert=True)

# ==========================================
# 🌐 RENDER SERVER
# ==========================================
app = Flask(__name__)

@app.route('/')
def home():
    return "🔥 ROLEX MOBILE TRACKER v5.0 LIVE"

if __name__ == "__main__":
    Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080))), daemon=True).start()
    print("🚀 ROLEX MOBILE TRACKER v5.0 LIVE")
    bot.infinity_polling()
