import json, hashlib
from telebot import TeleBot
from datetime import datetime
from time import time

BOT_TOKEN = "8684463452:AAHD24ZFRHIymIyAuEdnixUhyLN01uV54bc"
ADMIN_IDS = [7071414779]
COLLAB_IDS = [7071414779]

USERS_FILE = "users.json"
bot = TeleBot(BOT_TOKEN, parse_mode="HTML")

try:
    with open(USERS_FILE, "r") as f:
        USERS = json.load(f)
except:
    USERS = {}

def save():
    with open(USERS_FILE, "w") as f:
        json.dump(USERS, f)

def get_tun(uid): return USERS.get(uid, {}).get("tun", 0)
def cong(uid, v): USERS.setdefault(uid, {})["tun"] = get_tun(uid) + v; save()
def tru(uid, v): USERS.setdefault(uid, {})["tun"] = max(0, get_tun(uid) - v); save()
def set_tun(uid, v): USERS.setdefault(uid, {})["tun"] = max(0, v); save()

last_cmd = {}
def is_spam(uid):
    now = time()
    if uid in last_cmd and now - last_cmd[uid] < 2:
        return True
    last_cmd[uid] = now
    return False

def md5_ai(md5):
    md5 = md5.lower()
    digits = [int(c, 16) for c in md5]
    rules = [
        lambda: "Tài" if int(md5[-4:], 16) % 2 else "Xỉu",
        lambda: "Tài" if sum(digits) % 2 else "Xỉu",
        lambda: "Tài" if int(md5[13:19], 16) % 2 else "Xỉu",
        lambda: "Tài" if int(md5, 16) % 2 else "Xỉu",
        lambda: "Tài" if sum(digits[:8]) % 18 >= 11 else "Xỉu",
        lambda: "Tài" if digits.count(8) + digits.count(9) >= 8 else "Xỉu",
        lambda: "Tài" if bin(int(md5, 16)).count("1") >= 64 else "Xỉu",
        lambda: "Tài" if int(md5[-1], 16) >= 8 else "Xỉu",
        lambda: "Tài" if sum(digits[::2]) > sum(digits[1::2]) else "Xỉu",
        lambda: "Tài" if sum(int(c, 16) for c in md5[::-1]) % 2 else "Xỉu",
        lambda: "Tài" if max(digits) - min(digits) > 8 else "Xỉu",
        lambda: "Tài" if digits[0] % 2 == 0 else "Xỉu",
        lambda: "Tài" if digits[15] % 2 else "Xỉu",
        lambda: "Tài" if len(set(md5)) < 16 else "Xỉu",
        lambda: "Tài" if sum(digits) > 200 else "Xỉu",
        lambda: "Tài" if sum(digits[i] * i for i in range(32)) % 100 > 50 else "Xỉu",
        lambda: "Tài" if digits.count(1) + digits.count(3) + digits.count(5) > 10 else "Xỉu",
    ]
    results = [r() for r in rules]
    tai = results.count("Tài")
    xiu = len(rules) - tai
    return ("Tài" if tai > xiu else "Xỉu", round(100 * max(tai, xiu) / len(rules), 2))

