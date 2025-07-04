import telebot
from telebot import types
import json
import os
import threading
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# بيانات البوت والمطور
TOKEN = "7869769364:AAGWDK4orRgxQDcjfEHScbfExgIt_Ti8ARs"
ADMIN_ID = 6964741705
ADMIN_PASSWORD = "admin"
WALLET_ID = "6964741705"
SUBSCRIPTION_IMAGE = "subscription.jpg"
USERS_FILE = "users.json"
TEXTS_FILE = "texts.json"
SESSIONS = {}

bot = telebot.TeleBot(TOKEN)

# إنشاء الملفات المطلوبة إذا لم تكن موجودة
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

if not os.path.exists(TEXTS_FILE):
    texts = {
        "welcome": "👋 مرحباً بك في بوت التوصيات.",
        "subscription_msg": f"💳 للاشتراك أرسل 3 USDT إلى المحفظة: `{WALLET_ID}`",
        "wait_msg": "⏳ تم إرسال طلب التفعيل. يرجى الانتظار...",
        "activated_msg": "✅ تم تفعيل اشتراكك في البوت بنجاح 🌟",
        "rejected_msg": "⛔️ لم يتم تأكيد وصول المبلغ. الرجاء التأكد من الإيداع وإرسال صورة واضحة مرة أخرى."
    }
    with open(TEXTS_FILE, "w", encoding="utf-8") as f:
        json.dump(texts, f, ensure_ascii=False)

if not os.path.exists("pending"):
    os.makedirs("pending")

# أدوات المساعدة
def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f)

def get_analysis():
    return "Strong Sell"

def get_indicator_details():
def safe_get(indicator):
    return indicator if indicator else {"value": "?", "signal": "?"}

e20 = safe_get(indicators.get("EMA20"))
e50 = safe_get(indicators.get("EMA50"))
rsi = safe_get(indicators.get("RSI(14)"))
boll = safe_get(indicators.get("Bollinger Bands"))
trend = indicators.get("Trend", {"value": "?", "signal": "?"})
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table", class_="technicalIndicatorsTbl")
        rows = table.find_all("tr")[1:]
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                name = cols[0].text.strip()
                value = cols[1].text.strip()
                signal = cols[2].text.strip()
                if name in indicators:
                    indicators[name] = {"value": value, "signal": signal}
    except Exception as e:
        print("خطأ في جلب المؤشرات:", e)
    return indicators

def explain_indicator(name, value, signal):
    try:
        val = float(value)
    except:
        return "🔍 لا يمكن تفسير القيمة."
    if "EMA" in name:
        if signal == "Buy":
            return "🔍 السعر أعلى من المتوسط → الاتجاه صاعد ✅"
        elif signal == "Sell":
            return "🔍 السعر أقل من المتوسط → الاتجاه هابط 🔻"
        else:
            return "🔍 قريب من المتوسط → سوق غير واضح ⏳"
    if "RSI" in name:
        if val < 30:
            return "🔍 RSI منخفض → تشبّع بيعي → احتمال صعود 🔼"
        elif val > 70:
            return "🔍 RSI مرتفع → تشبّع شرائي → احتمال هبوط 🔽"
        else:
            return "🔍 RSI طبيعي → لا ضغط حالياً 🔁"
    if "Bollinger" in name:
        if signal == "Buy":
            return "🔍 قريب من الحد السفلي → ارتداد صعودي محتمل 🔼"
        elif signal == "Sell":
            return "🔍 قريب من الحد العلوي → ضغط بيعي 🔽"
        else:
            return "🔍 داخل النطاق → لا ضغط حالي 🔍"
    return "🔍 لا يوجد تفسير."

def explain_trend(signal):
    if signal == "Buy":
        return "🔍 السوق في اتجاه صاعد حالياً ✅"
    elif signal == "Sell":
        return "🔍 السوق في اتجاه هابط حالياً 🔻"
    elif signal == "Neutral":
        return "🔍 لا يوجد اتجاه واضح (سوق متذبذب) ⏳"
    return "🔍 لا يمكن تفسير الاتجاه"

