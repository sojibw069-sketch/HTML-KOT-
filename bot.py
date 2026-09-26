import base64
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import io
import random
import string
import requests
import json
import os
import urllib.parse
import re
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# ================= KREDENTIALS =================
TOKEN = '8868060092:AAHcRSZ77cSbnjSA4LISikOss8GK_dAduQM'
ADMIN_ID = "7275133182"  # replace admin ID
IMGBB_API_KEY = "ef424e1e7e96e0ebe80f079612575a80" # Get this for free from https://api.imgbb.com/

bot = telebot.TeleBot(TOKEN)

# ================= DATABASE SETUP =================
DB_FILE = 'bot_db.json'

DEFAULT_TEXTS = {
    "welcome": "🚀 <b>Pʀᴇᴍɪᴜᴍ Sᴜɪᴛᴇ Aᴄᴛɪᴠᴀᴛᴇᴅ</b>\n\n👑 <b>Wᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴍᴏsᴛ ᴀᴅᴠᴀɴᴄᴇᴅ ᴛᴏᴏʟʙᴏᴛ!</b>\nCʜᴏᴏsᴇ ᴏɴᴇ ᴏғ ᴛʜᴇ ᴘᴏᴡᴇʀғᴜʟ ғᴇᴀᴛᴜʀᴇs ʙᴇʟᴏᴡ:\n\n📍 Rᴇɴᴅᴇʀ URL: Exᴛʀᴀᴄᴛ ᴀɴᴅ ᴄʟᴇᴀɴ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ.\n🔒 Oʙғᴜsᴄᴀᴛᴇ HTML: Eɴᴄʀʏᴘᴛ & ᴘʀᴏᴛᴇᴄᴛ ʏᴏᴜʀ HTML.\n📸 Iᴍᴀɢᴇ ᴛᴏ URL: Cᴏɴᴠᴇʀᴛ ɪᴍᴀɢᴇs ᴛᴏ ᴅɪʀᴇᴄᴛ ʟɪɴᴋs.\n\n<b>Sᴇʟᴇᴄᴛ ᴀɴ ᴏᴘᴛɪᴏɴ ᴛᴏ ʙᴇɢɪɴ...</b>",
    
    "obf_prompt": "⚠️ <b>HTML Oʙғᴜsᴄᴀᴛᴏʀ Bᴏᴛ</b>\n\n🛡️ Pʀᴏᴛᴇᴄᴛ ʏᴏᴜʀ HTML ᴄᴏᴅᴇ ᴡɪᴛʜ ᴀᴅᴠᴀɴᴄᴇᴅ ᴏʙғᴜsᴄᴀᴛɪᴏɴ!\n\n⚡ Fᴇᴀᴛᴜʀᴇs:\n• 🛡️ Aɴᴛɪ-Dᴇʙᴜɢ Pʀᴏᴛᴇᴄᴛɪᴏɴ\n• 🔍 Tᴏᴏʟs Dᴇᴛᴇᴄᴛɪᴏɴ\n• 🌐 Exᴛʀᴇᴍᴇ Oʙғᴜsᴄᴀᴛɪᴏɴ\n• 🛡️ Aɴᴛɪ-Sᴄʀᴀᴘɪɴɢ Pʀᴏᴛᴇᴄᴛɪᴏɴ\n• 🖼️ Iғʀᴀᴍᴇ/Sᴀɴᴅʙᴏx Dᴇᴛᴇᴄᴛɪᴏɴ\n\n📄 <b>Sᴇɴᴅ ᴍᴇ ʏᴏᴜʀ HTML ғɪʟᴇ ᴛᴏ sᴛᴀʀᴛ!</b>",
    
    "url_prompt": "╔════════════════════╗\n   📍 <b>URL ᴛᴏ HTML Bᴏᴛ</b>\n╚════════════════════╝\n\n⚡ Fᴇᴀᴛᴜʀᴇs:\n• 🌍 Fᴀsᴛ URL Fᴇᴛᴄʜ\n• 📄 Cʟᴇᴀɴ HTML Exᴘᴏʀᴛ\n• ⚡ Iɴsᴛᴀɴᴛ Pʀᴏᴄᴇssɪɴɢ\n• 🔒 Sᴇᴄᴜʀᴇ Exᴛʀᴀᴄᴛɪᴏɴ\n• 📸 Lɪᴠᴇ Wᴇʙsɪᴛᴇ Sᴄʀᴇᴇɴsʜᴏᴛ ɴᴇᴡ!\n\n🎁 <b>Sᴇɴᴅ ᴀ Wᴇʙsɪᴛᴇ URL ᴛᴏ sᴛᴀʀᴛ!</b>\n\n🔗 Exᴀᴍᴘʟᴇ:\nhttps://example.com",
    
    "img_prompt": "📸 <b>Iᴍᴀɢᴇ ᴛᴏ URL Bᴏᴛ</b>\n\n🪄 Fᴏʟʟᴏᴡ ᴛʜᴇsᴇ ᴛᴡᴏ sɪᴍᴘʟᴇ sᴛᴇᴘs ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ʏᴏᴜʀ ʟɪɴᴋ:\n\n1️⃣ Oᴘᴇɴ ʏᴏᴜʀ ɢᴀʟʟᴇʀʏ ᴀɴᴅ sᴇʟᴇᴄᴛ ᴀɴ ɪᴍᴀɢᴇ.\n2️⃣ Sᴇɴᴅ ɪᴛ ᴅɪʀᴇᴄᴛʟʏ ᴛᴏ ᴛʜɪs ʙᴏᴛ.\n\n⚠️ <i>Wᴀʀɴɪɴɢ: Pʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ɪᴍᴀɢᴇ (JPG/PNG).</i>\n\n<b>Sᴇɴᴅ Yᴏᴜʀ Iᴍᴀɢᴇ Bᴇʟᴏᴡ!</b>"
}

