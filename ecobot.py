import telebot
from telebot import types

TOKEN = "TOKEN"
bot = telebot.TeleBot(TOKEN)

tips = [
    "выключай свет когда выходишь",
    "не бери лишние пакеты в магазине",
    "пей воду из многоразовой бутылки",
    "если можешь, иди пешком вместо машины",
    "не лей воду пока чистишь зубы",
    "сортируй хотя бы пластик и бумагу"
]

facts = [
    "самый лучший мусор это тот который не появился",
    "экономия электричества = меньше выбросов",
    "одна бутылка многоразовая может заменить кучу одноразовых",
    "если покупаешь меньше лишнего, меньше упаковки летит в мусор"
]

challenges = [
    "день без одноразовых пакетов",
    "короткий душ (быстрее обычного)",
    "сегодня выключай свет всегда",
    "сегодня возьми с собой бутылку воды",
    "сегодня не бери лишние салфетки"
]

user_score = {}
user_i = {}

def kb():
    k = types.ReplyKeyboardMarkup(resize_keyboard=True)
    k.add("совет", "факт")
    k.add("челлендж", "сделал")
    k.add("счёт", "помощь")
    return k

def norm(t):
    return (t or "").strip().lower()

def get_i(uid):
    if uid not in user_i:
        user_i[uid] = {"t": 0, "f": 0, "c": 0, "has_ch": 0}
    return user_i[uid]

@bot.message_handler(commands=["start"])
def start(m):
    if m.from_user.id not in user_score:
        user_score[m.from_user.id] = 0
    bot.send_message(m.chat.id, "хай, я экобот. я не умный я тупица", reply_markup=kb())

@bot.message_handler(commands=["help"])
def help_cmd(m):
    bot.send_message(m.chat.id, "напиши: совет / факт / челлендж / сделал / счёт", reply_markup=kb())

@bot.message_handler(commands=["tip"])
@bot.message_handler(func=lambda m: norm(m.text) in ["совет", "🌿 совет"])
def tip(m):
    st = get_i(m.from_user.id)
    if st["t"] >= len(tips):
        st["t"] = 0
    bot.send_message(m.chat.id, "совет: " + tips[st["t"]])
    st["t"] += 1

@bot.message_handler(commands=["fact"])
@bot.message_handler(func=lambda m: norm(m.text) in ["факт", "📚 факт"])
def fact(m):
    st = get_i(m.from_user.id)
    if st["f"] >= len(facts):
        st["f"] = 0
    bot.send_message(m.chat.id, "факт: " + facts[st["f"]])
    st["f"] += 1

@bot.message_handler(commands=["challenge"])
@bot.message_handler(func=lambda m: norm(m.text) in ["челлендж", "🎯 челлендж"])
def challenge(m):
    st = get_i(m.from_user.id)
    if st["has_ch"] == 1:
        bot.send_message(m.chat.id, "ты уже взял челлендж. сначала напиши: сделал")
        return
    if st["c"] >= len(challenges):
        st["c"] = 0
    st["has_ch"] = 1
    st["cur"] = challenges[st["c"]]
    bot.send_message(m.chat.id, "твой челлендж: " + st["cur"])
    st["c"] += 1

@bot.message_handler(commands=["done"])
@bot.message_handler(func=lambda m: norm(m.text) in ["сделал", "✅ сделал"])
def done(m):
    uid = m.from_user.id
    if uid not in user_score:
        user_score[uid] = 0
    st = get_i(uid)
    if st["has_ch"] != 1:
        bot.send_message(m.chat.id, "ты ещё не брал челлендж. напиши: челлендж")
        return
    user_score[uid] += 3
    st["has_ch"] = 0
    bot.send_message(m.chat.id, "молодец. +3. теперь у тебя " + str(user_score[uid]) + " очков")

@bot.message_handler(commands=["score"])
@bot.message_handler(func=lambda m: norm(m.text) in ["счёт", "счет", "🏆 счёт"])
def score(m):
    uid = m.from_user.id
    if uid not in user_score:
        user_score[uid] = 0
    bot.send_message(m.chat.id, "у тебя " + str(user_score[uid]) + " очков")

@bot.message_handler(func=lambda m: norm(m.text) in ["помощь", "🆘 помощь"])
def help_btn(m):
    help_cmd(m)

@bot.message_handler(func=lambda m: True)
def other(m):
    bot.send_message(m.chat.id, "я не понял. напиши: совет / факт / челлендж / сделал / счёт", reply_markup=kb())


bot.infinity_polling()
