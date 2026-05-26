from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "ВСТАВЬ_СЮДА_СВОЙ_ТОКЕН"

questions = [
    {
        "text": "Что для вас страшнее?",
        "answers": {
            "Потерять человека": "abandonment",
            "Потерять себя": "distance"
        }
    },
    {
        "text": "Есть ли ощущение, что любовь нужно заслужить?",
        "answers": {
            "Да": "deserve",
            "Нет": "safe"
        }
    }
]

results = {
    "abandonment": "Похоже, у вас может проявляться сценарий покинутости.\n\nКанал Натальи Васильевой:\nt.me/natalyavassileva",

    "deserve": "Похоже, внутри есть сценарий «любовь нужно заслужить».\n\nКанал Натальи Васильевой:\nt.me/natalyavassileva",

    "distance": "Возможно, у вас есть страх потерять себя в отношениях.\n\nКанал Натальи Васильевой:\nt.me/natalyavassileva"
}

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users[update.effective_user.id] = {
        "step": 0,
        "scores": []
    }

    await ask_question(update, context)

async def ask_question(update, context):
    user = users[update.effective_user.id]
    step = user["step"]

    if step >= len(questions):
        await show_result(update, context)
        return

    q = questions[step]

    keyboard = [[a] for a in q["answers"].keys()]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        q["text"],
        reply_markup=markup
    )

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = users[update.effective_user.id]
    step = user["step"]

    q = questions[step]

    answer = update.message.text

    if answer in q["answers"]:
        user["scores"].append(q["answers"][answer])

    user["step"] += 1

    await ask_question(update, context)

async def show_result(update, context):
    user = users[update.effective_user.id]

    scores = user["scores"]

    if not scores:
        await update.message.reply_text("Не удалось определить сценарий.")
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8755186358:AAHJJ6J2tIJS6cFHqWua_WDFBZOqsAQH2tA"

questions = [
    {
        "text": "Что для вас страшнее?",
        "answers": {
            "Потерять человека": "abandonment",
            "Потерять себя": "distance"
        }
    },
    {
        "text": "Есть ли ощущение, что любовь нужно заслужить?",
        "answers": {
            "Да": "deserve",
            "Нет": "safe"
        }
    }
]

results = {
    "abandonment": "Похоже, у вас может проявляться сценарий покинутости.\n\nКанал Натальи Васильевой:\nt.me/natalyavassileva",

    "deserve": "Похоже, внутри есть сценарий «любовь нужно заслужить».\n\nКанал Натальи Васильевой:\nt.me/natalyavassileva",

    "distance": "Возможно, у вас есть страх потерять себя в отношениях.\n\nКанал Натальи Васильевой:\nt.me/natalyavassileva"
}

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users[update.effective_user.id] = {
        "step": 0,
        "scores": []
    }

    await ask_question(update, context)

async def ask_question(update, context):
    user = users[update.effective_user.id]
    step = user["step"]

    if step >= len(questions):
        await show_result(update, context)
        return

    q = questions[step]

    keyboard = [[a] for a in q["answers"].keys()]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        q["text"],
        reply_markup=markup
    )

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = users[update.effective_user.id]
    step = user["step"]

    q = questions[step]

    answer = update.message.text

    if answer in q["answers"]:
        user["scores"].append(q["answers"][answer])

    user["step"] += 1

    await ask_question(update, context)

async def show_result(update, context):
    user = users[update.effective_user.id]

    scores = user["scores"]

    if not scores:
        await update.message.reply_text("Не удалось определить сценарий.")
        return

    result = max(set(scores), key=scores.count)

    text = results.get(result, "Сценарий не найден.")

    await update.message.reply_text(text)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_answer))

print("Бот запущен")

app.run_polling()o