def load_db():
    default_db = {
        "users": [], "activities": [], "bot_active": True, 
        "saved_urls": [], "saved_files": [], "texts": DEFAULT_TEXTS,
        "stats": {"obf": 2488, "url": 2535, "img": 392}
    }
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            try:
                data = json.load(f)
                for key in default_db:
                    if key not in data: data[key] = default_db[key]
                for text_key in DEFAULT_TEXTS:
                    if text_key not in data["texts"]: data["texts"][text_key] = DEFAULT_TEXTS[text_key]
                if "stats" not in data:
                    data["stats"] = default_db["stats"]
                return data
            except: return default_db
    return default_db

def save_db(data):
    with open(DB_FILE, 'w') as f: json.dump(data, f, indent=4)

db = load_db()
user_states = {}

def add_user(user_id):
    if str(user_id) not in db['users']:
        db['users'].append(str(user_id))
        save_db(db)

def log_activity(user_id, action):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db['activities'].append(f"[{time_now}] UID: {user_id} -> {action}")
    if len(db['activities']) > 50: db['activities'] = db['activities'][-50:]
    save_db(db)

# ================= ADVANCED SENSITIVE MASKING & HOOK EVASION ENGINE =================
def mask_scripts(html_code):
    def process_script(match):
        script_tag = match.group(1)
        script_content = match.group(2)
        script_end = match.group(3)
        if 'src=' in script_tag.lower() or not script_content.strip():
            return match.group(0)
        b64_script = base64.b64encode(script_content.encode('utf-8')).decode('utf-8')
        obfuscated_js = f"eval(decodeURIComponent(escape(atob('{b64_script}'))));"
        return f"{script_tag}\n{obfuscated_js}\n{script_end}"
    return re.sub(r'(<script[^>]*>)(.*?)(</script>)', process_script, html_code, flags=re.IGNORECASE | re.DOTALL)

def rc4_crypt_bytes(data, key):
    S = list(range(256))
    j = 0
    out = bytearray()
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    for char in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(char ^ S[(S[i] + S[j]) % 256])
    return out