def get_recommendation_message(signal, indicators):
    emoji_map = {
        "Buy": "🟢", "Strong Buy": "🟢",
        "Sell": "🔴", "Strong Sell": "🔴",
        "Neutral": "🟡"
    }
    explain = {
        "Buy": "📈 المؤشرات تشير إلى اتجاه صاعد → شراء",
        "Strong Buy": "📈 المؤشرات بقوة لصالح الشراء",
        "Sell": "📉 المؤشرات تشير إلى هبوط → بيع",
        "Strong Sell": "📉 المؤشرات بقوة لصالح البيع",
        "Neutral": "⏳ السوق غير واضح → انتظار"
    }

    now = datetime.now().strftime("%I:%M %p")
    e20 = indicators.get("EMA20", {"value": "?", "signal": "?"})
    e50 = indicators.get("EMA50", {"value": "?", "signal": "?"})
    rsi = indicators.get("RSI(14)", {"value": "?", "signal": "?"})
    boll = indicators.get("Bollinger Bands", {"value": "?", "signal": "?"})
    trend = indicators.get("Trend", {"value": "?", "signal": "?"})

    msg = f"""📊 توصية التداول لزوج EUR/USD:

🔸 التوصية النهائية: {signal} {emoji_map.get(signal, '')}

━━━━━━━━━━━━━━

# أدوات المساعدة

def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f)

def get_analysis():
    return "Strong Sell"

def get_indicator_details():
    def safe_get(indicator):
        return indicator if indicator else {"value": "?", "signal": "?"}

    url = "https://www.investing.com/currencies/eur-usd-technical"
    headers = {"User-Agent": "Mozilla/5.0"}

    indicators = {
        "EMA20": None,
        "EMA50": None,
        "RSI(14)": None,
        "Bollinger Bands": None,
        "Trend": None
    }

    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table", class_="technicalIndicatorsTbl")
        rows = table.find_all("tr")[1:]
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                name = cols[0].text.strip()
                value = cols[1].text.strip()
                signal = cols[2].text.strip()
                if name in indicators:
                    indicators[name] = {"value": value, "signal": signal}
    except Exception as e:
        print("خطأ في جلب المؤشرات:", e)

    # تأكد من تعويض المؤشرات الناقصة
    return {
        "EMA20": safe_get(indicators.get("EMA20")),
        "EMA50": safe_get(indicators.get("EMA50")),
        "RSI(14)": safe_get(indicators.get("RSI(14)")),
        "Bollinger Bands": safe_get(indicators.get("Bollinger Bands")),
        "Trend": safe_get(indicators.get("Trend"))
    }

def explain_indicator(name, value, signal):
    try:
        val = float(value)
    except:
        return "🔍 لا يمكن تفسير القيمة."
    if "EMA" in name:
        if signal == "Buy":
            return "🔍 السعر أعلى من المتوسط → الاتجاه صاعد ✅"
        elif signal == "Sell":
            return "🔍 السعر أقل من المتوسط → الاتجاه هابط 🔻"
        else:
            return "🔍 قريب من المتوسط → سوق غير واضح ⏳"
    if "RSI" in name:
        if val < 30:
            return "🔍 RSI منخفض → تشبّع بيعي → احتمال صعود 🔼"
        elif val > 70:
            return "🔍 RSI مرتفع → تشبّع شرائي → احتمال هبوط 🔽"
        else:
            return "🔍 RSI طبيعي → لا ضغط حالياً 🔁"
    if "Bollinger" in name:
        if signal == "Buy":
            return "🔍 قريب من الحد السفلي → ارتداد صعودي محتمل 🔼"
        elif signal == "Sell":
            return "🔍 قريب من الحد العلوي → ضغط بيعي 🔽"
        else:
            return "🔍 داخل النطاق → لا ضغط حالي 🔍"
    return "🔍 لا يوجد تفسير."

def explain_trend(signal):
    if signal == "Buy":
        return "🔍 السوق في اتجاه صاعد حالياً ✅"
    elif signal == "Sell":
        return "🔍 السوق في اتجاه هابط حالياً 🔻"
    elif signal == "Neutral":
        return "🔍 لا يوجد اتجاه واضح (سوق متذبذب) ⏳"
    return "🔍 لا يمكن تفسير الاتجاه"

def get_recommendation_message(signal, indicators):
    emoji_map = {
        "Buy": "🟢", "Strong Buy": "🟢",
        "Sell": "🔴", "Strong Sell": "🔴",
        "Neutral": "🟡"
    }
    explain_map = {
        "Buy": "📈 المؤشرات تشير إلى اتجاه صاعد → شراء",
        "Strong Buy": "📈 المؤشرات بقوة لصالح الشراء",
        "Sell": "📉 المؤشرات تشير إلى هبوط → بيع",
        "Strong Sell": "📉 المؤشرات بقوة لصالح البيع",
        "Neutral": "⏳ السوق غير واضح → انتظار"
    }

    now = datetime.now().strftime("%I:%M %p")

    e20 = indicators.get("EMA20", {"value": "?", "signal": "?"})
    e50 = indicators.get("EMA50", {"value": "?", "signal": "?"})
    rsi = indicators.get("RSI(14)", {"value": "?", "signal": "?"})
    boll = indicators.get("Bollinger Bands", {"value": "?", "signal": "?"})
    trend = indicators.get("Trend", {"value": "?", "signal": "?"})

    msg = f"""📊 توصية التداول لزوج EUR/USD:

🔸 التوصية النهائية: {signal} {emoji_map.get(signal, '')}

━━━━━━━━━━━━━━