def md5_vip(md5):
    md5 = md5.lower()
    digits = [int(c, 16) for c in md5]
    ascii_sum = sum(ord(c) for c in md5)
    rules = []
    rules.extend([  # 17 thường
        lambda: "Tài" if int(md5[-4:], 16) % 2 else "Xỉu",
        lambda: "Tài" if sum(digits) % 2 else "Xỉu",
        lambda: "Tài" if int(md5[13:19], 16) % 2 else "Xỉu",
        lambda: "Tài" if int(md5, 16) % 2 else "Xỉu",
        lambda: "Tài" if sum(digits[:8]) % 18 >= 11 else "Xỉu",
        lambda: "Tài" if digits.count(8) + digits.count(9) >= 8 else "Xỉu",
        lambda: "Tài" if bin(int(md5, 16)).count("1") >= 64 else "Xỉu",
        lambda: "Tài" if int(md5[-1], 16) >= 8 else "Xỉu",
        lambda: "Tài" if sum(digits[::2]) > sum(digits[1::2]) else "Xỉu",
        lambda: "Tài" if sum(int(c, 16) for c in md5[::-1]) % 2 else "Xỉu",
        lambda: "Tài" if max(digits) - min(digits) > 8 else "Xỉu",
        lambda: "Tài" if digits[0] % 2 == 0 else "Xỉu",
        lambda: "Tài" if digits[15] % 2 else "Xỉu",
        lambda: "Tài" if len(set(md5)) < 16 else "Xỉu",
        lambda: "Tài" if sum(digits) > 200 else "Xỉu",
        lambda: "Tài" if sum(digits[i] * i for i in range(32)) % 100 > 50 else "Xỉu",
        lambda: "Tài" if digits.count(1) + digits.count(3) + digits.count(5) > 10 else "Xỉu",
    ])
    rules.extend([  # 9 VIP nâng cao
        lambda: "Tài" if sum((i + 1) * int(c, 16) for i, c in enumerate(md5)) % 50 > 25 else "Xỉu",
        lambda: "Tài" if sum(int(md5[i], 16) ^ int(md5[31 - i], 16) for i in range(16)) % 30 > 15 else "Xỉu",
        lambda: "Tài" if bin(int(md5, 16)).count("1") > 64 else "Xỉu",
        lambda: "Tài" if ascii_sum % 100 > 49 else "Xỉu",
        lambda: "Tài" if md5[12:20].count('a') * 2 + md5[12:20].count('f') * 3 > 6 else "Xỉu",
        lambda: "Tài" if any(p in md5 for p in ['abc', '123', 'def', 'cba', '789']) else "Xỉu",
        lambda: "Tài" if sum(i * digits[i] for i in range(len(digits))) % 40 > 20 else "Xỉu",
        lambda: "Tài" if len(set(md5)) > 10 else "Xỉu",
        lambda: "Tài" if md5[10] in 'abcdef' else "Xỉu",
    ])
    results = [r() for r in rules]
    tai = results.count("Tài")
    xiu = len(results) - tai
    result = "Tài" if tai > xiu else "Xỉu"
    ratio = max(tai, xiu) / len(results)
    conf = 97 if ratio == 1.0 else 95 if ratio >= 0.8 else max(50, round(50 + ratio * 45))
    return result, conf

@bot.message_handler(commands=['start'])
def cmd_start(msg):
    uid = str(msg.from_user.id)
    cid = msg.chat.id
    if uid not in USERS:
        USERS[uid] = {"tun": 5}
        save()
    now = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
    bot.send_message(cid, f"""👋 <b>Chào mừng đến BOT TÀI XỈU AI!</b>

🎲 /tx &lt;mã MD5&gt; — Dự đoán thường (1 lượt)
🚀 /vip &lt;mã MD5&gt; — Dự đoán VIP (2 lượt)
🪙 /mytun — Xem lượt còn lại
🆔 /id — Xem ID

— <b>ADMIN</b> —
/addtun &lt;id&gt; &lt;lượt&gt;
/settun &lt;id&gt; &lt;lượt&gt;
/ctc &lt;id&gt; &lt;lượt&gt;
/thongke /danhsachxu

🕒 {now}
""", parse_mode="HTML")

@bot.message_handler(commands=['tx'])
def cmd_tx(msg):
    uid = str(msg.from_user.id)
    cid = msg.chat.id
    parts = msg.text.strip().split()
    if is_spam(uid): return
    if len(parts) != 2 or len(parts[1]) != 32 or not all(c in '0123456789abcdefABCDEF' for c in parts[1]):
        return bot.send_message(cid, "❌ Dùng: /tx <mã MD5 32 ký tự hex>")
    if get_tun(uid) <= 0:
        return bot.send_message(cid, "🚫 Hết lượt.")
    tru(uid, 1)
    result, conf = md5_ai(parts[1])
    bot.send_message(cid, f"🎲 DỰ ĐOÁN: <b>{result}</b> ({conf}%)\n💰 Còn: <code>{get_tun(uid)}</code>", parse_mode="HTML")