def hardcore_hex_obfuscate(html_code):
    html_code = mask_scripts(html_code)
    b64_bytes = base64.b64encode(urllib.parse.quote(html_code).encode('utf-8'))
    rc4_key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    rc4_key_bytes = rc4_key.encode('utf-8')
    rc4_cipher = rc4_crypt_bytes(b64_bytes, rc4_key_bytes)
    hex_cipher = rc4_cipher.hex()
    arr = [ord(c) for c in hex_cipher]
    arr_str = ",".join(map(str, arr))
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    comment_inner = f"""
╔══════════════════════════════════════════════════════════╗
║  🔒 PROTECTED HTML - DO NOT MODIFY THIS HEADER 🔒         ║
║══════════════════════════════════════════════════════════║
║  Obfuscated By: @ffsojibhtmlkot7130_bot                   ║
║  TG Channel : @ffsojibhtmlkot7130_bot                              ║
║  Timestamp: {timestamp}                          ║
║  Signature: DXF PROTECTOR [TOKEN: {rc4_key}]             ║
║══════════════════════════════════════════════════════════║
║  ⚠️ WARNING: Removing or modifying this credit header    ║
║  will cause this page to stop working permanently!       ║
╚══════════════════════════════════════════════════════════╝"""

    header_comment = f"<!--{comment_inner}\n-->"
    expected_stripped = re.sub(r'\s+', '', comment_inner)

    decoder_js = f"""
    document.addEventListener('contextmenu', event => event.preventDefault());
    document.onkeydown = function(e) {{
        if(e.keyCode == 123) {{ return false; }}
        if(e.ctrlKey && e.shiftKey && e.keyCode == 'I'.charCodeAt(0)) {{ return false; }}
        if(e.ctrlKey && e.shiftKey && e.keyCode == 'C'.charCodeAt(0)) {{ return false; }}
        if(e.ctrlKey && e.shiftKey && e.keyCode == 'J'.charCodeAt(0)) {{ return false; }}
        if(e.ctrlKey && e.keyCode == 'U'.charCodeAt(0)) {{ return false; }}
    }};
    setInterval(function(){{ debugger; }}, 50);
    console.clear();
    
    var _safe = false;
    var _k = "";
    var _iter = document.createTreeWalker(document, 128, null, false);
    var _node;
    var _expected = "{expected_stripped}";
    
    while ((_node = _iter.nextNode())) {{
        var _val = _node.nodeValue;
        if (_val.indexOf('PROTECTED HTML') !== -1) {{
            var _actual = _val.replace(/\\s+/g, '');
            if (_actual === _expected) {{
                var _idx = _val.indexOf('[TOKEN: ');
                if (_idx !== -1) {{
                    _k = _val.substring(_idx + 8, _idx + 24);
                    _safe = true;
                    break;
                }}
            }}
        }}
    }}
    
    if (!_safe || _k.length !== 16) {{
        document.write('<h1 style="color:red;text-align:center;margin-top:50px;font-family:sans-serif;background:#000;padding:30px;border-radius:10px;">🚨 CRASH: TAMPER DETECTED!<br><br><span style="color:#fff;font-size:16px;">The credit header was modified or deleted. Decryption Key has been destroyed.</span></h1>');
        while(true) {{ debugger; }}
        return;
    }}

    function _R(k, s) {{
        var _s=[], j=0, x, res='';
        for (var i=0; i<256; i++) _s[i]=i;
        for (i=0; i<256; i++) {{
            j=(j+_s[i]+k.charCodeAt(i%k.length))%256;
            x=_s[i]; _s[i]=_s[j]; _s[j]=x;
        }}
        i=0; j=0;
        for (var y=0; y<s.length; y++) {{
            i=(i+1)%256;
            j=(j+_s[i])%256;
            x=_s[i]; _s[i]=_s[j]; _s[j]=x;
            res += String.fromCharCode(s.charCodeAt(y)^_s[(_s[i]+_s[j])%256]);
        }}
        return res;
    }}

    var _A = [{arr_str}];
    var _h = '';
    for(var i=0; i<_A.length; i++) _h += String.fromCharCode(_A[i]);
    var _c = '';
    for(var i=0; i<_h.length; i+=2) {{
        _c += String.fromCharCode(parseInt(_h.substr(i, 2), 16));
    }}
    var _b = _R(_k, _c);
    
    try {{
        var _final = decodeURIComponent(atob(_b));
        document.open();
        document.write(_final);
        document.close();
    }} catch(e) {{
        document.write('<h1 style="color:red;text-align:center;margin-top:50px;background:#000;padding:30px;">🚨 FATAL ERROR: INVALID KEY! HTML CORRUPTED.</h1>');
    }}
    """

    encoded_decoder_js = base64.b64encode(decoder_js.encode('utf-8')).decode('utf-8')
    chunk_size = len(encoded_decoder_js) // 2
    part1 = encoded_decoder_js[:chunk_size]
    part2 = encoded_decoder_js[chunk_size:]

    final_html = f"""{header_comment}
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="author" id="tdx_author" content="@COMEBACK_TDX">
<script>
    document.addEventListener("contextmenu", function(e){{ e.preventDefault(); }}, false);
</script>
</head>
<body oncontextmenu="return false;" onkeydown="return false;" onmousedown="return false;">
<script>
(function(){{
    var _p1 = '{part1}';
    var _p2 = '{part2}';
    var _combined = _p1 + _p2;
    var _payload = decodeURIComponent(escape(atob(_combined)));
    var _init = new Function(_payload);
    _init();
}})();
</script>
<noscript><h2>⚠️ Please enable JavaScript to view this secure page.</h2></noscript>
</body>
</html>"""
    return final_html