📈 المتوسطات المتحركة:
• EMA20 = {e20["value"]} → {e20["signal"]}
{explain_indicator("EMA20", e20["value"], e20["signal"])}

• EMA50 = {e50["value"]} → {e50["signal"]}
{explain_indicator("EMA50", e50["value"], e50["signal"])}

📊 مؤشر القوة النسبية (RSI 14):
• RSI = {rsi["value"]} → {rsi["signal"]}
{explain_indicator("RSI(14)", rsi["value"], rsi["signal"])}

📉 مؤشر بولينجر باند:
• Bollinger Bands = {boll["value"]} → {boll["signal"]}
{explain_indicator("Bollinger Bands", boll["value"], boll["signal"])}

📈 مؤشر الاتجاه (Trend):
• Trend = {trend["value"]} → {trend["signal"]}
{explain_trend(trend["signal"])}

━━━━━━━━━━━━━━

💡 خلاصة التحليل:
{explain_map.get(signal, 'لا يوجد تفسير.')}

📅 توقيت التوصية: {now}
"""
    return msg
# التوصيات التلقائية
def send_recommendations():
    while True:
        signal = get_analysis()
        indicators = get_indicator_details()
        message = get_recommendation_message(signal, indicators)
        users = load_users()
        for uid, info in users.items():
            if info.get("subscribed"):
                try:
                    bot.send_message(int(uid), message)
                except:
                    pass
        time.sleep(60)

threading.Thread(target=send_recommendations).start()

# أوامر التسجيل
@bot.message_handler(commands=["start"])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("إنشاء حساب", callback_data="register"))
    markup.add(types.InlineKeyboardButton("تسجيل الدخول", callback_data="login"))
    bot.send_message(message.chat.id, "👋 مرحبًا بك! اختر أحد الخيارات:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["register", "login"])
def handle_auth(call):
    user_id = call.from_user.id
    if call.data == "register":
        bot.send_message(user_id, "📝 أدخل اسمك:")
        bot.register_next_step_handler_by_chat_id(user_id, get_name)
    elif call.data == "login":
        bot.send_message(user_id, "📧 أدخل الإيميل:")
        bot.register_next_step_handler_by_chat_id(user_id, do_login)

def get_name(message):
    name = message.text
    bot.send_message(message.chat.id, "📧 أدخل الإيميل:")
    bot.register_next_step_handler(message, lambda m: get_email(m, name))

def get_email(message, name):
    email = message.text
    bot.send_message(message.chat.id, "🔐 أدخل كلمة المرور:")
    bot.register_next_step_handler(message, lambda m: finish_register(m, name, email))

def finish_register(message, name, email):
    password = message.text
    user_id = str(message.from_user.id)
    users = load_users()
    users[user_id] = {"name": name, "email": email, "password": password, "subscribed": False}
    save_users(users)
    bot.send_message(message.chat.id, "✅ تم إنشاء الحساب بنجاح.\nالرجاء الدفع لتفعيل الاشتراك.")
    send_subscription_info(message.chat.id)

def do_login(message):
    email = message.text
    bot.send_message(message.chat.id, "🔐 أدخل كلمة المرور:")
    bot.register_next_step_handler(message, lambda m: finish_login(m, email))

def finish_login(message, email):
    password = message.text
    user_id = str(message.from_user.id)
    users = load_users()
    for uid, info in users.items():
        if info["email"] == email and info["password"] == password:
            bot.send_message(message.chat.id, "✅ تم تسجيل الدخول.")
            if not info.get("subscribed"):
                send_subscription_info(message.chat.id)
            return
    bot.send_message(message.chat.id, "❌ فشل تسجيل الدخول.")

def send_subscription_info(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📤 تم الدفع، إرسال الإثبات", callback_data="wait_proof"))
    text = f"""💳 الاشتراك:
السعر: 3 USDT
المحفظة: {WALLET_ID}

📸 بعد الدفع، اضغط الزر أدناه وأرسل صورة الإثبات."""
    bot.send_message(chat_id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "wait_proof")
def ask_for_proof(call):
    bot.send_message(call.message.chat.id, "📷 أرسل صورة الإثبات:")
    bot.register_next_step_handler(call.message, receive_proof)

def receive_proof(message):
    if not message.photo:
        bot.send_message(message.chat.id, "❌ أرسل صورة فقط.")
        return
    user_id = str(message.from_user.id)
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    proof_path = f"pending/{user_id}.jpg"
    with open(proof_path, "wb") as f:
        f.write(downloaded_file)
    users = load_users()
    info = users.get(user_id, {})
    caption = f"🆕 طلب تفعيل:\nالاسم: {info.get('name', 'غير معروف')}\nالإيميل: {info.get('email', '')}\nID: {user_id}"
    bot.send_photo(ADMIN_ID, open(proof_path, "rb"), caption=caption)

# تشغيل البوت
bot.infinity_polling()