@bot.message_handler(commands=['vip'])
def cmd_vip(msg):
    uid = str(msg.from_user.id)
    cid = msg.chat.id
    parts = msg.text.strip().split()
    if is_spam(uid): return
    if len(parts) != 2 or len(parts[1]) != 32 or not all(c in '0123456789abcdefABCDEF' for c in parts[1]):
        return bot.send_message(cid, "❌ Dùng: /vip <mã MD5 32 ký tự hex>")
    if get_tun(uid) < 2:
        return bot.send_message(cid, "🚫 Cần ít nhất 2 lượt.")
    tru(uid, 2)
    result, conf = md5_vip(parts[1])
    tai_percent = conf if result == "Tài" else 100 - conf
    xiu_percent = 100 - tai_percent
    icon = "🔥" if result == "Tài" else "💧"
    text = f"""🎰 <b>KẾT QUẢ PHÂN TÍCH MD5</b> 🎰
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Người dùng: <code>{uid}</code>
🔐 MD5: <code>{parts[1]}</code>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[1] <b>TỶ LỆ TỔNG HỢP</b>
📈 <b>TÀI:</b> {tai_percent}%
📉 <b>XỈU:</b> {xiu_percent}%
━━━━━━━━━━━━━━━━━━━━━━
💬 <b>Gợi ý:</b> NÊN CHỌN “<b>{result}</b>” {icon}
💰 Còn: <code>{get_tun(uid)}</code>
"""
    bot.send_message(cid, text, parse_mode="HTML")

@bot.message_handler(commands=['mytun'])
def cmd_mytun(msg):
    uid = str(msg.from_user.id)
    bot.send_message(msg.chat.id, f"🪙 Lượt còn lại: <b>{get_tun(uid)}</b>", parse_mode="HTML")

@bot.message_handler(commands=['id'])
def cmd_id(msg):
    bot.send_message(msg.chat.id, f"🆔 ID: <code>{msg.from_user.id}</code>", parse_mode="HTML")

@bot.message_handler(commands=['addtun', 'settun'])
def cmd_add(msg):
    if msg.from_user.id not in ADMIN_IDS: return
    parts = msg.text.split()
    if len(parts) != 3: return
    uid, val = parts[1], int(parts[2])
    if msg.text.startswith("/addtun"):
        cong(uid, val)
    else:
        set_tun(uid, val)
    bot.send_message(msg.chat.id, f"✅ Done cho ID {uid}")

@bot.message_handler(commands=['ctc'])
def cmd_ctc(msg):
    from_id = str(msg.from_user.id)
    cid = msg.chat.id
    if msg.from_user.id not in COLLAB_IDS:
        return bot.send_message(cid, "🚫 Bạn không phải cộng tác viên.")
    parts = msg.text.strip().split()
    if len(parts) != 3:
        return bot.send_message(cid, "❌ Dùng: /ctc <id> <lượt>")
    to_id, amount_str = parts[1], parts[2]
    if not amount_str.isdigit(): return
    amount = int(amount_str)
    if get_tun(from_id) < amount:
        return bot.send_message(cid, f"🚫 Không đủ lượt. Bạn còn {get_tun(from_id)}")
    tru(from_id, amount)
    cong(to_id, amount)
    bot.send_message(cid, f"✅ Đã cấp {amount} lượt cho ID {to_id}. Còn lại: {get_tun(from_id)}")

@bot.message_handler(commands=['thongke'])
def thongke(msg):
    if msg.from_user.id not in ADMIN_IDS: return
    total = len(USERS)
    using = sum(1 for u in USERS if get_tun(u) > 0)
    bot.send_message(msg.chat.id, f"📊 Tổng user: {total}\n🔄 Đang dùng: {using}")

@bot.message_handler(commands=['danhsachxu'])
def danhsach(msg):
    if msg.from_user.id not in ADMIN_IDS: return
    lines = [f"{uid}: {USERS[uid]['tun']}" for uid in USERS]
    bot.send_message(msg.chat.id, "\n".join(lines))

if __name__ == "__main__":
    print("🤖 Bot đang chạy...")
    bot.infinity_polling()