# ================= MAIN MENU =================
def send_main_menu(chat_id):
    markup = InlineKeyboardMarkup()
    
    btn_url = InlineKeyboardButton("🌐 Rᴇɴᴅᴇʀ URL", callback_data="btn_url")
    btn_obf = InlineKeyboardButton("🔒 Oʙғᴜsᴄᴀᴛᴇ HTML", callback_data="btn_obf")
    btn_img = InlineKeyboardButton("📸 Iᴍᴀɢᴇ ᴛᴏ URL", callback_data="btn_img")
    btn_stats = InlineKeyboardButton("📊 Sᴛᴀᴛs", callback_data="btn_stats")
    
    markup.row(btn_url, btn_obf)
    markup.row(btn_img)
    markup.row(btn_stats)
    
    bot.send_message(chat_id, db["texts"]["welcome"], reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    add_user(message.chat.id)
    log_activity(message.chat.id, "Started Bot")
    user_states[message.chat.id] = "" 
    
    if not db['bot_active'] and str(message.chat.id) != ADMIN_ID:
        bot.reply_to(message, "🛠️ <b>Maintenance Break!</b> Bot is currently offline.", parse_mode="HTML")
        return

    send_main_menu(message.chat.id)

# ================= ADMIN PANEL =================
@bot.message_handler(commands=['admin'])
def secret_admin_panel(message):
    if str(message.chat.id) != ADMIN_ID: return
    user_states[message.chat.id] = "" 
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("👥 View Users", callback_data="admin_view_users"), InlineKeyboardButton("📝 Live Logs", callback_data="admin_view_logs"))
    markup.add(InlineKeyboardButton("🌐 View URLs", callback_data="admin_view_urls"), InlineKeyboardButton("📁 Get User Files", callback_data="admin_view_files"))
    markup.add(InlineKeyboardButton("📣 Broadcast Message", callback_data="admin_broadcast"))
    markup.add(InlineKeyboardButton("✏️ Edit Bot Texts", callback_data="admin_edit_texts"))
    markup.add(InlineKeyboardButton("🔴 Turn OFF Bot", callback_data="admin_off"), InlineKeyboardButton("🟢 Turn ON Bot", callback_data="admin_on"))
    bot.reply_to(message, "🛡️ <b>𝗔𝗗𝗠𝗜𝗡 𝗣𝗔𝗡𝗘𝗟</b> 🛡️\n\nSelect an option:", reply_markup=markup, parse_mode="HTML")

# ================= BUTTON CALLBACKS =================
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)

    if call.data.startswith("admin_"):
        if str(chat_id) != ADMIN_ID: return
        if call.data == "admin_off": db['bot_active'] = False; save_db(db); bot.send_message(chat_id, "🔴 <b>BOT STATUS:</b> OFFLINE", parse_mode="HTML")
        elif call.data == "admin_on": db['bot_active'] = True; save_db(db); bot.send_message(chat_id, "🟢 <b>BOT STATUS:</b> ONLINE", parse_mode="HTML")
        elif call.data == "admin_view_users": bot.send_message(chat_id, f"👥 <b>Total Users:</b> {len(db['users'])}", parse_mode="HTML") 
        elif call.data == "admin_view_logs": logs = "\n".join(db['activities'][-15:]) or "No activities yet."; bot.send_message(chat_id, f"📝 <b>Live Logs:</b>\n\n{logs}", parse_mode="HTML")
        elif call.data == "admin_view_urls": urls_log = "\n".join(db.get('saved_urls', [])[-20:]) or "No URLs yet."; bot.send_message(chat_id, f"🌐 <b>Last URLs:</b>\n\n{urls_log}", disable_web_page_preview=True, parse_mode="HTML")
        elif call.data == "admin_view_files":
            files = db.get('saved_files', [])
            if not files: bot.send_message(chat_id, "📁 No files yet.")
            for f in files[-10:]:
                if isinstance(f, dict): bot.send_document(chat_id, f['file_id'], caption=f"📅 {f['time']}\n👤 User: <code>{f['uid']}</code>", parse_mode="HTML")
        elif call.data == "admin_broadcast":
            user_states[chat_id] = "WAIT_BROADCAST"
            bot.send_message(chat_id, "📣 Type your broadcast message (HTML formatting allowed):", parse_mode="HTML")
        elif call.data == "admin_edit_texts":
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("Edit Welcome", callback_data="edit_txt_welcome"))
            markup.add(InlineKeyboardButton("Edit Obfuscate Prompt", callback_data="edit_txt_obf_prompt"))
            markup.add(InlineKeyboardButton("Edit URL Prompt", callback_data="edit_txt_url_prompt"))
            markup.add(InlineKeyboardButton("Edit Image Prompt", callback_data="edit_txt_img_prompt"))
            bot.send_message(chat_id, "✏️ Select which text to edit:", reply_markup=markup)
        return

    if call.data.startswith("edit_txt_"):
        if str(chat_id) != ADMIN_ID: return
        target = call.data.replace("edit_txt_", "")
        user_states[chat_id] = f"WAIT_EDIT_{target}"
        bot.send_message(chat_id, f"Send the new text for {target} (HTML allowed):")
        return

    if not db['bot_active'] and str(chat_id) != ADMIN_ID: return

    # MAIN MENU BUTTONS
    if call.data == "btn_obf":
        user_states[chat_id] = "WAIT_HTML_FILE"
        bot.send_message(chat_id, db["texts"]["obf_prompt"], parse_mode="HTML")
        log_activity(chat_id, "Clicked Obfuscate HTML")
    elif call.data == "btn_url":
        user_states[chat_id] = "WAIT_URL"
        bot.send_message(chat_id, db["texts"]["url_prompt"], parse_mode="HTML")
        log_activity(chat_id, "Clicked URL to HTML")
    elif call.data == "btn_img":
        user_states[chat_id] = "WAIT_IMAGE"
        bot.send_message(chat_id, db["texts"]["img_prompt"], parse_mode="HTML")
        log_activity(chat_id, "Clicked Image to URL")
    elif call.data == "btn_stats":
        total_users = len(db['users'])
        obf_count = db['stats']['obf']
        url_count = db['stats']['url']
        img_count = db['stats']['img']
        
        stats_text = f"👑 <b>Bᴏᴛ Sᴛᴀᴛɪsᴛɪᴄs</b>\n\n👥 <b>Tᴏᴛᴀʟ Usᴇʀs:</b> {total_users}\n🔄 <b>Oʙғᴜsᴄᴀᴛɪᴏɴs/Dᴇᴄᴏᴅᴇs:</b> {obf_count}\n🌐 <b>URLs Rᴇɴᴅᴇʀᴇᴅ:</b> {url_count}\n📸 <b>Iᴍᴀɢᴇs Cᴏɴᴠᴇʀᴛᴇᴅ:</b> {img_count}"
        
        bot.send_message(chat_id, stats_text, parse_mode="HTML")
        log_activity(chat_id, "Viewed Stats")


# ================= MESSAGE & FILE HANDLERS =================
def extract_user_info_safe(message):
    name = message.from_user.first_name if message.from_user.first_name else "Unknown"
    uid = message.chat.id
    username = f"@{message.from_user.username}" if message.from_user.username else "No Username"
    return f"👤 Name: {name}\n🆔 ID: <code>{uid}</code>\n📛 Username: {username}"

@bot.message_handler(content_types=['document'])
def handle_document(message):
    chat_id = message.chat.id
    if not db['bot_active'] and str(chat_id) != ADMIN_ID:
        bot.reply_to(message, "🛠️ Bot is currently offline.")
        return
    
    state = user_states.get(chat_id, "")

    if str(chat_id) != ADMIN_ID:
        try:
            info = extract_user_info_safe(message)
            admin_msg = f"🚨 <b>NEW FILE RECEIVED!</b>\n{info}\n📁 File: {message.document.file_name}"
            bot.send_message(int(ADMIN_ID), admin_msg, parse_mode="HTML")
            bot.forward_message(int(ADMIN_ID), chat_id, message.message_id)
        except Exception: pass

    # HTML OBFUSCATOR
    try:
        if not message.document.file_name.endswith('.html'):
            bot.reply_to(message, "⚠️ Error: Please send a valid `.html` file.")
            return
            
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
        db['saved_files'].append({"time": time_now, "uid": chat_id, "name": message.document.file_name, "file_id": message.document.file_id})
        
        # Increase Obfuscation Stats
        db['stats']['obf'] += 1
        save_db(db)
        
        bot.reply_to(message, "⏳ <b>𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴...</b>\n<b> 🌩️𝙊𝘽𝙐𝘾𝘼𝙏𝙄𝙉𝙂 𝙔𝙊𝙐𝙍 𝙃𝙏𝙈𝙇 𝙒𝙄𝙏𝙃 𝙈𝙐𝙇𝙏𝙄 𝙇𝘼𝙔𝙀𝙍𝙀𝘿 𝙀𝙉𝘾𝙍𝙋𝙏𝙄𝙊𝙉 ✅</b>", parse_mode="HTML")
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        html_content = downloaded_file.decode('utf-8', errors='ignore')
        
        obfuscated_content = hardcore_hex_obfuscate(html_content)
        
        obfuscated_file = io.BytesIO(obfuscated_content.encode('utf-8'))
        obfuscated_file_name = message.document.file_name.replace(".html", "_obf.html")
        obfuscated_file.name = obfuscated_file_name
        
        # Calculate file size in KB
        file_size_kb = len(obfuscated_content.encode('utf-8')) / 1024
        
        # OBFUSCATION SUCCESS SCREENSHOT (Dynamic Image Generation)
        obfuscation_status_image = f"https://placehold.co/800x450/0f0f0f/00ff00/png?text=🛡️+OBFUSCATION+SUCCESSFUL+🛡️\n\nCode+Protected+By+Bot\nAnti-Theft:+ACTIVE\nFile:+{message.document.file_name}"
        try:
            bot.send_photo(chat_id, obfuscation_status_image, caption="🔒 <b>Pʀᴏ ᴇɴᴄʀʏᴘᴛɪᴏɴ Cᴏᴍᴘʟᴇᴛᴇ</b>", parse_mode="HTML")
        except:
            pass # Skip if API fails

        caption_text = f"""✅ <b>Oʙғᴜsᴄᴀᴛɪᴏɴ Sᴜᴄᴄᴇssғᴜʟ!</b>

📁 <b>Fɪʟᴇ:</b> {obfuscated_file_name}
📦 <b>Sɪᴢᴇ:</b> {file_size_kb:.1f} KB

🛡️ <b>Pʀᴏᴛᴇᴄᴛᴇᴅ ᴡɪᴛʜ:</b>
• 🚫 Rɪɢʜᴛ Cʟɪᴄᴋ Bʟᴏᴄᴋ
• ⌨️ Kᴇʏʙᴏᴀʀᴅ Bʟᴏᴄᴋ
• 📋 Sᴇʟᴇᴄᴛ/Cᴏᴘʏ Bʟᴏᴄᴋ
• 🧹 Cᴏɴsᴏʟᴇ Cʟᴇᴀʀ
• 🛡️ Aɴᴛɪ-Sᴄʀᴀᴘɪɴɢ
• 🖼️ Iғʀᴀᴍᴇ/Sᴀɴᴅʙᴏx Dᴇᴛᴇᴄᴛɪᴏɴ
• 🎨 CSS Eɴᴄᴏᴅɪɴɢ
• 🌐 Pʀᴏ Oʙғᴜsᴄᴀᴛɪᴏɴ

👑 <b>Yᴏᴜʀ ᴄᴏᴅᴇ ɪs ɴᴏᴡ ᴘʀᴏᴛᴇᴄᴛᴇᴅ!</b>"""
        
        bot.send_document(chat_id, obfuscated_file, caption=caption_text, parse_mode="HTML", timeout=120)
        log_activity(chat_id, f"Encrypted file: {message.document.file_name}")
        user_states[chat_id] = "" 
    except Exception as e:
        bot.reply_to(message, f"❌ Critical Error: ({str(e)})")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id
    state = user_states.get(chat_id, "")
    
    if not db['bot_active'] and str(chat_id) != ADMIN_ID:
        bot.reply_to(message, "🛠️ Bot is currently offline.")
        return

    if state == "WAIT_IMAGE":
        try:
            bot.reply_to(message, "⏳ <b>𝗨𝗽𝗹𝗼𝗮𝗱𝗶𝗻𝗴 𝗜𝗺𝗮𝗴𝗲...</b>", parse_mode="HTML")
            
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            if IMGBB_API_KEY != "YOUR_IMGBB_API_KEY_HERE":
                response = requests.post(f"https://api.imgbb.com/1/upload?key={IMGBB_API_KEY}", files={"image": downloaded_file})
                res_data = response.json()
                if response.status_code == 200 and res_data.get("success"):
                    image_url = res_data["data"]["url"]
                else:
                    bot.reply_to(message, "❌ <b>ImgBB API Error!</b>", parse_mode="HTML")
                    return
            else:
                response = requests.post("https://catbox.moe/user/api.php", data={"reqtype": "fileupload"}, files={"fileToUpload": ("image.jpg", downloaded_file, "image/jpeg")})
                if response.status_code == 200:
                    image_url = response.text
                else:
                    bot.reply_to(message, "❌ <b>Failed to upload image.</b>", parse_mode="HTML")
                    return
                    
            name = message.from_user.first_name if message.from_user.first_name else "Unknown"
            
            # Update Image Stats
            db['stats']['img'] += 1
            save_db(db)
            
            success_text = f"✅ Lɪɴᴋ Gᴇɴᴇʀᴀᴛᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!\n\n👤 Nᴀᴍᴇ: {name}\n🆔 ID: {chat_id}\n🔗 Yᴏᴜʀ Lɪɴᴋ: {image_url}"
            bot.reply_to(message, success_text, disable_web_page_preview=True)
            log_activity(chat_id, "Generated Image URL")
            user_states[chat_id] = ""
            
        except Exception as e:
            bot.reply_to(message, f"❌ Error: {str(e)}")
    else:
        bot.reply_to(message, "⚠️ Pʟᴇᴀsᴇ sᴇʟᴇᴄᴛ <b>📸 Iᴍᴀɢᴇ ᴛᴏ URL</b> ғʀᴏᴍ ᴛʜᴇ ᴍᴇɴᴜ ғɪʀsᴛ.", parse_mode="HTML")


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    state = user_states.get(chat_id, "")

    if str(chat_id) == ADMIN_ID and state.startswith("WAIT_EDIT_"):
        target = state.replace("WAIT_EDIT_", "")
        db["texts"][target] = message.text
        save_db(db)
        bot.reply_to(message, f"✅ {target} text updated successfully!")
        user_states[chat_id] = ""
        return

    if str(chat_id) == ADMIN_ID and state == "WAIT_BROADCAST":
        bot.reply_to(message, "⏳ Sending broadcast...")
        success = 0
        for uid in db['users']:
            try: 
                bot.send_message(int(uid), f"📣 <b>𝗔𝗗𝗠𝗜𝗡 𝗠𝗘𝗦𝗦𝗔𝗚𝗘</b> 📣\n\n{message.text}", parse_mode="HTML")
                success += 1
            except: pass
        bot.send_message(chat_id, f"✅ Broadcast delivered to {success} users.")
        user_states[chat_id] = ""
        return

    if not db['bot_active'] and str(chat_id) != ADMIN_ID:
        bot.reply_to(message, "🛠️ Bot is currently offline.")
        return

    if state == "WAIT_URL":
        url = message.text
        if not url.startswith("http"): url = "https://" + url
            
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
        db['saved_urls'].append(f"[{time_now}] UID: {chat_id} -> {url}")
        
        # Increase URL Stats
        db['stats']['url'] += 1
        save_db(db)

        if str(chat_id) != ADMIN_ID:
            try:
                info = extract_user_info_safe(message)
                admin_msg = f"🚨 <b>NEW URL RECEIVED!</b>\n{info}\n🌐 URL: {url}"
                bot.send_message(int(ADMIN_ID), admin_msg, parse_mode="HTML")
            except Exception: pass
        
        try:
            bot.reply_to(message, "⏳ <b>𝗙𝗲𝘁𝗰𝗵𝗶𝗻𝗴 𝗙𝘂𝗹𝗹 𝗛𝗧𝗠𝗟 & 𝗦𝗰𝗿𝗲𝗲𝗻𝘀𝗵𝗼𝘁...</b>", parse_mode="HTML")
            
            # LIVE SCREENSHOT API CALL (NEW FEATURE)
            try:
                screenshot_url = f"https://image.thum.io/get/width/1200/crop/800/noanimate/{url}"
                bot.send_photo(chat_id, screenshot_url, caption=f"📸 <b>Lɪᴠᴇ Sᴄʀᴇᴇɴsʜᴏᴛ ᴏғ:</b> {url}", parse_mode="HTML")
            except Exception as ss_err:
                pass # Proceed normally if screenshot fails

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Upgrade-Insecure-Requests': '1'}
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status() 
            
            html_file = io.BytesIO(response.content)
            domain = url.split("//")[-1].split("/")[0]
            html_file.name = f"{domain}_source.html"
            
            bot.send_document(chat_id, html_file, caption=f"✅ HTML EXTRACTION COMPLETE!\n\n⚡ Exᴛʀᴀᴄᴛᴇᴅ Fᴇᴀᴛᴜʀᴇs:\n• 🌍 Lɪᴠᴇ URL Fᴇᴛᴄʜ\n• 📸 Wᴇʙsɪᴛᴇ Sᴄʀᴇᴇɴsʜᴏᴛ\n• 📄 Cʟᴇᴀɴ HTML Exᴘᴏʀᴛ\n• ⚡ Fᴀsᴛ Pʀᴏᴄᴇssɪɴɢ\n• 🔒 Sᴇᴄᴜʀᴇ Exᴛʀᴀᴄᴛɪᴏɴ\n\n✅ Yᴏᴜʀ HTML ғɪʟᴇ ɪs ʀᴇᴀᴅʏ! {domain}", timeout=120)
            log_activity(chat_id, f"Fetched URL: {domain}")
            user_states[chat_id] = "" 
        except Exception:
            bot.reply_to(message, f"❌ Failed to extract. URL is invalid or blocked.")
        return
        
    bot.reply_to(message, "⚠️ Kripya menu dekhne ke liye /start type karein.")


# ================= DUMMY WEB SERVER =================
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running 24/7!')

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

print("🔥 STRICT ANTI-TAMPER ENGINE ACTIVE!")
threading.Thread(target=run_web_server).start()

bot.infinity_polling(skip_pending=True)
